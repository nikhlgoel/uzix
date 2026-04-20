# Feature Report

Status of all features across versions.

---

## v0.1 Features

| Feature | Status | Notes |
|---|---|---|
| Dataset — normal.csv (200+ entries) | Done | English + Hindi + Hinglish |
| Dataset — injections.csv (200+ entries) | Done | English + Hindi + Hinglish |
| Rule-based detector — English patterns | Done | 16 regex patterns |
| Rule-based detector — Hindi patterns | Done | Devanagari script |
| Rule-based detector — Hinglish patterns | Done | Transliterated |
| Returns SAFE / SUSPICIOUS / DANGEROUS | Done | Based on match count |
| Unit tests | Done | 4 test cases, all passing |
| CLI usage (python detector/rule_based.py) | Done | Accepts sys.argv or stdin |

---

## v0.2 Features

| Feature | Status | Notes |
|---|---|---|
| ML model — TF-IDF + Logistic Regression | Done (untrained) | Needs `python detector/ml_model.py` to train |
| ML model — train/eval output | Done | Prints accuracy + classification report |
| ML model — predict() function | Done | Returns risk + confidence |
| Flask API — POST /detect | Done | Returns JSON risk response |
| Flask API — GET /health | Done | Returns `{"status": "ok"}` |
| Flask API — input validation | Done | Rejects empty/missing/long inputs |
| Chrome Extension — content script | Done | Attaches to all text inputs |
| Chrome Extension — paste/blur listener | Done | Auto-checks on user action |
| Chrome Extension — badge overlay | Done | Shows risk level bottom-right |
| Chrome Extension — popup.html | Done | Manual check UI |

---

## v1.0 Features (planned)

| Feature | Status | Notes |
|---|---|---|
| PyPI package | Planned | |
| Public hosted API | Planned | |
| API key auth | Planned | |
| Firefox extension | Planned | Needs MV2 version |
| Docker setup | Planned | |
| HuggingFace multilingual model | Planned | IndicBERT candidate |
| Performance benchmarks | Planned | vs rule-only baseline |
| Research paper / README findings | In progress | See research/findings.md |
