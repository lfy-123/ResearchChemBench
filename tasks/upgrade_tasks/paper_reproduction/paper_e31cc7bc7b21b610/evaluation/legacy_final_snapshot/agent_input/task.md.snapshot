# Scientific objective

Study the neutral, closed-shell singlet cis-α-(egan)IrCl and cis-β-(egan)IrCl complexes supplied as Cartesian geometries.

# Author-provided scientific guidance

The author hypothesis to test is that the two cis isomers can interconvert and have different relative stabilities; independently plan and execute calculations that determine whether each supplied structure relaxes to a minimum and which isomer is lower in gas-phase electronic energy. Do not assume the author's software or model chemistry.

# Public inputs and scientific boundaries

`data/inputs/cis_alpha_egan_IrCl.xyz` is the 58-atom cis-α complex and `cis_beta_egan_IrCl.xyz` is the 58-atom cis-β complex. These are source-provided isomer geometries for a fixed-object energy comparison, not a test of discovering the isomers. XYZ element labels and coordinates are the complete molecular identity; each is neutral and singlet. The computational ligand is the hydrogen-substituted egan model represented by these files. The boundary is gas phase and electronic energy; solvent, crystal packing, free energy, kinetics and reaction barriers are outside scope.

# Required scientific validation/investigation

For each named file, choose and report a defensible optimization method, basis/ECP treatment, charge and multiplicity, convergence settings and software. Optimize the supplied geometry, then validate the resulting stationary point with harmonic frequencies or a scientifically justified equivalent. Report the number and sign of imaginary frequencies for each named object. Compute ΔE = E(cis-β) − E(cis-α) from energies evaluated consistently at the two final structures and convert it to kcal/mol. Completion requires both named objects to have a reported endpoint and validation result.

# Deliverables

Submit `report/results.json` conforming to the schema. Include reproducibility metadata, per-isomer energies and validation, ΔE with units, the lower-energy identity, a concise conclusion about the author's qualitative stability hypothesis, and explicit diagnostic evidence. Do not report paper values as if they were your calculations.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.

# Partial or unsuccessful submission

Use `status: "partial"` or `status: "bounded_failure"` when required calculations or analyses remain unavailable. Retain all actual partial results in their original fields. Include `failure` with a nonempty `reason`, a nonempty `missing_observables` array naming the unavailable result fields, and an `evidence` array of existing input, output or diagnostic paths (empty only if no artifact was produced). Explain which calculation failed or was not attempted; do not invent output files.

For these two statuses, the schema permits `null` for the specified unavailable calculated values, selected structures, state assignments or output paths. Keep the known molecular identities, charges, multiplicities, units and attempted methods. Report actual counts, including zero generated/validated candidates when appropriate. An unavailable frequency result is `null`, not zero imaginary modes or an empty list claiming a completed frequency analysis. A genuinely computed zero or an established empty imaginary-mode list remains valid evidence. A missing comparison is not a zero difference or zero RMSE.

Other statuses, and omission of status where the original schema permits it, retain the complete-result format. Passing this format check does not establish scientific completion: uncomputed endpoints receive no completion credit, and existing scientific rules still assess the actual evidence. This reporting branch does not change the scientific target, required successful investigation, or numerical acceptance criteria.
