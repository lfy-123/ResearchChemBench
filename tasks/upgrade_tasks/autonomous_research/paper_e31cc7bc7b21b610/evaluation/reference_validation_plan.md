# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main synthesis formula C44H52N2O6 and full dimer C88H104Ir2N4O12, computational section p3 and bonding pp7–9; SI pp27–30 contains Hap4Ir2 (54-atom) structures, not full/truncated Egan dimer references. Prepared named full graph and exactly four tBu-to-H deletions per ligand, checked formulas. This supplies an implementable new pair while preserving the missing-pilot limitation.

- `papers/paper_e31cc7bc7b21b610/documents/main.pdf` — [8, 9, 10]
- `papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf` — [20, 22]
- `docs/evalution/update/paper_e31cc7bc7b21b610.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- No full/truncated Egan dimer minimum, fragment decomposition or multi-reference calibration has been computed.
- Source Hap reference is a different truncation and cannot certify this new paired model.

## Callable route and pilot

Gaussian/ORCA DFT, fragment single points and wavefunction analysis; Multiwfn and available multireference diagnostic if necessary. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Validate one full/truncated pair and neutral fragment doublets, source-relativity consistency and state stability before distance/twist scans.

## Minimum complete reference

1. Assemble full/truncated A,C dimers independently, test singlet/BS/triplet solutions and validate retained minima with spin/occupation evidence.
2. Using the fixed neutral-doublet decomposition, calculate equilibrium and rigid distance/twist controls, fragment relaxation terms and density differences at both model sizes.
3. Compare orbital mixing, densities, bond indices and interaction response to identify which explanations survive truncation and method/fragment sensitivity.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
