# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main p2 Scheme1, pp3-4 computational section, pp8-10 torsion/photostability; CCDC2441197. SI pp32-37 Tables S5-S8 contain composition/label inconsistency.

- `papers/paper_43d74f8a469d9ad3/documents/main.pdf` SHA-256 `3702c207117b172cf5f60f75a5488e55a7c10fc33cccf97eb8ff0c1a3bc721cb`
- `papers/paper_43d74f8a469d9ad3/documents/supplementary_001.pdf` SHA-256 `7b0fafc26a4cfda88dd80c6a1b3d524940e51ec7eb20480383262cb8c4f7d3d5`

## Scientific definitions and original route

Core comparison: Scheme1 compound1 C23H20BNO3 and compound2 C24H22BNO4, neutral singlets. Compound1 is fixed by CCDC2441197; compound2 adds the para-to-phenoxy methoxy group shown in Scheme1, retaining the 3,5-dimethylphenyl boron substituent. Use mapped X-B-Cipso-Cortho on that aryl branch in both. Primary gas phase and an explicitly identical optical solvent sensitivity. Source SI coordinate labels S5/S6 conflict with Scheme1 identities; their unchecked coordinate assignments are not authorized.

The source proposes steric shielding/restricted rotation; its torsion subsection uses PBE0/def2-SVP and a 24-point ground-state scan, while general TD calculations use M06-2X/6-311++G(d,p). These are distinct source protocols. The benchmark adds state-tracked S1 scans and relaxed/restrained comparison; a ground-state scan maximum is not a transition state and does not predict bleaching rates.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Map the actual CCDC boron aryl branch and Scheme1 methoxy substitution; validate continuous S1 state tracking on one short torsion segment before completing a scan.

## Minimum complete reference

- torsion_profiles: dye1_S0, dye1_S1, dye2_S0, dye2_S1. Store a numeric angle-energy-property CSV with mapped atoms at each point, constrained degrees of freedom and forward/backward state overlap; include released anchors.
- restriction_control: dye1_restricted_vs_free, dye2_restricted_vs_free. Use the same mapped angle intervention in both compounds, with actual frozen and relaxed calculations. Root switching is recorded, not smoothed away.
- continuity_and_robustness: state_following, method_or_grid. Demonstrate TD root-window/step-size or method sensitivity and identify discontinuities. Do not extrapolate S0 resistance to an absolute photobleaching rate.

## Available software and resource boundary

Gaussian/ORCA TDDFT＋扫描/态分析. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Nonadiabatic trajectories, conical intersections and absolute lifetime prediction are optional.
