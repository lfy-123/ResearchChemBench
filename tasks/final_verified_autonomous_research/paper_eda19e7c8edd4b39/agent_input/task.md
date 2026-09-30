# Scientific objective

Independently determine the neutral substitutional Ni-vacancy and Al-vacancy formation energies in ordered bulk β-NiAl (B2), compare the two defect classes, and state what conclusion about relative defect propensity is justified by the calculation. The benchmark is route-neutral: discover and justify your own computational model and validation strategy.

# Public inputs and scientific boundaries

Use `data/inputs/beta_nial_b2_primitive.poscar` as the ordered B2 conventional cell: cubic lattice parameter 2.890 Å, Ni at fractional (0,0,0), Al at (0.5,0.5,0.5), one formula unit, neutral periodic solid. `system_definition.json` fixes the defect identities and requires a neutral charge state. Build a periodic supercell, remove exactly one Ni for the Ni-vacancy state and exactly one Al for the Al-vacancy state. The measurement is the 0 K electronic formation energy in eV under the Ni-rich primary reservoir convention. The public problem contains no author mechanism or candidate route; do not use the paper, SI, source-data archive or general web as inputs.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

Primary benchmark reservoir convention (Ni-rich): E_f(V_X) = E_defect - E_pristine + mu_X, for one removed atom from the same supercell. Set mu_Ni = E(fcc Ni)/atom and mu_Al = E(B2 beta-NiAl)/formula_unit - mu_Ni. Compute reservoir and host energies consistently and report them with atom/formula-unit normalization. A different reservoir convention may be reported separately but does not define the primary comparison.

# Required scientific validation/investigation

Propose and execute a reproducible periodic first-principles calculation or a justified equivalent. Generate and compare the pristine, Ni-vacancy and Al-vacancy states under one coherent convention. Validate the atom identities, charge, relaxation and numerical convergence or sensitivity, and report coverage of the settings explored. Completion is reached when both formation energies, their difference/order, validation evidence, and an independently reasoned interpretation are available.

The Ni-rich reservoir definition above is the benchmark comparison convention. It is not a claim that the source article uniquely specified those chemical potentials. Keep the reservoir normalization and both formation energies explicit when interpreting the result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For a completed investigation, include the discovered method, all reference and defect energies, formation energies with units and reservoir convention, ordering, validation evidence, conclusion. If the investigation remains bounded by a missing calculation or unresolved sensitivity, use the bounded-failure branch and identify the missing calculated result without fabricating energies or an ordering. Do not invent an experimental result or claim that bulk vacancy energetics alone proves a complete surface mechanism.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
