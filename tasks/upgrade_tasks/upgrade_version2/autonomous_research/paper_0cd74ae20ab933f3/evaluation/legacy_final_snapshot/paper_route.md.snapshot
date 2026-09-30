# Private paper route

## 1. Scientific objective and author claim

The paper tests whether the electronics of axial 4-substituted pyridines tune the singlet–triplet magnetic exchange gap of Cu(II) paddlewheel model complexes. The authors claim that electron-donating substituents strengthen antiferromagnetic coupling, producing a modestly lower thermally populated triplet fraction.

## 2. System and model boundary

The computational models are isolated neutral Cu2(AnCOO)4(4-RPy)2 paddlewheel complexes, with R = H, CH3, and OCH3. AnCOO is the 9-anthracenecarboxylate bridge; each Cu(II) is represented in the dimer and each axial site is capped by 4-RPy. The singlet is open-shell/multireference, so the triplet geometry is used as the equilibrium structural approximation. The reported observable is the singlet–triplet gap J in cm^-1 and the triplet population A at 300 K.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain equilibrium model structures | Cu2(AnCOO)4(4-RPy)2 starting structures | ORCA 6.0.1 triplet DFT geometry optimization | B3LYP, def2-SVP, D3BJ, def2/J, RIJCOSX/COSX | Optimized triplet geometries | ev_doc_dc21c53cc060_000276_2b1aa068d3a2; ev_doc_dc21c53cc060_000278_2c7144eead6e |
| 2 | Compute singlet–triplet gaps | Optimized triplet geometries | PySCF-forge multicollinear SF-TDDFT | B3LYP/def2-SVP, def2-svp-jkfit; unrestricted Sz=1 triplet reference; no TDA for reported SF-TDDFT | J for H, Me, OMe | ev_doc_dc21c53cc060_000280_7e773e530c68; ev_doc_dc21c53cc060_000282_da1c7a4829d0 |
| 3 | Relate coupling to thermochromic spin population | J values | Boltzmann/Bleaney-style expression | A=100·3 exp(J/kT)/(1+3 exp(J/kT)); T=300 K | A and substituent trend | ev_doc_7a54bf831714_000383_2feb94e7f8e6; ev_doc_7a54bf831714_000384_7a2b2cd78ddd |

## 4. Validation and analysis protocol

The SI benchmarks functional, basis-set, and geometry sensitivity for R=H and reports close agreement between SF-TDDFT and SF-TDA, triple-zeta Cu calculations, and CASSCF-optimized geometry. The paper compares calculated and measured J values for all three pyridines and evaluates the relative trend against Hammett substituent constants. The triplet population is evaluated from the reported J convention and temperature expression.

## 5. Private reference results

SI Table S4 reports calculated J/A: H −335 cm^-1/37.6%, CH3 −342/36.8%, OCH3 −345/36.4%; measured values: H −367/34.0%, CH3 −383/32.3%, OCH3 −381/32.5%.

## 6. Limitations and interpretation boundaries

The models omit the extended MOF lattice and use triplet geometries for an intrinsically multireference singlet. Numerical agreement is therefore a method-reproduction target, not proof that the isolated model uniquely predicts the solid-state material. Sign conventions must be stated explicitly; this task uses the paper's negative-J convention.
