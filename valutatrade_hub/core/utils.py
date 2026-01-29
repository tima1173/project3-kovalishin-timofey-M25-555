'''from datetime import datetime
import json
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")


def get_rate(from_currency: str, to_currency: str) -> dict:
    exchange_rates = {
        "EUR_USD": 1.1,
        "BTC_USD": 60000,
        "RUB_USD": 0.01,
        "ETH_USD": 3720,
        "USD_USD": 1,
    }

    pair = f"{from_currency}_{to_currency}"
    if pair in exchange_rates:
        return {
            "rate": exchange_rates[pair],
            "updated_at": datetime.now().isoformat(),
        }

    reverse_pair = f"{to_currency}_{from_currency}"
    if reverse_pair in exchange_rates:
        return {
            "rate": 1 / exchange_rates[reverse_pair],
            "updated_at": datetime.now().isoformat(),
        }

    raise ValueError(f"Курс {pair} недоступен")


def validate_amount(amount: float) -> None:
    if not isinstance(amount, (int, float)) or float(amount) <= 0:
        raise ValueError("'amount' должен быть положительным числом")


def validate_currency_code(currency_code: str) -> str:
    if not isinstance(currency_code, str) or not currency_code.strip():
        raise ValueError("currency_code должен быть непустой строкой")
    return currency_code.strip().upper()


def require_login(current_user) -> None:
    if current_user is None:
        raise PermissionError("Сначала выполните login")

def load_json(filename: str) -> Any:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Файл {filename} не найден")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename: str, data: Any) -> None:
    path = DATA_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
'''