# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_c625cba3ce868eb1/documents/main.pdf`, PDF pages 3, 5, 6, 7; SHA256 44b374957665d941b519f781fe9341f1632c84a6c7b975c4cd231874281e0ef8
- `papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf`, PDF pages 30, 31, 32; SHA256 19d3e128aae61e6d8f4904d7f5f3cc8cd31230ccb210eb81ba15402de096e4db

Authors propose hydroperoxide-induced alkene polarization and a bromiranium intermediate; nonenzymatic NBS gives the same profile as CiVCPO (main p3). Main p7 explicitly reports NBS/Et3N in dry DCM, whereas original descriptors used aqueous B3LYP/CBSB7 C-PCM. The new local model uses the identified NBS control and tests six/seven closures. It does not identify the microscopic enzyme brominating species or import a nonexistent five-membered source channel.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- closure_paths: Correct graph-derived ring sizes and chemically identified NBS control.
- active_reagent_ledger: No naked bromide substituted for an electrophilic brominating reagent.
- regioselectivity_test: Regioselectivity from connected paths, with source/model boundaries explicit.

Historical aqueous reactant Loewdin charges/dipoles explicitly did not model reagent, intermediate or TS. They can motivate candidate polarization but do not certify regioselectivity, and are not directly transferable to the DCM NBS control.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_c625cba3ce868eb1_20260921_050613_b19fdc/runs/cli_runs/batch_20260921_050617_82c9a1/autonomous_research-paper_c625cba3ce868eb1-codex-20260921_050618-a30796/report/results.json`; SHA256 5c625d99b85e2bf2bce1775598e784601f3e241a49b97630e81f1c7afaa5af06

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Validate NBS bromination and proton-transfer bookkeeping on (R)-4, then locate one six-membered and one seven-membered closure from comparable brominated precursors. Include precursor face/conformation costs and succinimide/Et3N proton balance. Keep the local one-equivalent relay model separate from experimental catalytic loading.

### Scientific adversarial calibration (not executed here)

Force a five-membered channel, label row22 oxygen, use Br- as the electrophile, or accept a failed TS search as excluded regioisomer: reject.

A conformation-driven explanation or unresolved six/seven competition is acceptable after both connected paths and matched controls.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Wrong ring sizes; row22 treated as hydroperoxide O; Br− used as electrophilic source; failed TS called exclusion; charge asymmetry claimed to establish regioselectivity or enzyme mechanism.
