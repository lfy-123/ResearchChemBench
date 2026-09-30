# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum chemistry to test whether the ionic liquid [C8MIm][NTf2] strengthens the association of 1,3,5-triformylbenzene (Tb) with p-phenylenediamine (Pa), supporting the proposed explanation for rapid, high-crystallinity TbPa-COF membrane formation. The reported interaction-energy change is from −16.5 to −95.2 kJ/mol.

## 2. System and model boundary

The molecular systems are isolated neutral Tb, neutral Pa, the neutral ion-pair representation of [C8MIm][NTf2], a 1:1 Tb·Pa complex, and a 1:1:1 C8-IL·Tb·Pa complex. The paper treats the complexes as molecular interaction models; solvent, periodicity, polymer growth and the macroscopic membrane are outside this DFT calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize every molecular/complex geometry | Tb, Pa, C8-IL and complexes | Gaussian 09 | B3LYP/6-311G(d); isolated-molecule model | optimized geometries | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 2 | Verify stationary points | optimized geometries | Gaussian 09 frequency calculation | no imaginary frequency required for local minima | frequency-validated minima | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 3 | Evaluate interaction energies | optimized monomers and complexes | Gaussian 09 | B3LYP-D3(BJ)/6-311G(d) | Tb·Pa and C8-IL·Tb·Pa binding energies | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 4 | Interpret noncovalent contacts | optimized wavefunctions | Multiwfn + VMD | Hirshfeld IGM, isosurface 0.001 a.u. | interaction-region visualization | ev_doc_5891573f19ff_000304_970872bd65a9 |
| 5 | Relate computation to mechanism | computed interaction strengthening plus experiments/MD | qualitative synthesis | IL ion/H-bond network and water encapsulation | mechanistic interpretation | ev_doc_5891573f19ff_000088_4ab34ceb2f98; ev_doc_5891573f19ff_000089_849b61cb66c0 |

## 4. Validation and analysis protocol

The authors optimized structures, used frequencies to identify local minima, then evaluated dispersion-corrected interaction energies. The interaction is interpreted together with IGM contact maps and the paper's WAXS/RDF/FT-IR and reverse-phase-microemulsion observations. The DFT result is a qualitative mechanistic support, not a direct calculation of a crystallization barrier.

## 5. Private reference results

The reported binding energies are −16.5 kJ/mol for Tb·Pa and −95.2 kJ/mol for C8-IL·Tb·Pa. Thus the ternary model is more strongly bound by 78.7 kJ/mol in the authors' calculation. The paper attributes the effect to orderly Tb prearrangement in the IL ion/H-bond network, while water encapsulation and acid-mediated kinetics contribute separately to rapid polymerization.

## 6. Limitations and interpretation boundaries

The paper does not publish a unique Cartesian starting geometry or a complete conformer ensemble. Interaction energies depend on the submitted conformer, charge treatment for the ion pair, and the chosen computational model. The reported values should therefore be compared as model-specific isolated-complex observables. They do not establish a unique transition state, a quantitative crystallization barrier, or causality independent of the experimental and MD evidence.
