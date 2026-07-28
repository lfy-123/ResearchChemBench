---
software_id: orca
versions: ["6.1.1"]
topics: [optimization-frequency, optimization, frequency]
aliases: [ORCA Opt Freq, geometry optimization, frequency calculation]
example_path: chemistry_toolbox/examples/native/orca/optimization_frequency/input.inp
---
# ORCA Optimization and Frequency

## Setup
Use `Opt` for geometry optimization and `Freq` only when a Hessian and vibrational analysis are required. A combined `Opt Freq` job evaluates frequencies at the final geometry.

## Validation
Require normal termination, optimization convergence, and the expected number of vibrational modes. A minimum should have no meaningful imaginary frequencies; a transition state should have one intended imaginary mode and must be checked separately.

## Restart
Do not claim convergence from the last geometry of an interrupted job. Restart from a collected geometry or ORCA restart artifact using syntax compatible with the installed version.
