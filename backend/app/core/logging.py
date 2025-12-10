from logging import getLogger
from logging.config import dictConfig

LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": LOG_FORMAT,
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "INFO",
                }
            },
            "root": {"handlers": ["console"], "level": "INFO"},
        }
    )


logger = getLogger("codex")
