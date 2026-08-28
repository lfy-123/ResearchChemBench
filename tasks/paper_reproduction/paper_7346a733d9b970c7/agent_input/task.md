# Scientific objective

Determine the C–H bond dissociation enthalpy (BDE) for the explicitly defined cyclohexane/cyclohexyl-radical pair. This is the hydrocarbon reference used to interpret whether catalyst-derived X–H formation is thermochemically competitive. The research object is the homolytic cleavage reaction cyclohexane → cyclohexyl radical + H atom; report the BDE in kcal/mol and explain what the value does and does not establish about HAT.

The paper's qualitative hypothesis is that a sufficiently strong catalyst-derived X–H bond could make hydrogen abstraction from a hydrocarbon thermochemically competitive, helping distinguish an N-centered from a weak S-centered HAT route. Test that motivation with the independent cyclohexane reference; the paper does not supply the outcome of this benchmark.

# Public inputs and scientific boundaries

`data/inputs/system.json` gives each species’ unique SMILES, formula, charge, multiplicity, role and coordinate file. The XYZ files are starting geometries, not answer-bearing structures; preserve their connectivity and generate chemically complete hydrogenated geometries before calculation. The boundary is gas-phase molecular enthalpy for the isolated species and the stated homolytic reaction. No paper, SI, database lookup or catalyst structure is needed. You may choose software, electronic structure method, solvation treatment, thermal convention and conformer protocol, but must disclose them and keep the same convention across the three species.

# Required scientific validation/investigation

Construct at least one chemically valid conformer for cyclohexane and the cyclohexyl radical, verify formula, connectivity, charge and doublet/singlet multiplicities, and calculate the H atom consistently. Optimize all non-atomic species and verify they are minima (or explicitly report an alternative validation with evidence). Evaluate the reaction enthalpy as H(cyclohexyl radical)+H(H atom)−H(cyclohexane), with units and thermal components stated. Completion requires energies for all three species, a reproducible formula and a numerical BDE or a bounded-failure report identifying which species/validation could not be completed. Stop after the stated conformer search is exhausted or after additional conformers no longer change the reported BDE beyond your chosen reporting precision; report coverage and limitations.

# Deliverables

Submit `report/results.json` conforming to the schema. Include method/settings, per-species energies and validation, the BDE, uncertainty/coverage, and a concise interpretation. A bounded failure is valid only when all attempted species, errors and next scientific limitation are documented; do not fabricate a number.
