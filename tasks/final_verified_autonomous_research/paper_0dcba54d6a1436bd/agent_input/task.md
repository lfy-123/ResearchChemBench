# Scientific objective

Compute and validate the lowest five singlet vertical excitations of the two public neutral molecules NPCZCS and AQCZCS. Report excitation energy (eV), wavelength (nm), oscillator strength, dominant orbital configuration, and an evidence-based interpretation of whether S1 is ICT-like or locally excited.

# Public inputs and scientific boundaries

Use `data/inputs/systems.json`. Each identity, formula, charge 0, and singlet multiplicity is fixed. The physical system is an isolated monomer; solvent effects may be represented by a stated continuum model. The measured targets are vertical singlet excitation observables, not relaxed emission, aggregate, or solid-state properties. Do not use the paper or SI during the investigation.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

# Required scientific validation/investigation

For each molecule, generate a defensible starting structure, optimize the ground state, and validate it as a minimum or explicitly report failure. Compute and identify S1–S5, retaining state labels and orbital/configuration evidence. Perform NTO, transition-density, fragment-charge, or an explicitly justified equivalent analysis for S1. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result. Do not invent missing numerical values or interpretations. Report software, method, basis, solvent treatment, convergence settings, and any sensitivity checks.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include per-system validation, per-state observables, dominant configurations, analysis evidence, comparison/interpretation. A bounded-failure branch is allowed only with concrete diagnostics and partial results.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
