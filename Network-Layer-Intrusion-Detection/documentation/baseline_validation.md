# Logistic Regression Baseline Validation

## Purpose

The first Network Layer classifier is an interpretable conventional baseline. It establishes how well a relatively simple linear model can separate malicious from benign UNSW-NB15 traffic before comparison with a stronger nonlinear tabular model.

Training uses only the 140,269-row development partition. Evaluation uses the 35,072-row leakage-resistant validation partition. The official test set remains sealed.

## Model

- Classifier: Logistic Regression
- Solver: L-BFGS
- Maximum iterations: 1,000
- Random seed: 42
- Decision threshold: default 0.50
- Numerical preprocessing: StandardScaler fitted on development only
- Categorical preprocessing: one-hot encoding fitted on development only with unknown-category handling
- Excluded: `id`, `attack_cat`, `ct_ftp_cmd`

No validation-driven threshold optimization was performed for these baseline results.

## Validation Results

| Metric | Result |
| --- | ---: |
| Accuracy | **93.2824%** |
| Precision | **92.0100%** |
| Recall / TPR | **98.7014%** |
| F1 | **95.2383%** |
| False-positive rate | **18.2662%** |
| False-negative rate | **1.2986%** |
| ROC AUC | **0.98368** |
| Balanced accuracy | **90.2176%** |

Confusion matrix:

| | Predicted benign | Predicted attack |
| --- | ---: | ---: |
| Actual benign | **9,155** | **2,046** |
| Actual attack | **310** | **23,561** |

## Attack-Family Detection on Validation

| Category | n | Correct / detected |
| --- | ---: | ---: |
| Analysis | 421 | 99.76% |
| Backdoor | 362 | 97.24% |
| DoS | 2,523 | 98.97% |
| Exploits | 6,888 | 99.17% |
| Fuzzers | 3,713 | 94.37% |
| Generic | 7,654 | 99.97% |
| Reconnaissance | 2,057 | 99.81% |
| Shellcode | 228 | 99.56% |
| Worms | 25 | 100.00% |

The Worms estimate is based on only 25 validation observations and must not be interpreted as evidence of reliable 100% Worm detection.

For benign traffic, 81.73% was correctly classified and 18.27% was falsely flagged as malicious.

## Interpretation

The baseline detects attacks at a very high rate, missing only 310 of 23,871 malicious validation flows. However, this sensitivity comes with a substantial operational weakness: **2,046 of 11,201 benign validation flows were falsely flagged**, corresponding to an 18.27% false-positive rate.

Therefore, the baseline's 93.28% accuracy and 95.24% F1 score should not be interpreted alone as strong deployment performance. For an intrusion detector, repeatedly alerting on nearly one in five benign flows could create an impractical alert burden.

This establishes a useful benchmark for the stronger tabular model: improvement should not merely raise aggregate accuracy. It should materially reduce false positives while preserving strong attack recall.

## Test-Set Policy

These results are validation-only. The official UNSW-NB15 test partition has not been used to choose the model, preprocessing, threshold, or hyperparameters and remains reserved for the final frozen evaluation.
