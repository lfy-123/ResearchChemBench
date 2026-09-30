# Scientific objective

Determine, from first-principles computational chemistry, whether the two supplied neutral singlet iridium complexes are gas-phase minima and compare their electronic energies. Identify which named structure is lower in energy under your consistently defined computational protocol, while distinguishing electronic-energy ordering from thermodynamic or kinetic claims.

# Public inputs and scientific boundaries

`data/inputs/cis_alpha_egan_IrCl.xyz` and `data/inputs/cis_beta_egan_IrCl.xyz` are complete Cartesian XYZ definitions of two named cis-(egan)IrCl structures, with element identities and coordinates. Both are neutral closed-shell singlets. The egan ligand is the hydrogen-substituted structure encoded in the files. The scored system is each isolated molecule in the gas phase; do not add a host, solvent, counterion, or crystal environment. The observables are electronic energies and stationary-point character, not free energies, kinetics, or barriers.

# Required scientific validation/investigation

Independently choose and report a defensible electronic-structure method, basis/ECP treatment, charge and multiplicity, convergence settings, and software. Optimize each supplied structure and validate each final stationary point with harmonic frequencies or a justified equivalent. Report imaginary-frequency counts and signs for each named object. Calculate ΔE = E(cis-β) − E(cis-α) consistently in kcal/mol and state the lower-energy identity. Generate and test your own computational explanation for any observed ordering without assuming a particular interconversion pathway. Completion requires both endpoints and validation outcomes. Stop when both named structures have been optimized and validated; no additional structure or pathway search is required because the objects are fixed. Do not invent placeholder values if a calculation cannot be completed.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include method metadata, per-object energies and validation, ΔE, ordering, conclusion, uncertainty/limitations and enough provenance to reproduce the calculation. Do not claim solution-phase, kinetic or global-minimum conclusions from this task.
