# Final Untouched UNSW-NB15 Test Evaluation

## Test-set consumption policy

The official 82,332-row UNSW-NB15 test partition was reserved throughout development. Model selection, preprocessing choices, feature exclusions, robustness experiments, and interpretation work were completed before this final evaluation.

The test set is now considered **consumed**. These results must not be used for further hyperparameter tuning, threshold tuning, feature selection, or model selection. Any future revised model would require a new independent evaluation set for an unbiased final estimate.

## Final results

| Metric | Logistic Regression | Histogram Gradient Boosting |
| --- | ---: | ---: |
| Accuracy | 80.94% | **87.38%** |
| Precision | 75.33% | **82.12%** |
| Recall | 97.23% | **98.53%** |
| F1 | 84.89% | **89.58%** |
| False-positive rate | 39.01% | **26.29%** |
| False-negative rate | 2.77% | **1.47%** |
| Balanced accuracy | 79.11% | **86.12%** |
| ROC AUC | 95.59% | **98.48%** |

### Logistic Regression confusion matrix

- TN: 22,565
- FP: 14,435
- FN: 1,254
- TP: 44,078

### Histogram Gradient Boosting confusion matrix

- TN: 27,273
- FP: 9,727
- FN: 666
- TP: 44,666

## Validation-to-test generalization

The stronger model's validation accuracy was 95.59%, but final test accuracy was 87.38%. Balanced accuracy declined from 94.48% to 86.12%.

The largest operational change is the benign false-positive rate:

**8.59% on validation → 26.29% on the official test set.**

Attack recall remained extremely high and actually increased slightly:

**97.56% → 98.53%.**

This means the primary final-test failure is not inability to recognize attacks overall. It is substantially poorer discrimination of benign traffic under the official train/test shift.

For Logistic Regression, the same pattern is even stronger: FPR rises from 18.27% on validation to 39.01% on the final test set.

## Stronger-model category results

| Category | n | Correct classification / detection |
| --- | ---: | ---: |
| Analysis | 677 | 95.57% |
| Backdoor | 583 | 100.00% |
| DoS | 4,089 | 99.85% |
| Exploits | 11,132 | 99.42% |
| Fuzzers | 6,062 | 90.80% |
| Generic | 18,871 | 99.99% |
| Normal | 37,000 | **73.71%** |
| Reconnaissance | 3,496 | 99.89% |
| Shellcode | 378 | 99.47% |
| Worms | 44 | 100.00% |

The 100% Worm point estimate is based on only 44 test observations and should not be interpreted as proof of perfect generalization.

## Interpretation

The final test results reinforce the central Network Layer finding: strong internal validation performance does not guarantee equally strong behavior under a shifted evaluation distribution.

The nonlinear model preserves excellent overall attack sensitivity, but its false-positive rate triples relative to validation, from 8.59% to 26.29%. In an operational intrusion-detection setting, falsely flagging more than one quarter of benign flows would represent a substantial alert burden.

This final-test degradation is distinct from the pre-specified TTL ablation experiments. The controlled ablations demonstrated sensitivity to TTL-related information, while the official test evaluation demonstrates a broader validation-to-test generalization gap. The study should not claim that TTL dependence alone caused the final-test gap without additional evidence.

## Finality

No model-development decision will be changed in response to these test results. The official test partition is permanently consumed for this version of the Network Layer.
