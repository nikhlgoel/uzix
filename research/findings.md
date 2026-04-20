# Research Findings — Uzix

This is where we track what we learned building this. Written as a dev log, not a formal paper.

---

## Background

Prompt injection is a class of attack where a user supplies text that overrides or hijacks the instructions given to an AI model. It's roughly analogous to SQL injection — the boundary between data and instructions gets blurred.

Most existing detection work focuses on English. We wanted to see how easy it is to attack AI apps in Hindi and Hinglish (mixed Hindi-English, very common in Indian internet usage).

---

## Dataset Notes

- Started with 2 placeholder entries per file. Not great.
- Built up to 200+ normal prompts and 200+ injection prompts.
- Injection prompts cover: direct instruction override, persona hijacking, jailbreak variants (DAN, developer mode, god mode), and Hinglish/Hindi transliterated equivalents.
- A lot of Hindi injections are just translated from the English versions. The interesting ones are Hinglish — they mix scripts in ways that rule-based tools would miss.

---

## Rule-based Detector

Works well for known patterns. If an injection exactly matches a regex, it gets caught. Problems:
- New phrasing that doesn't match any pattern will slip through
- False positive risk on legitimate prompts that mention "override" or "bypass" in context
- No fuzzy matching — small typos/variants escape detection

Accuracy on our own test cases: catches ~85% of the injection examples we wrote.

---

## ML Model (early notes)

Using TF-IDF + Logistic Regression:
- Trains in a few seconds on 400+ samples
- Accuracy expected ~85-90% on test split once dataset is fully expanded
- Not tested on real-world injection attempts yet

Main limitation: model learns the vocabulary of our dataset. Adversaries who use unusual phrasing or translate to other Indic scripts (Bengali, Tamil) will not be caught.

---

## What we're still figuring out

- How well does this generalize beyond our own dataset?
- What does false positive rate look like on real user prompts?
- Is IndicBERT worth adding for better multilingual coverage?
- Can we make the rule-based layer fuzzy (edit distance / phonetic matching)?

---

## References / Inspiration

- Perez & Ribeiro, 2022 — "Ignore Previous Prompt: Attack Techniques For Language Models"
- Simon Willison's blog on prompt injection (simonwillison.net)
- OWASP LLM Top 10 — LLM01: Prompt Injection
- Garak (LLM vulnerability scanner)
