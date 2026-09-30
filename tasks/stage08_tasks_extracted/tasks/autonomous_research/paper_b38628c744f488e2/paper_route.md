# Private paper route

## 1. Scientific objective and author claim

Quantify methanol hydrogen-bonding enthalpy changes on reduction of 2,3,5,6-tetramethyl-1,4-benzoquinone (Q(CH3)4). The authors attribute the strong redox response to the more basic dianion carbonyl oxygen and report an out-of-plane methanol contact caused by methyl sterics.

## 2. System and model boundary

One Q(CH3)4 plus one CH3OH, in radical-anion (charge -1, multiplicity 2) and dianion (charge -2, multiplicity 1) states. PCM acetonitrile, 298.15 K, 1 atm. ΔH1 and ΔH2 are complexation enthalpies relative to the corresponding isolated ion and methanol; ΔH_HB = ΔH2 − ΔH1. NAC1/NAC2 are carbonyl-oxygen natural atomic charges; d1/d2 are OH···O distances.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Search solvation structures | QH4 + CH3OH | CONFLEX MMFF94s | >2500 conformers; 290 radical and 341 dianion conformers converged | Lowest-energy starting pairs | ev_doc_688d59e690b5_000320_9564d21e077a |
| 2 | Initial pair optimization | Lowest conformers | Gaussian 16 B3LYP/6-31+G(d) | Radical and dianion states | Optimized starting structures | ev_doc_688d59e690b5_000320_9564d21e077a |
| 3 | Refine and calculate thermochemistry | quinone, methanol, pairs | Gaussian 16 DFT | B3LYP/aug-cc-pVDZ; PCM CH3CN; 298.15 K; 1 atm | H, geometry | ev_doc_688d59e690b5_000320_9564d21e077a; ev_doc_688d59e690b5_000430_e93a28bdbb1c |
| 4 | Population analysis | refined wavefunctions | Gaussian natural population analysis | carbonyl O | NAC1/NAC2 | ev_doc_688d59e690b5_000430_e93a28bdbb1c |
| 5 | Derived descriptor | state enthalpies | arithmetic | ΔH_HB = ΔH2 − ΔH1 | ΔH_HB | ev_doc_688d59e690b5_000430_e93a28bdbb1c |
| 6 | Coordination trend | Q(CH3)4 with n=1–4 CH3OH | same DFT/PCM series | n increased systematically | multi-methanol trend | ev_doc_688d59e690b5_000430_e93a28bdbb1c |

## 4. Validation and analysis protocol

The authors compare calculated and experimental ΔH_HB (Figure S11), inspect Q(CH3)4 geometry (S12), redox-dependent distances (S13), distance-change correlation (S14), NAC correlation (Figure 3d), and n=1–4 methanol calculations (Figure 3e/S15).

## 5. Private reference results

SI Table S4 gives Q(CH3)4: ΔH1 −6.72, ΔH2 −11.8 kcal mol−1, NAC1 −0.758 e, NAC2 −0.973 e, d1 1.716 Å, d2 1.515 Å; hence ΔH_HB −5.08 kcal mol−1. The paper also estimates −20.8 kcal mol−1 for four methanols and reports α near −3.1 mV K−1, contextual only.

## 6. Limitations and interpretation boundaries

The SI has no machine-readable complex coordinates, so public inputs provide unambiguous isolated structures and require independent complex construction. Multiple minima and method sensitivity are possible. This calculation does not prove bulk solvation populations or thermocell stability.
