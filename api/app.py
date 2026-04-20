from flask import Flask, request, jsonify
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from detector.hybrid import detect as hybrid_detect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "Uzix",
        "description": "Multilingual prompt injection detector API",
        "version": "0.2.1",
        "endpoints": {
            "/detect": "POST - detect prompt injection in text",
            "/health": "GET - health check"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json(force=True, silent=True)
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' field in request body"}), 400

    prompt = data["prompt"]
    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "'prompt' must be a non-empty string"}), 400

    if len(prompt) > 5000:
        return jsonify({"error": "Input too long. Max 5000 characters."}), 413

    result = hybrid_detect(prompt)
    risk = result["risk"]

    return jsonify({
        "prompt": prompt,
        "risk": risk,
        "rule_risk": result["rule_risk"],
        "rule_matches": result["rule_matches"],
        "ml": result["ml"],
        "ml_available": result["ml_available"],
        "info": {
            "SAFE": "No injection patterns detected.",
            "SUSPICIOUS": "One or more injection signals found. Review recommended.",
            "DANGEROUS": "Multiple injection signals matched. High risk."
        }.get(risk)
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
