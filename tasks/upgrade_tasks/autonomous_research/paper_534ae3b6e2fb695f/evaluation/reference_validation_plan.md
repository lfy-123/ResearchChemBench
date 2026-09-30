# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_534ae3b6e2fb695f/documents/main.pdf`, PDF pages 2, 3; SHA256 285a5ec0e199ceec20676911267bae9407b30b2576f345aa5884611d83955e11
- `tasks/upgrade_tasks/coordination_20260927/batch4/source_review/paper_534ae3b6e2fb695f/publisher_formal_SI.pdf`, PDF pages 10, 11, 12, 13, 14, 20, 21, 22, 32; SHA256 b1244e83d3294b7f9628231d1c173995c3158077fcf8663266632602c2306c89

Formal publisher SI (117 pages), Note8 pp10–12 describes ORCA5.0.4 B3LYP-D3BJ/def2-SVP geometries and def2-TZVP refinement, with some subsequent all-TZVP wording; keep one primary protocol and disclose this ambiguity. SI pp20–22/Note13 interprets electronic descriptors as ODA>6FODA>PFMB nucleophilicity; these are not acylation TS results. New TMC paths and distortion controls test that explanation. MD/diffusion discussion in SI p32 is separate and not scored here.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- first_acylation: Real connected first-acylation paths under identical proton/Cl bookkeeping.
- descriptors_vs_barriers: Identity-matched descriptor versus barrier comparison; contrary ordering is a valid result.
- distortion_interaction: Fixed TMC/diamine fragment comparison at matched N–C distances.

Old ODA/6FODA/PFMB gas-phase HOMOs (-5.0297/-5.667/-5.7768 eV) and fixed TCE reference -9.1212 eV define a descriptor baseline only. TMC was explicitly context-only; no old first-acylation barrier exists.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_534ae3b6e2fb695f_20260921_055245_5ad2d2/runs/cli_runs/batch_20260921_055249_66bff8/autonomous_research-paper_534ae3b6e2fb695f-codex-20260921_055249-4fb4a0/report/results.json`; SHA256 34ef08f9722b11457fc84925fcc6fa5200016c783505e84028ec5ac45b6bc456

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Start with ODA+TMC at the mapped C1002/Cl1003 site and the complete monoamide+HCl endpoint. Validate addition/elimination/proton-transfer segments as required, then apply precisely the same model to 6FODA/PFMB. Compute the effective maximum and matched-progress decomposition rather than selecting the lowest single segment.

### Scientific adversarial calibration (not executed here)

Submit three HOMO-derived indices without a TMC path, omit HCl, or compare addition for one amine with elimination for another: reject.

A barrier ordering that contradicts the isolated nucleophilicity ordering earns credit if all paths and deformation controls are complete.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

TMC left context-only; missing HCl/proton inventory; substituting local descriptor for the fixed global index; comparing different acylation stages; inferring membrane filtration from isolated molecular barriers.
