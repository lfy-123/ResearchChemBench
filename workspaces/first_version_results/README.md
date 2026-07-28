# First-Version Experiment Results

This directory contains the 14 formal Agent runs summarized in
`docs/results/RESEARCHCHEMBENCH_EXPERIMENT_RESULTS_SUMMARY_20260728.md`.

- Code version: Git tag `第一版代码`
- Tagged commit: `367f3f8`
- Agent model: `deepseek-v4-flash`
- Judge model: `deepseek-v4-flash`
- Scoring rule: `dual_axis_100`
- Run directory: `workspaces/first_version_results/runs`
- Older trials and intermediate results: `workspaces/previous_results`

## Formal Runs

| Task | Mode | Run directory |
|---|---|---|
| `GEOM_Hierarchical_Conformer_Reranking` | Autonomous | `runs/GEOM_Hierarchical_Conformer_Reranking_opencode_20260726_103452_37b4ec` |
| `GEOM_Hierarchical_Conformer_Reranking_Reproduction` | Reproduction | `runs/GEOM_Hierarchical_Conformer_Reranking_Reproduction_opencode_20260726_090315_8d11a2` |
| `Electron_Flexible_Ensemble_Surface` | Autonomous | `runs/Electron_Flexible_Ensemble_Surface_opencode_20260726_105217_64d3fa` |
| `Electron_Flexible_Ensemble_Surface_Reproduction` | Reproduction | `runs/Electron_Flexible_Ensemble_Surface_Reproduction_opencode_20260726_101013_2c9b71` |
| `Electron_Isodensity_04_Blind_Prediction` | Autonomous | `runs/Electron_Isodensity_04_Blind_Prediction_opencode_20260725_095033_10564d` |
| `Electron_Isodensity_Reproduction_04_Blind_Prediction` | Reproduction | `runs/Electron_Isodensity_Reproduction_04_Blind_Prediction_opencode_20260725_062227_c10a4f` |
| `PV_Protonation_Barrier_Trend` | Autonomous | `runs/PV_Protonation_Barrier_Trend_opencode_20260728_030321_c1df11` |
| `PV_Protonation_Barrier_Trend_Reproduction` | Reproduction | `runs/PV_Protonation_Barrier_Trend_Reproduction_opencode_20260728_031154_f9bb6b` |
| `BaO_Phase_Crossover_And_5d_Bonding` | Autonomous | `runs/BaO_Phase_Crossover_And_5d_Bonding_opencode_20260728_032019_e2addb` |
| `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | Reproduction | `runs/BaO_Phase_Crossover_And_5d_Bonding_Reproduction_opencode_20260728_033821_00e073` |
| `Heterobiaryl_PV_02_CC_Selectivity` | Autonomous | `runs/Heterobiaryl_PV_02_CC_Selectivity_opencode_20260728_052721_eb0869` |
| `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | Reproduction | `runs/Heterobiaryl_PV_Reproduction_02_CC_Selectivity_opencode_20260728_053512_d4d0d9` |
| `Heterobiaryl_PV_05_Rate_Determining_Step` | Autonomous | `runs/Heterobiaryl_PV_05_Rate_Determining_Step_opencode_20260728_054620_5ce409` |
| `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | Reproduction | `runs/Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step_opencode_20260728_055337_f38dbd` |

The run directories are intentionally ignored by Git because they contain large generated
artifacts. This README and the result reports are the version-controlled index.
