# Design Doc — Uzix

Quick design notes. Not a formal spec, just enough to keep things consistent.

---

## Architecture

```
User Input
    │
    ▼
[Rule-based Detector]  ← fast, no model needed, works offline
    │
    ▼
[ML Classifier] (optional, Phase 2)
    │
    ▼
Risk Level: SAFE / SUSPICIOUS / DANGEROUS
    │
    ├── Python script (CLI)
    ├── Flask REST API (POST /detect)
    └── Browser Extension (content script + popup)
```

---

## Risk Levels

| Level | Meaning |
|---|---|
| SAFE | No patterns matched |
| SUSPICIOUS | 1 injection pattern matched |
| DANGEROUS | 2+ injection patterns matched (or ML high-confidence positive) |

---

## Rule-based detector (v0.1)

- Regex patterns for English + Hindi (Devanagari) + Hinglish (transliterated)
- Patterns compiled once at import time for performance
- Case-insensitive matching
- No external dependencies

## ML model (v0.2)

- TF-IDF vectorizer (unigrams + bigrams, max 5000 features)
- Logistic Regression (C=1.0, lbfgs solver)
- Train/test split: 80/20
- Model serialized with pickle
- Confidence threshold: >=85% → DANGEROUS, else SUSPICIOUS

## API (v0.2)

- Single endpoint: `POST /detect`
- Input: `{ "prompt": "..." }`
- Output: `{ "prompt": "...", "risk": "...", "info": "..." }`
- Input length cap: 5000 chars
- No auth for local dev; will add API key in v1.0

## Extension (v0.2)

- MV3 Chrome extension
- Content script watches all textareas and text inputs
- Checks on paste and blur events
- Shows a badge overlay (bottom-right corner)
- Popup for manual check
- Connects to local API on 127.0.0.1:5000

---

## What we're not over-engineering right now

- No auth/rate limiting on API (local use only for now)
- No database — just CSV dataset
- No CI/CD pipeline yet
- No Docker setup yet (planned for v1.0)
