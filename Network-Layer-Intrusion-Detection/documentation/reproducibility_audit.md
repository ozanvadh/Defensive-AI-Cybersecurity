# Network Layer Reproducibility Audit

## Reproducible components

The repository contains scripts for raw-data auditing, leakage analysis, group-preserving splitting, EDA, baseline training, nonlinear training, interpretation, pre-specified robustness testing, and final test evaluation.

## Data identity

Official raw modeling files were preserved outside version-controlled source code and fingerprinted before transformation.

- Training: 175,341 rows, 32,293,018 bytes, SHA-256 `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`
- Testing: 82,332 rows, 15,380,800 bytes, SHA-256 `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559`

## Frozen decisions

- random seed: 42
- `id` excluded for identifier/order leakage risk
- `attack_cat` excluded from model inputs
- `ct_ftp_cmd` excluded as perfectly redundant with `is_ftp_login`
- identical modeling predictor vectors kept within one development/validation partition
- default 0.50 classification threshold retained
- robustness protocol committed before robustness execution
- official test consumed only after development decisions were frozen
- no post-test tuning permitted for this version

## Test-set status

The official test partition is now permanently consumed for Network Layer v1. A revised model informed by final-test results must not be presented as having an unbiased evaluation on the same test set.

## Remaining environment requirement

Exact package versions from the machine on which the final model artifacts were trained should be archived if they have not already been captured. Repository scripts specify the algorithms and fixed seeds, but exact library versions are necessary for the strongest environment-level reproducibility claim.

## Scope

Reproducibility of the computational procedure does not imply reproducibility of real-world deployment performance. The dataset is a controlled benchmark, and the robustness transformations are diagnostic experiments rather than live-network interventions.
