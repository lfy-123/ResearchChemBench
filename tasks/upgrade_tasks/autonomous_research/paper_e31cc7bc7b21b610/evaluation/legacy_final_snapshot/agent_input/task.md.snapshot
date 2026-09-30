# Scientific objective

Determine, from first-principles computational chemistry, whether the two supplied neutral singlet iridium complexes are gas-phase minima and compare their electronic energies. Identify which named structure is lower in energy under your consistently defined computational protocol, while distinguishing electronic-energy ordering from thermodynamic or kinetic claims.

# Public inputs and scientific boundaries

`data/inputs/cis_alpha_egan_IrCl.xyz` and `data/inputs/cis_beta_egan_IrCl.xyz` are complete 58-atom Cartesian XYZ definitions of two named cis-(egan)IrCl structures, with element identities and coordinates. These are source-provided isomer geometries for a fixed-object energy comparison, not a test of discovering the isomers. Both are neutral closed-shell singlets. The egan ligand is the hydrogen-substituted structure encoded in the files. The boundary is gas-phase electronic energies and stationary-point character; solvent, crystal packing, free energies, kinetics and barriers are excluded.

# Required scientific validation/investigation

Independently choose and report a defensible electronic-structure method, basis/ECP treatment, charge and multiplicity, convergence settings and software. Optimize each supplied structure and validate each final stationary point with harmonic frequencies or a justified equivalent. Report imaginary-frequency counts and signs for each named object. Calculate ΔE = E(cis-β) − E(cis-α) consistently in kcal/mol and state the lower-energy identity. Completion requires both endpoints and validation outcomes. Do not invent placeholder values if a calculation cannot be completed.

# Deliverables

Submit `report/results.json` conforming to the schema. Include method metadata, per-object energies and validation, ΔE, ordering, conclusion, enough provenance to reproduce the calculation. Do not claim solution-phase, kinetic or global-minimum conclusions from this task.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.

# Partial or unsuccessful submission

Use `status: "partial"` or `status: "bounded_failure"` when required calculations or analyses remain unavailable. Retain all actual partial results in their original fields. Include `failure` with a nonempty `reason`, a nonempty `missing_observables` array naming the unavailable result fields, and an `evidence` array of existing input, output or diagnostic paths (empty only if no artifact was produced). Explain which calculation failed or was not attempted; do not invent output files.

For these two statuses, the schema permits `null` for the specified unavailable calculated values, selected structures, state assignments or output paths. Keep the known molecular identities, charges, multiplicities, units and attempted methods. Report actual counts, including zero generated/validated candidates when appropriate. An unavailable frequency result is `null`, not zero imaginary modes or an empty list claiming a completed frequency analysis. A genuinely computed zero or an established empty imaginary-mode list remains valid evidence. A missing comparison is not a zero difference or zero RMSE.

Other statuses, and omission of status where the original schema permits it, retain the complete-result format. Passing this format check does not establish scientific completion: uncomputed endpoints receive no completion credit, and existing scientific rules still assess the actual evidence. This reporting branch does not change the scientific target, required successful investigation, or numerical acceptance criteria.
