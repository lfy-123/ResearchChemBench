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
| `BaO_Phase_Crossover_And_5d_Bonding` | `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | native VASP/LOBSTER route available; Gold Run required |
| `PV_CC_CO_Pathway_Selectivity` | `PV_CC_CO_Pathway_Selectivity_Reproduction` | blocked pending curated endpoints/mapping and solvent-contract repair |
| `NHC_Adsorption_Decomposition_Bonding` | `NHC_Adsorption_Decomposition_Bonding_Reproduction` | direct programming/native route available; adsorption Gold Run required |

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

All six tasks now use `dual_axis_100`:

- scientific-conclusion score `C`: three task-specific hidden paper claims totaling 100;
- autonomous research-process score `P`: problem framing, method selection, managed
  execution, validation, failure recovery, resource efficiency, and provenance,
  totaling 100;
- final score: `C * P / 100`.

The paper route remains hidden and is not mandatory in autonomous mode. The paper-level
scientific findings are mandatory for high conclusion credit and must be supported by
newly generated artifacts. `reference_conclusion_gate_policy` and the former separate
score-cap gates are empty because conclusion agreement is represented directly by `C`.

## Reproducible generation and tests

- Builder: `scripts/build_multisoftware_autonomous_tasks.py`
- Tests: `tests/test_multisoftware_autonomous_tasks.py`

The builder replaces only the six autonomous directories when invoked with
`--force`. Tests check task loading, hashes, hidden pairing, method/pathway
disclosure flags, prohibited visible route markers, absence of source-paper
protocol files, and task-specific raw input contracts.

Validation after the dual-axis migration on 2026-07-26:

- task, scoring, and schema regression selection: `28 passed`;
- all eight newly migrated tasks passed JSON, hash, input-boundary, hidden-claim,
  and score-total checks;
- the full suite still reaches the unrelated existing shell-entrypoint failure in
  `test_open_discovery_submission_script_has_model_specific_output_roots`.

## Release recommendation

Do not put all six tasks into one formal model-ranking pool yet. GEOM and Electron
have model trajectories, while the two P(V) tasks still need closed-path Gold Runs.
BaO and NHC can use the allowed direct native-software layer for VASP/LOBSTER and
adsorption setup, but still require fresh end-to-end Gold Runs before formal ranking.
