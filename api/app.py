from flask import Flask, request, jsonify
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from uzix.api import create_app
from uzix.config import Settings

settings = Settings.from_env()
app = create_app(settings=settings)

if __name__ == "__main__":
    app.run(host=settings.api_host, port=settings.api_port, debug=settings.debug)
