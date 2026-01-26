
from valutatrade_hub.cli.interface import run_cli

'''
from valutatrade_hub.parser_service.config import ParserConfig
from valutatrade_hub.parser_service.api_clients import CoinGeckoClient
from valutatrade_hub.parser_service.storage import RatesStorage
from valutatrade_hub.parser_service.updater import RatesUpdater'''
def main():
    '''
    cfg = ParserConfig()

    clients = [
        CoinGeckoClient(cfg),
    ]

    storage = RatesStorage(cfg.RATES_FILE_PATH, cfg.HISTORY_FILE_PATH)
    updater = RatesUpdater(clients, storage)

    result = updater.run_update()
    print(result)
    '''

    run_cli()


if __name__ == "__main__":
    main()
    
