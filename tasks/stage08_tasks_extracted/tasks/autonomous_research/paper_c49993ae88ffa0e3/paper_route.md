# Private paper route

## 1. Scientific objective and author claim

The authors used computation to test how the first hydrogen-equivalent transfer from photoexcited 9,10-phenanthrenehydroquinone (H₂PQ) to pyridine N-oxide (PyO) can begin: proton transfer followed by electron transfer, or electron transfer followed by proton transfer. They further tested whether explicit water preferentially stabilizes the ionic/radical-ion intermediates. The author claim is that both dry stepwise orders are thermodynamically accessible, while water particularly stabilizes electron-transfer-generated ionic intermediates; concerted PCET and HAT were not excluded.

## 2. System and model boundary

The computational model is H₂PQ + unsubstituted pyridine N-oxide in acetonitrile, initiated on the lowest singlet excited state associated mainly with an H₂PQ HOMO–LUMO π→π* excitation. The scored subproblem is the first elementary proton-transfer or electron-transfer event from the separated excited reactants, with and without explicit water. The published thermochemical tables denote the species as H₂PQ, HPQ⁻, H₂PQ•⁺, PyO, PyOH⁺ and PyO•⁻. The calculation is a thermodynamic comparison; it does not establish full nonadiabatic kinetics or exclude concerted PCET/HAT.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Locate stationary structures | H₂PQ, PyO and charge/proton-transfer states, including water-associated structures | Gaussian DFT/TD-DFT | M06-2X/6-31+G(d,p), SMD acetonitrile | Optimized geometries | SI p. S38, ev_doc_66ed0a19fcf4_000686_6979634fd12d and ev_doc_66ed0a19fcf4_000688_57d772af3559 |
| 2 | Check stationary-point character and obtain thermal terms | Optimized structures | Harmonic frequencies | 298.15 K; minima required for thermodynamic states | Frequencies and thermal corrections | SI p. S38, ev_doc_66ed0a19fcf4_000686_6979634fd12d |
| 3 | Address configurational uncertainty | OH rotations and alternative substrate···catalyst, substrate···H₂O and catalyst···H₂O interactions | Manual conformational search | Multiple interaction motifs; Boltzmann-weighted step energies | Conformer ensembles | SI p. S38, ev_doc_66ed0a19fcf4_000689_9f4ebe48f70f |
| 4 | Refine electronic energies | Optimized stationary structures | Gaussian single points | M06-2X/def2-TZVPP, SMD acetonitrile | Refined electronic energies | SI p. S38, ev_doc_66ed0a19fcf4_000687_af02d12360d4 and ev_doc_66ed0a19fcf4_000688_57d772af3559 |
| 5 | Form solution free energies | Frequencies and refined energies | GoodVibes 3.0.2 | 298.15 K, 1 M, Grimme quasi-harmonic entropy with 100 cm⁻¹ cutoff, symmetry and single-point corrections | Boltzmann-weighted relative Gibbs energies | SI pp. S38–S40, ev_doc_66ed0a19fcf4_000697_1ff2729d0b5a and ev_doc_66ed0a19fcf4_000698_b05f07355bf3 |
| 6 | Validate excited-state assignment | Optimized excited H₂PQ and HPQ⁻ states | TD-DFT orbital/configuration analysis | Lowest singlet, predominantly HOMO–LUMO π→π* | Excited-state character | SI pp. S41–S42 and main paper p. 4, ev_doc_3c029ba74c8a_000159_1412e4e6dd05 |
| 7 | Compare elementary-step orders and water response | Relative free energies of reactants and ionic intermediates | Thermodynamic profile comparison | Dry versus explicitly hydrated model | ΔG values and mechanistic interpretation | Main paper Figure 2/p. 4 and SI p. S40, ev_doc_3c029ba74c8a_000159_1412e4e6dd05 and ev_doc_3c029ba74c8a_000166_2038613b5c0f |

## 4. Validation and analysis protocol

The authors verified minima by vibrational analysis, manually sampled OH orientations and intermolecular/water contacts, used Boltzmann-weighted relative energies, included SMD acetonitrile throughout, and checked that the relevant S₁ states were predominantly HOMO–LUMO excitations. They also explored deprotonation scans and described the deprotonation steps as barrierless. A fair reproduction should preserve charge, multiplicity and excited-state identities; compare like standard states; report conformer coverage; and test whether water-placement choices change the inferred ordering.

## 5. Private reference results

For the first transfer, the main paper reports ΔG = −0.9 kcal mol⁻¹ for proton transfer first and −1.6 kcal mol⁻¹ for electron transfer first without explicit water. Figure 2 reports −1.3 and −8.2 kcal mol⁻¹, respectively, with explicit water. Thus both dry alternatives are mildly favorable, and explicit water stabilizes the electron-transfer intermediate much more strongly. The SI p. S40 table independently gives −0.9 and −1.6 for the dry models and −8.2 for hydrated electron transfer, but gives −2.2 kcal mol⁻¹ for hydrated proton transfer; this source discrepancy must be acknowledged rather than silently collapsed.

## 6. Limitations and interpretation boundaries

The calculations concern H₂PQ + unsubstituted PyO, not the H₂PQ-CF₃/4-methoxypyridine N-oxide pair used in some experiments. They are preliminary thermodynamic models, not rate constants. The explicit-water construction is model-dependent, the main Figure 2 hydrated proton-transfer value differs from the SI thermochemical table, and the authors explicitly state that concerted PCET or direct HAT might contribute. Conclusions should therefore be limited to relative thermodynamic support within the sampled states and solvent models.
