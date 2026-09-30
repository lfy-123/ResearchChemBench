# Private paper route

## 1. Scientific objective and author claim

The paper studies arene-fused o-carboranes and argues that the fusion mode and arene extension control frontier-orbital energies, the HOMO–LUMO gap, and the lowest singlet absorption. For compound 2a, the authors claim that the naphthyl-fused C–B architecture has a stabilized LUMO and a comparatively narrow gap; the lowest absorption is dominated by frontier-orbital excitation.

## 2. System and model boundary

The benchmark system is neutral C(1),B(3)-(naphthalene-1,8-diyl)-C(2)-phenyl-1,2-dicarba-closo-dodecaborane (2a), formula C18H20B10. The SI supplies 48 Cartesian atoms for the isolated molecule. The computational boundary is an isolated neutral singlet molecule in an implicit THF environment; no crystal packing, counterions, explicit solvent, or experimental spectrum is part of the calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain a ground-state geometry | SI Cartesian coordinates for 2a | Gaussian 09 DFT geometry optimization | B3LYP/6-31G(d,p), IEF-PCM, THF; neutral singlet | Optimized S0 geometry and orbital energies | ev_doc_0431af98d49d_000226_746b1233027f; ev_doc_0431af98d49d_000227_50ef2bf98784; ev_doc_0431af98d49d_000228_c95883c86fb1 |
| 2 | Compute vertical singlet excitations | Optimized 2a geometry | Gaussian 09 TD-DFT | B3LYP/6-31G(d,p)/IEF-PCM(THF) | Singlet excitation energies, wavelengths, oscillator strengths and configurations | ev_doc_0431af98d49d_000226_746b1233027f; ev_doc_0431af98d49d_000227_50ef2bf98784; ev_doc_0431af98d49d_000228_c95883c86fb1 |
| 3 | Interpret the lowest absorption | TD-DFT output | Orbital/configuration analysis | Inspect the lowest reported singlet and dominant orbital contributions | Frontier-gap and S0–S1 comparison | ev_doc_0431af98d49d_000241_8311803d5258; ev_doc_0596c27d90c1_000097_74552a84732c |

## 4. Validation and analysis protocol

The authors compare the calculated frontier gap and lowest singlet excitation against their reported values and inspect the dominant orbital contribution. The SI labels the 2a coordinate block and reports the low-lying singlet output; the article identifies the HOMO→LUMO contribution as the main part of the lowest-energy S0–S1 process. Interpretation is limited to this isolated-molecule/implicit-solvent model and should not be presented as a prediction of solid-state emission.

## 5. Private reference results

The main paper (PDF p.4) reports a 4.30 eV HOMO–LUMO gap for 2a. SI PDF p.22 explicitly labels Excited State 1 as S1 = 3.8591 eV (321.27 nm), f = 0.2308, with the 89→90 contribution 0.69587. This is the existing lowest-singlet scoring target. Excited State 2 is a different, higher root at 4.1762 eV (296.88 nm), f = 0.0087; it must not replace S1. The unusual printed orbital index in the S2 block is not interpreted or corrected here and is not part of the S1 reference. All values remain evaluator-private.

## 6. Limitations and interpretation boundaries

Independent software and model chemistry are allowed in the public task, so absolute agreement is not expected across methods. The evaluator therefore scores reported numerical observables with authored tolerances and separately checks geometry/convergence evidence, state identity, and frontier-transition interpretation. Atom labels in the SI are not exposed as a scored mapping beyond the supplied ordered coordinate list.
