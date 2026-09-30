# Private paper route

## 1. Scientific objective and author claim

The paper tests whether the Polytope Formalism connectivity graph for H-tautomerism in the free-base subporphyrin monoanion is isomorphic to the topology of the real-space potential-energy surface (PES). The authors claim that the three representative stationary points—LM, TS and second-order saddle—are connected by first- and second-order motions whose bond-stretching normal modes point toward graph neighbours.

## 2. System and model boundary

The system is the charge −1, singlet free-base subporphyrin monoanion (triphyrin[1.1.1]ate), treated as a single nondissociating molecule. The three N sites are the connectivity sites and the inner H atom is the mobile bonder; all other atoms are spectators. The SI19 coordinate records for species 6a, 7a and 8a each contain 28 atoms with explicit charge and multiplicity. The original v0 public mapping was incorrect (candidate B was 8a and candidate C was the unrelated 29-atom species 9); v1 corrects the mapping to A=6a, B=7a and C=8a.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimise and characterise the LM representative | SI19 LM coordinate record (species 6a) | Gaussian16 | B3LYP/6-31+G**, GD3BJ, chloroform SCRF, charge −1, singlet, tight optimisation plus frequency calculation | Optimised geometry, SCF energy, frequencies and thermal free energy | ev_doc_1f70c563ed4e_000535_99274f8c3ebe; ev_doc_1f70c563ed4e_000536_9e1004ba53cb; ev_doc_1f70c563ed4e_000543_efbfe5f168cc; ev_doc_1f70c563ed4e_000544_e643501abc6e; ev_doc_1f70c563ed4e_000545_c3f049a2631b |
| 2 | Optimise and characterise the first-order saddle representative | SI19 TS coordinate record (species 7a) | Gaussian16 | B3LYP/6-31+G**, GD3BJ, chloroform SCRF, charge −1, singlet, TS optimisation and frequency calculation | Optimised geometry, SCF energy, frequencies and thermal free energy | ev_doc_1f70c563ed4e_000540_10a57850de00; ev_doc_1f70c563ed4e_000543_efbfe5f168cc; ev_doc_1f70c563ed4e_000544_e643501abc6e; ev_doc_1f70c563ed4e_000545_c3f049a2631b |
| 3 | Optimise and characterise the second-order saddle representative | SI19 second-order-saddle coordinate record (species 8a) | Gaussian16 | B3LYP/6-31+G**, GD3BJ, chloroform SCRF, second-order saddle optimisation and frequency calculation | Optimised geometry, SCF energy, frequencies and thermal free energy | ev_doc_1f70c563ed4e_000540_10a57850de00; ev_doc_1f70c563ed4e_000543_efbfe5f168cc; ev_doc_1f70c563ed4e_000544_e643501abc6e; ev_doc_1f70c563ed4e_000545_c3f049a2631b |
| 4 | Compare stationary-point character with the connectivity graph | Outputs of steps 1–3 and graph relations | Hessian and normal-mode analysis | Count negative Hessian eigenvalues; inspect whether imaginary modes are bond-stretching motions toward graph neighbours | PES-character assignment and graph/PES validation | ev_doc_d12dcce011e7_000220_ee3faf3a1e04; ev_doc_d12dcce011e7_000221_4695196baa93; ev_doc_d12dcce011e7_000363_d7507393d6c6 |

## 4. Validation and analysis protocol

The paper assigns PES character from the Hessian: a local minimum has no imaginary frequency, a first-order transition structure has one, and a second-order saddle has two. The authors inspect the corresponding normal modes and report that the imaginary modes of the TS and second-order saddle distort the H-bonder along minimum-energy paths toward reaction-graph neighbours. The graph contains first-order links between the LM and TS and between the TS and second-order saddle, and a second-order LM-to-saddle relationship; its topology is reported to map isomorphically onto the PES.

## 5. Private reference results

SI19 reports for species 6a: E = −742.047761126 hartree, lowest listed frequencies 114.1096, 119.5232 and 132.6605 cm−1, and free energy −741.873538 hartree. For 7a: E = −742.047761126 hartree, lowest listed frequencies −1148.3611, 113.3209 and 129.4563 cm−1, and free energy −741.871203 hartree. For 8a: E = −742.032503022 hartree, lowest listed frequencies −1399.2028, −1384.8909 and 115.9554 cm−1, and free energy −741.865297 hartree. These values are hidden from Agents.

## 6. Limitations and interpretation boundaries

The benchmark evaluates reproduction of the SI stationary-point records and the qualitative topology claim, not universal proof that every chemical PES is graph-isomorphic. Frequency values are method-, solvent-model- and numerical-convergence-dependent. Mode correspondence is assessed from the submitted normal-mode interpretation, with a bounded failure branch allowed if a requested stationary point cannot be validated.
