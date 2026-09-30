# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_fcc3c7f2c46a0fbe/documents/main.pdf`, PDF pages 3, 4, 8, 9; SHA256 dbc96d35a3beaafb5d41415bf651ceab2898a633c1041488383fdbc449178e16
- `papers/paper_fcc3c7f2c46a0fbe/documents/supplementary_001.pdf`, PDF pages 30, 31, 32, 34; SHA256 f5438a3984038ec249597117f09d3d008f96683c95ac8fc4a239c4ae8932f92c

The authors used B3LYP/6-311+G(d,p) geometries/descriptors and linked acidic 4c/4i to HAT; discussion of methoxy derivatives invoked SPLET and phenoxide (main pp8–9). That phenoxide explanation must be tested against actual connectivity, not adopted. The new cycles and HAT controls were not computed in the source. The assay medium is ethanol (main p4), not the NMR solvent DMSO or a presumed methanol assay.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- thermochemical_cycles: Real donor sites and charge-balanced cycle closure, not descriptor correlation.
- decisive_local_paths: Matched explicit-acceptor HAT paths spanning acidic and nonacidic structures.
- activity_boundary: Mechanistic discrimination with correct experimental endpoint limits.

Old 4b isolated-geometry/XRD comparison documents a source SMILES/name conflict and conformer limitations. The name/selector graph can guide identity correction; that geometry result does not validate antioxidant thermochemistry or measured activity.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_fcc3c7f2c46a0fbe_20260920_122408_dea90c/runs/cli_runs/batch_20260920_122411_4d27a7/autonomous_research-paper_fcc3c7f2c46a0fbe-codex-20260920_122411-d4f5c6/report/results.json`; SHA256 a5f9afeed3c4c66edb547e61f2b03e2fd6d5e589dfa549681f74dfb190a07520

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Verify E configuration and the real donor sites, then close one 4c and one 4h cycle with a single proton/electron convention. Test explicit DPPH H-transfer paths for those two before extending thermochemical cycles to 4b/4i. Validate cycle closure, solvent response and donor-site alternatives.

### Scientific adversarial calibration (not executed here)

Create a phenoxide from an OMe group, use DMSO as the assay solvent, label insoluble 4e inactive, or predict exact IC50 from a HOMO-LUMO gap: reject.

A source HAT/SPLET assignment may be refuted by site-correct cycles; multiple feasible mechanisms with complete evidence are allowed.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Invented phenolic OH/phenoxide; using NMR solvent as assay medium; IC50 predicted from a local orbital gap; proton/electron references mixed between cycles; insoluble 4e assigned zero activity.
