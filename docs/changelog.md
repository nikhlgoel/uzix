# Changelog

Format: [version] — date — description

---

## [0.2.1] — April 20, 2026

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
