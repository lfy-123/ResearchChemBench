# Scientific objective

Determine computationally whether the two supplied protonated piperidine molecules exhibit a reproducible conformational/ electronic signature associated with a close intramolecular N–H+···O contact, by comparing their named chair-like and twist-boat-like starting structures. Quantify optimized relative energies within each molecule, the NH+ proton chemical shift relative to TMS (or a documented equivalent), and the closest NH+···O distance. Do not assume a mechanism or preferred conformer in advance; infer the conclusion from the calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that charge-assisted intramolecular hydrogen bonding may explain unusual NH+ chemical shifts in trans protonated piperidines 11 (4-hydroxy) and 12 (4-methoxy). They specifically associate the effect with a conformationally enabled close contact between the ammonium N–H donor and the pendant oxygen acceptor.

**Candidate route or mechanism.**
Their candidate explanation is that the twist-boat arrangement brings N–H+ and the pendant oxygen into close proximity, potentially making this interaction more favorable than in the corresponding equatorial chair arrangement. The comparison should therefore examine both conformational preference and the linked geometric and shielding changes for each compound.

**Discriminating evidence.**
Useful tests include optimized relative energies and frequency-confirmed minima, the closest N–H+···O distance, proton shielding converted with a TMS reference, and (if calculated) an oxygen charge or related electronic descriptor. These observables should be assessed together while keeping the isolated gas-phase cation boundary explicit.

# Public inputs and scientific boundaries

`data/inputs/11_eq_protonated.xyz`, `11__twist_boat_protonated.xyz`, `12_eq_protonated.xyz`, and `12__twist_boat_protonated.xyz` are the complete Cartesian XYZ inputs from SI pages S118–S121. They are isolated cations with charge +1 and singlet multiplicity; atom order and coordinates are authoritative. Molecule 11 has a hydroxy oxygen and molecule 12 a methoxy oxygen. No counterions, solvent molecules, paper computational settings, reference values, or expected ordering are supplied. The boundary is the gas-phase electronic structure of these four fixed cations; optional extra conformers are exploratory and cannot replace the named comparison.

# Required scientific validation/investigation

Select and justify a reproducible method for optimization, frequency validation, and proton shielding. Apply identical settings to all four named inputs. Retain a structure as a validated minimum only when optimization convergence is documented and its frequency analysis has zero imaginary frequencies; report bounded failure otherwise. Define molecule-specific relative-energy zeros explicitly, identify the N–H+ and pendant O atoms unambiguously, state the shielding reference, and report the closest N–H+···O distance. If additional conformers or sensitivity calculations are run, define how they were generated, deduplicated, and used, and report coverage; stop when all four named structures and any declared sensitivity set are complete. A conclusion must distinguish computed gas-phase evidence from claims about solution behavior.

# Submission contract and completeness

The `structures` array must contain exactly four objects, one and only one for each literal ID
`11_eq_protonated`, `11__twist_boat_protonated`, `12_eq_protonated`, and
`12__twist_boat_protonated`; do not substitute labels or duplicate an ID. A bounded failure is
reported on the affected object with null unavailable observables and a specific reason, while
the other objects remain fully reported. A paired comparison is null only when its pair cannot
be validly compared, with that reason stated in the conclusion or validation evidence.

# Deliverables

Write `report/results.json` conforming to the submission schema, with structure-level identities, optimization and frequency validation, energies/relative energies, atom selectors, distances, shielding/chemical shift or truthful unavailable status, comparison summaries, conclusion, and limitations. Write `report/method.md` with the independent method choice, settings, convergence, validation, referencing, optional-search coverage, and failure handling.
