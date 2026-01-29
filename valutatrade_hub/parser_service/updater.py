from datetime import datetime, timezone

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.parser_service.api_clients import BaseApiClient
from valutatrade_hub.parser_service.storage import RatesStorage

from valutatrade_hub.parser_service.api_clients import (
    CoinGeckoClient,
    ExchangeRateApiClient,
)
from valutatrade_hub.parser_service.config import ParserConfig

class RatesUpdater:
    def __init__(self, clients: list, storage: RatesStorage):
        self.clients = clients
        self.storage = storage

    def run_update(self) -> dict:
        all_rates = {}
        history_records = []

        now = datetime.now(timezone.utc).isoformat()

        for client in self.clients:
            try:
                rates = client.fetch_rates()
            except ApiRequestError as e:
                print(f"[ERROR] {e}")
                continue

            source_name = client.__class__.__name__

            for pair, rate in rates.items():
                history_records.append(
                    {
                        "id": f"{pair}_{now}",
                        "from_currency": pair.split("_")[0],
                        "to_currency": pair.split("_")[1],
                        "rate": rate,
                        "timestamp": now,
                        "source": source_name,
                    }
                )

                all_rates[pair] = {
                    "rate": rate,
                    "updated_at": now,
                    "source": source_name,
                }

        if all_rates:
            self.storage.write_snapshot(all_rates)
            self.storage.append_history(history_records)

        return {
            "updated": len(all_rates),
            "last_refresh": now,
        }
    
    @staticmethod
    def build_rates_updater(source: str | None):
        cfg = ParserConfig()
        storage = RatesStorage(cfg.RATES_FILE_PATH, cfg.HISTORY_FILE_PATH)

        clients = []

        if source in (None, "coingecko"):
            clients.append(CoinGeckoClient(cfg))

        if source in (None, "exchangerate"):
            clients.append(ExchangeRateApiClient(cfg))

        return RatesUpdater(clients, storage)
