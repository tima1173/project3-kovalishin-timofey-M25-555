from abc import ABC, abstractmethod
from valutatrade_hub.core.exceptions import CurrencyNotFoundError


class Currency(ABC):
    def __init__(self, name: str, code: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name должен быть непустой строкой")
        if (
            not isinstance(code, str)
            or not code.isupper()
            or not (2 <= len(code) <= 5)
            or " " in code
        ):
            raise ValueError("code должен быть в верхнем регистре, 2–5 символов, без пробелов")

        self.name = name
        self.code = code

    @abstractmethod
    def get_display_info(self) -> str:
        pass


class FiatCurrency(Currency):
    def __init__(self, name: str, code: str, issuing_country: str) -> None:
        super().__init__(name, code)
        if not isinstance(issuing_country, str) or not issuing_country.strip():
            raise ValueError("issuing_country должен быть непустой строкой")
        self.issuing_country = issuing_country

    def get_display_info(self) -> str:
        return f"[FIAT] {self.code} — {self.name} (Issuing: {self.issuing_country})"


class CryptoCurrency(Currency):
    def __init__(self, name: str, code: str, algorithm: str, market_cap: float) -> None:
        super().__init__(name, code)
        if not isinstance(algorithm, str) or not algorithm.strip():
            raise ValueError("algorithm должен быть непустой строкой")
        if not isinstance(market_cap, (int, float)) or market_cap <= 0:
            raise ValueError("market_cap должен быть положительным числом")

        self.algorithm = algorithm
        self.market_cap = float(market_cap)

    def get_display_info(self) -> str:
        return (
            f"[CRYPTO] {self.code} — {self.name} "
            f"(Algo: {self.algorithm}, MCAP: {self.market_cap:.2e})"
        )




_CURRENCY_REGISTRY = {
    "USD": FiatCurrency("US Dollar", "USD", "United States"),
    "EUR": FiatCurrency("Euro", "EUR", "Eurozone"),
    "RUB": FiatCurrency("Russian Ruble", "RUB", "Russia"),
    "BTC": CryptoCurrency("Bitcoin", "BTC", "SHA-256", 3_075_031_224_952),
    "ETH": CryptoCurrency("Ethereum", "ETH", "Ethash", 351_005_166_082),
    "SOL": CryptoCurrency("Solana", "SOL", "Proof of History", 70_302_875_011),
} 





def get_currency(code: str) -> Currency:
    if not isinstance(code, str):
        raise CurrencyNotFoundError(str(code))

    key = code.strip().upper()
    currency = _CURRENCY_REGISTRY.get(key)
    if currency is None:
        raise CurrencyNotFoundError(key)

    return currency
