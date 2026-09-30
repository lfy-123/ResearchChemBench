# Scientific objective

Independently determine the gas-phase interaction enthalpy of the neutral, closed-shell methyl-capped IIPO--oIPP artificial-base-pair model and test whether a validated pairing geometry is compatible with the C1'--C1' proxy. Formulate and discriminate plausible explanations for any stable geometry or failure; generate and test your own explanations or pathways without presuming an author route.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that a directional iodine halogen-bond arrangement can stabilize an approximately planar pair while keeping the methyl-cap separation compatible with a strand-like geometry. Their interpretation is that the iodine-containing IIPO--oIPP motif is a promising intrinsic gas-phase pair; this is a qualitative claim to test computationally.

**Candidate route or mechanism.**
Prioritize testing a coplanar IIPO--oIPP arrangement featuring directional iodine interactions with acceptor sites on the partner, while also considering alternative orientations and the corresponding bromine analogue and carbonyl-oxygen-to-sulfur substitutions as comparisons. Assess whether these candidates retain planarity and the cap-carbon compatibility proxy after optimization.

**Discriminating evidence.**
Useful evidence includes optimized geometries and vibrational minimum checks, interaction enthalpies, cap-carbon distance and quantitative planarity, together with electronic-structure analyses such as charge-transfer descriptors, noncovalent-interaction maps or electrostatic potentials, and decomposition of pair interaction components. Compare iodine and bromine and oxygen/sulfur variants to distinguish directional halogen bonding from generic dispersion, electrostatics, or distortion effects.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It uniquely defines one methyl-capped IIPO molecule and one methyl-capped oIPP molecule, each neutral and singlet, and their noncovalent gas-phase pair. The methyl cap is the sugar-attachment proxy; the scored distance is between the two cap carbon atoms. The scored system is the isolated molecule pair; do not add solvent, counterions, phosphodiester backbone, stacking partner, or a covalent bond between monomers. The target endpoint is ΔH = H(pair) − H(IIPO cap) − H(oIPP cap), with a clearly stated unit and energy convention.

# Required scientific validation/investigation

Generate and deduplicate plausible pair orientations/conformers without assuming a preferred interaction motif. Advance candidates using an explicit reproducible criterion, validate optimized minima by frequencies or a justified alternative, and compute monomers and pair consistently. Report cap-carbon distance, planarity, interaction contacts, and competing explanations supported by your calculations. Completion requires exhaustion of the declared search rule and at least one validated minimum or a bounded failure report. Stop when the search rule and validation tests are exhausted. If the structure or endpoint cannot be established, report bounded failure with candidate-level evidence and limitations and omit unavailable success-only quantities rather than inventing them.

# Deliverables

Submit `report/results.json` and `report/validation.json`. For `complete`, results must identify candidates and the selected structure, ΔH and units, monomer/pair energies or thermochemical quantities, cap-carbon distance, planarity metric, and the evidence-based conclusion. For `bounded_failure`, report candidates, evidence and limitations without unavailable success-only numbers or structures. Validation must retain candidate identities, search coverage, deduplication/advancement rule, minimum evidence, convergence, alternative hypotheses considered, and reasons for exclusions or failure. Include coordinates and provenance sufficient to reproduce the selected calculation when one is selected.
