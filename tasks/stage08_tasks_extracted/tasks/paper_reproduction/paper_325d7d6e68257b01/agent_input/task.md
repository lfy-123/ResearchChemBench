# Scientific objective

Independently determine buffer insertion free energies for H3BO3 and Tris at the defined Ce6-MOF-808 truncated node in oxidized and singly reduced states, and calculate reduced-minus-oxidized shifts. Explain what the computed thermodynamics imply within the stated model boundary.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that buffer coordination at the Ce6 node differs between oxidation states and that these oxidation-state-dependent thermodynamic changes can contribute to direction-dependent proton-coupled electron-transfer kinetics. This is a qualitative interpretation to test with the requested insertion free energies.

**Candidate route or mechanism.**
A candidate comparison is insertion of either H3BO3 or Tris at a terminal aqua ligand, evaluated for the oxidized node and for the singly reduced, protonated node. Comparing each buffer's binding thermodynamics across those states provides the proposed route for assessing whether oxidation-state-dependent coordination could distinguish the buffers.

**Discriminating evidence.**
Use a consistent bound-versus-separated thermochemical free-energy cycle for all four systems, together with converged optimized structures, frequency validation of accepted minima, atom and charge bookkeeping, and reduced-state spin localization and protonation. Alternative sites or conformers should be recorded and deduplicated so the comparison tests the proposed state-dependent coordination rather than an untracked structural choice.

# Public inputs and scientific boundaries

Use only `data/inputs/bare_node.xyz`, `boric_acid.smi`, `tris.smi`, and `problem_definition.json`. The node, buffer identities, oxidation states, protonation, binding operation, solvent, observable, units, and charge/spin conventions are explicitly defined there. The scored system is the isolated molecule represented by the supplied truncated node and buffer species; do not add a host or solvent beyond the stated model.

# Required scientific validation/investigation

Compute four named systems, recording any alternative sites/conformers and deduplicating them by connectivity and geometry. Optimize bound and separated species, form a consistent free-energy cycle, verify convergence and atom/charge bookkeeping, frequency-check accepted minima, and report reduced-state spin localization and protonation. Generate and test your own explanations for differences between buffers and oxidation states. Completion is all four systems with reproducible values, or a bounded failure report retaining all identities, diagnostics, coverage, and limitations. Stop at that point.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`, including the schema-required `status`, `method_summary`, four `systems`, `delta_delta_g_kcal_mol`, `coverage`, `limitations`, and `conclusion`. Include state/buffer values, methods, validation evidence, and artifacts as permitted by that schema. Bounded failure must use null numeric fields plus diagnostics rather than fabricated numbers.
