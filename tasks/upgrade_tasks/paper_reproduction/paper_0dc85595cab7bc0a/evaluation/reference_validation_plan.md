# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_0dc85595cab7bc0a/documents/main.pdf`, PDF pages 2, 3; SHA256 f23bf2094145eada8d43b6e1bf7cce14fdd9db27d9f82fae7948b0fd86183451
- `papers/paper_0dc85595cab7bc0a/documents/supplementary_001.pdf`, PDF pages 9, 10, 11; SHA256 84d40a48033a1d1cfc425d3b981e79b39eaf00fa29ffdffbde03807e528bc652

Source main p2/Fig2 and SI pp9–11 compare omegaB97X-D/def2-TZVP intermediate G and LUMO site density/phase for sequential Mallory oxidation/cyclization. The authors infer selectivity; those ground-state comparisons do not establish excited-surface access. New representative path/state diagnostics deliberately constrain the strength of the conclusion. Full SHARC dynamics and exact branching ratios remain optional.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- candidate_layers: Two-stage chemically distinct candidate coverage and auditable same-formula energy comparisons.
- accessibility_diagnostics: Real representative closure profiles and physical-state tracking; S0 diagnostics cannot establish a unique photoproduct.
- supported_set: Conclusion remains an evidence-supported candidate set unless a separate calibrated photochemical extension is supplied.

Old candidate enumeration and xTB endpoint graph checks are search diagnostics only. Old 4.30 angstrom and +/-15 kJ/mol filters were not calibrated; a nearby excluded candidate must be reconsidered. No excited-surface reachability is established by that report.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_0dc85595cab7bc0a_20260920_164554_4baadc/runs/cli_runs/batch_20260920_164558_4a5af1/autonomous_research-paper_0dc85595cab7bc0a-codex-20260920_164558-491621/report/results.json`; SHA256 b58a1cbec6e43d8c7ee3c0e261d06cb932bb2c0c1733b08f95a2f89992b7efdf

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Verify the displaced precursor preserves the intended graph without terminal-answer labels. Include both graph-distinct ortho closures and conformers near the former distance cutoff; DFT-refine advanced candidates at both stages. For one critical closure per stage, obtain mapped S0 path plus physical excited-state tracking, and explicitly limit conclusions when the excited surface cannot be calibrated.

### Scientific adversarial calibration (not executed here)

Compare total energies across different hydrogen counts, prune solely by the old cutoff, use xTB-only ranking as DFT refinement, or call the lowest S0 endpoint the unique photoproduct: reject.

A supported set of multiple photoproduct candidates with complete declared S0/state diagnostics is valid; full dynamics and unique branching are not required.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Comparing raw total energies across H counts; source terminal structures or product names leaked as independent discoveries; lowest S0 product asserted as uniquely photoaccessible; static LUMO picture substituted for state/path evidence.
