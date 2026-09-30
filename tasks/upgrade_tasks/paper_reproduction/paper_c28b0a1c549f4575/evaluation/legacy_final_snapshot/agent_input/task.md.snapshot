# Scientific objective

Compute signed electronic binding energies for the explicitly named DED2_PC, TEA_PC and BF4_PC pairs and determine the DED2_PC versus TEA_PC ordering. The benchmark concerns isolated gas-phase ion–PC pairs, not bulk solvation free energies.

# Author-provided scientific guidance

Independently test the authors' qualitative hypothesis that the divalent DED2+ cation binds propylene carbonate (PC) more strongly than the monovalent TEA+ cation and can therefore compete for PC in a solvent-limited electrolyte.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It uniquely defines the four molecular graphs, formal charges, singlet multiplicities, atom-element lists, pair identities, and the binding-energy equation. You must generate 3-D starting geometries; the supplied connectivity is authoritative. PC is racemic/unspecified at its ring stereocenter, so do not claim an enantiopure result. Report kcal/mol, preserve the stated atom identities, and do not use the paper or general web as an input. No electrode, continuum-solvent, bulk concentration, or experimental value is part of the scored calculation.

# Required scientific validation/investigation

For each of the three named pairs, generate at least two chemically distinct initial ion–PC orientations, optimize the complex and both isolated components with a defensible electronic-structure method, and verify every retained minimum by frequencies or an equivalently justified minimum test. Deduplicate converged structures using a stated structural criterion, retain the identity and provenance of every candidate, and compute binding energies by explicit energy bookkeeping from the same component convention. Perform at least one sensitivity check (different conformer, orientation, dispersion treatment, basis, or validated alternative) and explain its effect on the DED2_PC/TEA_PC ordering. The investigation is complete when every named pair has at least one validated retained minimum, all reported energies are traceable to component calculations, and the sensitivity result is recorded.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` with the required schema. Include method and sign convention, per-pair candidate identity, energies and validation evidence, the cross-pair ordering, sensitivity outcome, and a concise source-independent scientific conclusion. A bounded-failure branch is allowed and must identify which pair or validation condition prevented completion.
