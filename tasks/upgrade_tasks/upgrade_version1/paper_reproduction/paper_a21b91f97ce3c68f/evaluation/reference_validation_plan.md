# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main theory/hyperconjugation discussion and SI computational methods/TableS3, which specifies 6a/e thp, 7a/e 1,3-dioxane and 13a/e 1,3-dithiane-5. RDKit graph/formula checks preserve the three full butyl groups and mapped Sn/C sites. Source nonrelativistic Hamiltonian is explicit despite TZP-ZORA basis label.

- `papers/paper_a21b91f97ce3c68f/documents/main.pdf` — [1, 2, 3]
- `papers/paper_a21b91f97ce3c68f/documents/supplementary_001.pdf` — [2, 3, 4, 5, 6]
- `docs/evalution/update/paper_a21b91f97ce3c68f.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- New constrained J grid and method sensitivity have not been computed; no tolerance is transferred across Hamiltonians.
- The exact coupling basis and orbital metric must be staged and demonstrated by the pilot.

## Callable route and pilot

Gaussian NMR spin-spin couplings and available NBO3.1 or supported ORCA coupling/wavefunction analysis with independently defined metric. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Validate one full pair with signed isotope J decomposition and one orbital-analysis route, then run one constrained torsion before the three-pair grid.

## Minimum complete reference

1. Build the six chair conformers, select reproducible low-energy representatives and calculate each signed Sn–C coupling with component and localized-orbital evidence.
2. Run the matched torsion-at-fixed-distance and distance-at-fixed-torsion grids for one specified Sn–Bu bond in each compound; preserve constrained structures and actual J outputs.
3. Compare ordinary and sulfur responses and repeat the decisive coupling under a documented Hamiltonian/basis sensitivity, separating methodological changes from chemical effects.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
