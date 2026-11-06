# case_04 Scientific question

For substrate S and the supplied Rh carbonyl chloride precursor, construct and compute a catalytic transformation network that explains the two product connectivities P1 and P2 under the specified conditions. Compare the relevant competing branches and alternatives for the initial transformation. Report the principal activation requirements with explicit physical references and species inventories, and identify which branches are supported by actual evidence. P2 has a cis relationship between the hydrogens at its two fused-ring junctions (atom_id 6 and 10 in the P2 molecular graph). This relative configuration is part of the supplied target identity; its complete mirror image is equally acceptable.

## Input files

- molecules.json: directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- precursor_definitions.json: textual descriptions of the composition, formal oxidation states and known initial coordination of metal/salt precursors.
- facts_and_conditions.json: conditions, starting states and permitted experimental facts.
- run_settings.json: common execution budget.
- submission_schema.json: common results structure.
- input_preparation.md: description of files already supplied and what requires no additional preparation.

All required identities and facts are supplied as text; reading images, spectra or PDFs is unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

Cycloisomerization and intramolecular [2+2] transformation of the specified O-linked 1,7-allenene model. Carbonylation products from CO insertion, the full distribution of actual solution species and quantitative experimental yields are outside this task.

## Required results

- Explain how the catalyst mediates formation of each supplied product from S, including the bond and hydrogen rearrangements relevant to each mechanism.
- Compare relevant initial mechanisms and explain the role of coordination or ligand exchange.
- Identify the kinetically demanding transformation with the appropriate reference, and explain how the two product-forming branches compete; exact numerical reproduction is not a scoring objective.

### Required computed numerical evidence

- Computed relative energies and local activation requirements along the connected P1 route, with CO/ligand inventory included consistently.
- Computed relative energies and local activation requirements along the connected P2 route, with CO/ligand inventory included consistently.
- Local and resting-state-referenced activation energies, comparable overall activation requirements for both product branches and their difference, with reference conversions stated.
- Comparable activation energies and differences for the proposed initial mechanism and substantive alternatives; an exhaustive reproduction of every published alternative is not required.

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; state the extent of any simplification of the supplied identities. Support judgments with actual calculations. The authors' intermediate names, a fixed number of hypotheses, search tools or prescribed trajectories are not required. The relevant alternatives compared must suffice to support your conclusions.

Minima/transition states require appropriate evidence of convergence, vibrational characterization and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not prove correct connectivity. For energies, specify whether they are electronic energies/enthalpies/Gibbs energies, together with temperature, solvent, standard state, low-frequency treatment, species inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The allowed statuses in results.json are completed/partial/failed; report incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Permitted resources are the files in this directory, general chemical-method/software documentation and computational tools. The source paper, its mechanistic or energy answers, the authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not allowed. Supplied experimental facts serve only as context for explanation; restating them without computational support does not constitute a scientific result.
