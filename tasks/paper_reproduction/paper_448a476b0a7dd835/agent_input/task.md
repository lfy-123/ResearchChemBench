# Scientific objective

Determine the gas-phase interaction enthalpy of the neutral, closed-shell methyl-capped IIPO--oIPP artificial-base-pair model and establish whether the reported pairing geometry is a genuine minimum and compatible with the C1'--C1' proxy. Independently plan calculations that test the authors' qualitative hypothesis that a directional iodine halogen-bond arrangement can stabilize an approximately planar, strand-compatible pair. Do not assume any particular software, functional, basis, conformer, or execution order.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It uniquely defines one methyl-capped IIPO molecule and one methyl-capped oIPP molecule, each neutral and singlet, and their noncovalent gas-phase pair. The methyl cap is the sugar-attachment proxy; the scored distance is between the two cap carbon atoms. Include no solvent, counterions, phosphodiester backbone, stacking partner, or covalent bond between monomers. The target endpoint is ΔH = H(pair) − H(IIPO cap) − H(oIPP cap), with a clearly stated unit and energy convention.

# Required scientific validation/investigation

Generate and deduplicate plausible pair orientations/conformers, then advance candidates using a stated, reproducible criterion. Optimize the selected structures and validate a true minimum by a vibrational calculation with no imaginary frequencies, or report a technically justified alternative minimum-validation method. Compute the two monomers and pair consistently, document all methods and convergence settings, and calculate the cap-carbon distance and a quantitative planarity measure. The calculation is complete when the search rule has been exhausted, at least one validated pair minimum or a bounded failure has been reported, and the energy bookkeeping is reproducible. Stop after the declared search/validation rule is exhausted. If no validated minimum is found, report bounded failure with explored candidates, failed-validation evidence and limitations, and omit unavailable success-only quantities rather than inventing a result.

# Deliverables

Submit `report/results.json` and `report/validation.json`. For `complete`, results must identify the selected structure, ΔH, units, monomer/pair energies or thermochemical quantities, cap-carbon distance, planarity metric, and conclusion about the halogen-bond hypothesis. For `bounded_failure`, report explored candidates and evidence/limitations without unavailable success-only numbers or structures. Validation must retain candidate identities, search coverage, deduplication/advancement rule, minimum evidence, convergence, and all reasons for exclusions or failure. Include enough coordinates and provenance to reproduce the selected calculation when a structure is selected.
