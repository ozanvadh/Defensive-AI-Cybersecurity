# Stronger-Model Interpretation and Error Analysis

Interpretation was performed on the already evaluated validation model. It was not used to access or tune against the official test partition.

## Permutation Importance

Permutation importance was measured using validation balanced accuracy, with five deterministic repeats (seed 42). The largest observed importance values were:

| Feature | Mean decrease in balanced accuracy |
| --- | ---: |
| `sttl` | **0.2731** |
| `sbytes` | 0.0228 |
| `smean` | 0.0226 |
| `ct_dst_src_ltm` | 0.0199 |
| `ct_dst_sport_ltm` | 0.0167 |
| `ct_srv_dst` | 0.0164 |
| `ct_srv_src` | 0.0156 |
| `dmean` | 0.0149 |
| `proto` | 0.0118 |
| `dbytes` | 0.0106 |
| `service` | 0.0101 |
| `ct_dst_ltm` | 0.0097 |

The result is striking: permuting `sttl` alone reduces balanced accuracy by roughly **27 percentage points**, far more than any other individual feature. This does not prove that `sttl` is leakage or causal. It does show that the fitted model depends heavily on a source-TTL pattern present in this dataset.

That dependence is now a specific robustness hypothesis to test rather than something to silently remove after observing validation results.

## Where the False Negatives Occur

The nonlinear model made 583 attack false negatives. They were highly concentrated:

| Attack family | Validation attacks | Misses | Miss rate |
| --- | ---: | ---: | ---: |
| Fuzzers | 3,713 | **496** | **13.36%** |
| Analysis | 421 | **44** | **10.45%** |
| Shellcode | 228 | 3 | 1.32% |
| Exploits | 6,888 | 33 | 0.48% |
| DoS | 2,523 | 3 | 0.12% |
| Reconnaissance | 2,057 | 2 | 0.10% |
| Generic | 7,654 | 2 | 0.03% |
| Backdoor | 362 | 0 | 0.00% |
| Worms | 25 | 0 | 0.00% |

**540 of the 583 attack misses (92.62%) are Fuzzers or Analysis**, even though those two families account for a much smaller fraction of validation attacks.

The Worm result is based on only 25 observations and is not evidence of reliable perfect detection.

## Error-Profile Clues

For Fuzzers, missed flows have lower median `sbytes` (629 versus 994) and lower median `smean` (59 versus 91) than detected Fuzzer flows, while their median `sttl` is the same (254).

For Analysis traffic, the contrast is more pronounced. Missed Analysis flows have median `sttl` of **62**, compared with **254** among correctly detected Analysis flows. Missed Analysis flows also have larger median `sbytes` (827 versus 200) and `dbytes` (1,162 versus 0).

These are descriptive associations, not causal explanations. They suggest that some Analysis attacks resemble patterns the classifier has learned to associate with benign traffic, especially around TTL and traffic-volume behavior.

## Scientific Interpretation

Aggregate validation performance conceals two vulnerabilities:

1. **Concentrated attack-family failures.** Most false negatives come from Fuzzers and Analysis.
2. **Heavy dependence on one feature.** The model relies unusually strongly on `sttl`.

This creates a concrete next robustness question: does performance remain strong when the model cannot rely as heavily on the TTL-related signal, and how does performance change under a defensible network-traffic distribution shift?

No feature has been removed or model retrained based on these interpretation results yet. Any robustness experiment must be specified before it is run to avoid post-hoc result chasing.

## Reproducibility

`src/analyze_stronger_model.py` reproduces the permutation-importance and attack-family error analysis and writes machine-readable outputs under `results/stronger_model/interpretation/`.
