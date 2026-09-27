# Network Layer: Intrusion Detection Under Distribution Shift

This directory contains the completed Network Layer v1 of the Defensive AI Cybersecurity Research Project.

## Research question

**How accurately can machine-learning models distinguish malicious from benign network traffic while maintaining a low false-positive rate, and how robust are those models when evaluated under network-traffic distribution shift?**

## Headline result

A Histogram Gradient Boosting intrusion detector achieved **95.59% validation accuracy**, **97.56% attack recall**, and an **8.59% false-positive rate**. Interpretation revealed unusually heavy reliance on source TTL. In the pre-specified `sttl` neutralization stress test, balanced accuracy fell from **94.48% to 69.41%** because the false-positive rate rose from **8.59% to 58.84%**, while attack recall remained **97.67%**.

On the untouched official UNSW-NB15 test partition, the frozen model retained **98.53% attack recall**, but accuracy fell to **87.38%** and the false-positive rate increased to **26.29%**.

The main conclusion is not that the model fails universally. It is that excellent internal metrics concealed substantial feature dependence and a serious benign-traffic generalization gap.

## Quick navigation

- [Full Network Layer research report](documentation/network_layer_research_report.md)
- [Dataset provenance and reproducibility policy](documentation/dataset_provenance_and_reproducibility.md)
- [Training-data leakage audit](documentation/training_data_leakage_audit.md)
- [Development/validation split protocol](documentation/development_validation_split.md)
- [Formal EDA](documentation/formal_eda.md)
- [Baseline validation](documentation/baseline_validation.md)
- [Stronger-model validation](documentation/stronger_model_validation.md)
- [Model interpretation and error analysis](documentation/stronger_model_interpretation.md)
- [Pre-specified robustness protocol](documentation/robustness_protocol.md)
- [Corrected robustness results](documentation/robustness_results.md)
- [Final untouched test evaluation](documentation/final_test_evaluation.md)
- [Reproducibility audit](documentation/reproducibility_audit.md)
- [Captured Python environment](network_environment.txt)
- [Consolidated results table](results/results_summary.csv)

## Scientific safeguards

- Raw official files fingerprinted with SHA-256 before transformation
- Identifier/target leakage audited before training
- Identical modeling predictor vectors prevented from crossing development/validation
- Official test partition withheld from model development
- Robustness protocol committed before robustness execution
- Frozen models and default thresholds used for robustness and final testing
- Official test declared permanently consumed after final evaluation
- Controlled feature ablations explicitly distinguished from realistic adversarial attacks
- Python 3.13.5 and the project-machine package environment archived
- Final audit independently reproduced the split, validation metrics, and final-test metrics from the preserved raw CSVs

## Scope

This is defensive research using pre-recorded public network-flow data. It does not scan, probe, attack, or automatically block live systems. UNSW-NB15 is a controlled benchmark, so the results should not be interpreted as direct estimates of present-day deployment performance.
