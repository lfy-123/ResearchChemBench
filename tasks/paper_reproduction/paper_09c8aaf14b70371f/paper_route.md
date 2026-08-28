# Private paper route

## 1. Scientific objective and author claim

The paper uses unsubstituted chalcone 3 as a representative system to explain E–Z geometric isomerization. Its qualitative claim is that rotation about the central C=C bond follows a concerted torsional pathway with a high barrier, so thermal interconversion is kinetically hindered while photochemical activation can enable E-to-Z conversion.

## 2. System and model boundary

The system is neutral, singlet (2E)/(2Z)-1,3-diphenylprop-2-en-1-one (C15H12O), isolated in the gas phase or represented in acetonitrile by an implicit IEF-PCM solvent. The measured coordinate is the C(CO)–C(alpha)–C(beta)–C1 dihedral, where C(CO) is the carbonyl carbon, C(alpha) and C(beta) are the two alkene carbons, and C1 is the ipso carbon of the beta-side phenyl ring.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and optimize E and Z structures | Chalcone structures | Gaussian 16; structures initially built in Chemcraft | B3LYP/6-311+G(2df,2p); neutral singlet; gas phase and IEF-PCM solvent | Optimized E/Z geometries | ev_doc_45530ad2cf56_000070_e7e84bb14e94; ev_doc_45530ad2cf56_000071_dcec5946246d |
| 2 | Confirm minima and obtain thermochemistry | Optimized geometries | Gaussian 16 frequency calculations | Frequencies on all geometries; Gibbs energies at 298 K | Minimum confirmation and Gibbs corrections | ev_doc_45530ad2cf56_000070_e7e84bb14e94 |
| 3 | Trace E–Z torsional PES | Optimized Z structure | Gaussian 16 relaxed PES scan | Systematically vary C(CO)–C(alpha)–C(beta)–C1 from about 0 to about 180 degrees; gas and acetonitrile | Energy profile | ev_doc_45530ad2cf56_000243_44a1c671a059 |
| 4 | Locate and characterize the barrier | PES maximum | Gaussian 16 optimization and frequency calculation | Optimize the maximum structure; first-order saddle verified by one imaginary frequency | TS geometry and barrier | ev_doc_45530ad2cf56_000250_c79465eef962 |
| 5 | Compare environments and structures | E, Z, TS in both environments | Table-based analysis | Relative energies/dihedrals and RMSD of corresponding optimized geometries | Table 8 comparison | ev_doc_45530ad2cf56_000262_22460400feb8 |

## 4. Validation and analysis protocol

The authors interpret the PES maximum as a transition state only after optimization and a frequency calculation identify exactly one imaginary frequency. The TS has an approximately halfway torsional geometry and trans-oriented alpha- and beta-hydrogens, consistent with concerted rotation. Relative energies are reported against the most stable E isomer in each environment. Gas/solvent geometry similarity is assessed using RMSD, and the barrier is interpreted against ambient thermal accessibility.

## 5. Private reference results

Table 8 reports, in acetonitrile, E: 0.00 eV and 179.0 degrees, TS: 1.42 eV and 92.5 degrees, and Z: 0.27 eV and -3.2 degrees; the corresponding gas-phase values are E: 0.00 eV and 179.1 degrees, TS: 1.43 eV and 92.5 degrees, and Z: 0.23 eV and -4.5 degrees. The corresponding RMSDs are 0.039, 0.058, and 0.081 Å for E, TS, and Z. The text also describes the TS dihedral as 93.0 degrees and the gas-phase barrier as 1.43 eV (1.42 eV in acetonitrile), and converts the gas barrier to approximately 137 kJ/mol.

## 6. Limitations and interpretation boundaries

These are electronic-structure/implicit-solvent results, not an experimental rate measurement. A relaxed one-coordinate scan can miss alternative pathways, and the reported solvent model does not include explicit solvent molecules. Numerical comparison must therefore identify the computational model and environment and should not claim universal kinetic behavior or photochemical excited-state dynamics.
