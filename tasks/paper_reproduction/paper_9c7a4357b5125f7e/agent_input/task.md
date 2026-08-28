# Scientific objective

Determine the Gibbs free-energy barrier, ΔG‡, for the first uncatalyzed acylation/nucleophilic-substitution event between neutral malonic acid and neutral acetic anhydride at 413.15 K in acetic-anhydride solvent. In reproduction mode, independently test the authors' qualitative hypothesis that this chemistry is a two-step substitution sequence involving six-membered-ring transition states; the hypothesis is not itself a supplied answer. Report the transition-state identity/geometry found, the reactant reference definition, ΔG‡ in kJ mol-1, and whether the proposed path is supported.

# Public inputs and scientific boundaries

The public input `data/inputs/system.json` uniquely defines malonic acid as `O=C(O)CC(=O)O` and acetic anhydride as `CC(=O)OC(=O)C`; both are neutral singlets. The solvent boundary is a continuum representation of acetic anhydride and the temperature is 413.15 K. The scored chemistry is the first uncatalyzed acylation event only; DMAP, later HAc removal, carbon-suboxide polymerization, and any paper coordinates are outside the scored system. You may generate conformers, complexes and 3-D geometries, but must state the reactant reference/standard state and any chemically consequential assumptions.

# Required scientific validation/investigation

Plan and execute an independent electronic-structure route without being required to copy the paper's software, functional, basis, solvent implementation or ordered protocol. Generate a finite, chemically justified set of reactant-complex and first-event TS candidates, deduplicate them by connectivity and geometry, and retain the candidate identities and screening evidence. A claimed TS must have one reaction-relevant imaginary frequency and an IRC (or a scientifically justified equivalent) connecting it to the stated reactant-side complex and acylated product-side state. Optimize/refine the accepted states consistently, calculate thermal free energies at 413.15 K, and report method and standard-state details. Completion requires either one validated first-event TS with a reproducible ΔG‡ or a bounded-failure report documenting all generated candidates, failed validation reasons, and the best defensible limitation. Stop when the candidate set is chemically exhausted under the stated generation rules and no new distinct candidate is produced, or when the bounded-failure resource/coverage limit is reached; report coverage and stopping rationale.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the selected candidate identity, reactant reference, barrier if obtained, method, validation evidence, candidate ledger, explicit generation/deduplication/coverage/stopping record, conclusion, and limitations. A bounded failure branch is valid only when it includes the required candidate ledger, validation attempts, search record and limitation statement; do not fabricate a numerical barrier or structure.
