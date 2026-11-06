# case_03 Scientific question

Investigate competition in the formation of the three constitutional isomers P1, P2 and P3 from siloxy cyclopropene S in dichloromethane with methanol (3.0 equiv) and TMSCl (5 mol %) at room temperature under acidic conditions. Compare the formation pathways for each connectivity and the relative Gibbs free energies of the three neutral products. Determine whether competition in formation and product stability favor the same outcome, and what direction of isomer redistribution these energies can support. P1/P2/P3 have no priority ranking. The stated MeOH/TMSCl mixture provides the acidic medium; its acid concentration and proton activity are unspecified.

## Input files

- molecules.json: directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: conditions, starting states and permitted experimental facts.
- run_settings.json: common execution budget.
- submission_schema.json: common results structure.
- input_preparation.md: description of files already supplied and what requires no additional preparation.

All required identities and facts are supplied as text; reading images, spectra or PDFs is unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

Limit the study to the methanol functionalization stage after S has been prepared. Upstream photochemical preparation, full yields, exact time courses and complete equilibrium ratios are outside the study. No precise numerical value was reported for experimental room temperature; 298.15 K is adopted for the primary computational comparison.

## Required results

- Explain the methanol-functionalization chemistry for the three different C–O connectivities using actual reaction evidence.
- Compare the competing formation processes of all three supplied candidate connectivities using compatible precursor references.
- Establish the neutral-product stability relationships and explain whether formation preference and thermodynamic redistribution favor the same outcome, without inferring uncomputed exchange rates.
- Report the complete stability ordering of the three neutral products from comparable calculations, separately from formation preference and redistribution kinetics.

### Required computed numerical evidence

- Computed formation-pathway energies and activation requirement for methanol capture giving P1, with the activation model and proton inventory defined.
- Computed formation-pathway energies and activation requirement for methanol capture giving P2, using references compatible with the competing channels.
- Computed formation-pathway energies and activation requirement for methanol capture giving P3, using references compatible with the competing channels.
- The P2/P3 formation activation-energy difference and its definition.
- The P2/P1 formation activation-energy difference and its definition.
- Computed Gibbs energies and their difference for neutral P2 and P3, kept separate from charged formation states.
- The computed Gibbs energy of neutral P1 and its differences from neutral P2 and P3.

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; state the extent of any simplification of the supplied identities. Support judgments with actual calculations. The authors' intermediate names, a fixed number of hypotheses, search tools or prescribed trajectories are not required. The relevant alternatives compared must suffice to support your conclusions.

Minima/transition states require appropriate evidence of convergence, vibrational characterization and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not prove correct connectivity. For energies, specify whether they are electronic energies/enthalpies/Gibbs energies, together with temperature, solvent, standard state, low-frequency treatment, species inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The allowed statuses in results.json are completed/partial/failed; report incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Permitted resources are the files in this directory, general chemical-method/software documentation and computational tools. The source paper, its mechanistic or energy answers, the authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not allowed. Supplied experimental facts serve only as context for explanation; restating them without computational support does not constitute a scientific result.
