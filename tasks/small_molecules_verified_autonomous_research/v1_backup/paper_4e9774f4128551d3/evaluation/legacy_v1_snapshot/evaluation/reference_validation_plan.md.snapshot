# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_4e9774f4128551d3/documents/main.pdf`, PDF pages 5, 6; SHA256 37a7fad866bff774d010cc6b61af21da2150a78c5bce69c1ff41574648c5b8b4
- `papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf`, PDF pages 20, 21, 71, 73, 76; SHA256 64fda6d0c684c5c53ad4434788b2fe57bfa21ff63ec78215d47885b4103de76a

Main p6 proposes soft enolization then CSA protonolysis, giving a nearly balanced cis/trans mixture and permitting recycling; this is not equilibrium control. Source calculations only compare 50/S20 using B3LYP-D3/6-31G(d,p), larger-basis SP and PCM methanol (SI p71). The new face-specific proton-transfer paths are benchmark extensions, not source-validated TSs. Disclose the main/SI THF:MeOH discrepancy rather than selecting the convenient condition.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- facial_paths: Two faces under racemic CSA with symmetry-supported equivalence allowed through explicit records.
- facial_comparison: Same-reference facial barrier differences and preorganization.
- racemate_control: Racemate and solvent-composition sensitivity, without equating endpoint stability and protonation selectivity.

Old report DeltaG(S20-50)=2.6389157917891617 kcal/mol is a fixed-product thermodynamic control. It supplies neither a protonation saddle nor racemic-acid kinetic weighting.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_4e9774f4128551d3_20260921_195740_34afaf/runs/cli_runs/batch_20260921_195747_460558/autonomous_research-paper_4e9774f4128551d3-codex-20260921_195747-7efad5/report/results.json`; SHA256 f1e514fc239d1dd9670d715e59af6dcdeb2901a805a11d3ae1a676b52613c2da

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Construct and independently optimize the mapped enol-TMS plus one CSA enantiomer and one MeOH. Validate both C6-face proton-transfer paths and common-zero approach costs. Only then add the second CSA enantiomer (or demonstrated symmetry-equivalent mapping), racemate aggregation and solvent control.

### Scientific adversarial calibration (not executed here)

Compare cis/trans product G and call it facial protonation selectivity, or omit CSA counterion/one acid enantiomer without symmetry evidence: reject.

A near-zero racemate-weighted difference supported by all facial paths and solvent/conformer sensitivity is acceptable.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Wrong alpha carbon, source product coordinates passed as independently found TS, omitted acid/counterion, unbalanced silicon/proton inventory, or endpoint G used as kinetic selectivity.
