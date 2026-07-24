# Evaluation Profiles and Electron Isodensity Q1 Grid Audit

Date: 2026-07-24

## Evaluation profiles

ResearchChemBench now distinguishes two evaluation objectives.

| Profile | Main dimensions | Reference-conclusion policy |
|---|---|---|
| Autonomous scientific discovery | problem framing 15; autonomous method/route design 25; adaptive managed execution 25; validation/falsification 20; defensible conclusion 15 | Agreement with the hidden paper conclusion is not required when the independent conclusion is supported by valid evidence. |
| Paper reproduction | paper conclusion agreement 55; protocol fidelity 20; managed recomputation 10; numerical/validation quality 10; provenance/uncertainty 5 | A conflicting main conclusion receives zero conclusion credit and caps the total at 45. An uncertain conclusion is capped at 60. |

For reproduction tasks, the judge must return `reference_conclusion_status` as
`matched`, `not_matched`, or `uncertain`. The evaluator applies the score cap
deterministically. Electron Isodensity Q1 also checks
`report/method_comparison.json:production_method.recovered`; an explicit
`false` overrides a judge that incorrectly reports a match.

## Q1 high-resolution diagnosis

The completed DeepSeek V4 Flash run used a 300³ CCSD/MDCI cube for ISO-M1 but
downgraded ISO-M2 and ISO-M3 to 100³ after 600-second synchronous timeouts.
The original 300³ `orca_plot` processes continued after the timeout and later
wrote valid cubes, but the Agent no longer observed them.

The retained 300³ cubes were reanalyzed over all 18 density cutoffs. Their
integrated electron-count errors were 0.0161% for ISO-M2 and 0.0127% for
ISO-M3, both within the new 0.2% strict-validation threshold.

| Reference treatment | PBE average MUPE | B3LYP average MUPE | DSD-PBEP86 average MUPE | Best |
|---|---:|---:|---:|---|
| Original run, including 100³ ISO-M2/ISO-M3 references | 0.3797% | 0.2679% | 0.5896% | B3LYP |
| Reanalysis with 300³ references for all three molecules | 0.1822% | 0.4277% | 0.2739% | PBE |
| Paper result | 0.24% | 0.36% | 0.08% | DSD-PBEP86 |

The 100³ downgrade was therefore a material source of the incorrect B3LYP
ranking, but it was not the sole cause of the failure to reproduce the paper.
At consistent 300³ resolution, the three-molecule Q1 subset still does not
recover DSD-PBEP86.

## Remaining reproduction gap

The paper's method selection is based on its full molecular/conformer study,
whereas the benchmark Q1 exposes only one conformer each for ISO-M1 to ISO-M3.
That subset is not conclusion-preserving under the currently feasible
calculation. In addition, ORCA 6.1 provides a reproducible unrelaxed CCSD
density but not a true CCSD(T) one-particle density, and the previous run also
introduced frozen-core and stability-analysis deviations.

Consequently, Q1 is currently classified as `partially_solvable`, and it was
not resubmitted after this audit: adding CPU resources cannot make a
single-process `orca_plot` export faster, and a corrected 300³ rerun is still
expected to select PBE on the supplied subset.

## Reliability changes

- The default MCP client timeout is now 7500 seconds, longer than the 7200-second synchronous ORCA ceiling.
- Timed-out external programs are terminated as a complete process group, preventing orphan ORCA/orca_plot children and late untracked artifacts.
- A 300³-or-larger MDCI cube request now requires at least 1800 seconds of declared walltime.
- Cube export reports expected and integrated electron counts, error percentage, tolerance status, and optional strict rejection.
- Q1 explicitly requires a common 300³ reference grid, strict electron-count validation at no more than 0.2%, preserved protocol fidelity, and sufficient walltime.
- The tool catalog now states that `orca_plot` cube export is single-process; CPU parallelism must be applied across independent molecule exports.

## Required Q1 redesign before another benchmark run

Choose one of the following before resubmission:

1. Curate and independently verify a small, conclusion-preserving molecular/conformer subset that recovers the paper's DSD-PBEP86 ranking with the exact benchmark software route.
2. Expose the full paper comparison set and accept the much larger runtime and storage cost.
3. Change the task target to reproduction of the supplied subset result instead of the paper-wide method-selection conclusion; this is no longer a strict reproduction of Table 1.

For exact protocol fidelity, a backend capable of the paper's intended
CCSD(T)-density treatment, or a documented determination that the author used
the CCSD density associated with a CCSD(T) calculation, is also required.
