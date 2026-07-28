---
software_id: gaussian
versions: ["16"]
topics: [quickstart, input-syntax]
aliases: [Gaussian input, route section, blank lines]
example_path: chemistry_toolbox/examples/native/gaussian/optimization/input.gjf
---
# Gaussian Quickstart

## Required sections
Place Link 0 commands first, then one route section beginning with `#`. Follow it with a blank line, a non-empty title, another blank line, charge and multiplicity, coordinates, and a final blank line.

## Resources
Make `%NProcShared` equal to or lower than the scheduler CPU request. Keep `%Mem` below the whole-job memory allocation.

## Termination
Require `Normal termination of Gaussian`. Separately verify SCF and optimization convergence and inspect imaginary frequencies when `Freq` was requested.
