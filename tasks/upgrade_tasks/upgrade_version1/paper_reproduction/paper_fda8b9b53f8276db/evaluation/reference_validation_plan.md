# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main p4 computational structure discussion; SI Table S2 and FigsS11-S13; immutable CCDC2433822 and current final experimental_bonds.json define the six-bond scope.

- `papers/paper_fda8b9b53f8276db/documents/main.pdf` SHA-256 `0afa69242ab928c082802d029d66eaa4c3c58cea7f791438d64de1c7f88de8d1`
- `papers/paper_fda8b9b53f8276db/documents/supplementary_001.pdf` SHA-256 `13ace6b2daec90e737a69c21f21a4af2d7cab7a54b967859e270ca1147c496de`

## Scientific definitions and original route

Use neutral singlet 6,7-dimethyl-2-(pyridin-2-yl)quinoxaline, C15H13N3, from CCDC2433822. Cis/trans is the mapped N1-C1-C2-N2 torsion; preserve deposited labels. Primary gas phase and acetonitrile continuum at 298.15 K, consistent 1 M molecular convention for solution. Six bonds are exactly those in experimental_bonds.json; seven SI or 33 CIF bond sets must not enter this RMSE.

The authors compare a gas-phase cis local minimum with crystal intramolecular bonds using Gaussian03 B3LYP/6-311+G(2d,p). The crystal pyridyl orientation differs; a local minimum need not be globally lowest. The paired cis/trans solvent and torsion controls are benchmark extensions.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Recover the current cis six-bond baseline and N1-C1-C2-N2 mapping, not a historical trans/seven-bond result; then validate both environments and one restrained torsion.

## Minimum complete reference

- conformer_environment: cis_gas, trans_gas, cis_MeCN, trans_MeCN. Validate graph/minima, searches and environment-specific conformer identity; a released candidate may merge into another basin with actual evidence.
- six_bond_residuals: cis_gas, trans_gas, cis_MeCN, trans_MeCN. Recompute six unrounded residuals and RMSE against the authorized experimental distances. Separate any larger bond statistics; include OLS with intercept only if called R squared.
- torsional_intervention: gas_fixed_vs_relaxed, MeCN_fixed_vs_relaxed. A defined mapped torsion restraint and relaxed counterpart distinguish geometric from solvent effects. Nonstationary restrained points receive no borrowed harmonic G.

## Available software and resource boundary

Gaussian/ORCA＋CREST；有限CIF簇仅可选. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

CIF neighbor clusters, solid-state explanation and NMR are optional.

## Phase1 actual reference update 2026-09-28T08:21:41.016228+00:00

Development-only zero-calculation statements above are historical. The finite10rowmatrix now has native references and all required comparisons; see verified_computation_reference.md and scientific_reference/. ExperimentalESDs are preserved separately fromrounding. No blindtrial, globalconformerpopulation or universalnumericthreshold is asserted.
