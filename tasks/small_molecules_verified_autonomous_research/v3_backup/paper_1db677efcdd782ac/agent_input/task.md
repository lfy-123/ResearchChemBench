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

- Explain the local ring-opening energetic tendency of H, cis-Me and trans-Me in the +1 doublet boundary, with appropriate qualification of method-sensitive or near-thermoneutral comparisons.
- Relate common-reference cis/trans open/closed stability to a possible methyl-isomer interconversion mechanism, distinguishing compatibility from a computed complete interconversion rate.
- Test local ring-closed stability of the Ph model and compare opening accessibility across the series to assess whether fast irreversible opening can be generalized.

### Required computed numerical evidence

- Computed ring-opened/ring-closed electronic energies and ring-opening ΔE for H.
- Computed ring-opened/ring-closed electronic energies and ring-opening ΔE for cis-Me, including the actual values when near-degenerate or method-sensitive.
- Computed ring-opened/ring-closed electronic energies and ring-opening ΔE for trans-Me.
- Common-reference electronic-energy differences among cis/trans-Me open and closed states; a new complete interconversion-rate calculation is not required.
- Actual energies and geometries from a Ph closed-ring-start relaxation, a ring-closing profile or an equivalent local stability test.
- Computed local ring-opening electronic-energy barriers ΔE‡ for H, cis-Me and trans-Me, and their cross-substrate differences.

Independently choose candidate mechanisms, molecular models, electronic states, conformations and computational methods; state the extent of any simplification of the supplied identities. Support judgments with actual calculations. The authors' intermediate names, a fixed number of hypotheses, search tools or prescribed trajectories are not required. The relevant alternatives compared must suffice to support your conclusions.

Minima/transition states require appropriate evidence of convergence, vibrational characterization and chemical assignment. For any claimed continuous pathway, provide reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone do not prove correct connectivity. For energies, specify whether they are electronic energies/enthalpies/Gibbs energies, together with temperature, solvent, standard state, low-frequency treatment, species inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The allowed statuses in results.json are completed/partial/failed; report incomplete work honestly. Molecular models, numerical results and conclusions must each be traceable.

Permitted resources are the files in this directory, general chemical-method/software documentation and computational tools. The source paper, its mechanistic or energy answers, the authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not allowed. Supplied experimental facts serve only as context for explanation; restating them without computational support does not constitute a scientific result.
