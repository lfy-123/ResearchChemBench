# Private paper route

## 1. Scientific objective and author claim

The authors use quantum-chemical descriptors of a model Cs/PEG-SrO complex to interpret electronic polarization, reactive sites, and stability in gas and aqueous environments. Their qualitative claim is that aqueous solvation increases hardness and thermodynamic stability while decreasing electrophilicity/chemical reactivity; oxygen atoms are the principal negative-potential sites.

## 2. System and model boundary

The modeled object is the 12-atom Cs/PEG-SrO structure supplied in SI Table S2 (O3C2SrOCs plus five H atoms, with the atom identities and Cartesian coordinates listed there). The paper treats gas and aqueous phases; the latter uses a polarizable continuum water model. The reported observables are dipole moment, HOMO/LUMO, gap, ionization potential, electron affinity, electronegativity, electrochemical potential, hardness, softness, electrophilicity, and oxygen Mulliken charges.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build model complex | Cs/PEG-SrO coordinates and structure | Gaussian 09 workflow | SI Table S2 geometry | Initial model | ev_doc_cc114948bfd3_000200_71842d818bc0; ev_doc_405bea18b067_000011_fbde0cb9d1fd |
| 2 | Optimize geometry | Initial model | DFT in Gaussian 09 | B3LYP/SDD | Optimized geometry and wavefunction | ev_doc_cc114948bfd3_000200_71842d818bc0 |
| 3 | Evaluate gas/aqueous electronic properties | Optimized model | Single-point electronic analysis; PCM for water | Gas and PCM aqueous phases | Frontier orbitals, dipole, MESP, Mulliken charges | ev_doc_cc114948bfd3_000200_71842d818bc0 |
| 4 | Derive global descriptors | HOMO/LUMO results | Frontier-orbital-derived descriptor analysis | IP, EA, chi, mu, eta, softness, omega | Table S1 descriptors | ev_doc_405bea18b067_000009_2b303c2b8f20; ev_doc_cc114948bfd3_000201_f32751fddb52 |

## 4. Validation and analysis protocol

The paper compares gas and PCM-water descriptors, interprets MESP qualitatively, and reports negative oxygen Mulliken charges. It explicitly notes that vibrational frequencies were not calculated, so stability is an electronic-descriptor interpretation rather than a verified minimum by frequency analysis. The reported conclusions are checked by descriptor directionality (hardness up; electrophilicity down in water) and oxygen-site charge interpretation.

## 5. Private reference results

SI Table S1 reports, in gas then aqueous order: dipole 3.3390/2.9779 D; HOMO -0.11628/-0.09379 a.u.; LUMO 0.05757/0.01852 a.u.; gap 1.598/2.049 eV; IP 3.164/2.552 eV; EA 1.568/0.504 eV; electronegativity 2.366/1.528 eV; electrochemical potential -2.366/-1.528 eV; hardness 0.798/1.024 eV; softness 1.253/0.977 eV^-1; electrophilicity 3.506/1.141 eV. The paper reports oxygen Mulliken charges of -1.213584 (gas) and -1.361285 (aqueous).

## 6. Limitations and interpretation boundaries

The model is a small cluster representation of a nanocomposite, and Mulliken charges and frontier-orbital descriptors are method-dependent. PCM water is a continuum approximation. No frequency calculation was reported, and descriptor trends do not alone establish a reaction mechanism, binding affinity, or biological efficacy.
