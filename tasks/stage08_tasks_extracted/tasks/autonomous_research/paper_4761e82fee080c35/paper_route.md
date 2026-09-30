# Private paper route

## 1. Scientific objective and author claim

The paper tests whether oxidative activation of phosphoryl donor 1 and radical species 3 is thermodynamically feasible under acridinium photoredox conditions. The authors claim that the calculated oxidation potentials support electron transfer and that C–H bond dissociation energies support hydrogen-atom-transfer steps in their phosphorylation mechanism.

## 2. System and model boundary

The computational system is the four SI-labeled optimized structures 1–4 derived from diethyl 1-(diphenoxyphosphoryl)-1,4-dihydropyridine-3,5-dicarboxylate and its oxidized/dehydrogenated partners. The reported observables are redox potentials for 1/2 and 3/4 and C–H BDEs for 1 and 2. Potentials are referenced to SCE in acetonitrile; thermochemical calculations use 298.15 K and 1 atm.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize structures 1–4 | SI Cartesian coordinates | Gaussian16 C.02 DFT | B3LYP/6-31+G(d,p), PCM(MeCN), ε=35.6880 | optimized geometries and energies | ev_doc_7b058133419e_000178_466682643e0a–ev_doc_7b058133419e_000185_f71218ff9597 |
| 2 | Confirm minima and obtain thermal corrections | optimized structures | Gaussian16 frequency | 298.15 K, 1 atm; no imaginary frequencies | frequencies and Gibbs corrections | ev_doc_7b058133419e_000186_c19e06dd3b1f |
| 3 | Obtain oxidation potentials | Gibbs energies for 1–4 | energy differences converted to potentials | SCE/MeCN reference | E(1/2), E(3/4) | ev_doc_7b058133419e_000189_5740853dae02, ev_doc_7b058133419e_000191_304e4e8e76e9 |
| 4 | Obtain C–H BDEs | Gibbs energies of 1, 2 and H atom | thermochemical energy differences | kcal/mol conversion | BDE(1), BDE(2) | ev_doc_7b058133419e_000192_6f56d46ebc61 |

## 4. Validation and analysis protocol

Each optimized structure was checked by frequency analysis for zero imaginary frequencies. The energy table reports thermal Gibbs corrections and electronic potential energies for all four labels. Redox and BDE values were then compared with the mechanistic feasibility interpretation in the paper.

## 5. Private reference results

The SI reports thermal corrections (hartree) 1: 0.367654, 2: 0.367335, 3: 0.352818, 4: 0.359966 and potential energies (hartree) 1: −1813.297159, 2: −1813.076920, 3: −1812.680015, 4: −1812.528678. It reports E(1/2)=+1.33 V and E(3/4)=−0.54 V vs SCE in MeCN, BDE(1)=76.1 kcal/mol and BDE(2)=32.9 kcal/mol.

## 6. Limitations and interpretation boundaries

These are single-level implicit-solvent DFT results, not experimental potentials or a complete kinetic model. The values test thermodynamic plausibility of proposed elementary steps; they do not by themselves establish the full catalytic cycle or product selectivity.
