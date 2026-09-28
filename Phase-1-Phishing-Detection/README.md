# Human Layer: Phishing Detection Under Controlled Synthetic Distribution Shift

This directory contains the completed Human Layer v1 of the Defensive AI Cybersecurity project.

## Research Question

**How accurately can machine-learning and NLP models distinguish phishing-class from legitimate historical emails while maintaining a low false-positive rate, and how robust are those frozen classifiers to a controlled synthetic phishing-class distribution?**

## Headline Result

Both classifiers generalized strongly to the untouched historical test set, but both degraded sharply on the separately frozen controlled synthetic phishing-class distribution.

| Model | Historical-test accuracy | Historical-test recall | Historical-test FPR | Synthetic detection |
| --- | ---: | ---: | ---: | ---: |
| TF-IDF + Logistic Regression | 98.25% | 98.47% | 1.96% | 55.40% |
| DistilBERT | 99.23% | 99.16% | 0.70% | 36.20% |

The synthetic set contains only positive-class messages, so synthetic precision, false-positive rate, and overall accuracy are not estimated.

DistilBERT missed 319 of the 500 controlled synthetic messages. Of those misses, 290 were predicted legitimate with at least 90% raw confidence and 233 with at least 99% raw confidence.

![Historical versus controlled synthetic detection](results/figures/figure_2_historical_vs_synthetic.svg)

## Quick Navigation

- [Full Human Layer research report](documentation/human_layer_research_report.md)
- [Dataset documentation](data/README.md)
- [Final untouched historical-test evaluation](documentation/final_test_evaluation.md)
- [Controlled synthetic methodology](documentation/synthetic_evaluation_methodology.md)
- [Controlled synthetic results](documentation/synthetic_evaluation_results.md)
- [Reproducibility audit](documentation/reproducibility_audit.md)
- [Aggregate results](results/results_summary.csv)
- [Publication figures](results/figures/)
- [Defensive demo](demo/)
- [Transformer training notes](documentation/transformer_colab.md)

## Data

After cleaning and exact-body deduplication:

- 208,161 total emails
- 108,953 legitimate
- 99,208 phishing-class
- training: 145,712
- validation: 31,224
- untouched test: 31,225

No exact duplicate email bodies crossed the train, validation, and test partitions.

## Models

### TF-IDF + Logistic Regression

The baseline provides an interpretable classical NLP comparison using sparse lexical features.

### DistilBERT

The stronger contextual model uses a fine-tuned DistilBERT classifier with a 256-token training input length.

## Controlled Synthetic Evaluation

The frozen evaluation contains 500 positive-class messages across five designed communication styles:

- account/security
- workplace/business
- delivery/service
- promotional/offer
- general social engineering

Copilot and Gemini each contributed 250 accepted messages.

The set was created for defensive robustness testing under non-operational safety constraints. It should not be interpreted as a representative sample of all real-world or AI-generated phishing.

## Statistical Result

On the same 500 synthetic messages:

- both detected: 168
- both missed: 210
- baseline only: 109
- DistilBERT only: 13

The exact two-sided McNemar test produced **p < 0.001** for this designed evaluation set. This does not establish that Logistic Regression is universally more robust than DistilBERT.

## Scientific Safeguards

- fixed split seed
- exact-body cross-split duplicate control
- untouched historical final test
- frozen synthetic evaluation before classifier exposure
- no tuning against the consumed final test or synthetic evaluation
- artifact and length checks
- paired model comparison
- confidence analysis
- documented limitations and AI-use disclosure

## Scope

This is defensive research. The synthetic materials were constrained to remain non-operational, and the prototype is a research demonstration rather than a production email-security system.

For the integrated interpretation, see the [combined cross-layer research paper](../Cross-Layer-Integration/documentation/combined_research_paper.md).
