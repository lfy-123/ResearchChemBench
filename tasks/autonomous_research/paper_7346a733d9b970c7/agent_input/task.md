# Scientific objective

Compute and interpret the homolytic C–H bond dissociation enthalpy of the explicitly defined cyclohexane/cyclohexyl-radical pair. Report the BDE in kcal/mol and assess whether the calculation is adequate as a thermochemical reference for HAT studies, while separating energetic evidence from kinetic or mechanistic claims.

# Public inputs and scientific boundaries

`data/inputs/system.json` provides unique SMILES, formulas, charges, multiplicities, roles and starting XYZ files for cyclohexane, cyclohexyl radical and an H atom. The XYZ files are starting geometries; the SMILES and formulas define the complete scientific identity. The boundary is the isolated-species homolytic reaction and its molecular enthalpy. Choose and justify the computational method, thermal convention, conformer coverage and validation; do not assume a paper-specific route or answer.

# Required scientific validation/investigation

Generate chemically valid structures from the supplied identities, optimize the closed-shell and radical species, and validate minima or clearly document an alternative. Compute H(cyclohexyl radical)+H(H atom)−H(cyclohexane) consistently in kcal/mol. Report conformer generation, deduplication and coverage; stop when the explored conformers are exhausted under your stated rule or the BDE is stable to the stated reporting precision. Completion requires all three energies and a reproducible BDE, or a bounded-failure report with attempted calculations, diagnostics and limitation. Explain how your result supports only thermochemical comparison, not a full catalytic mechanism.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the independent protocol, species-level energies and validation, BDE, coverage/uncertainty, conclusion and limitations. If computation cannot be completed, use the schema’s bounded-failure branch and provide truthful diagnostics.
