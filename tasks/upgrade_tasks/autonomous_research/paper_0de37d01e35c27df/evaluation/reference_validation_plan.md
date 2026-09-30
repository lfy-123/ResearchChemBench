# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp3-4 Fig2/Table1; SI pp10-11 TablesS3/S4, pp15-18 TablesS7/S8 and orbital/EPR sections.

- `papers/paper_0de37d01e35c27df/documents/main.pdf` SHA-256 `0e7674491acb0b2565ea4dbec1dc37cad1a408c963344f839db245d3b7f85177`
- `papers/paper_0de37d01e35c27df/documents/supplementary_001.pdf` SHA-256 `5db011e6236dc4acc437de3264214f79e39ea967de00ab8459a83934f55623a1`

## Scientific definitions and original route

Use the exact mapped norDTCO C10H14S2 graph already supplied, with S16/S17, and source DTCO (1,5-dithiacyclooctane C6H12S2) as the rigidity control. Each neutral is charge 0 singlet and radical cation charge +1 doublet. Compare each at its own relaxed backbone and vertically on the other oxidation-state geometry in gas phase. A geometric S...S contact is not a covalent edge in the starting neutral graph.

The source proposes sulfur-centered oxidation and 2c-3e interaction; main Fig2 and SI Tables S3/S4/S7/S8 use BP86/TZVP Gaussian16 (unrestricted for radicals). It also discusses distinct dications, which are not the one-electron oxidation target. Cross-geometry and orbital-occupation controls below extend the baseline.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

First fix norDTCO topology/charge and reject spurious S-S bonds inferred by distance alone. Validate one neutral/cation pair and the DTCO ring graph before correlating contraction with bonding.

## Minimum complete reference

- oxidation_pairs: nor_neutral, nor_cation, DTCO_neutral, DTCO_cation. Require valid structures, unrestricted spin diagnostic, natural/SOMO occupations and density/bond analysis. Bond order definition must be consistent across both topologies.
- vertical_geometry: nor_cation_on_neutral, nor_neutral_on_cation, DTCO_cation_on_neutral, DTCO_neutral_on_cation. Pair fixed backbone and relaxed state evidence to separate mechanical contraction from electronic bonding. Retain same atom map.
- bonding_interpretation: rigidity_contrast, analysis_sensitivity. Compare contraction against orbital occupation/spin localization and independent density evidence. A short distance without electronic support weakens the hypothesis; ring opening must have a new topology ID.

## Available software and resource boundary

Gaussian/ORCA＋Multiwfn. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Dication chemistry, full aryl series and electrochemical reversibility are optional.

## Phase 1 completion update 2026-09-28T06:44:43.181429+00:00

The development plan above is historical. The complete finite reference matrix and numerical sensitivity are now executed and audited; see verified_computation_reference.md, scientific_reference/, and task_provenance/phase1_verification.json. Independent blind-agent success and universal cross-method tolerances are not asserted.
