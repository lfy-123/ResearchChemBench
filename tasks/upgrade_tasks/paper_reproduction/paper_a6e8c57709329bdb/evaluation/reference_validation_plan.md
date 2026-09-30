# Expanded reference validation plan

Status: **blocked**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp2,5-7 Fig4 and theoretical calculation section; SI FigsS5-S8/S20. DMF is explicit; salt counterion, water activity and pH for Fe/Co sensing are not established by the accessed records.

- `papers/paper_a6e8c57709329bdb/documents/main.pdf` SHA-256 `5a566dd113353d03624849466569e890d4212bc2e0a7298ec2bcb77e7cbef2a1`
- `papers/paper_a6e8c57709329bdb/documents/supplementary_001.pdf` SHA-256 `dcb7c395f4cad30dbeae17d62a11bdf820207bf7d8b83b8866def961e7322f60`

## Scientific definitions and original route

HL is the full C20H22N4O6 neutral singlet graph with two E imines and phenolic OH groups. Source sensing medium is DMF; Co(II) is selected because it is an explicitly measured partial-quenching competitor. Fe(III) spin space includes doublet/quartet/sextet; Co(II) doublet/quartet. Water/DMF ligands, protonation and counterions must be fixed with salt/pH data before a unique binding-energy cycle is defined. Do not compare unlike total compositions or assign selectivity from smallest gap.

The authors use Gaussian09 B3LYP/6-31G(d,p) for free HL and propose Fe(III)-associated LMCT quenching; Fig4 also shows weaker response to Co/Mn/Pb. Mn-L is a separate heteroleptic binuclear complex involving HL-prime and is not a clean Fe-HL control. Expanded Fe/Co coordination/protonation and solution exchanges are new and not validated by free-ligand gap agreement.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Obtain the salt/counterion and acid/water boundary, define finite coordination/protonation with mass balance, then pilot a Fe/Co ligand-exchange pair and open-shell response.

## Minimum complete reference

- coordination_candidates: HL, Fe_HL_protonated, Fe_HL_deprotonated, Co_HL_protonated, Co_HL_deprotonated. All models require atom-complete solvent/counterion/proton bookkeeping and applicable spin search; apparent nonconvergence is not proof a species is absent.
- solution_cycles: Fe_exchange, Co_exchange, proton_exchange. Use one balanced exchange reference and explicit proton reservoir; bare Fe3+ binding in vacuum cannot be substituted for an unreported DMF experimental salt.
- selectivity_tests: binding_contrast, state_contrast, speciation_sensitivity. Keep binding preference separate from potential quenching channels, accept multiple Fe species consistent with evidence. TD/NTO alone does not produce a rate or detection limit.

## Available software and resource boundary

Gaussian/ORCA＋CREST＋Multiwfn. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Verified blocker

blocked_solution_definition: DMF and competing Co(II) are confirmed, but the accessed main/SI do not fix sensing salt counterions, pH/proton reservoir or water content. Define those from source records or an explicitly authorized model before atom-complete Fe/Co exchange references. No invented salt/pH or calibrated selectivity is supplied.

## Optional boundary

Full quenching dynamics, detection limits and biological medium are optional.
