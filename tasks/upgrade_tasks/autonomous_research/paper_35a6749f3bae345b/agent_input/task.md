# Scientific objective

Determine whether terminal substitution changes DBC photophysics through ground-state twisting, excited-state relaxation or state localization, using DBC-Ph/DBC-Nap and a frozen DBC-Cbz prediction with a common-geometry control.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. All neutral singlets in toluene. Retain full DBC, para-phenylene and terminal groups. Track singlet state character through optimization; a root-index change is not automatically the same S1. Ordinary S0→Sn TD transitions at an S1 geometry are not excited-state absorption. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Three identity- and state-tracked four-point cycles.** Optimize and validate S0 and trackedS1, retaining root/state history and NTO evidence. Recompute four-point absorption, emission and reorganization terms. Define the solvation convention at each point; a darkS1/brightS2 distinction must remain explicit.

2. **Matched Ph/Nap geometries isolate relaxation effects.** Compare matched45° and relaxed Ph/Nap in S0 and trackedS1. Use consistent localization metrics and atom mappings, distinguishing geometric and state-switch effects. Do not infer ESA from ordinary ground-reference roots at R1.

3. **Frozen extension to an additional author member.** Freeze the explanatory rule from Ph/Nap beforeCbz interpretation. Submit predicted and computedCbz properties plus a consistent experimental-band comparison and error bound. A failure of transfer is an acceptable scientific outcome after completing the panel.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Film quantum yields and complete nonradiative dynamics are outside scope.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
