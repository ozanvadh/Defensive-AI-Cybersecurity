# Cross-Layer Integration Framework

## Purpose

This document freezes the conceptual integration of the completed Human Layer and Network Layer before the combined research report is written.

The two layers are not treated as one pooled statistical experiment. They use different data modalities, datasets, models, robustness tests, and outcome structures. Their results are integrated at the level of the research question and recurring empirical pattern.

## Overarching Research Question

**Can machine-learning defenses detect cyber threats at both the human communication layer and the network-traffic layer while maintaining low false-positive rates, and how reliably do strong benchmark results persist when the evaluation distribution changes?**

## Layer 1: Human Communication

### Task

Classify historical email content as legitimate or phishing-class.

### Models

- TF-IDF + Logistic Regression
- fine-tuned DistilBERT

### In-distribution evidence

On the untouched 31,225-email historical test set:

| Model | Accuracy | Recall | False-positive rate |
| --- | ---: | ---: | ---: |
| TF-IDF + Logistic Regression | 98.25% | 98.47% | 1.96% |
| DistilBERT | 99.23% | 99.16% | 0.70% |

### Distribution-shift evidence

On a separately frozen positive-only set of 500 controlled synthetic phishing-class messages:

- TF-IDF + Logistic Regression detected **55.4%**
- DistilBERT detected **36.2%**
- DistilBERT made many synthetic misses with very high raw confidence

Because this synthetic set contains only positive-class examples, it estimates detection rate under the designed shift but cannot estimate precision or false-positive rate for that synthetic distribution.

### Human Layer interpretation

The models generalized strongly to unseen historical emails from the familiar data distribution but did not retain that performance on the controlled synthetic phishing-class distribution. The more complex DistilBERT model was stronger in-distribution yet degraded more sharply on this particular synthetic shift.

The experiment does not establish performance on all AI-generated phishing and does not establish that the synthetic set represents the population of real-world phishing.

## Layer 2: Network Traffic

### Task

Classify UNSW-NB15 network flows as benign or malicious.

### Models

- Logistic Regression
- Histogram Gradient Boosting

### Internal validation evidence

The stronger Histogram Gradient Boosting model achieved:

- **95.59% accuracy**
- **97.56% attack recall**
- **8.59% false-positive rate**
- **94.48% balanced accuracy**

### Controlled feature-shift evidence

Under the pre-specified source-TTL neutralization test:

- balanced accuracy: **94.48% → 69.41%**
- attack recall: **97.56% → 97.67%**
- false-positive rate: **8.59% → 58.84%**

Under broader TTL-family neutralization:

- balanced accuracy: **56.79%**
- attack recall: **97.65%**
- false-positive rate: **84.07%**

The principal failure mode was loss of benign discrimination rather than loss of attack sensitivity.

### Untouched official test evidence

On the official 82,332-row test partition, the frozen stronger model achieved:

- **87.38% accuracy**
- **98.53% attack recall**
- **26.29% false-positive rate**
- **86.12% balanced accuracy**

The study does not establish that TTL dependence caused the official test-set generalization gap.

## Cross-Layer Finding

The strongest common result is:

> **High performance on familiar or internal evaluation data did not guarantee stable defensive performance when the information distribution changed.**

This pattern appeared differently in the two layers.

| Layer | Strong familiar-distribution result | Shift/stress result | Dominant observed failure |
| --- | --- | --- | --- |
| Human | DistilBERT 99.23% historical-test accuracy, 99.16% recall | 36.2% detection on controlled synthetic phishing-class set | malicious messages classified as legitimate, often with high confidence |
| Network | HGB 95.59% validation accuracy, 8.59% FPR | 26.29% FPR on untouched official test; 58.84% FPR under `sttl` neutralization | benign flows increasingly classified as malicious |

The direction of failure is therefore **not the same across layers**. The Human Layer shift primarily exposed false negatives on synthetic malicious content. The Network Layer shifts primarily exposed false positives on benign traffic.

This distinction is central to the combined study.

## Complexity Does Not Guarantee Robustness

Both layers include a simpler baseline and a stronger nonlinear/contextual model.

In the Human Layer, DistilBERT clearly outperformed Logistic Regression on the historical distribution but performed worse than the baseline on the controlled synthetic phishing-class set.

In the Network Layer, Histogram Gradient Boosting outperformed Logistic Regression on both validation and the official final test, particularly by reducing false positives relative to the baseline. However, interpretation and controlled ablation showed substantial dependence on TTL-related information.

The combined evidence therefore supports a limited conclusion:

**Higher in-distribution performance or greater model complexity should not be treated as evidence of distribution-shift robustness.**

It does not support a universal claim that simpler models are more robust or that complex models are inherently brittle.

## Operational Tradeoff Across Layers

The two layers illustrate different security costs:

- **Human Layer false negatives:** malicious messages pass through as legitimate.
- **Network Layer false positives:** benign traffic is flagged as malicious, increasing alert burden and reducing practical usability.

A layered defensive system must therefore be evaluated with more than aggregate accuracy. Recall, false-positive rate, false-negative rate, class-specific behavior, confidence, and shift-specific failure modes all matter.

## What the Combined Project Can Claim

The completed evidence supports the following claims:

1. Strong held-out or internal benchmark performance was achieved in both defensive domains.
2. Both domains exhibited substantial degradation under at least one deliberately separated or shifted evaluation condition.
3. The failure mechanism differed across domains rather than following one universal pattern.
4. Model interpretation exposed specific dependencies that aggregate metrics alone concealed.
5. Untouched evaluation and frozen robustness protocols materially changed the scientific conclusions that would have been drawn from validation accuracy alone.

## What the Combined Project Cannot Claim

The project does **not** establish:

- real-world deployment performance for either detector;
- universal performance on AI-generated phishing;
- that the controlled synthetic email set represents all modern phishing;
- that TTL neutralization represents a realistic attacker action;
- that TTL dependence caused the official UNSW-NB15 test gap;
- that either detector is safe for autonomous production blocking;
- that one model family is universally more robust than another;
- that the Human and Network Layer numerical metrics are directly comparable as if they came from the same population.

## Integrated Scientific Contribution

The project's contribution is not a claim of having solved phishing or intrusion detection.

Its stronger contribution is an evaluation framework demonstrated across two distinct defensive cybersecurity domains:

1. build an interpretable baseline;
2. compare a stronger model;
3. control obvious leakage and artifacts;
4. preserve untouched evaluation data;
5. inspect errors and model dependence;
6. freeze robustness tests before execution when possible;
7. evaluate under a materially different condition;
8. report failure modes rather than only headline accuracy;
9. limit conclusions to what the evaluation design actually supports.

## Combined Thesis

**Defensive AI systems can achieve very high performance on familiar benchmark distributions while remaining vulnerable to materially different failure modes under distribution shift. Robust evaluation therefore requires layer-specific stress testing, explicit false-positive and false-negative analysis, leakage controls, model-dependence analysis, and untouched final evaluation rather than reliance on aggregate benchmark accuracy alone.**
