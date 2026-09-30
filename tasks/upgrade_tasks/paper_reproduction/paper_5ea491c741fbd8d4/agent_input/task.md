# Scientific objective

Determine whether molecular-neighbor contact surface area and fixed-crystal-geometry interaction energy give compatible rankings for the source crystal of the specified isoxazole 1a. Test whether area or shortest contact is a defensible proxy for stabilization, with separate geometric, electronic-energy and uncertainty evidence.

# Author-provided scientific guidance

The authors describe C–H···O motifs and aromatic contacts in the measured P21/c crystal and use CrystalExplorer 17.5 Hirshfeld fingerprints to discuss packing. Their isolated-molecule route is Gaussian 09 B3LYP/6-311+G(d,p); a later sentence in the method section says 6-31+G(d,p), so record that inconsistency instead of treating the names as equivalent. The contact interpretation is the author hypothesis to test, not an interaction-energy ranking. The original Hirshfeld procedure normalizes H distances to neutron values. Fixed-geometry dimer energies, counterpoise treatment, molecule-resolved area/energy ranking and cutoff controls below are benchmark additions; they were not established by the paper’s isolated orbital calculation. No author energy winner is supplied.

# Public inputs and scientific boundaries

`system.json` defines the complete 27-atom E molecule and a neutral singlet monomer; each dimer contains two identical neutral singlets (54 atoms, total charge 0, singlet). `crystal_source_specification.json` contains measured cell metadata only. A source-CIF atom-label mapping, occupancy/disorder model and space-group expansion remain prerequisites. The finite crystal-neighbor comparison does not establish a lattice free energy, docking affinity or biological efficacy. The CIF will be an observed input after authentication, not an optimized answer to predict.

This development package is BLOCKED. Read `data/inputs/development_gate.json`. Expanded numerical references and acceptance intervals have not been calibrated. Do not launch the full matrix until its prerequisites are actually closed. An evidence-backed diagnosis is a valid incomplete submission, not a successful result. Use only supplied public identities and observations; the paper, SI, author endpoint coordinates, private snapshots and evaluator are not authorized research inputs.

# Required scientific validation/investigation

After the source-CIF gate is closed, reconstruct intact molecules and every symmetry-inequivalent neighbor defined by `controls.json`, preserving symmetry operator, lattice translation and multiplicity. Validate composition and each graph-to-CIF atom correspondence. Obtain molecule-resolved surface partitions and contact types using a reproducible area definition; assess mesh convergence. For every primary pair compute dimer and frozen monomers consistently, including own/ghost-basis energies to expose BSSE. Recompute signed interaction energies and compare area, distance and energy rankings pairwise, using actual uncertainty to identify ties. Repeat neighbor selection at the second stated cutoff and quantify one decisive energy/geometry sensitivity. A surface contact percentage is not an energy decomposition. Do not manufacture a required pi pair before the real source packing is available.

Test at least two distinguishable explanations with the required numerical comparisons. Support, refutation and evidence-sufficient indistinguishability are equally acceptable; missing core controls are incomplete. Quantify one decisive sensitivity using both baseline and perturbed results. Optional extensions are not scored requirements.

# Deliverables

Submit `report/results.json` and readable `report/report.md`, following `submission_schema.json` and `submission_guide.md`. Include actual job inputs, raw outputs, mapped geometries, analysis tables/scripts and an artifact index with SHA-256 hashes. References must resolve to submitted files under `outputs/` or `report/`. Preserve failed attempts and distinguish constraints from free minima. Record actual engine launches, failures, engine wall time and allocated CPU core-hours; do not count analysis work units as launches. A `bounded_failure` or `partial` submission identifies missing endpoints and evidence without fabricating unavailable numbers. Scientific completion requires the entire core comparison and valid underlying evidence.
