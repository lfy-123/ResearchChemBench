## Scientific question

For the supplied homogeneous Pd-catalyzed Heck reaction of 1,2-dihydronaphthalene and 4-tert-butyliodobenzene, develop a computational explanation of α/β product preference under the two sets of conditions, and of how the cost of accessing productive states and competition within those states jointly affect reactivity. Investigate substrate dependence using styrene as a matched model-olefin control.

## Input files

- `data/molecules.json`: Directly parseable SMILES, atom-mapped SMILES, atom/bond tables and necessary stereochemical and coordination constraints.
- `data/precursor_definitions.json`: Text definitions of metal/salt precursor components, formal oxidation states and known initial coordination.
- `data/facts_and_conditions.json`: Conditions, initial states and supplied experimental facts.
- `data/README.md`: molecular identity, numbering and structural constraints.

Chemical numbering and JSON atom IDs are separate systems; preserve an explicit mapping. Retain the supplied stereochemical, coordination and initial charge/spin constraints when constructing three-dimensional models.

## Scope

Study the two supplied sets of conditions and one matched substrate control. Propose catalytic-state models independently; the active catalyst composition is not provided in advance. The supplied selectivities are known observations to explain computationally.

## Required results

1. Explain the α/β preference under each of the two supplied conditions from competing formation calculations. Report matched Gibbs activation energies and their difference for each condition, defining the catalyst state and subtraction order.

2. Explain how catalyst coordination changes access to productive olefin-bound states. Compute and compare the corresponding access/binding free energies in the relevant coordination environments, keeping this cost distinct from competition within an accessible state.

3. Use styrene as a matched control. Compute its binding/access free energies relative to the cyclic olefin, its competing α/β formation Gibbs barriers and their difference, and the insertion-barrier difference between styrene and the original substrate on matched catalyst references. Explain the supported substrate dependence without inferring exact rates or yields.

Choose mechanisms, molecular models, electronic states, conformers and methods independently; declare simplifications and compare alternatives sufficient to support the conclusions. Validate claimed minima and transition states with convergence, vibrational and chemical-assignment evidence, and claimed pathways with reaction modes, endpoints or equivalent connectivity evidence. Define each energy as electronic energy, enthalpy or Gibbs energy and state temperature, solvent, standard state, low-frequency treatment, component inventory and common reference. Support a barrierless assignment with a computed profile and defined reference. Explain method-sensitive or near-degenerate results and the scope of the supported inference.

Continue the research until you reach the final conclusions; do not end prematurely by submitting an unfinished report.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_schema.json` and `submission_guide.md`. Link each conclusion to its computed quantities and retained native inputs, outputs, geometries and supporting analyses.
