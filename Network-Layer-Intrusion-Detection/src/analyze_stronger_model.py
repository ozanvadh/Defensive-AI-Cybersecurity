"""Interpret the frozen nonlinear validation model using permutation importance and error analysis."""
from pathlib import Path
import joblib, pandas as pd
from sklearn.inspection import permutation_importance

ROOT=Path(__file__).resolve().parents[1]
VAL=ROOT/"data/processed/validation.csv"
MODEL=ROOT/"models/hist_gradient_boosting.joblib"
OUT=ROOT/"results/stronger_model/interpretation"; OUT.mkdir(parents=True,exist_ok=True)

val=pd.read_csv(VAL); model=joblib.load(MODEL)
excluded={"id","attack_cat","label","ct_ftp_cmd"}
features=[c for c in val.columns if c not in excluded]
pred=model.predict(val[features]); prob=model.predict_proba(val[features])[:,1]

pi=permutation_importance(model,val[features],val.label,n_repeats=5,random_state=42,
                          scoring="balanced_accuracy",n_jobs=-1)
importance=pd.DataFrame({"feature":features,"mean_importance":pi.importances_mean,
                         "std_importance":pi.importances_std}).sort_values("mean_importance",ascending=False)
importance.to_csv(OUT/"permutation_importance.csv",index=False)

errors=val[["attack_cat","label"]].copy()
errors["prediction"]=pred; errors["attack_probability"]=prob
attack=errors[errors.label.eq(1)]
category=(attack.groupby("attack_cat").agg(n=("label","size"),
          misses=("prediction",lambda x:int((x==0).sum()))))
category["miss_rate"]=category["misses"]/category["n"]
category.to_csv(OUT/"attack_family_miss_rates.csv")

print(importance.head(15).to_string(index=False))
print("\nAttack-family misses:")
print(category.sort_values("miss_rate",ascending=False).to_string())
