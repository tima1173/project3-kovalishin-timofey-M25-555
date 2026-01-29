# ValutaTrade Hub

## Описание

ValutaTrade Hub - это консольное приложение для управления валютным портфелем и отслеживания курсов валют. Приложение позволяет пользователям регистрироваться, входить в систему, покупать и продавать валюты, а также просматривать актуальные курсы обмена.

## Установка и запуск

### Требования

- Python 3.13 или выше
- Poetry для управления зависимостями

### Установка Poetry

Если у вас еще не установлен Poetry, следуйте инструкциям на [официальном сайте Poetry](https://python-poetry.org/docs/#installation).

### Настройка API ключа ExchangeRate

Для получения курсов фиатных валют через API exchangerate, необходимо зарегистрироваться на [exchangerate-api.com](https://www.exchangerate-api.com/) и получить бесплатный API ключ.

После получения ключа, установите его как переменную окружения:

**Windows (cmd):**
```bash
set EXCHANGERATE_API_KEY="ваш_ключ_здесь"
```

**Windows (PowerShell):**
```powershell
$env:EXCHANGERATE_API_KEY="ваш_ключ_здесь"
```

**Linux/macOS:**
```bash
export EXCHANGERATE_API_KEY=ваш_ключ_здесь
```

### Установка зависимостей

Для установки всех необходимых зависимостей выполните:

```bash
poetry install
```

### Запуск приложения

После установки зависимостей вы можете запустить приложение с помощью одной из следующих команд:

```bash
poetry run project
```

Или используя Makefile:

```bash
make project
```

## Доступные команды

После запуска приложения вы увидите список доступных команд:

- `register --username <name> --password <password>` - регистрация нового пользователя
- `login --username <name> --password <password>` - вход в систему
- `show-portfolio [--base <CODE>]` - показать портфель пользователя
- `buy --currency <CODE> --amount <amount>` - купить валюту
- `sell --currency <CODE> --amount <amount>` - продать валюту
- `get-rate --from <CODE> --to <CODE>` - получить курс обмена между двумя валютами
- `update-rates [--source <coingecko|exchangerate>]` - обновить актуальные курсы валют
- `show-rates [--currency <CODE>] [--top <N>] [--base <CODE>]` - показать курсы валют с фильтрацией
- `exit` - завершить программу
- `help` - показать справку по командам


## Структура проекта

```
project3-kovalishin-timofey-M25-555/
├── README.md                    # Документация проекта
├── pyproject.toml               # Конфигурация проекта и зависимостей (Poetry)
├── Makefile                     # Скрипты для автоматизации (запуск, тесты)
├── data/                        # Директория с данными приложения
│   ├── users.json               # Хранение данных пользователей
│   ├── portfolios.json          # Хранение данных портфелей пользователей
│   ├── rates.json               # Кэш актуальных курсов валют
│   └── exchange_rates.json       # История обновлений курсов
└── valutatrade_hub/             # Основной пакет приложения
    ├── __init__.py              # Инициализация пакета
    ├── main.py                  # Точка входа в приложение
    ├── logging_config.py         # Настройка логирования
    ├── decorators.py           # Декораторы (например, для логирования действий)
    ├── core/                    # Бизнес-логика приложения
    │   ├── __init__.py
    │   ├── models.py            # Модели данных (пользователь, кошелек, портфель)
    │   ├── currencies.py        # Определения валют (фиатные, криптовалюты)
    │   ├── exceptions.py        # Пользовательские исключения
    │   └── usecases.py          # Сценарии использования (регистрация, покупка/продажа валют и т.д.)
    ├── cli/                     # Компоненты интерфейса командной строки
    │   ├── __init__.py
    │   └── interface.py          # Парсинг команд, взаимодействие с пользователем
    ├── infra/                   # Инфраструктурные компоненты
    │   ├── __init__.py
    │   ├── database.py         # Менеджер для работы с JSON-файлами
    │   └── settings.py          # Загрузчик настроек из pyproject.toml
    └── parser_service/          # Сервис получения курсов валют
        ├── __init__.py
        ├── config.py           # Конфигурация API-клиентов
        ├── api_clients.py       # Клиенты для внешних API (CoinGecko, ExchangeRate)
        ├── storage.py          # Хранилище курсов (чтение/запись файлов)
        └── updater.py         # Обновление курсов через API
```

## Asciinema
[Ссылка на запись](https://asciinema.org/a/0ACGbWs6Rw77Fwak)
