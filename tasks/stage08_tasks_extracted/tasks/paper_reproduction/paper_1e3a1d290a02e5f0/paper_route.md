# Private paper route

## 1. Scientific objective and author claim

The paper designs three carbazole–diphenylamine hole-transport materials (JY1, JY2, JY3) differing by one, two, or three fluorines on the terminal biphenyl ring. The computational claim is that fluorination tunes frontier orbital energies and charge-transport-relevant internal hole reorganization energy; JY2 is described as the strongest overall performer.

## 2. System and model boundary

The isolated neutral singlet molecules are the synthesized compounds named in SI S1.5. Geometry, FMO energies, and internal hole reorganization energies are molecular properties. The later crystal/MD hopping and perovskite-interface simulations are outside this task's primary molecular boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground state | JY1–JY3 neutral singlets | Gaussian 09 DFT | B3P86/6-311G(d,p) | optimized structures | ev_doc_2e3bd9857e3a_000036_d3cee0072653; SI S1.1 |
| 2 | Validate minima | optimized structures | Gaussian 09 frequency | same level; no imaginary frequencies | frequencies/minimum check | SI S1.1 |
| 3 | Obtain FMO energies | optimized structures | same DFT wavefunction | HOMO/LUMO extraction | orbital energies | ev_doc_2e3bd9857e3a_000036_d3cee0072653 |
| 4 | Compute λh | neutral/cation energy surfaces | same theoretical level | internal hole reorganization cycle | λh | SI S1.1; ev_doc_2e3bd9857e3a_000049_f2f4a5df82fc; ev_doc_2e3bd9857e3a_000051_ae4d8e10a477 |
| 5 | Interpret trend | three molecule results | comparison | fluorine-count comparison | HOMO/LUMO and λh trend | ev_doc_2e3bd9857e3a_000036_d3cee0072653 |

## 4. Validation and analysis protocol

The authors use absence of imaginary frequencies as the lowest-structure check. They report HOMO and LUMO for all three molecules and λh values, then interpret fluorination and the relative transport implications. Their stated λh values are 0.191, 0.186, and 0.189 eV for JY1, JY2, and JY3.

## 5. Private reference results

Reported calculated HOMO (eV): JY1 −5.12, JY2 −5.17, JY3 −5.18. Reported calculated LUMO (eV): JY1 −1.88, JY2 −2.19, JY3 −2.18. Reported λh (eV): JY1 0.191, JY2 0.186, JY3 0.189. The paper states HOMO decreases with fluorine count and JY2 has the smallest λh.

## 6. Limitations and interpretation boundaries

The paper does not provide Cartesian coordinates, so public inputs encode exact systematic names and formulas rather than author geometries. Orbital energies are method- and convention-dependent. λh is an internal molecular quantity and does not by itself reproduce the paper's later crystal hopping mobility or device PCE. No claim about a unique global conformer beyond the frequency-validated optimized structure should be inferred.
