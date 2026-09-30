# Scientific objective

For the named neutral singlets DBC-Ph and DBC-Nap, calculate S0 and first-singlet S1 geometries, the two explicitly defined inter-ring dihedrals, and vertical singlet transitions at both optimized geometries. Compare substituents and state whether the calculations support the proposal.

# Author-provided scientific guidance

Independently test the authors' qualitative proposal that the DBC core and para-aryl-substituted N-phenyl unit form a moderately twisted chromophore with predominantly DBC-localized occupied orbitals and aryl-extended accepting orbitals.

# Public inputs and scientific boundaries

Both XYZ files are independently embedded, unoptimized initial geometries, not converged S0 results. The corresponding `*_identity.json` files supply explicit atom-mapped chemical graphs; use these graphs and charges as authoritative and optimize the coordinates. The existing s0 filename suffix labels the starting electronic state only. Preserve or explicitly map atom IDs through S0/S1 optimization.

Use `data/inputs/system_definition.json` and its two complete XYZ files (DBC-Ph C32H21N, 54 atoms; DBC-Nap C36H23N, 60 atoms). The XYZ atom order is authoritative; do not infer identity from an internal label. Both molecules are neutral, closed-shell singlets initially. The physical boundary is one isolated molecule in implicit toluene, S0 and the first singlet S1, with vertical electronic transitions evaluated at optimized geometries. Report wavelengths in nm, oscillator strengths dimensionless, and dihedrals in degrees. You choose and disclose method, basis, solvent implementation, convergence settings and any conformer generation. The public files contain no target values.

# Required scientific validation/investigation

Distinguish the DBC–N-phenyl and N-phenyl–para-aryl rotations for each molecule and each state; record explicit atom tuples and, if a least-squares inter-ring plane angle is used, its atom selections and acute-plane convention. Evaluate the qualitative interpretation separately for S0 and S1: state-dependent twisting, orbital mixing and supported exceptions are valid outcomes, not reasons to force every state into a single twist category.

Plan and execute a reproducible route for both molecules: validate connectivity and charge, optimize S0 and S1 (or provide a scientifically justified bounded-failure explanation), and compute transitions at both optimized geometries. For each molecule, explicitly identify the four atom indices for each dihedral and verify state optimization/convergence and singlet character. At each optimized geometry (S0 and S1), report at least the five lowest singlet roots separately for each molecule, with root index, wavelength, oscillator strength and dominant configuration where available. In each transition record, `state` labels the optimized geometry, not the initial state of an S1→Sn excited-state-absorption calculation; use ordinary vertical singlet excitation energies at that geometry. Include roots 1–5 once per geometry, with `root` numbered by increasing excitation energy; retain higher roots separately in the same array if computed, without duplicate (state, root) records. Compare orbital localization on DBC versus aryl fragments using a disclosed population or visual criterion. Completion requires validated results for both molecules. Otherwise submit a failure/partial report identifying the failed state, attempted settings and specific failure cause.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`. Include calculation provenance, geometries or paths to them, convergence/state checks, per-molecule dihedrals and transitions, orbital-localization evidence, a Ph-versus-Nap comparison, an explicit conclusion about support for the qualitative proposal. Numeric values must be your calculations, not copied from the paper.
