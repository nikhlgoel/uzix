import time
import uuid

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

from uzix import __version__
from uzix.config import Settings
from uzix.core import Detector, model_ready
from uzix.errors import RateLimitError, UnauthorizedError, ValidationError
from uzix.logging_utils import configure_logger
from uzix.security import InMemoryRateLimiter, get_client_ip, require_api_key


INFO_BY_RISK = {
    "SAFE": "No injection patterns detected.",
    "SUSPICIOUS": "One or more injection signals found. Review recommended.",
    "DANGEROUS": "Multiple injection signals matched. High risk.",
}


def _serialize_result(prompt: str, result: dict) -> dict:
    risk = result["risk"]
    return {
        "prompt": prompt,
        "risk": risk,
        "rule_risk": result["rule_risk"],
        "rule_matches": result["rule_matches"],
        "ml": result["ml"],
        "ml_available": result["ml_available"],
        "info": INFO_BY_RISK.get(risk),
    }


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    detector = Detector(settings=settings)
    logger = configure_logger("uzix.api", level=settings.log_level, json_logs=settings.json_logs)
    rate_limiter = InMemoryRateLimiter(
        limit=settings.rate_limit_requests,
        window_seconds=settings.rate_limit_window_seconds,
    )

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    protected_paths = {"/detect", "/detect/batch"}

    @app.before_request
    def before_request():
        g.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        g.request_started_at = time.perf_counter()
        g.rate_limit_state = None
        g.authenticated = False
        g.detected_risk = None

        if request.path not in protected_paths:
            return None

        api_key = require_api_key(
            request,
            allowed_keys=settings.api_keys,
            header_name=settings.api_key_header,
        )
        g.authenticated = api_key is not None

        if settings.rate_limit_enabled:
            client_ip = get_client_ip(request)
            rate_limit_key = f"{client_ip}:{api_key or 'anonymous'}:{request.path}"
            g.rate_limit_state = rate_limiter.check(rate_limit_key)
            if g.rate_limit_state.retry_after > 0:
                raise RateLimitError(retry_after=g.rate_limit_state.retry_after)

        return None

    @app.after_request
    def after_request(response):
        request_id = getattr(g, "request_id", None)
        if request_id:
            response.headers["X-Request-ID"] = request_id

        state = getattr(g, "rate_limit_state", None)
        if state is not None:
            response.headers["X-RateLimit-Limit"] = str(state.limit)
            response.headers["X-RateLimit-Remaining"] = str(state.remaining)
            if state.retry_after > 0:
                response.headers["Retry-After"] = str(state.retry_after)

        started_at = getattr(g, "request_started_at", None)
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2) if started_at else None
        logger.info(
            "request_complete",
            extra={
                "event": "request_complete",
                "context": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "remote_addr": get_client_ip(request),
                    "risk": getattr(g, "detected_risk", None),
                    "rate_limited": response.status_code == 429,
                    "auth_enabled": bool(settings.api_keys),
                },
            },
        )
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return jsonify({"error": str(exc)}), exc.status_code

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(exc: UnauthorizedError):
        response = jsonify({"error": str(exc)})
        response.status_code = exc.status_code
        response.headers["WWW-Authenticate"] = f"Bearer realm=\"Uzix\", header=\"{settings.api_key_header}\""
        return response

    @app.errorhandler(RateLimitError)
    def handle_rate_limit(exc: RateLimitError):
        state = getattr(g, "rate_limit_state", None)
        response = jsonify({"error": str(exc)})
        response.status_code = exc.status_code
        if state is not None:
            response.headers["X-RateLimit-Limit"] = str(state.limit)
            response.headers["X-RateLimit-Remaining"] = str(state.remaining)
        if exc.retry_after > 0:
            response.headers["Retry-After"] = str(exc.retry_after)
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        if isinstance(exc, HTTPException):
            return jsonify({"error": exc.description}), exc.code

        logger.exception(
            "request_failed",
            extra={
                "event": "request_failed",
                "context": {
                    "request_id": getattr(g, "request_id", None),
                    "method": request.method,
                    "path": request.path,
                },
            },
        )
        return jsonify({"error": "Internal server error"}), 500

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "name": "Uzix",
            "description": "Multilingual prompt injection detector API",
            "version": __version__,
            "ml_enabled": settings.use_ml,
            "auth_enabled": bool(settings.api_keys),
            "endpoints": {
                "/detect": "POST - detect prompt injection in one text",
                "/detect/batch": "POST - detect prompt injection across multiple texts",
                "/health": "GET - health check",
            },
        })

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "version": __version__,
            "ml_enabled": settings.use_ml,
            "ml_ready": model_ready() if settings.use_ml else False,
            "auth_enabled": bool(settings.api_keys),
            "api_key_header": settings.api_key_header,
            "rate_limit": {
                "enabled": settings.rate_limit_enabled,
                "requests": settings.rate_limit_requests,
                "window_seconds": settings.rate_limit_window_seconds,
            },
        })

    @app.route("/detect", methods=["POST"])
    def detect_route():
        data = request.get_json(force=True, silent=True)
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' field in request body"}), 400

        result = detector.detect(data["prompt"])
        g.detected_risk = result["risk"]

        return jsonify(_serialize_result(data["prompt"], result))

    @app.route("/detect/batch", methods=["POST"])
    def detect_batch_route():
        data = request.get_json(force=True, silent=True)
        if not data or "prompts" not in data:
            return jsonify({"error": "Missing 'prompts' field in request body"}), 400

        results = detector.detect_batch(data["prompts"])
        g.detected_risk = ",".join(result["risk"] for result in results)

        return jsonify({
            "count": len(results),
            "results": [
                _serialize_result(prompt, result)
                for prompt, result in zip(data["prompts"], results)
            ],
        })

    return app