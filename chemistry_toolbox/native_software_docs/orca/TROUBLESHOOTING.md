---
software_id: orca
versions: ["6.1.1"]
topics: [troubleshooting, errors]
aliases: [ORCA failed, ORCA parser error, SCF not converged]
inputs: ["ORCA input deck", "referenced geometry or basis files"]
outputs: ["stdout.log", "ORCA property and restart files"]
last_smoke_tested: null
---
# ORCA Troubleshooting

## Immediate parser failure
Check the first keyword line, coordinate delimiters, `%` block closure, and exact staged filenames. These failures normally occur within seconds and should be fixed before requesting more resources.

## Memory or parallel failure
Ensure `%pal nprocs` does not exceed the scheduler CPU count and `%maxcore * nprocs` leaves memory headroom. More cores can increase memory use and does not repair invalid input.

## Incomplete result
Absence of `ORCA TERMINATED NORMALLY` means software failure or interruption. A normal marker without SCF or geometry convergence is software success but not scientific convergence.
