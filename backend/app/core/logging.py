import json
import logging
from contextvars import ContextVar
from logging import Filter, getLogger
from logging.config import dictConfig
from typing import Any

TRACE_ID_CTX: ContextVar[str | None] = ContextVar("trace_id", default=None)


class RequestContextFilter(Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: ANN001
        record.trace_id = TRACE_ID_CTX.get()
        return True


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: ANN001
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        trace_id = getattr(record, "trace_id", None)
        if trace_id:
            payload["trace_id"] = trace_id
        skipped_keys = {
            "args",
            "msg",
            "levelname",
            "levelno",
            "name",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "trace_id",
        }

        for key, value in record.__dict__.items():
            if key in skipped_keys:
                continue
            payload[key] = value
        return json.dumps(payload, default=str)


LOG_FORMATTER_NAME = "json"


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "formatters": {
                LOG_FORMATTER_NAME: {
                    "()": JSONFormatter,
                }
            },
            "filters": {
                "request_context": {
                    "()": RequestContextFilter,
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": LOG_FORMATTER_NAME,
                    "level": "INFO",
                    "filters": ["request_context"],
                }
            },
            "root": {"handlers": ["console"], "level": "INFO"},
        }
    )


logger = getLogger("codex")
