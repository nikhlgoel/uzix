from flask import Flask, request, jsonify
import sys
import os

# so detector module can be imported from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from detector.rule_based import detect_prompt_injection

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "Uzix",
        "description": "Multilingual prompt injection detector API",
        "version": "0.1",
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

    # cap input length to prevent abuse
    if len(prompt) > 5000:
        return jsonify({"error": "Input too long. Max 5000 characters."}), 413

    result = detect_prompt_injection(prompt)

    return jsonify({
        "prompt": prompt,
        "risk": result,
        "info": {
            "SAFE": "No injection patterns detected.",
            "SUSPICIOUS": "One injection pattern matched. Review recommended.",
            "DANGEROUS": "Multiple injection patterns matched. High risk."
        }.get(result)
    })

if __name__ == "__main__":
    # debug=False for any real deployment
    app.run(host="127.0.0.1", port=5000, debug=True)
