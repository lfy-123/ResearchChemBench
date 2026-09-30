# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_8fefc96b015c4577/documents/main.pdf`, PDF pages 2, 3, 4; SHA256 6fdb5e76c4af7f7b03c05b28d33bdbc9173ca66fcfa476df7c1346cbe422d01b
- `papers/paper_8fefc96b015c4577/documents/supplementary_001.pdf`, PDF pages 34; SHA256 e4b428c6727ab05447160b59531f470d81ecb1d07986771510870c657b6f9a56

Main Scheme3c p4 compares benzyl-aryl versus sulfonyl-aryl closure and attributes tether effects to strain/electronics. SI p34 uses B3LYP-D3/def2-TZVPP, SMD DMSO for short and DCE for long. Source local long-chain gap is only about0.52kcal/mol, so a robust reversal is not guaranteed. The full solvent cross and bidirectional connections are new required controls, while full photoredox/additive networks remain outside scope.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- crossed_paths: Full2×2×2 local competition; eight combinations are not eight engine calls.
- factorial_contrasts: Double differences of within-system channel G barriers, never unlike absolute total energies.
- strain_and_robustness: Actual matched-progress deformation and long-chain sensitivity, with no forced sign.

Old author-informed DMSO short-chain records give B-referenced barriers 13.253000/19.257011 kcal/mol with correct C-C mode displacements but no full IRC claim. Source height -0.05/6.12 belongs to a different zero; historical values cannot fill new long-chain, DCE or endpoint evidence.

Historical structured reports directly inspected in this development pass:

- `docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/INDEPENDENT_RESULTS.json`; SHA256 f2e1e8e9864c9fde8ea69a79168cbee3387680fe94a1998085daa870c5ef4c60
- `docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/autonomous_research/report/results.json`; SHA256 793e54cdbb621d90b9363e1b653af4013ae52cb29bd73e68d21c2eebb4145a8a

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Verify the 56-atom C22H26F2NO4S homologue and radical map10. First validate the decisive long-chain pair with real modes and bidirectional endpoints, then complete both chain/solvent crosses at common zeros. Quantify long-chain low-mode/conformer/method spread and matched-progress strain before interpreting a small difference.

### Scientific adversarial calibration (not executed here)

Copy short-chain TS row numbers to the long graph, compare separated heights as local barriers, omit a cross cell, or force a significant sign reversal despite uncertainty: reject.

Close or indistinguishable long-chain competition is acceptable with the full cross and uncertainty; no author-prescribed winner.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Missing cross-solvent corner or competing path; comparing unlike-composition total energies; wrong atom-order migration; forcing a small source gap sign; ignoring additive confounding or asserting a product ratio from one TS pair.
