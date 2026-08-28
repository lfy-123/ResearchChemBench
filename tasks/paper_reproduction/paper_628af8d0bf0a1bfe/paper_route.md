# Private paper route

## 1. Scientific objective and author claim

The authors quantify substituent-dependent antiaromaticity in benzothiophene-fused pentalenes using the out-of-plane tensor component of nucleus-independent chemical shift at 1.7 Å, NICS(1.7)zz. Their claim is that the 1,4-substituents modulate the paratropic response: electron-withdrawing substituents strengthen, whereas electron-donating substituents weaken, the antiaromatic character, consistent with the topological charge stabilization rule.

## 2. System and model boundary

The benchmark uses the neutral closed-shell singlets 4a and 4c. Compound 4a is 6,12-bis[3,5-bis(trifluoromethyl)phenyl]pentaleno[1,2-b:4,5-b']dibenzothiophene (C36H14F12S2). Compound 4c is 6,12-bis(4-methoxyphenyl)pentaleno[1,2-b:4,5-b']dibenzothiophene (C34H22O2S2). The evaluated quantity is the zz component of the magnetic shielding-derived NICS at a ghost center 1.7 Å normal to the centroid of each of the two monocyclic five-membered rings of the pentalene core; the molecular value is the arithmetic mean of the two symmetry-related probes. Gas-phase equilibrium structures and electronic magnetic response are considered. Solvent, temperature, vibrational averaging, crystal packing, excited states, and kinetic stability are outside scope.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Select a geometry method sensitive to pentalene bond-length alternation | TMS model 4e′ and experimental 4e core bond lengths | Gaussian 16 Rev. B.01; DFT benchmark | B3LYP, M06, M06-2X, ωB97X-D, M11 with 6-31++G(d); compare pentalene C–C lengths | M06-2X selected as best agreement | SI Computational Methods, ev_doc_bdc1c3beb1ba_000443_513c88d74038, ev_doc_bdc1c3beb1ba_000445_fe140d495c31, ev_doc_bdc1c3beb1ba_000447_1fdc4237f1ac |
| 2 | Obtain equilibrium structures | 4a and 4c molecular structures | Gaussian 16; M06-2X/6-31++G(d) | No symmetry assumptions; default thresholds/algorithms | Optimized geometries | SI, ev_doc_bdc1c3beb1ba_000450_7e389655588e and coordinate Tables S11/S13, ev_doc_bdc1c3beb1ba_000620_abba8d458556, ev_doc_bdc1c3beb1ba_000624_27fe59b7d66e |
| 3 | Validate stationary points | Optimized 4a and 4c structures | Harmonic frequency analysis at optimization level | NIMAG = 0 | Confirmed minima | SI, ev_doc_bdc1c3beb1ba_000451_d5b60057dedc |
| 4 | Calculate magnetic response | Validated optimized geometries and ghost centers | M06-2X/6-311+G(2d,p), Gaussian-compatible NMR calculation; py.Aroma 4 preparation/analysis | Ghost atoms 1.7 Å above monocyclic ring centroids; zz tensor component; pentalene mean plane | NICS(1.7)zz values | SI, ev_doc_bdc1c3beb1ba_000463_c7319ab9fdc6 through ev_doc_bdc1c3beb1ba_000468_7f98585586c6 |
| 5 | Interpret substituent effect | NICS values across series | Ordering and qualitative electronic-effect analysis | Compare electron-withdrawing and electron-donating endpoints | Structure–property conclusion | Main paper, ev_doc_81fda1f0fd26_000105_7e2bd38c4a3f and ev_doc_81fda1f0fd26_000106_3a3e5838996f |

## 4. Validation and analysis protocol

The authors optimized without symmetry constraints and verified every stationary point by frequency analysis with zero imaginary frequencies. Their functional choice was benchmarked against experimental pentalene-core C–C bond lengths of 4e because NICS is sensitive to bond-length distributions. NICS probes were positioned 1.7 Å normal to the pentalene mean plane above monocyclic ring centroids. For this benchmark, a submission must independently demonstrate minima, define both probes reproducibly, show approximate equivalence of the two ring values, and report method sensitivity or a defensible limitation.

## 5. Private reference results

The main paper reports NICS(1.7)zz = +23.6 ppm for 4a and +19.2 ppm for 4c. Therefore 4a > 4c by 4.4 ppm in positive NICS(1.7)zz. Both values are strongly positive and support pronounced antiaromaticity; the more electron-withdrawing 3,5-bis(trifluoromethyl)phenyl substitution in 4a gives the stronger paratropic response relative to the p-methoxyphenyl-substituted 4c. Source: ev_doc_81fda1f0fd26_000105_7e2bd38c4a3f.

## 6. Limitations and interpretation boundaries

NICS is a magnetic aromaticity descriptor, not a standalone proof of every aspect of aromaticity. The paper supplements it with ACID analysis for 4a, but the two-endpoint benchmark does not require reproducing ACID. The numerical comparison is method- and geometry-sensitive, and gas-phase equilibrium calculations do not include crystal packing, solvent, temperature, or vibrational averaging. The endpoint result supports a substituent association within this scaffold; it does not establish a universal causal law for all antiaromatic systems.
