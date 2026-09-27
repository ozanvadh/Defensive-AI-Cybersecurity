# Cross-Layer Quantitative Synthesis

## Purpose

This document integrates the completed Human and Network Layer results quantitatively without pooling unlike datasets or treating different metrics as directly interchangeable.

The Human Layer shift analysis is expressed primarily through **positive-class detection/recall**, because the controlled synthetic set contains only phishing-class examples. The Network Layer shift analysis is expressed primarily through **false-positive rate and balanced accuracy**, because its dominant observed failure under shift was benign traffic being classified as malicious.

## Human Layer: Detection Under Text Distribution Shift

The untouched historical test set contained 31,225 emails. The controlled synthetic evaluation contained 500 positive-class phishing-style messages.

| Model | Historical test recall | Synthetic detection | Change |
| --- | ---: | ---: | ---: |
| TF-IDF + Logistic Regression | 98.47% | 55.40% | -43.07 pp |
| DistilBERT | 99.16% | 36.20% | -62.96 pp |

DistilBERT had the stronger historical-test result, but the ordering reversed on the controlled synthetic set. The baseline detected 277/500 synthetic messages while DistilBERT detected 181/500.

This comparison is valid as a positive-class detection comparison. The synthetic set cannot provide a synthetic false-positive rate, precision estimate, or overall accuracy because it contains no legitimate examples.

### Confidence behavior

Of DistilBERT's 319 synthetic misses:

- 290, or 90.9%, were predicted legitimate with at least 90% raw confidence;
- 233, or 73.0%, were predicted legitimate with at least 99% raw confidence;
- median confidence among misses was 99.92%.

The raw softmax scores are not treated as calibrated real-world probabilities.

## Network Layer: Benign Discrimination Under Shift

For the stronger Histogram Gradient Boosting model:

| Condition | Attack recall | False-positive rate | Balanced accuracy |
| --- | ---: | ---: | ---: |
| Internal validation | 97.56% | 8.59% | 94.48% |
| Untouched official test | 98.53% | 26.29% | 86.12% |
| Controlled `sttl` neutralization | 97.67% | 58.84% | 69.41% |
| Controlled TTL-family neutralization | 97.65% | 84.07% | 56.79% |

Relative to internal validation:

- official-test FPR increased by **17.70 percentage points**;
- `sttl`-neutralized FPR increased by **50.25 percentage points**;
- TTL-family-neutralized FPR increased by **75.48 percentage points**;
- official-test balanced accuracy decreased by **8.36 percentage points**;
- `sttl`-neutralized balanced accuracy decreased by **25.07 percentage points**;
- TTL-family-neutralized balanced accuracy decreased by **37.70 percentage points**.

Attack recall remained high across these conditions. The dominant shift-related problem was therefore benign discrimination rather than attack sensitivity.

## Cross-Layer Comparison

The two layers should not be reduced to one pooled performance score.

| Dimension | Human Layer | Network Layer |
| --- | --- | --- |
| Data modality | Email text | Network-flow features |
| Main stronger model | DistilBERT | Histogram Gradient Boosting |
| Familiar/internal performance | 99.23% historical-test accuracy; 99.16% recall | 95.59% validation accuracy; 97.56% recall; 8.59% FPR |
| Main shifted evaluation | 500 controlled synthetic positive-class messages | official test distribution plus pre-specified feature ablations |
| Dominant failure | false negatives | false positives |
| Key shifted result | DistilBERT detection 36.20% | official-test FPR 26.29%; `sttl`-ablation FPR 58.84% |
| Interpretation | malicious text can move outside learned historical patterns | benign/malicious separation depends strongly on evaluation distribution and TTL-related information |

## Model-Complexity Result

The two studies do not support one universal complexity-versus-robustness rule.

### Human Layer

DistilBERT outperformed the simpler baseline on the untouched historical test:

- accuracy: 99.23% vs. 98.25%;
- recall: 99.16% vs. 98.47%;
- FPR: 0.70% vs. 1.96%.

On the controlled synthetic positive-class set, the ordering reversed:

- baseline detection: 55.40%;
- DistilBERT detection: 36.20%.

### Network Layer

Histogram Gradient Boosting outperformed Logistic Regression on the untouched official test:

- accuracy: 87.38% vs. 80.94%;
- recall: 98.53% vs. 97.23%;
- FPR: 26.29% vs. 39.01%.

However, the stronger network model still exhibited substantial distribution sensitivity and feature dependence.

The supported cross-layer conclusion is therefore narrow:

> **Better familiar-distribution performance did not establish robustness under distribution shift.**

## Quantitative Thesis

Across two different defensive domains, conventional benchmark performance would have produced an incomplete picture.

The Human Layer stronger model retained 99.16% recall on untouched historical email but detected only 36.20% of the controlled synthetic phishing-class set. The Network Layer stronger model retained 98.53% attack recall on the untouched official test but its benign false-positive rate increased from 8.59% internally to 26.29%. Controlled TTL-information ablations increased that false-positive rate further without materially reducing attack recall.

The common empirical pattern is therefore **instability under changed information distributions**, while the direction and operational cost of failure remain layer-specific.

## Statistical Boundary

No cross-layer significance test is performed. The Human and Network experiments use different populations, sample construction procedures, models, metrics, and shift mechanisms. Their integration is comparative and conceptual rather than a pooled statistical meta-analysis.
