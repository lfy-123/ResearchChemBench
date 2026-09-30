# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main electronic/optical discussion and SI computational methods plus Cartesian blocks from p42 onward for four named models. Extracted graph-only identities; 1M versus 2M differs by C2H2. Closed-shell coordinate block provenance is private and does not assign a winner.

- `papers/paper_c23cfabbd34b087f/documents/main.pdf` — [4, 5]
- `papers/paper_c23cfabbd34b087f/documents/supplementary_001.pdf` — [42, 43, 50, 56]
- `docs/evalution/update/paper_c23cfabbd34b087f.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- New state minima, common-scaffold interventions and diagnostic-calibrated optical references remain uncomputed.

## Callable route and pilot

Gaussian/ORCA DFT/TDDFT, natural orbitals and available CASSCF/spin-adapted calibration; RDKit graph mapping. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Validate full 1M_OMe and one 2M spin-state set and common-scaffold map; inspect whether independent calibration is needed before full state matrix.

## Minimum complete reference

1. Build all four structures and evaluate stable CS, BS and triplet alternatives with conformer/collapse evidence; calculate matched low optical states in a consistent medium.
2. Generate common-scaffold interventions for both substitution pairs using the public mapped graph correspondence and evaluate electronic-state differences without borrowing equilibrium thermal corrections.
3. Select one ambiguous representative by a recorded rule, perform independent spin calibration, and quantify topology/substituent/relaxation effects with a method sensitivity.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
