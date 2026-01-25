import logging
from functools import wraps
from datetime import datetime


def log_action(action: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(__name__)
            timestamp = datetime.now().isoformat()

            try:
                result = func(*args, **kwargs)
                logger.info(f"Действие {action} совершено успешно! - {timestamp}")
                return result
            except Exception as e:
                logger.error(f"Ошибка при выполнении действия {action} - {timestamp}: {str(e)}")
                raise

        return wrapper
    return decorator

