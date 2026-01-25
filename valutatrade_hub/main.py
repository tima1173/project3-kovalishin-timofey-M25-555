
from valutatrade_hub.core.usecases import RateService
import datetime

def main():
    rates = RateService()
    rate = rates.get_rate("BTC", "USD")
    
    print(rate)
    print(datetime.datetime.now(datetime.timezone.utc))


if __name__ == "__main__":
    main()
    
