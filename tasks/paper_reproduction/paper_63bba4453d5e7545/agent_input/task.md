# Scientific objective

Independently test the authors' qualitative hypothesis that a twist-boat arrangement of the trans protonated piperidines 11 and 12 can place the ammonium N–H donor near the pendant oxygen acceptor and account for their unusual NH+ NMR behavior. For each supplied structure, calculate a validated optimized geometry, relative conformer energies within each compound, the NH+ proton chemical shift relative to TMS (or an explicitly documented equivalent referencing procedure), and the closest NH+···O distance. The scored objects are explicitly named by the input filenames.

# Public inputs and scientific boundaries

`data/inputs/11_eq_protonated.xyz`, `11__twist_boat_protonated.xyz`, `12_eq_protonated.xyz`, and `12__twist_boat_protonated.xyz` are Cartesian XYZ geometries extracted from SI pages S118–S121. They are isolated protonated cations with charge +1 and singlet multiplicity; atom order and coordinates are authoritative. The 11 structures contain the 4-hydroxy substituent and the 12 structures the 4-methoxy substituent. No counterion, solvent molecule, experimental result, target value, paper method, or winning conformer is public. The model boundary is gas-phase electronic structure of these four fixed cations. You may generate additional conformers only as a robustness check; the four named inputs remain the scored comparison.

# Required scientific validation/investigation

Choose and justify a computational method capable of geometry optimization, harmonic frequencies, and proton shielding. Optimize all four named structures with identical settings, and verify each retained structure as a local minimum by reporting the number of imaginary frequencies. Define the energy zero separately for 11 and 12 as the lower of that molecule's two optimized structures, and report both relative energies. Identify the N–H+ proton and the pendant O by atom identity/indices, state the shielding-to-shift reference, and report the closest N–H+···O distance. Provide convergence evidence and discuss method, conformer, gas-phase, and referencing limitations. Completion requires all four structures to have a documented optimization outcome and either a validated minimum plus observables or a clearly bounded failure record; stop after the four named structures and any explicitly justified robustness checks are complete.

# Submission contract and completeness

The `structures` array must contain exactly four objects, one and only one for each literal ID
`11_eq_protonated`, `11__twist_boat_protonated`, `12_eq_protonated`, and
`12__twist_boat_protonated`; do not substitute labels or duplicate an ID. A bounded failure is
reported on the affected object with null unavailable observables and a specific reason, while
the other objects remain fully reported. A paired comparison is null only when its pair cannot
be validly compared, with that reason stated in the conclusion or validation evidence.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include per-structure identity, optimization status, imaginary-frequency count, total energy, relative energy, N–H+ and O atom selectors, N–H+···O distance, shielding and referenced chemical shift (or a declared unavailable status with reason), and validation evidence. Include a comparison table, a conclusion about whether the conformational comparison supports the stated qualitative hypothesis, and limitations. Also provide `report/method.md` describing software, method, settings, convergence, referencing, and any failed or additional calculations.
