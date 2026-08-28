# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to support an HLCT excited state and a higher-lying-triplet hRISC explanation for efficient triplet harvesting in the deep-blue emitter oPmPCZ. The computational claim is that S1 is far above T1, while T6/T7 are close enough in energy and have larger S1–T SOCs than T1.

## 2. System and model boundary

The system is neutral singlet oPmPCZ, C44H28N4: 2-(5-(3-(9H-carbazol-9-yl)phenyl)pyridin-2-yl)-1-phenyl-1H-phenanthro[9,10-d]imidazole. The authors model an isolated gas-phase molecule. The calculated route concerns S0 geometry, singlet/triplet vertical excited states, NTOs, and SOC matrix elements; it does not model solvent, crystal packing, OLED layers, or kinetics.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state structure | neutral oPmPCZ | Gaussian 16 W DFT | BMK/6-31G(d,p), singlet | optimized S0 geometry | ev_doc_cd513d66b81f_000047_332d5104d278; ev_doc_cd513d66b81f_000049_4386069d449d |
| 2 | Evaluate excited states and NTOs | optimized S0 geometry | Gaussian 16 W TD-DFT | BMK/6-31G(d,p); singlet/triplet states; S0→S1 NTO | S1, T1, T6, T7 energies and S1 NTO character | ev_doc_cd513d66b81f_000064_985d209f39e3; ev_doc_cd513d66b81f_000066_3eac789c5cc9 |
| 3 | Compute spin–orbit coupling | excited-state wavefunctions/densities | ORCA | SOC between S1 and T1/T6/T7; paper does not fully specify all technical settings | SOC matrix elements | ev_doc_cd513d66b81f_000084_4cedb2fc7af1; ev_doc_cd513d66b81f_000088_f3c067470fd7; ev_doc_cd513d66b81f_000095_5e50c79b80ca |
| 4 | Interpret hRISC feasibility | outputs of steps 1–3 | quantitative comparison | compare S1–T1 gap and S1–Tn SOCs | support for/against proposed hRISC picture | ev_doc_cd513d66b81f_000070_f7263fcc5718; ev_doc_cd513d66b81f_000096_d66cd0863fd7 |

## 4. Validation and analysis protocol

Validate molecular identity, charge and multiplicity; report optimization convergence and absence of an imaginary frequency or otherwise explain the chosen stationary point. Verify that the excited-state calculation contains and labels S1, T1, T6 and T7 consistently, and preserve state-indexing evidence. Report the S1–T1 gap and all three SOCs with units and method details. Treat differences caused by geometry, state ordering, SOC convention, software, and unspecified technical settings as interpretation limitations rather than silently changing state labels.

## 5. Private reference results

The paper reports ΔE(S1–T1)=0.93 eV, |SOC(S1,T6)|=0.362 cm−1, |SOC(S1,T7)|=0.215 cm−1, and |SOC(S1,T1)|=0.073 cm−1. It reports S1 oscillator strength 1.2257 and interprets the higher-triplet SOCs and energetic proximity as supporting hRISC. These values are evaluator-only.

## 6. Limitations and interpretation boundaries

The article does not fully specify SOC method/basis details, solvent treatment, number of roots, or convergence thresholds. The calculated gap is not the 77 K spectroscopic gap (0.65 eV). Agreement is therefore evaluated as reproduction of the reported computational observables, not proof of a unique mechanism or exact experimental rate.
