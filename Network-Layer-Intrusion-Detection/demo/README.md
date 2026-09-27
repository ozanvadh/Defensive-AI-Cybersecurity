# Network Layer Defensive Demo

This Streamlit prototype applies the locally trained frozen Histogram Gradient Boosting classifier to **pre-recorded UNSW-NB15-style CSV rows**.

It is intentionally not a live network scanner or blocking tool.

## Run locally

From `Network-Layer-Intrusion-Detection`:

```powershell
python -m pip install -r demo/requirements.txt
streamlit run demo/network_detector_app.py
```

The app expects `models/hist_gradient_boosting.joblib`, produced by `src/train_stronger_model.py`.

The uploaded CSV must contain the same modeling feature columns used during training. Metadata columns such as `id`, `attack_cat`, `label`, and `ct_ftp_cmd` are ignored if present.

## Interpretation

The app reports the binary prediction and attack probability. It also displays a warning that model confidence does not establish correctness under distribution shift.

This is a research demonstration, not a production intrusion-detection or automated blocking system.
