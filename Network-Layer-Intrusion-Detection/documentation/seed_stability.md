# Network Multi-Seed Stability Supplement

## Purpose

This is a **post-hoc supplementary stability analysis** of the stronger Histogram Gradient Boosting model.

It was added during publication preparation after the primary v1 experiments were complete. It does not reopen or reuse the consumed official test partition. It evaluates the same leakage-resistant development/validation split only.

## Seeds

Predeclared supplementary seed set:

`[7, 17, 29, 42, 73]`

All model hyperparameters were held fixed:

- max iterations: 300
- learning rate: 0.08
- max leaf nodes: 31
- L2 regularization: 1.0
- early stopping: enabled
- validation fraction: 0.10
- no threshold tuning

## Environment Note

This supplementary run used scikit-learn **1.8.0** in the independent audit environment rather than the captured project-machine scikit-learn 1.9.1 environment.

Importantly, the seed-42 run reproduced the already verified v1 validation metrics exactly to the precision recorded in the project. This does not prove complete cross-version equivalence, but it provides a direct compatibility check for the primary seed.

## Results

| Seed | Accuracy | Recall | FPR | Balanced accuracy | ROC AUC |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 7 | 95.45% | 97.42% | 8.76% | 94.33% | 99.28% |
| 17 | 95.46% | 97.40% | 8.67% | 94.36% | 99.29% |
| 29 | 95.51% | 97.58% | 8.90% | 94.34% | 99.28% |
| 42 | 95.59% | 97.56% | 8.59% | 94.48% | 99.29% |
| 73 | 95.47% | 97.52% | 8.91% | 94.31% | 99.27% |

Across the five seeds:

| Metric | Mean | SD | Min | Max |
| --- | ---: | ---: | ---: | ---: |
| Accuracy | 95.50% | 0.06 pp | 95.45% | 95.59% |
| Recall | 97.50% | 0.08 pp | 97.40% | 97.58% |
| FPR | 8.77% | 0.14 pp | 8.59% | 8.91% |
| Balanced accuracy | 94.37% | 0.07 pp | 94.31% | 94.48% |
| ROC AUC | 99.28% | 0.01 pp | 99.27% | 99.29% |

## Interpretation

The internal validation result is not highly sensitive to the five tested random seeds. The observed variation is small relative to the much larger distribution-shift effects documented elsewhere in the Network Layer.

For example:

- mean validation FPR across seeds: **8.77%**
- official-test FPR for the frozen seed-42 model: **26.29%**
- `sttl`-neutralized FPR: **58.84%**
- TTL-family-neutralized FPR: **84.07%**

This strengthens the interpretation that the large robustness and official-test gaps are not plausibly explained by ordinary random-seed variation in the internal HGB fit.

## Claim Boundary

This is a post-hoc validation-stability analysis, not a new final-test experiment.

The official test remains consumed. The multi-seed results may be used to discuss internal training stability, but they must not be used to choose a new seed and then re-evaluate the same official test as if it were untouched.
