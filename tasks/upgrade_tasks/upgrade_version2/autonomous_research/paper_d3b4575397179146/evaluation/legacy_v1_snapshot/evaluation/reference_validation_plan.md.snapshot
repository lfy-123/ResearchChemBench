# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_d3b4575397179146/documents/main.pdf`, PDF pages 3, 4, 5; SHA256 da7d8a332e3db06579fabefe3cebeeebac3f61e58a0cb964b9e91a70eb54a22b
- `papers/paper_d3b4575397179146/documents/supplementary_001.pdf`, PDF pages 19, 47, 48, 49, 50, 51, 52, 53, 54, 55; SHA256 1b9598869e850445e58e1ae41e64fee1f5cd1b6ae49ab9f63bf06143c9e7aee5

Authors used B3LYP/6-311+G(d,p) geometries and TD-PBE0/6-311+G(d,p), IEFPCM MeCN, 18 singlet roots (SI p19) and interpret weak visible bands through substituent-dependent orbitals. Main Fig4 gives 1a, O2/MeCN/0°C and456nm conditions. The new substrate/O2 redox and triplet cycles were not established by the four vertical-state calculations; they test necessary conditions only.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- photoredox_matrix: Four catalysts on a common SET/EnT and redox/state reference.
- oxygen_states: Correct oxygen state energetics and spin identity.
- mechanism_discrimination: Fair possibility of both routes being feasible; no exact oxidation-yield prediction.

Old four-catalyst TDA/def2-SVP spectra and NTO/orbital analysis support state-character diagnostics. They contain no substrate radical-cation cycle, catalyst anion thermodynamics, triplet oxygen transfer or regeneration evidence.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_d3b4575397179146_20260921_161326_0be178/runs/cli_runs/batch_20260921_161327_edb693/autonomous_research-paper_d3b4575397179146-codex-20260921_161327-689cfa/report/results.json`; SHA256 36a6047e8a3d14e2e8099734ba1be350237813b3a30eaba7ef81e62130608e07

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

For dF/dOMe first obtain stable neutral/anion and substrate-cation states, relaxed triplets and a defensible E00. Audit triplet O2/singlet O2/superoxide states using a justified method or calibrated state gap; then close SET, EnT and regeneration reactions for all four with the same reference. Do not equate a closed-shell O2 energy to a calibrated singlet state by label alone.

### Scientific adversarial calibration (not executed here)

Use triplet O2 with singlet multiplicity, equate E00 and vertical S1, shift electrode references between catalysts or infer exclusive mechanism/yield from thermodynamic possibility: reject.

Both SET and oxygen sensitization can remain feasible, with exclusivity unresolved by the completed thermochemical matrix.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Wrong substrate or oxygen state; E00 equated to vertical S1; unmatched potential references; thermodynamic feasibility asserted as exclusive mechanism or exact yield.
