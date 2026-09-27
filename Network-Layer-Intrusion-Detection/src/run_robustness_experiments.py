"""Execute the pre-specified Network Layer robustness protocol on validation only."""
from pathlib import Path
import json, math, joblib, pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
 confusion_matrix, roc_auc_score, balanced_accuracy_score)

ROOT=Path(__file__).resolve().parents[1]
dev=pd.read_csv(ROOT/"data/processed/development.csv")
val=pd.read_csv(ROOT/"data/processed/validation.csv")
model=joblib.load(ROOT/"models/hist_gradient_boosting.joblib")
OUT=ROOT/"results/robustness"; OUT.mkdir(parents=True,exist_ok=True)
excluded={"id","attack_cat","label","ct_ftp_cmd"}
features=[c for c in val.columns if c not in excluded]

def metrics(frame):
    y=frame.label; p=model.predict(frame[features]); q=model.predict_proba(frame[features])[:,1]
    tn,fp,fn,tp=confusion_matrix(y,p).ravel()
    return {"accuracy":accuracy_score(y,p),"precision":precision_score(y,p),
      "recall":recall_score(y,p),"f1":f1_score(y,p),"fpr":fp/(fp+tn),
      "fnr":fn/(fn+tp),"balanced_accuracy":balanced_accuracy_score(y,p),
      "roc_auc":roc_auc_score(y,q),"tn":int(tn),"fp":int(fp),"fn":int(fn),"tp":int(tp)}

conditions={"reference":val.copy()}
a=val.copy(); a["sttl"]=dev["sttl"].median(); conditions["sttl_median"]=a
b=val.copy()
for c in ["sttl","dttl","ct_state_ttl"]: b[c]=dev[c].median()
conditions["ttl_family_median"]=b
for c in ["proto","service","state"]:
    x=val.copy(); x[c]="__UNSEEN_CATEGORY__"; conditions[f"unknown_{c}"]=x
x=val.copy()
for c in ["proto","service","state"]: x[c]="__UNSEEN_CATEGORY__"
conditions["unknown_all_categoricals"]=x

results={name:metrics(frame) for name,frame in conditions.items()}
pd.DataFrame(results).T.to_csv(OUT/"condition_metrics.csv")
with open(OUT/"condition_metrics.json","w") as f: json.dump(results,f,indent=2)

# Frozen model attack-family Wilson intervals on unmodified validation.
pred=model.predict(val[features])
z=1.959963984540054
rows=[]
for cat,g in val[val.label.eq(1)].assign(prediction=pred[val.label.eq(1)]).groupby("attack_cat"):
    n=len(g); k=int(g.prediction.sum()); phat=k/n
    den=1+z*z/n; center=(phat+z*z/(2*n))/den
    half=z*math.sqrt(phat*(1-phat)/n+z*z/(4*n*n))/den
    rows.append({"attack_cat":cat,"n":n,"detected":k,"missed":n-k,
                 "detection_rate":phat,"wilson95_low":center-half,"wilson95_high":center+half})
pd.DataFrame(rows).to_csv(OUT/"attack_family_wilson_intervals.csv",index=False)
print(pd.DataFrame(results).T.to_string())
