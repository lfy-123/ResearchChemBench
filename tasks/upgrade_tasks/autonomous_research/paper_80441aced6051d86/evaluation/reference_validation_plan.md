# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp2–4 and publisher SI Sections B (NMR stoichiometry), C (photophysics) and D (computational structures/TableS2). Extracted host-only graphs from 190-/272-atom complexes; verified CB7 C42H42N28O14 and CB8 C48H48N32O16. No new bound coordinates or TD outputs were published.

- `papers/paper_80441aced6051d86/documents/main.pdf` — [3, 4, 5]
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_80441aced6051d86.publisher_si.docx` — Relevant methods, experimental observations and identity blocks; see source review.
- `docs/evalution/update/paper_80441aced6051d86.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- No new host/partner-deletion reference or placement/spectral uncertainty is computed.
- TD state windows and dark-state identification need calibration for both bound stoichiometries.

## Callable route and pilot

Gaussian or ORCA TDDFT, xTB/CREST for placement prescreening if compatible with host charge, Multiwfn transition-density analysis. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Verify one neutral CB host graph and G1 charge; relax a CB7:G1 placement and test the matched full/deleted host TD calculation before CB8.

## Minimum complete reference

1. Build and validate both complete host–guest systems from independent placements; calculate state-resolved optical properties before and after frozen host deletion.
2. Perform the four frozen partner-deletion controls and relaxed isolated monomer/dimer baselines. Preserve mappings, placements, raw TD vectors and transition densities.
3. Compare host response, guest–guest coupling and geometric confinement with a common state definition, and quantify one basis/solvent/placement sensitivity.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
