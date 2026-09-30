# Private paper route

## 1. Scientific objective and author claim

The paper studies how spacer length and imine/amine donor state alter the coordination geometry and catalytic behavior of Cu(I) P,N complexes. For the non-crystallizing hexyl-bridged iminophosphine complex 7a, the authors use DFT to estimate the ground-state geometry and argue that the flexible C6H12 bridge relaxes, but does not eliminate, steric congestion at the N donors. The related crystallographic complexes 5a and 6a provide context, but are not the computational target.

## 2. System and model boundary

The target is the cation of [Cu(L7)]BF4, where L7 is N,N′-(hexane-1,6-diyl)bis((2-(diphenylphosphanyl)phenyl)methanimine), also called Hex-bisImP. The chemically modeled species is a four-coordinate Cu(I) cation bound by both P,N chelating arms; BF4− is a counterion and is not part of the coordination sphere. The SI reports a gas-phase ground-state calculation and selected Cu–P/Cu–N distances and P/N–Cu angles.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define the simulated complex | 7a, [Cu(L7)]BF4, L7 = Hex-bisImP | Molecular model construction | Cationic Cu(I), both P,N arms coordinated | Initial 3-D model | ev_doc_8fdf7eb8b59f_000048_ebac320a303b; ev_doc_8fdf7eb8b59f_000881_861d80134c8b |
| 2 | Optimize the geometry | Initial model of 7a | Gaussian 16 | CAM-B3LYP/def2-TZVP, gas phase, opt | Converged optimized geometry | ev_doc_1f425fec2790_000412_44035a4980d6; ev_doc_1f425fec2790_000414_ca1608eee05a |
| 3 | Verify a minimum | Optimized geometry | Gaussian 16 frequency calculation | freq on the optimized structure; no imaginary modes | Minimum verification | ev_doc_1f425fec2790_000414_ca1608eee05a |
| 4 | Extract structural observables | Validated optimized structure | Geometry analysis | Cu–P, Cu–N distances and six unique P/N–Cu angles | Numerical comparison with reported simulation | ev_doc_1f425fec2790_000381_9cf45caf9e49 |

## 4. Validation and analysis protocol

The authors optimized all discussed systems in the gas phase and then performed frequency analyses to establish true minima. They subsequently analyzed HOMO/LUMO properties, but the reported structural claim for 7a rests on the optimized geometry and the selected bond lengths and angles. The paper compares the simulated 7a P–Cu–P framework and N–Cu–N angle with experimental structures of related bridged complexes, interpreting the larger hexyl spacer as permitting partial relaxation.

## 5. Private reference results

For 7a, the SI Fig. S101 reports Cu(1)–P(1) 2.2959 Å, Cu(1)–P(2) 2.2889 Å, Cu(1)–N(1) 2.2821 Å, Cu(1)–N(2) 2.0537 Å; P(1)–Cu(1)–P(2) 123.17°, P(1)–Cu(1)–N(1) 80.32°, P(1)–Cu(1)–N(2) 134.15°, P(2)–Cu(1)–N(1) 119.04°, P(2)–Cu(1)–N(2) 97.35°, and N(1)–Cu(1)–N(2) 99.27°. The SI states that no imaginary frequencies were detected for the optimized structures. These values are private evaluator references.

## 6. Limitations and interpretation boundaries

The paper does not provide the authors' starting Cartesian coordinates or an electronic-structure input file. Different reasonable starting conformers and computational choices can therefore produce legitimate method-dependent deviations. The task scores the reported selected geometry and minimum verification, not an assertion that the calculation proves a unique mechanism or catalytic rate. BF4− should not be included as a bonded ligand, and the reported atom labels are defined by the public donor-label map rather than by an assumed input-file ordering.
