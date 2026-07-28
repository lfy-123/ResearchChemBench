---
software_id: vasp
versions: ["6"]
topics: [relaxation, optimization]
aliases: [VASP geometry optimization, ionic relaxation, cell relaxation]
---
# VASP Relaxation

## Controls
Set `IBRION`, `NSW`, `EDIFFG`, and `ISIF` explicitly for the intended atomic or cell degrees of freedom. Encode atom constraints in POSCAR selective dynamics when required.

## Validation
Verify both electronic convergence at each ionic step and the declared ionic stopping condition. Collect `CONTCAR` only after confirming it is complete and consistent with the final step.
