
from valutatrade_hub.cli.interface import run_cli

from valutatrade_hub.parser_service.config import ParserConfig
from valutatrade_hub.parser_service.api_clients import CoinGeckoClient

def main():


    cfg = ParserConfig()
    client = CoinGeckoClient(cfg)
    print(client.fetch_rates())



if __name__ == "__main__":
    main()
    
