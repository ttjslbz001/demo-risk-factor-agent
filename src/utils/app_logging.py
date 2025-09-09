import json
import logging
import sys
import time
import uuid
from typing import Any, Dict, Optional


_LOGGER_INITIALIZED = False


def _ensure_configured() -> None:
    global _LOGGER_INITIALIZED
    if _LOGGER_INITIALIZED:
        return
    if not logging.getLogger().handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        root = logging.getLogger()
        root.addHandler(handler)
        root.setLevel(logging.INFO)
    _LOGGER_INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    _ensure_configured()
    return logging.getLogger(name)


def new_request_id() -> str:
    return str(uuid.uuid4())


def start_timer() -> float:
    return time.perf_counter()


def elapsed_ms(start: float) -> int:
    return int((time.perf_counter() - start) * 1000)


def log_json(logger: logging.Logger, event: str, data: Optional[Dict[str, Any]] = None) -> None:
    payload: Dict[str, Any] = {"event": event, "ts": int(time.time() * 1000)}
    if data:
        payload.update(data)
    logger.info(json.dumps(payload, ensure_ascii=False))
