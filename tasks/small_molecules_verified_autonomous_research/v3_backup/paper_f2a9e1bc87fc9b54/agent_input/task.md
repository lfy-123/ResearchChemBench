# case_14 Scientific question

For the given 3-nitropyrrole, propargyl bromide and NaH/DMF conditions, establish a pathway for formation of the N-propargyl product supported by actual calculations. Explain the conversion using chemical connectivity, local activation requirements and the Gibbs energy of the balanced net reaction, distinguishing local activation difficulty from the overall thermodynamic driving force.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: Conditions, starting states and experimental facts permitted for use.
- run_settings.json: Common execution budget.
- submission_schema.json: Common result structure.
- input_preparation.md: Description of the files already provided and those requiring no additional preparation.

All required identities and facts are provided as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

The scope is the local synthetic conversion; molecular docking, cellular activity and all subsequent derivatizations are outside the investigation. Explicitly declared molecular/ionic simplifications may be used, but balance must be maintained within their stated boundaries; they must not be described as complete models of solid/aggregated/solution-phase NaH.

## Required results

- Explain base-mediated nitrogen activation and subsequent or coupled N–C bond formation, supported by actual connectivity and balanced proton/hydride accounting.
- Determine which local chemical event has the greater activation demand and distinguish that from overall thermodynamic driving force.
- Establish the thermodynamic direction of the balanced net reaction within the explicitly declared molecular or ionic model.

### Required computed numerical evidence

- Computed local activation energies, precursor/reactive-state energies and differences for base/nitrogen activation and N–C substitution; a coupled mechanism must supply an actual profile addressing the same comparison.
- Computed energies for the complete balanced reactant/product inventory, including required ions, gases and coproducts, and the resulting net Gibbs ΔG.

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; declare the scope of any simplification of a supplied identity. Support judgments with actual calculations. Author intermediate names, a fixed number of hypotheses, search tools and fixed trajectories are not prescribed. The relevant competing alternatives should be sufficient to support your conclusions.

Minima/transition states require corresponding evidence of convergence, vibrations and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, treatment of low frequencies, component inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and available materials

Submit report/results.json, report/report.md and the referenced native computational inputs/outputs, geometries and necessary analyses. Allowed statuses in results.json are completed/partial/failed; record incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are available. The source paper, its mechanism or energy answers, author computational structures, historical runs, private scoring files and other systems' results are not available inputs. General online literature searches are not permitted. Supplied experimental facts serve only as explanatory context; restating them without computational support does not constitute a scientific result.
