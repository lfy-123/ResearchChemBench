# Private paper route

## 1. Scientific objective and author claim

The authors compare the electronic structure of AQ, an anthraquinone-derived donor–acceptor molecule, with EQ, its cyano-functionalized analogue. Their claim is that strengthening the acceptor increases intramolecular charge transfer and produces small singlet–triplet gaps that favor intersystem crossing and ROS generation.

## 2. System and model boundary

The computational objects are isolated neutral AQ and EQ molecules and isolated neutral AQ and EQ dimers used as simplified aggregate models. The reported observables are HOMO–LUMO gaps, TD-DFT singlet/triplet excitation energies and ΔE_ST, frontier-orbital localization, electrostatic-potential patterns, and dipole moments. This route does not model DPPC, solvent, ultrasound, or bacterial chemistry.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state structures | AQ and EQ monomers; AQ and EQ dimer models | DFT, Gaussian 16 | B3LYP/6-31G*(d,p) (paper text; SI reports B3LYP/6-31G*) | optimized geometries, HOMO/LUMO and dipole/ESP data | ev_doc_bea0d1c9500c_000055_54ffb52ac5c4; ev_doc_f5c8306fc893_000075_f9676402d460 |
| 2 | Obtain low excited states | optimized monomer and dimer geometries | TD-DFT, Gaussian 16 | S1–S3 and T1–T3 | excited-state energies and ΔE_ST | ev_doc_bea0d1c9500c_000058_93c009735c52; ev_doc_f5c8306fc893_000075_f9676402d460 |
| 3 | Interpret structure–property relationship | computed orbital, gap, dipole, ESP and excited-state data | authors' comparison | monomer versus dimer; AQ versus EQ | cyano substitution/aggregation interpretation | ev_doc_bea0d1c9500c_000062_2df3c4ad24ac |

## 4. Validation and analysis protocol

The authors compare AQ and EQ monomers and dimers, inspect spatial separation of donor-localized HOMOs and acceptor-localized LUMOs, and use the first singlet–triplet gap as the ISC-relevant quantity. They relate the computed trends to the experimental ROS hierarchy, but the benchmark isolates the molecular calculation and does not score experimental ROS data.

## 5. Private reference results

The paper reports monomer ΔE_ST values of 0.2482 eV (AQ) and 0.2632 eV (EQ); dimer values are 0.1782 eV (AQ) and approximately 0.0001 eV (EQ). Monomer HOMO–LUMO gaps are reported as 2.12 eV (AQ) and 1.58 eV (EQ), while the dimer values are 1.88 and 1.14 eV. Reported dipoles are 3.02 D (AQ) and 11.09 D (EQ). These values are hidden evaluator references.

## 6. Limitations and interpretation boundaries

The dimer is a simplified aggregate proxy, not a periodic nanoparticle or explicit DPPC environment. Functional/basis choices, conformer selection, and treatment of excited-state geometries can shift absolute values. Conclusions should therefore be stated for the submitted isolated-molecule models and compared quantitatively with appropriate methodological caveats.

## Source-convention qualification

Source-convention review 2026-09-15: main Figure3 B/C places S1 above T1 and labels the downward positive separation; the reported positive Delta E_ST is E(S1)-E(T1). The old task reversed that signed subtraction. Keep all reference magnitudes and numeric tolerances unchanged. SI S5 explicitly says B3LYP/6-31G*, equivalent to 6-31G(d); main text instead prints redundant 6-31G*(d,p). Existing 6-31G(d,p) calculations are a documented alternative-basis branch, not proof of identical SI parameters. SI describes ground/excited-state geometries; the old vertical-only TD branch does not establish that geometry convention. No dimers or biological endpoints are required by the scoped monomer question.
