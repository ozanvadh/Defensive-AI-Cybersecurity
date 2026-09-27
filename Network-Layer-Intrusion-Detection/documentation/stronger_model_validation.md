# Nonlinear Tabular Model Validation

A Histogram Gradient Boosting classifier was trained on the 140,269-row development partition and evaluated once on the leakage-resistant 35,072-row validation partition. The official test set remains sealed.

## Configuration

- Histogram Gradient Boosting
- 300 maximum boosting iterations
- learning rate 0.08
- 31 maximum leaf nodes
- L2 regularization 1.0
- seed 42
- default 0.50 decision threshold
- ordinal encoding for `proto`, `service`, and `state`, fitted on development data only
- excluded predictors: `id`, `attack_cat`, `ct_ftp_cmd`

## Validation Results

| Metric | Result |
| --- | ---: |
| Accuracy | **95.5948%** |
| Precision | **96.0330%** |
| Recall | **97.5577%** |
| F1 | **96.7893%** |
| False-positive rate | **8.5885%** |
| False-negative rate | **2.4423%** |
| ROC AUC | **0.99290** |
| Balanced accuracy | **94.4846%** |

Confusion matrix:

| | Predicted benign | Predicted attack |
| --- | ---: | ---: |
| Actual benign | 10,239 | 962 |
| Actual attack | 583 | 23,288 |

Compared with the Logistic Regression baseline, the nonlinear model substantially reduces false positives, from 18.27% to 8.59%, while increasing accuracy, precision, F1, ROC AUC, and balanced accuracy. This improvement comes with lower attack recall: 97.56% versus 98.70%. The comparison therefore represents a real sensitivity/specificity tradeoff rather than uniform dominance.

## Category-Level Correct Classification

| Category | n | Correct rate |
| --- | ---: | ---: |
| Analysis | 421 | 89.55% |
| Backdoor | 362 | 100.00% |
| DoS | 2,523 | 99.88% |
| Exploits | 6,888 | 99.52% |
| Fuzzers | 3,713 | 86.64% |
| Generic | 7,654 | 99.97% |
| Normal | 11,201 | 91.41% |
| Reconnaissance | 2,057 | 99.90% |
| Shellcode | 228 | 98.68% |
| Worms | 25 | 100.00% |

Rare-category percentages, especially Worms, should not be interpreted as stable estimates.

## Interpretation

The stronger model cuts the baseline false-positive burden by more than half in relative terms while preserving very high overall attack recall. However, the category analysis exposes substantially weaker detection for Fuzzers and Analysis than aggregate metrics suggest. These errors are a priority for interpretation and robustness analysis.

No official test-set performance is reported here, and the test partition must remain unavailable to model-development decisions.
