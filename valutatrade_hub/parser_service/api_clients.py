from abc import ABC, abstractmethod
from typing import Dict

import requests

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.parser_service.config import ParserConfig


class BaseApiClient(ABC):
    def __init__(self, config: ParserConfig):
        self.config = config

    @abstractmethod
    def fetch_rates(self) -> Dict[str, float]:
        raise NotImplementedError


class CoinGeckoClient(BaseApiClient):
    def fetch_rates(self) -> Dict[str, float]:
        ids = ",".join(self.config.CRYPTO_ID_MAP.values())
        params = {
            "ids": ids,
            "vs_currencies": self.config.BASE_CURRENCY.lower(),
        }

        try:
            response = requests.get(
                self.config.COINGECKO_URL,
                params=params,
                timeout=self.config.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ApiRequestError(f"CoinGecko error: {e}")

        rates: Dict[str, float] = {}

        for code, coin_id in self.config.CRYPTO_ID_MAP.items():
            try:
                rate = data[coin_id][self.config.BASE_CURRENCY.lower()]
                pair = f"{code}_{self.config.BASE_CURRENCY}"
                rates[pair] = float(rate)
            except (KeyError, TypeError):
                continue

        return rates


class ExchangeRateApiClient(BaseApiClient):
    def fetch_rates(self):
        if not self.config.EXCHANGERATE_API_KEY:
            raise ApiRequestError("ExchangeRate API key not configured")

        url = (
            f"{self.config.EXCHANGERATE_API_URL}/"
            f"{self.config.EXCHANGERATE_API_KEY}/latest/"
            f"{self.config.BASE_CURRENCY}"
        )

        try:
            response = requests.get(url, timeout=self.config.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ApiRequestError(f"ExchangeRate-API error: {e}")

        if data.get("result") != "success":
            raise ApiRequestError("ExchangeRate-API returned non-success result")

        conversion_rates = data.get("conversion_rates", {})
        if not isinstance(conversion_rates, dict):
            raise ApiRequestError("ExchangeRate-API malformed response")

        base = self.config.BASE_CURRENCY
        rates = {}

        for code in self.config.FIAT_CURRENCIES:
            if code == base:
                continue
            try:
                base_to_code = float(conversion_rates[code])  
                rates[f"{code}_{base}"] = 1 / base_to_code  
            except (KeyError, TypeError, ZeroDivisionError, ValueError):
                continue

        return rates




