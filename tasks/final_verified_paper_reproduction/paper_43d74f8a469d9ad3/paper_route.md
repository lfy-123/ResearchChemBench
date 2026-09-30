# Private paper route

## 1. Scientific objective and author claim

The paper uses a relaxed-independent torsion scan to test whether steric shielding by the two meta-methyl groups of organoboron ester 1 makes rotation of the boron–phenyl bond less favorable than in para-substituted analogue 3, thereby supporting the reported photobleaching-resistance trend.

## 2. System and model boundary

The computational object is an isolated neutral gas-phase molecule of ester 1, with the boron atom in its tetrahedral N,O,O chelate and the 3,5-dimethylphenyl substituent attached through B–C. The scanned coordinate is the dihedral defining rotation about the B–C bond. The reported profile is a rigid-rotor, single-point electronic-energy profile relative to its minimum; it is not a free-energy, solvated, vibrationally averaged, or excited-state result.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Prepare equilibrium structures | Crystallographic-derived molecular models | Gaussian 16 | PBE0/def2-SVP for the torsion study | optimized structures of 1 and 3 | ev_doc_6d91df1be8bd_000402_5c937ac96719 |
| 2 | Check optimized structure | optimized geometry | Gaussian 16 frequency analysis (general paper protocol) | minimum characterization | stationary-point validation | ev_doc_6d91df1be8bd_000403_5219be36b1a9 |
| 3 | Generate torsion scan geometries | optimized structure | coordinate manipulation | rotate B–phenyl bond in 15° increments through 360° | 24 rigid-rotor geometries per compound | ev_doc_6d91df1be8bd_000403_5219be36b1a9; ev_doc_6d91df1be8bd_000404_982cca5b0596 |
| 4 | Evaluate scan energies | 24 geometries | Gaussian 16 | PBE0/def2-SVP single points | electronic energies E(theta) | ev_doc_6d91df1be8bd_000404_982cca5b0596 |
| 5 | Reduce and interpret profile | scan energies | numerical profile analysis | E(theta) referenced to the lowest point; integrated total rotation energy | profile and barrier metrics | ev_doc_6d91df1be8bd_000404_982cca5b0596; ev_doc_6d91df1be8bd_000405_0debae751323 |

## 4. Validation and analysis protocol

The optimized geometry is required to be a genuine minimum. Scan points are checked for complete angular coverage, consistent atom identity for the B–C torsion, continuity and 360° periodicity. Relative energies are formed from the common minimum. Main paper p11 reports that 1 has 1.81 kJ mol−1 greater integrated full-rotation energy and 2.61 kJ mol−1 greater energy at the most unstable point than 3. It cites Fig. S57 for the torsion scan, not Figs. S58–S59 (discussed on p12 for ring geometry). The SI is not locally available for independent curve inspection. These comparative metrics are outside the current compound-1-only task and are not numeric acceptance targets.

## 5. Private reference results

The current evaluator uses semantic checks for the 24-point profile of ester 1, the rigid ground-state model, convergence, mapping, coverage and bounded interpretation. It contains no independently inspected 24-point numerical reference table. Main p11 supports the qualitative torsional-resistance rationale, but a scan of compound 1 alone cannot isolate a methyl-substituent effect or reproduce the compound-1-versus-3 comparative metrics (1.81 and 2.61 kJ mol−1). Report that limitation rather than treating those comparative values as single-compound targets.

## 6. Limitations and interpretation boundaries

The scan is a gas-phase electronic-energy model and does not establish solution photobleaching kinetics, a decay rate, or an excited-state surface. The unavailable SI curve has not been digitized or numerically reproduced. The source text contains a general M06-2X/6-311++G(d,p) TD-DFT protocol for other calculations; the torsion subsection explicitly uses PBE0/def2-SVP and that distinction is retained here. The figure-reference correction changes provenance only, not the public objective, scientific scoring criteria or tolerance.
