from logging.config import dictConfig
import sys
import logging
from src.core.config import settings

log_level_str = settings.LOG_LEVEL.upper()
log_level = getattr(logging, log_level_str, logging.WARNING)


def setup_logging(level=log_level, log_to_file=False, filename="app.log"):
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,  # <== important!
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": level,
                "formatter": "default",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["default"],
                "level": level,
            },
            "uvicorn": {
                "level": level,
            },
            "uvicorn.error": {
                "level": level,
            },
            "uvicorn.access": {
                "level": level,
                "handlers": ["default"],
                "propagate": False,
            },
        },
    }

    dictConfig(log_config)


def get_logger(name=None):
    """Returns a logger for a module."""
    return logging.getLogger(name if name else __name__)
