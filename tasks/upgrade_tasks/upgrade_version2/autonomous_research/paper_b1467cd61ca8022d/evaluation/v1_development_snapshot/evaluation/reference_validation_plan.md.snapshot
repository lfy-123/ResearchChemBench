# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp2-5,12 Fig2/methods; formal publisher SI pp5-8 FigsS5-S8 and p36 TableS1. Local supplementary_001 is a peer-review file, not the formal scientific SI.

- `papers/paper_b1467cd61ca8022d/documents/main.pdf` SHA-256 `5d8206d63bf9546ab21cd825a8b6401671658eb2b405a2a6f4d2512b9079a058`
- `tasks/upgrade_tasks/coordination_20260927/batch3/evidence/paper_b1467cd61ca8022d_official_si.pdf` SHA-256 `990e77372a82e68e2f69c340c32bad64e4f83a0d2065a48f55751e312ea3b155`

## Scientific definitions and original route

Use PM COCCC, BM COCCCC, TFPM COCCC(F)(F)F and TFBM COCCCC(F)(F)F; all solvent molecules neutral singlets. Li+ is singlet; FSI- is F-S(=O)2-N(-)-S(=O)2-F, singlet. Core clusters contain exactly one Li+, one FSI- and one solvent (total charge0 singlet). Compare O-facing, O/F-contact where F exists, and FSI-dominated orientations at identical composition. No 2 M bulk interpretation follows from this finite-cluster design.

The authors use Gaussian16 B3LYP/6-311+G(d,p), define Eb=Ecomplex-E(Li+)-Esolvent, and use Multiwfn descriptors. Main/SI propose Li-O/F chelation and report MD separately. The eV RESPO axis is not an atomic RESP charge; electronic potential, fitted charges and dipole units must be distinguished. Neutral one-salt cluster competition and frozen/relaxed fragment controls are benchmark extensions.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Confirm all four ether graphs and LiFSI charge; validate one O/F versus anion-contact pair with frequency/fragment energies, then calibrate analysis definitions.

## Minimum complete reference

- cluster_orientations: PM_solvent_contact, PM_anion_contact, BM_solvent_contact, BM_anion_contact, TFPM_solvent_contact, TFPM_anion_contact, TFBM_solvent_contact, TFBM_anion_contact. For nonfluorinated solvents any F contact is to FSI and must be labeled. Fluorinated candidates include attempted bidentate and O-only starts; retain real collapse evidence.
- fragment_controls: PM, BM, TFPM, TFBM. Compute common-fragment interaction/distortion and state explicitly surface/isodensity/gauge for ESP. A gas-phase ion-solvent Eb and neutral salt-cluster interaction are separate quantities.
- descriptor_test: O_F_contrast, anion_competition, method_sensitivity. Test a descriptor prediction against actual coordination and anion intervention, not a restatement of source ordering. Do not infer conductivity/SEI or bulk RDF.

## Available software and resource boundary

Gaussian/ORCA＋CREST；GROMACS仅体相扩展. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

2 M molecular dynamics, RDF/CN, conductivity and battery performance are optional.
