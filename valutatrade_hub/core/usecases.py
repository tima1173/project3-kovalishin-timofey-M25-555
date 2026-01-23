class AuthService:
    def register(self, username: str, password: str) -> None:
        pass

    def login(self, username: str, password: str) -> None:
        pass


class PortfolioService:
    def show_portfolio(self, base_currency: str | None = None) -> None:
        pass

    def buy(self, currency: str, amount: float) -> None:
        pass

    def sell(self, currency: str, amount: float) -> None:
        pass


class RateService:
    def get_rate(self, from_currency: str, to_currency: str) -> None:
        pass
