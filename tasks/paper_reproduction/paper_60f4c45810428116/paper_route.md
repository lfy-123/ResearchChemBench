# Private paper route

## 1. Scientific objective and author claim

The authors computed one-electron reduction potentials of sulfur-containing chloromethyl precursor 1a and thiophenyl leaving-group precursor 1h relative to the ferrocene/ferrocenium couple. Their interpretation is that the lower reduction potential of the SPh leaving group helps explain delayed carbenoid generation and distinctive sulfur reactivity.

## 2. System and model boundary

The systems are neutral closed-shell 1a and 1h, their dissociative one-electron reduction products (a neutral carbon-centered radical plus an anionic leaving fragment), and neutral ferrocene/its cationic doublet ferrocenium reference. The reported thermochemistry is solution-phase THF at 298 K.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize and frequency-check 1a | SI Table S11 structure | Gaussian 16; B3LYP-D3 | 6-311+G(d,p), SMD(THF) | G298(1a) | ev_doc_1953ff03f3f7_000311_acb3e8728e2c; ev_doc_1953ff03f3f7_000316_7288090c2774 |
| 2 | Optimize and frequency-check 1h | SI Table S15 structure | Gaussian 16; B3LYP-D3 | 6-311+G(d,p), SMD(THF) | G298(1h) | ev_doc_1953ff03f3f7_000311_acb3e8728e2c; ev_doc_1953ff03f3f7_000332_183b99513533 |
| 3 | Optimize and frequency-check ferrocene | SI Table S7 structure | Gaussian 16; B3LYP-D3 | 6-311+G(d,p), SMD(THF), LANL08 on Fe | G298(Fc) | ev_doc_1953ff03f3f7_000311_acb3e8728e2c; ev_doc_1953ff03f3f7_000316_7288090c2774 |
| 4 | Optimize and frequency-check ferrocenium | SI Table S8 structure | Gaussian 16; B3LYP-D3 | 6-311+G(d,p), SMD(THF), LANL08 on Fe, charge +1, doublet | G298(Fc+) | ev_doc_1953ff03f3f7_000311_acb3e8728e2c; ev_doc_1953ff03f3f7_000317_0c298e97fea8 |
| 5 | Form dissociative reduction free energies and reference potentials | four G298 values plus fragment calculations | thermochemical redox protocol based on cited ref. 23 | Fc/Fc+ reference | potentials vs Fc/Fc+ | ev_doc_1953ff03f3f7_000313_459ed7808bc0; ev_doc_1953ff03f3f7_000373_744bfc6bd086 |

## 4. Validation and analysis protocol

Each optimized structure was checked by harmonic frequencies as a minimum. Reaction free energies were combined with the calculated Fc/Fc+ reference electrode and converted to potentials for the two dissociative reactions. The paper compares the two sulfur-containing substrates and uses their relative redox behavior to interpret flow-reactivity observations.

SI PDF page 19 describes 5.36 V (Table S6) as a calculated Fc/Fc+ output, not a measured calibration to supply to the agent. Table S5 prints G298(Fc) = -510.542802 Eh and G298(Fc+) = -510.347148 Eh; their difference implies about 5.324 V, so the source's table-level discrepancy should be reported rather than silently fitted. LANL08 includes an Fe effective core potential; a Gaussian general orbital-basis block alone does not activate it. Verify the native ECP/effective-electron record (10 Fe core electrons removed), not a job title or unused appended ECP block. These are verifier checks, not prescribed agent route choices.

## 5. Private reference results

Table S10 reports −1.75 V for 1a and −2.81 V for 1h, both versus Fc/Fc+. The associated reaction free energies are −348.5 and −245.8 kJ mol−1, respectively. These values are hidden from Agent-visible inputs.

## 6. Limitations and interpretation boundaries

The benchmark scores the reported computed potentials, not experimental potentials or a unique optimized geometry. Alternative conformers, spin-state treatment, thermal conventions, and implementation choices must be disclosed and validated by the investigator; agreement with the hidden reference does not establish a unique mechanism.
