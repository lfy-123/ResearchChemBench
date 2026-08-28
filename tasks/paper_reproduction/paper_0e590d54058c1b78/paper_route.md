# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to assign the emissive excited states of mononuclear copper(I) iodide complex 2, [CuI(L)(PPh3)2]·MeOH, where L is 2-phenyl-5-(4-pyridyl)-1,3,4-oxadiazole. The authors claim that both the lowest singlet and triplet emissive states have mixed metal/halide-to-ligand charge-transfer ((M+X)LCT) character and report isolated-molecule S1→S0 and T1→S0 emission wavelengths of 689 and 605 nm.

## 2. System and model boundary

The computed object is the neutral mononuclear complex [CuI(L)(PPh3)2], with the crystallographic methanol solvent omitted from the isolated-molecule quantum calculation. S0 is a closed-shell singlet; S1 is the lowest singlet excited state; T1 is the lowest triplet. The paper compares isolated-molecule calculations with solid-state measurements and explicitly attributes differences to crystal packing.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state structure | Complex 2 molecular geometry | DFT in ORCA 5.0 | PBE0/def2-TZVP; no dispersion correction | S0 equilibrium geometry | ev_doc_a6b5901cd1d1_000489_879779c72e80; ev_doc_a6b5901cd1d1_000499_b0da16e74b76 |
| 2 | Optimize excited-state structures | S0 geometry | DFT for T1; TDDFT/TDA for S1 in ORCA 5.0 | PBE0/def2-TZVP; TDA; 10 lowest singlets; IRoot=1 | S1 and T1 equilibrium geometries and orbitals | ev_doc_a6b5901cd1d1_000291_bbbb1868238c; ev_doc_a6b5901cd1d1_000499_b0da16e74b76; ev_doc_a6b5901cd1d1_000500_cb31e559c22e |
| 3 | Calculate emission and assign state character | Optimized S1/T1 geometries | TDDFT/TDA in ORCA 5.0; NTO analysis | Vertical S1→S0 and T1→S0 energies; NTOs | 689 nm (S1), 605 nm (T1); (M+X)LCT assignment | ev_doc_a6b5901cd1d1_000332_d905112fa15c; ev_doc_a6b5901cd1d1_000505_b7d81858f4bc |

## 4. Validation and analysis protocol

The authors inspect the optimized excited-state geometries, singly occupied orbitals/NTO pairs, and compare calculated isolated-molecule wavelengths with solid-state emission. For complex 2, the NTOs support mixed Cu(I)/iodide donor to ligand acceptor charge transfer. The calculation is interpreted as a state-character assignment rather than a direct prediction of the solid-state peak.

## 5. Private reference results

The reported isolated-molecule emission wavelengths are 689 nm for 1(M+X)LCT S1→S0 and 605 nm for 3(M+X)LCT T1→S0. Both states are assigned (M+X)LCT character. The experimental room-temperature solid-state emission maximum of complex 2 is 523 nm; the authors explain the difference from isolated-molecule values through crystal-environment effects. Complex 2 is discussed as TADF-active.

## 6. Limitations and interpretation boundaries

The references are isolated-molecule calculations, not solid-state or periodic calculations. Emission wavelengths depend on geometry, electronic-structure method, state tracking, and conformational treatment. NTO assignment is qualitative. Agreement with the hidden values should therefore be interpreted within a stated computational uncertainty, and a defensible failure/limitation report is scientifically valid if the state optimization or state tracking cannot be completed.
