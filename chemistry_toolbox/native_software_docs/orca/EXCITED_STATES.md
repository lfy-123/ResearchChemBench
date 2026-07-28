---
software_id: orca
versions: ["6.1.1"]
topics: [excited-states, tddft]
aliases: [ORCA TDDFT, vertical excitations]
---
# ORCA Excited States

## Setup
Declare the ground-state method and basis, then use a `%tddft` block with an explicit number of roots and any spin-state settings required by the scientific task. Close the block with `end`.

## Validation
Require SCF convergence before interpreting excited states. Record the requested root count, returned root count, state energies, oscillator strengths, and any root-following warnings.
