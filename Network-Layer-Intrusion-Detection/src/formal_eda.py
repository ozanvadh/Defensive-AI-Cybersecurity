"""Formal development-only EDA for the UNSW-NB15 Network Layer."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "development.csv"
OUT = ROOT / "results" / "eda"
FIG = OUT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)
excluded = {"id", "attack_cat", "label", "ct_ftp_cmd"}
features = [c for c in df.columns if c not in excluded]
categorical = ["proto", "service", "state"]
numeric = [c for c in features if c not in categorical]

# Machine-readable summaries.
df["label"].value_counts().rename_axis("label").to_csv(OUT / "class_counts.csv")
df["attack_cat"].value_counts().rename_axis("attack_cat").to_csv(OUT / "attack_category_counts.csv")
pd.DataFrame({
    "feature": features,
    "dtype": [str(df[c].dtype) for c in features],
    "unique_values": [df[c].nunique(dropna=False) for c in features],
    "zero_fraction": [(df[c].eq(0).mean() if c in numeric else np.nan) for c in features],
}).to_csv(OUT / "feature_summary.csv", index=False)

df[numeric].describe(percentiles=[.01,.05,.25,.5,.75,.95,.99]).T.to_csv(
    OUT / "numeric_descriptive_statistics.csv"
)
df[numeric].skew().sort_values(key=abs, ascending=False).rename("skew").to_csv(
    OUT / "numeric_skew.csv"
)
corr = (
    df[numeric + ["label"]].corr(numeric_only=True)["label"]
      .drop("label").sort_values(key=abs, ascending=False)
)
corr.rename("pearson_r_with_label").to_csv(OUT / "numeric_label_correlations.csv")

for c in categorical:
    pd.crosstab(df[c], df["label"], normalize="index").to_csv(OUT / f"{c}_label_rates.csv")

# Publication-style exploratory figures.
ax = df["label"].map({0:"Benign",1:"Attack"}).value_counts().plot.bar()
ax.set_title("Development-set binary class distribution")
ax.set_xlabel("")
ax.set_ylabel("Records")
plt.tight_layout()
plt.savefig(FIG / "binary_class_distribution.png", dpi=300)
plt.close()

ax = df["attack_cat"].value_counts().sort_values().plot.barh()
ax.set_title("Development-set traffic categories")
ax.set_xlabel("Records")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(FIG / "attack_category_distribution.png", dpi=300)
plt.close()

top = corr.head(12).sort_values()
ax = top.plot.barh()
ax.set_title("Strongest numerical associations with binary label")
ax.set_xlabel("Pearson correlation")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(FIG / "top_numeric_label_correlations.png", dpi=300)
plt.close()

print(f"rows={len(df)}")
print(f"attack_rate={df['label'].mean():.12f}")
print(f"categorical_cardinalities={ {c: int(df[c].nunique()) for c in categorical} }")
print("top_numeric_label_correlations:")
print(corr.head(12))
print("most_skewed_numeric_features:")
print(df[numeric].skew().sort_values(key=abs, ascending=False).head(10))
