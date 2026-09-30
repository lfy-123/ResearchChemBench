# Private paper route

## 1. Scientific objective and author claim

The authors computed gas-phase electronic properties for the synthesized azetidine–pyridazine series AZ1–AZ10 to support structure–activity discussion. For AZ9, the private reproducibility target is the optimized neutral closed-shell structure, frontier-orbital energies, HOMO–LUMO gap, dipole moment, and algebraically derived global reactivity descriptors. The paper argues qualitatively that frontier-orbital placement, electronic softness/polarizability, and molecular polarity can help rationalize biological interaction propensity; it does not establish a causal free-energy relationship to antimicrobial potency.

## 2. System and model boundary

AZ9 is 1-(2-benzyl-6-chloro-3-oxo-2,3-dihydropyridazin-4-yl)-N-(2,4-dimethylphenyl)azetidine-3-carboxamide, formula C23H23ClN4O2. The authors treated the isolated neutral molecule as a singlet in the gas phase. The reported values are Kohn–Sham orbital and molecular properties of one optimized structure, not solution observables, redox free energies, ensemble averages, or binding affinities.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build the molecular model | AZ9 chemical structure | GaussView 6.0 | Neutral, closed-shell molecule | Initial 3D structure | SI §1.4.1; SI chemical characterization of AZ9, p. 6 |
| 2 | Obtain a stationary molecular geometry | Initial AZ9 structure | Gaussian 16, DFT | B3LYP/6-31G(d), gas phase | Optimized AZ9 coordinates | SI §1.4.1; Table S10, pp. 38–39 |
| 3 | Determine frontier orbitals and molecular polarity | Optimized AZ9 structure | Gaussian 16, DFT | B3LYP/6-31G(d), gas phase | HOMO, LUMO, gap, dipole moment | SI §1.4.1; Table S12, p. 41 |
| 4 | Derive global descriptors | Reported HOMO and LUMO energies | Algebraic post-processing | IP=-EHOMO; EA=-ELUMO; η=(IP-EA)/2; σ=1/(2η); μ=-(IP+EA)/2; χ=(IP+EA)/2. The table reports ω=η/2, although this differs from the conventional μ²/(2η) definition. | IP, EA, hardness, softness, chemical potential, electrophilicity, electronegativity | Table S12 note, p. 41 |

## 4. Validation and analysis protocol

The SI identifies the coordinates as an optimized geometry but does not report a vibrational-frequency calculation or imaginary-frequency count. Accordingly, a reproduction should independently verify stationarity/minimum character rather than assume it. Descriptor arithmetic should be checked directly from the submitted HOMO/LUMO values. Because the SI's stated electrophilicity formula is nonstandard and its tabulated values equal η/2, both the paper-defined value and the conventional μ²/(2η) value should be distinguished when interpreting results.

## 5. Private reference results

Table S12 reports for AZ9: EHOMO -5.5758 eV; ELUMO -1.1556 eV; gap 4.4202 eV; IP 5.5758 eV; EA 1.1556 eV; hardness 2.2101 eV; softness 0.2262 eV^-1; chemical potential -2.2101 eV as printed; electrophilicity 1.1050 eV as printed; electronegativity 3.3657 eV; dipole moment 5.8470 D. The printed chemical-potential and electrophilicity columns follow the formulas stated in the table note, not conventional conceptual-DFT definitions.

## 6. Limitations and interpretation boundaries

The paper supplies no conformer-search protocol, frequency results, solvent model, thermal corrections, or method-sensitivity analysis. Kohn–Sham eigenvalues are method-dependent approximations and should not be presented as experimental IP/EA. The electronic descriptors alone do not demonstrate antimicrobial mechanism, protein binding, aqueous solubility, or membrane permeability. Any discrepancy in the two nonstandard printed descriptors must be discussed rather than silently relabeled.
