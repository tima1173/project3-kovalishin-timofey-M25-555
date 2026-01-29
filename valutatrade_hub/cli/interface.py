import shlex

from prettytable import PrettyTable
from valutatrade_hub.core.usecases import AuthService, PortfolioService, RateService
from valutatrade_hub.core.exceptions import (
    CurrencyNotFoundError,
    InsufficientFundsError,
    ApiRequestError,
)
from valutatrade_hub.parser_service.config import ParserConfig
from valutatrade_hub.parser_service.api_clients import CoinGeckoClient, ExchangeRateApiClient
from valutatrade_hub.parser_service.storage import RatesStorage
from valutatrade_hub.parser_service.updater import RatesUpdater
from valutatrade_hub.infra.database import DatabaseManager


def parse_args(parts: list[str]) -> dict:
    args = {}
    it = iter(parts)
    for p in it:
        if p.startswith("--"):
            key = p[2:]
            args[key] = next(it, None)
    return args


def handle_error(exc: Exception) -> None:
    if isinstance(exc, InsufficientFundsError):
        print(str(exc))
    elif isinstance(exc, CurrencyNotFoundError):
        print(str(exc))
        print("Валюта не распознана. Используйте: get-rate --from <CODE> --to <CODE>")
    elif isinstance(exc, ApiRequestError):
        print(str(exc))
        print("Повторите попытку позже.")
    elif isinstance(exc, ValueError):
        print(str(exc))
    else:   
        print("Неизвестная ошибка.")


def print_help() -> None:
    print(
        """
\nДоступные команды:
====================================
- register --username <name> --password <password> - регистрация
- login --username <name> --password <password> - вход
- show-portfolio [--base <CODE>] - показать портфель
- buy --currency <CODE> --amount <amount> - купить валюту
- sell --currency <CODE> --amount <amount> - продать валюту
- get-rate --from <CODE> --to <CODE> - получить курс
- update-rates [--source <coingecko|exchangerate>] - обновить актуальные курсы
- show-rates [--currency <CODE>] [--top <N>] [--base <CODE>] - показать курсы
- exit - завершить программу
- help - показать это сообщение
====================================

"""
    )


def run_cli() -> None:
    auth = AuthService()
    portfolio = PortfolioService(auth)
    rates = RateService()

    print("\nПлатформа запущена!")
    print_help()

    while True:
        try:
            raw = input("> ").strip()
            if not raw:
                continue

            parts = shlex.split(raw)
            command = parts[0]
            args = parse_args(parts[1:])

            match command:
                case "exit":
                    print("\nПрограмма завершается...")
                    break

                case "register":
                    username = args.get("username")
                    password = args.get("password")

                    if not username or not password:
                        print("Использование: register --username <name> --password <password>")
                        continue

                    auth.register(username, password)


                case "login":
                    username = args.get("username")
                    password = args.get("password")

                    if not username or not password:
                        print("Использование: login --username <name> --password <password>")
                        continue

                    auth.login(username, password)


                case "show-portfolio":
                    base = args.get("base", "USD")

                    data = portfolio.show_portfolio(base)

                    table = PrettyTable()
                    table.field_names = ["Currency", "Balance", f"Value ({base})"]

                    for item in data["items"]:
                        table.add_row([
                            item["currency"],
                            f"{item['balance']:.4f}",
                            f"{item['value']:.2f}",
                        ])

                    print(f"\nПортфель пользователя '{data['user']}' (база: {base})")
                    if data["items"]:
                        print(table)
                        print("-" * 40)
                        print(f"ИТОГО: {data['total']:.2f} {base}")
                    else:
                        print("Портфель пуст")


                case "buy":
                    currency = args.get("currency")
                    amount = args.get("amount")

                    if not currency or not amount:
                        print("Использование: buy --currency <CODE> --amount <FLOAT>")
                        continue

                    portfolio.buy(currency, float(amount))
                    print(f"Покупка выполнена: {amount} {currency.upper()}")

                case "sell":
                    currency = args.get("currency")
                    amount = args.get("amount")

                    if not currency or not amount:
                        print("Использование: sell --currency <CODE> --amount <FLOAT>")
                        continue

                    portfolio.sell(currency, float(amount))
                    print(f"Продажа выполнена: {amount} {currency.upper()}")


                case "get-rate":
                    src = args.get("from")
                    dst = args.get("to")

                    if not src or not dst:
                        print("Использование: get-rate --from <CODE> --to <CODE>")
                        continue

                    data = rates.get_rate(src, dst)

                    print(
                        f"Курс {src.upper()}→{dst.upper()}: "
                        f"{data['rate']} (обновлено: {data['updated_at']})"
                    )

                case "update-rates":
                    source = args.get("source")

                    if source is not None and source not in ("coingecko", "exchangerate"):
                        print("Источник должен быть 'coingecko' или 'exchangerate'")
                        continue

                    updater = RatesUpdater.build_rates_updater(source)
                    result = updater.run_update()

                    print(
                        f"Update successful. Total rates updated: {result['updated']}. "
                        f"Last refresh: {result['last_refresh']}"
                    )

                case "show-rates":
                    data = DatabaseManager().read("rates.json")
                    pairs = data.get("pairs", {})
                    if not pairs:
                        print("Локальный кеш курсов пуст. Выполните 'update-rates'.")
                        continue

                    base = args.get("base", None)
                    currency = args.get("currency", None)
                    top = args.get("top", None)

                    rows = []
                    for pair, entry in pairs.items():
                        frm, to = pair.split("_")

                        if currency and frm != currency and to != currency:
                            continue

                        if base and to != base:
                            continue

                        rows.append((pair, entry["rate"], entry["updated_at"], entry["source"]))

                    if not rows:
                        print("Курсы по заданным фильтрам не найдены.")
                        continue

                    if top:
                        try:
                            n = int(top)
                            rows.sort(key=lambda r: r[1], reverse=True)
                            rows = rows[:n]
                        except ValueError:
                            print("'top' должен быть числом")
                            continue

                    print(f"Rates from cache (updated at {data.get('last_refresh')}):")
                    for pair, rate, updated_at, source in rows:
                        print(f"- {pair}: {rate} (updated: {updated_at}, source: {source})")


                case "help":
                    print_help()

                case _:
                    print(f"Неизвестная команда '{command}' введите 'help'.")

        except Exception as e:
            handle_error(e)
