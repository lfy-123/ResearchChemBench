# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main PDF pp6–7 (Figure 5, exchange argument, Eqs1–2), SI pp5–6 (computational methods), pp35–36 (Table S4, SF-TDA versus full SF-TDDFT and CASSCF benchmark). No common-core reference is supplied by the paper. Old run J values differ substantially from source anchors; that mismatch is retained privately.

- `papers/paper_0cd74ae20ab933f3/documents/main.pdf` — [6, 7]
- `papers/paper_0cd74ae20ab933f3/documents/supplementary_001.pdf` — [5, 6, 35, 36]
- `docs/evalution/update/paper_0cd74ae20ab933f3.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- Actual common-core and relaxed three-series outputs, high-level calibration and uncertainty remain uncomputed.
- No specific PySCF-forge availability or full-matrix budget is assumed.

## Callable route and pilot

ORCA native BS-DFT/CASSCF, available PySCF plus Python population analysis. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Verify one neutral R_H assembly, stable triplet/BS pair, projection convention and same-geometry spin-adapted reference before the common-core series.

## Minimum complete reference

1. Construct the mapped series and evaluate relaxed triplet references plus common-core controls, retaining S2 and spin-density evidence for singlet/BS and triplet states. Report projected exchange, population and core distances.
2. Before expanding the series, calibrate the R_H spin gap at a common geometry using an available high-level/spin-adapted route and document the active orbitals and numerical stability.
3. Compute the substituent differences at both geometrical regimes and the method-sensitive comparison of the closest pair. Decide what the intervention resolves about ligand electronics.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
