# case_02 Scientific question

Given the complete molecular graph of radical R, investigate its competing intramolecular aryl ring closures in a DMSO model at 298.15 K. Determine the relevant ring-closure connectivities and activation free energies, compare their energy ordering, and make a selection supported by actual calculations. All barriers are relative to the same uncyclized radical minimum.

## Input files

- molecules.json: directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: conditions, starting states and permitted experimental facts.
- run_settings.json: common execution budget.
- submission_schema.json: common results structure.
- input_preparation.md: description of files already supplied and what requires no additional preparation.
- initial_geometry.xyz: independently generated initial guess; not an optimized minimum or transition state.
- initial_geometry.mapping.json: mapping from XYZ row numbers to atom indices in this molecule.

All required identities and facts are supplied as text; reading images, spectra or PDFs is unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

Local radical ring closure. The photocatalyst, upstream radical generation and subsequent oxidation/aromatization are outside this task. R has charge 0 and multiplicity 2.

## Required results

- Determine the chemically distinct competing ring-closure connectivities, including the aryl attachment positions and ring skeletons, from actual reaction evidence.
- Compare channel-specific formation accessibility from the same uncyclized radical and identify the final favored connectivity.
- Distinguish any additional tested regioisomers from the final selection; energies support the conclusion without paper-specific numerical targets.

### Required computed numerical evidence

- Computed Gibbs barrier and reference/reactive-state energies for benzyl-ring closure, identifying the actual bond-forming atoms.
- Computed Gibbs barrier and reference/reactive-state energies for sulfonyl-ring closure, identifying the actual bond-forming atoms.
- The barrier difference between the two ring closures relative to the same uncyclized R reference.

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; state the extent of any simplification of the supplied identities. Support judgments with actual calculations. The authors' intermediate names, a fixed number of hypotheses, search tools or prescribed trajectories are not required. The relevant alternatives compared must suffice to support your conclusions.

Minima/transition states require appropriate evidence of convergence, vibrational characterization and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not prove correct connectivity. For energies, specify whether they are electronic energies/enthalpies/Gibbs energies, together with temperature, solvent, standard state, low-frequency treatment, species inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The allowed statuses in results.json are completed/partial/failed; report incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Permitted resources are the files in this directory, general chemical-method/software documentation and computational tools. The source paper, its mechanistic or energy answers, the authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not allowed. Supplied experimental facts serve only as context for explanation; restating them without computational support does not constitute a scientific result.
