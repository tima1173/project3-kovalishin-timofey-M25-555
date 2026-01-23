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
    ):
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
    def __init__(self, currency_code: str, balance: float = 0.0):
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


class Portfolio:
    def __init__(self, user_id: int):
        self._user_id = int(user_id)
        self._wallets = {}

    @property
    def user(self) -> int:
        return self._user_id

    @property
    def wallets(self) -> dict:
        return self._wallets.copy()

    def add_currency(self, currency_code: str):
        code = str(currency_code).strip().upper()
        if not code:
            raise ValueError("currency_code должен быть непустой строкой")
        if code in self._wallets:
            raise ValueError("Код валюты должен быть уникален")
        self._wallets[code] = Wallet(currency_code=code, balance=0.0)

    def get_wallet(self, currency_code: str) -> Wallet | None:
        code = str(currency_code).strip().upper()
        return self._wallets.get(code)

    def get_total_value(self, base_currency: str = "USD") -> float:
        exchange_rates = {
            "USD_USD": 1,
            "EUR_USD": 1.1,
            "BTC_USD": 60000,
            "ETH_USD": 3720,
            "RUB_USD": 0.01,
        }

        base = str(base_currency).strip().upper()
        if not base:
            raise ValueError("base_currency должен быть непустой строкой")

        total = 0.0
        for code, wallet in self._wallets.items():
            if code == base:
                total += wallet.balance
                continue

            pair = f"{code}_{base}"
            rate = exchange_rates.get(pair)
            if not rate:
                raise ValueError(f"Не удалось получить курс для {code}→{base}")

            total += wallet.balance * float(rate)

        return total
