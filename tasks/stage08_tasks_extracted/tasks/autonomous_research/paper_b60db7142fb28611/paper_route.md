# Private paper route

## 1. Scientific objective and author claim

The paper studies the CuAAC reaction of 4-(prop-2-yn-1-yloxy)benzaldehyde (2) with 3-azido-1H-1,2,4-triazole (3), for which four adducts are possible. The authors claim that Pdt2 is both the thermodynamically most stable adduct and the kinetically preferred pathway.

## 2. System and model boundary

The computational system is the neutral closed-shell organic reaction system, treated in the gas phase as isolated molecules. The authors report four product adducts, their optimized stationary points and thermodynamic quantities, and four corresponding transition states. Their model boundary does not include explicit Cu, solvent, counterions, or entropic treatment beyond the frequency calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize four possible adducts | Four product connectivities from the alkyne/azide reaction | Gaussian 09, DFT | B3LYP/6-311G(d,p) | Optimized product geometries and energies | ev_doc_bf7dc1235aa4_000062_349f1bd0ecc5; ev_doc_bf7dc1235aa4_000063_ded867fd0aeb; ev_doc_bf7dc1235aa4_000150_35ff8c61e016 |
| 2 | Verify minima and obtain thermodynamic corrections | Optimized adducts | Gaussian 09 frequency calculation | Same model chemistry | ZPVE, enthalpy, Gibbs free energy, frequencies | ev_doc_bf7dc1235aa4_000064_55cb819cb8d5; ev_doc_bf7dc1235aa4_000150_35ff8c61e016 |
| 3 | Locate pathway transition states | Reactant and product structures for each pathway | Gaussian 09 QST3 | B3LYP/6-311G(d,p) | Four TS structures and activation energies | ev_doc_bf7dc1235aa4_000065_8cfdc807d089; ev_doc_bf7dc1235aa4_000066_d25863aa6365 |
| 4 | Compare kinetic and thermodynamic preference | Validated stationary points | Relative comparison of calculated quantities | Activation energies in kcal/mol; product relative energies | Ordering and mechanistic interpretation | ev_doc_bf7dc1235aa4_000066_d25863aa6365; ev_doc_bf7dc1235aa4_000152_06401204bc7b |

## 4. Validation and analysis protocol

The authors identify minima by requiring only positive vibrational frequencies and transition states by requiring one imaginary frequency. They compare product electronic/thermodynamic quantities and transition-state activation energies across the four adduct pathways.

## 5. Private reference results

The reported thermodynamic ordering is Pdt2 > Pdt1 > Pdt3 > Pdt4, with Pdt1 1.3627 kcal/mol above Pdt2 in corrected relative energy. Reported activation energies are Pdt2 15.1815, Pdt1 16.4327, Pdt3 24.0031, and Pdt4 22.4967 kcal/mol. The reported conclusion is that Pdt2 is favored both kinetically and thermodynamically.

## 6. Limitations and interpretation boundaries

These are gas-phase, single-level DFT/QST3 results and do not establish solution-phase free energies or a full copper-mediated catalytic mechanism. The paper does not provide machine-readable Cartesian coordinates or exhaustive conformer/TS searches. Comparisons therefore concern the four defined connectivity classes and the submitted investigation's stated conformer coverage.
