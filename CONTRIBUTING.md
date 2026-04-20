# Contributing to Uzix

This is an open research project. Contributions of any size are welcome.

---

## What we need most

**Evasion attempts** — the most valuable contribution. If you craft a prompt injection
payload that slips past the detector (rule-based, ML, or hybrid), open an issue using
the evasion report template. This directly improves the project.

**Dataset additions** — more labeled prompts, especially:
- Hinglish injection variants
- Persona hijacking / roleplay jailbreaks
- Indirect prompt injection (injections embedded in retrieved content)
- False positives — safe prompts that currently get flagged

**New language patterns** — if you know Hindi, Bengali, Tamil, Marathi or other Indic
languages and can contribute injection patterns in those languages, that's huge.

**ML improvements** — better model, better features, better training pipeline.
Run `python eval.py` to get baseline numbers, make your change, run it again, include both.

---

## Running tests

```bash
python -m pytest detector/
```

## Running the eval

Train the model first, then benchmark all three detectors:
```bash
python detector/ml_model.py
python eval.py
```

## Code style

No strict linting rules. Keep it readable. If something needs a comment to understand,
add a comment. If it's obvious, don't bother.

---

## Process

1. Open an issue first if you're planning something significant
2. Fork the repo, make your change
3. Run the tests and eval
4. Open a PR — the template will ask for what you need

Small fixes (typos, obvious bugs) can just go straight to PR.

---

## Dataset format

`dataset/normal.csv` and `dataset/injections.csv` — both have a single column: `prompt`.
UTF-8 encoded. Devanagari and Hinglish work fine in the existing format.

If you're adding rows, just append — don't reorder existing entries (it makes diffs noisy).

---

## Questions

Open an issue tagged `question`. Or just check the research log at `research/log.md` —
a lot of open questions are documented there already.
