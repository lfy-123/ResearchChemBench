# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum chemistry to explain the optical properties of benzoyl-PXX chromophore 1 and Lewis-acid complexes. For compound 1, the lowest-energy absorption band is assigned to S1 and is overwhelmingly HOMO-to-LUMO; Lewis-acid coordination is proposed to strengthen the acceptor character and red-shift the transition.

## 2. System and model boundary

Compound 1 is neutral C43H28O3, singlet. The calculations model an isolated molecule in implicit dichloromethane; the reported excitation is an electronic vertical singlet excitation from the optimized ground-state geometry. The public task uses the SI optimized XYZ geometry for 1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build/pre-optimize structures | Molecular structures | GaussView/Chemcraft, then CREST 3.0.2/GFN-FF | Non-covalent interaction mode; 7 kcal/mol threshold | Candidate conformers | ev_doc_d98bbe83bb8d_001856_490c62cc6a36 |
| 2 | Optimize geometry | Selected conformer of 1 | Gaussian16 | B3LYP/6-31G(d), PCM(CH2Cl2); SI says D3BJ was used in the conformer/full optimization description | Optimized ground-state geometry | ev_doc_d98bbe83bb8d_000118_ad95fccfeac8; ev_doc_d98bbe83bb8d_000120_d25b019ad274 |
| 3 | Compute the spectrum corresponding to the scored Table S1 endpoint | Supplied optimized geometry of compound 1 | Gaussian16 TD-DFT | First 20 singlet states; B3LYP-D3BJ/6-311G(d), PCM(CH2Cl2), as specified by the dedicated Section 6 Methods | Excitation energies, oscillator strengths | SI S168 Table S1; SI S170 Methods; main Figure 7 |
| 4 | Analyze transitions | TD-DFT output | Multiwfn 3.7 | Orbital contribution analysis | S1 orbital composition | ev_doc_d98bbe83bb8d_001921_fd2d6d3e9bb1 |

## 4. Validation and analysis protocol

Source reconciliation (2026-09-18): the general SI S5–S6 description mentions 6-31G(d) and 64 singlet states, whereas the dedicated Section 6, Table S1 caption (S168), and Methods (S170) use 6-311G(d) and 20 states for the spectrum scored here. S170 explicitly includes D3BJ and distinguishes geometry optimization at 6-31G(d) from the excited-state calculation at 6-311G(d). Use the specific endpoint description for strict author-route verification; do not label an older 6-31G(d)/64-state output as a reproduction of the Table S1 route merely because S1 happens to fall in a scoring tolerance. The fixed public geometry, task scope and evaluator values are unchanged.

The authors identify S1 as the lowest-energy absorption band and report the dominant orbital pair and percentage. SI Table S1 gives the excitation-energy spectrum and Table S2 gives orbital contributions. The comparison is made on the S1 energy and HOMO-to-LUMO contribution, with the qualitative interpretation that a dominant HOMO-to-LUMO transition supports the assignment.

## 5. Private reference results

For compound 1, S1 is 2.204 eV (reported in the main paper as 2.20 eV), with transition 155→156 contributing 98.8%. The paper states that the lowest-energy absorption band originates from S1. These values are evaluator-only.

## 6. Limitations and interpretation boundaries

The adduct 1·BAr3F is not released as a task object because the supplied SI does not contain a public Cartesian geometry for it; guessing its connectivity or orientation would violate input closure. The task therefore tests only the closed compound-1 sub-objective. Method and conformer choices can shift absolute excitation energies; evaluation focuses on transparent, independently justified calculations and the source-backed target.
