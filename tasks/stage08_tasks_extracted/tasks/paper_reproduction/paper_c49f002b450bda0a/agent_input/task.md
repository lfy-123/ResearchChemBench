# Scientific objective

Determine the conformer-resolved aqueous relative Gibbs free-energy landscape at 298.15 K of the four specified stereoisomers of neutral 2-azidocyclohexan-1-ol. Establish whether the four states form any robust thermodynamic grouping or ordering, identify which named configurations occupy each group, and explain the scope of what that product-state result can support. No candidate grouping or expected direction is supplied.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the mixed-configuration products, (1S,2R) and (1R,2S), as unstable diastereomers and propose that their formation can be excluded on thermodynamic grounds. They report that quantum-chemical free-energy comparisons of dominant conformations were used to support this interpretation.

**Candidate route or mechanism.**
The proposed product-state explanation is that nucleophilic attack in cyclohexene-oxide ring opening leads preferentially to the RR/SS configuration class, while the SR/RS mixed-configuration class is disfavored because it corresponds to higher-energy diastereomeric products. Treat this as a candidate thermodynamic interpretation to test across independently generated conformers.

**Discriminating evidence.**
Compare the conformer-resolved aqueous free energies of the RR/SS and SR/RS classes, including their lowest validated minima, conformer populations or energy separations, achiral-pair symmetry, and sensitivity to conformer coverage or thermochemical treatment.

# Public inputs and scientific boundaries

Use `data/inputs/system.json` and `data/inputs/README.md`. They define the atom-mapped connectivity, absolute configurations RR, SS, SR, and RS, molecular formula C6H11N3O, total charge 0, singlet multiplicity, aqueous environment, and 298.15 K target temperature. Atom 1 is the hydroxyl-bearing carbon and atom 2 is the adjacent azide-bearing carbon. Treat each as an isolated neutral solute in an achiral aqueous model and generate all 3D conformers independently. Do not use or infer an enzyme structure, reaction path, transition state, rate, product ratio, or preferred stereochemical outcome. Choose and document a defensible electronic-structure, solvation, standard-state, and thermal model. No paper-specific computational route or result is a public input.

# Required scientific validation/investigation

For each named stereoisomer, generate a reproducible finite conformer set, verify the specified connectivity and absolute configuration, deduplicate equivalent structures, and report generation settings and counts. Define an energy-window or population-based advancement rule before high-level comparison, retain all candidates satisfying it, and report individual validation context for every advanced candidate. Optimize candidates and establish local-minimum character with harmonic frequencies or a justified equivalent. Use the same free-energy definition for all states, including aqueous treatment, 298.15 K thermal corrections, standard state, low-frequency handling, and any explicit solvent. Report each named stereoisomer's lowest conformer relative to the global minimum. Test achiral symmetry through RR versus SS and SR versus RS comparisons. Formulate plausible groupings from the calculated landscape and discriminate them using energy separations, conformer uncertainty, and at least one sensitivity check on coverage or model treatment. Completion requires a validated minimum for every stereoisomer, exhaustion of the advancement rule, a complete four-state ordering/grouping, and a sensitivity result showing whether the grouping is robust; stop then. If a predeclared resource bound is reached first, stop and explicitly identify unresolved states and refrain from a resolved grouping claim.

# Deliverables

Submit `report/results.json` matching `submission_schema.json`. Report the computational model and reproducibility settings; named RR, SS, SR, and RS free energies in kcal/mol, conformer coverage, and stationary-point validation; symmetry and sensitivity results; the complete ordering and independently inferred grouping; a final thermodynamic conclusion; and limitations on extrapolating isolated-product stability to reaction or enzyme selectivity.
