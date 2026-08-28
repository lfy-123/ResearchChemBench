# Scientific objective

Determine the solution-phase Gibbs free-energy difference between the two supplied neutral singlet Ir(III)–salen-NHC isomers at 339 K and derive the Boltzmann population ratio [2]/[1]. Use the calculations to state which labeled isomer is thermodynamically preferred within the chosen model and how strongly that conclusion is supported.

# Public inputs and scientific boundaries

`data/inputs/complex_1.xyz` and `complex_2.xyz` are complete Cartesian geometries for the two labeled isomers, with element symbols and Å coordinates. Each is neutral (charge 0) and closed-shell singlet (multiplicity 1). The physical boundary is the isolated molecular complex in implicit THF at 339 K; exclude crystal packing, counterions, explicit solvent, and kinetics. Measure Gibbs free energy for each labeled input, ΔΔG(1–2) = G(1) − G(2) in kJ mol−1, and [2]/[1]. No author mechanism or preferred isomer is supplied; develop the interpretation from the computed evidence.

# Required scientific validation/investigation

Independently select and document a defensible electronic-structure, basis/ECP, solvation, thermal, and software protocol. Optimize both labeled inputs and use vibrational information to establish minima; report imaginary modes or a bounded failure if this cannot be done. Compute both Gibbs energies at 339 K, convert units consistently, and recompute the ratio from ΔΔG, temperature, and a stated gas constant. Completion means both labeled endpoints and validation records are present, or a reproducible technical failure is fully documented. Stop after both inputs and all checks have been attempted, and report uncertainty, model sensitivity, and any limitation on interpreting a thermodynamic ratio as an experimental yield.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-isomer validation and method records, available energies, derived quantities, equations/constants, and an evidence-based conclusion. If a calculation fails, use the failure branch with concrete details rather than fabricated values.
