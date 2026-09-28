# Final Scientific Audit — Defensive AI Cybersecurity v1

**Audit date:** 2026-09-27  
**Scope:** Human Layer, Network Layer, Cross-Layer Integration, combined paper, repository landing pages, machine-readable results, publication figures, reproducibility records, and defensive demos.

## Audit Outcome

**PASS with documented limitations.**

The final audit found no remaining numerical contradiction in the headline Human Layer, Network Layer, or cross-layer results after correction. Confusion-matrix arithmetic, percentage-point changes, Human Wilson intervals, the Human exact paired McNemar result, Network robustness values, Network final-test values, and the values displayed in the principal integration figures were cross-checked against the preserved result records.

No experimental headline metric required revision during this final audit.

The audit did identify repository implementation and documentation defects. These were corrected before v1 was closed.

## Quantitative Verification

### Human Layer

The untouched historical-test confusion matrices reproduce the reported metrics:

- TF-IDF + Logistic Regression: 16,023 TN, 320 FP, 227 FN, 14,655 TP
- DistilBERT: 16,228 TN, 115 FP, 125 FN, 14,757 TP

These counts reproduce the reported historical-test results, including:

- baseline accuracy 98.2482%, recall 98.4747%, FPR 1.9580%
- DistilBERT accuracy 99.2314%, recall 99.1601%, FPR 0.7037%

The controlled synthetic totals are internally consistent:

- baseline: 277/500 detected = 55.40%
- DistilBERT: 181/500 detected = 36.20%
- paired outcomes: 168 both detected, 210 both missed, 109 baseline-only detected, 13 DistilBERT-only detected
- paired outcomes sum to 500
- exact two-sided McNemar p-value: approximately 4.6782 × 10^-20
- DistilBERT high-confidence misses: 290/319 at >=90% raw confidence and 233/319 at >=99%

The reported overall and category-level Wilson intervals were independently recalculated and agree with the documented rounded values.

### Network Layer

The preserved validation and final-test confusion matrices reproduce the reported metrics.

Logistic Regression validation:

- 9,155 TN, 2,046 FP, 310 FN, 23,561 TP
- accuracy 93.2824%
- recall 98.7014%
- FPR 18.2662%
- balanced accuracy 90.2176%

Histogram Gradient Boosting validation:

- 10,239 TN, 962 FP, 583 FN, 23,288 TP
- accuracy 95.5948%
- recall 97.5577%
- FPR 8.5885%
- balanced accuracy 94.4846%

Histogram Gradient Boosting official final test:

- 27,273 TN, 9,727 FP, 666 FN, 44,666 TP
- accuracy 87.3767%
- recall 98.5308%
- FPR 26.2892%
- balanced accuracy 86.1208%

Verified controlled robustness conditions include:

- `sttl` neutralization: 97.6708% recall, 58.8430% FPR, 69.4139% balanced accuracy
- TTL-family neutralization: 97.6457% recall, 84.0729% FPR, 56.7864% balanced accuracy

The final audit found no recurrence of the earlier superseded robustness values.

## Cross-Layer Verification

The cross-layer CSV, synthesis document, combined paper, root README, and principal SVG figures agree on the main comparison:

- Human DistilBERT historical-test recall: 99.16%
- Human DistilBERT controlled synthetic detection: 36.20%
- Network HGB validation FPR: 8.59%
- Network HGB official-test FPR: 26.29%
- Network HGB `sttl`-neutralized FPR: 58.84%
- Network HGB TTL-family-neutralized FPR: 84.07%

The integration correctly avoids pooling unlike Human and Network metrics into a single score or cross-layer significance test.

## Methodology and Claim Audit

The final documents consistently preserve the following boundaries:

- the Human synthetic set is positive-only and cannot estimate synthetic precision, FPR, or overall accuracy;
- the controlled synthetic set is not claimed to represent all real-world or AI-generated phishing;
- raw DistilBERT softmax confidence is not treated as a calibrated real-world probability;
- UNSW-NB15 is a controlled cyber-range benchmark and does not establish present-day production-network performance;
- TTL neutralization is a diagnostic feature-information ablation, not a realistic attacker action;
- the project does not claim TTL dependence caused the official Network test gap;
- the Human and Network experiments are not treated as one pooled statistical experiment;
- neither detector is presented as safe for autonomous production blocking.

## Reference Audit

The 11 references in the combined paper were spot-checked against publisher, dataset, conference, or scholarly index records. Titles, authorship, publication venues/years, and DOI or canonical identifiers were found to be consistent with the cited works.

This included the Human dataset's Zenodo v2 record and the UNSW-NB15 IEEE publication.

## Link and Figure Audit

Relative links in the principal root, Human, Network, and cross-layer Markdown documents were checked against the repository tree. No broken relative links were found in the audited documents.

The principal Human and cross-layer SVG figures were checked against the preserved numerical results. The Network synthesis figures were likewise checked against the verified validation, robustness, and final-test records.

## Corrections Made During Final Audit

### 1. Human Streamlit demo startup bug

**Problem:** `phishing_detector_app.py` loaded the tokenizer from `MODEL_ID` but attempted to load the model from an undefined `MODEL_DIR`.

**Correction:** model loading now uses `MODEL_ID`, matching the documented Hugging Face model source.

