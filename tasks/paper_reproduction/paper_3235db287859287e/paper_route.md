# Private paper route

## 1. Scientific objective and author claim

The paper studies electrochemical sulfinylation-driven skeletal rearrangement of Baylis–Hillman adducts. Its relevant computational claim is that neutral methyl 3-phenyl-2-((phenylsulfinyl)methyl)acrylate (3aa) has a thermodynamically preferred alkene stereoisomer, supporting experimentally observed Z-selectivity. The authors qualitatively attribute this to reduced steric congestion in the Z arrangement.

## 2. System and model boundary

The public scientific objective compares the E/Z preference of neutral 3aa. However, the SI coordinate blocks labelled 3aa contain 39 atoms, including an additional H and I (an HI-containing model), rather than the isolated 37-atom public molecule. The source uses implicit acetonitrile and 298 K thermal corrections. This model-boundary discrepancy remains unresolved; the isolated-molecule calculation must not be represented as a reproduction of those source coordinate blocks.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize Z and E stationary points | SI 39-atom E/Z models including HI | Gaussian 09 DFT; functional not identified in supplied main/SI | C,H 6-31G; O,S 6-311G**; I aug-cc-pVDZ-PP/ECP; SMD(MeCN) | optimized geometries and energies; exact Hamiltonian remains incomplete | SI printed S98 and S112–S115, physical PDF pages 100 and 114–117 |
| 2 | Characterize stationary points | optimized structures | vibrational analysis | 298 K, 1 atm thermal Gibbs corrections | minima confirmation and G values | ev_doc_735b0692630f_000515_ad0a47173949 |
| 3 | Compare stereoisomers | Z/E Gibbs energies | direct subtraction | ΔΔG = G(E) − G(Z) | favored isomer and relative stability | ev_doc_735b0692630f_000588_c05dd23f0c91 |

## 4. Validation and analysis protocol

Each submitted structure must retain its assigned alkene stereochemistry and be a genuine minimum with zero imaginary frequencies. The same charge, multiplicity, solvent treatment, temperature, and energy convention must be used for both structures. Conformer coverage and method sensitivity are to be reported as limitations.

## 5. Private reference results

The SI reports electronic energies of -1577.569576 Hartree for its Z-labelled block and -1577.567140 Hartree for its E-labelled block. These values accompany the HI-containing coordinate blocks and are not established reference energies for isolated 3aa. The reported 1.5 kcal mol⁻¹ preference and qualitative Z-selectivity are retained as source claims, not as independently validated isolated-molecule results.

## 6. Limitations and interpretation boundaries

This comparison does not establish the full reaction mechanism, electrochemical potential dependence, isolated yield, or kinetic selectivity. The historical M06-2X calculation is a verifier-chosen diagnostic: no named functional was found in the supplied computational-method section. It must not be attributed to the authors or used to restore qualification. Reproduction remains blocked by the functional and model-boundary gaps. No target value or scoring tolerance has been changed by this factual correction (2026-09-25).
