"""Generate publication-style Network Layer summary figures from recorded result files."""
from pathlib import Path
import json, pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results/figures"; OUT.mkdir(parents=True,exist_ok=True)

# Validation vs final test comparison.
data=pd.DataFrame({
 "Metric":["Accuracy","Balanced accuracy","Attack recall","False-positive rate"],
 "Validation":[.955948,.944846,.975577,.085885],
 "Final test":[.8738,.8612,.9853,.2629],
}).set_index("Metric")
ax=data.plot.bar(rot=0)
ax.set_ylabel("Rate")
ax.set_ylim(0,1)
ax.set_title("Stronger model: validation vs untouched final test")
plt.tight_layout(); plt.savefig(OUT/"validation_vs_final_test.png",dpi=300); plt.close()

# Robustness conditions.
rob=pd.DataFrame({
 "Condition":["Reference","sttl neutralized","TTL family neutralized","All categorical unknown"],
 "Balanced accuracy":[.9448,.8337,.8228,.9018],
 "Attack recall":[.9756,.8104,.7895,.9472],
}).set_index("Condition")
ax=rob.plot.bar(rot=15)
ax.set_ylabel("Rate"); ax.set_ylim(0,1)
ax.set_title("Pre-specified robustness stress tests")
plt.tight_layout(); plt.savefig(OUT/"robustness_summary.png",dpi=300); plt.close()

# False-positive comparison.
fpr=pd.Series({"Validation":.0859,"Final test":.2629})
ax=fpr.plot.bar(rot=0)
ax.set_ylabel("False-positive rate"); ax.set_ylim(0,.30)
ax.set_title("Benign false-positive generalization gap")
plt.tight_layout(); plt.savefig(OUT/"false_positive_generalization_gap.png",dpi=300); plt.close()

print(f"Saved figures to {OUT}")
