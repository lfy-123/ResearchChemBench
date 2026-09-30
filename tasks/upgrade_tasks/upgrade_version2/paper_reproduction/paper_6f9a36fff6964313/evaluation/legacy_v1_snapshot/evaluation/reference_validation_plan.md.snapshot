# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_6f9a36fff6964313/documents/main.pdf`, PDF pages 1, 3, 4; SHA256 52d820c30c17046603a1f36d40eaa3ee538c8b16a60d329a00ed678a09d61c4c
- `papers/paper_6f9a36fff6964313/documents/supplementary_001.pdf`, PDF pages 7, 8, 12, 16; SHA256 e6f2422063d54b825e1ee8290d0671b06674dc7633081ca057c2388d636bf419

The authors attribute the improved cycloaddition to the trifluoroacetyl group increasing quaternary-ammonium activation of epoxide; KI is essential (main Tables2–3). Charge protocol: B3LYP-D3BJ/6-31G(d,p), PCM MeCN geometries and M06-2X-D3/def2-TZVP/SMD refinement. Those charge calculations did not validate ring-opening TSs. This benchmark selects only the KI opening segment and matched preorganization controls; H2O2 stoichiometry conflicts in the epoxidation discussion do not enter this version.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- ring_opening_paths: Matched real ring-opening competition in one chosen stage.
- preorganization: Separate organization from local activation; fixed geometry is not a free minimum.
- synergy_comparison: Actual catalyst intervention and numerical uncertainty; no forced positive synergy.

Old isolated-ion-pair Mulliken differences (+0.004509 e at quaternary N and -0.018633 e at carbonyl C against their controls) are partition-specific descriptors. They do not validate a multicomponent ring-opening path or synergy.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_6f9a36fff6964313_20260921_201905_ead760/runs/cli_runs/batch_20260921_201909_1abee7/autonomous_research-paper_6f9a36fff6964313-codex-20260921_201909-4633f5/report/results.json`; SHA256 151060af26ab3a1d213da6ceb2fbb7dc75ff4e715f432502de38144b7a7ff739

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Verify both complete ion-pair/KI/epoxide/water/CO2 inventories. Locate one matched terminal-opening path for each catalyst with iodide attack and alkoxide endpoint; then add benzylic alternatives and an explicit restrained catalyst-position control including organization cost.

### Scientific adversarial calibration (not executed here)

Use catalyst charges alone as synergy proof, omit OTf/KI, or compare epoxidation for one catalyst with CO2 cycloaddition for the other: reject.

No retained bifunctional advantage after common-zero and conformer corrections is a fair supported outcome.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Missing OTf/KI; unmatched molecular inventories; second reaction stage made mandatory; declaring synergy from tiny charges alone; treating ~15cm−1 mode by absolute cutoff without displacement/convergence checks.
