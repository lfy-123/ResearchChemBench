---
software_id: orca
versions: ["6.1.1"]
topics: [single-point, energy]
aliases: [ORCA SP, ORCA electronic energy]
example_path: chemistry_toolbox/examples/native/orca/single_point/input.inp
---
# ORCA Single Point

## Preconditions
Use a complete molecular geometry, integer charge, positive multiplicity, explicit method, and explicit basis. The tested example uses a small neutral closed-shell molecule.

## Outputs
Collect the main output and any property files required by later analysis. Extract the final energy only from a normally terminated, converged calculation.

## Common errors
Unknown keyword errors usually indicate a keyword from another ORCA version or a misspelled method. Coordinate parser errors usually indicate a missing final `*`, malformed atom line, or charge/multiplicity placed outside the coordinate header.
