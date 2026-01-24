import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from valutatrade_hub.infra.settings import SettingsLoader




def setup_logging():
    settings = SettingsLoader()
    log_level = settings.get("LOG_LEVEL", "INFO")
    log_path: Path = settings.get("LOG_PATH")

    log_path.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=3)

    root = logging.getLogger()
    root.setLevel(log_level)
    root.addHandler(handler)