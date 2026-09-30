# Scientific objective

For the explicitly supplied neutral singlet 1M-TIPS model geometry, independently determine the intense lowest-energy vertical UV-vis absorption and explain its electronic character. Report wavelength, oscillator strength, dominant orbital transition or transition-density description, and whether the excitation is π–π* within the stated model.

# Public inputs and scientific boundaries

Use `data/inputs/1M-TIPS.xyz`, a 102-atom Cartesian geometry in Å, together with `data/inputs/system.json` (charge 0, multiplicity 1, implicit CHCl3 solvent). The model is the supplied C58H42Si2 molecular system; do not add the experimental dodecyl groups or infer a different protonation, charge, or spin state. The measured endpoint is a vertical electronic excitation from the optimized ground-state geometry, including wavelength (nm), oscillator strength (dimensionless), state identity, and orbital/transition character. Report all computational choices, convergence settings, and any solvent approximation.

# Required scientific validation/investigation

Validate that the ground-state structure is converged and a true stationary point by a frequency or an equivalently justified curvature/stability test; report imaginary-frequency findings. Generate and inspect enough low-lying excited states to identify the intense lowest-energy absorption rather than selecting a state by an assumed index. Generate and test your own explanations of the transition character. Generate and test your own explanations of the transition character. Characterize the selected transition using orbital contributions, transition-density analysis, or an equivalent state-resolved diagnostic, comparing plausible descriptions where the calculation supports more than one interpretation. Deduplicate equivalent state descriptions, retain the selected state identity and evidence, and check that the selected state is converged. Completion requires a converged geometry/ground state, a validated excited-state calculation, and an explicit state-selection justification. Stop once these conditions and all deliverables are met. Do not claim a spectral assignment from an unvalidated state.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Report a successful validated result; do not substitute guessed values for a calculation. Numerical values must be the Agent's calculations, not an external answer. Include enough provenance to reproduce the actual investigation and a concise evidence-based conclusion about the transition character.
