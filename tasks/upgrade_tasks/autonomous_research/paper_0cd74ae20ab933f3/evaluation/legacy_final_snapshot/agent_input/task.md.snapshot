# Scientific objective

For the three explicitly identified neutral Cu2(AnCOO)4(4-RPy)2 molecular dimers (R = H, CH3, OCH3), independently determine the singlet–triplet exchange gap J (cm^-1), the triplet population at 300 K (%), and whether the substituent series exhibits a systematic relationship in the calculated coupling.

# Public inputs and scientific boundaries

Use J=ES−ET (negative for a lower singlet), in cm^-1. The triplet population at 300 K is 100×3 exp[J/(kBT)]/{1+3 exp[J/(kBT)]}; with J in cm^-1 use kB=0.69503476 cm^-1/K. The factor 3 is triplet spin degeneracy. For unambiguous scoring, the complete `systems` array contains exactly R_H, R_CH3, R_OCH3 in that order, once each. Put additional attempts separately. At least one methodological sensitivity check is required, not necessarily a new control for every derivative.

Use `data/inputs/model_systems.json`, which uniquely identifies the three derivatives, component SMILES, paddlewheel assembly, charge, reference triplet multiplicity, target states, and units. Construct 3-D geometries from the connectivity. The boundary is the isolated dimer, not the periodic MOF or experimental measurement. Define the J sign convention and the energy-to-population expression used.

# Required scientific validation/investigation

For each named system, generate and deduplicate at least one valid geometry, establish a triplet reference, and calculate the lowest singlet and triplet energies with a defensible open-shell method. Record convergence, spin/state identity, and any stability or frequency check. Perform at least one justified sensitivity check and explain why the three-system coverage is sufficient for the stated relationship (or state what cannot be inferred). Completion requires traceable results for all three systems; incomplete work uses a diagnostic failure record.

# Completion and allowed outcomes

Submit a successful result only when all three named systems have the requested gap and
population plus the required validation records and series interpretation. If a system or the
sensitivity check cannot be completed after the attempted scope, submit the bounded-failure
branch with the covered systems, attempted calculations, diagnostics, and the specific missing
result; do not invent numeric values or placeholder structures.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` with per-system identity, geometry provenance, J, 300 K population, units, method, validation (including sign convention and population expression), coverage/status, and conclusion. A bounded-failure branch is valid only with attempted scope and diagnostics.
