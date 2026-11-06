# case_10 Scientific question

How does triethylphosphine promote formation of the specified cyclopentenone from the supplied alkyne–ester substrate and 4-fluorophenol? Establish and compute a balanced route from reactants to product that also regenerates the catalyst. Compare relevant competing branches and identify the main factors controlling kinetic and thermodynamic accessibility.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: Conditions, initial states and permitted experimental facts.
- run_settings.json: Uniform execution budget.
- submission_schema.json: Uniform result structure.
- input_preparation.md: Description of the files already supplied and those requiring no further preparation.

All required identities and facts are supplied as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id values are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

The scope is a bounded catalytic route for the specified substrate, nucleophile and PEt3; all conformers, the full substrate scope or asymmetric variants are not required.

## Required results

- Connectivity evidence for catalyst participation, skeleton construction, nucleophile incorporation and catalyst regeneration
- Common-reference comparison of relevant competing branches and the highest activation requirement
- Product structure, balanced total free energy and a final mechanistic explanation

Independently choose candidate mechanisms, molecular models, electronic states, conformers and computational methods; declare the scope of any simplification of the supplied identities. Support judgments with actual calculations. No authors' intermediate names, hypothesis count, search tools or fixed trajectories are prescribed. Relevant competitors should be sufficient to support the conclusions you draw.

Minima/transition states require corresponding convergence, vibrational and chemical-assignment evidence. For any claimed continuous pathway, supply reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone cannot establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, low-frequency treatment, component inventory and common reference.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The status in results.json may be completed/partial/failed; record unfinished work truthfully. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are permitted. The source paper, its mechanism or energy answers, authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not enabled. Supplied experimental facts serve only as explanatory context; repeating them without computational support does not constitute a scientific result.
