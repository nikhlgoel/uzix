# Tech Stack

Current choices and why we picked them (not fancy, just practical).

---

## Core

| Layer | Tool | Why |
|---|---|---|
| Language | Python 3.10+ | Standard for ML, easy to prototype |
| ML library | scikit-learn | Lightweight, no GPU needed, beginner-friendly |
| API | Flask | Simple, no overhead, easy to extend |
| Dataset | CSV | Easy to version control, anyone can open it |
| Extension | Vanilla JS | No build step, works in any Chromium browser |
| Docs | Markdown | Standard for open source |

---

## Phase 2 / later

| Layer | Tool | Notes |
|---|---|---|
| Multilingual embeddings | HuggingFace transformers (multilingual-BERT or IndicBERT) | Better Hindi/Hinglish accuracy |
| API hosting | Railway / Fly.io / Render | Free tier, no infra to manage |
| Package | PyPI package (uzix) | `pip install uzix` |

---

## Dev Setup

```
Python 3.10+
pip install flask scikit-learn
```

Optional for ML training:
```
pip install pandas numpy
```

---

## Not using (and why)

- **FastAPI** — Flask is enough for v0.x
- **PyTorch / TensorFlow** — overkill for a TF-IDF classifier
- **React/Vue for extension** — no build tooling needed at this scale
- **Postgres** — no persistent storage needed yet
