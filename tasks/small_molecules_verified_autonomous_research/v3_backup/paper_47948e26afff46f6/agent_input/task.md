# case_13 Scientific question

For the given quinoxalin-2(1H)-one, diazo ester and blue-light/DCM reaction system, which of the supplied N-connected and O-connected candidate products is favored by the local bond-formation competition? Independently propose and test relevant active-species and reaction models, compare actual activation free energies on a consistent basis, and explain the predicted site preference with computational evidence.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: Conditions, starting states and experimental facts permitted for use.
- run_settings.json: Common execution budget.
- submission_schema.json: Common result structure.
- input_preparation.md: Description of the files already provided and those requiring no additional preparation.

All required identities and facts are provided as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

The core scope is local N/O bond-formation competition and a qualitative prediction of the favored connection. P_N and P_O are candidate connectivities, not disclosed experimental outcomes. Define the local precursor composition, proton placement and electronic state, justify their chemical relevance, and compare the channels on a compatible reference. Local precursors may be treated as explicitly stated model assumptions; computation of their upstream photochemical generation, preceding chemical steps and a complete spin-conversion network is not required. These local results do not by themselves establish whole-reaction selectivity, populations or yield. Full thermochemistry of both final products is not required.

## Required results

- Explain the distinct N- and O-bond-forming chemistry from a chemically justified common local precursor, with explicit proton and electronic-state assumptions.
- Predict the favored site from actual compatible competing formation evidence and support the favored product identity and local stability.
- Limit the inference to the investigated local model; upstream precursor generation, a complete spin network and full thermochemistry of both products are not required.

### Required computed numerical evidence

- Computed local N–C formation Gibbs barrier and precursor/reactive-state energies, with proton positions and electronic states defined.
- Computed local O–C formation Gibbs barrier and compatible precursor/reactive-state energies, with proton positions and electronic states defined.
- The N/O formation barrier difference relative to the same local precursor.

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; declare the scope of any simplification of a supplied identity. Support judgments with actual calculations. Author intermediate names, a fixed number of hypotheses, search tools and fixed trajectories are not prescribed. The relevant competing alternatives should be sufficient to support your conclusions.

Minima/transition states require corresponding evidence of convergence, vibrations and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, treatment of low frequencies, component inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and available materials

Submit report/results.json, report/report.md and the referenced native computational inputs/outputs, geometries and necessary analyses. Allowed statuses in results.json are completed/partial/failed; record incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are available. The source paper, its mechanism or energy answers, author computational structures, historical runs, private scoring files and other systems' results are not available inputs. General online literature searches are not permitted. Supplied experimental facts serve only as explanatory context; restating them without computational support does not constitute a scientific result.
