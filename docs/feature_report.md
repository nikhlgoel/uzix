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
| Preprocessor — homoglyph normalization | Done | Cyrillic + Greek → ASCII |
| Preprocessor — zero-width char stripping | Done | |
| Preprocessor — leet speak normalization | Done | |
| Preprocessor — base64 decoding | Done | Appends decoded to input |
| Preprocessor — HTML entity decoding | Done | |
| Preprocessor — punctuation obfuscation | Done | i.g.n.o.r.e → ignore |

---

## v0.2 Features

| Feature | Status | Notes |
|---|---|---|
| ML model — TF-IDF + Logistic Regression | Done (untrained) | Run: python detector/ml_model.py |
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

## v0.2.1 Features

| Feature | Status | Notes |
|---|---|---|
| Hybrid detector (rules + ML combined) | Done | detector/hybrid.py |
| Eval / benchmark script | Done | eval.py — all three detectors side by side |
| Research log (dev diary) | Done | research/log.md |
| ROADMAP.md | Done | |
| LICENSE (MIT) | Done | |
| GitHub issue templates | Done | bug, evasion, dataset contribution |
| GitHub PR template | Done | |
| README — open-source positioning | Done | Rewritten |
| CONTRIBUTING.md — substantial | Done | Rewritten |

---

## v1.0 Features (planned)

| Feature | Status | Notes |
|---|---|---|
| PyPI package | Planned | pip install uzix |
| Docker setup | Planned | |
| Public hosted API | Planned | |
| API key auth | Planned | |
| Firefox extension | Planned | Needs MV2 version |
| HuggingFace multilingual model | Planned | IndicBERT candidate |
| Fuzzy pattern matching | Planned | Edit distance on rule patterns |
| Performance benchmarks published | Planned | vs rule-only baseline |
| Expanded dataset (1000+ per class) | Planned | Hinglish focus |
| Hybrid wired into API | Next | Simple swap in api/app.py |
