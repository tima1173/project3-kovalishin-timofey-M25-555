from valutatrade_hub.infra.database import DatabaseManager
from valutatrade_hub.infra.settings import SettingsLoader
from valutatrade_hub.core.currencies import get_currency
from valutatrade_hub.core.exceptions import (
    CurrencyNotFoundError,
    InsufficientFundsError,
    ApiRequestError,
)
from valutatrade_hub.decorators import log_action
from valutatrade_hub.core.models import User

import datetime
from datetime import datetime, timezone









class AuthService:
    def __init__(self):
        self.db = DatabaseManager()
        self.settings = SettingsLoader()
        self.current_user: User | None = None

    def register(self, username: str, password: str) -> None:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        if not isinstance(password, str) or len(password) < 4:
            raise ValueError("Пароль должен быть не короче 4 символов")

        users = self.db.read("users.json")

        for u in users:
            if u["username"] == username:
                raise ValueError(f"Имя пользователя '{username}' уже занято")

        next_id = max((u["user_id"] for u in users), default=0) + 1

        user = User(
            user_id=next_id,
            username=username,
            hashed_password="",
            salt="",
            registration_date=datetime.now(),
        )
        user.change_password(password)

        users.append({
            "user_id": user.user_id,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "salt": user.salt,
            "registration_date": user.registration_date.isoformat(),
        })

        self.db.write("users.json", users)

        portfolios = self.db.read("portfolios.json")
        portfolios.append({
            "user_id": next_id,
            "wallets": {}
        })
        self.db.write("portfolios.json", portfolios)

        print(
            f"Пользователь '{username}' зарегистрирован (id={next_id}). "
            f"Войдите: login --username {username} --password ****"
        )

    def login(self, username: str, password: str) -> None:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        if not isinstance(password, str):
            raise ValueError("Пароль обязателен")

        users = self.db.read("users.json")

        for data in users:
            if data["username"] == username:
                user = User(
                    user_id=data["user_id"],
                    username=data["username"],
                    hashed_password=data["hashed_password"],
                    salt=data["salt"],
                    registration_date=datetime.fromisoformat(
                        data["registration_date"]
                    ),
                )

                if not user.verify_password(password):
                    raise ValueError("Неверный пароль")

                self.current_user = user
                print(f"Вы вошли как '{username}'")
                return

        raise ValueError(f"Пользователь '{username}' не найден")

  


class PortfolioService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.db = DatabaseManager()
        self.settings = SettingsLoader()


    def show_portfolio(self, base_currency: str = "USD") -> dict:
        user = self.auth_service.current_user
        if not user:
            raise ValueError("Сначала выполните login")

        base = get_currency(base_currency)

        portfolios = self.db.read("portfolios.json")

        for p in portfolios:
            if p["user_id"] == user.user_id:
                wallets = p.get("wallets", {})
                if not wallets:
                    return {
                        "user": user.username,
                        "base": base.code,
                        "items": [],
                        "total": 0.0,
                    }

                rates = self.db.read("rates.json")

                result = []
                total = 0.0

                for code, data in wallets.items():
                    currency = get_currency(code)
                    balance = float(data.get("balance", 0.0))

                    if currency.code == base.code:
                        value = balance
                    else:
                        pair = f"{currency.code}_{base.code}"
                        if pair not in rates:
                            raise ApiRequestError(f"Курс {pair} недоступен")
                        rate = rates[pair]["rate"]
                        value = balance * float(rate)

                    total += value
                    result.append({
                        "currency": currency.code,
                        "balance": balance,
                        "value": value,
                    })

                return {
                    "user": user.username,
                    "base": base.code,
                    "items": result,
                    "total": total,
                }

        raise ValueError("Портфель пользователя не найден")




    @log_action("BUY")
    def buy(self, currency: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("'amount' должен быть положительным числом")

        cur = get_currency(currency)

        user = self.auth_service.current_user
        if not user:
            raise ValueError("Сначала выполните login")

        portfolios = self.db.read("portfolios.json")

        for p in portfolios:
            if p["user_id"] == user.user_id:
                wallets = p.setdefault("wallets", {})
                w = wallets.setdefault(cur.code, {"balance": 0.0})
                w["balance"] += amount
                self.db.write("portfolios.json", portfolios)
                return

        raise ValueError("Портфель пользователя не найден")
    
    

    @log_action("SELL")
    def sell(self, currency: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("'amount' должен быть положительным числом")

        cur = get_currency(currency)

        user = self.auth_service.current_user
        if not user:
            raise ValueError("Сначала выполните login")

        portfolios = self.db.read("portfolios.json")

        for p in portfolios:
            if p["user_id"] == user.user_id:
                wallets = p.get("wallets", {})
                if cur.code not in wallets:
                    raise CurrencyNotFoundError(cur.code)

                balance = wallets[cur.code].get("balance", 0.0)
                if amount > balance:
                    raise InsufficientFundsError(balance, amount, cur.code)

                wallets[cur.code]["balance"] -= amount
                self.db.write("portfolios.json", portfolios)
                return

        raise ValueError("Портфель пользователя не найден")




class RateService:
    def __init__(self):
        self.db = DatabaseManager()
        self.settings = SettingsLoader()


    def get_rate(self, from_currency: str, to_currency: str) -> dict:
        src = get_currency(from_currency)
        dst = get_currency(to_currency)

        rates = self.db.read("rates.json")
        key = f"{src.code}_{dst.code}"

        if key not in rates:
            raise ApiRequestError(f"Курс {key} недоступен")

        entry = rates[key]
        updated_at = datetime.fromisoformat(entry["updated_at"]).replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)

        ttl = int(self.settings.get("RATES_TTL_SECONDS", 300))
        age_seconds = (now - updated_at).total_seconds()

        if age_seconds > ttl:
            raise ApiRequestError(f"Курс {key} устарел")

        return {
            "rate": entry["rate"],
            "updated_at": entry["updated_at"],
        }


