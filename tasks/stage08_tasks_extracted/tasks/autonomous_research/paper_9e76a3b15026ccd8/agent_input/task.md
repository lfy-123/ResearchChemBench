# Scientific objective

Independently determine the relaxed adsorption energy, O2 center-to-top-layer height, net Bader charge received by O2, and O2 magnetic moment for the fixed neutral triplet O2 molecule in the supplied upright fcc-hollow Ag(111) model. Generate and test your own explanation of whether the computed observables establish substrate-induced spin reduction.

# Public inputs and scientific boundaries

Use `data/inputs/adsorbate_ag111.vasp`, containing 24 Ag atoms in six (111) layers in a 2×2 periodic cell, 15 Å of slab vacuum, and two upright O atoms at the fcc hollow, together with `data/inputs/isolated_o2.xyz`, the neutral triplet reference. The manifest specifies charge, multiplicity, atom identity, and surface spacing. Construct a matching clean Ag slab and isolated-O2 energy reference. The scored system is this single O2 adsorbate on the fixed Ag(111) slab; keep the supplied adsorption site and orientation, and do not add coadsorbates or a molecular overlayer.

# Required scientific validation/investigation

Select and justify your own computational method and analysis protocol. Relax the combined system and verify stationarity, identify the atoms used for height and O2 electronic properties, and perform at least one explicit numerical stability check. Record convergence evidence for the combined, clean-slab, and isolated-molecule references and quantify changes in the reported observables. Completion requires converged reference energies, a traceable relaxed structure, and reproducible charge/moment analysis. Stop once those conditions and a reasoned conclusion are met; if they cannot be met, use the bounded-failure branch with diagnostics, attempted scope, and limitations.

# Deliverables

Submit `report/results.json` according to the local `submission_schema.json`. Report method, validation, object identity, all observables with units, and a conclusion about spin reduction, or provide the bounded-failure branch without invented numbers. Include auditable output paths or hashes and distinguish direct calculation from interpretation.
