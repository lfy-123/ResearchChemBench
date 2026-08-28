# Scientific objective

Determine the low-frequency harmonic vibrational modes of neutral singlet Rhodamine 101 (C32H30N2O3) in methanol for S0 and the first singlet excited state S1. The authors qualitatively motivate testing whether state-specific quantum-chemical vibrations can explain SLT peaks and mode assignments; independently plan and execute calculations that test this motivation. Report state-matched frequencies in the 0–125 cm−1 window, mode correspondence, deviations/summary metrics, and a scientifically bounded conclusion.

# Public inputs and scientific boundaries

`data/inputs/rhodamine101_S0.xyz` and `rhodamine101_S1.xyz` are explicit 67-atom Cartesian starting geometries for the same molecule, each with charge 0 and multiplicity 1. S0 means the electronic ground state; S1 means the first singlet excited state. The solvent boundary is methanol represented by a declared continuum or other explicitly described solvent treatment. The measured/computed observable is the harmonic vibrational frequency in cm−1; only modes whose frequency lies in 0–125 cm−1 are in scope. Experimental comparison is to state-matched SLT peak positions where available; a missing observation must remain missing, not be imputed. Do not use the paper, SI, or general web as input.

# Required scientific validation/investigation

Design a reproducible calculation route and state all model choices, convergence settings, software, and post-processing. Optimize or otherwise converge an S0 structure and an S1 structure appropriate to their electronic states, then calculate harmonic frequencies for both. Provide convergence/stationarity evidence and report any imaginary modes rather than silently discarding them. Match modes using a stated, reproducible identity rule (frequency plus displacement/structural character), retain state and mode identity, and calculate per-state and aggregate deviations only for observed pairs. Completion requires both states attempted, final geometries and frequency outputs recorded, and every in-scope mode either matched, explicitly unmatched, or reported as a bounded failure. Stop when both state calculations have converged and the 0–125 cm−1 mode list and validation table are complete; if a calculation cannot converge, stop after a documented finite set of remedial attempts and report the limitation.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include the route, software/model choices, convergence and imaginary-frequency evidence, state-specific mode arrays with unique mode labels, match evidence, numeric metrics with units, and a conclusion explaining whether the calculated modes support the qualitative author hypothesis within the stated scope. Include limitations and failed-attempt information when applicable.
