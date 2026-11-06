## Scientific question

How does the ligand environment of the specified Mn precursors affect the reactivity and stereochemistry of acetophenone transfer hydrogenation under the supplied basic isopropanol conditions? Make paired comparisons for the Me and tBu series by independently proposing and testing candidate catalytic states and reaction mechanisms, using the supplied experimental control as context. Determine how ligand-dependent stabilization and accessibility affect isopropanol oxidation and acetophenone reduction, and which half-reaction imposes the greater effective activation demand. Integrate these results to explain the supplied activity observations. Calculate S/R-face preferences for explicitly defined catalyst configurations, and explain what those results can establish about macroscopic stereoselectivity.

## Input files

- `data/molecules.json`: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- `data/precursor_definitions.json`: Components, formal oxidation states and textual descriptions of known initial coordination for metal/salt precursors.
- `data/facts_and_conditions.json`: Conditions, starting states and supplied experimental facts.
- `data/README.md`: molecular identity, numbering and structural constraints.

Chemical numbering and JSON atom IDs are separate systems; preserve an explicit mapping. Retain the supplied stereochemical, coordination and initial charge/spin constraints when constructing three-dimensional models.

## Scope

The scope is the given Me/tBu ligand series, with the sulfur-free HL_0 precursor serving as the supplied experimental NN control. Do not identify that control with a candidate that retains a sulfur-containing ligand. Complete actual species populations, precise rates and experimental ee are not required. Independently propose and test active species and coordination/electronic states.

## Required results

1. Explain ligand-dependent candidate formation and stabilization for both Me and tBu series using balanced Gibbs-energy differences for formation/conversion and alcohol binding. Preserve the sulfur-free HL_0 identity of the experimental NN control.

2. Compare NN and NNS environments for isopropanol oxidation in both series using matched Gibbs activation energies and coordination-environment differences. Propose the active states independently and balance CO/proton inventories.

3. Compare NN and NNS environments for acetophenone reduction in both series using matched Gibbs activation energies and their differences, with donor states and catalyst configurations defined. No fixed carbonyl count is imposed on an active state.

4. Include the relevant alcohol-bound/resting-state references to compute effective activation requirements for both half-reactions and their difference. Identify the harder half-reaction and integrate the accessibility and stabilization results to explain the supplied activity observations.

5. Predict face-specific S/R reduction preferences for each explicitly investigated catalyst configuration using computed activation energies and their differences. Apply these values and mappings to mirror-related configurations and the macroscopic ensemble; a complete additional mirror-pathway calculation is outside scope.

Choose mechanisms, molecular models, electronic states, conformers and methods independently; declare simplifications and compare alternatives sufficient to support the conclusions. Validate claimed minima and transition states with convergence, vibrational and chemical-assignment evidence, and claimed pathways with reaction modes, endpoints or equivalent connectivity evidence. Define each energy as electronic energy, enthalpy or Gibbs energy and state temperature, solvent, standard state, low-frequency treatment, component inventory and common reference. Support a barrierless assignment with a computed profile and defined reference. Explain method-sensitive or near-degenerate results and the scope of the supported inference.

Continue the research until you reach the final conclusions; do not end prematurely by submitting an unfinished report.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_schema.json` and `submission_guide.md`. Link each conclusion to its computed quantities and retained native inputs, outputs, geometries and supporting analyses.
