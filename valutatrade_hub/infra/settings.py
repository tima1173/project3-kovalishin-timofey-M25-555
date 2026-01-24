from pathlib import Path
from typing import Any
import tomllib


class SettingsLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self) -> None:
        defaults = {
            "DATA_DIR": Path("data"),
            "RATES_TTL_SECONDS": 300,
            "DEFAULT_BASE_CURRENCY": "USD",
            "LOG_LEVEL": "INFO",
            "LOG_PATH": Path("logs/actions.log"),
        }

        config = {}
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            with pyproject_path.open("rb") as f:
                data = tomllib.load(f)
            config = (((data.get("tool") or {}).get("valutatrade")) or {})

        self._settings = defaults

        if "data_dir" in config:
            self._settings["DATA_DIR"] = Path(str(config["data_dir"]))
        if "rates_ttl_seconds" in config:
            self._settings["RATES_TTL_SECONDS"] = int(config["rates_ttl_seconds"])
        if "default_base_currency" in config:
            self._settings["DEFAULT_BASE_CURRENCY"] = str(config["default_base_currency"]).upper()
        if "log_level" in config:
            self._settings["LOG_LEVEL"] = str(config["log_level"]).upper()
        if "log_path" in config:
            self._settings["LOG_PATH"] = Path(str(config["log_path"]))


    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def reload(self) -> None:
        self._load()
