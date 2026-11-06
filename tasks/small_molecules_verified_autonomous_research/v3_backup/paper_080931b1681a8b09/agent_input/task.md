# case_08 Scientific question

For the supplied benzothiazole and bicyclobutane under Ni(OTf)2/(S,S)-tert-butyl PyBOX conditions in CHCl3, develop and test a molecular explanation for formation of the specified cycloaddition-product connectivity. Compute the competing enantiomer-formation processes, predict the favored absolute configuration at the specified saturated CH, and compare the computationally supported selectivity strength with the supplied experimental er within explicit bounds.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables and necessary stereochemical and coordination constraints.
- precursor_definitions.json: Text definitions of metal/salt precursor components, formal oxidation states and known initial coordination.
- facts_and_conditions.json: Conditions, initial states and permitted experimental facts.
- run_settings.json: Uniform execution budget.
- submission_schema.json: Uniform result structure.
- input_preparation.md: Description of the files already supplied and those requiring no further preparation.

All required identities and facts are supplied as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id values are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

Study only the specified catalyst/ligand, reactants and product; do not mix in data for other nickel salts or ligands. Initial coordination configuration, active-species charge/spin and the formation route are not supplied.

## Required results

- Explain catalyst binding and the bond-reorganization chemistry producing the supplied cycloadduct connectivity.
- Predict the preferred absolute configuration at the specified saturated CH from competing enantiomer-forming processes.
- Explain the physical origin using actual comparative molecular evidence and assess what the model can establish about the supplied experimental enrichment, without treating numerical agreement as a scoring criterion.

### Required computed numerical evidence

- Computed key-state energies and activation requirements supporting binding and the proposed ring-opening/closure or equivalent product-formation mechanism.
- Computed R/S Gibbs activation energies and ΔΔG‡ for the correctly mapped competing configurations.
- Computed R/S structural or electronic data supporting the chosen physical explanation, such as contact distances, angles, deformation or interaction quantities; choose data appropriate to the claim, with no mandatory decomposition algorithm.

Independently choose candidate mechanisms, molecular models, electronic states, conformers and computational methods; declare the scope of any simplification of the supplied identities. Support judgments with actual calculations. No authors' intermediate names, hypothesis count, search tools or fixed trajectories are prescribed. Relevant competitors should be sufficient to support the conclusions you draw.

Minima/transition states require corresponding convergence, vibrational and chemical-assignment evidence. For any claimed continuous pathway, supply reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone cannot establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, low-frequency treatment, component inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The status in results.json may be completed/partial/failed; record unfinished work truthfully. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are permitted. The source paper, its mechanism or energy answers, authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not enabled. Supplied experimental facts serve only as explanatory context; repeating them without computational support does not constitute a scientific result.
