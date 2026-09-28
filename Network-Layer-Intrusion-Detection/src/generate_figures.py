"""Generate Network Layer summary figures from verified result files."""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results/figures"
OUT.mkdir(parents=True,exist_ok=True)

with open(ROOT/"results/stronger_model/validation_metrics.json") as f:
    validation=json.load(f)
with open(ROOT/"results/final_test/final_test_metrics.json") as f:
    final=json.load(f)["hist_gradient_boosting"]
with open(ROOT/"results/robustness/condition_metrics.json") as f:
    robustness=json.load(f)

data=pd.DataFrame({
 "Metric":["Accuracy","Balanced accuracy","Attack recall","False-positive rate"],
 "Validation":[validation["accuracy"],validation["balanced_accuracy"],validation["recall"],validation["false_positive_rate"]],
 "Final test":[final["accuracy"],final["balanced_accuracy"],final["recall"],final["fpr"]],
}).set_index("Metric")
ax=data.plot.bar(rot=0)
ax.set_ylabel("Rate")
ax.set_ylim(0,1)
ax.set_title("Stronger model: validation vs untouched final test")
plt.tight_layout()
plt.savefig(OUT/"validation_vs_final_test.png",dpi=300)
plt.close()

names=["reference","sttl_median","ttl_family_median","unknown_all_categoricals"]
labels=["Reference","sttl neutralized","TTL family neutralized","All categorical unknown"]
rob=pd.DataFrame({
 "Condition":labels,
 "Balanced accuracy":[robustness[n]["balanced_accuracy"] for n in names],
 "Attack recall":[robustness[n]["recall"] for n in names],
 "False-positive rate":[robustness[n]["fpr"] for n in names],
}).set_index("Condition")
ax=rob.plot.bar(rot=15)
ax.set_ylabel("Rate")
ax.set_ylim(0,1)
ax.set_title("Pre-specified robustness stress tests")
plt.tight_layout()
plt.savefig(OUT/"robustness_summary.png",dpi=300)
plt.close()

fpr=pd.Series({"Validation":validation["false_positive_rate"],"Final test":final["fpr"]})
ax=fpr.plot.bar(rot=0)
ax.set_ylabel("False-positive rate")
ax.set_ylim(0,max(.30,float(fpr.max())*1.1))
ax.set_title("Benign false-positive generalization gap")
plt.tight_layout()
plt.savefig(OUT/"false_positive_generalization_gap.png",dpi=300)
plt.close()

print(f"Saved figures to {OUT}")
