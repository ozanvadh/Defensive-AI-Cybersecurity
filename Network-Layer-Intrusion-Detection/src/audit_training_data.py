"""Training-only UNSW-NB15 integrity and leakage audit.

This script must be run only on the official training partition. It does not
read the reserved official test partition.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRAIN = ROOT / "data" / "raw" / "UNSW_NB15_training-set.csv"
OUT = ROOT / "results" / "training_data_audit"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TRAIN)
target = "label"
metadata = ["id", "attack_cat"]
predictors = [c for c in df.columns if c not in metadata + [target]]

summary = []
summary.append(f"rows={len(df)}")
summary.append(f"columns={len(df.columns)}")
summary.append(f"missing_values={int(df.isna().sum().sum())}")
summary.append(f"exact_duplicate_rows={int(df.duplicated().sum())}")
summary.append(f"id_label_correlation={df['id'].corr(df[target]):.12f}")
summary.append(f"is_ftp_login_equals_ct_ftp_cmd={bool((df['is_ftp_login'] == df['ct_ftp_cmd']).all())}")

numeric = df[predictors].select_dtypes(include=np.number)
summary.append(f"infinite_numeric_values={int(np.isinf(numeric.to_numpy()).sum())}")

X = df[predictors]
summary.append(f"unique_predictor_vectors={len(X.drop_duplicates())}")
summary.append(f"rows_in_repeated_predictor_vectors={int(X.duplicated(keep=False).sum())}")

groups = df.groupby(predictors, dropna=False)[target].agg(["size", "nunique"])
conflicting = groups[(groups["size"] > 1) & (groups["nunique"] > 1)]
summary.append(f"conflicting_label_repeated_groups={len(conflicting)}")
summary.append(f"rows_in_conflicting_label_repeated_groups={int(conflicting['size'].sum())}")

categorical = df[predictors].select_dtypes(exclude=np.number).columns.tolist()
summary.append(f"categorical_predictors={categorical}")

id_deciles = (
    df.assign(id_decile=pd.qcut(df["id"], 10, labels=False, duplicates="drop"))
      .groupby("id_decile", observed=True)[target]
      .agg(["count", "mean"])
      .rename(columns={"mean": "attack_rate"})
)
id_deciles.to_csv(OUT / "id_decile_attack_rates.csv")

cardinality = pd.DataFrame({
    "feature": predictors,
    "dtype": [str(df[c].dtype) for c in predictors],
    "unique_values": [df[c].nunique(dropna=False) for c in predictors],
})
cardinality.to_csv(OUT / "feature_cardinality.csv", index=False)

with open(OUT / "audit_summary.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(summary) + "\n")

print("\n".join(summary))
print(f"\nSaved audit outputs to: {OUT}")
