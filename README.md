# Defensive AI Cybersecurity

**A two-layer machine-learning security study showing how near-99% benchmark performance can conceal severe failures when the data distribution changes.**

[Research Paper](Cross-Layer-Integration/documentation/combined_research_paper.md) · [Human Layer](Phase-1-Phishing-Detection/README.md) · [Network Layer](Network-Layer-Intrusion-Detection/README.md) · [Scientific Audit](FINAL_SCIENTIFIC_AUDIT.md)

> **Central question:** Can machine-learning defenses maintain reliable security decisions across human communication and network-traffic layers when evaluation moves beyond familiar data distributions?

## Headline Finding

Strong familiar-distribution performance did **not** guarantee stable defensive behavior under distribution shift, and the failure direction differed by security layer.

| Layer | Familiar distribution | Shifted evaluation | Dominant failure |
| --- | --- | --- | --- |
| **Human communication** | DistilBERT: **99.23% accuracy**, **99.16% recall** | **36.20% detection** on 500 frozen controlled synthetic phishing-class messages | False negatives: malicious messages classified as legitimate |
| **Network traffic** | HGB: **95.59% accuracy**, **8.59% FPR** | **26.29% FPR** on untouched official test; **58.84% FPR** under controlled `sttl` neutralization | False positives: benign flows classified as malicious |

The two layers are **not statistically pooled**. They use different datasets, models, populations, and shift mechanisms. Their connection is methodological: both show why familiar-distribution accuracy alone is insufficient evidence of defensive robustness.

![Cross-layer failure modes](Cross-Layer-Integration/results/figures/cross_layer_failure_modes.svg)

## What This Project Does

The project contains two completed defensive experiments and a cross-layer synthesis:

**Human Layer:** TF-IDF + Logistic Regression and fine-tuned DistilBERT were trained on a cleaned **208,161-email** historical corpus. Both performed near 99% on the untouched historical test, then were frozen and evaluated on a separately constructed 500-message controlled synthetic phishing-class distribution.

**Network Layer:** Logistic Regression and Histogram Gradient Boosting were evaluated on **UNSW-NB15** after leakage auditing and a group-preserving development/validation split. The stronger frozen model was subjected to pre-specified feature-information stress tests and then evaluated once on the untouched official **82,332-row** test partition.

**Cross-Layer Integration:** The studies are combined around a shared evaluation framework emphasizing leakage controls, frozen models, untouched holdouts, explicit false-positive/false-negative analysis, feature dependence, uncertainty, and distribution-shift testing.

## Key Results

### Human Layer

| Model | Historical accuracy | Historical recall | Historical FPR | Synthetic detection |
| --- | ---: | ---: | ---: | ---: |
| TF-IDF + Logistic Regression | **98.25%** | **98.47%** | **1.96%** | **55.40%** |
| DistilBERT | **99.23%** | **99.16%** | **0.70%** | **36.20%** |

DistilBERT missed **319 of 500** synthetic phishing-class messages. Of those misses, **290** were classified as legitimate with at least 90% raw confidence and **233** with at least 99% raw confidence.

Because the synthetic dataset contains only positive-class examples, its result is a detection rate/recall. It cannot estimate synthetic-set precision, overall accuracy, or false-positive rate.

![Historical versus synthetic Human detection](Phase-1-Phishing-Detection/results/figures/figure_2_historical_vs_synthetic.svg)

### Network Layer

| Evaluation | Accuracy | Attack recall | FPR | Balanced accuracy |
| --- | ---: | ---: | ---: | ---: |
| HGB validation | **95.59%** | **97.56%** | **8.59%** | **94.48%** |
| Untouched official test | **87.38%** | **98.53%** | **26.29%** | **86.12%** |
| `sttl` neutralized | **79.62%** | **97.67%** | **58.84%** | **69.41%** |
| TTL-family neutralized | **71.55%** | **97.65%** | **84.07%** | **56.79%** |

The Network degradation was dominated by **benign false positives**, not loss of attack sensitivity. The feature neutralizations are diagnostic information-ablation experiments, not simulations of a specific attacker.

A five-seed supplementary HGB analysis produced a mean validation FPR of **8.77% with SD 0.14 percentage points**, making ordinary seed variation very small relative to the observed distribution-shift effects.

