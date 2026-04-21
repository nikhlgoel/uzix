from __future__ import annotations

import logging
from dataclasses import replace
from typing import Iterable

from detector.hybrid import detect as hybrid_detect
from detector.ml_model import load_model, model_is_available
from detector.preprocessor import preprocess

from uzix.config import Settings
from uzix.errors import ModelUnavailableError, ValidationError


logger = logging.getLogger("uzix")


def validate_prompt(text: str, *, max_prompt_chars: int) -> str:
    if not isinstance(text, str):
        raise ValidationError("'prompt' must be a string")
    if not text.strip():
        raise ValidationError("'prompt' must be a non-empty string")
    if len(text) > max_prompt_chars:
        raise ValidationError(
            f"Input too long. Max {max_prompt_chars} characters.",
            status_code=413,
        )
    return text


def model_ready() -> bool:
    if not model_is_available():
        return False

    try:
        load_model()
        return True
    except Exception:
        logger.exception("Failed to load the Uzix ML model.")
        return False


class Detector:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings.from_env()
        if self.settings.warmup_model and self.settings.use_ml:
            self.warmup()

    def warmup(self) -> bool:
        if not self.settings.use_ml or not model_is_available():
            return False

        try:
            load_model()
            return True
        except FileNotFoundError:
            return False
        except Exception as exc:
            logger.exception("Failed to warm up the Uzix ML model.")
            raise ModelUnavailableError("Could not warm up the Uzix ML model.") from exc

    def detect(self, text: str) -> dict:
        validated = validate_prompt(text, max_prompt_chars=self.settings.max_prompt_chars)
        return hybrid_detect(validated, use_ml=self.settings.use_ml)

    def detect_batch(self, texts: Iterable[str]) -> list[dict]:
        if texts is None or isinstance(texts, (str, bytes)):
            raise ValidationError("'prompts' must be a list of strings")

        items = list(texts)
        if not items:
            raise ValidationError("'prompts' must contain at least one prompt")
        if len(items) > self.settings.max_batch_size:
            raise ValidationError(
                f"Batch too large. Max {self.settings.max_batch_size} prompts.",
                status_code=413,
            )

        return [self.detect(text) for text in items]


DEFAULT_SETTINGS = Settings.from_env()
DEFAULT_DETECTOR = Detector(settings=DEFAULT_SETTINGS)


def detect(text: str, *, use_ml: bool | None = None) -> dict:
    if use_ml is None:
        return DEFAULT_DETECTOR.detect(text)
    return Detector(settings=replace(DEFAULT_SETTINGS, use_ml=use_ml)).detect(text)


def detect_batch(texts: Iterable[str], *, use_ml: bool | None = None) -> list[dict]:
    if use_ml is None:
        return DEFAULT_DETECTOR.detect_batch(texts)
    return Detector(settings=replace(DEFAULT_SETTINGS, use_ml=use_ml)).detect_batch(texts)