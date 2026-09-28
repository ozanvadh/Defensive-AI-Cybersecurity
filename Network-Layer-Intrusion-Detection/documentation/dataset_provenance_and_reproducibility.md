# Network Layer Dataset Provenance and Reproducibility Plan

## Research Scope

The Network Layer investigates the following primary research question:

> How accurately can machine-learning models distinguish malicious from benign network traffic while maintaining a low false-positive rate, and how robust are those models when evaluated under network-traffic distribution shift?

The work is limited to defensive classification of pre-recorded public network-flow data. It does not involve scanning, attacking, probing, or generating malicious traffic against real systems.

## Primary Dataset

**Dataset:** UNSW-NB15  
**Creator:** UNSW Canberra Cyber Range Lab  
**Official source:** https://research.unsw.edu.au/projects/unsw-nb15-dataset  
**Original publication:** Nour Moustafa and Jill Slay, "UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)," MilCIS, 2015. DOI: 10.1109/MilCIS.2015.7348942

According to the official dataset documentation, UNSW-NB15 was created using the IXIA PerfectStorm tool in the UNSW Canberra Cyber Range Lab. The dataset combines normal network activity with synthetic attack behavior. Approximately 100 GB of raw traffic was captured with tcpdump. Argus, Bro-IDS, and additional feature-generation algorithms were used to derive network-flow features.

The complete dataset contains 2,540,044 records stored across four primary CSV files. The official documentation describes 49 features with the class label.

Nine attack categories are represented:

- Fuzzers
- Analysis
- Backdoors
- DoS
- Exploits
- Generic
- Reconnaissance
- Shellcode
- Worms

The dataset also includes normal traffic.

## Official Modeling Partitions

The initial Network Layer experiment will use the official preconfigured modeling partitions:

- `UNSW_NB15_training-set.csv`: 175,341 records
- `UNSW_NB15_testing-set.csv`: 82,332 records

The official testing partition will remain isolated from model development.

A validation partition will be derived only from the official training data. The exact validation procedure, random seed, class distributions, duplicate checks, and any grouping or leakage controls will be documented before model training.

## Verified Raw File Integrity

The original uploaded CSV files were verified before preprocessing.

| File | Bytes | Rows | Columns | Missing Values | Exact Duplicate Rows | SHA-256 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `UNSW_NB15_training-set.csv` | 32,293,018 | 175,341 | 45 | 0 | 0 | `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa` |
| `UNSW_NB15_testing-set.csv` | 15,380,800 | 82,332 | 45 | 0 | 0 | `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559` |

Observed binary-label counts:

- Training: 119,341 attack and 56,000 normal.
- Testing: 45,332 attack and 37,000 normal.

The preconfigured modeling CSVs contain 45 columns as observed directly from the files. This observed schema count is used for the experiment even though broader UNSW-NB15 documentation describes a larger feature set in other dataset representations.

The official testing CSV was inspected only for file integrity, schema, labels, missingness, duplicate-row count, and category counts. Its predictive features were not used for model development, feature selection, preprocessing fitting, hyperparameter tuning, or model selection.

## Raw Dataset Verification

The two official preconfigured modeling CSVs were verified before preprocessing. Verification was limited to file identity, schema, row counts, missing values, exact duplicate rows, and label/category counts. No test-set features were used for model selection, feature selection, threshold selection, or tuning.

### Training partition

- Filename: `UNSW_NB15_training-set.csv`
- Size: 32,293,018 bytes
- SHA-256: `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`
- Rows: 175,341
- Columns: 45
- Missing values: 0
- Exact duplicate rows: 0
- Attack records (`label = 1`): 119,341
- Normal records (`label = 0`): 56,000

Training attack-category counts:

- Normal: 56,000
- Generic: 40,000
- Exploits: 33,393
- Fuzzers: 18,184
- DoS: 12,264
- Reconnaissance: 10,491
- Analysis: 2,000
- Backdoor: 1,746
- Shellcode: 1,133
- Worms: 130

### Testing partition

- Filename: `UNSW_NB15_testing-set.csv`
- Size: 15,380,800 bytes
- SHA-256: `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559`
- Rows: 82,332
- Columns: 45
- Missing values: 0
- Exact duplicate rows: 0
- Attack records (`label = 1`): 45,332
- Normal records (`label = 0`): 37,000

Testing attack-category counts:

- Normal: 37,000
- Generic: 18,871
- Exploits: 11,132
- Fuzzers: 6,062
- DoS: 4,089
- Reconnaissance: 3,496
- Analysis: 677
- Backdoor: 583
- Shellcode: 378
- Worms: 44

### Observed schema

The supplied preconfigured training and testing CSVs each contain 45 columns:

`id`, `dur`, `proto`, `service`, `state`, `spkts`, `dpkts`, `sbytes`, `dbytes`, `rate`, `sttl`, `dttl`, `sload`, `dload`, `sloss`, `dloss`, `sinpkt`, `dinpkt`, `sjit`, `djit`, `swin`, `stcpb`, `dtcpb`, `dwin`, `tcprtt`, `synack`, `ackdat`, `smean`, `dmean`, `trans_depth`, `response_body_len`, `ct_srv_src`, `ct_state_ttl`, `ct_dst_ltm`, `ct_src_dport_ltm`, `ct_dst_sport_ltm`, `ct_dst_src_ltm`, `is_ftp_login`, `ct_ftp_cmd`, `ct_flw_http_mthd`, `ct_src_ltm`, `ct_srv_dst`, `is_sm_ips_ports`, `attack_cat`, and `label`.

