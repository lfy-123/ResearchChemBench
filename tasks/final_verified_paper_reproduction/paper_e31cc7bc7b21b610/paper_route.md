# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to compare the gas-phase electronic energies of the cis-α and cis-β isomers of the monochloride complex cis-(Egan)IrCl (with tert-butyl groups replaced by hydrogen in the computational egan model). This comparison supports the experimental discussion of thermal isomerization and relative isomer stability.

## 2. System and model boundary

The calculated species are neutral, closed-shell singlet cis-α-(egan)IrCl and cis-β-(egan)IrCl. The computational egan ligand is the Egan ligand with tert-butyl groups replaced by hydrogen. Calculations are gas phase; solvent, counterions and crystal packing are excluded.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize cis-α structure | SI Cartesian starting/optimized geometry for cis-α-(egan)IrCl | Gaussian 16 DFT geometry optimization | B3LYP; SDD on Ir; 6-31G* on all other atoms; neutral singlet; gas phase | optimized geometry and electronic energy | ev_doc_5ccb7b51871a_000302_1fa04590812b; ev_doc_5ccb7b51871a_000304_fd5dc7553e0e; ev_doc_5ccb7b51871a_000306_80edac933a9e; ev_doc_84440e2ee670_000203_0a6088017185 |
| 2 | Optimize cis-β structure | SI Cartesian starting/optimized geometry for cis-β-(egan)IrCl | Gaussian 16 DFT geometry optimization | same model and state | optimized geometry and electronic energy | ev_doc_5ccb7b51871a_000302_1fa04590812b; ev_doc_5ccb7b51871a_000304_fd5dc7553e0e; ev_doc_5ccb7b51871a_000306_80edac933a9e; ev_doc_84440e2ee670_000207_663eef882274 |
| 3 | Validate stationary points | optimized geometries | harmonic vibrational-frequency calculations in Gaussian 16 | same model; frequencies scaled 0.9614 for reported frequencies | zero-imaginary-frequency minimum assignment for each isomer | ev_doc_5ccb7b51871a_000304_fd5dc7553e0e; ev_doc_5ccb7b51871a_000309_4ca3ad9b3e7d; ev_doc_5ccb7b51871a_000313_1adc4275bbab |
| 4 | Compare isomer energies | two validated optimized structures | subtraction of electronic energies | ΔE = E(cis-β) − E(cis-α), converted to kcal mol−1 | relative electronic energy | ev_doc_84440e2ee670_000203_0a6088017185; ev_doc_84440e2ee670_000207_663eef882274 |

## 4. Validation and analysis protocol

Each optimized structure was checked by a vibrational-frequency calculation. The paper states that cis-α and cis-β are minima; the reported frequencies use a 0.9614 scale factor. The energy comparison is the electronic-energy difference between the two optimized minima, not a free-energy or solution-phase quantity.

## 5. Private reference results

The SI reports electronic energies of −2204.52499146 a.u. for cis-α-(egan)IrCl and −2204.52269915 a.u. for cis-β-(egan)IrCl. Thus Eβ−Eα is positive and approximately 1.44 kcal mol−1 (using 627.5095 kcal mol−1 per hartree). Both structures are reported as minima.

## 6. Limitations and interpretation boundaries

These are gas-phase single-method electronic energies for a hydrogen-substituted computational ligand model. They do not establish solution equilibria, kinetics, barriers, or complete conformational/global-minimum sampling. Numerical agreement should be interpreted within normal DFT and optimization sensitivity; the evaluator scores the stated endpoint and validation evidence, not reproduction of an undisclosed software-specific trajectory.
