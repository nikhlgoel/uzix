# Changelog

Format: [version] — date — description

---

## [0.3.0] — April 21, 2026

### Added
- `uzix-serve` command via `uzix/server.py` using Waitress for a production-friendly HTTP server
- `uzix-train` command via `uzix/train.py` for one-command model training
- `uzix/logging_utils.py` — structured JSON/key-value request logging
- `uzix/security.py` — API key extraction, client IP handling, in-memory rate limiting
- `.env.example` — environment-based runtime configuration template
- `Dockerfile` — container build that installs Uzix and trains the model at image build time
- `docker-compose.yml` — one-command local container setup
- `.dockerignore` — leaner Docker builds
- `detector/test_api_hardening.py` — tests for request IDs, API keys, rate limiting, and health metadata

### Changed
- `uzix/api.py` — now includes request IDs, structured request logs, API key auth, rate limit headers, and batch endpoint hardening
- `uzix/config.py` — now supports `.env` loading, API keys, rate limit config, and structured log toggles
- `detector/hybrid.py` — ML availability is now checked dynamically instead of only once at import time
- `README.md` — updated with package install, `uzix-serve`, `uzix-train`, auth, batch API, and Docker setup
- `setup.py` / `requirements.txt` — added `waitress` and `python-dotenv`; version bumped to `0.3.0`

### Test results
- 59 tests — hardening and public API coverage included

---

## [0.2.2] — session 2

### Fixed
- **F-009 — Preprocessing mismatch** (critical): `ml_model.py` now preprocesses text
  at training time (`load_dataset`) and inference time (`predict`). `hybrid.py` updated
  to pass raw text to `ml_predict` to avoid double-processing.

### Changed
- `detector/rule_based.py` — patterns reorganised into 9 attack classes (80+ patterns, up from 25):
  - `OVERRIDE_PATTERNS` — direct instruction cancellation (now handles multi-word qualifiers)
  - `JAILBREAK_PATTERNS` — DAN, god mode, developer mode, unrestricted mode
  - `PERSONA_PATTERNS` — identity/role hijacking
  - `LEAKING_PATTERNS` — prompt extraction (Perez & Ribeiro 2022 — second attack class)
  - `CONTEXT_PARTITION_PATTERNS` — HouYi-style separator attacks, XML tag injection
  - `ALIGNMENT_BYPASS_PATTERNS` — RLHF/safety training override attempts
  - `PRIVILEGE_PATTERNS` — false authority claims
  - `HINDI_PATTERNS` — Devanagari script
  - `HINGLISH_PATTERNS` — transliterated Hinglish (18 patterns)
- `api/app.py` — API now uses hybrid detector (`detector.hybrid.detect`) instead of
  rule-based only. Response includes `rule_risk`, `rule_matches`, and `ml` fields.
- `research/findings.md` — expanded with all 6 academic papers read, key insights mapped
  to codebase design decisions
- `docs/failure_report.md` — F-009 marked as Fixed

### Added
- `setup.py` — project is now pip-installable (`pip install -e .`)
- `detector/__main__.py` — CLI: `python -m detector "some prompt"` or `uzix "prompt"`
  - Exit codes: 0=SAFE, 1=SUSPICIOUS, 2=DANGEROUS (pipe-friendly)
- `detector/__init__.py` — exports `detect`, `detect_prompt_injection`, `preprocess`
- `detector/test_hybrid.py` — 18 new tests for hybrid detector (direct, persona, leaking,
  Hinglish, context partition, edge cases)
- `detector/ml_model.py` — retrained at 97.50% accuracy on preprocessed dataset

### Test results
- 49 tests — 49 passed, 0 failed

### Research papers incorporated
All patterns and design decisions now grounded in published work:
- Perez & Ribeiro 2022 — arXiv:2211.09527
- Greshake et al. 2023 — arXiv:2302.12173
- Liu et al. 2023 (HouYi) — arXiv:2306.05499
- Liu et al. 2023 (USENIX) — arXiv:2310.12815
- Yi et al. 2023 (BIPIA) — arXiv:2312.14197
- OWASP LLM Top 10

---

## [0.2.1] — session 1

### Added
- `detector/hybrid.py` — combines rule-based + ML into a single scorer
  - Rules run first (fast path for DANGEROUS)
  - ML used to confirm, upgrade, or downgrade rule-based result
  - Returns detailed dict showing which signals fired
  - Gracefully falls back to rule-only if model not trained
- `eval.py` — benchmarks all three detectors on the full dataset
  - Side-by-side accuracy / precision / recall / F1
  - Lists false positives and false negatives for rule-based
  - Skips ML/hybrid gracefully if model not available
- `research/log.md` — running research diary, informal dev log
- `ROADMAP.md` — where the project is heading
- `LICENSE` — MIT
- `.github/ISSUE_TEMPLATE/` — bug report, evasion report, dataset contribution
- `.github/PULL_REQUEST_TEMPLATE.md`

### Changed
- README significantly expanded — better open-source positioning, why this matters,
  clearer quick-start for all three detectors
- CONTRIBUTING.md rewritten — focused on what we actually need (evasions, dataset, ML)

### Notes
- Hybrid detector identified a preprocessing mismatch: ML model sees raw text,
  rule-based sees preprocessed text. Need to decide on one approach. Tracked in research/log.md.
- API still uses rule-based only. Hybrid wiring to API is next.

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
- Obfuscation-aware preprocessor (`detector/preprocessor.py`)
  - Homoglyph normalization (Cyrillic, Greek → ASCII)
  - Zero-width character stripping
  - Leet speak normalization
  - Base64 fragment decoding
  - HTML entity decoding
  - Punctuation obfuscation removal (i.g.n.o.r.e → ignore)
- Docs: prd.md, tech_stack.md, design_doc.md, compatibility.md, framework.md,
  changelog.md, feature_report.md, failure_report.md
- `research/findings.md` — initial findings
- `.gitignore`, `requirements.txt`, `CONTRIBUTING.md`, `README.md`

---

## Upcoming

### [0.3.0] — planned
- Wire hybrid detector into API (replace rule-only with hybrid)
- Add confidence score to API response
- Expand dataset to 1000+ per class (Hinglish focus)
- Solve preprocessing mismatch between ML and rule-based paths

### [1.0.0] — planned
- PyPI package (`pip install uzix`)
- Docker setup
- Firefox extension support
- Fuzzy pattern matching (edit distance)
- Performance benchmarks published
