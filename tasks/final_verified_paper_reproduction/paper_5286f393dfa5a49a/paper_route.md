# Private paper route

## 1. Scientific objective and author claim

The paper tests whether chiral side chains select the helical conformation of bay-fused tetrachlorinated diperylene diimide (di-ClPDI-Ph). The authors claim that the (RRRR)-MM conformer is thermodynamically preferred to (SSSS)-MM by 6.56 kJ mol−1.

## 2. System and model boundary

The isolated neutral singlet molecule is tetrachlorinated di-ClPDI-Ph (C80H42Cl4N4O8 as assigned in the SI coordinate tables). Three starting geometries are considered: crystal, (RRRR)-MM and (SSSS)-MM. Solvent is dichloromethane represented by SMD.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize three conformations | SI Tables S3–S5 geometries | ORCA 6.0 | B3LYP-D3/def2-TZVP(-f), SMD(DCM), RI/COSX | optimized structures | ev_doc_05b0b4a3e168_000110_235b920cd59e; ev_doc_05b0b4a3e168_000113_e52ee3f51b84; ev_doc_05b0b4a3e168_000114_e393c5b3e5c7 |
| 2 | Refine energies | optimized structures | ORCA 6.0 | ωB97M-V/def2-TZVP, SMD(DCM), RI/COSX | electronic energies | ev_doc_05b0b4a3e168_000116_7efd2bdd4254; ev_doc_05b0b4a3e168_000117_c42cfdd9884c |
| 3 | Compare conformers | three energies | energy subtraction | relative to a stated reference | relative energies | ev_doc_05b0b4a3e168_000192_ea99a81e069f; ev_doc_05b0b4a3e168_000194_52d7638d0aa8 |

## 4. Validation and analysis protocol

The authors compare the three optimized isolated-state conformations and use the relative energy to support stereochemical induction. Their SI states that the geometries are optimized and the main paper reports the conformational energy difference. The paper does not provide a complete independent conformer-search protocol; the approved D3 benchmark adaptation instead compares the supplied fixed geometries with wB97M-V/def2-TZVP/SMD(DCM) single points. Report SCF convergence and fixed-input provenance; optimization/frequency work is an optional separate sensitivity branch, not a prerequisite or a claim of minimum validation.

## 5. Private reference results

The (RRRR)-MM conformer is 6.56 kJ mol−1 lower in energy than (SSSS)-MM. The result is used to support preferential induction of P-helicity by (S)-1-phenylethyl and M-helicity by the R analogue. Source: ev_doc_05b0b4a3e168_000192_ea99a81e069f; ev_doc_7cb3000b394e_000061_48fe606dc56f.

## 6. Limitations and interpretation boundaries

The comparison is a three-geometry calculation, not proof of a global minimum over all conformers. Relative electronic energies depend on geometry, solvation, dispersion, basis and treatment of thermal effects. The crystal geometry is a separate labeled starting structure and should not be treated as a periodic-crystal lattice energy.
