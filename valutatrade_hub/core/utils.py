from datetime import datetime


def get_rate(from_currency: str, to_currency: str) -> dict:
    """
    Контракт получения курса.
    Возвращает словарь:
    {
        "rate": float,
        "updated_at": str (ISO)
    }
    """
    exchange_rates = {
        "EUR_USD": 1.1,
        "BTC_USD": 60000,
        "RUB_USD": 0.01,
        "ETH_USD": 3720,
        "USD_USD": 1,
    }

    pair = f"{from_currency}_{to_currency}"
    if pair not in exchange_rates:
        raise ValueError(f"Курс {pair} недоступен")

    return {
        "rate": exchange_rates[pair],
        "updated_at": datetime.now().isoformat(),
    }

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
