# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp4-5 optical/quatsome discussion; SI pp15-16 FigsS12-S13, pp45-64 Tables S8-S11.

- `papers/paper_b276b18215cba283/documents/main.pdf` SHA-256 `389f29d6530237e6642f504587587564347b11765747bb427fc6568960d0b1c4`
- `papers/paper_b276b18215cba283/documents/supplementary_001.pdf` SHA-256 `2c5e532a011fe24841808d9dd1c9f5ef653d924992cc1080a13cbc7e7ee09abf`

## Scientific definitions and original route

Use the neutral singlet single-arm C26H27NO3 and complete three-arm C66H69N3O3 graphs. Cisoid/transoid are mapped torsional families on each exocyclic arm, not a change of composition. Primary gas-phase calculations permit direct comparison with the source; a common ethanol continuum is the environment sensitivity, not a model of a membrane. Each full-model result requires arm partitions and matched transition densities.

SI FigsS12-S13 and Tables S8-S11 use CAM-B3LYP/6-31G(d,p), Gaussian16, and compare transoid/cisoid S0 geometries and low singlet states. Authors propose this shift as one contributor to the long-wavelength quatsome absorption. Frozen-arm cross-model and medium controls below are new; linear TDDFT does not establish two-photon brightness or membrane aggregation.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Confirm complete 141-atom three-arm graph and three arm maps, then pilot full TD root window/cost. Without at least one complete three-arm electronic result there is no transfer conclusion.

## Minimum complete reference

- relaxed_models: single_transoid, single_cisoid, three_transoid, three_cisoid. Retain at least four low roots in the three-arm model with NTO and arm-resolved transition-density fractions; do not equate root labels across models.
- arm_geometry_control: single_on_three_transoid, single_on_three_cisoid, three_fixed_arm. Extract mapped arm from full geometry under a declared cap rule; compare frozen and relaxed arm and complete model. Preserve graph/partition/constraint files.
- transfer_and_medium: gas_transfer, ethanol_transfer. Quantify whether transfer survives medium, state mapping and method/conformer uncertainty; actual full-model data are mandatory. No membrane or two-photon mechanism inferred.

## Available software and resource boundary

Gaussian/ORCA TDDFT＋Multiwfn. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Two-photon cross sections, membrane aggregates and absolute lifetimes are optional.

Metric applicability clarification: For single_on_three_transoid and single_on_three_cisoid, interarm_transfer_fraction is null with metric_applicability_reason: the capped single-arm object has no second arm. Excitation, oscillator strength and the mapped frozen-arm calculation remain mandatory. The three_fixed_arm row still requires a numeric interarm transfer fraction from the full three-arm transition density, with explicit fragment partitions and normalization; null is forbidden there.
