# case_09 Scientific question

In the supplied TfOH/HFIP system, establish a molecular pathway explaining formation of the observed trans adamantyl lactone from the E-alkenyl acid, and compare it with the corresponding cyclization of the specified E-alkenyl sulfonamide. Actually compute both types of connectivity, local activation free energies and net reaction free energies, and judge what explanation of reactivity their differences support.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: Conditions, initial states and permitted experimental facts.
- run_settings.json: Uniform execution budget.
- submission_schema.json: Uniform result structure.
- input_preparation.md: Description of the files already supplied and those requiring no further preparation.

All required identities and facts are supplied as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id values are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

The scope is local product formation and comparison of the two substrate classes. Excluding every cis pathway, a complete 1,1/1,2 network or exact yields is not required. The computational comparison temperature of 293.15 K is a model convention; do not misrepresent experimental room temperature as an exact temperature.

## Required results

- Actual connectivity from both substrate classes to the trans products
- Respective local barriers and balanced net reaction Gibbs energies under common definitions
- An explanation of the energetics and product formation in the two local reactions

Independently choose candidate mechanisms, molecular models, electronic states, conformers and computational methods; declare the scope of any simplification of the supplied identities. Support judgments with actual calculations. No authors' intermediate names, hypothesis count, search tools or fixed trajectories are prescribed. Relevant competitors should be sufficient to support the conclusions you draw.

Minima/transition states require corresponding convergence, vibrational and chemical-assignment evidence. For any claimed continuous pathway, supply reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone cannot establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, low-frequency treatment, component inventory and common reference.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The status in results.json may be completed/partial/failed; record unfinished work truthfully. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are permitted. The source paper, its mechanism or energy answers, authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not enabled. Supplied experimental facts serve only as explanatory context; repeating them without computational support does not constitute a scientific result.
