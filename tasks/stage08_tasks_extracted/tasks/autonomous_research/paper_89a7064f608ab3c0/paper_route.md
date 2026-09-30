# Private paper route

## 1. Scientific objective and author claim

The authors use DFT to test an oxidative radical-cation cycloreversion of a BN-benzvalene derived from C5-aryl-1,2-azaborine 1a. They claim sequential C5-C6 then C3-C4 cleavage gives the C4-aryl product through Int-1 and Int-2, and that this route is favored over the alternative C3-C6 cleavage.

## 2. System and model boundary

The computed system is the 65-atom radical cation [2a]•+ (charge +1, doublet), its ring-opening intermediates and transition states, and C4/C5 product pathways. The reported thermochemistry is solution-phase Gibbs free energy at 298 K and 1 atm, with dichloromethane solvation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize minima and TSs and obtain frequencies | [2a]•+, Int-1, TS-1, TS-2, Int-2, 1a and alternative-path structures | Gaussian 16 | (U)B3LYP/6-31G(d); doublet radical cation; 298 K, 1 atm corrections | Optimized geometries, frequencies, thermochemical corrections | ev_doc_b9f9266bd61e_001121_0d08d88131e2; SI Cartesian Coordinates, pp. S82-S100 |
| 2 | Refine electronic energies in solvent | optimized structures | Gaussian 16 | ωB97XD/def2-TZVPP with SMD(CH2Cl2) | solvated electronic energies | ev_doc_b9f9266bd61e_001121_0d08d88131e2; ev_doc_ba00b377573c_000123_3faffad434ff |
| 3 | Assemble free-energy profile | energies and thermal corrections | Gaussian 16/post-processing | relative to [2a]•+ or Int-1 as appropriate | ΔG profile and barriers | ev_doc_ba00b377573c_000126_b69858994b24; ev_doc_ba00b377573c_000128_b47804542abb |

## 4. Validation and analysis protocol

Minima were checked by zero imaginary frequencies and transition states by one imaginary frequency; IRC/connectivity checks establish the adjacent states. Barriers are read relative to the immediately preceding minimum. The competing C3-C6 route is compared through its highest transition state. Spin-density and central C-C bond analysis support radical-cation localization.

## 5. Private reference results

The main paper reports ΔG‡([2a]•+→TS-1)=1.9 kcal/mol and ΔG‡(Int-1→TS-2)=4.6 kcal/mol. The C4 route is lower than the C5 alternative; the alternative TS-A is shown at 6.3 kcal/mol in Scheme S7. The authors describe the oxidative radical-cation pathway as consistent with the experimental C4 selectivity.

## 6. Limitations and interpretation boundaries

These are model-dependent computed free energies, not direct kinetic measurements. The public task does not expose the paper's optimized TS/intermediate geometries or protocol, so an agent must independently construct and validate them. Agreement is assessed within a declared evaluator tolerance and alongside frequency/connectivity evidence.
