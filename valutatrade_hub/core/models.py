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

