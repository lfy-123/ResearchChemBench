# Scientific objective

Determine the character of the lowest singlet excitation S1 in four specified phenanthrimidazole molecules, and how Me/CF3 substitution and introduction of spirofluorene change local-excitation (LE) and charge-transfer (CT) contributions. Use optimized geometry and frontier orbitals as supporting evidence, and same-state NTO and interfragment charge-transfer analysis as the primary evidence. Allow the calculations to support, qualify or reject the proposed relationships.

# Public inputs and scientific boundaries

Use all four identities in `data/inputs/compound_definitions.json`: MeAC, TfAC, MeACFy and TfACFy, isolated neutral singlets. The mapped molecular graphs define connectivity and measurement selectors. Generate geometries independently and map those labels to the atom order of your own outputs. No optimized coordinates or theoretical answers are supplied. Do not read the target paper/SI, hidden evaluator files, private reference calculations or their calculated answers.

Measure α3 using the specified bonded four-atom torsion, retaining its sign. Measure β1 in the two Fy members using the two specified aryl least-squares planes, unit normals and acos(|n1·n2|), in degrees from 0 to 90; it is not a four-atom torsion. β1 is null for MeAC and TfAC. Record plane atom sets and fit residuals. The three IFCT fragments are explicitly mapped in the input, including the donor-side phenyl bridge and fluorene; attach hydrogens to their parent fragment. This fixed measurement convention is needed for comparable results across independently generated atom orders.

# Required investigation

1. Construct and optimize every named S0 molecule with a justified electronic-structure protocol. Establish identity, convergence and local-minimum evidence from frequencies/Hessian or an explicitly justified equivalent. Retain the selected conformer and its input/output paths.
2. Obtain the mapped α3/β1 geometry observations and fragment-resolved HOMO/LUMO localization on the selected geometry. State the population/visualization method; an unqualified sum of squared AO coefficients is not an overlap-aware population analysis.
3. Determine vertical singlet excitations on that same S0 geometry. Identify S1 as the lowest singlet root, retain its energy, oscillator strength and state-assignment evidence, and calculate enough nearby states to resolve ambiguous assignments. A brighter higher state cannot replace a dark S1.
4. For that same S1, obtain NTO hole/electron orbitals, leading pair weights and spatial/fragment interpretation. Perform IFCT using the three supplied fragments; retain the population partition, directed transfer matrix, CT/LE percentages and raw analysis outputs. Check state, geometry, atom mapping and normalization consistently across TD, NTO and IFCT. FMO localization alone cannot replace these excited-state endpoints.
5. Compare MeAC–TfAC, MeACFy–TfACFy, MeAC–MeACFy and TfAC–TfACFy using quantitative differences and the supporting geometry/orbital evidence. Distinguish robust effects from small differences sensitive to conformation or analysis conventions. Do not assert a required direction unsupported by your results.

Solvent/aggregate/device effects, triplet kinetics, RISC rates, complete higher-state series and axis-resolved metrics are optional and do not replace the required isolated-molecule S1 evidence. The existence of LE and CT contributions under a declared fragment definition does not by itself prove an experimental emission mechanism.

# Deliverables

Write `report/results.json` following `submission_schema.json`, with one uniquely identified record for each of the four compounds, calculation provenance, geometry observables, FMO analysis, S1/NTO/IFCT evidence, all four paired comparisons and a supported conclusion. Provide the calculation/coordinate/wavefunction/analysis file paths needed to inspect your results. `complete` requires all primary endpoints; a truthful `bounded_failure` identifies missing results and diagnostics and does not count as an uncomputed scientific result.

This is the S1-core contract revision of 2026-09-23. Earlier ground-state-only outputs do not certify its additional excited-state endpoints.
