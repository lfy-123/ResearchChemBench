# Scientific objective

Determine the low-frequency harmonic vibrational modes of neutral singlet Rhodamine 101 (C32H30N2O3) in methanol for S0 and the first singlet excited state S1. Report state-matched frequencies in the 0–125 cm−1 window, mode correspondence, deviations/summary metrics, and a scientifically bounded conclusion.

# Author-provided scientific guidance

The authors qualitatively motivate testing whether state-specific quantum-chemical vibrations can explain SLT peaks and mode assignments; independently plan and execute calculations that test this motivation.

# Public inputs and scientific boundaries

`data/inputs/rhodamine101_S0.xyz` and `rhodamine101_S1.xyz` are explicit 67-atom Cartesian starting geometries for the same molecule, each with charge 0 and multiplicity 1. S0 means the electronic ground state; S1 means the first singlet excited state. The solvent boundary is methanol represented by a declared continuum or other explicitly described solvent treatment. The measured/computed observable is the harmonic vibrational frequency in cm−1; only modes whose frequency lies in 0–125 cm−1 are in scope. Experimental comparison is to the state-matched SLT peak positions in `data/inputs/experimental_slt_peaks.csv`; a blank observation in that file must remain missing, not be imputed. Do not use the paper, SI, or general web as input.

The two supplied geometries originate from source-optimized state structures. They define the provided starting objects for a vibrational-property investigation; this task does not test independent discovery of those geometries. Frequencies, displacement assignments and comparison results must still be computed.

# Required scientific validation/investigation

Design a reproducible calculation route and state all model choices, convergence settings, software, and post-processing. Optimize or otherwise converge an S0 structure and an S1 structure appropriate to their electronic states, then calculate harmonic frequencies for both. Provide convergence/stationarity evidence and report any imaginary modes rather than silently discarding them. Match modes using a stated, reproducible identity rule (frequency plus displacement/structural character), retain state and mode identity, and calculate per-state and aggregate deviations only for observed pairs. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Match S0/S1 physical modes using atom-mapped displacement or local-coordinate evidence before interpreting shifts; equal integer mode numbers alone do not establish correspondence. Retain mixed modes, mode reordering, near-zero shifts and supported exceptions. Missing experimental peaks remain missing and never contribute zero errors.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include the route, software/model choices, convergence and imaginary-frequency evidence, state-specific mode arrays with unique mode labels, match evidence, numeric metrics with units, and a conclusion explaining whether the calculated modes support the qualitative author hypothesis under the stated computational conditions. Include failed-attempt information when applicable.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
