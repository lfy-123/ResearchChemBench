# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp3/5 and SI pp21–22 exact DFT/ECP/thermochemistry definitions, p33 reference13 (Dolg et al., Theor. Chim. Acta 75,173–194,1989) and water equations. Checked 81-atom C32H38N4O6La+ starting structures. After BSE RLC lacked Ln entries, fetched the exact MWB ECP and (7s6p5d)/[5s4p3d] basis from the originating University of Cologne library. Parsed coefficients: cores46/54/60, 11 explicit atom electrons, primitive7s6p5d and contracted5s4p3d for all three. Input gate resolved by actual files; no engine parsing/minimum/expanded reference has been run.

- `papers/paper_d8e5490cd9942f4f/documents/main.pdf` — [3, 5]
- `papers/paper_d8e5490cd9942f4f/documents/supplementary_001.pdf` — [21, 22]
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_La_ECP46MWB.txt` — Official originating-library molecular ECP/basis coefficients; parsed identity only.
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_La_basis.gbs` — Official originating-library molecular ECP/basis coefficients; parsed identity only.
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Lu_ECP60MWB.txt` — Official originating-library molecular ECP/basis coefficients; parsed identity only.
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Lu_basis.gbs` — Official originating-library molecular ECP/basis coefficients; parsed identity only.
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Tb_ECP54MWB.txt` — Official originating-library molecular ECP/basis coefficients; parsed identity only.
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Tb_basis.gbs` — Official originating-library molecular ECP/basis coefficients; parsed identity only.
- `docs/evalution/update/paper_d8e5490cd9942f4f.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- Engine input parsing and an actual minimum/frequency pilot with the verified supplied coefficients remain unperformed.
- Expanded metal/hydration minima, thermochemical cycles and uncertainty remain uncomputed.

## Callable route and pilot

Gaussian/ORCA molecular ECP calculations using the supplied verified coefficient files; GoodVibes or independently checked thermochemistry. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Parse the supplied exact ECP/basis blocks in the chosen engine, verify molecular electron counts, then run one La minimum/frequency and one Tb single point before the expanded reference.

## Minimum complete reference

1. Use and verify the supplied exact ECP/basis files in the selected engine, then validate dry/hydrated syn/anti models for all metals and report matched thermochemistry with collapse evidence where appropriate.
2. Calculate dry frozen La-skeleton metal replacements and matched water-addition cycles; separate relaxation and hydration contributions to within-metal preferences.
3. Audit ECP/basis electron counts and repeat the decisive low-frequency or solvation choice. Explain conformational trends only within the validated model.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
