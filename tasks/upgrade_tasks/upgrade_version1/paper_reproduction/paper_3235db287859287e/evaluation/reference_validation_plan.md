# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_3235db287859287e/documents/main.pdf`, PDF pages 5, 6, 7; SHA256 2e417419fc4e482fb87a3a8545ab10eba95d2cbff12baa254e30fbbe3cef1925
- `papers/paper_3235db287859287e/documents/supplementary_001.pdf`, PDF pages 94, 95, 96, 97, 98, 99, 100; SHA256 4946aeb29d0288c3c0e7b788fe6bd3c51c121b1463b4353ad3a764d10ca53341

The authors propose thiyl-radical addition, iodine capture, an iodide-assisted H relay and cyclic S–O reorganization, with substrate hydroxyl oxygen entering the sulfoxide. Main pp5–7 and SI p100 support this proposal; SI uses Gaussian09, SMD MeCN, 298 K/1 atm, 6-31G(C,H), 6-311G**(O,S), aug-cc-pVDZ-PP(I). The functional is not specified in the extracted SI paragraph, so do not invent one. This benchmark adds independent competing routes and reservoir-balanced barriers; the original E/Z thermochemistry did not establish kinetic selectivity.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- paths: Two chemically different, connected local oxygen-transfer routes with common reservoir bookkeeping.
- oxygen_tests: Atom-source predictions and computed protection perturbation, bound to actual paths.
- path_comparison: Compare reference-corrected barriers, not merely E/Z product G.

The historical report contains a gas-phase r2SCAN-3c E/Z comparison, DeltaG(E-Z)=0.6609588459769071 kcal/mol. It can test endpoint identity/arithmetic only under its own convention, not oxygen transfer or kinetics. The full original final payload remains a snapshot.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_3235db287859287e_20260921_184040_f24e8a/runs/cli_runs/batch_20260921_184043_26d647/autonomous_research-paper_3235db287859287e-codex-20260921_184043-572267/report/results.json`; SHA256 8ff257330eb0a7d83b583d2922397b21e28d4be8e612ed2aad8ce239ef30faec

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Build one atom-balanced substrate-O radical sequence and one water-O/ionic competitor. First validate the O-transfer endpoint and the I/proton/electron reservoir ledger; then add the protected-OH perturbation and both isotope maps. Record distinct intermediates and the maximum along any multistep route, not merely its last saddle.

### Scientific adversarial calibration (not executed here)

Submit only E/Z DeltaG plus copied isotope prose, with no mapped O-transfer path: reject missing_matrix and dependent mechanistic conclusion.

An independently calculated alternative with balanced reservoirs and both isotope constraints may refute the author route; complete evidence earns the same endpoint credit.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Wrong sulfur reagent; unbalanced electron/proton or labelled O bookkeeping; E/Z stability asserted as oxygen-transfer mechanism; monotonic scan asserted as barrierless free energy.
