# Compatibility

Notes on what works where, tested or expected.

---

## Python

| Version | Status |
|---|---|
| 3.10 | Tested, works |
| 3.11 | Expected to work |
| 3.12 | Expected to work |
| 3.8 / 3.9 | Should work, not tested |
| 2.x | Not supported |

---

## Flask API

| Environment | Status |
|---|---|
| Local (Windows) | Tested |
| Local (macOS/Linux) | Expected to work |
| Docker | Not set up yet (planned v1.0) |
| Railway / Render | Should work with Gunicorn |

---

## Browser Extension

| Browser | Status |
|---|---|
| Chrome (MV3) | Tested locally |
| Edge (Chromium) | Should work, not tested |
| Firefox | Not supported (uses MV3 only) |
| Safari | Not supported |

---

## Dataset

| Format | Status |
|---|---|
| CSV (UTF-8) | Works, tested |
| Devanagari in CSV | Works with Python utf-8 reader |
| Excel | Not officially supported, but CSV opens fine in Excel |

---

## ML Model

| Dependency | Version | Notes |
|---|---|---|
| scikit-learn | >=1.0 | Tested on 1.3+ |
| numpy | >=1.21 | Pulled in by scikit-learn |
| pickle | stdlib | No version issue |

---

## Known Issues

- Extension requires Uzix API to be running locally on port 5000
- Firefox does not support MV3 fully (planned fix in v1.0)
- Model file (model.pkl) is gitignored — you need to retrain after cloning
