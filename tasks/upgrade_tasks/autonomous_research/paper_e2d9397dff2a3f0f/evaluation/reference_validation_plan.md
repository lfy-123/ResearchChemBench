# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_e2d9397dff2a3f0f/documents/main.pdf`, PDF pages 8, 9, 10, 11; SHA256 c24bbaae86761a8d40104b001d415708990565d075c29789011a3c8104993875
- `papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf`, PDF pages 25, 26, 47, 48; SHA256 1f4f524a63c1856d741bc9b9016079f9fe8ba2eea9117df6a2df9f72bd626975

Main pp8–10/Figures5–6 proposes that bda stabilizes a conjugated N–O contact, while the sulfonate arm in bcs provides a proton relay. Source B3LYP-D3BJ/SDD(Ru)/6-31G(d,p) Opt/Freq and def2-TZVP/SMD-MeCN SPs (SI p47) distinguish oxidation thermodynamics and N–O chemistry. The old approximately 109.995i mode and 13.8434 kcal/mol are not validated proof of the intended cleavage path. This benchmark requires recalibration and one ligand intervention, not all three full catalytic networks.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- local_paths: For each ligand validate opening, subsequent NH3 attack and the competing direct attack. A lost N–O basin may be documented by a complete collapse profile; never invent a bound bcs minimum.
- ligand_effect: Compare direct attack with the complete opening-plus-attack sequence ending in the same N–N-connected composition on each ligand. Include every segment and preparation cost; an opening barrier alone is not comparable to the full NH3 attack. Compare only within-ligand barrier differences across ligand formulas.
- mode_identity: Actual cleavage displacement versus transverse modes; source oxidation G is not a chemical barrier.

Old PBEh-3c/SMD report gives DeltaE=16.32339 and DeltaG=13.8434269818 kcal/mol and one 109.9948i mode, without IRC. Its reported signed displaced N-O distances 2.49543/2.50502 angstrom make mode projection a required recheck. This is a diagnostic, not a validated reference barrier.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_e2d9397dff2a3f0f_20260918_213702_530445/runs/cli_runs/batch_20260918_213703_c81414/autonomous_research-paper_e2d9397dff2a3f0f-codex-20260918_213703-0c5ce8/report/results.json`; SHA256 d2afe621c899fec0c310eb4ceb12e7ffcf841042a218e69b6c6d05890e44e41f

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Recover the bda N10-O5 cleavage identity with actual displacement projection and forward/reverse endpoints first. Then test the single bcs graph intervention and complete direct versus opening-plus-NH3 attack. Use maximum segment free energies relative to the same initial complex+NH3, explicit proton relay and a common N-N-connected endpoint. A bcs N-O basin that disappears must remain an evidenced collapse, not an invented minimum.

### Scientific adversarial calibration (not executed here)

Count a transverse unstable mode as cleavage, omit a pyridine, use oxidation G as an activation barrier, or compare an opening-only cost with a complete attack route: reject.

A properly documented loss of the closed bcs basin and merged direct/sequential path is acceptable without fabricated separate barriers.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Transverse single imaginary mode accepted as N–O TS; missing pyridine; wrong ligand charge; oxidation free energy used as activation barrier; arbitrary aqueous pH correction in MeCN; opening-only cost compared to a complete N–N-forming route.
