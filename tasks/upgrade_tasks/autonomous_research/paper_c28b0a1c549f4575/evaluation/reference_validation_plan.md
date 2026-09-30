# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp1-3 electrolyte identity and association; SI pp5-6 computational details.

- `papers/paper_c28b0a1c549f4575/documents/main.pdf` SHA-256 `4e3ad96c28503f3a100df2083569811eef0ee848ae6aca2def236523628f8909`
- `papers/paper_c28b0a1c549f4575/documents/supplementary_001.pdf` SHA-256 `51551c36ef22b1633c2ee346411edf4c5b5f3ec9edd9ea1ce7e923c011387546`

## Scientific definitions and original route

DED is 1,4-diethyl-1,4-diazabicyclo[2.2.2]octane dication, not a neutral diamine. Define A=TEA+BF4- and B=DED2+(BF4-)2 (both charge0 singlet). For each use one and two PC molecules in contact and separated configurations. PC is racemic; choose a fixed stereochemical composition and report it. Compare PC transfer A.PC+B -> A+B.PC and the corresponding second-PC exchange; compare contact/separated at equal solvent count. Source 1 M TEABF4 +0.2 M DED salt is experimental context, not a finite-cluster concentration.

The source suggests DED2+ competes for PC and facilitates TEA desolvation. Gaussian16 B3LYP-D3BJ/def2-SVP optimization/frequency and B3LYP/6-311+G(2d,p) binding single points are reported; frontier orbital protocol differs. Explicit neutral ion-pair and solvent-count exchange controls below are benchmark extensions; they cannot establish capacitance or cycling life.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Verify DED ethylated quaternary-N graph and two BF4 anions. Pilot contact/separated A.PC and one balanced PC exchange with DFT refinement.

## Minimum complete reference

- equal_composition_clusters: TEA_PC1_contact, TEA_PC1_separated, TEA_PC2_contact, TEA_PC2_separated, DED_PC1_contact, DED_PC1_separated, DED_PC2_contact, DED_PC2_separated. Keep correct anion count and PC count; separated structures may collapse, but only actual mapped optimization evidence establishes that fact.
- PC_exchange: first_PC, second_PC. Balance both salt compositions and every PC molecule. Record component energies and coefficients so the exchange is recomputable; no direct ranking of charged DED-PC versus TEA-PC totals.
- ion_pair_control: TEA_contact_effect, DED_contact_effect, conformer_sensitivity. Separate ion pairing, PC coordination count and conformer uncertainty; conclusions only concern finite molecular necessary conditions.

## Available software and resource boundary

Gaussian/ORCA＋CREST/xTB. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Capacity, cycling lifetime and bulk GROMACS are optional.
