from __future__ import annotations

import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        event = getattr(record, "event", None)
        if event:
            payload["event"] = event

        context = getattr(record, "context", None)
        if isinstance(context, dict):
            payload.update(context)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


class KeyValueFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        parts = [f"level={record.levelname}", f"logger={record.name}", f"message={record.getMessage()}"]
        event = getattr(record, "event", None)
        if event:
            parts.append(f"event={event}")

        context = getattr(record, "context", None)
        if isinstance(context, dict):
            for key, value in context.items():
                parts.append(f"{key}={value}")

        if record.exc_info:
            parts.append(f"exception={self.formatException(record.exc_info)}")

        return " ".join(parts)


def configure_logger(name: str, *, level: str, json_logs: bool) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter() if json_logs else KeyValueFormatter())
    logger.handlers = [handler]
    return logger
