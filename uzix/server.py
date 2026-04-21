from uzix.api import create_app
from uzix.config import Settings


def main() -> None:
    from waitress import serve

    settings = Settings.from_env()
    app = create_app(settings=settings)
    serve(app, host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    main()