## Why the Result Matters

A security model can look excellent under a conventional benchmark while failing in a completely different operational direction after the information distribution changes.

In the Human Layer, the primary risk was **missed malicious content**.

In the Network Layer, the primary risk was **excessive benign alerts**.

That distinction matters because the operational consequences are different. Robust security evaluation therefore needs more than accuracy: it needs explicit sensitivity/specificity analysis, false-positive and false-negative behavior, confidence analysis, feature-dependence testing, leakage controls, and genuinely untouched evaluation data.

## Research Design and Integrity

The project includes:

- untouched final evaluation sets and no post-test v1 tuning;
- leakage and duplicate controls;
- fixed seeds and documented model configurations;
- a frozen Human synthetic dataset before classifier exposure;
- a pre-specified Network robustness protocol;
- exact paired McNemar testing for the Human synthetic comparison;
- Wilson confidence intervals and Network validation-to-test uncertainty analysis;
- permutation importance and category-level error analysis;
- raw-data fingerprints and machine-readable result summaries where applicable;
- a five-seed supplementary Network stability analysis;
- a repository-wide scientific audit and documented correction history;
- a preregistered protocol for any future independent external validation.

The completed Human historical test, Human synthetic set, and Network official test are considered **consumed**. They cannot be reused as untouched holdouts for future tuned models.

## Research Artifacts

| Resource | Purpose |
| --- | --- |
| **[Combined Research Paper](Cross-Layer-Integration/documentation/combined_research_paper.md)** | Full methods, results, related work, statistical analysis, discussion, and limitations |
| **[Human Layer](Phase-1-Phishing-Detection/README.md)** | Phishing-classification experiment, robustness analysis, figures, and prototype |
| **[Network Layer](Network-Layer-Intrusion-Detection/README.md)** | Intrusion-detection experiment, leakage audit, stress tests, and final evaluation |
| **[Cross-Layer Integration](Cross-Layer-Integration/README.md)** | Quantitative synthesis and integrated evaluation framework |
| **[Final Scientific Audit](FINAL_SCIENTIFIC_AUDIT.md)** | Repository-wide metric and claim verification |
| **[Statistical Supplement](Cross-Layer-Integration/documentation/statistical_uncertainty_and_operational_analysis.md)** | Confidence intervals and base-rate analysis |
| **[Publication Revision Log](PUBLICATION_REVISION_LOG.md)** | Post-audit manuscript and methodology improvements |

## Repository Structure

```text
Defensive-AI-Cybersecurity/
├── Phase-1-Phishing-Detection/          # Human communication layer
├── Network-Layer-Intrusion-Detection/   # Network traffic layer
├── Cross-Layer-Integration/             # Combined analysis and paper
├── FINAL_SCIENTIFIC_AUDIT.md
├── PUBLICATION_REVISION_LOG.md
└── README.md
```

Large raw datasets and trained model weights are not committed directly to the repository.

## Defensive Prototypes

The Human Layer includes a Streamlit research demo using the trained DistilBERT phishing classifier. The Network Layer includes a defensive CSV demo for pre-recorded UNSW-NB15-style flows.

These are research prototypes, **not production security products**.

## Scope and Limitations

This project is exclusively defensive. It does not conduct real phishing campaigns, collect credentials, attack live infrastructure, scan unauthorized systems, deploy malware, or generate operational attacks.

The Human historical corpus combines older public sources and uses a broad phishing-class definition. The controlled synthetic evaluation contains 500 positive-class messages from two generation sources and is not representative of all AI-generated or real-world phishing.

UNSW-NB15 was generated in a controlled cyber-range and does not establish current production-network performance. The Network feature ablations diagnose model dependence but do not establish how a real attacker would manipulate network conditions.

Neither detector has been independently validated for autonomous production deployment.

## Central Contribution

> **Defensive AI systems can achieve very high performance on familiar benchmark distributions while remaining vulnerable to materially different failure modes under distribution shift. Robust evaluation therefore requires layer-specific stress testing, explicit false-positive and false-negative analysis, leakage controls, model-dependence analysis, and untouched final evaluation rather than reliance on aggregate benchmark accuracy alone.**
