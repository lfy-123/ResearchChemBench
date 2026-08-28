# Private paper route

## 1. Scientific objective and author claim

The paper studies why two structural isomers of a cyclometalated Ir(III)–salen NHC complex are formed in a temperature-dependent mixture. The authors claim that isomer 2 is thermodynamically favored, and that intramolecular π–π stacking contributes to its stabilization. Their DFT thermochemistry is used to connect the free-energy difference to the observed product distribution.

## 2. System and model boundary

The systems are neutral, closed-shell mononuclear Ir(III) complexes containing a tetradentate salen-derived ligand and a cyclometalated 1-phenyl-3-methylimidazol-2-ylidene NHC ligand. Complexes 1 and 2 are constitutional/coordination isomers distinguished by which salen donor is trans to the NHC carbene carbon. The computational boundary is the isolated molecular complex in implicit THF at 339 K; no explicit solvent, crystal lattice, counterion, or kinetic model is included.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain stationary-point geometries for both isomers | SI Cartesian coordinates for 1 and 2 | DFT geometry optimization in Gaussian16 | B3LYP/def2SVP | Optimized molecular geometries | ev_doc_6bb8b4064ec6_000068_a057b61ff83d; ev_doc_6bb8b4064ec6_000069_aae3271b04d8; ev_doc_6bb8b4064ec6_000074_3d76509bb981 |
| 2 | Evaluate solution-phase thermal free energies | Optimized geometries | Gaussian16 DFT frequency/thermochemistry with implicit solvation | B3LYP/def2SVP, SMD(THF), 339 K | G(1) and G(2) | ev_doc_3b795b2a7017_000040_9cae9280f020; ev_doc_6bb8b4064ec6_000068_a057b61ff83d |
| 3 | Convert the free-energy difference into an isomer population ratio | G(1), G(2) | Boltzmann calculation | ΔΔG(1–2), T = 339 K, R in consistent units | ΔΔG and [2]/[1] | ev_doc_3b795b2a7017_000040_9cae9280f020; ev_doc_3b795b2a7017_000042_f6cfeac28775 |

## 4. Validation and analysis protocol

The intended stationary points are minima, checked by the absence of imaginary vibrational frequencies. The authors compare the computed free-energy preference and Boltzmann population ratio with the experimental mixture ratio at 339 K. Structural and spectroscopic discussion assigns stabilization of 2 to intramolecular π–π interactions; the paper also reports that the optimized S0 geometry of 2 agrees closely with its crystal structure.

## 5. Private reference results

The paper reports G(1) = −2795.458950 hartree and G(2) = −2795.46003 hartree. It reports ΔΔG(1–2) = 2.84 kJ mol−1, a calculated [2]/[1] ratio of 2.74, and an observed yield ratio of 2.78 at 339 K. The qualitative conclusion is that 2 is thermodynamically favored and that intramolecular π–π stacking is a stabilizing factor.

## 6. Limitations and interpretation boundaries

The paper does not specify every optimization, frequency, charge/multiplicity, or standard-state detail. The benchmark therefore evaluates independently reported thermochemical observables and validation evidence, not bitwise reproduction of one Gaussian input. A small free-energy difference is method-sensitive; agreement with an experimental yield ratio does not establish a complete kinetic mechanism or prove that π–π stacking is the sole source of stabilization.
