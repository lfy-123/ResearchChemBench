# case_11 Scientific question

Investigate how the ligand environment of the specified Mn precursors affects candidate active forms, isopropanol oxidation and acetophenone reduction. Make paired comparisons for the Me and tBu series, and calculate differences between S/R-face reactions for candidate catalytic states with explicitly defined configurations. Integrate the two half-reactions to explain the supplied activity observations and what results for fixed configurations can establish about macroscopic stereoselectivity.

## Input files

- molecules.json: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- precursor_definitions.json: Components, formal oxidation states and textual descriptions of known initial coordination for metal/salt precursors.
- facts_and_conditions.json: Conditions, starting states and experimental facts permitted for use.
- run_settings.json: Common execution budget.
- submission_schema.json: Common result structure.
- input_preparation.md: Description of the files already provided and those requiring no additional preparation.

All required identities and facts are provided as text; images, spectra and PDF reading are unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

The scope is limited to the given Me/tBu series and NN control; complete actual species populations, precise rates and experimental ee are not required. Independently propose and test active species and coordination/electronic states.

## Required results

- Coordination identities of candidate active forms, actual connectivity of the two half-reactions, and hydrogen/charge accounting
- Matched comparisons of stabilization, alcohol oxidation and ketone reduction in the Me/tBu series
- S/R comparisons for each explicitly defined catalyst configuration and their mirror-image/ensemble implications

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; declare the scope of any simplification of a supplied identity. Support judgments with actual calculations. Author intermediate names, a fixed number of hypotheses, search tools and fixed trajectories are not prescribed. The relevant competing alternatives should be sufficient to support your conclusions.

Minima/transition states require corresponding evidence of convergence, vibrations and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, treatment of low frequencies, component inventory and common reference.

## Submission and available materials

Submit report/results.json, report/report.md and the referenced native computational inputs/outputs, geometries and necessary analyses. Allowed statuses in results.json are completed/partial/failed; record incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are available. The source paper, its mechanism or energy answers, author computational structures, historical runs, private scoring files and other systems' results are not available inputs. General online literature searches are not permitted. Supplied experimental facts serve only as explanatory context; restating them without computational support does not constitute a scientific result.
