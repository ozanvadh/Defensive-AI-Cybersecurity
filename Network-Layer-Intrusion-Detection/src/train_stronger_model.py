"""Train a nonlinear histogram gradient-boosting model on UNSW-NB15 development data."""
from pathlib import Path
import json, joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, roc_auc_score, balanced_accuracy_score)

ROOT=Path(__file__).resolve().parents[1]
dev=pd.read_csv(ROOT/"data/processed/development.csv")
val=pd.read_csv(ROOT/"data/processed/validation.csv")
OUT=ROOT/"results/stronger_model"; OUT.mkdir(parents=True,exist_ok=True)
MODELS=ROOT/"models"; MODELS.mkdir(parents=True,exist_ok=True)

excluded={"id","attack_cat","label","ct_ftp_cmd"}
features=[c for c in dev.columns if c not in excluded]
categorical=["proto","service","state"]
numeric=[c for c in features if c not in categorical]

pre=ColumnTransformer([
 ("categorical",OrdinalEncoder(handle_unknown="use_encoded_value",unknown_value=-1),categorical),
 ("numeric","passthrough",numeric)
])
clf=HistGradientBoostingClassifier(max_iter=300,learning_rate=0.08,max_leaf_nodes=31,
 l2_regularization=1.0,random_state=42,early_stopping=True,validation_fraction=0.10,
 n_iter_no_change=20)
pipe=Pipeline([("preprocessor",pre),("classifier",clf)])
pipe.fit(dev[features],dev["label"])
pred=pipe.predict(val[features]); prob=pipe.predict_proba(val[features])[:,1]
tn,fp,fn,tp=confusion_matrix(val["label"],pred).ravel()
metrics={"accuracy":accuracy_score(val.label,pred),"precision":precision_score(val.label,pred),
"recall":recall_score(val.label,pred),"f1":f1_score(val.label,pred),
"false_positive_rate":fp/(fp+tn),"false_negative_rate":fn/(fn+tp),
"roc_auc":roc_auc_score(val.label,prob),"balanced_accuracy":balanced_accuracy_score(val.label,pred),
"tn":int(tn),"fp":int(fp),"fn":int(fn),"tp":int(tp),"iterations":int(clf.n_iter_)}
with open(OUT/"validation_metrics.json","w") as f: json.dump(metrics,f,indent=2)
rows=[]
for cat,g in val.assign(prediction=pred).groupby("attack_cat"):
 rows.append({"attack_cat":cat,"n":len(g),"correct_rate":float((g.prediction==g.label).mean())})
pd.DataFrame(rows).to_csv(OUT/"validation_category_performance.csv",index=False)
joblib.dump(pipe,MODELS/"hist_gradient_boosting.joblib")
print(json.dumps(metrics,indent=2))
