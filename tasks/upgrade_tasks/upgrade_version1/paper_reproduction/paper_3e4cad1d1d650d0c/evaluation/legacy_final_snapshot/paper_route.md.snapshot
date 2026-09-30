# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to test whether substituents on the 9-aryl group of fluorene anions tune frontier orbital energies. The authors claim that the anionic 9-phenylfluorene scaffold is readily oxidized and that electron-withdrawing para substitution stabilizes the HOMO, supporting tunable super-reducing photocatalysts.

## 2. System and model boundary

The computed systems are isolated 9-substituted fluorene anions in a DMSO continuum, with singlet multiplicity and total charge −1. The representative systems discussed quantitatively are 1a− (9-phenylfluorene anion) and 1e− (the para-CF3 analogue). The reported property is the Kohn–Sham HOMO energy of the optimized anion.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary-point geometries | 1a−–1e− structures and selected catalyst/substrate assemblies | Gaussian 16 DFT | CAM-B3LYP/6-311G*, CPCM(DMSO), no symmetry constraints, charge −1, singlet for isolated anions | Optimized geometries | ev_doc_27b1282aff03_000633_a58241b4eef8; ev_doc_27b1282aff03_000635_5fb1dddbf74e; ev_doc_27b1282aff03_000636_d1ff1a6690dc; ev_doc_27b1282aff03_000638_d9984aa77965; ev_doc_27b1282aff03_000639_419d305b24f1 |
| 2 | Establish true minima | Optimized geometries | Harmonic frequency calculation | Same electronic structure and CPCM(DMSO) boundary | No imaginary frequencies; thermochemistry | ev_doc_27b1282aff03_000639_419d305b24f1; ev_doc_27b1282aff03_000641_11477ba51236 |
| 3 | Extract frontier property and interpret tuning | Frequency-validated anions | Orbital-energy analysis | Compare HOMO energies and spatial distributions | HOMO values and substituent trend | ev_doc_7f0130e00b46_000032_9c866370fad2; ev_doc_7f0130e00b46_000034_3f1a8d7dd0f9 |

## 4. Validation and analysis protocol

The authors validate optimized isolated structures by frequencies and interpret the HOMO as substantially fluorene/benzylic in character, with substituent-dependent electronic communication through the twisted 9-aryl group. Their qualitative structural discussion reports a substantially non-planar phenyl/fluorene arrangement and spatial separation among frontier orbitals. Electrochemical and photophysical measurements are used in the paper to connect the calculated electronic tuning to oxidation and excited-state reduction behavior, but those measurements are outside the computational scoring target.

## 5. Private reference results

The main text reports HOMO energies of −5.03 eV for 1a− and −5.18 eV for 1e− (ev_doc_7f0130e00b46_000032_9c866370fad2; ev_doc_7f0130e00b46_000034_3f1a8d7dd0f9). The paper therefore reports stabilization of the HOMO on moving from the phenyl to the para-CF3 system. The SI reports the optimized-geometry and frequency protocol (ev_doc_27b1282aff03_000639_419d305b24f1; ev_doc_27b1282aff03_000641_11477ba51236).

## 6. Limitations and interpretation boundaries

The benchmark scores a computed orbital energy against a published value, not an observable with a unique experimental absolute scale. Different conformer coverage, integration grids, solvation implementations, and software can shift orbital energies. The evaluator therefore requires reporting the actual method, geometry provenance, frequency evidence, and any failure or sensitivity analysis; a numerical match without a stationary-point validation is not sufficient.
