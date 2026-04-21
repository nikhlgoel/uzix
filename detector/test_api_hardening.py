from uzix.api import create_app
from uzix.config import Settings


def test_request_id_header_is_added_to_responses():
    app = create_app(settings=Settings(use_ml=False))
    client = app.test_client()

    response = client.post("/detect", json={"prompt": "What is the capital of France?"})

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")


def test_api_key_is_required_when_configured():
    app = create_app(settings=Settings(use_ml=False, api_keys=("secret-key",)))
    client = app.test_client()

    unauthorized = client.post("/detect", json={"prompt": "What is the capital of France?"})
    authorized = client.post(
        "/detect",
        json={"prompt": "What is the capital of France?"},
        headers={"X-API-Key": "secret-key"},
    )

    assert unauthorized.status_code == 401
    assert authorized.status_code == 200


def test_rate_limit_blocks_after_limit_is_hit():
    app = create_app(
        settings=Settings(
            use_ml=False,
            rate_limit_enabled=True,
            rate_limit_requests=1,
            rate_limit_window_seconds=60,
        )
    )
    client = app.test_client()

    first = client.post("/detect", json={"prompt": "What is the capital of France?"})
    second = client.post("/detect", json={"prompt": "What is the capital of France?"})

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.headers.get("Retry-After")


def test_health_reports_security_and_rate_limit_settings():
    app = create_app(
        settings=Settings(
            use_ml=False,
            api_keys=("secret-key",),
            rate_limit_enabled=True,
            rate_limit_requests=10,
            rate_limit_window_seconds=30,
        )
    )
    client = app.test_client()

    response = client.get("/health")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["auth_enabled"] is True
    assert payload["api_key_header"] == "X-API-Key"
    assert payload["rate_limit"]["enabled"] is True
    assert payload["rate_limit"]["requests"] == 10
    assert payload["rate_limit"]["window_seconds"] == 30
