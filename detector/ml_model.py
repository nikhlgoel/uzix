"""
ML-based prompt injection classifier — Phase 2
Uses TF-IDF + Logistic Regression (scikit-learn)
Trains on dataset/normal.csv + dataset/injections.csv
Saves model to detector/model.pkl

NOTE: preprocessing is applied during training AND inference.
This was the F-009 mismatch. Fixed: both paths now see the same text.
"""

import os
import csv
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from detector.preprocessor import preprocess

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")
MODEL_CACHE = None


def load_dataset():
    texts, labels = [], []

    for filename, label in [("normal.csv", 0), ("injections.csv", 1)]:
        filepath = os.path.join(DATASET_DIR, filename)
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = row.get("prompt", "").strip().strip('"')
                if text:
                    # preprocess at training time — same as inference
                    texts.append(preprocess(text))
                    labels.append(label)

    return texts, labels


def train():
    global MODEL_CACHE
    print("Loading dataset...")
    texts, labels = load_dataset()
    print(f"  Total samples: {len(texts)} ({labels.count(0)} normal, {labels.count(1)} injection)")

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print("Fitting TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression classifier...")
    clf = LogisticRegression(max_iter=1000, C=1.0, solver="lbfgs")
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["normal", "injection"]))

    # Save model and vectorizer
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    MODEL_CACHE = (clf, vectorizer)
    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Vectorizer saved to {VECTORIZER_PATH}")
    return clf, vectorizer


def model_is_available() -> bool:
    return os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)


def load_model(force_reload: bool = False):
    global MODEL_CACHE
    if MODEL_CACHE is not None and not force_reload:
        return MODEL_CACHE

    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Model not trained yet. Run: python detector/ml_model.py")
    with open(MODEL_PATH, "rb") as f:
        clf = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    MODEL_CACHE = (clf, vectorizer)
    return MODEL_CACHE


def predict(text: str) -> dict:
    """
    Returns risk level and confidence using the trained ML model.
    Preprocesses input first — consistent with how the model was trained.
    """
    clf, vectorizer = load_model()
    cleaned = preprocess(text)
    vec = vectorizer.transform([cleaned])
    label = clf.predict(vec)[0]
    proba = clf.predict_proba(vec)[0]
    confidence = round(float(max(proba)) * 100, 2)

    if label == 1:
        risk = "DANGEROUS" if confidence >= 85 else "SUSPICIOUS"
    else:
        risk = "SAFE"

    return {
        "risk": risk,
        "confidence": confidence,
        "model": "ml"
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "predict":
        prompt = " ".join(sys.argv[2:]) or input("Enter prompt: ")
        result = predict(prompt)
        print(f"Risk: {result['risk']} | Confidence: {result['confidence']}%")
    else:
        train()
