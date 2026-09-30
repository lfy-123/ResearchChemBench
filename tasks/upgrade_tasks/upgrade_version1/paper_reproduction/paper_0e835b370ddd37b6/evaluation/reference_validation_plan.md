# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_0e835b370ddd37b6/documents/main.pdf`, PDF pages 2, 3, 4, 5; SHA256 4481b439479e8874cffa309e47cec459ec33ca4d18be30b921e08b43a3233971
- `papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf`, PDF pages 7, 8; SHA256 df2f9a3f458bd80190146adb77300f8cc65385fc12d2a5bba829e8d60a0e189c

Source PBE0-D3BJ/def2-TZVP, SMD benzene, frequency/IRC validation (main pp3–5; Table2) motivates donor/acceptor and structural explanations. This benchmark adds the 4 control and matched-coordinate decomposition. PyFrag or Multiwfn may assist; NBO licensing is not mandatory and descriptors cannot replace actual activation paths.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- activation_paths: Three actual H2 activation pathways with shared separated-reactant conventions.
- matched_coordinate_decomposition: Matched H–H coordinate strain and interaction terms with closure residuals.
- causal_comparison: Compare signed barriers and decomposition trends; isolated Si descriptors cannot establish causation.

Existing author-informed verification independently reports connected 1/V-prime H2 paths and separated-reference barriers 33.065984/47.132237 kcal/mol. Reuse only those labelled baselines after checking the source protocol; there is no existing 4 control or matched-coordinate decomposition.

Historical structured reports directly inspected in this development pass:

- `docs/verification/group_4/paper_0e835b370ddd37b6/provenance/author_h2_closure_20260925/result.json`; SHA256 e3c9ca20d05c076233349f095c2281fb75567bde03977daa212c55e525b790a3
- `docs/verification/group_4/paper_0e835b370ddd37b6/report/results.json`; SHA256 af55ee193eb2e2a519131316a4089c7f2f426bda4f0df0ad684f5b33c7d5d8c9

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Rebuild the exact neutral divalent-Si 4 graph and its H2 approach; validate its wavefunction, saddle and both endpoints. Reuse checked 1/V-prime baseline jobs where physically identical, then obtain frozen-fragment energies for all three systems at H-H=0.80/1.00/1.20/1.40 angstrom. Calibrate closure residual and functional sensitivity from actual jobs.

### Scientific adversarial calibration (not executed here)

Omit 4, compare unequal H-H progress, use spin/charge-inconsistent fragments or add thermal corrections to frozen fragments: reject.

Mixed deformation/interaction control with no unique electronic cause is acceptable when paths, decomposition closure and sensitivity are complete.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Missing 4; different H–H progress compared as an electronic effect; charged or spin-inconsistent fragments; adding frequency corrections to frozen fragments; absent decomposition closure.
