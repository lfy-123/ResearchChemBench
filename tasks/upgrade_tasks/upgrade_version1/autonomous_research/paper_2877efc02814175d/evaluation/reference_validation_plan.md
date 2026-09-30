# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Recovered user-supplied main PDF (10 pages; source_data/user_supplied_20260925/1-s2.0-S0022286025023567-main.pdf), p2 computational section and pp7-8 Figs8-10; SI pp11-13 TablesS1-S3 and p18 TableS8 directly checked. The default papers/main.pdf has no readable body and is not the evidence source. Experimental sensing is DMSO/water9:1, distinct from the bounded DMSO electronic calculation.

- `papers/paper_2877efc02814175d/documents/supplementary_001.pdf` SHA-256 `9244bf34a4da6ee7f3829c7eb75798289030a65fc3cf8107e6f8026a90edf45f`
- `docs/verification/group_2/paper_2877efc02814175d/source_data/user_supplied_20260925/1-s2.0-S0022286025023567-main.pdf` SHA-256 `3ed031e94536c075f14d4aaec6fced89d457235c3202c1bc2eb8c7a236ee2d39`

## Scientific definitions and original route

Full neutral DQCS is C31H27N3O3 singlet; retain the phenolic hydrogen present in the three source graphs. Metal complexes all have charge+2; Cd/Co/Ni source multiplicities are1/2/1. Primary medium DMSO. A free ligand extracted from a complex has charge0 singlet, not the parent complex charge. Identify ligand versus metal density partitions and fixed-geometry atom correspondence.

The authors use Gaussian09 B3LYP/6-311G(d,p) for DQCS and B3LYP/LanL2DZ for complexes in DMSO. SI S2 explicitly makes Co a doublet, although S8 labels its table as singlet transitions; that table heading must not force closed-shell Co TD. Gap, hardness and electrophilicity are algebraically related, not three independent mechanisms. Frozen-ligand controls are new.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Remove the metal from a verified 65-atom complex and check full neutral 64-atom ligand electron count; validate Co unrestricted response and spin before comparing NTO partitions.

## Minimum complete reference

- relaxed_species: DQCS, Cd_DQCS, Co_DQCS, Ni_DQCS. Compute like-defined TD/NTO observables with six roots or a justified larger window. Co transitions retain doublet reference/spin character rather than forced singlet labels.
- frozen_ligand: ligand_from_Cd, ligand_from_Co, ligand_from_Ni. Extract identical complete ligand graph/charge from each source complex, retaining all hydrogens; pair frozen and relaxed ligand results.
- attribution: Cd_effect, Co_effect, Ni_effect, method_sensitivity. Separate geometry and metal contributions with state matching and real density fractions. Do not use gap/hardness/electrophilicity algebra as independent causal evidence.

## Available software and resource boundary

Gaussian/ORCA＋Multiwfn＋构象工具. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

DNA association, quenching rates and antibacterial mechanism are optional.
