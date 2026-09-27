# Training-Only Leakage and Integrity Audit

## Scope

This audit was performed only on the official UNSW-NB15 training partition (175,341 records). The reserved official test features were not used for feature selection, model selection, hyperparameter tuning, threshold selection, or leakage analysis.

## Key Findings

### Identifier leakage

The `id` column is excluded from all predictive modeling.

Within the training partition, its Pearson correlation with the binary target is approximately **0.7272**. When IDs are divided into ten equal-frequency bins, the first two bins contain 0% attack labels while the final three contain 100% attack labels. This indicates that row/identifier ordering carries substantial information about the target and could allow a model to exploit dataset construction rather than network behavior.

### Direct target metadata

`attack_cat` is retained only for stratified descriptive analysis and attack-category evaluation. It is excluded from binary-classifier inputs because it directly describes whether a row belongs to Normal traffic or an attack family.

### Redundant features

`is_ftp_login` and `ct_ftp_cmd` are identical across every training row. To avoid carrying a perfectly redundant predictor, the initial modeling pipeline will retain `is_ftp_login` and exclude `ct_ftp_cmd`.

### Repeated predictor vectors

After removing `id`, `attack_cat`, and `label`:

- 101,040 unique predictor vectors remain among 175,341 rows.
- 84,049 rows participate in repeated predictor vectors.
- 229 repeated-feature groups, containing 940 rows, have conflicting binary labels.

Repeated rows will therefore not be blindly deduplicated. Identical exported feature vectors can correspond to different labels, and repeated flows may also represent legitimate repeated observations.

### Categorical predictors

The primary categorical network predictors are:

- `proto`
- `service`
- `state`

They require training-fitted categorical encoding. Category vocabularies must not be learned from the reserved test set.

### Sparse features

Several binary/count features, including `is_ftp_login` and `is_sm_ips_ports`, are highly sparse. Sparsity alone is not sufficient evidence for removal, so these features remain provisional predictors pending EDA and model diagnostics.

### Strong class associations

Features including `sttl` and `ct_state_ttl`, along with some protocol/state values, show strong training-set relationships with the target. They are not direct target fields and are provisionally retained, but later robustness and interpretation work should test whether models rely excessively on dataset-specific artifacts.

## Initial Feature Policy

**Excluded from model inputs:**

- `id`: identifier/order leakage risk
- `attack_cat`: direct target metadata
- `ct_ftp_cmd`: perfectly redundant with `is_ftp_login`

**Retained provisionally:**

All remaining network-flow predictors.

No further feature will be removed solely because it is strongly predictive. Any later removal must have a documented methodological reason.

## Reproducibility

The script `src/audit_training_data.py` reproduces the core integrity and leakage checks and writes machine-readable outputs under `results/training_data_audit/`.

This audit precedes validation splitting and model training. The feature policy established here should therefore be treated as a pre-modeling decision rather than a post-hoc response to test performance.
