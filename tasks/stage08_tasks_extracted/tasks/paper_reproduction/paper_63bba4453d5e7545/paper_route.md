# Private paper route

## 1. Scientific objective and author claim

The paper tests whether conformationally enabled charge-assisted intramolecular hydrogen bonding (CA-IMHB) explains anomalous NH+ chemical shifts and pKa–shift deviations for trans piperidinium derivatives 11 (4-hydroxy) and 12 (4-methoxy). The authors claim that the twist-boat conformers bring the NH+ donor and oxygen acceptor into proximity and are favored over the corresponding chair conformers.

## 2. System and model boundary

The calculated objects are the isolated, singly protonated trans cations of compounds 11 and 12, in the gas phase. Four SI-provided starting geometries are used: 11-equatorial chair, 11 twist-boat, 12-equatorial chair, and 12 twist-boat. Each has charge +1 and singlet multiplicity. Counterions, solvent molecules, and ensemble/solvent thermodynamics are outside the calculation boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax each supplied conformer and verify a minimum | Four SI XYZ geometries | Gaussian 09 DFT optimization and frequencies | M06-2X/6-311++G(d,p), gas phase, charge +1, multiplicity 1 | Optimized geometries, energies, vibrational frequencies | ev_doc_cf92824978e4_000759_4bb7fad1e88f; ev_doc_cf92824978e4_000760_0eaa3cd3c93a; ev_doc_cf92824978e4_000761_5a37efed4ba9 |
| 2 | Predict proton NMR shielding | Optimized structures | Gaussian 09 SCF GIAO NMR | Same level; isotropic shielding referenced to calculated TMS | NH+ chemical shifts | ev_doc_cf92824978e4_000600_ac99ab8b3dca; ev_doc_cf92824978e4_000759_4bb7fad1e88f |
| 3 | Diagnose the proposed interaction | Optimized structures | Geometry and Hirshfeld analysis | NH+···O distance and oxygen partial charge | Interaction/conformation interpretation | ev_doc_cf92824978e4_000600_ac99ab8b3dca; ev_doc_cf92824978e4_000601_8a893a3740ee |

## 4. Validation and analysis protocol

The authors compare chair and twist-boat relative energies for each molecule, inspect frequencies to establish minima, compare calculated NH+ shifts, and examine NH+···O proximity and Hirshfeld oxygen charges. The gas-phase naked-cation model is explicitly recognized as potentially exaggerating CA-IMHB strength.

## 5. Private reference results

The paper reports twist-boat stabilization magnitudes of 3.23 kcal/mol for 11 and 13.49 kcal/mol for 12. Reported calculated NH+ shifts are 4.4 ppm (chair) and 6.8 ppm (twist-boat) for 11, and 4.2 ppm (chair) and 6.8 ppm (twist-boat) for 12. NH+···O distances are reported as 2.0 and 1.98 Å, respectively. Reported isotropic shieldings are 27.7/25.3 ppm for 11 and 27.9/25.3 ppm for 12; oxygen Hirshfeld charges change from −0.224 to −0.217 (11) and −0.173 to −0.166 (12).

## 6. Limitations and interpretation boundaries

These are isolated gas-phase cation calculations, not solution free energies or direct salt measurements. Conformer coverage is limited to the four supplied starting structures, and no claim is made that they exhaust all conformers. Agreement with the paper supports the reported computational interpretation but does not by itself prove the full solution-phase mechanism.
