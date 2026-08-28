# Private paper route

## 1. Scientific objective and author claim

The authors used computation to relate the electronic structure of open-ring DTE derivative 3(o) to its rapid, visible-light-induced photocyclization. Their qualitative claim is that extended pi conjugation from terminal N,N-dimethylaniline/alkene units creates strong, asymmetric locally excited frontier-orbital transitions that facilitate directional ring closing.

## 2. System and model boundary

The computed systems are isolated neutral singlet open-ring 3(o) and closed-ring 3(c), each represented by the SI Cartesian structures. The authors report ground-state geometry optimization followed by vertical TD-DFT on optimized structures. The reported level is B3LYP/6-31G* with Gaussian 16; no solvent model is specified in the cited computational description.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish ground-state structures | SI coordinates for 3(o), 3(c) | DFT, Gaussian 16 | B3LYP/6-31G*, neutral singlets | optimized geometries and energies | ev_doc_113465ed1edb_000170_579eea56ab84; ev_doc_66f0b1fa258a_000085_99466f189f4e |
| 2 | Compute vertical electronic transitions | optimized geometries | TD-DFT, Gaussian 16 | same B3LYP/6-31G* level | excitation wavelengths, oscillator strengths, orbital compositions | ev_doc_113465ed1edb_000170_579eea56ab84; ev_doc_66f0b1fa258a_000092_c0892170f2f9 |
| 3 | Interpret orbital localization and photochemical relevance | frontier orbitals and electron-hole maps | GaussView 6, Multiwfn/VMD for maps | qualitative spatial analysis | LE character, asymmetry, reactive-carbon geometry interpretation | ev_doc_113465ed1edb_000176_e9350210adc6; ev_doc_113465ed1edb_000178_58d5b001f6b6 |

## 4. Validation and analysis protocol

The source workflow first optimizes both isomers and then performs TD-DFT on the optimized geometries. The authors inspect frontier orbitals and electron-hole density maps. Their structural interpretation includes an antiparallel photoactive open conformer, a 3.53 Angstrom reactive-carbon separation, open-isomer dipole moment 2.87 D versus closed-isomer 0.29 D, and a twisted open versus nearly planar closed geometry. These are interpretive source claims, not a guarantee that every independent calculation will reproduce them exactly.

## 5. Private reference results

For 3(o), the paper reports S0→S1 near 397 nm with oscillator strength 1.5896 and 94.8% HOMO→LUMO character; S0→S2 at 328 nm with oscillator strength 1.0343 and 82.7% HOMO−1→LUMO+1 character. The authors interpret both intense states, asymmetric frontier-orbital localization and locally excited character as supporting rapid directional photocyclization. The SI reports the 3(o) optimized-structure energy as −2261.45033926 hartree.

## 6. Limitations and interpretation boundaries

The paper does not specify all numerical convergence settings, the number of TD states, or a solvent treatment. Vertical TD-DFT absorption data do not by themselves establish a reaction rate, quantum yield, or complete excited-state reaction mechanism. Orbital labels and percentages can vary with state ordering, orbital conventions and analysis choices; conclusions should therefore preserve reported state identity and uncertainty.
