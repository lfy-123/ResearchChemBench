# case_11 Scientific question

How does the ligand environment of the specified Mn precursors affect the reactivity and stereochemistry of acetophenone transfer hydrogenation under the supplied basic isopropanol conditions? Make paired comparisons for the Me and tBu series by independently proposing and testing candidate catalytic states and reaction mechanisms, using the supplied experimental control as context. Determine how ligand-dependent stabilization and accessibility affect isopropanol oxidation and acetophenone reduction, and which half-reaction imposes the greater effective activation demand. Integrate these results to explain the supplied activity observations. Calculate S/R-face preferences for explicitly defined catalyst configurations, and explain what those results can establish about macroscopic stereoselectivity.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- precursor_definitions.json: Components, formal oxidation states and textual descriptions of known initial coordination for metal/salt precursors.
- facts_and_conditions.json: Conditions, starting states and experimental facts permitted for use.
- run_settings.json: Common execution budget.
- submission_schema.json: Common result structure.
- input_preparation.md: Description of the files already provided and those requiring no additional preparation.

All required identities and facts are provided as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

The scope is the given Me/tBu ligand series, with the sulfur-free HL_0 precursor serving as the supplied experimental NN control. Do not identify that control with a candidate that retains a sulfur-containing ligand. Complete actual species populations, precise rates and experimental ee are not required. Independently propose and test active species and coordination/electronic states.

## Required results

- Explain ligand-dependent candidate formation and stabilization using balanced comparisons for both Me and tBu series.
- Compare NN and NNS coordination environments for alcohol oxidation and ketone reduction in both ligand series, and identify the harder half-reaction after the relevant resting-state reference is considered. Propose and test the active states independently; no fixed carbonyl count is imposed on an active state, but CO/proton inventories must balance.
- Predict stereochemical preferences for explicitly defined catalyst configurations and apply those actual results to mirror-related configurations and the macroscopic ensemble.

### Required computed numerical evidence

- Computed balanced Gibbs-energy differences for candidate formation/conversion and alcohol-binding stabilization in both Me and tBu series.
- Computed matched Gibbs activation energies and coordination-environment differences for NN/NNS alcohol oxidation in the Me/tBu series.
- Computed matched Gibbs activation energies and coordination-environment differences for NN/NNS ketone reduction in the Me/tBu series, defining donor states and configurations.
- Computed effective activation energies and their difference for the two half-reactions after the relevant alcohol-bound/resting-state references are included.
- Computed face-specific reduction activation energies and S/R differences for each explicitly investigated configuration. Apply these values and mappings to mirror/ensemble reasoning; no additional complete mirror-pathway calculation is required.

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; declare the scope of any simplification of a supplied identity. Support judgments with actual calculations. Author intermediate names, a fixed number of hypotheses, search tools and fixed trajectories are not prescribed. The relevant competing alternatives should be sufficient to support your conclusions.

Minima/transition states require corresponding evidence of convergence, vibrations and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, treatment of low frequencies, component inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and available materials

Submit report/results.json, report/report.md and the referenced native computational inputs/outputs, geometries and necessary analyses. Allowed statuses in results.json are completed/partial/failed; record incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are available. The source paper, its mechanism or energy answers, author computational structures, historical runs, private scoring files and other systems' results are not available inputs. General online literature searches are not permitted. Supplied experimental facts serve only as explanatory context; restating them without computational support does not constitute a scientific result.
