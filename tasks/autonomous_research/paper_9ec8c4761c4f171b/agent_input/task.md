# Scientific objective

For the uniquely supplied neutral compound 6a, independently determine whether a validated ground-state frontier-orbital calculation gives a chloroform HOMO–LUMO gap consistent with the measured optical gap. Report gas-phase and implicit-chloroform HOMO/LUMO energies, gaps, and the quantitative comparison.

# Public inputs and scientific boundaries

Use `data/inputs/compound_6a.xyz`, the complete 35-atom Cartesian structure of (4Z)-5-(trifluoromethyl)-4-{2-[biphenyl-4-yl]hydrazinylidene}-2,4-dihydro-3H-pyrazol-3-one, and `problem.json` (charge 0, multiplicity 1, chloroform, optical gap 2.42 eV). The object is one isolated molecule; no explicit solvent, aggregate, excited-state geometry, or reaction pathway is in scope. Do not use the paper or SI.

# Required scientific validation/investigation

Verify atom count, charge, multiplicity and identity. Select a defensible electronic-structure method without assuming a prescribed protocol. Optimize gas-phase and implicit-chloroform ground states and validate each reported endpoint with frequencies or a justified equivalent local-minimum test. Extract signed HOMO/LUMO energies and calculate Eg = ELUMO − EHOMO in eV. Compare the chloroform gap with 2.42 eV and report absolute deviation plus sensitivity/limitations. Completion is two validated environments and complete provenance; stop then, or report bounded failure with its cause.

# Deliverables

Submit `report/results.json` matching the schema, with structure checks, validation evidence, method/provenance, both orbital-gap results, comparison, conclusion and limitations.
