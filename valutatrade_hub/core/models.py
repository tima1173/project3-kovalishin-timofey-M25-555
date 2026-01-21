import hashlib
import secrets
from datetime import datetime


class User:
    def __init__(
        self,
        user_id: int,
        username: str,
        hashed_password: str,
        salt: str,
        registration_date: datetime,
    ) -> None:
        self._user_id = user_id
        self._username = username
        self._hashed_password = hashed_password
        self._salt = salt
        self._registration_date = registration_date

    # setters

    @property
    def user_id(self) -> int:
        return self._user_id


    @property
    def username(self) -> str:
        return self._username


    @username.setter
    def username(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._username = value.strip()


    @property
    def hashed_password(self) -> str:
        return self._hashed_password


    @property
    def salt(self) -> str:
        return self._salt


    @property
    def registration_date(self) -> datetime:
        return self._registration_date


    # methods

    def get_user_info(self) -> dict:
        return {
            "user_id": self._user_id,
            "username": self._username,
            "registration_date": self._registration_date.isoformat(),
        }


    def change_password(self, new_password: str) -> None:
        if not isinstance(new_password, str) or len(new_password) < 4:
            raise ValueError("Пароль должен быть не короче 4 символов")
        self._salt = secrets.token_hex(8)
        self._hashed_password = hashlib.sha256((new_password + self._salt).encode()).hexdigest()


    def verify_password(self, password: str) -> bool:
        if not isinstance(password, str):
            return False
        hashed = hashlib.sha256((password + self._salt).encode()).hexdigest()
        return hashed == self._hashed_password


class Wallet:
    def __init__(self, currency_code: str, balance: float = 0.0) -> None:
        self.currency_code = currency_code
        self.balance = balance

    @property
    def currency_code(self) -> str:
        return self._currency_code

    @currency_code.setter
    def currency_code(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("currency_code должен быть непустой строкой")
        self._currency_code = value.strip().upper()

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("balance должен быть числом")
        if value < 0:
            raise ValueError("balance не может быть отрицательным")
        self._balance = value

    def deposit(self, amount: float) -> None:
        if not isinstance(amount, (int, float)) or float(amount) <= 0:
            raise ValueError("'amount' должен быть положительным числом")
        self._balance += float(amount)

    def withdraw(self, amount: float) -> None:
        if not isinstance(amount, (int, float)) or float(amount) <= 0:
            raise ValueError("'amount' должен быть положительным числом")
        amount = float(amount)
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount

    def get_balance_info(self) -> str:
        return f"Баланс: {self._balance:.4f} {self._currency_code}"

