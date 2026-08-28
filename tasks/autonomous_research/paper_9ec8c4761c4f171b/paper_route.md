# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical frontier-orbital calculations to test whether the extended 4-biarylhydrazinylidene pyrazolone dyes have smaller electronic gaps consistent with their long-wavelength UV–Vis absorption. The authors claim that the calculated HOMO–LUMO gaps are consistent with optical gaps estimated from absorption edges and report a correlation of R² = 0.81 for the compound set.

## 2. System and model boundary

The relevant representative is compound 6a, (4Z)-5-(trifluoromethyl)-4-{2-[biphenyl-4-yl]hydrazinylidene}-2,4-dihydro-3H-pyrazol-3-one, a neutral closed-shell molecule. The paper discusses gas phase and chloroform continuum calculations, frontier orbitals, and the Z-ketohydrazone (Z-HK) form. The public task uses the explicitly supplied 6a Cartesian connectivity/geometry and the experimental optical gap, but not hidden calculated values or the authors’ protocol.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish relevant tautomeric form | 7a model forms | ORCA | B3LYP-D3(BJ)/6-311+G*, gas and CHCl3 C-PCM; compare AK, AE, Z-HK, E-HK | Relative Gibbs free energies; Z-HK lowest | ev_doc_5bf9e46ce014_000183_e5e31963cd80; ev_doc_5bf9e46ce014_000200_057f5fbd575b |
| 2 | Optimize ground-state geometries | 5f,g, 6a-g, 7a-g, 8a,b structures/conformers | ORCA (conformers generated with AQME) | B3LYP-D3(BJ)/6-311+G*; gas and CHCl3 C-PCM | optimized geometries | ev_doc_5bf9e46ce014_000113_bbd4befc0733; ev_doc_5bf9e46ce014_000705_64cb03c7390b |
| 3 | Verify stationary points | optimized geometries | ORCA frequency calculation | same level as optimization | no imaginary frequencies/local minima | ev_doc_5bf9e46ce014_000183_e5e31963cd80 |
| 4 | Compute frontier-orbital gaps | optimized geometries | ORCA DFT | HOMO and LUMO energies; Eg = EHOMO − ELUMO | Eg values in gas and CHCl3 | ev_doc_5bf9e46ce014_000185_8ce143a5e0ef; ev_doc_8b002b908a55_000112_25d974dcb020 |
| 5 | Compare with experiment | calculated Eg and optical gaps | regression/plotting | optical gap from absorption-edge wavelength | correlation and deviations | ev_doc_5bf9e46ce014_000200_057f5fbd575b; ev_doc_5bf9e46ce014_000201_b2a56b729df0 |

## 4. Validation and analysis protocol

The authors verify the structural assignment using XRD, IR and NMR and use the QM tautomer comparison to support Z-HK assignment. For the photophysical analysis they compare calculated frontier gaps with optical gaps estimated as 1240/λa.e. and use the aggregate correlation shown in Fig. 10. Their TDDFT analysis assigns the intense low-energy transition primarily to HOMO→LUMO character.

## 5. Private reference results

For 6a, Table S2 reports Eg values of 3.11 eV (gas phase) and 3.04 eV (chloroform C-PCM), with corresponding HOMO/LUMO entries. The optical gap listed for 6a is 2.42 eV. Across the extended 6–8 series the reported calculated gap is 2.93 ± 0.14 eV, lower than monoaryl references 5f and 5g (3.31 and 3.26 eV), and the paper reports R² = 0.81 for calculated versus experimental energies.

## 6. Limitations and interpretation boundaries

Kohn–Sham orbital gaps are not excitation energies; solvent treatment, tautomer/protonation state, conformer choice and numerical settings affect them. The optical-gap comparison is an empirical consistency test, not proof that a single orbital gap exactly equals an absorption energy. The public benchmark therefore scores state identity, stationary-point validation, independently obtained gap values and transparent comparison, while allowing scientifically justified alternative computational methods to be reported.
