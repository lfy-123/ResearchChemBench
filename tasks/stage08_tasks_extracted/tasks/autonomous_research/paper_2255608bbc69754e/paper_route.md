# Private paper route

## 1. Scientific objective and author claim

The authors use a simplified polyene model (cal-1) to explain EtzB-catalysed formation of a fused furofuran ring. They claim that two consecutive epoxidation/epoxide-opening cascades, with acid-promoted SN1-type ring opening and barrierless intramolecular capture, are preferred to the alternative sequential-epoxidation/SN2 route.

## 2. System and model boundary

The model is the neutral singlet cal-1 polyene/allylic alcohol and the explicitly modelled reagent pool cal-1 + 2 mCPBA + HOAc + H2O + HO−. The reported profile is a 298 K Gibbs free-energy profile for stationary points and branch alternatives in water; protein/environment effects are not represented.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Find low-energy conformers | cal-1 and intermediates | CREST | conformational exploration before QM | conformer set | ev_doc_4043dc68c5cf_000311_8f12f1dfa864 |
| 2 | Optimize and classify stationary points | conformers, TS guesses | Gaussian ωB97X-D/def2-SVP, SMD(water) | frequency analysis; 298.15 K, 1 atm; ZPVE scale 0.9791; quasi-RRHO low modes | minima/TS thermochemistry | ev_doc_4043dc68c5cf_000311_8f12f1dfa864; ev_doc_4043dc68c5cf_000598_8fc25dadd03c |
| 3 | Refine electronic energies | optimized structures | Gaussian ωB97X-D/def2-QZVP, SMD(water) | same solvation settings | refined energies | ev_doc_4043dc68c5cf_000598_8fc25dadd03c |
| 4 | Assemble profile | refined energies and corrections | G(final)=E_SP(QZVP)+ΔG_corr(SVP) | relative to common reagent pool | free-energy profile and branch comparison | ev_doc_4043dc68c5cf_000614_04a897a17091 |

## 4. Validation and analysis protocol

Frequencies distinguish minima (zero imaginary modes) from transition states (one imaginary mode); transition states were checked by IRC. Flexible scans and conformer averaging were used for the two intramolecular O–C closures, and the scans were interpreted as barrierless where no stationary point was found. The profile compares the SN1 and SN2 alternatives and reports the stereochemical branch ratio for the first closure.

## 5. Private reference results

The SI energy table contains G(final) values for cal-1, cal-2a, cal-2b, cal-3a, cal-3c, cal-4a, cal-4b, cal-5 and the transition states TS-1, TSa-2a/b/c, TSa-3a, TS-4a/b, TSb-2 and TSb-3b. Main-text barriers include TS-1 25.3, TSa-2b 14.3, TSa-2c 21.0, TS-4a 15.9 and TS-4b 20.7 kcal mol−1. The SI reports barrierless cal-2b→cal-3a/3b and cal-4b→cal-5 closure, with cal-3a 86.9% and cal-3b 13.1%.

## 6. Limitations and interpretation boundaries

This is a gas-phase molecular model with implicit water, not an enzyme QM/MM calculation. Relative energies depend on conformer coverage, protonation/reagent bookkeeping and the chosen electronic-structure approximation; the paper itself calls for protein-structure and QM/MM work.
