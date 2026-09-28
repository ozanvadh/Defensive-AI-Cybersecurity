"""Supplementary DistilBERT multi-seed stability analysis.

This script retrains on the existing Human Layer training split and evaluates
validation only. It never reads the consumed historical test or synthetic
evaluation set.

Expected runtime is substantial on GPU hardware.
"""

from pathlib import Path
import json
import random

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

ROOT = Path(__file__).resolve().parents[1]
TRAIN = ROOT / "data" / "processed" / "train.csv"
VAL = ROOT / "data" / "processed" / "validation.csv"
OUT = ROOT / "results" / "transformer_seed_stability"
OUT.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "distilbert-base-uncased"
SEEDS = [7, 17, 29, 42, 73]


def metrics(eval_pred):
    logits, labels = eval_pred
    pred = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, pred),
        "precision": precision_score(labels, pred, zero_division=0),
        "recall": recall_score(labels, pred, zero_division=0),
        "f1": f1_score(labels, pred, zero_division=0),
    }


train_df = pd.read_csv(TRAIN)[["body", "label"]].dropna()
val_df = pd.read_csv(VAL)[["body", "label"]].dropna()
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize(batch):
    return tokenizer(batch["body"], truncation=True, max_length=256)


train_ds = Dataset.from_pandas(train_df, preserve_index=False).map(tokenize, batched=True)
val_ds = Dataset.from_pandas(val_df, preserve_index=False).map(tokenize, batched=True)

rows = []
for seed in SEEDS:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    run_dir = OUT / f"seed_{seed}"
    args = TrainingArguments(
        output_dir=str(run_dir),
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=2,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        fp16=torch.cuda.is_available(),
        seed=seed,
        data_seed=seed,
        report_to=[],
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        processing_class=tokenizer,
        compute_metrics=metrics,
    )
    trainer.train()
    result = trainer.evaluate()
    rows.append({
        "seed": seed,
        "accuracy": result["eval_accuracy"],
        "precision": result["eval_precision"],
        "recall": result["eval_recall"],
        "f1": result["eval_f1"],
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "seed_metrics.csv", index=False)

summary = {}
for metric in ["accuracy", "precision", "recall", "f1"]:
    x = df[metric].to_numpy(float)
    summary[metric] = {
        "mean": float(x.mean()),
        "std": float(x.std(ddof=1)),
        "min": float(x.min()),
        "max": float(x.max()),
    }

with (OUT / "seed_summary.json").open("w", encoding="utf-8") as f:
    json.dump({"seeds": SEEDS, "metrics": summary}, f, indent=2)

print(df.to_string(index=False))
print(json.dumps(summary, indent=2))
print("Consumed historical test and synthetic evaluation data were not read.")
