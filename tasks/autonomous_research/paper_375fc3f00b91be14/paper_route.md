# Private paper route

## 1. Scientific objective and author claim

The paper tests whether the photoisomerization of the PyDIG photobase from E,E to Z,Z increases aqueous basicity enough to explain the observed pH swing and activation of GlyGly for direct-air capture. The computational claim is that calibrated DFT pKa values for the lowest-energy E,E and Z,Z forms reproduce both the direction and approximate magnitude of the experimental basicity increase.

## 2. System and model boundary

The modeled species are neutral and singly protonated E,E, E,Z, and Z,Z PyDIG. The reported pKa comparison uses the lowest-energy neutral and protonated conformations of E,E and Z,Z in water. The reaction is the aqueous deprotonation of the protonated base; the calculation excludes explicit water molecules, GlyGly, CO2, excited states, and photochemical dynamics.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Search and optimize neutral/protonated conformers | PyDIG E,E/E,Z/Z,Z structures | Gaussian 16 Rev. C.02; M06-2X/6-311++G(d,p) | Gas phase optimization; frequencies, ZPE and thermal corrections; frequencies below 60 cm-1 raised to 60 cm-1 | Optimized geometries and gas-phase Gibbs energies | ev_doc_a0c4a37e604c_000275_b1752101b307; ev_doc_a0c4a37e604c_000285_4fee02c037b7 |
| 2 | Include aqueous solvation | Gas-phase optimized geometries | Gaussian 16 SMD single points | Water; M06-2X/6-311++G(d,p) | Solvent-corrected free energies | ev_doc_a0c4a37e604c_000285_4fee02c037b7; ev_doc_a0c4a37e604c_000286_46d1fd837f4d |
| 3 | Select states for acidity calculation | Conformer/tautomer ensemble | Relative free-energy comparison | Lowest-energy solution conformer for each E,E/E,Z/Z,Z neutral and protonated family; rotations about imine C-N, Cα-N and C-C bonds | State-specific free energies | ev_doc_a0c4a37e604c_000307_66eaa72a9f6a; ev_doc_a0c4a37e604c_000335_f638189d0d0a |
| 4 | Compute and calibrate pKa | Solvent free energies of HA and A− | Thermodynamic pKa cycle and linear calibration | Proton solvation −257.55 kcal/mol; lg(2) for two equivalent deprotonating groups; pKa_pred = 0.6835 pKa_calc | Predicted pKa for E,E and Z,Z | ev_doc_a0c4a37e604c_000307_66eaa72a9f6a; ev_doc_a0c4a37e604c_000310_585cb17a6baf; ev_doc_a0c4a37e604c_000312_8169bcfa467c |

## 4. Validation and analysis protocol

The authors compared the computed E,E and Z,Z pKa values with spectrophotometric titration values and compared the computed change with the experimental change. They also interpreted the neutral conformer landscape: E,E-1 is the dominant neutral form, while protonated forms have many close-lying conformers; the increased Z,Z basicity is attributed mainly to destabilization of neutral Z,Z rather than unusually strong stabilization of protonated Z,Z.

## 5. Private reference results

The paper reports predicted pKa values of 7.04 for E,E and 9.60 for Z,Z, giving a computed increase of 2.56 log units. The experimental values are 6.31 and 9.12, an increase of 2.81 log units. The paper describes the calculated increase as differing from experiment by about 0.2 log units.

## 6. Limitations and interpretation boundaries

The protocol is an implicit-solvent, single-geometry-per-selected-family approximation with a calibrated regression. Protonated PyDIG has a crowded conformational landscape (7 E,E, 8 E,Z and 2 Z,Z structures in the reported search), so a single conformer result is not a complete ensemble free energy. The computation supports a thermodynamic basicity interpretation; it does not establish photochemical rates, excited-state mechanisms, CO2-transfer kinetics, or engineering performance.
