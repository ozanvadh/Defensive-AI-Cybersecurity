"""Create leakage-resistant development/validation partitions from UNSW-NB15 training data.

Identical modeling predictor vectors are kept entirely within one partition.
The official UNSW-NB15 testing set is never read by this script.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
VALIDATION_FRACTION = 0.20

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "UNSW_NB15_training-set.csv"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)
model_features = [c for c in df.columns if c not in {"id", "attack_cat", "label", "ct_ftp_cmd"}]

# Deterministic row hashes represent complete modeling predictor vectors.
row_hash = pd.util.hash_pandas_object(df[model_features], index=False)
group_stats = (
    pd.DataFrame({"group_hash": row_hash, "label": df["label"]})
    .groupby("group_hash")
    .agg(n=("label", "size"), attacks=("label", "sum"))
)

# Preserve groups with identical predictors. Stratify group assignment by whether
# a repeated vector is all-normal, all-attack, or contains conflicting labels.
group_type = np.where(
    group_stats["attacks"].eq(0), "normal",
    np.where(group_stats["attacks"].eq(group_stats["n"]), "attack", "mixed")
)

rng = np.random.default_rng(SEED)
validation_hashes = set()

for _, subset in group_stats.groupby(group_type):
    hashes = subset.index.to_numpy().copy()
    rng.shuffle(hashes)
    target_rows = subset["n"].sum() * VALIDATION_FRACTION
    selected_rows = 0
    for group_hash in hashes:
        if selected_rows >= target_rows:
            break
        validation_hashes.add(group_hash)
        selected_rows += int(group_stats.loc[group_hash, "n"])

is_validation = row_hash.isin(validation_hashes)
development = df.loc[~is_validation].copy()
validation = df.loc[is_validation].copy()

# Verify that no complete modeling predictor vector crosses partitions.
dev_hashes = set(pd.util.hash_pandas_object(development[model_features], index=False))
val_hashes = set(pd.util.hash_pandas_object(validation[model_features], index=False))
overlap = dev_hashes & val_hashes
assert not overlap, f"Predictor-vector leakage detected: {len(overlap)} shared groups"

development.to_csv(OUT / "development.csv", index=False)
validation.to_csv(OUT / "validation.csv", index=False)

print(f"seed={SEED}")
print(f"development_rows={len(development)}")
print(f"validation_rows={len(validation)}")
print(f"development_attack_rate={development['label'].mean():.12f}")
print(f"validation_attack_rate={validation['label'].mean():.12f}")
print(f"cross_partition_predictor_groups={len(overlap)}")
print("\nDevelopment attack categories:")
print(development["attack_cat"].value_counts())
print("\nValidation attack categories:")
print(validation["attack_cat"].value_counts())
