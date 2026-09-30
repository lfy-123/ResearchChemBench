# Scientific objective

Determine whether a frozen, small electronic-descriptor model for AZ1–AZ10 adds predictive information about the same Candida albicans MIC endpoint beyond a simple physicochemical baseline, using out-of-fold predictions and label permutation controls.

# Author-provided scientific guidance

The authors calculated isolated AZ9 at B3LYP/6-31G(d) with Gaussian 16 and tabulated frontier-orbital-derived descriptors alongside antimicrobial screening. They did not establish a validated ten-member predictive relationship from the AZ9 scalar alone. The fixed-feature LOOCV, competing baseline and permutation/censoring tests are new benchmark investigations. The added comparisons below are benchmark extensions; do not represent them as calculations or controls performed by the authors. Reproduce a defensible source baseline, then test its interpretation.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. Use all ten neutral singlets and the source assay as an ordinal dilution endpoint. This n=10 study tests an association and its fragility, not biological mechanism, broad QSAR validity or binding affinity. No replicate uncertainty or target protein is supplied. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Complete ten-member identity and descriptor panel.** Compute the same isolated-molecule electronic descriptors for all ten systems using a shared method, validated conformer choice and minimum checks. Retain comparable sampling across members. Verify substituted ring positions and report simple RDKit descriptors independently; do not reinterpret Koopmans descriptors as measured IP/EA.

2. **Frozen models and all held-out predictions.** For each AZ member retain nine training IDs, train-only preprocessing, coefficients and three predictions. Use exactly the frozen features and fixed regularization, no post-hoc feature selection or dropping outliers. Recompute MAE in ordinal bins and compare the electronic model with physicochemical and mean baselines.

3. **Permutation and assay-resolution challenge.** Permute labels and rerun the entire frozen fold procedure; submit all scores and seed. Test dilution/endpoint uncertainty and leave-one-member influence without claiming validation from an in-sample correlation. A null result or baseline dominance is scientifically acceptable.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Molecular targets, docking, cross-strain generalization and drug discovery are outside scope.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