### 2. Network figure-regeneration bug

**Problem:** `src/generate_figures.py` attempted to read `validation["fpr"]`, while the verified stronger-model validation JSON stores the field as `false_positive_rate`.

**Correction:** the figure generator now reads `validation["false_positive_rate"]`.

This bug affected regeneration code, not the already verified numerical results.

### 3. Network provenance/environment inconsistency

**Problem:** the provenance document still contained pre-experiment future-tense language claiming that the dependency snapshot would be captured before modeling, while the completed reproducibility audit correctly states that the project-machine environment was captured at project completion.

**Correction:** the provenance record now describes what was actually preserved and explicitly states the timing limitation.

### 4. Environment snapshot formatting

**Problem:** `network_environment.txt` contained `Python==3.13.5`, which is not a pip package and should not appear as a package-freeze entry.

**Correction:** the line was removed. Python 3.13.5 remains documented separately in the reproducibility audit.

### 5. Human report wording

**Problem:** the Human report abstract contained the duplicated phrase `controlled controlled synthetic`.

**Correction:** corrected to `controlled synthetic`.

### 6. Repository map clarity

**Problem:** the root map visually presented Network `data/` and `models/` as ordinary tracked directories even though the large raw data and generated model artifacts are intentionally not committed.

**Correction:** the map now marks these as local/generated, non-committed runtime directories.

### 7. Network EDA console output

**Problem:** the EDA script printed the categorical-cardinality dictionary expression literally instead of printing its evaluated values.

**Correction:** the diagnostic print now evaluates the dictionary.

## Reproducibility Status

### Human Layer

Strengths include preserved scripts, split sizes, model/test hashes where recorded, synthetic methodology, paired statistics, final-test records, and frozen evaluation policies.

Known limitation: the frozen TF-IDF artifact was serialized under scikit-learn 1.9.1 and later loaded under 1.6.1 with a documented compatibility adjustment. The exact original full training environment was not perfectly locked.

### Network Layer

Strengths include raw-file SHA-256 hashes, deterministic seed policy, leakage audit, group-preserving split logic, frozen model configurations, pre-specified robustness protocol, machine-readable verified metrics, final-test records, and a captured project-machine package environment.

A prior independent computational rerun reproduced the core split, validation, interpretation, and final-test results and exposed the earlier robustness-report mismatch that was corrected before integration.

Known limitations: the package snapshot was captured after project completion rather than automatically at the precise original training instant; exact hardware and OS build were not independently archived; trained-model artifact hashes were not preserved in the final v1 reproducibility record.

## Consumed Evaluation Policy

The Human historical test set, Human 500-message controlled synthetic evaluation, and Network official final test have all informed the completed v1 conclusions.

They must not be treated as fresh unbiased final holdouts for future tuned models. Any v2 model changes informed by these results require new independent evaluation data for an unbiased final estimate.

## Residual Scientific Limitations

The following remain legitimate limitations rather than repository defects:

1. the Human historical corpus combines older public sources;
2. the Human positive class is broader than narrowly defined credential phishing;
3. the controlled synthetic set contains 500 positive examples from two generation sources and five designed styles;
4. the Human synthetic set cannot measure false positives;
5. UNSW-NB15 comes from a controlled cyber-range and is not contemporary production traffic;
6. the Network split cannot prove host/session/temporal/campaign independence beyond the identifiers available in the modeling CSV;
7. rare Network attack families have wide uncertainty;
8. neither layer has yet been independently validated on a new contemporary external deployment dataset;
9. neither system is a production security product.

## Final v1 Conclusion

The repository supports the following bounded conclusion:

> **Strong performance on familiar benchmark distributions did not guarantee stable defensive behavior under changed information distributions. In the Human Layer, the controlled synthetic shift primarily exposed false negatives. In the Network Layer, the official test and controlled feature-information shifts primarily exposed false positives.**

The evidence does not support stronger universal claims about all AI-generated phishing, all network attacks, production deployment, or a universally superior model family.

**Final audit status: PASS. Defensive AI Cybersecurity v1 is complete and review-ready, subject to the documented limitations above.**


---

## Post-Audit Publication-Strengthening Addendum

After the v1 audit passed, a graduate-level peer-review simulation identified areas where the manuscript could be strengthened without changing the frozen v1 experiments.

The following work was subsequently completed:

- expanded the combined literature review from 11 to 19 references;
- added Wilson uncertainty intervals for primary Network rates;
- added Newcombe intervals for validation-to-test rate differences;
- added a base-rate/positive-predictive-value scenario analysis;
- added explicit counter-hypotheses for both Human and Network shifts;
- executed a five-seed supplementary HGB validation analysis without reopening the official test;
- added a frozen external-validation preregistration;
- added external-Human and multi-seed evaluation scripts;
- updated layer-specific reports and repository navigation.

The five-seed Network analysis found only small internal variation. Seed-42 exactly reproduced the already verified v1 validation metrics to recorded precision in the supplementary audit environment.

These additions strengthen the manuscript, but they do not erase the most important remaining limitation: no qualifying new contemporary independent external holdout has yet been executed with the frozen v1 models.

**Updated status:** v1 remains scientifically complete and internally audited. Publication preparation is substantially strengthened. External validation remains the principal outstanding empirical requirement for a stronger high-tier generalization claim.
