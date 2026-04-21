# hybrid.py
# Combines rule-based and ML detection into a single scorer.
#
# The idea: rules are fast and interpretable. ML catches patterns rules miss.
# Running both and combining the signals is better than either alone — at least
# that's the hypothesis. The eval script will tell us if that's actually true.
#
# Decision logic:
#   1. Preprocess first (shared across both methods)
#   2. Rule-based: if DANGEROUS → done, high confidence, no need for ML
#   3. If SAFE by rules but ML says high-confidence injection → flag as SUSPICIOUS
#   4. If SUSPICIOUS by rules → use ML to confirm or upgrade
#   5. Disagreements are surfaced in the result so callers can see what fired

from detector.preprocessor import preprocess
from detector.rule_based import COMPILED_PATTERNS

_ml_import_error = None
try:
    from detector.ml_model import load_model, model_is_available, predict as ml_predict
except Exception as exc:
    _ml_import_error = exc
    load_model = None
    model_is_available = None
    ml_predict = None


def _is_ml_available() -> bool:
    if _ml_import_error is not None or load_model is None or model_is_available is None:
        return False
    if not model_is_available():
        return False

    try:
        load_model()
        return True
    except Exception:
        return False


def detect(text: str, use_ml: bool = True) -> dict:
    cleaned = preprocess(text)
    ml_available = _is_ml_available()

    # rule-based pass
    rule_matches = [pat.pattern for pat in COMPILED_PATTERNS if pat.search(cleaned)]
    if len(rule_matches) >= 2:
        rule_risk = "DANGEROUS"
    elif len(rule_matches) == 1:
        rule_risk = "SUSPICIOUS"
    else:
        rule_risk = "SAFE"

    ml_result = None
    if use_ml and ml_available and ml_predict is not None:
        try:
            # ml_predict preprocesses internally — pass raw text
            ml_result = ml_predict(text)
        except Exception:
            ml_result = None

    # combine
    final_risk = rule_risk
    if ml_result:
        ml_risk = ml_result["risk"]
        ml_conf = ml_result["confidence"]

        if rule_risk == "SAFE" and ml_risk == "DANGEROUS" and ml_conf >= 85:
            # rules missed it but ML is very confident — bump up
            final_risk = "SUSPICIOUS"
        elif rule_risk == "SUSPICIOUS" and ml_risk == "DANGEROUS" and ml_conf >= 85:
            final_risk = "DANGEROUS"
        elif rule_risk == "DANGEROUS" and ml_risk == "SAFE" and ml_conf >= 90:
            # rules fired but ML is very confident it's safe — downgrade
            # keeping at SUSPICIOUS because rules are usually right on their patterns
            final_risk = "SUSPICIOUS"

    return {
        "risk": final_risk,
        "rule_risk": rule_risk,
        "rule_matches": rule_matches,
        "ml": ml_result,
        "ml_available": ml_available,
    }


if __name__ == "__main__":
    import sys
    import json
    text = sys.argv[1] if len(sys.argv) > 1 else input("Enter prompt: ")
    result = detect(text)
    print(json.dumps(result, indent=2))
