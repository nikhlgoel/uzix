# Framework Notes

Decisions on why we structured things the way we did.

---

## Why Flask and not FastAPI

Flask was chosen for simplicity. FastAPI is great but adds async complexity we don't need for a single-endpoint prototype. If we scale to high concurrency in v1.0, we'll probably migrate or add Gunicorn workers.

---

## Why scikit-learn and not HuggingFace

HuggingFace transformers are powerful but heavyweight. For Phase 2, a TF-IDF + Logistic Regression is:
- Fast to train (seconds, not hours)
- Easy to explain
- Good enough for pattern-heavy injection detection

We'll add multilingual-BERT or IndicBERT in Phase 2 if accuracy is not good enough.

---

## Why CSV dataset and not a database

Open-source discoverability. Anyone can download, view, and cite a CSV. A database requires setup. CSV also versions cleanly in Git.

---

## Why a Chrome extension and not an npm package

Easier to demo. A Chrome extension is visually demonstrable in a recording. npm package is better for developer adoption but harder to show. Both are planned.

---

## Project structure

```
uzix1/
├── dataset/     ← all training data lives here
├── detector/    ← rule_based.py and ml_model.py, self-contained
├── api/         ← Flask app, imports from detector/
├── extension/   ← browser extension, talks to api/
├── docs/        ← design, prd, changelog, etc.
└── research/    ← findings and benchmarks
```

The detector module is intentionally standalone — it should be importable without Flask running.

---

## Versioning plan

- v0.1 — Rule-based detector + dataset
- v0.2 — ML model + Flask API
- v1.0 — Extension + public API + PyPI package + full docs
