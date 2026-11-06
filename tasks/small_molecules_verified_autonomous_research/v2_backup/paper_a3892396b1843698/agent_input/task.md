# case_01 Scientific question

For the neutral molecule S in molecules.json, investigate competition between its transformations into the constitutional isomers P1 and P2 under isolated-molecule conditions at 298.15 K. Independently construct and test the transformation pathways, compare activation free energies relative to the same reactant reference, and identify the favored direction supported by calculations. P1/P2 are only labels for unranked candidate endpoints.

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

Study only the two candidate endpoints of the specified molecule; other polycyclic derivatives, dynamical trajectories and negative-activation-energy systems are not required.

## Required results

- Structures/atom mappings and connectivity evidence for S and both transformations
- The two activation free energies and their difference, in kcal/mol
- A conclusion about competition supported by calculations

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; state the extent of any simplification of the supplied identities. Support judgments with actual calculations. The authors' intermediate names, a fixed number of hypotheses, search tools or prescribed trajectories are not required. The relevant alternatives compared must suffice to support your conclusions.

Minima/transition states require appropriate evidence of convergence, vibrational characterization and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not prove correct connectivity. For energies, specify whether they are electronic energies/enthalpies/Gibbs energies, together with temperature, solvent, standard state, low-frequency treatment, species inventory and common reference.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The allowed statuses in results.json are completed/partial/failed; report incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Permitted resources are the files in this directory, general chemical-method/software documentation and computational tools. The source paper, its mechanistic or energy answers, the authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not allowed. Supplied experimental facts serve only as context for explanation; restating them without computational support does not constitute a scientific result.
