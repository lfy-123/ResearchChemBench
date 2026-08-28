# Private paper route

## 1. Scientific objective and author claim

The paper surveys monolayer 2H transition-metal dichalcogenides and claims that magnetic order in Group-VB compounds produces spin-polarized valley physics. For VSe2 specifically, the authors report a ferromagnetic state and a SOC-induced K/K' valley splitting.

## 2. System and model boundary

The system is an isolated monolayer 2H-VSe2 slab: one V layer between two Se layers in a hexagonal primitive cell, with periodic in-plane boundary conditions and >16 Å out-of-plane vacuum. The electronic calculation is spin-polarized; the valley analysis is non-collinear and includes spin-orbit coupling.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and relax the monolayer | 2H MX2 prototype | VASP PAW DFT | PBE-GGA, Dudarev DFT+U, 500 eV cutoff, 7x7x1 Monkhorst-Pack mesh, energy 1e-6 eV and force 0.01 eV/A convergence, >16 Å vacuum, spin-polarized | Relaxed geometry and total energy | ev_doc_7f22f4278dd4_000026_5a65ad270e11; ev_doc_7f22f4278dd4_000035_19ff754cfb8f; ev_doc_7f22f4278dd4_000036_df7bd09310e7; ev_doc_7f22f4278dd4_000037_4b0ed7a36524 |
| 2 | Determine magnetic ground state | Relaxed compound | VASP spin-polarized calculations | FM, three AFM orders and NM state compared; compound-specific U | Lowest-energy magnetic order and metal moment | ev_doc_7f22f4278dd4_000026_5a65ad270e11; ev_doc_7f22f4278dd4_000040_dd25dea3a0f1 |
| 3 | Analyze valley response | Relaxed Group-VB monolayers | VASP non-collinear DFT+U+SOC | SOC enabled for VX2, NbX2 and TaX2 | K/K' valence-band energy difference | ev_doc_7f22f4278dd4_000174_2b62fd369f3c; ev_doc_7f22f4278dd4_000182_796e41302adc |

## 4. Validation and analysis protocol

The authors compare magnetic configurations, inspect spin-resolved bands, and define valley splitting as the energy difference between the valence-band maximum at K and K'. Their SI Table S1 reports the Group-VB SOC values. The main-paper Table 1 reports the relaxed VSe2 lattice constant, magnetic state and moment.

## 5. Private reference results

For VSe2, Table 1 gives a=3.31 Å, formation enthalpy -1.94 eV, FM order and a V moment of 1.29 μB. Table S1 gives ΔKK'=137 meV with SOC. These values are private evaluator references.

## 6. Limitations and interpretation boundaries

These are static DFT results, not finite-temperature magnetic or substrate-supported predictions. Agreement is method-dependent because the paper uses compound-specific U values and does not provide a complete public input archive. The benchmark therefore evaluates a reproducible independent calculation/reporting protocol and interprets differences within explicitly stated numerical and methodological uncertainty.
