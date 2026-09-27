# Development / Validation Split Protocol

## Purpose

The official UNSW-NB15 training partition contains many repeated predictor vectors. Randomly assigning individual rows could place identical modeling inputs in both development and validation data and inflate validation performance.

The Network Layer therefore uses a **group-preserving split**.

## Predictor Group Definition

Rows are grouped by the complete candidate modeling feature vector after excluding the pre-modeling removals:

- `id`
- `attack_cat`
- `label`
- `ct_ftp_cmd`

Every row with the same remaining predictor values is assigned to the same partition.

## Assignment Procedure

The official 175,341-row training partition is divided into approximately:

- 80% development
- 20% validation

Seed: **42**

Predictor-vector groups are categorized as:

- all-normal;
- all-attack;
- mixed/conflicting-label.

Groups are randomly assigned within these categories using the fixed seed until approximately 20% of the rows in each group type have been allocated to validation.

The official UNSW-NB15 test partition is not read by the splitting script.

## Result

Applying the frozen procedure produced:

| Partition | Rows | Attack rate |
| --- | ---: | ---: |
| Development | 140,269 | 68.0621% |
| Validation | 35,072 | 68.0628% |

**Complete predictor-vector groups shared across development and validation: 0**

### Development attack-category counts

| Category | Rows |
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

### Validation attack-category counts

| Category | Rows |
| --- | ---: |
| Normal | 11,201 |
| Generic | 7,654 |
| Exploits | 6,888 |
| Fuzzers | 3,713 |
| DoS | 2,523 |
| Reconnaissance | 2,057 |
| Analysis | 421 |
| Backdoor | 362 |
| Shellcode | 228 |
| Worms | 25 |

The nearly identical binary class proportions were achieved without allowing identical modeling predictor vectors to cross partitions.

## Important Limitation

Grouping exact predictor vectors prevents one clear form of leakage, but it does not prove that development and validation traffic are independent at the original network-session, host, temporal, or attack-campaign level. The preconfigured CSVs do not preserve every identifier that would be required to reconstruct all such dependencies.

Validation performance will therefore be interpreted as internal development evidence rather than proof of deployment-level generalization. The later distribution-shift experiment is intended to provide a substantially stronger robustness challenge.

## Reproducibility

The exact procedure is implemented in:

`src/create_development_validation_split.py`

The split must be generated from the untouched official training CSV. The reserved official test CSV is not an input to the script.
