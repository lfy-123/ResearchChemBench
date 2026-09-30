# Scientific objective

Independently test the structural and vibrational assignment of neutral singlet IrCl2(eta2-O2NO)(PPh3)2. The authors' qualitative scientific route is that an alkyl-nitrite adduct exposed to oxygen/air can give a bidentate nitrato complex; test the proposed nitrate coordination motif and its calculated IR signature independently. Do not assume any source numerical value. Report the optimized structure, the nitrate-associated harmonic modes, and whether the results support the bidentate assignment.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the coordination environment as pseudo-octahedral and use the nitrate stretching pattern to support the structural assignment.

**Candidate route or mechanism.**
Consider a pseudo-octahedral starting arrangement and test assignments of nitrate-associated bands to symmetric and asymmetric NO2 stretching motions within the nitrate ligand.

**Discriminating evidence.**
The authors use DFT geometry optimization and harmonic-frequency calculations, comparing Ir-O and N-O distances, the nitrate bite angle and O-N-O angles with molecular X-ray observations, and assigned nitrate stretching bands with KBr IR observations.

# Public inputs and scientific boundaries

Use `data/inputs/complex_specification.json`. It uniquely defines formula C36H30Cl2IrNO3P2, neutral charge, singlet multiplicity, Ir1/Cl1/Cl2/P1/P2/N1/O1/O2/O3 labels, two PPh3 ligands, and O1/O2 bidentate nitrate connectivity. The model is one isolated molecule; omit crystal packing, solvent, counterions and periodicity. You may construct 3D coordinates and choose software, relativistic treatment, basis, functional, convergence settings and frequency scaling. The measured comparison quantities are Ir1-O1/O2, N1-O1/O2/O3, O1-Ir1-O2, O1-N1-O2, O1-N1-O3, O2-N1-O3, and nitrate-associated IR frequencies. The experimental comparison is to the molecular X-ray and KBr IR observations in `data/inputs/experimental_xray_ir_boundary.json`, not to a particular crystal cell or a hidden numerical target.

# Required scientific validation/investigation

Document the initial-geometry construction and any conformers considered. Optimize the specified connectivity without silently changing protonation, charge, multiplicity or nitrate hapticity. Establish a genuine stationary point using a vibrational calculation or an explicitly justified equivalent; report imaginary frequencies and explain any unresolved saddle-point issue. Identify the nitrate modes by inspecting displacement vectors or an equivalent mode-assignment procedure, and report the mapping from each selected mode to its frequency. Validate object identity by reporting the Ir-O and N-O bond identities and the O1-Ir1-O2 bite angle. Compare the resulting observables with the experimental observations supplied in `data/inputs/experimental_xray_ir_boundary.json` and state whether agreement supports the bidentate assignment. Hidden evaluator targets are not agent inputs. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include methods, starting-structure provenance, candidate/conformer records, stationary-point validation, named observables, nitrate mode assignments, comparison, conclusion. Include enough data for another researcher to identify every scored atom pair and mode. A bounded-failure branch is allowed only when it contains the attempted calculations, diagnostics, coverage and a scientifically honest failure cause.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
