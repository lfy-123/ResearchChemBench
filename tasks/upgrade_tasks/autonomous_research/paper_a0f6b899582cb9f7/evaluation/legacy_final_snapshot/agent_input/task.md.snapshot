# Scientific objective

Independently determine the isolated neutral singlet molecule's optimized geometry, dipole magnitude, full electric quadrupole tensor, and the physically meaningful molecular stacking-axis component for 2,5-di(thiophen-2-yl)pyrazine (M3). Establish whether its optimized structure is planar and whether a short intramolecular N···S contact is present, then state what these calculations do and do not support about its multipolar character.

# Public inputs and scientific boundaries

Use `data/inputs/m3_identity.json` and `data/inputs/m3.xyz`. They define C12H8N2S2, neutral charge, singlet multiplicity, connectivity, atom order and an initial coordinate frame. The coordinates are starting values only. The object is one isolated molecule in vacuum; no crystal, solvent, blend, polymer, or device calculation is requested. Report tensor units, origin, axis convention, and how the stacking axis was selected. For the quadrupole, report the raw Cartesian charge second-moment tensor Q_ij = sum_A(Z_A R_Ai R_Aj) - integral[rho(r) r_i r_j d^3r], including nuclei and electrons at the same declared origin, converted to Debye angstrom. Do not substitute the traceless tensor or its alternative factor-of-three convention. Rotate the full tensor consistently into the declared molecular frame and identify z as the normal to the fitted molecular plane. Report the complete tensor and origin so the component is reproducible; the initial XYZ laboratory z-axis is not the stacking axis. Do not use the paper, SI or general web.

# Required scientific validation/investigation

Choose and justify an electronic-structure method capable of geometry optimization and multipole analysis. Optimize from the supplied structure and, if relevant, additional distinct conformers; deduplicate by connectivity and geometry. Demonstrate convergence and validate a minimum with frequencies or an explicitly justified alternative. Quantify planarity, the shortest chemically relevant N···S distance, dipole magnitude, and all quadrupole components in one declared molecular frame. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, software, convergence/validation evidence, geometry metrics, tensor, axis convention, and a conclusion based only on your independent calculations. Numeric values must be your calculations, not copied references.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
