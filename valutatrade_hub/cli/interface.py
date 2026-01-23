from valutatrade_hub.core.usecases import *

auth_service = AuthService()
portfolio_service = PortfolioService()
rate_service = RateService()


def main():
    print("CLI started")
    auth_service.register("alice", "1234")



def cmd_register(args: dict) -> None:
    auth_service.register(
        username=args.get("username"),
        password=args.get("password"),
    )


def cmd_login(args: dict) -> None:
    auth_service.login(
        username=args.get("username"),
        password=args.get("password"),
    )


def cmd_show_portfolio(args: dict) -> None:
    portfolio_service.show_portfolio(
        base_currency=args.get("base"),
    )


def cmd_buy(args: dict) -> None:
    portfolio_service.buy(
        currency=args.get("currency"),
        amount=args.get("amount"),
    )


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
