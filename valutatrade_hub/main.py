from valutatrade_hub.core.currencies import get_currency

def main():
    print(get_currency("rub").get_display_info())
    print(get_currency("sdf").get_display_info())



