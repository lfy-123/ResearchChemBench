# Autonomous Research Hidden Scientific Gates

Date: 2026-07-26

## 1. Why the previous scores were too high

The six multi-software autonomous tasks previously used an intentionally process-oriented
`autonomous_discovery` rubric:

- scientific framing: 15
- autonomous method and route design: 25
- managed execution: 25
- validation and falsification: 20
- defensible conclusion: 15

The evaluator was explicitly told that agreement with the hidden paper conclusion was not
required, and `reference_conclusion_gate_policy` was empty. Consequently, an Agent could
receive a high score for a coherent plan, several successful software calls, and a cautious
report even when it had not completed the scientific question or recovered the paper-level
finding.

That design measured workflow competence, but it was too permissive for a benchmark whose
goal is successful autonomous scientific investigation.

## 2. New evaluation principle

The autonomous task still hides all paper methods, software routes, parameters, author
intermediates, and numerical answers. The Agent may choose any scientifically valid route.

However, the evaluator now has a hidden scientific acceptance contract. High credit requires
the Agent's newly generated evidence to recover the required paper-level scientific findings.
Method agreement is not required; scientific-outcome agreement is required.

The new 100-point rubric is:

| Criterion | Points | Meaning |
|---|---:|---|
| Hidden scientific conclusion recovery | 50 | Recover all task-level scientific findings from new evidence. |
| Autonomous method and route design | 20 | Independently frame hypotheses and select methods, alternatives, controls, and stopping rules. |
| Adaptive managed execution | 10 | Execute real managed calculations and recover from failures. |
| Validation and falsification | 15 | Establish convergence, chemical validity, numerical robustness, and competing-explanation checks. |
| Provenance and uncertainty | 5 | Link claims to artifacts and report uncertainty and failed branches honestly. |

Tool execution therefore remains necessary but is no longer the dominant source of points.

## 3. Programmatic score caps

The score engine now selects a strict autonomous judge prompt whenever an autonomous task has
a required reference-conclusion policy. The final score is then programmatically capped even
if the LLM Judger initially awards excessive criterion scores:

| Hidden conclusion status | Overall maximum | Maximum conclusion credit |
|---|---:|---:|
| `matched` | no conclusion cap | 50/50, subject to evidence quality |
| `uncertain` | 60 | 20/50 |
| `not_matched` | 40 | 0/50 |
| omitted/invalid status | 35 | 0/50 |

`matched` means that every required qualitative finding is supported by valid newly generated
evidence. A plausible narrative, unsupported paper-like statement, or numerically coincidental
answer is insufficient.

## 4. Task-specific hidden scientific gates

### GEOM Hierarchical Conformer Reranking

Required hidden findings:

1. The low-cost search covers multiple thermally relevant structural basins.
2. Identity-preserving quantum refinement and thermochemical treatment materially change at
   least one ranking or population conclusion.

Additional gates now check sampling coverage/convergence and whether a 298.15 K population is
actually supported by thermochemistry or by an explicitly bounded electronic-energy proxy.
A set of single-point electronic energies cannot silently be presented as a rigorous thermal
population analysis.

### Electron Flexible Ensemble Surface

Required hidden findings:

1. Newly computed conformer surfaces differ materially relative to numerical/grid uncertainty.
2. A traceable thermally weighted ensemble reduces arbitrary single-conformer dependence.

Additional gates compare the conformer effect with cutoff/grid sensitivity and require valid
weight normalization, conformer-truncation analysis, and weighting sensitivity. Merely running
several density calculations is insufficient.

### PV Protonation Barrier Trend

Required hidden findings:

1. Comparable P0, P1, and P2 evidence establishes the barrier order P0 > P1 > P2.
2. The first protonation produces a larger reduction than the second, without requiring exact
   reproduction of every rounded paper barrier.

The new trend-resolution gate requires validated transition states or controlled bounds strong
enough to determine the order for all three states.

### BaO Phase Crossover and 5d Bonding

Required hidden findings:

1. The enthalpy curves recover the B1 -> B8 -> dB2 sequence and both crossover regions.
2. Quality-gated orbital evidence supports selective Ba 5d-O stabilization of the denser phases.

Phase stability alone is partial completion. Separate gates require crossover resolution and a
fresh projection-ablation or equivalent orbital-resolved test. This also makes the existing
toolbox limitation visible rather than allowing workflow points to conceal it.

### PV C-C/C-O Pathway Selectivity

Required hidden findings:

1. Comparable kinetic evidence identifies C-C coupling as preferred.
2. C-O remains accessible but disfavored under the stated conditions.

The selectivity gate requires both pathways to be tested with compatible references and valid
transition states or controlled bounds.

### NHC Adsorption, Decomposition, and Bonding

Required hidden findings:

1. NHC4 is only modestly more strongly adsorbed overall than NHC1.
2. NHC4 has stronger local Pd-C bonding indicators, while deformation and other contributions
   moderate the total binding-energy difference.

Separate gates require matched adsorption references, the adsorption ordering and decomposition,
and a scientifically correct distinction between local bonding descriptors and total energy.

## 5. Effect on the previous Flash pilot interpretation

The earlier GEOM and Electron autonomous Flash scores should not be treated as final scores under
this revised standard. They were produced with the older process-heavy rubric.

- The GEOM trajectory used higher-level single-point reranking but did not establish a complete
  thermochemical population treatment. Under the new policy, failure of the thermochemical
  population gate limits the score to at most 65, even if the qualitative reranking narrative is
  plausible.
- The Electron trajectory used only a small conformer subset and electronic-energy-based weights
  without a complete convergence/weighting sensitivity argument. If the strict evaluator finds
  that the ensemble-validity contract is not met, the score is limited to at most 65.

These are policy implications, not retrospective official rescoring. A new evaluation run is
needed to obtain official scores with the revised Judger prompt and gates.

## 6. Files changed

- `evaluation/score.py`: strict autonomous outcome prompt and generic conclusion-cap wording.
- `scripts/build_multisoftware_autonomous_tasks.py`: new rubric, conclusion policy, hidden
  acceptance contracts, and task-specific scientific gates.
- Six autonomous `target_study/ground_truth.json` files: regenerated evaluator-only definitions.
- `tests/test_score.py`: verifies that a self-awarded 100 is capped to 40 for a mismatched hidden
  scientific conclusion.
- `tests/test_multisoftware_autonomous_tasks.py`: verifies the 50-point conclusion criterion,
  required conclusion policy, and task-specific gates.

## 7. Verification

The following targeted suite passed:

```text
24 passed in 18.64s
```

It covers task loading, dual-track task contracts, reproduction-task integrity, autonomous-task
input leakage checks, rubric validation, evidence caps, and strict hidden-conclusion caps.

The complete repository suite produced `313 passed, 1 failed`. The single failure is the existing
shell-entrypoint expectation that the printed Pro model name includes the `bailian/` prefix; the
unchanged submission script currently prints `deepseek-v4-pro`. It is unrelated to the scoring or
task-ground-truth changes in this audit.
