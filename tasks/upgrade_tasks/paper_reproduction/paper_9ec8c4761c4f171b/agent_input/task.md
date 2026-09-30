# Scientific objective

Test whether CF3 substitution and aryl extension explain optical shifts within the correctly matched N-phenyl pyrazolones7a/8a/5g, and discriminate fixed-species solvent effects from 7a tautomer/configuration redistribution using TD absorption and independent NMR/IR diagnostics.

# Author-provided scientific guidance

The authors favor the Z hydrazone-keto form using XRD, IR/NMR and B3LYP-D3(BJ)/6-311+G* gas/CPCM chloroform calculations in ORCA, and compute TD spectra with CAM-B3LYP/6-311+G*. They discuss CF3 and conjugation effects partly through orbital gaps. The new task tests this interpretation using correctly paired N–Ph molecules, explicit alternative7a species and media-separated cross-observable evidence. The added comparisons below are benchmark extensions; do not represent them as calculations or controls performed by the authors. Reproduce a defensible source baseline, then test its interpretation.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. Use 7a/8a for CF3→Me and5g/7a for phenyl→biphenyl hydrazone substitution, keeping ring N–Ph. 5f/6a is a different NH series and is excluded. All molecular models are neutral singlets. CHCl3/DMF absorption is distinct from CDCl3/DMSO-d6 NMR; no antimicrobial inference is requested. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Correct pairs at two solvents with matched state definition.** Validate paired identities; compute corresponding TD bright states and spectra in both solvents with a common broadening. Report CF3 and aryl-extension effects separately. Keep KS gap, excitation energy, spectral maximum and absorption edge as distinct observables.

2. **Four7a species under orthogonal spectroscopic constraints.** Attempt all four7a forms with mobile-proton mapping. Validate surviving minima, record collapse, and obtain same-species spectra plus NMR/IR functional-group diagnostics. Use the correct experimental medium and one shielding reference; an absent band must be marked and explained rather than fabricated as an observed peak. Deduplicate collapsed tautomer endpoints.

3. **Fixed-species versus population-weighted explanation.** Decompose7a CHCl3→DMF shift into fixed-species and redistribution contributions using normalized same-molecule free-energy weights. Check whether optical and NMR/IR evidence support one species model jointly. Unsupported redistribution or an indistinguishable support set must remain explicit.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Explicit solvent is optional only when justified by continuum residuals; cellular and antimicrobial extrapolation is outside scope.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
