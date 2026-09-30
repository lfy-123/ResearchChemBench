# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to explain why the meta-amino 1,8-naphthalimide (m-NH2) has stronger intramolecular charge-transfer (ICT) character than the para-amino analogue (p-NH2), and why acetylation changes the fluorescence response. The quantitative descriptor emphasized here is the hole–electron centroid distance (D-index) for the lowest singlet excitation. The authors claim that meta substitution gives a larger D-index and therefore stronger CT character.

## 2. System and model boundary

The target is neutral, singlet m-NH2: 2-butyl-6-amino-1H-benzo[de]isoquinoline-1,3(2H)-dione (also described in the SI as the n-butyl imide of 3-amino-1,8-naphthalic anhydride; formula C16H16N2O2). The computational solvent is water represented with the SMD continuum model. The paper also discusses simplified dye/two-water clusters, but the core route described for the D-index uses the dye model and SMD water. The D-index is the distance between hole and electron centroids for the S0→S1 excitation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain a ground-state geometry | m-NH2 structure | Gaussian 16 DFT optimization | B3LYP-GD3BJ/6-311+G(d,p) | optimized S0 geometry | ev_doc_e2b0baa00454_000002_5daf4e16247f; ev_doc_e2b0baa00454_000044_5daf4e16247f |
| 2 | Calculate low-lying absorption states | optimized S0 geometry | Gaussian 16 linear-response TDDFT | optimally tuned LC-BLYP*/6-311G+(d,p), SMD water; first two singlet roots | S0→S1/S2 energies and oscillator strengths | ev_doc_e2b0baa00454_000002_5daf4e16247f; ev_doc_e2b0baa00454_000044_5daf4e16247f |
| 3 | Determine the range-separation parameter | m-NH2 electronic structure | authors' GAP-TUNING procedure | molecule-specific optimal omega; value tabulated privately in SI Table S3 | tuned LC-BLYP* parameter | ev_doc_e2b0baa00454_000007_62b462179dc2; ev_doc_e2b0baa00454_000049_62b462179dc2 |
| 4 | Analyze charge transfer | S0→S1 excitation wavefunction | Multiwfn hole–electron distribution analysis | D-index = distance between hole and electron centroids | D-index in Angstrom | ev_doc_e2b0baa00454_000002_5daf4e16247f; ev_doc_e2b0baa00454_000044_5daf4e16247f |

The authors additionally optimized S1 geometries and calculated emission energies with the tuned LC-BLYP*/6-311G+(d,p) model in SMD water, but those outputs are outside the scored endpoint.

## 4. Validation and analysis protocol

The implemented workflow is sequential: verify a converged S0 optimization; preferably verify that the optimized structure has no imaginary frequency; verify a completed TDDFT calculation with the requested low-lying singlet states; then perform hole–electron analysis on the S0→S1 state and report one positive centroid distance. The paper compares m-NH2 and p-NH2 and interprets a larger D-index as stronger CT. It cautions that calculated photophysical quantities are interpreted comparatively rather than as exact experimental quantum yields.

## 5. Private reference results

The main paper reports D = 2.25 Angstrom for m-NH2 and D = 1.33 Angstrom for p-NH2, concluding that meta substitution has stronger CT character. The SI states that the molecule-specific optimal range-separation parameters are listed in Table S3; those values are private to evaluation and are not part of the public task input. The paper also reports a meta acetylation D change of 0.31 Angstrom, but this is not a required endpoint here.

## 6. Limitations and interpretation boundaries

A D-index depends on geometry, electronic-structure method, tuning procedure, solvent treatment, state identification and numerical integration details. Independent calculations may therefore differ from the published value. The evaluator should assess whether the submitted state is the lowest singlet excitation of the specified neutral molecule, whether the workflow is actually completed and validated, and whether the reported value supports the paper's qualitative comparison. The D-index alone does not prove a full reaction mechanism or guarantee an experimental fluorescence yield.
