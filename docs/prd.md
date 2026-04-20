# PRD — Uzix

**Version:** 0.1  
**Date:** April 2026  
**Author:** Uzix team

---

## Problem

AI apps (chatbots, customer tools, automated pipelines) are easy to manipulate with prompt injection — where someone sneaks in instructions to override the AI's intended behavior. Most existing tools only cover English. Indian deployments running on Hindi or Hinglish inputs are completely unprotected.

## Goal

A lightweight, open-source tool that:
- Detects prompt injection in English, Hindi, and Hinglish text
- Works as a Python library, a REST API, and a browser extension
- Has an openly published dataset so others can build on it

---

## Phases

### v0.1 — Research & Rule-based
- Build labeled dataset (200+ normal, 200+ injection, 100+ Hindi/Hinglish)
- Rule-based detector using regex patterns
- Returns: `SAFE` / `SUSPICIOUS` / `DANGEROUS`

### v0.2 — ML Model
- Train scikit-learn classifier on dataset
- Accuracy benchmarked and documented
- Flask REST API wrapper

### v1.0 — Usable Product
- Browser extension (Chrome)
- Public API
- Full docs
- Research findings published

---

## Non-goals (for now)
- Real-time streaming analysis
- Cloud hosting or SaaS
- Support for languages other than EN/HI/Hinglish
- Enterprise features

---

## Success Criteria
- Rule-based: catches >80% of known patterns in test set
- ML model: >85% accuracy on test split
- API: responds correctly to POST /detect
- Extension: shows risk badge on injection input
