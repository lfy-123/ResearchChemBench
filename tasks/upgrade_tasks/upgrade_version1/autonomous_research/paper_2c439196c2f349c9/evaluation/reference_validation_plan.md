# Expanded reference validation plan

Status: **blocked**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp3 and 9–11, Figures6/9/10 and SI pp6–7 S7/S8. Main p11 states data available on request; this audit has not contacted authors. The plotted time/power curves are present but an uncertainty-bearing measurement dataset and full beam/thermal calibration are not yet prepared. Status is explicitly blocked. Final development review digitized 27 actual discrete Figure10 markers from the native embedded 1000x845 plot using explicitly recorded pixel centers/calibration and +/-4 pixel reading bounds. Author curves and fitted taus are excluded. The public table contains no fitted model result; the full input gate remains blocked.

- `papers/paper_2c439196c2f349c9/documents/main.pdf` — [3, 9, 10, 11]
- `papers/paper_2c439196c2f349c9/documents/supplementary_001.pdf` — [6, 7]
- `docs/evalution/update/paper_2c439196c2f349c9.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- Figure 10 now has 27 traceable discrete temporal marker rows with pixel-reading bounds. Independent power/intensity and Z-scan measurement rows from the remaining figures, with defensible experimental/digitization errors, remain missing. Fitted curves and fitted time constants are not independent observations.
- The available source text does not establish a complete calibrated SSPM beam-waist, instrument-response and thermal-parameter dataset. Obtain measurement/plot digitization with bounded parameter provenance before completing model discrimination.
- Complete power/Z-scan measured rows and traceable SSPM beam, instrument-response, measurement-noise and thermal bounds remain needed; 27 temporal markers alone do not resolve identifiability.
- No fitted expanded reference, residual distribution or noise-based tolerance has been computed.

## Callable route and pilot

Existing Python/SciPy environment; no quantum-chemical engine is necessary for the minimum task. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

First audit measured rows, units and time resolution; fit a shared thermal response and compute a parameter-profile rank/identifiability check before requiring a contribution fraction.

## Minimum complete reference

1. Assemble and validate a measurement table with provenance and digitization/beam/thermal bounds. Resolve the current input gate before scientific fitting.
2. Fit all three physically defined responses jointly under one calibration; preserve residuals and code, including any model rejection.
3. Profile the mixed fraction and key correlated parameters, test rise-time/history dependence, and predict held-out conditions. Report bounded equivalence if justified.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
