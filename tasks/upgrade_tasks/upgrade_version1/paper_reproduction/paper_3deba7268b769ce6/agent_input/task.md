# Scientific objective

Test whether bulk dielectric stabilization, specific methanol hydrogen bonding, or a change in transition identity explains the three-solvent response of phenolate dyes 3 and 4. Separate substituent and solvent effects with a held-out methanol prediction and a stoichiometrically matched micro-solvation control.

# Author-provided scientific guidance

The authors interpret positive/negative solvatochromism in terms of solvent polarity, donor–acceptor charge redistribution and specific interactions. The source calculation uses ωB97X-D4/def2-TZVP with CPCM and vertical excitations. Use this as the baseline hypothesis; the matched one-methanol controls and frozen holdout/state-discrimination test are new. The added comparisons below are benchmark extensions; do not represent them as calculations or controls performed by the authors. Reproduce a defensible source baseline, then test its interpretation.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. Dye3 and dye4 differ by a terminal nitrothiophene versus nitrophenyl group. They are not positional isomers and do not share an elemental formula. Retain the E imine, q=-1 singlet and no counterion. Three solvents cannot locate a continuous inversion point or support a four-parameter Catalan fit. Molecular spectra do not establish bulk ion-pair or device behavior. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Two dyes in three identical solvent treatments.** Minimum-validate both dye graphs in toluene, ethyl acetate and methanol at a shared continuum protocol. Report a state window, energies/f and NTO or equivalent electron-hole descriptors. Follow corresponding character rather than silently comparing root1 to a different state. Check a diffuse basis sensitivity for the anion.

2. **Hydrogen-bond versus remote methanol control.** Use exactly one MeOH in both cluster placements with explicit atom correspondence and state matching. Separate relaxed cluster changes from fixed-geometry electronic differences. Demonstrated collapse/dissociation is an outcome; if using a constrained remote geometry do not assign Boltzmann population or claim it is a minimum.

3. **Frozen prediction and competing explanations.** Preserve a pre-holdout protocol artifact; calculate methanol residuals without per-dye refitting. Contrast continuum-only, specific-interaction and state-switch explanations using the controlled differences. Quantify uncertainty and avoid identifying an exact inversion threshold from three solvents.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: A comprehensive solvent library and kinetic lifetimes are outside scope.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
