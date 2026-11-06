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

- Explain the bond-forming chemistry producing each supplied trans product for the acid and sulfonamide substrates.
- Compare their local kinetic accessibility under compatible precursor definitions.
- Determine the thermodynamic driving direction of each balanced net reaction and distinguish it from kinetic accessibility.
- For each substrate, distinguish the computation-supported route connecting electrophilic incorporation to the product from validation of its key local bond-forming transition state.
- For each claimed transition state, establish the chemical event through geometry, reaction-mode and endpoint or equivalent connectivity evidence; report which local events are established even if the full route remains incomplete.

### Required computed numerical evidence

- Computed local Gibbs activation energy and matched precursor/reactive-state energies for the acid-derived formation route.
- Computed local Gibbs activation energy and matched precursor/reactive-state energies for the sulfonamide-derived formation route.
- The difference between acid and sulfonamide local activation energies under the same definition.
- Computed Gibbs energies for the complete balanced acid-reaction inventory and the resulting net ΔG.
- Computed Gibbs energies for the complete balanced sulfonamide-reaction inventory and the resulting net ΔG.
- Computed connected profile energies and applicable activation estimates for acid electrophilic incorporation and intramolecular capture to the given product, with component/proton bookkeeping; detailed saddle validation is a separate result.
- Computed connected profile energies and applicable activation estimates for sulfonamide electrophilic incorporation and intramolecular capture to the given product, with component/proton bookkeeping; detailed saddle validation is a separate result.

Independently choose candidate mechanisms, molecular models, electronic states, conformers and computational methods; declare the scope of any simplification of the supplied identities. Support judgments with actual calculations. No authors' intermediate names, hypothesis count, search tools or fixed trajectories are prescribed. Relevant competitors should be sufficient to support the conclusions you draw.

Minima/transition states require corresponding convergence, vibrational and chemical-assignment evidence. For any claimed continuous pathway, supply reaction modes, endpoints or other sufficient connectivity evidence. One imaginary frequency and a normal-termination label alone cannot establish correct connectivity. For energies, specify electronic energy/enthalpy/Gibbs energy, temperature, solvent, standard state, low-frequency treatment, component inventory and common reference.

## Assessment basis

Assessment concerns distinct, computation-supported scientific conclusions within this task: the requested mechanistic explanations, structural or stereochemical outcomes, comparisons and their physical implications. Energies and other numerical results remain auditable supporting evidence, but agreement with paper-specific numerical values, tolerances or exact experimental ratios is not a scoring objective. Explain method-sensitive or near-degenerate results honestly. Merely restating supplied products, observations or plausible textbook mechanisms without relevant computed support is insufficient. Equivalent evidence-supported models are acceptable within the stated chemical scope; no fixed author pathway or software is required.

The numerical evidence listed above is mandatory: perform the relevant computations and report the resulting values in `report/results.json.metrics`, with units, definitions, subtraction order, reference states, methods/conditions and evidence IDs. Link claims to metric IDs and explain their scientific meaning in `report/report.md`. Supply auditable native inputs/outputs and the relevant geometries or reaction-mode evidence. Correctly guessing a conclusion, copying literature numbers, preparing inputs or submitting unfinished jobs does not satisfy this requirement. A conclusion lacking its necessary computed quantities or genuine supporting evidence fails that item, while independently supported items retain their points. No separate credit is given for completing calculations. Integrated or symmetry-based inferences may reuse identified computed values; equivalent mechanisms still require quantitative evidence addressing the same physical questions. A claimed barrierless process requires a computed profile and a defined reference, not an invented zero.

## Submission and permitted resources

Submit report/results.json, report/report.md and the cited native computational inputs/outputs, geometries and necessary analyses. The status in results.json may be completed/partial/failed; record unfinished work truthfully. Molecular models, numerical results and conclusions must each be traceable.

Files in this directory, general chemical-method/software documentation and computational tools are permitted. The source paper, its mechanism or energy answers, authors' computed structures, historical runs, private scoring files and other systems' results are not permitted inputs. General web literature searches are not enabled. Supplied experimental facts serve only as explanatory context; repeating them without computational support does not constitute a scientific result.
