"""Evaluate frozen Human Layer models on a new independent labeled email holdout.

This script performs evaluation only. It does not train, tune, calibrate, or
change decision thresholds.

Example:
    python src/evaluate_external_holdout.py \
        --input data/external/external_emails.csv \
        --text-column "Email Text" \
        --label-column "Email Type" \
        --safe-label "Safe Email" \
        --phishing-label "Phishing Email"

Requirements:
    pandas, numpy, scikit-learn, joblib, torch, transformers
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = ROOT / "models" / "baseline_tfidf_logreg.joblib"
DEFAULT_TRANSFORMER = "ozuvadh/defensive-ai-phishing-distilbert"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    den = 1 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return center - half, center + half


def expected_calibration_error(y: np.ndarray, prob: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (prob >= lo) & (prob < hi if hi < 1 else prob <= hi)
        if not mask.any():
            continue
        confidence = prob[mask].mean()
        accuracy = y[mask].mean()
        ece += mask.mean() * abs(accuracy - confidence)
    return float(ece)


def summarize(y: np.ndarray, pred: np.ndarray, prob: np.ndarray) -> dict:
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    recall_ci = wilson(int(tp), int(tp + fn))
    fpr_ci = wilson(int(fp), int(fp + tn))
    return {
        "accuracy": accuracy_score(y, pred),
        "precision": precision_score(y, pred, zero_division=0),
        "recall": recall_score(y, pred, zero_division=0),
        "f1": f1_score(y, pred, zero_division=0),
        "specificity": tn / (tn + fp),
        "false_positive_rate": fp / (fp + tn),
        "false_negative_rate": fn / (fn + tp),
        "balanced_accuracy": balanced_accuracy_score(y, pred),
        "roc_auc": roc_auc_score(y, prob),
        "brier_score": brier_score_loss(y, prob),
        "ece_10_bin": expected_calibration_error(y, prob, 10),
        "recall_wilson95": list(recall_ci),
        "fpr_wilson95": list(fpr_ci),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def transformer_probabilities(texts: list[str], model_id: str, batch_size: int) -> np.ndarray:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    probs = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        encoded = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt",
        ).to(device)
        with torch.no_grad():
            logits = model(**encoded).logits
            p = torch.softmax(logits, dim=-1)[:, 1]
        probs.extend(p.detach().cpu().numpy().tolist())
    return np.asarray(probs, dtype=float)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--text-column", required=True)
    ap.add_argument("--label-column", required=True)
    ap.add_argument("--safe-label", default="0")
    ap.add_argument("--phishing-label", default="1")
    ap.add_argument("--baseline-model", default=str(DEFAULT_BASELINE))
    ap.add_argument("--transformer-model", default=DEFAULT_TRANSFORMER)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--output-dir", default=str(ROOT / "results" / "external_validation"))
    args = ap.parse_args()

    input_path = Path(args.input)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    needed = {args.text_column, args.label_column}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df = df.dropna(subset=[args.text_column, args.label_column]).copy()
    mapping = {str(args.safe_label): 0, str(args.phishing_label): 1}
    labels = df[args.label_column].astype(str).map(mapping)
    if labels.isna().any():
        bad = sorted(df.loc[labels.isna(), args.label_column].astype(str).unique())
        raise ValueError(f"Unexpected label values: {bad}")

    y = labels.astype(int).to_numpy()
    texts = df[args.text_column].astype(str).tolist()

    manifest = {
        "input_file": input_path.name,
        "sha256": sha256(input_path),
        "rows": len(df),
        "safe": int((y == 0).sum()),
        "phishing": int((y == 1).sum()),
        "threshold": 0.50,
        "tuning_performed": False,
    }

    results = {"manifest": manifest}

    baseline_path = Path(args.baseline_model)
    if baseline_path.exists():
        baseline = joblib.load(baseline_path)
        base_prob = baseline.predict_proba(texts)[:, 1]
        base_pred = (base_prob >= 0.50).astype(int)
        results["tfidf_logistic_regression"] = summarize(y, base_pred, base_prob)
        df["baseline_probability"] = base_prob
        df["baseline_prediction"] = base_pred
    else:
        results["tfidf_logistic_regression"] = {
            "status": "not_evaluated",
            "reason": f"Frozen baseline artifact not found at {baseline_path}",
        }

    bert_prob = transformer_probabilities(texts, args.transformer_model, args.batch_size)
    bert_pred = (bert_prob >= 0.50).astype(int)
    results["distilbert"] = summarize(y, bert_pred, bert_prob)
    df["distilbert_probability"] = bert_prob
    df["distilbert_prediction"] = bert_pred

    with (out / "external_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    df.to_csv(out / "external_predictions.csv", index=False)

    print(json.dumps(results, indent=2))
    print("No model training, calibration fitting, or threshold tuning was performed.")


if __name__ == "__main__":
    main()
