import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return default


def _read_int(name: str, default: int, *, minimum: int | None = None, maximum: int | None = None) -> int:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        parsed = int(value)
    except ValueError:
        return default

    if minimum is not None and parsed < minimum:
        return minimum
    if maximum is not None and parsed > maximum:
        return maximum
    return parsed


def _read_csv(name: str) -> tuple[str, ...]:
    value = os.getenv(name, "")
    if not value.strip():
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    max_prompt_chars: int = 5000
    max_batch_size: int = 128
    use_ml: bool = True
    warmup_model: bool = False
    api_host: str = "127.0.0.1"
    api_port: int = 5000
    debug: bool = False
    log_level: str = "WARNING"
    json_logs: bool = True
    api_keys: tuple[str, ...] = ()
    api_key_header: str = "X-API-Key"
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            max_prompt_chars=_read_int("UZIX_MAX_PROMPT_CHARS", 5000, minimum=1, maximum=100000),
            max_batch_size=_read_int("UZIX_MAX_BATCH_SIZE", 128, minimum=1, maximum=10000),
            use_ml=_read_bool("UZIX_USE_ML", True),
            warmup_model=_read_bool("UZIX_WARMUP_MODEL", False),
            api_host=os.getenv("UZIX_API_HOST", "127.0.0.1"),
            api_port=_read_int("UZIX_API_PORT", 5000, minimum=1, maximum=65535),
            debug=_read_bool("UZIX_DEBUG", False),
            log_level=os.getenv("UZIX_LOG_LEVEL", "WARNING").upper(),
            json_logs=_read_bool("UZIX_JSON_LOGS", True),
            api_keys=_read_csv("UZIX_API_KEYS"),
            api_key_header=os.getenv("UZIX_API_KEY_HEADER", "X-API-Key"),
            rate_limit_enabled=_read_bool("UZIX_RATE_LIMIT_ENABLED", True),
            rate_limit_requests=_read_int("UZIX_RATE_LIMIT_REQUESTS", 60, minimum=1, maximum=100000),
            rate_limit_window_seconds=_read_int("UZIX_RATE_LIMIT_WINDOW_SECONDS", 60, minimum=1, maximum=86400),
        )