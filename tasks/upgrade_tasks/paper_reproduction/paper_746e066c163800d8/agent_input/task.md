# Scientific objective

Explain static hyper-Rayleigh first-hyperpolarizability differences for compounds 1, 3, 5 and 7 by separating π-extension and common-core twist, while validating tensor units, orientation averaging and response convergence.

# Author-provided scientific guidance

The authors examine lateral π extension of helicene systems and static/dynamic nonlinear response. The source uses B3LYP/6-31G(d) geometries and CAM-B3LYP/6-31+G(d) static response, with functional checks. Its interpretation uses isotropic hyper-Rayleigh response and tensor decomposition. The paired four-member scope and fixed-core-twist tests here are newly bounded interventions. The added comparisons below are benchmark extensions; do not represent them as calculations or controls performed by the authors. Reproduce a defensible source baseline, then test its interpretation.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. Only four specified molecules, neutral singlets in the gas-phase source baseline. Source coordinates were used privately to transcribe connectivity; no optimized answer coordinates are supplied. Static response (ω=0) is not interchangeable with dynamic response at 4556 nm. A single Cartesian beta component is not beta_HRS. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Four full static tensors and isotropic observables.** For each compound validate geometry, compute the complete static tensor, beta_HRS and DR, and retain raw derivative/response output. Verify unit conversion, permutation symmetry, rigid-frame invariance and orientation quadrature/analytical formula. Compare the 1→3 and5→7 pairs at equal frequency and units.

2. **Common mapped helicene twist intervention.** Validate and publish the common-core mapping, then compare relaxed5/7 with the identical signed five-torsion control. Give beta_HRS and a state/CT diagnostic on each geometry, separating extension and geometry effects. Do not claim a constrained geometry is a minimum.

3. **Numerical response and rotation calibration.** Calibrate compound5 static response using field-step or analytic/finite-field comparison and rotation-average convergence. Show how numerical uncertainty affects the paired attribution; a tensor or unit error cannot be hidden in broad tolerance.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: The other 42 members, dynamic response at 4556 nm and material-design extrapolation are optional future extensions.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
