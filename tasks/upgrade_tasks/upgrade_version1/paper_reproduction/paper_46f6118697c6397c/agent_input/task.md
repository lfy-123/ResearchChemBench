# Scientific objective

Determine whether boron substituents tune the corresponding B2N6-dominated bright excitation primarily through electronic or structural effects, by comparing complete compounds1–4 at relaxed geometries and a common mapped core geometry.

# Author-provided scientific guidance

The source studies substituent effects on boron-bridged hexazenes using absorption and TDDFT. Gaussian16 B3LYP/6-31+G(d) with SMD dichloromethane is reported; the SI includes D3(BJ) while the main computational summary is less explicit. Treat that as a method-label ambiguity to document, not an adjustable tuning parameter. The shared-core geometry intervention and systematic NTO correspondence are new controls. The added comparisons below are benchmark extensions; do not represent them as calculations or controls performed by the authors. Reproduce a defensible source baseline, then test its interpretation.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. All four molecules are neutral singlets with the full benzyl-substituted B2N6 graph. Compound2 contains four covalent B-O-SO2CF3 groups; these are not removable counterions. Molecular excitation comparisons do not establish emission lifetime or decomposition mechanism. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Four complete molecules and corresponding bright states.** Verify full composition and B/N connectivity, optimize and minimum-validate each complete molecule, then match corresponding bright states by character. Report alternative nearby states so the selected transition cannot be cherry-picked to an experimental peak.

2. **Matched geometry electronic intervention.** Use solver-generated compound2 core as the common constrained geometry for the four substituents; quantify RMSD and state character. Optimize only permitted peripheral coordinates and label the points constrained. Compare substituent effects at fixed core separately from relaxed geometry changes.

3. **Electronic and structural attribution with source ambiguity.** Recompute each contrast relative to2 and the relaxed-minus-fixed difference. State how root correspondence, D3 method ambiguity and basis/functional sensitivity affect attribution. Original compound2 root-energy mismatch is an audit item, not justification for selecting a different physical state.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Dissociation networks and emission lifetimes are future extensions; four covalent triflates must remain part of compound 2.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
