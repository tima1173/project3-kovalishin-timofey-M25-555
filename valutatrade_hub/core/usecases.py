from datetime import datetime

from valutatrade_hub.core.models import User
from valutatrade_hub.core.utils import load_json, save_json


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


class PortfolioService:
    def show_portfolio(self, base_currency: str | None = None) -> None:
        pass

    def buy(self, currency: str, amount: float) -> None:
        pass

    def sell(self, currency: str, amount: float) -> None:
        pass


class RateService:
    def get_rate(self, from_currency: str, to_currency: str) -> None:
        pass
