# Scientific objective

Determine computationally how replacing the terminal phenyl ring of DBC-Ph with a 1-naphthyl group in DBC-Nap changes ground- and first-singlet-excited-state geometry, vertical singlet spectroscopy and frontier-orbital localization in toluene. Establish whether the calculated differences provide a defensible structure–property explanation within the stated model boundary.

# Public inputs and scientific boundaries

Both XYZ files are independently embedded, unoptimized initial geometries, not converged S0 results. The corresponding `*_identity.json` files supply explicit atom-mapped chemical graphs; use these graphs and charges as authoritative and optimize the coordinates. The existing s0 filename suffix labels the starting electronic state only. Preserve or explicitly map atom IDs through S0/S1 optimization.

Use `data/inputs/system_definition.json` and its two complete XYZ files (DBC-Ph C32H21N, 54 atoms; DBC-Nap C36H23N, 60 atoms). The XYZ atom order is authoritative; do not infer identity from an internal label. Both molecules are neutral, closed-shell singlets initially. The physical boundary is one isolated molecule in implicit toluene, S0 and the first singlet S1, with vertical electronic transitions evaluated at optimized geometries. Choose and disclose method, basis, solvent implementation, convergence settings and any conformer generation. No author route, target values or answer-bearing structures are supplied.

# Required scientific validation/investigation

Distinguish the DBC–N-phenyl and N-phenyl–para-aryl rotations for each molecule and each state; record explicit atom tuples and, if a least-squares inter-ring plane angle is used, its atom selections and acute-plane convention. Evaluate the qualitative interpretation separately for S0 and S1: state-dependent twisting, orbital mixing and supported exceptions are valid outcomes, not reasons to force every state into a single twist category.

Independently formulate and execute a reproducible computational comparison for both molecules: validate connectivity and charge, optimize S0 and S1 (or provide a scientifically justified bounded-failure explanation), and compute transitions at both optimized geometries. Explicitly identify the four atom indices for each dihedral and verify state optimization/convergence and singlet character. At each optimized geometry (S0 and S1), report at least the five lowest singlet roots separately for each molecule, with root index, wavelength, oscillator strength and dominant configuration where available. In each transition record, `state` labels the optimized geometry, not the initial state of an S1→Sn excited-state-absorption calculation; use ordinary vertical singlet excitation energies at that geometry. Include roots 1–5 once per geometry, with `root` numbered by increasing excitation energy; retain higher roots separately in the same array if computed, without duplicate (state, root) records. Use a disclosed population or visual criterion to assess orbital localization. Completion requires validated results for both molecules; otherwise report the failed state, attempts and specific failure cause. Propose and discriminate at least one plausible explanation for any substituent-dependent difference.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`. Include provenance, geometries or paths, convergence/state checks, per-molecule dihedrals and transitions, orbital-localization evidence, the independent Ph-versus-Nap comparison, a final conclusion. Do not claim experimental or literature validation beyond what you compute and explicitly identify.
