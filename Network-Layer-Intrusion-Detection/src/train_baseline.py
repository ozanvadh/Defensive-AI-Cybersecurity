"""Train and validate an interpretable Logistic Regression baseline for UNSW-NB15."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, roc_auc_score, balanced_accuracy_score)

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "data" / "processed" / "development.csv"
VAL = ROOT / "data" / "processed" / "validation.csv"
OUT = ROOT / "results" / "baseline"
MODEL = ROOT / "models"
OUT.mkdir(parents=True, exist_ok=True)
MODEL.mkdir(parents=True, exist_ok=True)

dev = pd.read_csv(DEV)
val = pd.read_csv(VAL)

excluded = {"id", "attack_cat", "label", "ct_ftp_cmd"}
features = [c for c in dev.columns if c not in excluded]
categorical = ["proto", "service", "state"]
numeric = [c for c in features if c not in categorical]

preprocessor = ColumnTransformer([
    ("numeric", StandardScaler(), numeric),
    ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, solver="lbfgs", random_state=42)),
])

pipeline.fit(dev[features], dev["label"])
pred = pipeline.predict(val[features])
prob = pipeline.predict_proba(val[features])[:, 1]

tn, fp, fn, tp = confusion_matrix(val["label"], pred).ravel()
metrics = {
    "accuracy": accuracy_score(val["label"], pred),
    "precision": precision_score(val["label"], pred),
    "recall": recall_score(val["label"], pred),
    "f1": f1_score(val["label"], pred),
    "false_positive_rate": fp / (fp + tn),
    "false_negative_rate": fn / (fn + tp),
    "roc_auc": roc_auc_score(val["label"], prob),
    "balanced_accuracy": balanced_accuracy_score(val["label"], pred),
    "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
}

category_rows = []
for category, group in val.assign(prediction=pred).groupby("attack_cat"):
    category_rows.append({
        "attack_cat": category,
        "n": len(group),
        "correct": int((group["prediction"] == group["label"]).sum()),
        "accuracy_or_detection_rate": float((group["prediction"] == group["label"]).mean()),
    })

with open(OUT / "validation_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)
pd.DataFrame(category_rows).to_csv(OUT / "validation_category_performance.csv", index=False)
joblib.dump(pipeline, MODEL / "logistic_regression_baseline.joblib")

print(json.dumps(metrics, indent=2))
