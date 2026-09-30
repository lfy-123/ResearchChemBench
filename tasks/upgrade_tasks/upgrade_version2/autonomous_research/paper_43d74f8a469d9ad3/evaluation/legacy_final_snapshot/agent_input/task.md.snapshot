# Scientific objective

Determine the ground-state electronic torsion-energy profile of organoboron ester 1 for rotation about the bond joining boron to its aryl ring. Report relative E(theta), the minimum and maximum scan energies, and the implications of the result for rotational relaxation and photostability within the stated model.

# Public inputs and scientific boundaries

Define the angle using a consecutive X–B–Cipso–Cortho tuple with X bonded to B on the non-aryl side. Record the CIF labels and working atom indices. Rotate the complete 3,5-dimethylphenyl branch about B–Cipso; retain the rest of the same optimized reference geometry. The geometric period is 360°: 360° coincides with 0°, whereas the separately sampled 345° and 0° energies need not be equal.

Use the supplied immutable `data/inputs/ccdc_2441197.cif` and the accompanying `data/inputs/ccdc_record.json` to obtain one complete molecule of compound 1. The CCDC record number is provenance only; CCDC database retrieval is not required or scored. Preserve the CIF connectivity, stereochemistry, neutral charge and singlet state; document any deterministic hydrogen completion. The scanned coordinate is the B–ipso-carbon bond to the 3,5-dimethylphenyl ring, with a fixed ordered four-atom dihedral and atom IDs retained at every point. The requested observable is the ground-state electronic energy relative to the lowest point, in kJ/mol, at angles 0, 15, ..., 345 degrees. This is an isolated-molecule rigid-rotor electronic-energy model: do not interpret it as a solvent free energy, rate, photobleaching quantum yield, or excited-state surface.

# Required scientific validation/investigation

Choose and justify an electronic-structure method, basis, charge/state, geometry treatment, convergence criteria and energy-unit conversion independently. Optimize the starting structure or otherwise justify its use, and provide evidence that the optimized structure is a minimum or clearly label a bounded failure. Generate all 24 fixed-angle structures from one consistent atom mapping, evaluate each point, remove duplicate/missing angles, reference energies to the lowest submitted point, and check continuity across the 345°→0° sampling boundary and geometric closure at 0°/360°. The calculation is complete when all 24 angles have converged energies and the validation checks are reported; otherwise submit the actual completed points and failure diagnostics.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to the schema. Include the profile, scan identity and validation evidence, method and convergence details, minimum/maximum metrics, conclusion, and either successful completion or a truthful bounded-failure record. State the actual angular coverage.
