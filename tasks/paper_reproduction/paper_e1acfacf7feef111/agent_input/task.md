# Scientific objective

Reproduce the authors' formula-unit cluster calculation for (C10H13N4)[BiBr4]·2H2O using the supplied 38-atom structure in `data/inputs/formula_unit_cluster.xyz`. Test whether the author model reproduces local Bi(III) coordination and the six characteristic low-frequency Bi–Br Raman bands. Report optimized Bi–Br distances, Br–Bi–Br angles, six assigned low-frequency Raman frequencies, and quantitative comparison metrics.

# Public inputs and scientific boundaries

`data/inputs/formula_unit_cluster.xyz` contains one [BiBr4]− anion, one monoprotonated C10H13N4+ cation and two water molecules, for a neutral singlet 38-atom cluster. Atom 1 is Bi and atoms 2–5 are Br; Cartesian coordinates are in Å and were converted from SI fractional coordinates. `data/inputs/reference_observables.json` gives the six observed Raman bands and the crystal-derived direct Bi–Br/Br–Bi–Br pairings required for the metrics. The legacy five-atom file is retained only as a v0 task-error audit artifact and is not the evaluated model. Periodic chains, electronic band gaps and optical emission are outside scope.

# Required scientific validation/investigation

Use the source route as the primary reproduction protocol: Gaussian DFT with B3LYP/GENECP, LANL2DZ ECP/basis for Bi and Br, and 6-311++G* for H/C/N/O. Optimize all 38 atoms and establish that the returned structure is a minimum using a frequency calculation; report charge, multiplicity, convergence and any imaginary-frequency findings. Assign six distinct low-frequency modes to Bi/Br motion, retaining mode identity and computed wavenumber. Deduplicate only by explicit mode identity. Report each direct distance and angle with explicit atom-index identity and observable pairing, and each frequency with explicit mode identity and observed-band pairing; calculate MAE for the four direct distances, MAE for the six direct angles and RMSD for the six frequencies, with units and pairing rules. Completion requires a converged optimization, no unaccounted imaginary frequency, six identified modes, and all three metrics or a scientifically justified bounded-failure report.

# Deliverables

Submit `report/results.json` following the schema. Include the computational provenance, optimized geometry, frequency assignments, mappings, metrics, validation status and a concise conclusion. A bounded-failure branch is allowed only with explicit reason and attempted work.
