# External Validation Preregistration

## Status

**Frozen before any v2 external-model evaluation.**

This document defines the next-stage validation rules for the completed Defensive AI Cybersecurity v1 project. It is intended to prevent external-data selection, threshold changes, or model changes from being made in response to observed external results.

The v1 Human historical test set, v1 Human 500-message controlled synthetic set, and v1 Network official test set are already consumed and must not be treated as fresh unbiased final holdouts.

## Primary Objective

Test whether the main v1 conclusion generalizes beyond the completed benchmark ecosystem:

> Strong familiar-distribution performance may fail to remain stable when a defensive model encounters an independently sourced distribution, and the operational direction of failure may depend on the defensive layer.

## Human Layer External Validation

### Frozen models

Primary v1 models:

1. TF-IDF + Logistic Regression baseline
2. DistilBERT classifier

No retraining, threshold adjustment, vocabulary refitting, calibration fitting, prompt adaptation, or category-specific tuning may occur before the primary external results are recorded.

### Dataset eligibility

A primary external Human holdout must satisfy all of the following:

- contain both legitimate and phishing-class email text;
- be independently sourced from the v1 merged training corpus;
- not be a direct re-release, merge, or simple resampling of Enron, SpamAssassin, TREC 2005-2007, CEAS, Nazario, Nigerian-fraud, or other corpora already represented in the v1 source;
- provide enough provenance to audit likely source overlap;
- not have been used to tune the v1 models;
- permit defensive academic evaluation under its license;
- contain at least 1,000 total labeled examples where feasible;
- preserve the natural class distribution if the released dataset has one.

A candidate dataset may be rejected **before model inference** if provenance or duplicate auditing shows substantial source overlap. Rejection criteria may not use model performance.

### Candidate identified before inference

The 2024 **Phishing validation emails dataset** by Miltchev, Rangelov, and Genchev (Zenodo DOI: 10.5281/zenodo.13474746) is a candidate because it contains 2,000 labeled safe/phishing emails. It is **not automatically accepted as the primary external holdout** because its description states that it mixes real-world and artificially generated messages without fully specifying all source corpora. It must first pass provenance and duplicate-overlap checks.

### Primary Human metrics

Report for each frozen model:

- accuracy;
- precision;
- recall;
- F1;
- specificity;
- false-positive rate;
- false-negative rate;
- balanced accuracy;
- ROC AUC when probabilities are available;
- confusion matrix;
- 95% Wilson intervals for recall and FPR;
- Brier score;
- expected calibration error;
- reliability diagram.

### Human hypotheses

H1: external performance will differ materially from the familiar historical-test result.

H2: the direction and magnitude of external degradation will not be assumed in advance.

H3: model ordering on the external holdout will be treated as an empirical result rather than inferred from either the historical or synthetic v1 evaluation.

## Network Layer External Validation

### Direct transportability track

Direct frozen-model validation is primary only if an independent dataset contains semantically compatible versions of the full frozen v1 predictor schema or supports a defensible, pre-declared one-to-one mapping without fitting to labels.

If such a dataset is found:

- keep the frozen v1 model and 0.50 threshold;
- do not refit encoders;
- do not select a feature subset after viewing labels;
- report the same binary metrics and uncertainty intervals used in v1.

### Independent-protocol replication track

Most public intrusion datasets use incompatible flow schemas. If no defensible direct feature mapping exists, the project will **not pretend that a newly trained model is direct external validation of the frozen UNSW-NB15 model**.

Instead, an independent-protocol replication may be performed:

1. select an independent network dataset before model training;
2. audit leakage and duplicates;
3. create a leakage-resistant development/validation split;
4. train the same model classes where technically appropriate;
5. pre-specify one or more robustness tests;
6. preserve an untouched final partition;
7. compare whether the same high-level phenomenon appears.

Such a replication tests the **evaluation framework**, not direct transportability of the v1 model.

## Multi-Seed Stability

Multi-seed experiments are supplementary analyses and may use development/validation data only.

They must not reopen consumed v1 final test sets for repeated model selection.

Pre-declared seed set:

`[7, 17, 29, 42, 73]`

Report mean, standard deviation, minimum, maximum, and all individual validation metrics.

## Statistical Plan

No claim of generalization will be based only on point estimates.

For binary rates, use Wilson 95% intervals. For differences in independent proportions, use Newcombe intervals. Paired tests may be used only when the same examples are scored by both models.

No cross-layer pooled significance test will be performed.

## Stopping and Reporting Rules

- Record the first valid external evaluation of each frozen model.
- Do not alter models after seeing those primary results and then continue calling the same dataset an untouched holdout.
- Report negative, null, or unfavorable outcomes.
- Report provenance limitations and class balance.
- If an external dataset fails eligibility, document why before model inference.
- Any later tuned model becomes a v2 model and requires a new final holdout.

## Claim Boundary

External validation can strengthen transportability evidence, but one or two additional datasets still cannot establish universal deployment performance.

The goal is to replace a single-benchmark claim with a progressively stronger chain of independent evidence.
