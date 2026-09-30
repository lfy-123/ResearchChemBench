# Private paper route

## 1. Scientific objective and author claim

The paper tests whether conformational photoisomerization of the merocyanine chromophore can account for a new red-shifted absorption feature near 700 nm in dye-loaded quatsomes. The authors claim that the cisoid conformer has lower-energy low-lying excitations than the transoid conformer, supporting a photoinduced cis–trans explanation.

## 2. System and model boundary

The computational model is a neutral, singlet, simplified single chromophoric arm. Long alkyl and triethylene-glycol substituents are replaced by butyl groups. Both transoid and cisoid geometries are represented by the 57-atom S0-optimized Cartesian structures in SI Tables S8 and S9. The solvent model is gas phase; the calculated observable is the lowest singlet vertical excitation, especially S0→S1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define reduced chromophore | Full dye, peripheral chains | Structural simplification | Replace long alkyl/triethylene-glycol chains by butyl groups | Single-arm model | ev_doc_13b05be938fe_000376_d2d7df232e92 |
| 2 | Optimize transoid S0 geometry | Transoid starting structure | DFT, Gaussian16 Rev. B.01 | CAM-B3LYP/6-31G(d,p), gas phase | S0-optimized transoid geometry | ev_doc_e2fff3ecb4d3_000211_146d8dba3786; ev_doc_13b05be938fe_000376_d2d7df232e92 |
| 3 | Optimize cisoid S0 geometry | Cisoid starting structure obtained by twisting the arm | DFT, Gaussian16 Rev. B.01 | CAM-B3LYP/6-31G(d,p), gas phase | S0-optimized cisoid geometry | ev_doc_e2fff3ecb4d3_000212_bf6cfc4b1dee; ev_doc_13b05be938fe_000376_d2d7df232e92 |
| 4 | Compute excited states | Each optimized geometry | TD-DFT | Same CAM-B3LYP/6-31G(d,p) level | Vertical excitation energies, oscillator strengths and orbital assignments | ev_doc_e2fff3ecb4d3_000100_b8aecbd43501; ev_doc_e2fff3ecb4d3_000102_1334addd5cc9 |
| 5 | Compare conformers | S0→S1 values | Direct energy subtraction | cisoid minus transoid, interpreted as a red shift when negative | Relative shift | ev_doc_13b05be938fe_000120_b96ab8a91be3; ev_doc_e2fff3ecb4d3_000102_1334addd5cc9 |

## 4. Validation and analysis protocol

Verify charge/multiplicity and atom count, successful SCF and optimization convergence, and absence of imaginary frequencies if a frequency calculation is performed. Confirm that the reported state is S1 rather than a higher state, record oscillator strength and dominant orbital contribution, and compute the signed and absolute conformer difference in eV. Interpret the result only as a gas-phase model comparison; do not claim that it alone proves the experimental photochemical mechanism.

## 5. Private reference results

The SI/main text reports that S0→S1 is predominantly HOMO→LUMO and that the cisoid single-arm transition is 0.08 eV lower than the transoid transition. The paper connects this red shift to the experimentally observed ~700 nm band and presents it as support for photoinduced cis–trans isomerization.

## 6. Limitations and interpretation boundaries

Absolute excitation energies are not stated in the supplied text blocks; the robust source-backed scalar is the relative 0.08 eV shift. The reduced single-arm gas-phase model omits the full three-arm environment, solvent, quatsome membrane and photochemical kinetics. Agreement in the relative shift supports, but does not uniquely establish, the proposed mechanism.
