# Statistical Uncertainty and Operational Interpretation

## Purpose

This supplement adds uncertainty estimates and an operational base-rate analysis without changing any frozen v1 model or reusing final test data for tuning.

## Network Rate Intervals

Wilson 95% confidence intervals calculated from the preserved confusion-matrix counts:

| Condition | Metric | Estimate | 95% Wilson CI |
| --- | --- | ---: | ---: |
| HGB validation | Attack recall | 97.56% | 97.35%-97.75% |
| HGB validation | FPR | 8.59% | 8.08%-9.12% |
| HGB official test | Attack recall | 98.53% | 98.42%-98.64% |
| HGB official test | FPR | 26.29% | 25.84%-26.74% |
| HGB `sttl` neutralized | Attack recall | 97.67% | 97.47%-97.85% |
| HGB `sttl` neutralized | FPR | 58.84% | 57.93%-59.75% |
| HGB TTL family neutralized | Attack recall | 97.65% | 97.45%-97.83% |
| HGB TTL family neutralized | FPR | 84.07% | 83.38%-84.74% |

## Validation-to-Test Differences

Using Newcombe intervals for independent proportions:

- official-test FPR minus validation FPR: **+17.70 percentage points**, approximate 95% CI **+17.01 to +18.38 pp**;
- official-test recall minus validation recall: **+0.97 percentage points**, approximate 95% CI **+0.75 to +1.20 pp**.

The large FPR change is therefore not an artifact of rounding uncertainty in the reported point estimates.

## Base-Rate Scenario Analysis

For a detector with true-positive rate `TPR`, false-positive rate `FPR`, and attack prevalence `p`, the positive predictive value is:

`PPV = TPR × p / (TPR × p + FPR × (1 - p))`

Using the HGB official-test rates, TPR = 0.985308 and FPR = 0.262892:

| Hypothetical attack prevalence | Implied PPV |
| --- | ---: |
| 0.1% | 0.37% |
| 1% | 3.65% |
| 5% | 16.48% |
| 10% | 29.40% |
| 25% | 55.54% |
| 50% | 78.94% |

These are mathematical scenarios, not deployment estimates. UNSW-NB15 does not provide a valid estimate of modern production attack prevalence.

The purpose is to demonstrate why false-positive rate is operationally consequential even when attack recall is extremely high.

## Interpretation Boundary

Confidence intervals quantify sampling uncertainty conditional on the observed benchmark data. They do not correct dataset bias, source dependence, hidden duplication, temporal drift, or lack of representativeness.

The external-validity limitations documented in the main paper therefore remain.
