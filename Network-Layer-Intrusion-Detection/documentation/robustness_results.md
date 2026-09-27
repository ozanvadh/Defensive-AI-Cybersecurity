# Network Robustness Experiment Results

These results implement the protocol frozen in `documentation/robustness_protocol.md` before execution. All experiments use the already trained Histogram Gradient Boosting model and the leakage-resistant validation partition. The official test set remains sealed.

## Condition Results

| Condition | Accuracy | Recall | F1 | FPR | FNR | Balanced accuracy | ROC AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Reference | 95.59% | 97.56% | 96.79% | 8.59% | 2.44% | 94.48% | 99.29% |
| `sttl` median | 82.53% | 81.04% | 86.35% | 14.29% | 18.96% | 83.37% | 90.83% |
| TTL family median | 81.08% | 78.95% | 85.03% | 14.39% | 21.05% | 82.28% | 89.74% |
| Unknown `proto` | 94.94% | 96.65% | 96.29% | 8.70% | 3.35% | 93.97% | 98.92% |
| Unknown `service` | 94.75% | 96.49% | 96.15% | 8.96% | 3.51% | 93.77% | 98.98% |
| Unknown `state` | 93.86% | 96.59% | 95.52% | 11.96% | 3.41% | 92.32% | 98.52% |
| All categorical unknown | 91.82% | 94.72% | 94.09% | 14.36% | 5.28% | 90.18% | 97.47% |

## Primary Robustness Effects

### Source-TTL removal

Replacing only `sttl` with its development-set median reduced balanced accuracy from **94.48% to 83.37%**, an absolute decline of **11.11 percentage points**.

Attack recall fell from **97.56% to 81.04%**, while the false-negative rate increased from **2.44% to 18.96%**. The false-positive rate also increased from **8.59% to 14.29%**.

This confirms substantial sensitivity to the source-TTL signal under the pre-specified ablation. It does not establish that an attacker can realistically force this exact transformation.

### TTL-family removal

Neutralizing `sttl`, `dttl`, and `ct_state_ttl` produced a larger degradation:

- balanced accuracy: **94.48% → 82.28%**
- attack recall: **97.56% → 78.95%**
- false-negative rate: **2.44% → 21.05%**
- ROC AUC: **99.29% → 89.74%**

The model therefore depends materially on TTL/state-derived information as a family.

### Categorical novelty

Novel categorical values caused smaller but measurable degradation individually. Unknown `state` was the strongest single categorical perturbation, increasing FPR to **11.96%**.

When all three categorical predictors were simultaneously unknown, balanced accuracy declined to **90.18%**, FPR rose to **14.36%**, and attack recall fell to **94.72%**.

The model is therefore more robust to categorical novelty than to TTL-family removal under these particular controlled tests.

## Attack-Family Uncertainty

On the unmodified validation set:

| Family | n | Detection | 95% Wilson CI |
| --- | ---: | ---: | ---: |
| Analysis | 421 | 89.55% | 86.25–92.13% |
| Backdoor | 362 | 100.00% | 98.95–100.00% |
| DoS | 2,523 | 99.88% | 99.66–99.96% |
| Exploits | 6,888 | 99.52% | 99.33–99.65% |
| Fuzzers | 3,713 | 86.64% | 85.50–87.70% |
| Generic | 7,654 | 99.97% | 99.91–99.99% |
| Reconnaissance | 2,057 | 99.90% | 99.65–99.97% |
| Shellcode | 228 | 98.68% | 96.19–99.55% |
| Worms | 25 | 100.00% | 86.68–100.00% |

The wide Worms interval illustrates why a raw 100% point estimate should not be interpreted as proof of perfect detection.

## Interpretation

The robustness experiments support a more qualified conclusion than the unmodified 95.59% validation accuracy alone.

The frozen nonlinear detector is highly effective on the internal validation distribution, but its performance is substantially sensitive to removal of TTL-related information. The `sttl`-only condition causes a roughly 11-point balanced-accuracy loss and a large increase in missed attacks. Broader TTL-family removal pushes the false-negative rate above 21%.

At the same time, categorical-novelty experiments produce smaller degradation, demonstrating that the model is not equally fragile to every tested shift.

These results establish **controlled sensitivity**, not real-world adversarial vulnerability. The transformations are diagnostic stress tests and should not be represented as measurements of deployment performance or realistic attacker capabilities.

The official test partition has not been used in these robustness experiments.
