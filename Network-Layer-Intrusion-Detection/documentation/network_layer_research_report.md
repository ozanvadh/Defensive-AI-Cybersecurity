# Network Layer Research Report

## Evaluating Machine-Learning Intrusion Detection Under Internal Validation, Controlled Feature Stress Tests, and Official Test Distribution Shift

### Abstract

This Network Layer investigates whether machine-learning classifiers can distinguish malicious from benign network traffic while maintaining a low false-positive rate, and whether strong internal performance persists under distribution shift. Using the official UNSW-NB15 modeling partitions, the study preserved the 82,332-row official test set until all development decisions were frozen. The 175,341-row official training partition underwent leakage auditing, group-preserving development/validation splitting, exploratory analysis, baseline modeling, nonlinear modeling, interpretation, and pre-specified robustness testing. An identifier artifact (`id`) was excluded before modeling because it strongly encoded target ordering. Logistic Regression achieved 93.28% validation accuracy and 98.70% attack recall but an 18.27% false-positive rate. Histogram Gradient Boosting improved validation accuracy to 95.59% and reduced false positives to 8.59%, while retaining 97.56% attack recall. Interpretation showed unusually strong dependence on source TTL (`sttl`). In a protocol committed before robustness execution, neutralizing only `sttl` reduced balanced accuracy from 94.48% to 83.37% and increased the false-negative rate from 2.44% to 18.96%. Neutralizing a broader TTL-derived feature family reduced balanced accuracy to 82.28%. Finally, on the untouched official test partition, the stronger model achieved 87.38% accuracy and 98.53% attack recall, but its false-positive rate increased to 26.29%. The results demonstrate that high internal validation performance can coexist with substantial feature dependence and a major benign-traffic generalization gap. The controlled ablations diagnose sensitivity but are not evidence that an attacker can produce the tested transformations in deployment.

## Research Question

**How accurately can machine-learning models distinguish malicious from benign network traffic while maintaining a low false-positive rate, and how robust are those models when evaluated under network-traffic distribution shift?**

## Dataset and Evaluation Design

UNSW-NB15 was selected as the primary Network Layer dataset. The official modeling files contain 175,341 training rows and 82,332 testing rows. Both files contain 45 observed columns.

The raw files were fingerprinted before processing:

- Training SHA-256: `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`
- Testing SHA-256: `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559`

The official test partition was reserved until the end of model development. Development and validation were derived only from the official training partition.

### Leakage audit

The audit identified `id` as unsafe for predictive modeling. Within training it had approximately 0.727 correlation with the target, and ID ranges strongly reflected class ordering. `attack_cat` was also excluded from model inputs because it directly describes Normal versus attack-family membership. `ct_ftp_cmd` was removed because it was identical to `is_ftp_login` throughout training.

Repeated predictor vectors were kept together during splitting. This produced:

- Development: 140,269 rows
- Validation: 35,072 rows
- Complete predictor-vector groups crossing development/validation: 0

This controls one important duplication pathway, although it cannot establish independence at every underlying host, session, temporal, or campaign level.

## Exploratory Analysis

The development partition was 68.06% malicious. Attack-family sizes were highly unequal, ranging from tens of thousands of Generic and Exploits observations to only 105 Worms observations in development.

Several features showed strong univariate association with the target. `sttl` was especially notable, with a development-set Pearson correlation around 0.695. Numerous timing and traffic-volume features were highly skewed, and some predictors were overwhelmingly zero-valued.

These findings were documented before model training rather than used to remove strongly predictive features post hoc.

## Models

### Logistic Regression baseline

Numerical features were standardized and categorical features were one-hot encoded using transformations fitted on development data only.

Validation results:

| Metric | Result |
| --- | ---: |
| Accuracy | 93.28% |
| Precision | 92.01% |
| Recall | 98.70% |
| F1 | 95.24% |
| False-positive rate | 18.27% |
| False-negative rate | 1.30% |
| Balanced accuracy | 90.22% |
| ROC AUC | 98.37% |

