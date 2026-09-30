# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp6–8/Figure6 and methods; fetched formal Nature Communications SI 41467_2025_67397_MOESM1_ESM.pdf, including surface-segregation discussion (local supplementary_001 is peer review, not scientific SI). Prepared ideal B2/L12 lattice definitions and balanced cycles; no source slab/CIF fabricated. Bulk/segregation/precipitate are different endpoints.

- `papers/paper_eda19e7c8edd4b39/documents/main.pdf` — [7, 8]
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_eda19e7c8edd4b39.publisher_si.pdf` — Relevant methods, experimental observations and identity blocks; see source review.
- `docs/evalution/update/paper_eda19e7c8edd4b39.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- New surface, phase, balanced-cycle and convergence references have not been computed.
- Native model/PAW/basis settings require a demonstrated pilot; source numerical defaults are not inferred from the installed engine.

## Callable route and pilot

Configured Quantum ESPRESSO, GPAW or CP2K plus ASE with explicitly staged elemental datasets; VASP only if legitimately callable with licensed PAW data. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Validate elemental/B2 references and one vacancy, then one mixed(110) slab and a balanced transfer cycle before expanding terminations.

## Minimum complete reference

1. Calculate elemental/B2 reservoirs and both bulk vacancies at two sizes, with magnetic/numerical consistency and the declared Ni-rich reference.
2. Build three specified surface terminations, search top/bridge/hollow adatom placements and calculate atom-balanced exchange/transfer comparisons; preserve site/layer/count evidence.
3. Evaluate the L12 competitor, reservoir consistency and actual slab/k-point/vacuum sensitivity, then test whether bulk preference alone explains surface behavior.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
