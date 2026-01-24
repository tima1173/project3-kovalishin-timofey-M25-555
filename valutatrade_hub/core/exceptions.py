class CurrencyNotFoundError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(f"Неизвестная валюта '{code}'")
        self.code = code
