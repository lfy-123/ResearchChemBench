# Private paper route

## 1. Scientific objective and author claim

The paper tests whether moving a pinacol boronate ester (Bpin) between the 1, 2, and 4 positions of carbazole changes excited-state structure, spin–orbit coupling (SOC), and ultimately blue room-temperature phosphorescence (RTP) in PVA. The authors claim that CZ2B has the most favorable excited-state separation/polarity and hydrogen bonding, giving the longest lifetime and high quantum yield.

## 2. System and model boundary

The computational objects are isolated, neutral, closed-shell singlet CZ1B, CZ2B, and CZ4B molecules. Experimentally, the emitters are guest-doped at 0.5 wt% in PVA films; the calculations model the isolated molecular electronic states rather than an explicit polymer environment. The compounds are 1-, 2-, and 4-(4,4,5,5-tetramethyl-1,3,2-dioxaborolan-2-yl)-9H-carbazole. Crystal deposition identifiers are CZ1B CCDC 2474736, CZ2B CCDC 2474784, and CZ4B CCDC 2474735.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain molecular ground-state structures | CZ1B, CZ2B, CZ4B | DFT in ORCA | B3LYP/6-31G; neutral singlet | optimized S0 geometries | ev_doc_d5323eaeff10_000001_d0be096319f3 |
| 2 | Compute excited states and SOC | optimized isolated molecules | TD-DFT and ORCA SOC | B3LYP/6-31G(d,p); inspect triplets close to S1 | energies, NTOs, SOC matrix elements | ev_doc_d5323eaeff10_000001_d0be096319f3; ev_doc_9e063f9c1ba7_000045_ddf2aa77b5a5; ev_doc_9e063f9c1ba7_000046_242e7bdb6158 |
| 3 | Interpret excited-state character | excited-state wavefunctions | Multiwfn/VMD NTO, ESP and IRI analyses | source specifies these analyses | orbital localization, polarity and interactions | ev_doc_d5323eaeff10_000001_d0be096319f3; ev_doc_9e063f9c1ba7_000047_77596831b4b5 |
| 4 | Relate computation to RTP | SOC and electronic descriptors plus films | comparison with measured PVA-film photophysics | lifetimes and quantum yields measured experimentally | structure–property interpretation | ev_doc_9e063f9c1ba7_000041_4df704c45076; ev_doc_9e063f9c1ba7_000108_fec1a4b95644 |

## 4. Validation and analysis protocol

The authors compare the three isomers on common state definitions, identify triplets near S1 (the text specifies ±0.3 eV), and use NTO localization to interpret the SOC-bearing state. The source reports gaps of 4.48, 4.49, and 4.40 eV for CZ1B, CZ2B, and CZ4B. It states that the largest-SOC state is T3 for CZ1B/CZ4B and T4 for CZ2B, with CZ2B showing Bpin-associated electron density and HLCT character. AIM hydrogen-bond energies are 4.21, 4.71, and 4.33 kcal mol−1 for CZ1B, CZ2B, and CZ4B. Experimental PVA-film lifetimes are 3.96, 5.20, and 4.27 s for CZ1B, CZ2B, and CZ4B, respectively; quantum yields are 17.94%, 25.31%, and 26.95%.

## 5. Private reference results

The source-backed reference set is: CZ2B has the longest lifetime (5.20 s), CZ1B the shortest (3.96 s), and CZ4B is intermediate (4.27 s); smaller SOC is associated qualitatively with longer lifetime; CZ1B and CZ4B highest-SOC states are T3, while CZ2B's is T4 and has Bpin-involving HLCT character. Numerical SOC labels are retained privately from Fig. 2c and are not exposed in public inputs.

## 6. Limitations and interpretation boundaries

The paper does not explicitly state the geometry source used for the electronic calculations, so crystal structures are only reproducible starting geometries, not asserted author inputs. The isolated-molecule model omits explicit PVA and cannot by itself establish hydrogen-bond energies or film kinetics. SOC values are method- and geometry-sensitive, and the figure-derived values should be treated as comparison targets rather than universal constants. Correlation with three lifetimes is descriptive, not proof of causation.
