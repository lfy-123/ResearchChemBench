# Stage02/Stage03 final calibration report (2026-08-10)

## Objective and audit method

The calibrated gates target high precision in this order:

1. retain original, in-scope, pure computational-chemistry papers;
2. reject current-author physical experiments and non-original articles;
3. retain only papers whose required software is present in the frozen three-layer toolbox;
4. hold papers whose core scientific implementation cannot be identified.

All 76 papers in the hard calibration set were read against main text and every known SI document. After every
code change, the complete set was replayed; all Stage03 passes and all Stage03 rejects/holds were then reviewed
again using their evidence, workflow inventory, required-software mapping, and current toolbox snapshot.

The implementation deliberately uses general contracts rather than paper IDs, title lists, or product-specific
exceptions. Stage02 requires positive evidence for a computational-chemistry task family. Stage03 combines
evidence-bound model extraction with catalog aliases and general executable syntax; it never infers support from
general software knowledge.

## Final observed results

Run: `data_pipeline/runs/v2_gold76_flash_r14_20260810`

| Gate | Input | Pass | Reject | Hold/error |
|---|---:|---:|---:|---:|
| Stage02 pure computational chemistry | 76 | 65 | 11 | 0 |
| Stage03 toolbox software coverage | 65 | 13 | 48 | 4 / 0 |

Stage02 rejects comprise seven out-of-scope computational papers, two mixed experimental/computational papers,
and two review/commentary articles. Stage03 has no processing errors. Its four holds lack a named core solver:
an unnamed microkinetic ODE solver, unnamed DFT/topology engines, unnamed MD/free-energy engines, and unnamed
wave-packet/QCT implementations.

The 13 manually confirmed Stage03 passes are:

- `paper_371f15fb65bd60c3`: VASP, Materials Project, pymatgen.
- `paper_4a217ec2ed066e3f`: CP2K, Gaussian.
- `paper_511cc19067df008b`: ORCA plus task-specific analytic Python.
- `paper_59d787fdcd19352b`: OpenMM, MDTraj, Packmol.
- `paper_6c26b11ef14b1e06`: ORCA, Gaussian.
- `paper_726a75e9ac4eff5b`: VASP plus task-specific entropy analysis.
- `paper_768e15849d5eff5d`: LAMMPS, NumPy.
- `paper_83bcb87e982af6fa`: Packmol, LAMMPS, CP2K, PLUMED.
- `paper_e1c7cc620647cd21`: VASP.
- `paper_e68148717191f0d6`: Gaussian, OpenMM, PLUMED plus task-specific model code.
- `paper_e86c38ea6471168b`: GPAW, ASE.
- `paper_f95d34466bfd9110`: VASP, Gaussian.
- `paper_fccb6813a9f5b43b`: VASP, ASE.

Every one of the 48 explicit rejects has at least one real missing required package, extension, or exact custom
runtime. Incidental packages found in a lock file but absent from a managed runtime/module contract are not
declared as toolbox capabilities.

## Problems fixed

- Replaced a negative keyword blacklist with a positive computational-chemistry workflow boundary.
- Kept deterministic current-author laboratory evidence and non-original-article guards.
- Fixed alias collisions so canonical software IDs take precedence; ORCA no longer resolves to PyFrag.
- Preserved exact development/local/custom runtime identities instead of collapsing them to public parents.
- Separated ordinary task-specific Python analysis from unnamed core DFT/MD/kinetics/dynamics engines.
- Added evidence-guided lowercase software discovery without force-merging ordinary English nouns.
- Recovered omitted software quotes from bound evidence instead of failing the paper.
- Resolved compound plugin and decorated method names without collapsing independent packages into parents.
- Added an immutable hash over the complete screening capability snapshot.
- Confirmed that removed software, including Q-Chem, TURBOMOLE, TeraChem, Molpro, and CASTEP, is not exported.

## Final pipeline flow

1. **Stage00 corpus assembly**: copy a bounded remote sample and group main PDF plus known SI by paper.
2. **Stage01 acquisition and low-cost normalization**: find only missing SI; parse main and all SI with GROBID,
   falling back to `pdftotext`; an incomplete document bundle cannot enter Stage02.
3. **Stage02 pure computational chemistry**: evidence map/reduce over main plus SI, deterministic experiment and
   article-type audit, positive computational-chemistry domain gate, and strict pure-computation decision.
4. **Stage03 toolbox/resource gate**: extract complete workflows and actual required software, preserve exact
   extensions/custom runtimes, resolve against the frozen three-layer toolbox, and perform preliminary resource
   extraction. Missing software rejects; unnamed core engines hold; short task-specific Python is allowed.
5. **Stage04 high-quality normalization**: release the screening model and run GPU MinerU only for Stage03 passes.
6. **Stage05 suitability review**: a separately configured strong API model checks the ten task directions,
   nontrivial scientific workflow, objective targets, assets, and benchmark suitability.
7. **Stage06 Builder**: an independent configurable model constructs the paired autonomous/reproduction task.
8. **Stage07 Judge**: an independent configurable model validates faithfulness, leakage, executability, scoring,
   and final resource feasibility.

The deployed Qwen model path remains supported, but GPU scheduling reported zero schedulable nodes during this
calibration. The complete semantic rerun therefore used `deepseek-v4-flash` through the configured proxy; raw
responses and hashes are cached for replay. Qwen parity should be run when an H200 worker is available.
