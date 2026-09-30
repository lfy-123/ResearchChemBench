# Scientific objective

Independently determine and validate the relative Gibbs free-energy profile and mechanistic explanation for conversion of the supplied cal-1 polyene model to cal-5 in the explicitly defined reagent pool cal-1 + 2 mCPBA + HOAc + H2O + HO−. Discover and discriminate chemically plausible epoxidation, epoxide-opening, cyclization and competing branch pathways, reporting stationary-point identities, relative Gibbs energies, activated barriers, barrierless steps and stereochemical outcomes.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that conversion proceeds through two consecutive epoxidation/epoxide-opening cascades, with acid-promoted SN1-type epoxide opening followed by intramolecular capture. They regard this cascade as the preferred explanation for formation of the fused furofuran framework in the cal-1 model.

**Candidate route or mechanism.**
Examine the proposed sequence of two epoxidations followed by acid-promoted epoxide openings and intramolecular O–C capture steps, including the stereochemical alternatives of the first closure. Compare it with a sequential-epoxidation route in which epoxide opening proceeds by an SN2-type alternative.

**Discriminating evidence.**
Use optimized and frequency-validated minima and first-order saddle points with connectivity evidence, together with conformer-aware scans of each intramolecular O–C closure, to distinguish activated from barrierless capture and to compare the competing branches and stereochemical outcomes.

# Public inputs and scientific boundaries

The only molecular structure input is `data/inputs/cal-1.xyz`: 52 atoms, neutral charge, singlet multiplicity, Cartesian coordinates in Å. Treat atom identities and coordinates as fixed; do not infer omitted stereochemistry or change protonation. The common reference pool is cal-1 + 2 mCPBA + HOAc + H2O + HO−. The research object is the isolated molecular model in implicit aqueous environment; enzyme protein, explicit solvent and QM/MM effects are outside scope. Report Gibbs energies relative to the common pool in kcal/mol at approximately 298 K. No author mechanism, candidate ranking or target structure is provided; propose plausible explanations from the supplied chemistry and discriminate them computationally.

# Required scientific validation/investigation

Define a finite candidate-generation strategy for reaction branches and conformers, preserve unique connectivity/stereochemistry for every candidate, deduplicate, and state advancement criteria. Search enough plausible epoxidation, ring-opening, cyclization and alternative pathways to support a coverage claim. For every reported minimum, provide optimization/frequency or equivalent local-minimum validation; for every reported transition state, provide a first-order saddle criterion and connectivity evidence (IRC, endpoint following, or justified equivalent). Establish whether each investigated closure is activated or barrierless using a reported scan or other direct evidence. Assemble a common-pool relative Gibbs profile, compare competing explanations, report failed searches and unresolved alternatives, and explain how the result bears on the mechanism. Completion requires either a validated profile covering every chemically distinct branch in the declared search scope with an explicit coverage statement, or a bounded-failure report naming missing states and why no stronger conclusion is justified. Stop when the declared branch/conformer search is saturated under its stated criteria, or computational limits prevent this; document the limitation and stopping evidence.

# Deliverables

Submit `report/results.json` plus supporting files referenced by it (coordinate files, logs, frequency/IRC or scan evidence, and scripts where used). JSON must state status (`complete` or `bounded_failure`), model/reference definition, candidate records with unique identity and validation context, relative Gibbs energies and barriers with units, proposed/discriminated mechanisms, stereochemical outcomes, search scope/coverage/stopping statement, and limitations. A bounded failure must include all successfully validated candidates and a scientifically specific explanation of what remains unresolved; do not fabricate missing energies.

Use 1-based atom indices from the supplied XYZ, together with an explicit connectivity and stereochemical description, to identify every minimum, saddle, and branch; paper-internal labels alone are not sufficient. For every profile edge give source and destination candidate IDs, its activated/barrierless classification, and supporting scan, frequency, or connectivity evidence. State the common-pool definition and charge/multiplicity in the result. Compare at least two chemically distinct hypotheses when the declared search finds such alternatives; if none exists, explain why direct computation is the appropriate test. A bounded-failure report omits unresolved numerical values and structures rather than using placeholders.
