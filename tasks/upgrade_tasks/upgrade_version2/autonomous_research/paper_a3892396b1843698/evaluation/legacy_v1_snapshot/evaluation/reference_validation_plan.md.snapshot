# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_a3892396b1843698/documents/main.pdf`, PDF pages 2, 4, 5, 6; SHA256 fae49816db907e5dce86872c757d439fca946b2721e5af626900a04e54c98f57
- `papers/paper_a3892396b1843698/documents/supplementary_001.pdf`, PDF pages 5; SHA256 d70347560db74d188f67b4507f632405908a9b8e8ef217e96519d8f4381ae7ea

The authors discuss cyclopropyl strain and double-boat/double-chair organization (main p4/Fig5) and use omegaB97X-D/def2-SVP geometries/frequencies, def2-TZVPP refinement, GoodVibes and selected dynamics. The benchmark keeps two local channels and an explicit same-graph torsional intervention; it does not require all bridged systems or trajectories. Prior two-TS energetics alone did not establish bidirectional connectivity or the proposed causal control.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- rearrangement_paths: Both original and matched geometric-control paths, allowing evidenced collapse of the control.
- preorganization: Quantify geometric preparation, distinguish constraints from free stationary points.
- channel_response: Intervention response with electronic/Gibbs separation and genuine endpoint evidence.

Old GFN2-xTB/RRHO reports 13.951829/16.472965 kcal/mol and path evidence for the two channels. These support preparation/debugging only and are not DFT calibration, causal preorganization control or dynamics branching evidence.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_a3892396b1843698_20260920_162206_b67206/runs/cli_runs/batch_20260920_162208_122e0e/autonomous_research-paper_a3892396b1843698-codex-20260920_162208-f6eeb7/report/results.json`; SHA256 c1d2d8a504d24ce496598fc48fe58b24d06e7f9f5e2584853b2c5b268940b740

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

DFT-refine both unconstrained rearrangement paths and validate maps 1-2 cleavage, 10-13 or 16-20 formation. Then impose the stated opposite-sign torsion pair, record electronic preparation cost, release constraints and search both channels. If both controls return to the same basin, preserve independent search/profile evidence and omit a fictitious separate free-energy barrier.

### Scientific adversarial calibration (not executed here)

Call a constrained geometry a free minimum, ignore preparation cost, reuse semiempirical barriers as calibrated DFT or claim exact trajectory branching from stationary points: reject.

Evidenced collapse of the geometric intervention is allowed and can refute a distinct-preorganized-basin interpretation.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Wrong bond map; unconnected TS; constrained point called a free minimum; negative electronic difference called negative activation free energy; ignoring preparation cost or double counting conformer weights.
