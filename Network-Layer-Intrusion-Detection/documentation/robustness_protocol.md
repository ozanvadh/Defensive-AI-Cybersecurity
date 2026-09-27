# Pre-Specified Network Robustness and Distribution-Shift Protocol

## Status

This protocol is frozen **before the robustness experiments are executed**. It was motivated by development/validation findings but is being committed before observing the outcomes of the experiments defined below.

The official UNSW-NB15 test partition is not used in these experiments and remains reserved for final evaluation.

## Motivation

The frozen Histogram Gradient Boosting validation model achieved strong aggregate performance but showed two warning signs:

1. Permutation of `sttl` caused an unusually large decrease in validation balanced accuracy, suggesting heavy dependence on source-TTL information.
2. False negatives were concentrated in Fuzzers and Analysis traffic.

These observations motivate targeted robustness tests. They do not establish that `sttl` is leakage, nor do they establish that any controlled perturbation represents real deployment traffic.

## Frozen Model

The primary subject is the already trained Histogram Gradient Boosting pipeline:

`models/hist_gradient_boosting.joblib`

No retraining, hyperparameter tuning, threshold tuning, or feature removal will occur during the primary perturbation experiments.

The Logistic Regression baseline may be evaluated under the same perturbations as a secondary comparison if its frozen artifact is available.

## Reference Condition

The unmodified leakage-resistant validation partition is the reference condition.

All robustness effects will be reported relative to the exact unmodified validation predictions already established.

## Experiment A: Source-TTL Information Removal

### Question

How much does the frozen classifier's performance change when the source-TTL signal is no longer informative at inference time?

### Transformation

Create a copy of validation data and replace every `sttl` value with the **median `sttl` calculated from development data only**.

No other feature is changed.

### Interpretation

This is a controlled feature-ablation stress test, **not a simulation of a specific real-world attack**. A large degradation would demonstrate reliance on `sttl`, but would not by itself prove vulnerability to an attacker or deployment failure.

## Experiment B: TTL-Family Information Removal

### Question

Is the model's dependence broader than `sttl` alone?

### Transformation

Create a second validation copy and replace the following TTL/state-derived numerical fields with their respective **development-set medians**:

- `sttl`
- `dttl`
- `ct_state_ttl`

All replacements are determined from development data only.

### Interpretation

This tests sensitivity to a broader TTL/state-derived signal family. It remains a controlled ablation rather than a claim about realistic adversarial manipulation.

## Experiment C: Attack-Family Distribution Shift

### Question

How does performance change when evaluation emphasizes attack families for which the frozen model showed weaker internal generalization?

### Frozen subsets

Without changing model inputs, report performance separately for:

- Fuzzers
- Analysis
- all other malicious families combined
- benign traffic

This experiment does not manufacture new traffic. It treats the observed attack-family composition as a distributional dimension and quantifies heterogeneity that aggregate metrics can conceal.

Because the Analysis subset is relatively small, uncertainty intervals must accompany its detection-rate estimate.

## Experiment D: Categorical Novelty Stress Test

### Question

How sensitive is the frozen model to categorical values that were not available during model fitting?

### Transformation

For each categorical feature (`proto`, `service`, `state`) independently, replace that feature in the validation copy with a single reserved unknown token that was not present during fitting. The frozen encoder's configured unknown-category behavior will handle the value.

Run three one-feature conditions plus one combined condition in which all three categorical features are unknown.

### Interpretation

This is a controlled missing/novel-category stress test. It does not claim that all categories would simultaneously become unknown in deployment.

## Metrics Frozen in Advance

For every applicable condition report:

- accuracy
- precision
- recall / true-positive rate
- F1
- false-positive rate
- false-negative rate
- balanced accuracy
- ROC AUC when probability outputs remain meaningful
- confusion matrix

For attack-family subsets, report sample size, detection rate, number missed, and a 95% Wilson confidence interval for the detection rate.

## Primary Comparisons

The principal robustness quantities are absolute percentage-point changes from the unmodified validation condition in:

1. balanced accuracy;
2. false-positive rate;
3. false-negative rate;
4. attack recall.

No single metric will be used alone to characterize robustness.

## Rules Against Post-Hoc Result Chasing

After this protocol is committed:

- the perturbations will not be redefined because a result is weak, strong, or inconvenient;
- the default decision threshold will not be changed to improve stress-test results;
- model hyperparameters will not be tuned against these conditions;
- no feature will be removed and the model retrained as part of the primary experiment;
- additional exploratory analyses are allowed only if clearly labeled **post-hoc exploratory**;
- the official test set remains unavailable until the model and evaluation plan are frozen for final testing.

## Claims Policy

The study may conclude that the model is **sensitive to a specified controlled perturbation** if the measured metrics materially change.

It must not automatically describe controlled feature replacement as a realistic cyberattack, adversarial exploit, or estimate of real-world degradation.

Similarly, stability under these tests would provide evidence only against the specific tested sensitivities, not proof of general robustness.

## Reproducibility

The implementation must:

- load the frozen model artifact;
- read the development partition only to calculate pre-specified medians;
- read validation for evaluation;
- never read the official test partition;
- use deterministic transformations;
- save condition-level metrics and attack-family results in machine-readable files.
