# case_06 Scientific question

Under the supplied Pd/L-pyroglutamic-acid olefination conditions, compare productive reaction pathways of the two nitrogen configurations of racemic substrate S, and separately investigate configurational interconversion of isolated S and product P. Provide actual structures, activation free energies and energy comparisons, explaining how far these independent results support the supplied observations of product enrichment and configurational stability.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables and necessary stereochemical and coordination constraints.
- precursor_definitions.json: Text definitions of metal/salt precursor components, formal oxidation states and known initial coordination.
- facts_and_conditions.json: Conditions, initial states and permitted experimental facts.
- run_settings.json: Uniform execution budget.
- submission_schema.json: Uniform result structure.
- input_preparation.md: Description of the files already supplied and those requiring no further preparation.

All required identities and facts are supplied as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id values are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

Compare reactivity and the respective configurational interconversions of S/P; each of the three comparisons uses its own explicitly stated solvent and temperature. A full catalytic cycle, complete dynamic kinetic resolution model, exact ee or optoelectronic material properties are not required.

## Required results

- Map the two initial nitrogen configurations consistently to A and B and establish a connected productive route from each to its corresponding product, identifying the chemical transformations; complete catalytic turnover is outside scope.
- Determine which productive step distinguishes the configurations and what the computed competition implies for product enrichment, without assuming an exact ee.
- Assess isolated S and isolated P inversion and configurational persistence separately at their respective specified conditions. Compare their computed activation requirements while explicitly accounting for the different solvent and temperature definitions; do not infer a same-condition rate ordering from these different models.
- Integrate productive selectivity and isolated configurational persistence to explain enrichment and retention, distinguishing these from an unverified complete dynamic kinetic resolution model.

### Required computed numerical evidence

- Computed Gibbs activation energies for both productive configurations and their difference on a common reference, linked to the actual configuration mapping.
- Computed inversion Gibbs barrier and state energies for isolated S in the specified MeCN/353.15 K model, with evidence connecting the configurations.
- Computed inversion Gibbs barrier and state energies for isolated P in the specified n-octane/398.15 K model, with evidence connecting the configurations.
- Computed key-state Gibbs energies and activation requirements along a connected productive route from initial nitrogen configuration A to the specified product, with component/reference bookkeeping; complete catalyst turnover is not required.
- Computed key-state Gibbs energies and activation requirements along a connected productive route from initial nitrogen configuration B to the specified product, with component/reference bookkeeping; complete catalyst turnover is not required.

Independently choose candidate mechanisms, molecular models, electronic states, conformers and computational methods; declare the scope of any simplification of the supplied identities. Support judgments with actual calculations. No authors' intermediate names, hypothesis count, search tools or fixed trajectories are prescribed. Relevant competitors should be sufficient to support the conclusions you draw.

Minima/transition states require corresponding convergence, vibrational and chemical-assignment evidence. For any claimed continuous pathway, supply reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone cannot establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, low-frequency treatment, component inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The status in results.json may be completed/partial/failed; record unfinished work truthfully. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are permitted. The source paper, its mechanism or energy answers, authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not enabled. Supplied experimental facts serve only as explanatory context; repeating them without computational support does not constitute a scientific result.
