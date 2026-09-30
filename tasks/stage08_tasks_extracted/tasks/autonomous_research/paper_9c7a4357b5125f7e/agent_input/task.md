# Scientific objective

Determine the Gibbs free-energy barrier, ΔG‡, for the first uncatalyzed acylation/nucleophilic-substitution event between neutral malonic acid and neutral acetic anhydride at 413.15 K in acetic-anhydride solvent. Independently formulate and discriminate plausible first-event reaction pathways, then report the validated transition-state identity/geometry, reactant reference definition and ΔG‡ in kJ mol-1. Do not assume that a particular mechanism, ring size or candidate is correct.

# Public inputs and scientific boundaries

The public input `data/inputs/system.json` uniquely defines malonic acid as `O=C(O)CC(=O)O` and acetic anhydride as `CC(=O)OC(=O)C`; both are neutral singlets. The scored system is the first uncatalyzed acylation event between these two molecules in a continuum representation of acetic anhydride at 413.15 K; do not add a catalyst or extend the modeled chemistry to subsequent reaction events. You may generate conformers, complexes and 3-D geometries, but must state the reactant reference/standard state and any chemically consequential assumptions.

# Required scientific validation/investigation

Propose plausible first-event pathways from the supplied reactants and define chemically meaningful candidate-generation rules. Generate a finite candidate set, deduplicate by connectivity and geometry, and retain each candidate's identity, screening evidence and reason for advancement or rejection. A claimed TS must have one reaction-relevant imaginary frequency and an IRC (or a scientifically justified equivalent) connecting it to the stated reactant-side complex and product-side state. Optimize/refine accepted states consistently, calculate thermal free energies at 413.15 K, and report method and standard-state details. Completion requires either one validated first-event TS with a reproducible ΔG‡ or a bounded-failure report documenting the explored pathways, candidates, failed validation reasons and best defensible limitation. Stop when the candidate set is chemically exhausted under the stated generation rules and no new distinct candidate is produced, or when the bounded-failure resource/coverage limit is reached; report coverage and stopping rationale.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include the candidate ledger, selected candidate identity, reactant reference, barrier if obtained, method, validation evidence, an explicit generation/deduplication/coverage/stopping record, conclusion and limitations. A bounded failure branch is valid only when it includes the schema-required candidate ledger, validation attempts, search record and limitation statement; do not fabricate a numerical barrier or structure.
