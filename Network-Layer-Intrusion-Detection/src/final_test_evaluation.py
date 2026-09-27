"""Final one-time evaluation of frozen Network Layer models on official UNSW-NB15 test data.

Run only after all model-development and robustness decisions are frozen.
No tuning may follow from these results.
"""
from pathlib import Path
import json, joblib, pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
 confusion_matrix, roc_auc_score, balanced_accuracy_score)

ROOT=Path(__file__).resolve().parents[1]
TEST=ROOT/"data/raw/UNSW_NB15_testing-set.csv"
OUT=ROOT/"results/final_test"; OUT.mkdir(parents=True,exist_ok=True)
test=pd.read_csv(TEST)
excluded={"id","attack_cat","label","ct_ftp_cmd"}
features=[c for c in test.columns if c not in excluded]

def evaluate(name,path):
    model=joblib.load(path)
    pred=model.predict(test[features]); prob=model.predict_proba(test[features])[:,1]
    tn,fp,fn,tp=confusion_matrix(test.label,pred).ravel()
    m={"accuracy":accuracy_score(test.label,pred),"precision":precision_score(test.label,pred),
       "recall":recall_score(test.label,pred),"f1":f1_score(test.label,pred),
       "false_positive_rate":fp/(fp+tn),"false_negative_rate":fn/(fn+tp),
       "roc_auc":roc_auc_score(test.label,prob),
       "balanced_accuracy":balanced_accuracy_score(test.label,pred),
       "tn":int(tn),"fp":int(fp),"fn":int(fn),"tp":int(tp)}
    cats=[]
    for cat,g in test.assign(prediction=pred).groupby("attack_cat"):
        cats.append({"attack_cat":cat,"n":len(g),
          "correct_rate":float((g.prediction==g.label).mean())})
    pd.DataFrame(cats).to_csv(OUT/f"{name}_category_performance.csv",index=False)
    return m

results={
 "logistic_regression":evaluate("logistic_regression",ROOT/"models/logistic_regression_baseline.joblib"),
 "hist_gradient_boosting":evaluate("hist_gradient_boosting",ROOT/"models/hist_gradient_boosting.joblib")
}
with open(OUT/"final_test_metrics.json","w") as f: json.dump(results,f,indent=2)
print(json.dumps(results,indent=2))
