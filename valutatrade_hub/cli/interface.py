from valutatrade_hub.core.usecases import *

auth_service = AuthService()
portfolio_service = PortfolioService(auth_service)
rate_service = RateService()


def main():
    print("CLI started")
    cmd_login({"username": "alice", "password": "1234"})
    cmd_buy({"currency": "BTC", "amount": 0.05})
    cmd_show_portfolio({})






def cmd_register(args: dict) -> None:
    try:
        auth_service.register(
            username=args.get("username"),
            password=args.get("password"),
        )
    except Exception as e:
        print(e)


def cmd_login(args: dict) -> None:
    try:
        auth_service.login(
            username=args.get("username"),
            password=args.get("password"),
        )
    except Exception as e:
        print(e)



def cmd_show_portfolio(args: dict) -> None:
    try:
        portfolio_service.show_portfolio(
            base_currency=args.get("base"),
        )
    except Exception as e:
        print(e)



def cmd_buy(args: dict) -> None:
    try:
        portfolio_service.buy(
            currency=args.get("currency"),
            amount=args.get("amount"),
        )
    except Exception as e:
        print(e)



def cmd_sell(args: dict) -> None:
    portfolio_service.sell(
        currency=args.get("currency"),
        amount=args.get("amount"),
    )


def cmd_get_rate(args: dict) -> None:
    rate_service.get_rate(
        from_currency=args.get("from"),
        to_currency=args.get("to"),
    )
