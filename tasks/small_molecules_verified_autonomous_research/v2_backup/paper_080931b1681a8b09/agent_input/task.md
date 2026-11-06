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

- Evidence for substrate binding and reaction connectivity leading to the cycloadduct
- Competition between the two enantiomers and correct absolute-configuration mapping
- Actual physical evidence for environmental differences and an explanation of the origin of selectivity

Independently choose candidate mechanisms, molecular models, electronic states, conformers and computational methods; declare the scope of any simplification of the supplied identities. Support judgments with actual calculations. No authors' intermediate names, hypothesis count, search tools or fixed trajectories are prescribed. Relevant competitors should be sufficient to support the conclusions you draw.

Minima/transition states require corresponding convergence, vibrational and chemical-assignment evidence. For any claimed continuous pathway, supply reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone cannot establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, low-frequency treatment, component inventory and common reference.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The status in results.json may be completed/partial/failed; record unfinished work truthfully. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are permitted. The source paper, its mechanism or energy answers, authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not enabled. Supplied experimental facts serve only as explanatory context; repeating them without computational support does not constitute a scientific result.
