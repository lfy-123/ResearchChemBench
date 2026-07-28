# Paper Reproduction Dual-Track Release

Date: 2026-07-28

## Release decision

Four paper-derived scientific targets are validated for dual-track evaluation. Each pair now exposes the same raw scientific data and requires the same scientific deliverables and conclusion. The reproduction track additionally exposes the paper-reconstructed method and pathway; the autonomous track does not.

| Scientific target | Autonomous task | Reproduction task | Validation result |
|---|---|---|---|
| P(V) protonation-barrier trend | `PV_Protonation_Barrier_Trend` | `PV_Protonation_Barrier_Trend_Reproduction` | Validated from author Gaussian frequency and ORCA single-point archives |
| BaO pressure phase sequence | `BaO_Phase_Crossover_And_5d_Bonding` | `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | Validated from 15 real VASP phase-volume calculations and EOS fitting |
| Heterobiaryl P(V) C-C selectivity | `Heterobiaryl_PV_02_CC_Selectivity` | `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | Validated by common-reference reanalysis of P0/P1/P2 Py-Py and Ph-Py profiles |
| Heterobiaryl P(V) rate-determining-step argument | `Heterobiaryl_PV_05_Rate_Determining_Step` | `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | Validated from the P2 author archive plus supplied experimental observations |

`Heterobiaryl_PV_Reproduction_01_Protonation` is not submitted because it duplicates the generic P(V) protonation target.

## Numerical revalidation

The toolbox GoodVibes action was rerun at 353.15 K, 1 M, ethanol, with Grimme quasi-harmonic entropy and matched DLPNO single-point corrections. The common-reference pyridyl-pyridyl activation free energies were:

- P0: 30.913439 kcal/mol
- P1: 19.813510 kcal/mol
- P2: 14.300442 kcal/mol

The corresponding phenyl-pyridyl barriers were 37.319201, 26.860664, and 25.569542 kcal/mol. The P2 full profiles place the Py-Py transition state at 14.293681 kcal/mol and the Ph-Py transition state at 22.308195 kcal/mol, while the final Ph-Py product is more exergonic. This supports kinetic, rather than product-thermodynamic, Py-Py selectivity.

Independent Birch-Murnaghan refitting of the completed BaO calculations reproduced the B1 to B8 to dB2 sequence with crossings at 6.023422 and 28.909141 GPa. These values lie inside the task acceptance intervals around the paper's approximately 8 and 25 GPa transitions.

## Scope exclusions

The generic P(V) C-C versus C-O task and heterobiaryl Q3 are not released as fully reproducible tasks. The public author archive contains C-C transition states only; the published C-O barrier lacks a public frequency, connectivity, and matched high-level single-point package.

The BaO task is scored only on phase stability. The paper-equivalent custom Ba 5d LOBSTER projection basis is not publicly available, and the standard basis silently omits the requested 5d channel. Keeping that claim in the score would make a perfect reproduction impossible.

The NHC task is not included in this release because the complete published VASP-to-LOBSTER raw-output chain is unavailable and a fresh full calculation is outside the fast validation scope.

## Integrity checks

The task tests enforce the following release contract:

- shared scientific data have identical SHA-256 hashes across each dual-track pair;
- required deliverables and scientific conclusion rubric targets match within each pair;
- autonomous tasks contain no paper protocol or mapped pathway files;
- guided tasks add only the reconstructed protocol/pathway layer;
- manifests hash every visible input and record author archive provenance;
- all selected task builders and task-contract tests pass.

Validation artifacts are retained under `workspaces/paper_reproduction_recovery_20260727/final_validation`.
