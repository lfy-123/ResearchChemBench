# case_05 Scientific question

For local molecular models of the supplied H-, Me- and Ph-substituted amines after one-electron oxidation, investigate the accessibility of cyclopropane ring opening and compare ring-opened/ring-closed electronic energies. Also compare the cis and trans relative configurations of the Me system and their interconversion. Based on actual calculations, determine whether the same fast irreversible ring-opening behavior can be generalized to all supplied substrates.

## Input files

- molecules.json: directly parseable SMILES, atom-mapped SMILES, atom/bond tables, and necessary stereochemical and coordination constraints.
- facts_and_conditions.json: conditions, starting states and permitted experimental facts.
- run_settings.json: common execution budget.
- submission_schema.json: common results structure.
- input_preparation.md: description of files already supplied and what requires no additional preparation.

All required identities and facts are supplied as text; reading images, spectra or PDFs is unnecessary. Chemical numbering in molecular names and JSON atom_id are separate numbering systems and must be explicitly mapped when used. Stereochemical constraints and known initial charge/spin are part of molecular identity and must not be omitted.

## Scope

Local states after one-electron oxidation, with charge +1 and doublet multiplicity. The starting molecular graphs define neutral amines; construct the corresponding electronic states by removing one electron. The primary comparison quantity is electronic energy ΔE, not ΔG. The complete photocycle, oxidation potentials, aldehyde formation and isotope provenance are outside this task.

## Required results

- Ring-opening pathways, local electronic-energy barriers and reaction electronic energies for H, cis-Me and trans-Me
- Ring-closed/ring-opened stability and interconversion relationships of the Me isomers under a common reference
- Actual tests of local ring-closed stability in the Ph model, and conclusions limited to this series

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; state the extent of any simplification of the supplied identities. Support judgments with actual calculations. The authors' intermediate names, a fixed number of hypotheses, search tools or prescribed trajectories are not required. The relevant alternatives compared must suffice to support your conclusions.

Minima/transition states require appropriate evidence of convergence, vibrational characterization and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not prove correct connectivity. For energies, specify whether they are electronic energies/enthalpies/Gibbs energies, together with temperature, solvent, standard state, low-frequency treatment, species inventory and common reference.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The allowed statuses in results.json are completed/partial/failed; report incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Permitted resources are the files in this directory, general chemical-method/software documentation and computational tools. The source paper, its mechanistic or energy answers, the authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not allowed. Supplied experimental facts serve only as context for explanation; restating them without computational support does not constitute a scientific result.
