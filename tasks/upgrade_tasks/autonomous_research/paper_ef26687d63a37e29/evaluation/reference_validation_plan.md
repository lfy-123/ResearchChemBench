# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_ef26687d63a37e29/documents/main.pdf`, PDF pages 9, 10; SHA256 bf0ec692ef2eec7d4342ed722884bcabb2137396dcb3fc6c6a867eed7f62b0b8
- `papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf`, PDF pages 4, 5, 7, 8, 9, 10, 11, 12; SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96

The source attributes dilution tolerance to phosphonium/chain-oxygen interactions and Et3B association; original B3LYP-D3BJ/6-31G(d), ADCH (SI pp4–5) compared only free phosphine/PO/PA local models. The added short-chain graphs, propagation/backbite barriers and concentration competition are benchmark extensions. They must not be attributed to already validated author calculations.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- chain_paths: Actual short-chain propagation/backbite with two Et3B reservoirs.
- chain_end_audit: Explicit chain connectivity, charge separation and coproduct balance.
- concentration_test: A retained concentration control with a transparent uncertainty range.

Old free/PO/PA initiator-adduct ADCH/ESP/contact analysis can check those graph identities and descriptor limitations. It is not a carbonate-growing chain and does not contain propagation or backbiting barriers.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_ef26687d63a37e29_20260921_064813_89a050/runs/cli_runs/batch_20260921_064818_61a71a/autonomous_research-paper_ef26687d63a37e29-codex-20260921_064818-303244/report/results.json`; SHA256 159da8047aa5f901c3bfdb717b3aff9af1bfd5a5c6c31731c26431886209210a

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Validate the PA two-PO/one-CO2 chain with two Et3B molecules and map the terminal alkoxide/carbonate. Compute the full CO2-insertion then PO-opening sequence and a balanced backbite with shortened-chain coproduct. Repeat the matched no-PA model, then apply the same computed barriers to a tenfold activity change; do not fit independent rates.

### Scientific adversarial calibration (not executed here)

Relabel the old PA initiator adduct a growing chain, omit shortened-chain coproduct/two Et3B, or take only the easier propagation segment: reject.

A reduced, absent or confounded PA advantage under the declared short-chain/concentration model is acceptable if properly bounded.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Original initiator adduct presented as growing carbonate chain; missing Et3B or coproduct; wrong P+/O− bookkeeping; independent fitted rate for each dilution; isolated P charge used as polymer selectivity proof.