The observed 45-column schema is recorded as the authoritative schema for these downloaded modeling files. Documentation describing broader UNSW-NB15 feature sets should not be interpreted as evidence that these specific preconfigured CSVs contain 49 columns.

The official test partition remains reserved for final model evaluation. Structural integrity verification does not constitute model-development use of the test features.

## Labels

The primary task is binary intrusion detection:

- `label = 0`: normal
- `label = 1`: attack

The `attack_cat` field identifies attack categories and will be retained for evaluation and error analysis. It will **not** be used as a predictive input for the binary classifier because it directly describes the target class and would introduce target leakage.

## Untouched-Test Policy

The official test partition is reserved for one final evaluation after:

1. preprocessing decisions are frozen;
2. feature-selection and leakage decisions are frozen;
3. candidate models are trained and compared using training/validation data;
4. hyperparameters and decision thresholds are frozen;
5. robustness experiments used for model-development decisions are complete;
6. the final evaluation protocol is documented.

After the official test partition is consumed, it will be treated permanently as consumed and will not be used for subsequent tuning, model selection, threshold adjustment, calibration fitting, or feature selection.

Any later model improvements will require a new independent holdout for unbiased final evaluation.

## Raw-Data Preservation

Original downloaded dataset files will be preserved unchanged under the local raw-data directory and excluded from ordinary source-control commits when their size makes Git storage inappropriate.

Before processing, the project will record for every downloaded source file:

- exact filename;
- byte size;
- SHA-256 hash;
- source URL;
- download date.

Cleaning and transformation will be performed through reproducible scripts rather than manual spreadsheet editing.

## Reproducibility Policy

The project records the information that was actually preserved during Network Layer v1:

- Python version;
- captured project-machine package versions;
- fixed random seed;
- preprocessing and leakage policy;
- model hyperparameters;
- raw-dataset hashes;
- evaluation and robustness scripts;
- machine-readable validation, robustness, and final-test metrics.

The package snapshot was captured at project completion rather than automatically at the exact instant each model artifact was trained. It is therefore described as the **captured project-machine environment**, not as proof that no package changed during the modeling session.

Python 3.13.5 is documented separately from the package snapshot. The package file `network_environment.txt` preserves package-version output rather than representing Python itself as a pip package.

Exact operating-system build, hardware details, trained-model artifact hashes, and an automatically captured environment from the precise original training instant were not independently archived for v1. These are reproducibility limitations rather than inferred values.

## Seed Policy

A fixed seed of **42** will be used where deterministic randomization is required unless a later experiment explicitly studies seed sensitivity.

Every script that performs randomized splitting, sampling, or model initialization must set and document its seed.

A fixed seed improves repeatability but does not guarantee bit-for-bit reproducibility across different libraries, hardware, operating systems, or parallel implementations.

## Leakage Audit

Before model training, the project will explicitly investigate:

- exact duplicate records;
- duplicates or highly related records across partitions;
- target-derived columns;
- identifiers that may encode collection artifacts;
- attack-category leakage;
- time or session information that could make the task artificially easy;
- categorical features with suspiciously direct relationships to the target;
- preprocessing fitted outside the training partition.

Any feature removed for leakage reasons will be documented with the reason for removal.

## Evaluation Metrics

Primary binary-classification metrics will include:

- accuracy;
- precision;
- recall;
- F1 score;
- false-positive rate;
- false-negative rate;
- confusion matrix.

Attack-category-specific detection performance will also be reported where sample sizes permit meaningful interpretation.

Because intrusion-detection systems can generate operational burden through false alarms, false-positive rate will be treated as a primary metric rather than relying on accuracy alone.

## Distribution-Shift Evaluation

The official test set provided the primary held-out evaluation for the UNSW-NB15 modeling protocol and was consumed only after model-development and robustness decisions were frozen.

After the training data were inspected and the leakage structure was understood, a separate robustness protocol was pre-specified and committed before execution. It evaluated the frozen stronger model under controlled feature-information transformations, including `sttl` neutralization, TTL-family neutralization, and categorical-novelty conditions.

These controlled transformations are diagnostic stress tests. They are not described as realistic adversarial attacks or as external real-world traffic, and their results are not automatically generalized to deployment.

## Known Scope Limitation

UNSW-NB15 was generated in a controlled cyber-range environment rather than collected as an unrestricted sample of modern production networks. Therefore, performance on UNSW-NB15 alone cannot establish real-world deployment performance.

This limitation motivated the completed distribution-shift and robustness evaluation.

## Citation

Moustafa, N., & Slay, J. (2015). UNSW-NB15: A comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set). *2015 Military Communications and Information Systems Conference (MilCIS)*. IEEE. https://doi.org/10.1109/MILCIS.2015.7348942

## Record Status

This document was created before Network Layer dataset processing or model training and was later updated with observed raw-file hashes, structural integrity results, feature-policy decisions, and final reproducibility limitations. The completed v1 environment record is preserved in `../network_environment.txt`, with Python 3.13.5 documented separately in the reproducibility audit.

The official test set has been consumed for v1, so future model changes informed by these results require a new independent holdout for an unbiased final evaluation.
