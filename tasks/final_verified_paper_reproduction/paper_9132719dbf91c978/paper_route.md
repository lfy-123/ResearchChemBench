# Private paper route

## 1. Scientific objective and author claim

The authors computationally analyze the photoinduced palladium-catalyzed denitrogenative cyclization of N-aroyl benzotriazoles. For the terminal hydrogen-evolution step, they claim that reductive elimination of H2 from palladium dihydride INT-G has a very small free-energy barrier and is compatible with regeneration of Pd(0).

## 2. System and model boundary

INT-G is the neutral singlet palladium dihydride complex in the SI Cartesian-coordinate appendix. The modeled endpoint is H2 release from this complex to the corresponding Pd(0) species. Energies are solution-phase free energies in DMAc; the authors use an optimized minimum and a transition state connected to the endpoint.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize structures and characterize stationary points | Mechanistic intermediates/TS guesses | Gaussian 16 A.03 | PBE0/def2-SVP with GD3-BJ; frequency analysis | Minima have 0 imaginary frequencies; TSs have 1 and connect endpoints | ev_doc_ad8d4ad88545_000195_afed2f27e96a |
| 2 | Refine energies in solvent | Step-1 geometries | Gaussian 16 A.03 | MN15/def2-TZVP single points with SMD DMAc | SCRF energies combined with thermal corrections | ev_doc_ad8d4ad88545_000195_afed2f27e96a |
| 3 | Analyze H2 evolution | INT-G and its reductive-elimination TS | Free-energy profile in Figure S4 | Compare the terminal reductive-elimination barrier and mechanistic alternatives | Small INT-G-to-H2 barrier; HAT is facile; silyl-radical path is favored over direct SET | ev_doc_ad8d4ad88545_000199_c59d4d6aeb1b |

## 4. Validation and analysis protocol

Stationary-point frequencies were used to distinguish minima and transition states, and the TS imaginary mode was required to connect the initial and final states. The authors compared silyl-radical generation with direct photoexcited-Pd/SET and catalyst-free alternatives; the latter alternatives were higher-energy or less plausible. The SI coordinate appendix identifies INT-G as a 0-imaginary-frequency, 0 1 structure.

## 5. Private reference results

The SI states that H2 evolution by reductive elimination from INT-G requires a free-energy barrier of 0.9 kcal/mol. The SI also states that INT-G is a minimum (Nimag = 0), that HAT to Pd(I)H is facile with a negative barrier, and that the silyl-radical-mediated path is more plausible than direct SET and catalyst-free paths.

## 6. Limitations and interpretation boundaries

This benchmark evaluates a terminal barrier and stationary-point validation, not a complete reproduction of every species in Figure S4. Differences in electronic-structure method, conformer choice, thermal convention, and TS search can shift the value; submissions must report those choices and any failure to locate a connected TS. The hidden reference is a paper/SI claim, not an assertion that the value is method-independent.
