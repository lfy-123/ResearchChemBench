# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_db6c4e0558113873/documents/main.pdf`, PDF pages 6, 7, 8; SHA256 9b9d8841f0eb5ec7561cb770ad3bd43d0820639e443412d5da1bc74842318c8c
- `papers/paper_db6c4e0558113873/documents/supplementary_001.pdf`, PDF pages 56, 60, 64, 65; SHA256 a6585fbc4d364923517f436132456b23b012d972eeecb7a818a8a4259c1a6608

The authors propose reduction to CuI, sulfonyl-radical generation, allyl capture by CuII and CuIII reductive elimination; they explain Z preference using Cu-organized allylic geometry. Original B3LYP-D3BJ/LANL2DZ(Cu)/6-31G(d,p) geometries and M06/SDD(Cu)/6-311+G(d,p), SMD MeCN SPs only establish a local intermediate comparison. New exit barriers, radical Cl transfer and spin checks are benchmark additions.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- exit_paths: Cu-organized and free-radical chlorine exits with real endpoint validation.
- reservoir_ledger: Charge/spin/chemical-potential ledger connecting different molecularities.
- stereochemical_control: Competing stereochemical exits, conformation and spin sensitivity.

Historical syn/anti Cu minimum difference 2.2929258933157253 kcal/mol at 298.15 K can be reused as a labelled endpoint/low-mode diagnostic only. It is not a reductive-elimination barrier or direct Cl-transfer comparison.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_db6c4e0558113873_20260918_203828_530445/runs/cli_runs/batch_20260918_203835_fcedec/autonomous_research-paper_db6c4e0558113873-codex-20260918_203835-126440/report/results.json`; SHA256 62e70d67170fccdc510fa38e73f9b08c7bc5d709a0af4b3fadacb721c926b90d

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

First validate the full allyl/acac identity and Cu electron-count ledger. Calculate one connected Cu C-Cl exit and one PhSO2Cl-to-radical transfer with matched reservoirs; add the second Cu stereochemical exit and spin/conformer sensitivity before ranking mechanisms.

### Scientific adversarial calibration (not executed here)

Use naked CuCl, omit the acac ligand, compare Cu-bound and free-radical absolute total energies, or substitute the old intermediate G difference for exit barriers: reject.

Direct radical transfer may be favoured or indistinguishable after association and spin bookkeeping; no Cu-route winner is prescribed.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Omission of acac or Cu-state electron balance; comparing unlike reservoirs; substituting intermediate G for exit barriers; choosing a TS by its energy instead of atom mapping.
