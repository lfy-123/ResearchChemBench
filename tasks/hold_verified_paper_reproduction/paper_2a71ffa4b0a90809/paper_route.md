# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to quantify conformational rigidity of perfluoroiodoarene XB donor 1a. The authors claim that 1a has a high syn-to-anti rotational barrier and is therefore atropisomeric/rigid because of steric crowding by iodine and fluorine atoms.

## 2. System and model boundary

The system is neutral singlet 1a (C18F12I2), specifically the SI Cartesian structure labelled 1a-syn, in implicit THF at 193.15 K. The scan concerns rotation between the C6F4I ring and its linker, with the SI-defined dihedral starting at 69.0° and reduced to 0°. The endpoint profile is an electronic/Gibbs free-energy computational observable, not an experimental kinetic measurement.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain solution conformers | 1a structures | DFT in Gaussian | SMD18(THF)/M06-2X-D3/6-311+G(d,p)-SDD(I), 193.15 K | Optimized geometries and E/H/G | SI S-60, S-66 and S-69; S-85 reference S24; ev_doc_600c5cbf2e8e_000158_b5a7ca47f7e7; ev_doc_85e0255cc1d7_001101_39447bba071e; ev_doc_85e0255cc1d7_001381_bafa6b31b993 |
| 2 | Follow rotation | optimized 1a-syn; defined dihedral | ModRedundant constrained scan | 69.0° to 0°; same solvent/model context | Gibbs profile relative to ground state | ev_doc_85e0255cc1d7_001155_d7a95a0774c6; ev_doc_85e0255cc1d7_001162_176899e528ce; ev_doc_85e0255cc1d7_001163_dc9a6a80bc1a |
| 3 | Extract barrier | scan profile | energy-profile analysis | maximum relative to ground state | rotational barrier | ev_doc_85e0255cc1d7_001165_bba49d556284; ev_doc_85e0255cc1d7_001166_2e35d355b687; ev_doc_85e0255cc1d7_001167_da86644e80cd |

## 4. Validation and analysis protocol

The scan was interpreted as the energy at the 0° endpoint relative to the ground-state structure. The SI reports increasing distortion during the constrained rotation and an estimated barrier. Independent validation should check atom identity/count, neutral singlet specification, dihedral atom definition, optimization/constrained-scan stationarity, profile continuity, and the reported maximum/endpoint extraction. Alternative computational methods are scientifically interpretable but should be identified as sensitivity tests rather than silently treated as the authors' protocol.

## 5. Private reference results

The paper reports a 31.0 kcal mol−1 rotational barrier for 1a; the SI describes the 0° endpoint as the estimated barrier and shows a rising profile. The SI computational table reports G values for 1a-anti and 1a-syn of −1906.468789 and −1906.469033 hartree, respectively, at the stated level and temperature. These values are hidden evaluator references.

## 6. Limitations and interpretation boundaries

A constrained relaxed scan is a pathway/profile estimate and need not be a transition-state optimization. The barrier is model-, solvent- and temperature-dependent. The supplied syn geometry is an author structure; independent conformer generation and numerical convergence remain the investigator's responsibility. The result supports a rigidity interpretation within the stated computational boundary and does not alone establish a solution-phase experimental rate.

## 7. 2026-09-27 verification-method discrepancy — HOLD

The main text abbreviates the solvation model as SMD, but SI S-60/S-66/S-69 explicitly specifies SMD18. Reference S24 (Engelage et al., 2018, DOI 10.1002/chem.201803652) defines refined Br/I Coulomb radii; the suffix is not a citation marker. The archived verification uses ordinary `SCRF=(SMD,Solvent=THF)` without an SMD18 radius override. Five stored scan-frequency formatted checkpoints show iodine cavity radii of 1.98 Angstrom. Thus the archived approximately 30 kcal/mol profile is not yet a demonstrated SMD18 reproduction of the published 31 kcal/mol result. The exact contribution of this method mismatch has not been calculated. No scoring target, public input, or historical calculation was altered. See evaluation/verified_computation_reference.md section 8 for evidence and the follow-up required before release.
