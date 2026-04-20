# eval.py
# Benchmark script — runs both detectors on the full dataset and prints metrics.
# Run this after training the ML model: python detector/ml_model.py
# Then: python eval.py
#
# Why this matters: we need to actually know if rule-based + ML combined is
# better than either alone, or if we're just adding complexity for nothing.
# This script answers that.

import os
import sys
import csv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from detector.preprocessor import preprocess
from detector.rule_based import detect_prompt_injection

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")

def load_labeled_data():
    data = []
    for filename, true_label in [("normal.csv", "SAFE"), ("injections.csv", "INJECTION")]:
        filepath = os.path.join(DATASET_DIR, filename)
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = row.get("prompt", "").strip().strip('"')
                if text:
                    data.append((text, true_label))
    return data

def score(predictions, labels):
    tp = sum(1 for p, l in zip(predictions, labels) if p != "SAFE" and l == "INJECTION")
    fp = sum(1 for p, l in zip(predictions, labels) if p != "SAFE" and l == "SAFE")
    tn = sum(1 for p, l in zip(predictions, labels) if p == "SAFE" and l == "SAFE")
    fn = sum(1 for p, l in zip(predictions, labels) if p == "SAFE" and l == "INJECTION")

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / len(labels) if labels else 0
    return {"precision": precision, "recall": recall, "f1": f1, "accuracy": accuracy,
            "tp": tp, "fp": fp, "tn": tn, "fn": fn}

def main():
    print("Loading dataset...")
    data = load_labeled_data()
    texts = [d[0] for d in data]
    labels = [d[1] for d in data]
    print(f"  {len(data)} total samples ({labels.count('SAFE')} normal, {labels.count('INJECTION')} injection)\n")

    # rule-based
    rule_preds = [detect_prompt_injection(t) for t in texts]
    rule_metrics = score(rule_preds, labels)
    print("=== Rule-based Detector ===")
    print(f"  Accuracy:  {rule_metrics['accuracy']*100:.1f}%")
    print(f"  Precision: {rule_metrics['precision']*100:.1f}%")
    print(f"  Recall:    {rule_metrics['recall']*100:.1f}%")
    print(f"  F1:        {rule_metrics['f1']*100:.1f}%")
    print(f"  TP={rule_metrics['tp']} FP={rule_metrics['fp']} TN={rule_metrics['tn']} FN={rule_metrics['fn']}")

    # ML (optional)
    try:
        from detector.ml_model import predict as ml_predict
        print("\n=== ML Detector (TF-IDF + LR) ===")
        ml_preds = []
        for t in texts:
            r = ml_predict(t)
            ml_preds.append(r["risk"])
        ml_metrics = score(ml_preds, labels)
        print(f"  Accuracy:  {ml_metrics['accuracy']*100:.1f}%")
        print(f"  Precision: {ml_metrics['precision']*100:.1f}%")
        print(f"  Recall:    {ml_metrics['recall']*100:.1f}%")
        print(f"  F1:        {ml_metrics['f1']*100:.1f}%")
        print(f"  TP={ml_metrics['tp']} FP={ml_metrics['fp']} TN={ml_metrics['tn']} FN={ml_metrics['fn']}")
    except Exception as e:
        print(f"\n[ML detector skipped — {e}]")
        print("  Train the model first: python detector/ml_model.py")

    # hybrid
    try:
        from detector.hybrid import detect as hybrid_detect
        print("\n=== Hybrid Detector (rules + ML) ===")
        hybrid_preds = [hybrid_detect(t)["risk"] for t in texts]
        hybrid_metrics = score(hybrid_preds, labels)
        print(f"  Accuracy:  {hybrid_metrics['accuracy']*100:.1f}%")
        print(f"  Precision: {hybrid_metrics['precision']*100:.1f}%")
        print(f"  Recall:    {hybrid_metrics['recall']*100:.1f}%")
        print(f"  F1:        {hybrid_metrics['f1']*100:.1f}%")
        print(f"  TP={hybrid_metrics['tp']} FP={hybrid_metrics['fp']} TN={hybrid_metrics['tn']} FN={hybrid_metrics['fn']}")
    except Exception as e:
        print(f"\n[Hybrid skipped — {e}]")

    # false positives breakdown (rule-based)
    print("\n--- Rule-based False Positives (safe prompts flagged) ---")
    fps = [(t, p) for t, p, l in zip(texts, rule_preds, labels) if p != "SAFE" and l == "SAFE"]
    if fps:
        for t, p in fps[:10]:
            print(f"  [{p}] {t[:80]}")
        if len(fps) > 10:
            print(f"  ... and {len(fps) - 10} more")
    else:
        print("  None — clean")

    print("\n--- Rule-based False Negatives (injections missed) ---")
    fns = [(t, p) for t, p, l in zip(texts, rule_preds, labels) if p == "SAFE" and l == "INJECTION"]
    if fns:
        for t, p in fns[:10]:
            print(f"  [missed] {t[:80]}")
        if len(fns) > 10:
            print(f"  ... and {len(fns) - 10} more")
    else:
        print("  None — clean")

if __name__ == "__main__":
    main()
