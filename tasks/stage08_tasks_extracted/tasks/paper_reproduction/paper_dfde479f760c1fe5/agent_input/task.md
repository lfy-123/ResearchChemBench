# Scientific objective

Quantify how the hydration state of the proton pathway changes chloride-ion permeation in the defined EcCLC system. Independently determine PMF profiles for both chain conditions, locate S_ext, S_cen and S_int, measure barriers from S_cen to each neighboring site, and use validated structural or hydration observables to explain the comparison. Generate and test your own explanations for any condition difference.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that hydration of the proton pathway lowers the free-energy barriers for chloride leaving the central binding site. They also relate chloride dissociation to widening and increased hydration of the proton pathway.

**Candidate route or mechanism.**
Prioritize comparison of chloride transport in the water-containing chain-A pathway with the water-depleted chain-B pathway, and consider coupling between central-site chloride occupancy, proton-pore hydration, and pore geometry as candidate explanations for the barrier difference. Treat these as proposed interpretations to test against the defined system.

**Discriminating evidence.**
Use condition-resolved PMF barriers and site valleys together with trajectory measurements of pore water occupancy, pore radius or geometry, chloride contacts, and relevant side-chain or proton-pathway conformational changes. A chloride-removal perturbation and its structural or hydration response can serve as additional evidence when feasible.

# Public inputs and scientific boundaries

Use every field in `data/inputs/system_definition.json` and retrieve PDB 1OTS only through the controlled PDB connector. The scored system is the defined EcCLC homodimer with chains A and B as separate permeation pathways, in the specified POPE membrane, TIP3P water, 0.2 M NaCl, protonation, temperature, pressure, coordinate convention and chain conditions. Report the model, force field, charge treatment, sampling strategy and all transformations from the public structure.

# Required scientific validation/investigation

Design and execute a finite, independently justified PMF investigation for both conditions, generating and deduplicating windows or equivalent sampling units across the complete S_ext–S_cen–S_int transport interval. Propose at least two plausible physical explanations for any condition difference, then discriminate them with submitted trajectory observables such as hydration, contacts, pore geometry or side-chain motion and state which explanation is supported or unresolved. Validate equilibration and PMF convergence quantitatively for each condition; bind every profile, window and diagnostic to its condition and coordinate range. Completion requires converged profiles in both conditions, resolved valleys and uncertainty-bearing barriers, or a scientifically bounded failure report. A bounded-failure submission may leave result arrays empty or partial but must identify the failed endpoint or validation and preserve attempted coverage and diagnostics. Stop after two successive convergence checks meet a predeclared change criterion, or at the declared resource/time boundary with coverage and limitations.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`, including the required status, provenance, condition definitions, profiles, site assignments, barriers, validation diagnostics and the mode-specific conclusion or explanations fields. Use the exact public condition IDs `chain_A_hydrated` and `chain_B_dehydrated`, and directions `S_cen_to_S_ext` and `S_cen_to_S_int`. A bounded-failure submission may leave result arrays empty or partial but must identify missing endpoints or failed validation and preserve all attempted results and limitations in `failure_details`; do not fabricate placeholders.
