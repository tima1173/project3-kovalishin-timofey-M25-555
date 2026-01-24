from datetime import datetime

from valutatrade_hub.core.models import User, Portfolio, Wallet
from valutatrade_hub.core.utils import (
    load_json, require_login, save_json, get_rate, validate_amount 
)
from valutatrade_hub.core.utils import get_rate as _get_rate, validate_currency_code



class AuthService:
    def register(self, username: str, password: str) -> None:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        if not isinstance(password, str) or len(password) < 4:
            raise ValueError("Пароль должен быть не короче 4 символов")

        users = load_json("users.json")

        for u in users:
            if u["username"] == username:
                raise ValueError(f"Имя пользователя '{username}' уже занято")

        next_id = max((u["user_id"] for u in users), default=0) + 1

        user = User(
            user_id=next_id,
            username=username,
            hashed_password="",
            salt="",
            registration_date=datetime.utcnow(),
        )
        user.change_password(password)

        users.append({
            "user_id": user.user_id,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "salt": user.salt,
            "registration_date": user.registration_date.isoformat(),
        })

        save_json("users.json", users)

        portfolios = load_json("portfolios.json")
        portfolios.append({
            "user_id": next_id,
            "wallets": {}
        })
        save_json("portfolios.json", portfolios)

        print(
            f"Пользователь '{username}' зарегистрирован (id={next_id}). "
            f"Войдите: login --username {username} --password ****"
        )

    def login(self, username: str, password: str) -> None:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        if not isinstance(password, str):
            raise ValueError("Пароль обязателен")

        users = load_json("users.json")

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

    def show_portfolio(self, base_currency: str | None = None) -> None:
        require_login(self.auth_service.current_user)

        base = (base_currency or "USD").upper()
        user_id = self.auth_service.current_user.user_id

        portfolios = load_json("portfolios.json")

        for p in portfolios:
            if p["user_id"] == user_id:
                wallets = p.get("wallets", {})
                if not wallets:
                    print("Портфель пуст")
                    return

                print(
                    f"Портфель пользователя '{self.auth_service.current_user.username}' "
                    f"(база: {base}):"
                )

                total = 0.0
                for code, data in wallets.items():
                    balance = data["balance"]

                    if code == base:
                        value = balance
                    else:
                        rate = get_rate(code, base)["rate"]
                        value = balance * rate

                    total += value
                    print(f"- {code}: {balance:.4f} → {value:.2f} {base}")

                print("-" * 33)
                print(f"ИТОГО: {total:.2f} {base}")
                return

        print("Портфель пользователя не найден")



    def buy(self, currency: str, amount: float) -> None:
        require_login(self.auth_service.current_user)

        code = validate_currency_code(currency)
        validate_amount(amount)

        user_id = self.auth_service.current_user.user_id
        portfolios = load_json("portfolios.json")

        for p in portfolios:
            if p["user_id"] == user_id:
                wallets = p.setdefault("wallets", {})

                wallet = wallets.setdefault(code, {"balance": 0.0})
                wallet["balance"] += amount

                save_json("portfolios.json", portfolios)

                print(f"Покупка выполнена: {amount:.4f} {code}")
                print(f"- {code}: {wallet['balance']:.4f}")
                return

        raise ValueError("Портфель пользователя не найден")



    def sell(self, currency: str, amount: float) -> None:
        require_login(self.auth_service.current_user)

        code = validate_currency_code(currency)
        validate_amount(amount)

        user_id = self.auth_service.current_user.user_id
        portfolios = load_json("portfolios.json")

        for p in portfolios:
            if p["user_id"] == user_id:
                wallets = p.get("wallets", {})

                if code not in wallets:
                    raise ValueError(
                        f"У вас нет кошелька '{code}'. "
                        f"Добавьте валюту: она создаётся автоматически при первой покупке."
                    )

                wallet = wallets[code]
                balance = wallet.get("balance", 0.0)

                if amount > balance:
                    raise ValueError(
                        f"Недостаточно средств: доступно {balance:.4f} {code}, "
                        f"требуется {amount:.4f} {code}"
                    )
                
                wallet["balance"] -= amount

                save_json("portfolios.json", portfolios)

                print(f"Продажа выполнена: {amount:.4f} {code}")
                print(f"- {code}: было {balance:.4f} → стало {wallet['balance']:.4f}")
                return

        raise ValueError("Портфель пользователя не найден")



class RateService:
    def get_rate(self, from_currency: str, to_currency: str) -> None:
        src = validate_currency_code(from_currency)
        dst = validate_currency_code(to_currency)

        info = _get_rate(src, dst)

        rate = info["rate"]
        updated_at = info["updated_at"]

        print(f"Курс {src}→{dst}: {rate}")
        print(f"Обновлено: {updated_at}")


