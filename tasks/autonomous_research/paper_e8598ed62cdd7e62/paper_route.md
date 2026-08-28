# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to explain prototropic tautomerism of N-(4-methoxyphenyl)-4-oxothiochromane-3-carbothioamide (2d). The authors claim that the gas-phase tautomerization network can be described by three concerted channels from keto form R to enol P1, enethiol P2, and thiol-imine P3, and that thermodynamic and kinetic quantities rationalize the observed tautomeric behavior (ev_doc_7aee6b9b6214_000430_10fa642e9974; ev_doc_7aee6b9b6214_000636_70e0738f5171).

## 2. System and model boundary

The modeled species is neutral, closed-shell C17H15NO2S2 2d. The paper considers gas-phase isolated-molecule calculations at 298.15 K, with optional CHCl3 IEFPCM optimizations and GIAO NMR calculations reported as ancillary work. The benchmark core is the gas-phase keto/enol/enethiol/thiol-imine network and its three R-to-P transition states; crystal packing and explicit solvent are outside the scored computational boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish stationary points for the four tautomeric forms | 2d connectivity and starting geometries | DFT geometry optimization in Gaussian 09 | B3LYP/6-31+G(d,p), gas phase; neutral molecule | Optimized R, P1, P2, P3 geometries and energies | ev_doc_7aee6b9b6214_000234_101b28691983 |
| 2 | Establish the three interconversion saddle points | Optimized reactant/product forms | Transition-state search and harmonic frequencies in Gaussian 09 | Same B3LYP/6-31+G(d,p) level, gas phase | TS1 (R↔P1), TS2 (R↔P2), TS3 (R↔P3), frequencies | ev_doc_7aee6b9b6214_000234_101b28691983; ev_doc_7aee6b9b6214_000430_10fa642e9974 |
| 3 | Validate stationary-point character | All optimized minima and TS candidates | Harmonic vibrational analysis | Minima: no imaginary modes; TS: one imaginary mode along reaction coordinate | Validated stationary points | ev_doc_7aee6b9b6214_000234_101b28691983 |
| 4 | Derive thermodynamic and kinetic observables | Validated energies, ZPVE and frequencies | Gaussian thermochemistry and energy differences | 298.15 K; ΔG=ΔH−TΔS; K=exp(−ΔG/RT) | ΔE, ΔH, ΔS, ΔG, K and activation ΔE#, ΔH#, ΔS#, ΔG#, K# | ev_doc_7aee6b9b6214_000439_77cf2488a3ca; ev_doc_7aee6b9b6214_000454_7912036b8140 |

## 4. Validation and analysis protocol

The authors required zero imaginary frequencies for minima and exactly one imaginary frequency for each transition state. They mapped TS1, TS2 and TS3 to R↔P1, R↔P2 and R↔P3, respectively, and compared relative ZPVE-corrected energies, reaction thermodynamics and forward/reverse activation parameters. The authors also compared computed NMR data with experiment and used X-ray diffraction to identify the solid-state form, but these are interpretive corroborations rather than part of the hidden numerical benchmark.

## 5. Private reference results

The paper reports reaction ΔE values of −4.44, 4.23 and 4.12 kcal mol−1 for R→P1, R→P2 and R→P3, respectively, with ΔH −4.66, 4.32 and 4.29; ΔS −4.92, 1.11 and 1.07 cal mol−1 K−1; ΔG −3.19, 3.99 and 3.97; and K 2.17×10^2, 1.18×10−3 and 1.22×10−3 (Table 1, ev_doc_7aee6b9b6214_000439_77cf2488a3ca). Forward activation ΔE# values are 50.66, 59.34 and 56.82 kcal mol−1 for R→TS1, R→TS2 and R→TS3, with ΔH# 50.65, 59.03 and 56.36; ΔS# −3.05, −7.32 and −6.60; ΔG# 51.56, 61.21 and 58.34; and K# 1.60×10−38, 1.34×10−45 and 1.73×10−43 (Table 2, ev_doc_7aee6b9b6214_000454_7912036b8140). Reverse activation rows are also reported there.

## 6. Limitations and interpretation boundaries

The authors explicitly caution that gas-phase DFT omits explicit solvent, intermolecular forces, hydrogen-bonding networks and temperature-dependent conformational dynamics; this helps explain why gas-phase thermodynamic preference need not equal the experimentally predominant solution/solid tautomer (ev_doc_7aee6b9b6214_000454_7912036b8140). The benchmark therefore scores the defined gas-phase model, not an experimentally universal tautomer population.
