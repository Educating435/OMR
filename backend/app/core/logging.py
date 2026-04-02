import logging
from logging.config import dictConfig


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "jsonish": {
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "jsonish",
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["default"],
            },
        }
    )


logger = logging.getLogger("omr_scanner")

