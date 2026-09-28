# Publication Revision Log

**Revision date:** 2026-09-27

## Purpose

This record documents manuscript and repository changes made after a graduate-level peer-review simulation identified weaknesses in literature coverage, uncertainty reporting, training-run stability, operational interpretation, and external validity.

No consumed v1 final holdout was reopened for model tuning.

## Completed Revisions

### 1. Literature review expanded

The combined paper now includes additional scholarship on:

- closed-world versus operational intrusion detection;
- network-intrusion dataset validity;
- general machine-learning pitfalls in computer security;
- concept and feature drift in IDS;
- base-rate effects and false alarms;
- documented benchmark-construction problems;
- recent generative-AI phishing robustness studies.

The combined paper bibliography expanded from 11 to 19 references.

### 2. Network uncertainty intervals added

The paper now reports Wilson 95% intervals for:

- validation attack recall;
- validation FPR;
- official-test attack recall;
- official-test FPR;
- `sttl`-neutralized recall/FPR;
- TTL-family-neutralized recall/FPR.

A Newcombe interval is also reported for the validation-to-test change in FPR and recall.

### 3. Operational base-rate analysis added

The paper now shows how the official-test HGB TPR/FPR would translate into positive predictive value under hypothetical attack prevalences.

These are scenario calculations, not deployment estimates.

### 4. Counter-hypotheses made explicit

The Human discussion now states that the synthetic decline cannot be attributed to AI authorship alone because recency, source, generation process, style, corpus construction, and safety constraints changed together.

The Network discussion now explicitly separates TTL dependence from possible causes of the official-test distribution gap.

### 5. Network multi-seed stability executed

A five-seed HGB validation analysis was run using seeds:

`[7, 17, 29, 42, 73]`

The consumed official test was not read.

Results:

- accuracy mean 95.50%, SD 0.06 percentage points;
- recall mean 97.50%, SD 0.08 pp;
- FPR mean 8.77%, SD 0.14 pp;
- balanced accuracy mean 94.37%, SD 0.07 pp;
- ROC AUC mean 99.28%, SD 0.01 pp.

The seed-42 result reproduced the already verified v1 validation metrics exactly to recorded precision.

The supplementary run used scikit-learn 1.8.0, which is disclosed because the captured project-machine environment records scikit-learn 1.9.1.

### 6. External validation preregistered

A frozen external-validation protocol was added before any v2 external-model evaluation.

It specifies:

- dataset eligibility and provenance rules;
- no post-result dataset selection;
- frozen models and threshold;
- primary metrics;
- calibration metrics;
- Wilson/Newcombe uncertainty methods;
- consumed-set restrictions;
- direct Network transportability versus independent-protocol replication;
- reporting rules for negative results.

### 7. External Human evaluator added

`Phase-1-Phishing-Detection/src/evaluate_external_holdout.py` now supports frozen two-class external evaluation with:

- standard classification metrics;
- FPR/FNR;
- balanced accuracy;
- ROC AUC;
- Wilson intervals;
- Brier score;
- 10-bin expected calibration error;
- dataset SHA-256;
- prediction export;
- explicit no-tuning behavior.

### 8. Multi-seed scripts added

Publication-preparation scripts now exist for:

- Network HGB five-seed validation stability;
- Human DistilBERT five-seed validation stability.

The Human multi-seed script has not been executed in this revision because the required transformer training environment and training artifacts are not available in the current audit runtime. No result is claimed.

## Remaining Evidence Gap

The most important unresolved publication-level limitation is **independent contemporary external validation**.

A suitable external holdout cannot be treated as valid merely because it is newer. It must pass source-provenance and overlap checks before model inference.

A 2024 Zenodo dataset containing 2,000 safe/phishing messages has been recorded as a **candidate**, not accepted automatically, because its full source provenance is not sufficiently detailed in the dataset description.

No external performance number is reported until a candidate passes the frozen eligibility rules and the frozen v1 model artifacts can be evaluated without tuning.

## Current Manuscript Status

The manuscript is materially stronger than the original v1 combined paper in:

- scholarly context;
- uncertainty reporting;
- operational interpretation;
- alternative-hypothesis discussion;
- Network seed-stability evidence;
- preregistered next-stage validation.

It still should not be described as having solved the external-validity problem until the preregistered independent holdout is actually executed.
