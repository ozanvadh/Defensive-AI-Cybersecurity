"""Supplementary multi-seed stability analysis for the Network Layer.

Runs on development/validation data only. It never reads the consumed official
test set. These results are supplementary and must not be used to retroactively
select a new v1 final model.
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "data" / "processed" / "development.csv"
VAL = ROOT / "data" / "processed" / "validation.csv"
OUT = ROOT / "results" / "seed_stability"
OUT.mkdir(parents=True, exist_ok=True)

SEEDS = [7, 17, 29, 42, 73]

dev = pd.read_csv(DEV)
val = pd.read_csv(VAL)

excluded = {"id", "attack_cat", "label", "ct_ftp_cmd"}
features = [c for c in dev.columns if c not in excluded]
categorical = ["proto", "service", "state"]
numeric = [c for c in features if c not in categorical]


def build(seed: int) -> Pipeline:
    pre = ColumnTransformer([
        (
            "categorical",
            OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
            categorical,
        ),
        ("numeric", "passthrough", numeric),
    ])
    clf = HistGradientBoostingClassifier(
        max_iter=300,
        learning_rate=0.08,
        max_leaf_nodes=31,
        l2_regularization=1.0,
        random_state=seed,
        early_stopping=True,
        validation_fraction=0.10,
        n_iter_no_change=20,
    )
    return Pipeline([("preprocessor", pre), ("classifier", clf)])


rows = []
for seed in SEEDS:
    model = build(seed)
    model.fit(dev[features], dev["label"])
    pred = model.predict(val[features])
    prob = model.predict_proba(val[features])[:, 1]
    tn, fp, fn, tp = confusion_matrix(val["label"], pred).ravel()
    rows.append({
        "seed": seed,
        "accuracy": accuracy_score(val["label"], pred),
        "precision": precision_score(val["label"], pred),
        "recall": recall_score(val["label"], pred),
        "f1": f1_score(val["label"], pred),
        "fpr": fp / (fp + tn),
        "fnr": fn / (fn + tp),
        "balanced_accuracy": balanced_accuracy_score(val["label"], pred),
        "roc_auc": roc_auc_score(val["label"], prob),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "seed_metrics.csv", index=False)

metric_cols = [
    "accuracy", "precision", "recall", "f1", "fpr", "fnr",
    "balanced_accuracy", "roc_auc",
]
summary = {}
for metric in metric_cols:
    values = df[metric].to_numpy(dtype=float)
    summary[metric] = {
        "mean": float(values.mean()),
        "std": float(values.std(ddof=1)),
        "min": float(values.min()),
        "max": float(values.max()),
    }

with (OUT / "seed_summary.json").open("w", encoding="utf-8") as f:
    json.dump({"seeds": SEEDS, "metrics": summary}, f, indent=2)

print(df.to_string(index=False))
print(json.dumps(summary, indent=2))
print("Official test data was not read.")
