---
software_id: orca
versions: ["6.1.1"]
topics: [quickstart, input-syntax]
aliases: [ORCA input, ORCA blocks, xyz coordinates]
example_path: chemistry_toolbox/examples/native/orca/single_point/input.inp
---
# ORCA Quickstart

## Input structure
Start the simple keyword line with `!`. Close every `%` block with `end`. Provide coordinates with `* xyz charge multiplicity` followed by element and Cartesian coordinates, then a final `*`.

## Staging
Stage the input as `input.inp` and call `orca input.inp`. If the deck references external coordinates or guess files, stage those exact targets too.

## Resources
Match `%pal nprocs N end` to the scheduler CPU request. Treat `%maxcore` as memory per processing core in MB and keep the total below the job allocation.

## Termination
Require `ORCA TERMINATED NORMALLY`. For SCF work also verify `SCF CONVERGED`; for optimization verify the geometry convergence message.
