# case_12 Scientific question

Why does substrate S rearrange to the specified bicyclic product P under the given thioxanthone/395 nm and DMSO conditions? Perform actual calculations of the relevant electronic states and bond-forming and bond-breaking processes, explain the changes in skeletal connectivity, and test which energetic/structural factors can support the observed cis relative configuration of the product.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: Conditions, starting states and experimental facts permitted for use.
- run_settings.json: Common execution budget.
- submission_schema.json: Common result structure.
- input_preparation.md: Description of the files already provided and those requiring no additional preparation.

All required identities and facts are provided as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

The scope covers local photosensitized skeletal rearrangement and evidence relevant to cis/trans. Precise intersystem-crossing rates, a complete photophysical network, or predictions of dr or 99% yield are not required.

## Required results

- Evidence for sensitization/electronic-state accessibility using compatible definitions
- Actual C–C bond formation, bond cleavage, ring expansion and product connectivity during the skeletal transformation
- Comparisons of cis/trans structures and energies and a bounded explanation of the stereochemical outcome

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; declare the scope of any simplification of a supplied identity. Support judgments with actual calculations. Author intermediate names, a fixed number of hypotheses, search tools and fixed trajectories are not prescribed. The relevant competing alternatives should be sufficient to support your conclusions.

Minima/transition states require corresponding evidence of convergence, vibrations and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, treatment of low frequencies, component inventory and common reference.

## Submission and available materials

Submit report/results.json, report/report.md and the referenced native computational inputs/outputs, geometries and necessary analyses. Allowed statuses in results.json are completed/partial/failed; record incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are available. The source paper, its mechanism or energy answers, author computational structures, historical runs, private scoring files and other systems' results are not available inputs. General online literature searches are not permitted. Supplied experimental facts serve only as explanatory context; restating them without computational support does not constitute a scientific result.
