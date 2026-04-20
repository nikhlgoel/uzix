# Changelog

Format: [version] — date — description

---

## [0.1.0] — April 2026

### Added
- Initial project structure (dataset, detector, api, extension, docs, research)
- Rule-based prompt injection detector (`detector/rule_based.py`)
  - English patterns: 16 regex patterns
  - Hindi/Hinglish patterns: 9 patterns
  - Returns SAFE / SUSPICIOUS / DANGEROUS
- Unit tests for rule-based detector (`detector/test_rule_based.py`)
- Dataset started: `dataset/normal.csv`, `dataset/injections.csv`
  - 200+ normal prompts (English + Hindi + Hinglish)
  - 200+ injection prompts (English + Hindi + Hinglish)
- Flask API (`api/app.py`)
  - POST /detect endpoint
  - GET / — index + endpoint listing
  - GET /health
- ML model scaffold (`detector/ml_model.py`)
  - TF-IDF + Logistic Regression
  - Train/eval/predict functions
  - model.pkl + vectorizer.pkl saved to disk
- Chrome extension (MV3)
  - `extension/manifest.json`
  - `extension/content.js` — attaches to all text inputs, checks on paste/blur
  - `extension/popup.html` — manual check UI
- Docs
  - `docs/prd.md`
  - `docs/tech_stack.md`
  - `docs/design_doc.md`
  - `docs/compatibility.md`
  - `docs/framework.md`
  - `docs/changelog.md`
  - `docs/feature_report.md`
  - `docs/failure_report.md`
- `research/findings.md` — initial findings
- `.gitignore`, `requirements.txt`, `CONTRIBUTING.md`, `README.md`

---

## Upcoming

### [0.2.0] — planned
- Retrain ML model on expanded dataset
- Add HuggingFace multilingual model option
- API key support for /detect
- Docker setup

### [1.0.0] — planned
- PyPI package (`pip install uzix`)
- Public hosted API
- Firefox extension support
- Performance benchmarks vs baseline tools
