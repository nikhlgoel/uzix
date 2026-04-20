# Roadmap

This is where we're trying to go. Not a promise — a direction.

---

## What's done (v0.1 — v0.2)

- Rule-based detector (English + Hindi + Hinglish)
- Obfuscation-aware preprocessor (homoglyphs, leet, base64, zero-width chars)
- TF-IDF + Logistic Regression ML model
- Labeled dataset (400+ entries)
- Flask REST API
- Chrome extension (MV3)
- Hybrid detector (rules + ML combined)
- Eval/benchmark script

---

## Near-term (v0.3)

Things that are basically decided, just need time:

- **Wire hybrid detector into the API** — right now API only uses rule-based.
  Simple change, just haven't done it yet.
- **Expand dataset** — 400 total is not enough. Target: 1000+ per class.
  More Hinglish specifically. More persona-hijacking variants. More DAN-style attacks.
- **Add confidence score to API response** — currently just returns SAFE/SUSPICIOUS/DANGEROUS.
  Confidence percentage would be more useful for downstream systems.
- **`python -m uzix` CLI** — make the package runnable as a module.

---

## Medium-term (v1.0)

This is where the project becomes actually useful beyond demos:

- **PyPI package** — `pip install uzix`. The detector should be a one-liner to use.
- **Docker setup** — containerize the API so anyone can run it without Python setup.
- **Fuzzy pattern matching** — edit-distance variants of injection patterns.
  The question is whether this degrades false positive rate too much.
  Need to benchmark before adding.
- **Firefox extension** — MV2 version or shared MV3 with Firefox's limited support.
- **API rate limiting + optional API key** — needed before any public deployment.
- **Bengali, Tamil, Marathi patterns** — expanding beyond Hindi/Hinglish.
  This is harder than adding patterns — need speakers or good data.

---

## Research track (ongoing alongside v1.0)

These are the questions we're actively trying to answer:

- **Does the hybrid approach actually outperform either method alone?**
  The eval script will tell us. We expect yes, but the margin might be small.
  
- **What's the false positive rate on real-world prompts?**
  Our current evals are on our own dataset. That's circular. Need external data.

- **Can we catch Hinglish injections that don't match known patterns?**
  ML might — if trained on enough Hinglish. IndicBERT would probably do better.

- **How do attackers actually try to bypass our detector?**
  Adversarial testing — manually trying to craft payloads that evade both layers.
  Document everything we find. That's the most valuable research output.

---

## Long-term / ambitious

Not committing to these, but worth keeping in mind:

- **IndicBERT / multilingual-BERT integration** — proper multilingual embeddings.
  Would need to benchmark vs the current TF-IDF approach first.
- **Real-time streaming analysis** — for chat interfaces that send token by token.
- **Public dataset release** — properly versioned, citable dataset for the research community.
  Right now it's just CSV files in a repo. We want it to be something people can cite.
- **Research writeup** — not a formal paper necessarily, but a proper findings document
  that could be shared on arXiv or similar.
- **Integration with LangChain / LlamaIndex guardrails** — so devs can add Uzix as
  a guardrail in their existing pipeline with one line of code.

---

## What we're explicitly not doing (for now)

- SaaS / cloud hosting with billing
- Support for right-to-left scripts (Arabic, Hebrew) — not our expertise
- Real-time streaming API
- Enterprise compliance features
