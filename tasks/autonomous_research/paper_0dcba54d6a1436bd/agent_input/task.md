# Scientific objective

Compute and validate the lowest five singlet vertical excitations of the two public neutral molecules NPCZCS and AQCZCS. Report excitation energy (eV), wavelength (nm), oscillator strength, dominant orbital configuration, and an evidence-based interpretation of whether S1 is ICT-like or locally excited.

# Public inputs and scientific boundaries

Use `data/inputs/systems.json`. Each identity, formula, charge 0, and singlet multiplicity is fixed. The physical system is an isolated monomer; solvent effects may be represented by a stated continuum model. The measured targets are vertical singlet excitation observables, not relaxed emission, aggregate, or solid-state properties. Do not use the paper or SI during the investigation.

# Required scientific validation/investigation

For each molecule, generate a defensible starting structure, optimize the ground state, and validate it as a minimum or explicitly report failure. Compute and identify S1–S5, retaining state labels and orbital/configuration evidence. Perform NTO, transition-density, fragment-charge, or an explicitly justified equivalent analysis for S1. The calculation is complete when both named molecules have a documented geometry/minimum status and either five tracked singlet states with all requested observables and S1 evidence, or a bounded-failure report with concrete diagnostics and any honestly obtained partial states. Do not invent missing numerical values or interpretations. Stop after those conditions are met; do not expand to other compounds. Report software, method, basis, solvent treatment, convergence settings, and any sensitivity checks.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include per-system validation, per-state observables, dominant configurations, analysis evidence, comparison/interpretation, and limitations. A bounded-failure branch is allowed only with concrete diagnostics and partial results.
