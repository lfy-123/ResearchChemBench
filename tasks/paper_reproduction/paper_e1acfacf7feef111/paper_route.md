# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to validate a local structural model for the bromobismuthate hybrid by comparing an optimized molecular cluster with single-crystal geometry and IR/Raman frequencies. The authors claim that a local isolated cluster reproduces the local Bi(III) coordination and the characteristic Bi–Br vibrational dynamics sufficiently well for interpretation.

## 2. System and model boundary

The experimental material is monoprotonated (C10H13N4)+[BiBr4]−·2H2O in monoclinic P21/n (Z′=1, Z=4). The authors’ model contains one [BiBr4]− anion, one organic cation and two water molecules. The corrected v1 benchmark uses this full 38-atom neutral-singlet formula-unit cluster. The original five-atom fragment is retained only as v0 diagnostic evidence because it cannot provide the requested six-mode comparison.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build local cluster | Formula-unit crystal structure | Gaussian 09W | one [BiBr4]−, organic cation, two waters; all atoms relaxed | initial cluster | ev_doc_554182bc3ad4_000161_d5130ddba9e7, ev_doc_554182bc3ad4_000186_13a7ef724cf0 |
| 2 | Find minimum | initial cluster | DFT geometry optimization | B3LYP; GENECP; LANL2DZ ECP for Bi/Br; 6-311++G* for H/C/N/O | optimized minimum | ev_doc_554182bc3ad4_000149_33b197345330, ev_doc_554182bc3ad4_000150_fb432fd1b88b |
| 3 | Validate dynamics | optimized minimum | harmonic frequency calculation | IR/Raman frequencies; mode visualization/assignment | calculated wavenumbers | ev_doc_554182bc3ad4_000164_481ff6309543 |
| 4 | Compare with experiment | optimized structure and frequencies | bond and spectrum comparison | local geometry and Table 4.S assignments | agreement assessment | ev_doc_554182bc3ad4_000203_5d35c214f73c, ev_doc_554182bc3ad4_000266_403078025703, ev_doc_554182bc3ad4_000291_6d5c29a07c7e |

## 4. Validation and analysis protocol

The paper compares optimized bond distances/angles with the crystal tables and calculated vibrational wavenumbers with IR/Raman observations. It interprets modest gas-phase/solid-state geometry differences as expected and treats close low-frequency Bi–Br agreement as support for the local model.

## 5. Private reference results

The SI reports Bi–Br distances 2.6812, 3.1803, 2.8596, 2.7151, 3.0211 and 2.8708 Å and Bi/Br angles including 175.782, 92.848, 90.024, 87.208, 94.392, 83.496, 89.542, 172.061, 91.580, 92.175, 91.672, 177.061, 90.650, 89.144, 87.562, 96.503 and 92.437°. The six reported low-frequency Raman observations are 183, 166, 131, 118, 90 and 75 cm−1, paired in the SI with calculated values 186, 164, 131, 113, 84 and 68 cm−1.

## 6. Limitations and interpretation boundaries

The corrected benchmark includes the organic cation and two waters required by the author model, but it remains a finite cluster rather than a periodic solid. It does not score electronic properties, periodic-chain energetics, or a unique mechanism; conclusions remain limited to local Bi–Br geometry and low-frequency vibrational behavior.
