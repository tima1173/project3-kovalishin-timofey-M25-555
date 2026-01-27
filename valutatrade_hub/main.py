
from valutatrade_hub.cli.interface import run_cli


from valutatrade_hub.parser_service.config import ParserConfig
from valutatrade_hub.parser_service.api_clients import ExchangeRateApiClient, CoinGeckoClient
from valutatrade_hub.parser_service.updater import RatesUpdater
from valutatrade_hub.parser_service.storage import RatesStorage


def main():

    run_cli()


if __name__ == "__main__":
    main()
    
