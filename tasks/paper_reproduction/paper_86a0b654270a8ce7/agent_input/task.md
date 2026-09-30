# Scientific objective

Determine whether the two supplied neutral singlet Ir(III)–salen-NHC isomers have different solution-phase Gibbs free energies at 339 K, and quantify the resulting ΔΔG(1–2) and Boltzmann population ratio [2]/[1]. The authors' qualitative hypothesis is that intramolecular π–π stacking helps stabilize isomer 2; independently plan and execute calculations that test this thermodynamic hypothesis. Do not assume any numerical result or preferred isomer before calculation.

# Public inputs and scientific boundaries

`data/inputs/complex_1.xyz` and `complex_2.xyz` are the complete Cartesian geometries for the two named isomers, with element symbols and Å coordinates. Each is neutral (charge 0) and closed-shell singlet (multiplicity 1). Use the molecules as isolated complexes with implicit THF solvent at 339 K. The requested endpoint is the molecular Gibbs free energy for each labeled input and the difference ΔΔG(1–2) = G(1) − G(2), in kJ mol−1, plus [2]/[1]. Do not add a crystal lattice, counterion, explicit solvent, or kinetic model.

For comparison after the independent calculation, `data/inputs/experimental_boundary.json` supplies the reported experimental product yield ratio at 339 K. It is an observed yield ratio, not a computed answer or an independently measured equilibrium constant. Explain the limits of comparing it with a thermodynamic population ratio; it must not determine the calculated energies or their sign.

# Required scientific validation/investigation

Choose and document a defensible computational protocol, including electronic structure method, basis/ECP treatment, solvation, thermal standard state, and software/version. Optimize each labeled input and establish whether the resulting structure is a minimum using vibrational information; report imaginary modes or a bounded failure if a minimum cannot be established. Obtain Gibbs free energies at 339 K, convert units consistently, and independently recompute [2]/[1] from ΔΔG using the stated gas constant and temperature. The calculation is complete when both inputs have documented endpoints and validation, or when a reproducible technical failure prevents one endpoint; stop after the two labeled systems and all required checks have been attempted. Report uncertainty and method-sensitivity limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-isomer method and minimum-validation records, G values when available, ΔΔG, ratio, equations/constants, and a conclusion about the thermodynamic hypothesis. A bounded-failure branch is allowed only with concrete failure details and the attempted-system record; do not invent missing numerical values.
