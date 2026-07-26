# Multi-software autonomous research tasks

Date: 2026-07-26

## Scope

This change adds autonomous-discovery counterparts for six guided reproduction
tasks. The autonomous tasks retain the scientific question and raw input boundary,
but do not expose the source-paper software DAG, computational protocol, author
conformers, stationary-point candidates, optimized adsorption structures, or
numerical conclusions.

Generated pairs:

| Autonomous task | Guided counterpart | Current status |
|---|---|---|
| `GEOM_Hierarchical_Conformer_Reranking` | `GEOM_Hierarchical_Conformer_Reranking_Reproduction` | pre-release, pilot ready after oracle tolerance calibration |
| `Electron_Flexible_Ensemble_Surface` | `Electron_Flexible_Ensemble_Surface_Reproduction` | pre-release, pilot ready |
| `PV_Protonation_Barrier_Trend` | `PV_Protonation_Barrier_Trend_Reproduction` | blocked pending a validated closed pathway/reference route |
| `BaO_Phase_Crossover_And_5d_Bonding` | `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | phase part pilotable; bonding part should be split or kept optional |
| `PV_CC_CO_Pathway_Selectivity` | `PV_CC_CO_Pathway_Selectivity_Reproduction` | blocked pending curated endpoints/mapping and solvent-contract repair |
| `NHC_Adsorption_Decomposition_Bonding` | `NHC_Adsorption_Decomposition_Bonding_Reproduction` | blocked by adsorption placement, constraints, and native periodic/bonding gaps |

## Public input boundary

- GEOM: one molecular identity and physical conditions; no supplied conformers.
- Electron surface: one flexible molecular identity and experimental TE area; no
  author conformers, density method, cutoff, or numerical grid.
- P(V) protonation: nine independent unoptimized reactant embeddings for P0/P1/P2,
  atom mapping, and physical conditions; no intermediates or transition states.
- BaO: three opaque candidate phase seeds and a pressure range; no volume grid,
  phase sequence, or electronic/bonding protocol.
- P(V) selectivity: three unoptimized P2 reactant embeddings, mapping, conditions,
  and four experimental observations; no products, endpoints, or TS candidates.
- NHC adsorption: two matched clean surfaces and two isolated ligand seeds; no
  adsorbed starting geometry or adsorption site.

Every task has a SHA-256 input manifest. The manifest deliberately does not name
the paired reproduction task, so an evaluated agent cannot use the public metadata
as a pointer to a disclosed route.

## Evaluation contract

All six tasks use the same 100-point autonomous-discovery rubric:

- scientific problem framing: 15;
- autonomous method and route design: 25;
- adaptive managed execution: 25;
- validation and falsification: 20;
- defensible scientific conclusion: 15.

The hidden paper conclusion is post-hoc diagnostic evidence. It is not a required
conclusion gate, and `reference_conclusion_gate_policy` is empty for every task.
Precise numerical claims still require newly generated artifacts and task-specific
validity gates.

## Reproducible generation and tests

- Builder: `scripts/build_multisoftware_autonomous_tasks.py`
- Tests: `tests/test_multisoftware_autonomous_tasks.py`

The builder replaces only the six autonomous directories when invoked with
`--force`. Tests check task loading, hashes, hidden pairing, method/pathway
disclosure flags, prohibited visible route markers, absence of source-paper
protocol files, and task-specific raw input contracts.

Validation on 2026-07-26:

- autonomous plus reproduction task tests: `8 passed`;
- full repository: `303 passed, 2 failed`.

The two full-suite failures are unrelated to these tasks:

1. the existing open-discovery submission dry-run does not print the expected
   agent-model line;
2. the selected test environment lacks the `ase` dependency required by an
   existing electron-density backend unit test.

## Release recommendation

Do not put all six tasks into one formal model-ranking pool yet. Pilot GEOM and
Electron first and generate fresh oracle trajectories. Treat BaO phase stability as
a separate pilot from optional bonding analysis. Keep both P(V) tasks and NHC in
pre-release until their documented input/toolbox gaps are repaired and reference
runs establish fair numerical or bound-based scoring.
