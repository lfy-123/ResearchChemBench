# Scientific objective

Test the qualitative author hypothesis that extending the aryl-conjugated hydrazone of a pyrazolone dye produces a frontier-orbital gap consistent with its long-wavelength optical absorption. For the uniquely supplied neutral compound 6a, independently choose and execute a defensible electronic-structure calculation, obtain gas-phase and implicit-chloroform HOMO/LUMO gaps, and compare the chloroform result with the supplied optical gap.

# Public inputs and scientific boundaries

Use `data/inputs/compound_6a.xyz`, which contains the complete 35-atom Cartesian structure of (4Z)-5-(trifluoromethyl)-4-{2-[biphenyl-4-yl]hydrazinylidene}-2,4-dihydro-3H-pyrazol-3-one, and `problem.json` (charge 0, multiplicity 1, chloroform, optical gap 2.42 eV). The object is one isolated molecule; no explicit solvent, aggregate, excited-state geometry, or reaction pathway is in scope. Do not use the paper or SI.

# Required scientific validation/investigation

Check atom count, charge, multiplicity and chemical identity before calculation. Optimize a ground-state geometry in gas phase and in an implicit chloroform model, then validate each reported endpoint with a frequency calculation or a clearly justified equivalent local-minimum test. Extract signed HOMO and LUMO energies and calculate Eg = ELUMO − EHOMO in eV. Compare the chloroform Eg with 2.42 eV, state the absolute deviation, and explain method/conformer limitations. Completion requires both environments, validation evidence, and all requested fields; stop after validated endpoints are obtained, or report bounded failure and the reason if a calculation cannot be completed.

# Deliverables

Submit `report/results.json` matching the schema, including method, structure check, validation evidence, gas/chloroform orbital values, comparison, conclusion and limitations. Include enough provenance (software/version, input settings, output filenames or hashes) for an independent audit.
