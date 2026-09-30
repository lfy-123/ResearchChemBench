# Scientific objective

For the explicitly supplied neutral singlet 1M-TIPS model geometry, independently determine the intense lowest-energy vertical UV-vis absorption and explain its electronic character. Report wavelength, oscillator strength, dominant orbital transition or transition-density description, and whether the excitation is π–π* within the stated model.

# Public inputs and scientific boundaries

Use `data/inputs/1M-TIPS.xyz`, a 102-atom Cartesian geometry in Å, together with `data/inputs/system.json` (charge 0, multiplicity 1, implicit CHCl3 solvent). The model is the supplied C58H42Si2 molecular system; do not add the experimental dodecyl groups or infer a different protonation, charge, or spin state. The measured endpoint is a vertical electronic excitation from the optimized ground-state geometry, including wavelength (nm), oscillator strength (dimensionless), state identity, and orbital/transition character. Report all computational choices, convergence settings, and any solvent approximation.

The prescribed model coordinates originate from a source-optimized structure. The scored target is the calculated absorption and its electronic assignment, not discovery of that geometry; the input contains no excitation energies or oscillator strengths.

# Required scientific validation/investigation

Validate that the ground-state structure is converged and a true stationary point by a frequency or an equivalently justified curvature/stability test; report imaginary-frequency findings. Generate and inspect enough low-lying excited states to identify the intense lowest-energy absorption rather than selecting a state by an assumed index. Characterize the selected transition using orbital contributions, transition-density analysis, or an equivalent state-resolved diagnostic, comparing plausible descriptions where the calculation supports more than one interpretation. Deduplicate equivalent state descriptions, retain the selected state identity and evidence, and check that the selected state is converged. Completion requires a converged geometry/ground state, a validated excited-state calculation, and an explicit state-selection justification. Stop once these conditions and all deliverables are met. Do not claim a spectral assignment from an unvalidated state.

# Deliverables

Submit `report/results.json` conforming to the supplied schema. Report validated results when available, or use the partial/unsuccessful submission branch below; do not substitute guessed values for a calculation. Numerical values must be the Agent's calculations, not an external answer. Include enough provenance to reproduce the actual investigation and a concise evidence-based conclusion about the transition character.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.

# Partial or unsuccessful submission

Use `status: "partial"` or `status: "bounded_failure"` when required calculations or analyses remain unavailable. Retain all actual partial results in their original fields. Include `failure` with a nonempty `reason`, a nonempty `missing_observables` array naming the unavailable result fields, and an `evidence` array of existing input, output or diagnostic paths (empty only if no artifact was produced). Explain which calculation failed or was not attempted; do not invent output files.

For these two statuses, the schema permits `null` for the specified unavailable calculated values, selected structures, state assignments or output paths. Keep the known molecular identities, charges, multiplicities, units and attempted methods. Report actual counts, including zero generated/validated candidates when appropriate. An unavailable frequency result is `null`, not zero imaginary modes or an empty list claiming a completed frequency analysis. A genuinely computed zero or an established empty imaginary-mode list remains valid evidence. A missing comparison is not a zero difference or zero RMSE.

Other statuses, and omission of status where the original schema permits it, retain the complete-result format. Passing this format check does not establish scientific completion: uncomputed endpoints receive no completion credit, and existing scientific rules still assess the actual evidence. This reporting branch does not change the scientific target, required successful investigation, or numerical acceptance criteria.
