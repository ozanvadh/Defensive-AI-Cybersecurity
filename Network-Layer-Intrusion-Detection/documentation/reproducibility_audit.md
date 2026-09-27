# Network Layer Reproducibility Audit

## Reproducible components

The repository contains scripts for raw-data auditing, leakage analysis, group-preserving splitting, EDA, baseline training, nonlinear training, interpretation, pre-specified robustness testing, final test evaluation, and publication-figure generation.

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

## Captured software environment

The project-machine environment was captured after Network Layer v1 completion and archived as `../network_environment.txt`.

Interpreter:

- Python 3.13.5

Key scientific packages:

- scikit-learn 1.9.1
- pandas 3.0.6
- NumPy 2.5.3
- SciPy 1.18.1
- joblib 1.6.0
- Matplotlib 3.11.2

The archived environment file contains the complete `pip freeze` output supplied from the project machine. Because the environment snapshot was captured at project completion rather than automatically recorded at the instant each artifact was trained, it should be described as the captured project environment rather than proof that no package changed during the preceding modeling session.

## Test-set status

The official test partition is now permanently consumed for Network Layer v1. A revised model informed by final-test results must not be presented as having an unbiased evaluation on the same test set.

## Reproduction boundaries

The repository records dataset hashes, preprocessing and leakage policies, fixed random seed, model configurations, evaluation protocols, result summaries, and the captured software environment. These substantially strengthen computational reproducibility.

Some limitations remain. Exact hardware, operating-system build, low-level numerical libraries, and an automatically generated environment snapshot from the precise training instant were not independently recorded. Small numerical differences may therefore be possible across systems even when package versions match.

## Scope

Reproducibility of the computational procedure does not imply reproducibility of real-world deployment performance. The dataset is a controlled benchmark, and the robustness transformations are diagnostic experiments rather than live-network interventions.
