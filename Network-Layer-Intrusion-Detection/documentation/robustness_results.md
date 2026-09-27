# Network Robustness Experiment Results

These results implement the protocol frozen in `documentation/robustness_protocol.md` before execution. All experiments use the frozen Histogram Gradient Boosting model and the leakage-resistant validation partition. The official test set was not used during robustness analysis.

## Condition Results

| Condition | Accuracy | Recall | F1 | FPR | FNR | Balanced accuracy | ROC AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Reference | 95.59% | 97.56% | 96.79% | 8.59% | 2.44% | 94.48% | 99.29% |
| `sttl` median | 79.62% | 97.67% | 86.71% | 58.84% | 2.33% | 69.41% | 94.05% |
| TTL family median | 71.55% | 97.65% | 82.37% | 84.07% | 2.35% | 56.79% | 84.68% |
| Unknown `proto` | 92.44% | 99.76% | 94.73% | 23.16% | 0.24% | 88.30% | 97.79% |
| Unknown `service` | 95.53% | 97.50% | 96.74% | 8.66% | 2.50% | 94.42% | 99.26% |
| Unknown `state` | 95.05% | 97.37% | 96.40% | 9.88% | 2.63% | 93.74% | 99.22% |
| All categorical unknown | 92.42% | 99.76% | 94.71% | 23.24% | 0.24% | 88.26% | 97.79% |

## Primary Robustness Effects

### Source-TTL information removal

Replacing only `sttl` with its development-set median reduced balanced accuracy from **94.48% to 69.41%**, a **25.07 percentage-point decline**.

Attack recall remained essentially unchanged at **97.67%**, but the false-positive rate increased from **8.59% to 58.84%**. The degradation therefore came primarily from benign traffic being classified as malicious, not from attacks becoming invisible.

This demonstrates substantial model dependence on the source-TTL signal under the pre-specified ablation. It does not establish that a real attacker can force this exact transformation.

### TTL-family information removal

Neutralizing `sttl`, `dttl`, and `ct_state_ttl` produced a larger degradation:

- balanced accuracy: **94.48% → 56.79%**
- false-positive rate: **8.59% → 84.07%**
- attack recall: **97.56% → 97.65%**
- ROC AUC: **99.29% → 84.68%**

The frozen model therefore relies heavily on TTL/state-derived information for distinguishing benign traffic from attacks.

### Categorical novelty

Categorical novelty was heterogeneous. Replacing `service` or `state` alone with an unseen category caused only modest degradation. Replacing `proto` with an unseen value had a larger effect, increasing FPR to **23.16%**.

When all three categorical predictors were simultaneously unknown, balanced accuracy fell to **88.26%** and FPR rose to **23.24%**, while attack recall increased to **99.76%**. Again, the main failure mode was over-classification of traffic as malicious.

## Attack-Family Uncertainty

On the unmodified validation set:

| Family | n | Detection | 95% Wilson CI |
| --- | ---: | ---: | ---: |
| Analysis | 421 | 89.55% | 86.26–92.12% |
| Backdoor | 362 | 100.00% | 98.95–100.00% |
| DoS | 2,523 | 99.88% | 99.65–99.96% |
| Exploits | 6,888 | 99.52% | 99.33–99.66% |
| Fuzzers | 3,713 | 86.64% | 85.51–87.70% |
| Generic | 7,654 | 99.97% | 99.90–99.99% |
| Reconnaissance | 2,057 | 99.90% | 99.65–99.97% |
| Shellcode | 228 | 98.68% | 96.20–99.55% |
| Worms | 25 | 100.00% | 86.68–100.00% |

The wide Worms interval illustrates why a raw 100% point estimate should not be interpreted as proof of perfect detection.

## Interpretation

The robustness experiments support a more qualified conclusion than the unmodified 95.59% validation accuracy alone.

The frozen nonlinear detector is highly effective on the internal validation distribution, but it is strongly dependent on TTL-related information for benign-versus-malicious discrimination. Under the pre-specified `sttl` ablation, attack recall stays high while benign false alarms rise dramatically. Broader TTL-family removal makes that effect even stronger.

These results establish **controlled sensitivity**, not real-world adversarial vulnerability. The transformations are diagnostic stress tests and should not be represented as measurements of deployment performance or realistic attacker capabilities.

The official test partition was not used to define or tune these robustness conditions.
