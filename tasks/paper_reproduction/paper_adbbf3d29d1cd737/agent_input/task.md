# Scientific objective

Independently test the authors' qualitative proposal that the Cs/PEG-SrO model's electronic structure changes on moving from gas to aqueous environment in a way consistent with greater stability and lower electrophilic reactivity. Compute, for the fixed model, gas and implicit-water dipole moment, HOMO, LUMO, gap, IP, EA, electronegativity, electrochemical potential, hardness, softness, electrophilicity, and Mulliken charges for the three explicitly identified oxygen atoms (XYZ rows 1, 4, and 6). The authors' proposed interpretation is a hypothesis to test, not a supplied answer.

# Public inputs and scientific boundaries

Use `data/inputs/cs_peg_sro.xyz` exactly as the canonical atom ordering and Cartesian geometry (12 atoms, angstrom). Use `data/inputs/system_spec.json`: neutral singlet boundary, gas and aqueous implicit-water phases, and oxygen rows 1, 4, and 6. The object is an isolated cluster model, not a periodic solid or bulk nanocomposite. Do not use the paper, SI, general web, or unpinned external data. You may choose software and model chemistry, including how to implement continuum water, but document them. No experimental activity, docking, or reaction mechanism is being scored.

# Required scientific validation/investigation

Plan and execute an independent calculation for both phases. First verify atom count, symbols, row identity, charge, multiplicity, and absence of accidental coordinate changes. Establish a defensible electronic state and report optimization/single-point convergence or a scientifically justified bounded failure. For each phase retain the exact calculation settings and extract all requested observables with units and sign conventions. Validate descriptor derivations (including the formulae used for gap, hardness, softness, and electrophilicity), and bind oxygen charges to rows 1, 4, and 6. Compare phase directionality and explain whether the authors' stability/lower-electrophilicity hypothesis is supported. Completion requires either both phases and all requested observables with validation evidence, or a detailed bounded-failure report naming the missing phase/observable and attempted checks. Stop when the two phase calculations, extraction, identity/convergence checks, and limitation analysis are complete; do not expand to other structures or biological calculations.

# Deliverables

Write `report/results.json` and `report/methods_and_validation.md`. JSON must contain calculation status, system identity, method/settings for each phase, observables for each phase, oxygen charges keyed by XYZ row, phase differences/directions, validation evidence, limitations, and a conclusion. If completion is impossible, use the failure branch and provide attempted calculations, missing fields, and a scientifically specific limitation rather than fabricated values.
