# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic spin-state energetics of isolated Fe(II) complexes to establish the intrinsic ligand-field trend in `[Fe(LPh-TDA)(NCE)2]` (C1, E=S; C2, E=Se; C3, E=BH3), and then compares that trend with packing-dependent solid-state spin crossover. The qualitative claim is that stronger pseudohalide field increases stabilization of LS relative to HS in the order C3 > C2 > C1, while crystal packing can override this molecular trend.

## 2. System and model boundary

Each isolated neutral complex contains Fe(II), one tetradentate ligand LPh-TDA = 1-(5-phenyl-1,3,4-thiadiazol-2-yl)-N,N-bis(pyridin-2-ylmethyl)methanamine, and two cis monodentate anions NCS−, NCSe−, or NCBH3−. The Fe centre is octahedral, with four N donors from LPh-TDA and two pseudohalide N donors. The spin states are Fe(II) high-spin quintet (S=2, multiplicity 5) and low-spin singlet (S=0, multiplicity 1). The computed quantity is the electronic energy difference between optimized LS and HS isolated molecules, reported in kJ mol−1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build isolated C1, C2, C3 in HS and LS states | Complex identities above; octahedral cis coordination | Gaussian 16 | CAM-B3LYP; CEP-31G; Grimme D3 | Initial state-specific structures | ev_doc_679baf8443de_000415_7c539b6cff4d; ev_doc_679baf8443de_000416_42d45143c6b3; ev_doc_679baf8443de_000417_ae38089298df |
| 2 | Relax each spin state | Initial structures | Gaussian 16 geometry optimization | Same model chemistry; state-specific multiplicities | Optimized HS/LS geometries and electronic energies | ev_doc_679baf8443de_000415_7c539b6cff4d; ev_doc_679baf8443de_000416_42d45143c6b3; ev_doc_679baf8443de_000417_ae38089298df |
| 3 | Form isolated spin-transition energies | Optimized HS and LS energies | Energy difference analysis | E_el^iso = E_LS − E_HS, converted to kJ mol−1 | C1 −34, C2 −28, C3 −21 kJ mol−1 | ev_doc_679baf8443de_000308_f4108b2af0ed; ev_doc_679baf8443de_000309_4c894fb63a96; ev_doc_679baf8443de_000315_bc862471148c; ev_doc_679baf8443de_000318_49cb396fb8c2 |
| 4 | Interpret series | C1–C3 values and experimental context | Within-series comparison | More positive E_el^iso means greater LS stabilization; compare only within functional/model series | C3 > C2 > C1; packing explains departures in crystals | ev_doc_679baf8443de_000017_f73d13e7e7c2; ev_doc_679baf8443de_000310_4baa59f16651; ev_doc_679baf8443de_000311_51ab8ccdd0fd |

## 4. Validation and analysis protocol

The authors compare the three values within one consistent computational series because absolute spin-transition energies depend strongly on the exchange-correlation functional. Optimized minima should be stationary structures; the paper's central interpretation is a trend, not absolute functional transferability. The isolated trend is contrasted with the observed C1 partial SCO, C2 HS persistence, and C3 complete SCO at T1/2=153 K. For the crystal model, the paper separately optimized two central molecules in four Fe1/Fe2 spin distributions in a 22-molecule C1 assembly, freezing the matrix and replacing frozen HS Fe molecules by Zn analogues; this is contextual validation of packing effects, not required for the isolated-molecule task.

## 5. Private reference results

Table 2 reports E_el^iso: C1 = −34 kJ mol−1, C2 = −28 kJ mol−1, C3 = −21 kJ mol−1. Thus C3 > C2 > C1. The paper states that C3 has the lowest HS stabilization and that the sequence agrees with NCS− < NCSe− < NCBH3− ligand-field strength. In the solid, C1 has partial LS/HS ordering, C2 remains HS over 10–300 K, and C3 undergoes complete SCO centered at 153 K.

## 6. Limitations and interpretation boundaries

These are electronic, isolated-molecule DFT differences, not free energies or direct transition temperatures. Absolute values are functional-dependent. The public task must not require reproduction of the paper's exact software or protocol, and results should be compared within the submitted method and with explicit methodological uncertainty. Initial conformers and state-continuation choices can produce local-minimum variation; multiple starts and frequency checks are therefore appropriate.
