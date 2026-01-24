import json
from pathlib import Path
from typing import Any

from valutatrade_hub.infra.settings import SettingsLoader


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = SettingsLoader()
        return cls._instance

    def _get_path(self, filename: str) -> Path:
        data_dir: Path = self._settings.get("DATA_DIR")
        return data_dir / filename

    def read(self, filename: str) -> Any:
        path = self._get_path(filename)
        if not path.exists():
            raise FileNotFoundError(f"Файл {filename} не найден")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, filename: str, data: Any) -> None:
        path = self._get_path(filename)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
