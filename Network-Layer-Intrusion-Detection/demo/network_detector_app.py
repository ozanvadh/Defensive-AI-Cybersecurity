"""Defensive Network Layer research demo.

Loads the locally trained frozen Histogram Gradient Boosting model and classifies
UNSW-NB15-style CSV rows. This is a research prototype, not a live blocking system.
"""
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/"models/hist_gradient_boosting.joblib"
EXCLUDED={"id","attack_cat","label","ct_ftp_cmd"}

st.set_page_config(page_title="Defensive AI Network Detector",layout="wide")
st.title("Defensive AI Network Traffic Detector")
st.caption("Research prototype for pre-recorded UNSW-NB15-style network-flow data")

st.warning("This prototype is for defensive research only. It does not scan, attack, or automatically block live systems.")

if not MODEL.exists():
    st.error("Frozen model artifact not found. Run src/train_stronger_model.py first.")
    st.stop()

model=joblib.load(MODEL)
uploaded=st.file_uploader("Upload a CSV containing UNSW-NB15-style flow features",type=["csv"])

if uploaded is not None:
    df=pd.read_csv(uploaded)
    features=[c for c in df.columns if c not in EXCLUDED]
    try:
        pred=model.predict(df[features])
        prob=model.predict_proba(df[features])[:,1]
    except Exception as exc:
        st.error(f"Input columns do not match the trained model: {exc}")
        st.stop()

    out=df.copy()
    out["predicted_label"]=pred
    out["attack_probability"]=prob
    out["prediction"]=out["predicted_label"].map({0:"Benign",1:"Potential attack"})
    st.dataframe(out[["prediction","attack_probability"]].join(df),use_container_width=True)

    c1,c2,c3=st.columns(3)
    c1.metric("Rows",len(out))
    c2.metric("Predicted attacks",int(pred.sum()))
    c3.metric("Predicted benign",int((pred==0).sum()))

    st.info("Model confidence and benchmark accuracy do not guarantee correctness under distribution shift.")
