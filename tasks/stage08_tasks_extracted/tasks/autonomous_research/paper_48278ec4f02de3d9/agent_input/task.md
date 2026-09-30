# Scientific objective

Independently determine the kinetically controlling reaction mechanism for the Rh-catalyzed transformation of the explicitly supplied oxygen-bridged keto-VCP model substrate 1t, using the supplied Rh catalyst and CO as optional reactant. Generate and test your own chemically plausible mechanistic hypotheses and candidate pathways from computed Gibbs free-energy surfaces. Report the best-supported pathway and its key barriers without assuming any literature mechanism.

# Public inputs and scientific boundaries

`data/inputs/substrate_1t.xyz` is neutral singlet (23 atoms) substrate 1t, (E)-1-((3-cyclopropylallyl)oxy)propan-2-one, with atom identities and Cartesian coordinates supplied. `catalyst.xyz` is the neutral singlet [Rh(CO)2Cl]2 starting complex (8 atoms). `co.xyz` is neutral singlet carbon monoxide. These files uniquely define the molecular system; do not infer any paper atom labels or structures. The scored system is the isolated molecular system defined by these inputs; do not add a host or solvent. The measured quantities are relative Gibbs free energies and activation free energies in kcal/mol, referenced to a stated separated-reactant convention. No experimental rate prediction is required.

# Required scientific validation/investigation

Propose explicit hypotheses before candidate generation, then generate a finite candidate set spanning chemically plausible alternatives supported by the supplied system, preserving candidate IDs and connectivity. Deduplicate structures, advance candidates only when optimization and frequency/endpoint evidence supports the assigned state, and report failed searches rather than silently dropping them. Validate each scored transition state by one imaginary mode plus IRC or an equivalent bidirectional endpoint test; validate minima by zero imaginary frequencies or explain an alternative. Use consistent energy referencing, thermal and standard-state conventions, and report conformer coverage. Completion requires at least one validated pathway or a scientifically documented null result for each investigated alternative, plus a discriminating conclusion. Stop when additional searches yield no new connectivity or transition-state class under the stated generation strategy, and report the stopping rule and remaining limitations.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include hypotheses, candidate structures/IDs, validation evidence, methods, relative Gibbs energies and barriers, search coverage, failed attempts, uncertainty/limitations, and a final mechanism conclusion. The bounded-failure branch must still contain the candidate ledger and validation records; a status string alone is not sufficient. Ensure the result conforms to the local `submission_schema.json`, including all required keys for this mode.
