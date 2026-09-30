# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp3-5 optical tables/Figs and pp7-8 section3.1.4; formal publisher DOCX FigsS31-S39/TableS1 (downloaded and read in batch evidence), member12d synthesis/identity main pp6-7.

- `papers/paper_98b6f8a0352f72c2/documents/main.pdf` SHA-256 `714a568d5e123ebb80f11a9ab57fd85c282648d3f861353b63973f8d8cdf3492`
- `tasks/upgrade_tasks/coordination_20260927/batch3/evidence/paper_98b6f8a0352f72c2_official_si.docx` SHA-256 `275ca4700127d3f0cce5b5b9ae3a9d21f157acc0409cb8aa658fb06e4f65a924`

## Scientific definitions and original route

Select real members12a (NMe2, C24H19N3) and12d (NEt2, C26H23N3), neutral singlets, in CHCl3 and EtOAc. Each requires S0 preparation, vertical TD at S0, tracked relaxed S1 and vertical emission at S1; report the adiabatic energy separately. Use the mapped phenyl-phenazine single-bond torsion as common intervention. Calculate experimental kr=Phi/tau only if both measured values refer to the same conditions; 1/tau alone is total decay, not radiative rate.

The authors use ORCA4.2 omegaB97X-D3/def2-TZVP/def2-J, CPCM CHCl3 and40 singlet roots, with NTOs and oscillator-strength-derived lifetimes. Formal SI FiguresS31-S39 and TableS1 include EtOAc and CHCl3 calculations. Theoretical radiative lifetime is not a measured fluorescence lifetime; source main/old reference lifetime discrepancy must be disclosed. Relaxed S1, paired torsion and two-solvent tests are new.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Verify 12a/12d graphs and two media, then pilot one tracked S1 in both solvents with cross-program/state mapping. No series regression before states are matched.

## Minimum complete reference

- solvent_series: 12a_CHCl3, 12a_EtOAc, 12d_CHCl3, 12d_EtOAc. Save S0/S1 outputs, geometry and NTO evidence with solvent response convention; never equate absorption oscillator strength with measured radiative yield.
- common_torsion: 12a_CHCl3, 12a_EtOAc, 12d_CHCl3, 12d_EtOAc. Freeze identical mapped phenyl-phenazine angle, compare released structures and track state; distinguish ground/excited geometry relaxation.
- rates_and_robustness: radiative_convention, substitution_vs_solvent, state_sensitivity. State refractive-index/local-field/degeneracy convention and formula, and whether an experimental Phi/tau comparison is available. Do not invent missing quantum yields or treat SI theoretical lifetimes as measurements.

## Available software and resource boundary

Gaussian/ORCA TDDFT＋Multiwfn. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Thin-film nonradiative lifetimes and full device efficiency are optional.
