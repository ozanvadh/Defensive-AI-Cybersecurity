# Network Layer Reproducibility Audit

## Reproducible components

The repository contains scripts for raw-data auditing, leakage analysis, group-preserving splitting, EDA, baseline training, nonlinear training, interpretation, pre-specified robustness testing, final test evaluation, and publication-figure generation.

## Data identity

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
- no post-test tuning permitted for Network Layer v1

## Captured project-machine environment

The project-machine `pip freeze` output is archived as `../network_environment.txt`.

Interpreter:

- Python 3.13.5

Key packages from that snapshot:

- scikit-learn 1.9.1
- pandas 3.0.6
- NumPy 2.5.3
- SciPy 1.18.1
- joblib 1.6.0
- Matplotlib 3.11.2

Because the environment snapshot was captured at project completion rather than automatically at the instant each artifact was trained, it is described as the captured project environment rather than proof that no package changed during the preceding modeling session.

## Independent final audit

A separate clean rerun used the preserved raw CSVs and the committed algorithms/configurations. It reproduced:

- development rows: 140,269
- validation rows: 35,072
- Logistic Regression validation metrics
- Histogram Gradient Boosting validation metrics
- Histogram Gradient Boosting permutation-importance ordering, including `sttl` mean balanced-accuracy importance of approximately 0.2731
- final Logistic Regression test metrics
- final Histogram Gradient Boosting test metrics and confusion matrix

The audit detected that an earlier written robustness-results document did not match the output of the committed robustness code. The robustness experiment was rerun from the frozen protocol and the documentation was corrected. The verified `sttl`-median condition has **69.41% balanced accuracy, 58.84% FPR, and 97.67% attack recall**.

This correction occurred without changing the pre-specified robustness transformations, model configuration, threshold, or final-test model.

## Test-set status

The official test partition is permanently consumed for Network Layer v1. A revised model informed by final-test results must not be presented as having an unbiased evaluation on the same test set.

## Reproduction boundaries

The repository records dataset hashes, preprocessing and leakage policies, fixed random seed, model configurations, evaluation protocols, verified result files, result summaries, and the captured project-machine software environment.

Exact hardware, operating-system build, low-level numerical libraries, and an automatically generated environment snapshot from the precise original training instant were not independently recorded.

## Scope

Reproducibility of the computational procedure does not imply reproducibility of real-world deployment performance. The dataset is a controlled benchmark, and the robustness transformations are diagnostic experiments rather than live-network interventions.
