# Electron Isodensity Q4 Objective Feasibility Check

Date: 2026-07-25

Task: `Electron_Isodensity_Reproduction_04_Blind_Prediction`

## Conclusion

After correcting the Q4 task boundary, the current task inputs and chemistry toolbox can objectively reproduce the paper's held-out ISO-M4 result. The fresh toolbox calculation gave **110.05219 Å²** at the locked paper-calibrated cutoff of **0.0016 a.u.**, versus the paper value **109.9966 Å²**, a relative difference of **0.05054%**. The result also differs from the hidden experimental TE area, 110.538 Å², by only **0.43950%**.

No Flash-model evaluation was submitted during this check.

## Task-design correction

The original Q4 asked the agent to re-select a cutoff from only ISO-M1 to ISO-M3. A real full-grid calculation showed that this small subset objectively minimizes MUPE at 0.0014 a.u. (1.26869%), not at the paper-wide optimum of 0.0016 a.u. (subset MUPE 1.66436%). Applying 0.0014 to ISO-M4 gives 112.48778 Å², 2.26478% above the paper result. Therefore the old task could penalize a scientifically correct execution for a non-conclusion-preserving subset.

Q4 now treats 0.0016 a.u. as a disclosed, locked production-protocol parameter. This is consistent with the task decomposition: Q3 evaluates cutoff calibration, while Q4 evaluates blind application of the already calibrated paper protocol. ISO-M1 to ISO-M3 are validation systems in Q4 and no longer form a replacement calibration dataset.

The Q4 instruction now also states that, within server and backend limits, the agent should use substantial CPU parallelism, approximately 2000 MB per ORCA process, and concurrent independent molecule calculations when safe.

## Real tool execution

The test used the public task conformers and three existing general Actions; no task-specific Action or author quantum result was used.

| Stage | Action | Backend | Main settings |
|---|---|---|---|
| Production density | `calculate_correlated_electron_density` | ORCA 6.1.1 | DSD-PBEP86-D3BJ/def2-QZVPD, def2-TZVPD/C, NoFrozenCore, PModel, VeryTightSCF, stability analysis, relaxed MP2 density, 16 CPU, 32000 MB |
| Wavefunction export | `export_electron_density_grid` | ORCA `orca_2aim` | relaxed-MP2 source, WFN output |
| Surface analysis | `calculate_electron_isodensity_surface` | Multiwfn 2026.7.15 | 0.0008–0.0025 a.u. in 0.0001 increments, numerical grid setting 0.1, 8 CPU |

There were 12 successful Action calls: four ORCA density calculations, four WFN exports, and four 18-point Multiwfn scans. No Action failed.

## Numerical results at 0.0016 a.u.

| Molecule | Fresh toolbox area (Å²) | Paper area (Å²) | Relative difference |
|---|---:|---:|---:|
| ISO-M1 | 75.58673 | 75.61296 | 0.03469% |
| ISO-M2 | 95.58247 | 95.76939 | 0.19518% |
| ISO-M3 | 110.77191 | 110.97050 | 0.17896% |
| ISO-M4 | 110.05219 | 109.99660 | 0.05054% |

The four molecules completed sequentially in approximately 93.15, 171.79, 251.18, and 253.29 seconds. Total sequential wall time was about 12.82 minutes; every individual molecule remained below the benchmark's ten-minute per-calculation target. Independent molecule execution can be parallelized by an agent to reduce end-to-end wall time further.

## Evidence location

The real ORCA outputs, GBW/MP2 natural-orbital files, WFN exports, Multiwfn outputs, and Action result JSON files are under:

`workspaces/electron_isodensity_reproduction/q4_oracle_20260725/`

The directory contains about 92 MB of generated calculation evidence and is intentionally outside the agent-visible task input data.

## Remaining caveats

- The installed Multiwfn adapter's historical public field is named `grid_spacing_angstrom`, while the installed Multiwfn menu describes this numerical input in Bohr. The numerical value 0.1 reproduces the paper values closely, but the API unit label should eventually receive a compatibility-safe cleanup.
- This check establishes objective environmental feasibility. It does not establish that a particular language model will follow the supplied route, preserve the blind boundary, or use resources efficiently.
