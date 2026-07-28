---
software_id: gaussian
versions: ["16"]
topics: [optimization-frequency, optimization, frequency]
aliases: [Gaussian Opt Freq, geometry optimization, vibrational frequencies]
example_path: chemistry_toolbox/examples/native/gaussian/optimization/input.gjf
---
# Gaussian Optimization and Frequency

## Route
Use explicit method and basis with `Opt`, `Freq`, or both. Do not infer a minimum or transition state only from normal termination.

## Validation
An optimization must report completion. A frequency calculation must return the expected modes. A minimum normally has no chemically meaningful imaginary mode; a transition-state candidate normally has one intended imaginary mode.
