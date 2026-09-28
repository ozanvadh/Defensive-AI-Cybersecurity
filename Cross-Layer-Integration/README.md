# Cross-Layer Integration

This directory integrates the completed Human and Network Layer v1 studies into one Defensive AI cybersecurity research package.

## Overarching Question

**Can machine-learning defenses detect cyber threats at both the human communication layer and the network-traffic layer while maintaining low false-positive rates, and how reliably do strong benchmark results persist when the evaluation distribution changes?**

## Central Finding

> **High performance on familiar or internal evaluation data did not guarantee stable defensive performance when the information distribution changed.**

The two layers failed differently.

| Layer | Strong familiar/internal result | Shift result | Dominant observed failure |
| --- | --- | --- | --- |
| Human | DistilBERT: 99.23% historical-test accuracy, 99.16% recall | 36.20% detection on controlled synthetic phishing-class set | false negatives |
| Network | HGB: 95.59% validation accuracy, 8.59% FPR | 26.29% FPR on official test; 58.84% under `sttl` neutralization | false positives |

![Cross-layer failure modes](results/figures/cross_layer_failure_modes.svg)

The metrics are intentionally not pooled. The Human and Network studies use different data modalities, populations, models, outcome structures, and distribution-shift mechanisms.

## Read the Integrated Work

- **[Combined research paper](documentation/combined_research_paper.md)**
- [Integration framework](documentation/integration_framework.md)
- [Quantitative synthesis](documentation/quantitative_synthesis.md)
- [Machine-readable cross-layer results](results/cross_layer_results.csv)
- [Statistical uncertainty and operational analysis](documentation/statistical_uncertainty_and_operational_analysis.md)
- [External-validation preregistration](documentation/external_validation_preregistration.md)
- [Cross-layer figures](results/figures/)

## Human Layer in One Sentence

The stronger DistilBERT model generalized extremely well to unseen historical email but detected only 36.20% of the separately frozen controlled synthetic phishing-class set, with many misses receiving very high raw legitimate-class confidence.

## Network Layer in One Sentence

The stronger Histogram Gradient Boosting model retained high attack recall under both the official test distribution and controlled TTL-information ablations, but benign false positives increased substantially.

## Integrated Interpretation

The commonality is **distribution-shift instability**, not one universal failure mechanism.

- Human shift primarily reduced malicious-message sensitivity.
- Network shift primarily reduced benign-traffic specificity.
- Greater model complexity did not guarantee shift robustness.
- Untouched evaluation and pre-specified stress testing materially changed the conclusions that validation metrics alone would have supported.

## Claim Boundaries

The combined project does not establish:

- universal performance on AI-generated phishing;
- present-day production-network performance;
- that TTL dependence caused the official UNSW-NB15 test gap;
- that the controlled feature ablations represent realistic attacker actions;
- that one model family is universally more robust;
- that Human and Network numerical metrics are directly comparable;
- that either detector is safe for autonomous production blocking.

## Project Structure

```text
Cross-Layer-Integration/
├── README.md
├── documentation/
│   ├── integration_framework.md
│   ├── quantitative_synthesis.md
│   └── combined_research_paper.md
└── results/
    ├── cross_layer_results.csv
    └── figures/
        ├── human_distribution_shift.svg
        ├── network_distribution_shift.svg
        └── cross_layer_failure_modes.svg
```

For layer-specific methods, code, audits, and demos, return to the [repository root](../README.md).
