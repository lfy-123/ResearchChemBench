# Scientific objective

Determine which chemically distinct bis-Mallory photocyclization mechanism(s) of neutral singlet precursor 1-cis best explain the experimentally observed exclusive formation of dibenzo[a,o]picene. Generate and discriminate plausible site-selective pathways using computation and report the evidence-supported conclusion.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that catalyst-free intramolecular photocyclization is influenced by site-dependent frontier-orbital density and phase, and that sequential oxidation and cyclization of favored intermediates can account for the observed selectivity.

**Candidate route or mechanism.**
Consider a sequential two-stage bis-Mallory process in which alternative first-stage bond-forming site/connectivity choices lead to corresponding oxidized or cyclized intermediates, followed by competing second-stage site/connectivity choices. The proposed route should remain a hypothesis to test; compare the chemically distinct alternatives rather than assuming any intermediate is preferred.

**Discriminating evidence.**
Use relative thermochemical comparisons for the mapped competing intermediates together with electronic or structural analyses at the reactive sites, such as frontier-orbital density and phase, and validate the stationary-point character of advanced structures. These calculations should be interpreted alongside the exclusive dibenzo[a,o]picene product boundary while separating thermodynamic and electronic support from direct photochemical or kinetic proof.

# Public inputs and scientific boundaries

`data/inputs/precursor_1_cis.xyz` is the SI Table S5 optimized Cartesian geometry of compound 1-cis: 52 atoms, C30H22, neutral charge, singlet multiplicity. Atom rows and coordinates define the identity/mapping; preserve them or document any unambiguous reindexing. The only experimental outcome supplied is exclusive isolation of dibenzo[a,o]picene from the bis-Mallory photocyclization. The required object is isolated-molecule computational mechanism/selectivity; explicit solvent, iodine, propylene oxide, crystal packing, excited-state dynamics, rates and device properties are outside scope unless labeled optional. Any proposed product/intermediate must have an explicit atom mapping to the precursor.

# Required scientific validation/investigation

State a finite, chemically justified rule that generates the first-stage and sequential second-stage site/connectivity hypotheses, and remove symmetry-equivalent duplicates. For each candidate retained for comparison, optimize with stated method, charge and multiplicity, validate its stationary-point character with frequencies or a justified alternative, and compute a consistent relative free-energy quantity with temperature/standard-state and conformer treatment. Seek at least one independent electronic or structural discriminator in addition to energy. Report generated, discarded, failed and unresolved candidates individually, with coverage. Completion requires exhaustive application of your stated chemically distinct candidate rule, or a bounded-failure report that names the missing space and its effect on the conclusion. Stop at that criterion and report remaining uncertainty; do not invent a discovery story or claim kinetic proof from thermochemistry alone.

# Deliverables

Submit `report/results.json` matching the schema. Include one candidate record for every generated chemically distinct channel, including candidates discarded before optimization, failed calculations, and unresolved candidates. Each record must state its scientific assignment (stage/connectivity and sequential continuation where applicable), atom mapping, advancement status, and candidate-specific calculation/validation evidence. Validated advanced candidates must report the comparable relative free energy, unit, and uncertainty; non-advanced, failed, or unresolved records must explain why those quantities are unavailable. Include the independent computational plan/provenance, discriminating evidence, final mechanism/selectivity conclusion, coverage and limitations. A bounded failure must contain the unresolved candidates and the scientific consequence; do not use fabricated placeholder numerical values.
