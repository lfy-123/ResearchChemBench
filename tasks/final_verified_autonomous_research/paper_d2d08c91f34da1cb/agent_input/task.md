# Scientific objective

Independently determine and validate the low-frequency harmonic vibrational modes of neutral singlet Rhodamine 101 (C32H30N2O3) in methanol for S0 and the first singlet excited state S1. Establish whether state-specific calculations provide a defensible explanation of the low-frequency vibrational observations, without assuming any author route or mechanism. Report frequencies in the 0–125 cm−1 window, state-matched comparisons, validation metrics, and the conclusion supported by your calculations.

# Public inputs and scientific boundaries

`data/inputs/rhodamine101_S0.xyz` and `rhodamine101_S1.xyz` are explicit 67-atom Cartesian starting geometries for the same molecule, each with charge 0 and multiplicity 1. S0 means the electronic ground state; S1 means the first singlet excited state. The solvent boundary is methanol represented by a declared continuum or other explicitly described solvent treatment. The observable is harmonic vibrational frequency in cm−1; only modes in 0–125 cm−1 are in scope. Experimental comparison is limited to state-matched observed low-frequency peaks supplied in `data/inputs/experimental_slt_peaks.csv`; do not use the paper, SI, or general web as input, and do not claim blank entries are measured.

The two supplied geometries originate from source-optimized state structures. They define the provided starting objects for a vibrational-property investigation; this task does not test independent discovery of those geometries. Frequencies, displacement assignments and comparison results must still be computed.

# Required scientific validation/investigation

Choose and justify an independent computational model and reproducible route. Optimize or otherwise converge an S0 structure and an S1 structure appropriate to their electronic states, calculate harmonic frequencies, and document convergence/stationarity and all imaginary modes. Define a reproducible mode identity/matching rule, preserve state and mode labels, and report matched, unmatched, and failed cases. Provide per-state and aggregate comparison metrics only where observations exist. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Match S0/S1 physical modes using atom-mapped displacement or local-coordinate evidence before interpreting shifts; equal integer mode numbers alone do not establish correspondence. Retain mixed modes, mode reordering, near-zero shifts and supported exceptions. Missing experimental peaks remain missing and never contribute zero errors.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include independent model choices, route, convergence and imaginary-frequency evidence, state-specific modes, matching/coverage evidence, metrics with units, and a final conclusion supported by these data. If no scientifically valid result is obtained, use the bounded-failure branch and provide the attempted calculations and reason.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