The baseline detected attacks aggressively but falsely flagged 2,046 of 11,201 benign validation flows.

### Histogram Gradient Boosting

A nonlinear Histogram Gradient Boosting classifier was then trained with the pre-established feature policy.

Validation results:

| Metric | Result |
| --- | ---: |
| Accuracy | 95.59% |
| Precision | 96.03% |
| Recall | 97.56% |
| F1 | 96.79% |
| False-positive rate | 8.59% |
| False-negative rate | 2.44% |
| Balanced accuracy | 94.48% |
| ROC AUC | 99.29% |

Compared with Logistic Regression, the nonlinear model more than halved the relative false-positive rate while sacrificing approximately 1.14 percentage points of attack recall.

## Interpretation and Error Analysis

Permutation importance using validation balanced accuracy showed that `sttl` dominated individual feature reliance. Permuting it caused roughly a 27-percentage-point decrease in balanced accuracy, far exceeding the effect of other individual features.

False negatives were also concentrated by attack family. Fuzzers had a 13.36% miss rate and Analysis a 10.45% miss rate. Together they accounted for 540 of the model's 583 malicious validation misses, or 92.62%.

Within Analysis traffic, correctly detected observations had median `sttl` 254 while missed observations had median `sttl` 62. This is consistent with TTL-related dependence but does not establish causation.

## Pre-Specified Robustness Experiments

A robustness protocol was committed before executing the stress tests. The frozen model and threshold were not modified.

| Condition | Balanced accuracy | Recall | FPR | FNR |
| --- | ---: | ---: | ---: | ---: |
| Reference | 94.48% | 97.56% | 8.59% | 2.44% |
| `sttl` neutralized | 83.37% | 81.04% | 14.29% | 18.96% |
| TTL family neutralized | 82.28% | 78.95% | 14.39% | 21.05% |
| All categoricals unknown | 90.18% | 94.72% | 14.36% | 5.28% |

Neutralizing `sttl` alone produced an 11.11-point balanced-accuracy decline. Neutralizing `sttl`, `dttl`, and `ct_state_ttl` produced a 12.20-point decline and raised the false-negative rate above 21%.

These transformations are controlled diagnostic ablations. They are not simulations of a specific cyberattack and do not establish that a real attacker can force the model into these conditions.

## Final Untouched Test Evaluation

After development, interpretation, and robustness experiments were complete, both frozen classifiers were evaluated on the official 82,332-row test partition.

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

For Histogram Gradient Boosting, the final confusion matrix was TN 27,273, FP 9,727, FN 666, TP 44,666.

The principal generalization gap was benign discrimination. Stronger-model FPR increased from 8.59% on validation to 26.29% on final test, while attack recall remained high and increased from 97.56% to 98.53%.

This result should not be attributed solely to TTL dependence. The controlled ablations establish sensitivity to TTL-related information, while the official test result demonstrates a broader validation-to-test distribution gap.

## Limitations

UNSW-NB15 was generated in a controlled cyber-range and cannot establish present-day deployment performance. Exact predictor-vector grouping reduces one leakage pathway but does not guarantee independence across all latent traffic relationships. Rare attack families produce uncertain category-level estimates. The robustness ablations intentionally alter feature information and should not be described as realistic adversarial attacks. No conclusion from this study establishes that the models can safely block traffic in a live network.

## Conclusion

The Network Layer provides evidence that aggregate intrusion-detection metrics can materially overstate robustness. A nonlinear classifier achieved 95.59% validation accuracy and 99.29% ROC AUC, yet relied heavily on TTL-related information and experienced substantial degradation under pre-specified feature ablations. More importantly, its false-positive rate increased from 8.59% during internal validation to 26.29% on the untouched official test partition despite maintaining 98.53% attack recall.

The central result is therefore not simply that a classifier can detect attacks. It is that **high internal performance did not guarantee stable behavior when the information distribution changed**, reinforcing the need for leakage controls, feature-reliance analysis, distribution-shift testing, and untouched final evaluation in defensive machine-learning research.
