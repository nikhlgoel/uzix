# Failure Report

Tracks bugs, failures, and what was done about them.

---

## Format
Each entry: what broke, how many times it hit us, root cause, fix.

---

## v0.1

### F-001 — Rule-based detector missing Hinglish transliterated variants
- **Count:** Noticed during dataset review
- **Symptom:** Hinglish injections like `sabhi niyam bhool jao` not caught
- **Root cause:** Initial pattern list was English-only
- **Fix:** Added 9 Hindi/Hinglish patterns to `HINDI_PATTERNS` in `rule_based.py`
- **Status:** Fixed

---

### F-002 — Dataset had only 2 entries per file
- **Count:** 1
- **Symptom:** ML model could not train with 2 samples
- **Root cause:** Placeholder data was never expanded
- **Fix:** Expanded to 200+ per CSV (normal + injections), including multilingual entries
- **Status:** Fixed

---

### F-003 — Empty folders not tracked by Git
- **Count:** 1
- **Symptom:** `api/`, `extension/`, `docs/`, `research/` did not appear in GitHub repo
- **Root cause:** Git does not track empty directories
- **Fix:** Added `.gitkeep` or actual files to each folder before committing
- **Status:** Fixed

---

### F-004 — curl POST failing on Windows PowerShell
- **Count:** Multiple tries
- **Symptom:** Curl returned error when sending JSON via `-d` flag in PowerShell
- **Root cause:** PowerShell quote escaping is different from bash. Double quotes inside `-d` string break the JSON
- **Fix:** Assign JSON to a variable first: `$json = '{...}'; curl -d $json`
- **Status:** Documented + workaround in place

---

### F-005 — ML model not importable from API without sys.path fix
- **Count:** 1
- **Symptom:** `from detector.rule_based import ...` fails when running `api/app.py` directly
- **Root cause:** Python's module resolution doesn't include the project root by default
- **Fix:** Added `sys.path.insert(0, project_root)` at top of `api/app.py`
- **Status:** Fixed

---

## Open / Known Issues

| ID | Description | Priority |
|---|---|---|
| F-006 | model.pkl not committed (gitignored) — need to retrain after fresh clone | Medium |
| F-007 | Extension hardcodes API URL to 127.0.0.1:5000 — breaks if API changes port | Low |
| F-008 | Firefox not supported (MV3 only) | Low — planned for v1.0 |
