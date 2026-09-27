# Formal Development-Set Exploratory Data Analysis

## Scope

EDA is restricted to the **140,269-row development partition**. Validation is reserved for model-development evaluation, and the official UNSW-NB15 test partition remains sealed for final evaluation.

The pre-modeling feature policy excludes `id`, `attack_cat`, and `ct_ftp_cmd` from binary-classifier inputs. `attack_cat` is used here only as descriptive metadata.

## Class Structure

The development partition contains:

- 95,470 attack records
- 44,799 benign records
- attack prevalence: **68.0621%**

Attack-category counts are:

| Category | Records |
| --- | ---: |
| Normal | 44,799 |
| Generic | 32,346 |
| Exploits | 26,505 |
| Fuzzers | 14,471 |
| DoS | 9,741 |
| Reconnaissance | 8,434 |
| Analysis | 1,579 |
| Backdoor | 1,384 |
| Shellcode | 905 |
| Worms | 105 |

The large differences in category sample size mean aggregate binary metrics can hide weak performance on rare attack families. Category-level results will therefore be reported alongside overall metrics, with strong uncertainty caveats for very small categories such as Worms.

## Categorical Predictors

Three primary categorical predictors remain:

| Feature | Unique values |
| --- | ---: |
| `proto` | 133 |
| `service` | 13 |
| `state` | 8 |

Most common values include TCP and UDP for `proto`; the unspecified `-` value and DNS for `service`; and INT and FIN for `state`.

Some rare categorical values are strongly class-associated in this controlled dataset. These are not automatically treated as leakage, but later interpretation and robustness analyses must test whether models rely on category artifacts that may not generalize.

## Numerical Associations

The strongest development-set Pearson associations with the binary label include:

| Feature | Pearson r |
| --- | ---: |
| `sttl` | 0.695 |
| `ct_state_ttl` | 0.577 |
| `dload` | -0.392 |
| `ct_dst_sport_ltm` | 0.363 |
| `dmean` | -0.342 |
| `rate` | 0.339 |
| `swin` | -0.335 |
| `dwin` | -0.321 |
| `ct_src_dport_ltm` | 0.309 |
| `ct_dst_src_ltm` | 0.305 |

These are descriptive univariate relationships, not causal effects or measures of standalone model importance.

The especially strong associations involving TTL/state-derived variables reinforce the need for later feature-importance and robustness analysis.

## Distribution Shape and Sparsity

Many traffic-volume and timing variables are highly right-skewed. Particularly extreme skew appears in `trans_depth`, `response_body_len`, `sbytes`, `sloss`, `spkts`, `dloss`, `dbytes`, and `dpkts`.

Several features are also dominated by zero values:

- `is_ftp_login`: approximately 98.5% zero
- `is_sm_ips_ports`: approximately 98.3% zero
- `response_body_len`: approximately 93.6% zero
- `trans_depth` and `ct_flw_http_mthd`: approximately 89.9% zero

These distributions argue against assuming normally distributed predictors. Sparse features are retained unless subsequent evidence provides a methodological reason for removal.

## Modeling Implications

The EDA supports the following pre-training decisions:

1. Use preprocessing capable of handling mixed numerical and categorical data.
2. Fit all preprocessing transformations on development data only.
3. Do not infer category vocabularies from validation or test data.
4. Do not remove highly predictive features merely because their univariate associations are strong.
5. Report false-positive and false-negative rates in addition to accuracy/F1 because of class imbalance.
6. Report attack-family performance where sample size permits.
7. Explicitly inspect feature reliance after training, especially for TTL/state-related variables.
8. Preserve a later distribution-shift evaluation because strong internal validation alone cannot establish generalization.

## Reproducibility

`src/formal_eda.py` reproduces the EDA and writes machine-readable tables plus publication-style figures to `results/eda/`.

The script reads only `data/processed/development.csv`.
