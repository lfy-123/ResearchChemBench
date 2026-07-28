# Paper Dual-Track Manual Rescoring Report

Date: 2026-07-28

## Scope

This report manually reviews the eight runs in:

`workspaces/submissions/paper_dual_track_release_20260728_030320/runs/cli_runs/batch_20260728_030321_6969b1`

The review covers each task's final report, structured deliverables, failure log, managed tool trace, public scoring rubric, evidence gates, reference-conclusion gates, and the original Judge score. The manual score follows the task's current public rules rather than assigning one common rubric retrospectively.

## Executive Summary

| Task ID | Mode | Judge score | Manual score | Manual assessment |
|---|---|---:|---:|---|
| `PV_Protonation_Barrier_Trend` | autonomous | 0.0 | 10 | Managed analysis was attempted, but the thermochemistry and pathway selection were invalid and the second protonation effect was not resolved. |
| `PV_Protonation_Barrier_Trend_Reproduction` | reproduction | 64.8 | 38 | Strongly exergonic profiles were recovered, but the required P1 to P2 barrier reduction was not reproduced. |
| `BaO_Phase_Crossover_And_5d_Bonding` | autonomous | 71.0 | 38 | The VASP data support the phase sequence, but the final reported transition pressures are wrong and contradict the generated enthalpy table. |
| `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | reproduction | 91.0 | 90 | The phase sequence and both accepted transition-pressure neighborhoods were reproduced with real managed VASP and EOS analysis. |
| `Heterobiaryl_PV_02_CC_Selectivity` | autonomous | 55.0 | 38 | Author filename/path labels were misinterpreted, producing an unsupported and opposite selectivity conclusion. |
| `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | reproduction | 28.0 | 19 | The same route-label error prevented recovery of the paper conclusion; GoodVibes and connectivity requirements were also incomplete. |
| `Heterobiaryl_PV_05_Rate_Determining_Step` | autonomous | 55.0 | 40 | The downstream ligand-coupling maximum was incorrectly assigned as the overall rate-determining step; no managed scientific analysis succeeded. |
| `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | reproduction | 20.0 | 20 | The downstream profile was parsed, but the paper's rate/selectivity/irreversibility role separation was not reproduced and no managed scientific call was made. |

The Judge mean is 48.1/100. The manual mean is 36.6/100.

## Scoring Method

`PV_Protonation_Barrier_Trend`, `PV_Protonation_Barrier_Trend_Reproduction`, `BaO_Phase_Crossover_And_5d_Bonding`, and `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` use `dual_axis_100`:

```text
final score = process score * scientific-conclusion score / 100
```

The two process rubrics use mode-specific wording but share seven categories: planning, method selection or fidelity, managed execution, validation, failure recovery, resource efficiency, and provenance.

`Heterobiaryl_PV_02_CC_Selectivity`, `Heterobiaryl_PV_Reproduction_02_CC_Selectivity`, `Heterobiaryl_PV_05_Rate_Determining_Step`, and `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` currently use `rubric_100`. Their criterion scores are summed and then reduced by any applicable evidence, managed-computation, or reference-conclusion cap.

This is a task-configuration inconsistency, not the intended dual-track scoring design. The common scoring engine implements `dual_axis_100` for both autonomous and reproduction tasks and deterministically computes:

```text
final score = scientific_conclusion_score * research_process_score / 100
```

The Heterobiaryl builder leaves the autonomous tasks on a legacy process-only rubric and explicitly rewrites the reproduction tasks to `rubric_100`. It does not create a shared `scientific_conclusion_rubric` or `dual_axis_scoring_policy` for these pairs. The current manual scores below therefore describe the rules actually used in this run, but the Q2/Q5 autonomous-versus-reproduction totals are not a valid like-for-like dual-axis comparison.

## Detailed Manual Scores

### `PV_Protonation_Barrier_Trend`

Process score:

| Criterion | Score |
|---|---:|
| Problem framing and route design | 14/20 |
| Method and tool selection | 4/15 |
| Managed execution and artifact flow | 12/15 |
| Validation, falsification, and uncertainty | 5/20 |
| Failure diagnosis and adaptation | 8/10 |
| Resource and search efficiency | 8/10 |
| Provenance and reproducibility | 6/10 |
| **Process total** | **57/100** |

Scientific-conclusion score:

| Criterion | Score | Finding |
|---|---:|---|
| Successive protonation barrier order | 10/40 | The reported values are nominally ordered, but P1 and P2 are not resolved within uncertainty and the selected pathway is not the required comparable coupling pathway. |
| Stepwise barrier-reduction scale | 8/35 | The first reduction is large, but the second is reported as only 0.21 kcal/mol rather than a smaller additional paper-scale reduction. |
| Exergonic profiles distinct from kinetic trend | 0/25 | Consistently referenced P0/P1/P2 reaction free energies were not reported. |
| **Scientific total** | **18/100** | |

Final manual score: `57 * 18 / 100 = 10.26`, rounded to **10/100**.

The submitted barriers were 38.73, 24.50, and 24.29 kcal/mol for P0, P1, and P2. The custom RRHO implementation was not cross-validated against the available GoodVibes workflow and contained incomplete or inconsistent temperature-correction logic. The report also incorrectly described the chemical system as a Pd-catalyzed coupling. The independently validated toolbox values are approximately 30.913, 19.814, and 14.300 kcal/mol.

### `PV_Protonation_Barrier_Trend_Reproduction`

Process score:

| Criterion | Score |
|---|---:|
| Protocol interpretation and execution plan | 17/20 |
| Method, parameter, and structure fidelity | 10/15 |
| Managed recomputation and artifact flow | 13/15 |
| Validation, numerical quality, and uncertainty | 8/20 |
| Failure diagnosis and protocol recovery | 10/10 |
| Resource and execution efficiency | 7/10 |
| Provenance and reproducibility | 8/10 |
| **Process total** | **73/100** |

Scientific-conclusion score:

| Criterion | Score | Finding |
|---|---:|---|
| Successive protonation barrier order | 15/40 | One selected series is nominally P0 > P1 > P2, but P1 and P2 differ by only 0.53 kcal/mol; the same-substituent series instead increases from P1 to P2. |
| Stepwise barrier-reduction scale | 12/35 | The first reduction is large, but the required second reduction is not recovered. |
| Exergonic profiles distinct from kinetic trend | 25/25 | All three reaction profiles are consistently reported as strongly exergonic on a similar scale. |
| **Scientific total** | **52/100** | |

Final manual score: `73 * 52 / 100 = 37.96`, rounded to **38/100**.

The report contains two series:

| Reported series | P0 | P1 | P2 | Reaction free energies |
|---|---:|---:|---:|---|
| Ph/OMe | 35.00 | 21.10 | 22.04 | -34.82, -34.27, -35.39 |
| Py/OMe to PyH+/OMe | 30.39 | 17.74 | 17.21 | -31.92, -32.03, -30.48 |

These results do not reproduce the validated 30.913, 19.814, and 14.300 kcal/mol trend, especially the P1 to P2 reduction. The original Judge scientific score of 80/100 is therefore too high.

### `BaO_Phase_Crossover_And_5d_Bonding`

Process score:

| Criterion | Score |
|---|---:|
| Problem framing and route design | 18/20 |
| Method and tool selection | 13/15 |
| Managed execution and artifact flow | 10/15 |
| Validation, falsification, and uncertainty | 5/20 |
| Failure diagnosis and adaptation | 5/10 |
| Resource and search efficiency | 7/10 |
| Provenance and reproducibility | 5/10 |
| **Process total** | **63/100** |

Scientific-conclusion score:

| Criterion | Score | Finding |
|---|---:|---|
| BaO phase sequence | 40/40 | The real VASP data support B1 to B8 to dB2. |
| B1 to B8 transition pressure | 10/30 | The generated enthalpy table contains evidence near the accepted interval, but the final answer incorrectly reports 3.1 GPa. |
| B8 to dB2 transition pressure | 10/30 | The generated enthalpy table contains evidence near the accepted interval, but the final answer incorrectly reports 17.65 GPa. |
| **Scientific total** | **60/100** | |

Final manual score: `63 * 60 / 100 = 37.8`, rounded to **38/100**.

The final report and `phase_conclusion.json` state 3.1 and 17.65 GPa, both outside the accepted 6-12 and 20-30 GPa intervals. The generated enthalpy data instead support crossings near 6 and 29 GPa. The agent failed to detect this internal contradiction. The original Judge incorrectly assigned a 100/100 scientific-conclusion score by relying on the underlying table while ignoring the submitted conclusion.

### `BaO_Phase_Crossover_And_5d_Bonding_Reproduction`

Process score:

| Criterion | Score |
|---|---:|
| Protocol interpretation and execution plan | 18/20 |
| Method, parameter, and structure fidelity | 15/15 |
| Managed recomputation and artifact flow | 14/15 |
| Validation, numerical quality, and uncertainty | 17/20 |
| Failure diagnosis and protocol recovery | 10/10 |
| Resource and execution efficiency | 8/10 |
| Provenance and reproducibility | 8/10 |
| **Process total** | **90/100** |

Scientific-conclusion score:

| Criterion | Score | Finding |
|---|---:|---|
| BaO phase sequence | 40/40 | B1 to B8 to dB2 was recovered. |
| B1 to B8 transition pressure | 30/30 | 6.09 +/- 0.5 GPa lies in the accepted interval. |
| B8 to dB2 transition pressure | 30/30 | 29.0 +/- 1.0 GPa lies in the accepted interval. |
| **Scientific total** | **100/100** | |

Final manual score: `90 * 100 / 100 = 90/100`.

This run performed real managed VASP calculations, formula-unit normalization, fixed-volume internal relaxation, phase-identity checks, and two EOS fits. It is the only run in this batch that closely completes the intended scientific reproduction.

### `Heterobiaryl_PV_02_CC_Selectivity`

| Criterion | Score | Finding |
|---|---:|---|
| Scientific problem framing | 10/15 | A usable plan and stopping rules were provided. |
| Autonomous method and route design | 6/25 | The author archive labels were interpreted incorrectly, invalidating the pathway definition. |
| Adaptive managed execution | 16/25 | Several managed parsing programs succeeded and multiple parsing errors were repaired. |
| Validation and falsification | 4/20 | No forming-mode or connectivity validation was performed, and both actual path families were not compared correctly. |
| Defensible scientific conclusion | 2/15 | The claimed Ph-Py preference follows from a false "Py-Py TS absent" premise. |
| **Manual total** | **38/100** | |

The run reported Ph-Py barriers of 24.65, 19.33, and 11.25 kcal/mol for P0, P1, and P2 and concluded that Py-Py transition states were absent. This is a route-label error: the author archive's `Py` and `Ph` labels encode the mapped coupling outcome and must not be inferred by searching for a literal `Py,Py` transition-state filename. The resulting selectivity conclusion is unsupported and opposite to the paper target.

### `Heterobiaryl_PV_Reproduction_02_CC_Selectivity`

| Criterion | Score | Finding |
|---|---:|---|
| Paper conclusion agreement | 0/55 | The required kinetic Py-Py preference was not recovered. |
| Protocol fidelity | 5/20 | The mapped path definitions were misread and the required quasi-harmonic GoodVibes treatment was replaced by a harmonic fallback. |
| Managed recomputation | 8/10 | Several core parsing and energy-extraction programs ran successfully through managed execution. |
| Numerical and validation quality | 2/10 | The pathway mapping and references are invalid; no connectivity verification was supplied. |
| Provenance and uncertainty | 4/5 | Failures and artifact paths were documented clearly. |
| **Manual total** | **19/100** | |

The run reported Ph-Py barriers of approximately 23.1, 40.7, and 36.0 kcal/mol and treated the Py-Py pathway as absent. Because the same route-label error prevents reconstruction of both actual path families, the 55-point paper-conclusion criterion receives zero.

### `Heterobiaryl_PV_05_Rate_Determining_Step`

| Criterion | Score | Finding |
|---|---:|---|
| Scientific problem framing | 10/15 | Competing hypotheses were listed, but the upstream alcohol-addition question was not handled adequately. |
| Autonomous method and route design | 14/25 | A plausible downstream profile analysis was chosen, but it could not by itself assign the overall rate-determining step. |
| Adaptive managed execution | 6/25 | Managed analysis attempts did not produce the final scientific evidence; the final extraction used unmanaged commands. |
| Validation and falsification | 8/20 | Frequency counts were checked, but connectivity and the upstream/downstream mechanistic distinction were not established. |
| Defensible scientific conclusion | 2/15 | The downstream TS-I maximum was incorrectly equated with the overall reaction rate-determining step. |
| **Raw manual total** | **40/100** | |

The run reported a TS-I barrier of 8.76 kcal/mol and a TS-II local barrier of 7.37 kcal/mol, then assigned ligand coupling as both rate- and selectivity-determining. The task requires separate assessment of upstream alcohol addition, ligand-coupling selectivity, and post-coupling irreversibility. Because no managed scientific analysis succeeded, the managed-computation policy also limits the score to 40.

### `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step`

| Criterion | Score | Finding |
|---|---:|---|
| Paper conclusion agreement | 0/55 | The run assigned ligand coupling rather than upstream alcohol addition as the overall rate-determining step. |
| Protocol fidelity | 8/20 | The author outputs and GoodVibes conditions were used, but the required stage-role interpretation was not followed. |
| Managed recomputation | 0/10 | No managed Chemistry MCP scientific call was made. |
| Numerical and validation quality | 7/10 | The downstream profile is numerically plausible, but connectivity and the overall kinetic assignment are incomplete. |
| Provenance and uncertainty | 5/5 | Artifacts, experimental inputs, limitations, and uncertainty were documented. |
| **Raw manual total** | **20/100** | |

The reported downstream profile is 0.0, 13.90, -18.56, -10.77, and -32.26 kcal/mol for Int-I, TS-I, Int-II, TS-II, and Int-III. This profile can support a selectivity-determining ligand-coupling step and strongly exergonic downstream chemistry, but it does not show that ligand coupling is the overall rate-determining step. Zero managed scientific calls trigger the 20-point score cap.

## Why Some Autonomous Scores Exceed Reproduction Scores

The effect occurs for `Heterobiaryl_PV_02_CC_Selectivity` versus `Heterobiaryl_PV_Reproduction_02_CC_Selectivity`, and for `Heterobiaryl_PV_05_Rate_Determining_Step` versus `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step`.

Under the currently generated Heterobiaryl task files, the autonomous tasks use a legacy process-oriented 100-point rubric:

- scientific problem framing: 15 points;
- autonomous method and route design: 25 points;
- adaptive managed execution: 25 points;
- validation and falsification: 20 points;
- defensible scientific conclusion: 15 points.

Their generated ground truth has `evaluation_mode: rubric_100`, no `scientific_conclusion_rubric`, no `dual_axis_scoring_policy`, and an empty `reference_conclusion_gate_policy`. The builder also injects an evaluator instruction saying that agreement with the hidden paper conclusion is not required. This bypasses the common dual-axis outcome mechanism and allows the autonomous score to be determined entirely by the five process-oriented criteria.

The paired reproduction tasks instead allocate 55 points to `paper_conclusion_agreement`. If the paper conclusion is not matched, that criterion receives zero and the reference-conclusion policy can cap the total score at 45 or 60. Additional managed-computation caps can reduce the score to 20 or 40.

In this batch the autonomous Q2 and Q5 conclusions were not scientifically defensible, so the manual review reduced their conclusion and validation criteria. They nevertheless retain planning, method-selection, and attempted-execution points that the reproduction rubric assigns primarily to a 55-point conclusion gate. The resulting autonomous-over-reproduction ordering is caused by a builder/configuration defect that generated non-equivalent rubrics, not by better autonomous scientific performance.

## Judge Issues Found

1. `BaO_Phase_Crossover_And_5d_Bonding` received full scientific-conclusion credit even though its final answer reported 3.1 and 17.65 GPa, outside both accepted intervals.
2. `PV_Protonation_Barrier_Trend_Reproduction` received an 80/100 scientific score despite failing to reproduce the second protonation barrier reduction.
3. `Heterobiaryl_PV_02_CC_Selectivity` was not sufficiently penalized for an incorrect route-label interpretation and an unsupported opposite selectivity conclusion.
4. `Heterobiaryl_PV_05_Rate_Determining_Step` conflated the downstream ligand-coupling maximum with the overall rate-determining step but still reached the evidence-gate cap of 55.

## Recommendation

The Heterobiaryl Q2/Q5 builders should be migrated to the same structure already used by the P(V) protonation and BaO pairs:

- set `evaluation_mode` to `dual_axis_100` for both tracks;
- define one shared 100-point `scientific_conclusion_rubric` per pair;
- retain mode-specific 100-point process rubrics;
- set `dual_axis_scoring_policy.formula` to `scientific_conclusion_score * research_process_score / 100`;
- remove the reproduction-only 55-point conclusion criterion from the process rubric;
- use the scientific-conclusion axis, rather than a mode-specific hard gate, to make conclusion quality determine the score ceiling.

This would make both autonomous and reproduction tasks conclusion-limited while preserving their different research-process expectations.
