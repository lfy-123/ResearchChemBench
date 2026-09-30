# Scientific objective

Determine, from first-principles calculations on the supplied molecular system, the relative electronic binding strength of the explicitly named TEA+–PC, DED2+–PC and BF4−–PC ion–solvent pairs, and assess what that ordering does and does not establish about competitive solvent association. The benchmark evaluates the computed ordering and a defensible validation record; it does not assume a mechanism beyond the defined isolated-pair observable.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It uniquely defines the four molecular graphs, formal charges, singlet multiplicities, atom-element lists, pair IDs, and binding-energy equation. Generate 3-D geometries independently from the graphs. PC is racemic/unspecified at its ring stereocenter. The scored object is the electronic energy difference for isolated gas-phase pairs and monomers in kcal/mol. Bulk electrolyte concentrations, electrode surfaces, experimental measurements, and any paper-specific computational route are outside the public problem and cannot substitute for the requested calculation.

# Required scientific validation/investigation

For every named pair, explore at least two distinct starting orientations and any conformers needed to justify coverage, optimize the complex and isolated components with a stated method, and validate retained minima by frequencies or an equivalently justified minimum test. Keep unique candidate IDs and per-candidate orientation, convergence, minimum-test and energy-bookkeeping evidence. Deduplicate using a stated structural criterion. Perform at least one sensitivity check and independently decide whether the resulting ordering is robust. Completion requires one or more validated retained minima and traceable component energies for all three pairs, a reported ordering, sensitivity outcome, coverage statement, and limitations. Stop when these conditions are met and further tested orientations no longer alter the selected ordering; if a condition cannot be met, submit the bounded-failure branch with actual coverage and the scientific reason.

# Deliverables

Submit `report/results.json` with the required schema. State the method, energy sign convention, per-pair candidate results and validation, ordering, sensitivity, coverage, and conclusion. Do not report an author route or claim exact reproduction of an unavailable author geometry.
