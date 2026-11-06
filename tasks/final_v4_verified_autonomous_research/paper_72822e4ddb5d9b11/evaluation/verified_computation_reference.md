## 2026-10-28 V3范围与逐命题证据复用

r_ground_state：复用SOURCE_ROUTE_MATRIX和NATIVE_STATE_REVIEW的完整165原子/678电子态表，四态489个正模，B3LYP/BP86电子T−CS差32.2199006522/27.1657322700 kcal/mol；既有BS坍塌只作为支持闭壳层的证据，不要求被测者重走该操作。r_axial_mixing/r_equatorial_mixing：NI_MO_COMPARISON_RESULTS逐MO表分别给B3LYP Ni Mulliken占比39.5%/43.2%，Loewdin43.6%/47.0%；同时有轴向Cl和赤道C/N贡献。r_formal_valence：同电子占据/组成与正文Fig5支持Ni(IV)形式极限。r_physical_oxidation_limit：两泛函/两布居分区及来源未指定方案支持物理氧化态不可唯一确定。

证据缺口：旧批准为用户接受的定性结果及数值偏差，不是严格源值复现；电子态差相对源31.4/25.1 kcal/mol残差+0.8199006522/+2.0657322700；基态绝对能偏差约252–260 kcal/mol，不能归咎于未证明的软件版本效应；源TableS1只标Energy，E/E+ZPE/G不明；Fig5 Ni%布居定义也不唯一；有限态搜索不证明跨所有方法唯一基态。本轮未重新计算、未进行盲测或语义评分验证；以下历史正文逐字保留，不继承旧PASS为V3全部通过。活动标准以scoring_rules.json为准。

# Nickel carbaporphyrin: verified computation reference

## Current acceptance — 2026-10-20

**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**. Formal scoring is permitted for the unchanged bounded task. Original numerical gates have not been declared passed. No new quantum chemistry or HPC jobs were run during this scoring migration. This is a retrospective source/native verification, not an information-limited blind Agent experiment.

Current scientific scope: Electronic state and metal–ligand bonding of full neutral complex 4; no water reactivity or rate task.

Current scoring is paper_science_v2: 100 points, independent binary intermediate and conclusion leaves, no process score or multiplier. AR retains method freedom; PR follows the disclosed baseline or substantiates an equivalent. The public contract is byte-frozen, including stale process/calibration wording; current private scoring supersedes those legacy evaluator statements.

## Objects, methods and completed workflow

Full neutral C87H72Cl2N2NiO complex 4, 165 atoms and 678 electrons, both axial Cl retained. Compare like states and energy definitions; CS is singlet, T is triplet. Ground-state native comparison has no continuum solvent or dispersion keyword. Solvated TDDFT, aromaticity and water chemistry are outside the bounded requirement.

The retained calculations use ORCA 6.1.1, B3LYP and BP86, def2-TZVP on Ni and its six directly coordinated Cl/N/C atoms (one-based 1,3,5,7,9,49,59), and def2-SVP on the remaining 158 atoms: 1807 orbital basis functions. VeryTightSCF and DEFGRID3 were used. The verifier optimized CS/T structures, checked gradients and same-geometry Hessians/stability, tested independent broken-symmetry starts, compared six coordination distances, and read orbital populations for the axial/equatorial channels. These are retained verification choices, not mandatory AR search instructions. Source SI physical p10–11 specifies the functional/mixed-basis route.

All four minima have 489 positive modes; minimum frequencies are 8.6983/9.1782 cm−1 (B3LYP CS/T) and 8.3126/8.6251 cm−1 (BP86 CS/T), with positive stability eigenvalues. Some native optimizations signal convergence via overachieved gradients despite a remaining displacement flag; the reference does not rewrite every row as YES. Both BS starts in each method collapse to CS (electronic differences less than 0.00053 kcal/mol), not independent OSS minima.

## Full thermal-definition ledger and deviations

Source Table S1 labels its absolute values only Energy, so E, E+ZPE and G are all retained; none is selected because it is numerically closer. Thermochemistry is native 298.15 K/1 atm. Signed residual is native minus source; relative percentages of huge absolute electronic energies are not scientifically meaningful.

| State | Native definition | Source Energy kcal/mol | Native Eh | Native kcal/mol | Signed residual kcal/mol | Absolute residual |
| --- | --- | --- | --- | --- | --- | --- |
| B3LYP CS | E_freq | -3745020.4 | -5967.657038890000 | -3744761.32986282 | +259.07013718 | 259.07013718 |
| B3LYP CS | E_stable | -3745020.4 | -5967.657035789726 | -3744761.32791737 | +259.07208263 | 259.07208263 |
| B3LYP CS | E_plus_ZPE_freq | -3745020.4 | -5966.318540190000 | -3743921.40924755 | +1098.99075245 | 1098.99075245 |
| B3LYP CS | U_freq | -3745020.4 | -5966.236460570000 | -3743869.90350837 | +1150.49649163 | 1150.49649163 |
| B3LYP CS | H_freq | -3745020.4 | -5966.235516360000 | -3743869.31100765 | +1151.08899235 | 1151.08899235 |
| B3LYP CS | G_freq | -3745020.4 | -5966.420746440000 | -3743985.54463773 | +1034.85536227 | 1034.85536227 |
| B3LYP CS | E_stable_plus_ZPE | -3745020.4 | -5966.318537089726 | -3743921.40730210 | +1098.99269790 | 1098.99269790 |
| B3LYP CS | E_stable_plus_H_minus_Efreq | -3745020.4 | -5966.235513259726 | -3743869.30906220 | +1151.09093780 | 1151.09093780 |
| B3LYP CS | E_stable_plus_G_minus_Efreq | -3745020.4 | -5966.420743339726 | -3743985.54269228 | +1034.85730772 | 1034.85730772 |
| B3LYP T | E_freq | -3744989.0 | -5967.605693210000 | -3744729.10996217 | +259.89003783 | 259.89003783 |
| B3LYP T | E_stable | -3744989.0 | -5967.605693253608 | -3744729.10998953 | +259.89001047 | 259.89001047 |
| B3LYP T | E_plus_ZPE_freq | -3744989.0 | -5966.270872670000 | -3743891.49742714 | +1097.50257286 | 1097.50257286 |
| B3LYP T | U_freq | -3744989.0 | -5966.188480850000 | -3743839.79577951 | +1149.20422049 | 1149.20422049 |
| B3LYP T | H_freq | -3744989.0 | -5966.187536640000 | -3743839.20327879 | +1149.79672121 | 1149.79672121 |
| B3LYP T | G_freq | -3744989.0 | -5966.374144450000 | -3743956.30144750 | +1032.69855250 | 1032.69855250 |
| B3LYP T | E_stable_plus_ZPE | -3744989.0 | -5966.270872713608 | -3743891.49745451 | +1097.50254549 | 1097.50254549 |
| B3LYP T | E_stable_plus_H_minus_Efreq | -3744989.0 | -5966.187536683608 | -3743839.20330615 | +1149.79669385 | 1149.79669385 |
| B3LYP T | E_stable_plus_G_minus_Efreq | -3744989.0 | -5966.374144493608 | -3743956.30147486 | +1032.69852514 | 1032.69852514 |
| BP86 CS | E_freq | -3746796.2 | -5970.498209470000 | -3746544.19131920 | +252.00868080 | 252.00868080 |
| BP86 CS | E_stable | -3746796.2 | -5970.498209475372 | -3746544.19132257 | +252.00867743 | 252.00867743 |
| BP86 CS | E_plus_ZPE_freq | -3746796.2 | -5969.197265620000 | -3745727.83672810 | +1068.36327190 | 1068.36327190 |
| BP86 CS | U_freq | -3746796.2 | -5969.112618570000 | -3745674.71990227 | +1121.48009773 | 1121.48009773 |
| BP86 CS | H_freq | -3746796.2 | -5969.111674360000 | -3745674.12740155 | +1122.07259845 | 1122.07259845 |
| BP86 CS | G_freq | -3746796.2 | -5969.301566090000 | -3745793.28626118 | +1002.91373882 | 1002.91373882 |
| BP86 CS | E_stable_plus_ZPE | -3746796.2 | -5969.197265625372 | -3745727.83673147 | +1068.36326853 | 1068.36326853 |
| BP86 CS | E_stable_plus_H_minus_Efreq | -3746796.2 | -5969.111674365372 | -3745674.12740492 | +1122.07259508 | 1122.07259508 |
| BP86 CS | E_stable_plus_G_minus_Efreq | -3746796.2 | -5969.301566095372 | -3745793.28626455 | +1002.91373545 | 1002.91373545 |
| BP86 T | E_freq | -3746771.1 | -5970.454918120000 | -3746517.02558693 | +254.07441307 | 254.07441307 |
| BP86 T | E_stable | -3746771.1 | -5970.454918122741 | -3746517.02558865 | +254.07441135 | 254.07441135 |
| BP86 T | E_plus_ZPE_freq | -3746771.1 | -5969.156987170000 | -3745702.56161913 | +1068.53838087 | 1068.53838087 |
| BP86 T | U_freq | -3746771.1 | -5969.072019670000 | -3745649.24370789 | +1121.85629211 | 1121.85629211 |
| BP86 T | H_freq | -3746771.1 | -5969.071075460000 | -3745648.65120717 | +1122.44879283 | 1122.44879283 |
| BP86 T | G_freq | -3746771.1 | -5969.262481410000 | -3745768.76025418 | +1002.33974582 | 1002.33974582 |
| BP86 T | E_stable_plus_ZPE | -3746771.1 | -5969.156987172741 | -3745702.56162085 | +1068.53837915 | 1068.53837915 |
| BP86 T | E_stable_plus_H_minus_Efreq | -3746771.1 | -5969.071075462741 | -3745648.65120889 | +1122.44879111 | 1122.44879111 |
| BP86 T | E_stable_plus_G_minus_Efreq | -3746771.1 | -5969.262481412741 | -3745768.76025590 | +1002.33974410 | 1002.33974410 |

| T−CS | Definition | Source kcal/mol | Native kcal/mol | Signed residual | Absolute residual |
| --- | --- | --- | --- | --- | --- |
| B3LYP | E_freq | 31.4 | 32.2199006522 | +0.8199006522 | 0.8199006522 |
| B3LYP | E_stable | 31.4 | 32.2179278365 | +0.8179278365 | 0.8179278365 |
| B3LYP | E_plus_ZPE_freq | 31.4 | 29.9118204051 | -1.4881795949 | 1.4881795949 |
| B3LYP | U_freq | 31.4 | 30.1077288629 | -1.2922711371 | 1.2922711371 |
| B3LYP | H_freq | 31.4 | 30.1077288629 | -1.2922711371 | 1.2922711371 |
| B3LYP | G_freq | 31.4 | 29.2431902352 | -2.1568097648 | 2.1568097648 |
| B3LYP | E_stable_plus_ZPE | 31.4 | 29.9098475894 | -1.4901524106 | 1.4901524106 |
| B3LYP | E_stable_plus_H_minus_Efreq | 31.4 | 30.1057560472 | -1.2942439528 | 1.2942439528 |
| B3LYP | E_stable_plus_G_minus_Efreq | 31.4 | 29.2412174195 | -2.1587825805 | 2.1587825805 |
| BP86 | E_freq | 25.1 | 27.1657322700 | +2.0657322700 | 2.0657322700 |
| BP86 | E_stable | 25.1 | 27.1657339210 | +2.0657339210 | 2.0657339210 |
| BP86 | E_plus_ZPE_freq | 25.1 | 25.2751089756 | +0.1751089756 | 0.1751089756 |
| BP86 | U_freq | 25.1 | 25.4761943865 | +0.3761943865 | 0.3761943865 |
| BP86 | H_freq | 25.1 | 25.4761943865 | +0.3761943865 | 0.3761943865 |
| BP86 | G_freq | 25.1 | 24.5260069907 | -0.5739930093 | 0.5739930093 |
| BP86 | E_stable_plus_ZPE | 25.1 | 25.2751106266 | +0.1751106266 | 0.1751106266 |
| BP86 | E_stable_plus_H_minus_Efreq | 25.1 | 25.4761960375 | +0.3761960375 | 0.3761960375 |
| BP86 | E_stable_plus_G_minus_Efreq | 25.1 | 24.5260086417 | -0.5739913583 | 0.5739913583 |

Both methods preserve the singlet-below-triplet ordering and the source statement that the gap exceeds 20 kcal/mol, but the electronic gaps remain 32.2199006522 versus 31.4 and 27.1657322700 versus 25.1 kcal/mol. The B3LYP stable-SCF gap is separately 32.2179278365; it is not silently substituted for the frequency-run electronic gap. The BP86 fixed-geometry grid control shifts the gap by only 0.00825314 kcal/mol, so it does not explain the 2.06573227 residual.

## Structure and orbital comparison

| State | Bond | Source Å | Native Å | Signed residual Å | Absolute residual Å |
| --- | --- | --- | --- | --- | --- |
| B3LYP CS | Ni-N atom 7 | 2.008 | 2.017650092 | +0.009650092 | 0.009650092 |
| B3LYP CS | Ni-N atom 9 | 2.01 | 2.017669465 | +0.007669465 | 0.007669465 |
| B3LYP CS | Ni-C atom 49 | 1.929 | 1.931516511 | +0.002516511 | 0.002516511 |
| B3LYP CS | Ni-C atom 59 | 1.93 | 1.931557912 | +0.001557912 | 0.001557912 |
| B3LYP CS | Ni-Cl atom 5 | 2.226 | 2.238346514 | +0.012346514 | 0.012346514 |
| B3LYP CS | Ni-Cl atom 3 | 2.227 | 2.238347312 | +0.011347312 | 0.011347312 |
| B3LYP T | Ni-N atom 7 | 1.99 | 1.999281595 | +0.009281595 | 0.009281595 |
| B3LYP T | Ni-N atom 9 | 1.992 | 1.999305322 | +0.007305322 | 0.007305322 |
| B3LYP T | Ni-C atom 59 | 1.926 | 1.928341759 | +0.002341759 | 0.002341759 |
| B3LYP T | Ni-C atom 49 | 1.927 | 1.928488499 | +0.001488499 | 0.001488499 |
| B3LYP T | Ni-Cl atom 3 | 2.23 | 2.242938657 | +0.012938657 | 0.012938657 |
| B3LYP T | Ni-Cl atom 5 | 2.23 | 2.242939828 | +0.012939828 | 0.012939828 |
| BP86 CS | Ni-N atom 9 | 1.999 | 2.008524432 | +0.009524432 | 0.009524432 |
| BP86 CS | Ni-N atom 7 | 2.0 | 2.008545794 | +0.008545794 | 0.008545794 |
| BP86 CS | Ni-C atom 59 | 1.933 | 1.935467679 | +0.002467679 | 0.002467679 |
| BP86 CS | Ni-C atom 49 | 1.934 | 1.935474688 | +0.001474688 | 0.001474688 |
| BP86 CS | Ni-Cl atom 3 | 2.223 | 2.236092652 | +0.013092652 | 0.013092652 |
| BP86 CS | Ni-Cl atom 5 | 2.223 | 2.236103936 | +0.013103936 | 0.013103936 |
| BP86 T | Ni-N atom 9 | 1.989 | 1.999180634 | +0.010180634 | 0.010180634 |
| BP86 T | Ni-N atom 7 | 1.992 | 1.999379794 | +0.007379794 | 0.007379794 |
| BP86 T | Ni-C atom 59 | 1.927 | 1.930739403 | +0.003739403 | 0.003739403 |
| BP86 T | Ni-C atom 49 | 1.93 | 1.931106249 | +0.001106249 | 0.001106249 |
| BP86 T | Ni-Cl atom 5 | 2.226 | 2.238842585 | +0.012842585 | 0.012842585 |
| BP86 T | Ni-Cl atom 3 | 2.227 | 2.240481018 | +0.013481018 | 0.013481018 |

Equivalent same-element pairs are sorted rather than asserted to retain arbitrary source atom labels. BP86 CS coordination RMS deviation from crystal is smaller than B3LYP CS, consistent with the source. Both axial and equatorial frontier sigma-star channels contain metal and ligand contributions.

| Method | Orbital channel | Native population | Source Ni% | Native Ni atom% | Signed difference pp | Absolute difference pp |
| --- | --- | --- | --- | --- | --- | --- |
| B3LYP | axial_sigma_star | MULLIKEN | 41.7 | 39.5 | -2.20 | 2.20 |
| B3LYP | axial_sigma_star | LOEWDIN | 41.7 | 43.6 | +1.90 | 1.90 |
| B3LYP | equatorial_sigma_star | MULLIKEN | 45.0 | 43.2 | -1.80 | 1.80 |
| B3LYP | equatorial_sigma_star | LOEWDIN | 45.0 | 47.0 | +2.00 | 2.00 |
| BP86 | axial_sigma_star | MULLIKEN | 41.7 | 37.8 | -3.90 | 3.90 |
| BP86 | axial_sigma_star | LOEWDIN | 41.7 | 41.6 | -0.10 | 0.10 |
| BP86 | equatorial_sigma_star | MULLIKEN | 45.0 | 41.7 | -3.30 | 3.30 |
| BP86 | equatorial_sigma_star | LOEWDIN | 45.0 | 45.2 | +0.20 | 0.20 |

Source Fig5 does not uniquely identify population convention or atom-total versus d-only character. Both native conventions and d-only components are retained in the linked comparison; no percentage renormalization or nearest-number selection was made. This supports mixing, not a unique physical oxidation state.

## Recorded resources and runtime

| Run | Native elapsed runtime |
| --- | --- |
| B3LYP CS | 0 days 12 hours 47 minutes 48 seconds 860 msec |
| B3LYP T | 1 days 7 hours 26 minutes 19 seconds 754 msec |
| BP86 CS | 0 days 12 hours 6 minutes 6 seconds 248 msec |
| BP86 T | 1 days 2 hours 27 minutes 29 seconds 938 msec |

These are per-parent native runtimes, not total project wall time. The thermal parser repair took 2.5613795444 s with zero quantum calls. Complete cumulative CPU/GPU allocation, queue time, cost and memory peak were not recorded in this reference and are not inferred. Raw input/output filenames and hashes follow.

## Remaining limits

- SI Energy is not unambiguously E, E+ZPE, H or G; all absolute offsets and every definition remain visible. No exact numerical equivalence or original tolerance pass is asserted.
- Source does not provide four independently identified same-level state geometries or a uniquely specified orbital-population convention. Method/version differences are not demonstrated to explain all residuals.
- Finite state searches establish the tested collapse and singlet/triplet ordering; they do not prove uniqueness across all electronic methods. No water-reaction, spectroscopy-complete, or universal sigma-noninnocence claim is accepted.

## Auditable raw/source artifact inventory

| Artifact | SHA-256 |
| --- | --- |
| papers/paper_72822e4ddb5d9b11/documents/supplementary_001.pdf | 9a3e4f4ed9c562f45721aeab487b6df25be409086c6221fad642551526106ac1 |
| docs/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_72822e4ddb5d9b11/native_evidence.json | 4d9340eb217c76c4499a58cfd44bd5842a8476a5405009e6c54a67cebc4176e5 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/strict_Ni_source_component_parser_repair/attempt_01/Ni_source_component_audit.json | 4f50375b4197e584ef6d3f33e010a35e27c4bc6f878a22aa028113d34fa2886b |
| docs/upgrade_tasks_verification/group_6/papers/paper_d3b4575397179146/outputs/reopen_source_definition_impact_batch/attempt_01/Ni_definition_impact.json | 3c7a1a34b12cc26656549fedf25f9100d044e6bcadc294d8cf1026d09edf0274 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_CS_legacy_gradient/attempt_01/orca_stdout.log | b5da693ee92c35563c866941aee10f0b20d503c27fac47d3bd175206bb39791d |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_CS_legacy_gradient/attempt_01/input.inp | cc5ff90b5988cd75e84880b5395ed65a5c5a43bbfd774c6d36b2f6b4549ec645 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_CS_legacy_gradient/attempt_01/input.engrad | bcece3d54318d21d3b701e950956c6fd529a034098586efa991d02fe223644a1 |
| runs/hold_verification/group_5/complex4_endpoint_20260919/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_singlet_torsion_minimum_hessian_20260919/20260919T080601_476816_187/input.hess | 5681c5f8db2a23a88731a04d4d752b3ece5c21ba1907d378f5ed0efa54416b02 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_CS_stability/attempt_01/orca_stdout.log | 2f36fa4addbbe21fe4232bc64586d94cbdd26943a16e2d5ab2f924dbb313c87b |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_CS_stability/attempt_01/input.inp | 2c21d0bcd403cd4043a03a13560751f701c53f4e95bb02f977f250d4f197b603 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_T_legacy_gradient/attempt_01/orca_stdout.log | fc309ba5f00c572eb246bb6e1a0ca2d08aed1ccf63ed612755a30ec1e33f9e32 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_T_legacy_gradient/attempt_01/input.inp | c168bc6dd18f9f1cfcb8d60368511692bf050d9382e7cb4954b0f634a62118b7 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_T_legacy_gradient/attempt_01/input.engrad | 62a81833334d4067b22935410a73534279bd0825a022abf3976f1d01095626f5 |
| runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_triplet_matched_grid_stationarity_20260921/20260921T065101_137993_188/input.hess | 4e7709d158916cbe8d93d7d193b6b8916d647a93287b8d5ad238707d89423c9c |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_T_legacy_stability/attempt_01/orca_stdout.log | 707320510b85bfb00f2f83d8f4d7c0997fa8c90d5f1456a24288eccdc85512b5 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/B3LYP_T_legacy_stability/attempt_01/input.inp | 8e6f981ac62263192440005f262c7c26262237ca6f83a8360c1ebf8625015413 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_CS_free_optfreq/attempt_01/orca_stdout.log | de3855e5c5092da83419791ddace3037bd0fe2005d51d77b05e513eda753e9c0 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_CS_free_optfreq/attempt_01/input.inp | 1bfc0f696d92aa3dedf42b4dd9748f53cb537fb9916d72bf196cf67dd71dd286 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_CS_free_optfreq/attempt_01/input.engrad | 3746d11b4a32e74bdaf9df5ed9bfc631cde20b1f6dab14a153ee954b0d3cd6a1 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_CS_free_optfreq/attempt_01/input.hess | e7713dbb1e8a8248def6a9d7c5b7289d1de267677fd0600ea109a5c66c878d50 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_CS_relaxed_stability/attempt_01/orca_stdout.log | d98cb3f06b8734781854147ce262446023e879e8c5409d3621781b147f38662d |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_CS_relaxed_stability/attempt_01/input.inp | 991a82826832d2e5fdc1d596f678f5b88a591a579afb196112557b1daf96051c |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_T_free_optfreq/attempt_01/orca_stdout.log | e7a84ae62431a0fe1d2b0a220f393c9daaaa37ea2ca016076161573c9ac53ffa |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_T_free_optfreq/attempt_01/input.inp | 31506e80ed4c84db7112403aebe8e6f6993227bddffb7c991fece79b990a435d |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_T_free_optfreq/attempt_01/input.engrad | 9ac946d62e8d966c38b641b044c2480cee6bcde08e913fc033f04437782b5094 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/BP86_T_free_optfreq/attempt_01/input.hess | 5258fab12679e741418a4480ffe7f55a38fd9c6ccead91ae8f7503179a35f0b3 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/v2_BP86_T_relaxed_stability/attempt_01/orca_stdout.log | 05d3c11975f4dfcffa6408c267345104947e128654b5d26e73aa574f47d3e056 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/v2_BP86_T_relaxed_stability/attempt_01/input.inp | 289c475ab587dbfed67c6aa763df07b284e15e2282890982979071125af29b6c |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/quota_resume_Ni_TableS1_bond_source_comparison/attempt_01/Ni_TableS1_bond_comparison.json | d8ba25318b14f74afc6f58ebfda7d345bdf7e10d714346f609ca39eba13b000e |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/resume5_Ni_grid_checkpoint_name_fix/attempt_01/CS/orca_stdout.log | 38eeacff0c84e37f9b75999b1ddc6dfee0c10d62b4a20da0e893451effed448b |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/resume5_Ni_grid_checkpoint_name_fix/attempt_01/T/orca_stdout.log | 7f9133ae227d213387783a60e15ef6260643cc54913857ffe0c87c7895f71d3c |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/resume5_Ni_grid_checkpoint_name_fix/attempt_01/Ni_BP86_grid_definition_control.json | ffe1bcda1c74ae464438981c64411fb9bb9d94bbfe787555cb897800c0126404 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/author_route_Ni_D3_completed_native_collection/attempt_01/Ni_dispersion_diagnostic.json | 7097ec0d1989067949392c2efbf9761ab6703a76c55ec4604872376065c4570f |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/thermal_definition_repair/attempt_001/THERMAL_DEFINITION_RESULTS.json | dc8087fb94ced51a143efde05b66dae9e804fc6cc5765d0ae53390b5480187fc |
| runs/hold_verification/group_5/complex4_endpoint_20260919/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_singlet_torsion_minimum_hessian_20260919/20260919T080601_476816_187/orca_stdout.log | e14faa66c57818d8fddb8f5ff8cd0615966512748198b577ca196623a1052be5 |
| runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_triplet_matched_grid_stationarity_20260921/20260921T065101_137993_188/orca_stdout.log | d270b5d20f54bd412867aa45c7bf96b4eacb47f9950c69edc30b17072f775005 |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/author_route_Ni_energy_reference_diagnostic/attempt_01/Ni_energy_reference_diagnostic.json | 2872b1e713e793ab3f69f0f089b68283fac0769a53aafd5b38b98fe4780bac04 |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/RAW_THERMAL_FIELD_PREFLIGHT.json | b4d4760732c30f5d5a4597ec4717f4aa6e1b3d435a2de540eba8140af2ee5a3d |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/FINITE_REPAIR_PLAN.json | e51810c66428ef2ef39f05763428c0e3978306e7d03952d3b0b59312b9f6cf33 |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/thermal_definition_repair/attempt_001/input.json | e51810c66428ef2ef39f05763428c0e3978306e7d03952d3b0b59312b9f6cf33 |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/thermal_definition_repair/attempt_001/submission.json | f5c144aa3d48f027c7ed395537f80e1be7612163f8d93570ce5a4ad1aaed009c |
| docs/verification_forward_20261014T1430Z/deliveries/W04_NI_INTAKE.json | a8ec1c7b2251e6409a2cf74c53cd4bcf8fb0665fb7a1725899066a3fc529a829 |
| papers/paper_72822e4ddb5d9b11/documents/main.pdf | 69805929b078375456ecab8ac4c7dcc9f466b143f34fe8a29b9749bfefc6a7bb |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_72822e4ddb5d9b11/mo_population_checkpoint/attempt_001/B3LYP/stdout.log | 77480a017c57054ecf2b51332f62292594c2c9b25b1d0e728a623fc5d5b9c21d |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_72822e4ddb5d9b11/mo_population_checkpoint/attempt_001/BP86/stdout.log | 3f3be44aae603829995c9a538b5d1746fd83e04c34b0fe834454726bcaf39ca0 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_72822e4ddb5d9b11/mo_comparison/attempt_001/NI_MO_COMPARISON_RESULTS.json | 1f7c8c501d34abd5401817929f66fa14f19a8411769a2ac43f516a2ea21b56a3 |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/FROZEN_CONTRACT_HASHES.json | 81da045c949ba2ce0698c0021b4130ab464211be4ad4515e054297e3712ddefa |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/source/SOURCE_PAGES.json | 2eb14e8e37a540b5abca699beecc92235c896cf1d5ebf2a3d7530dc409f22f9e |
| docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/outputs/author_route_Ni_energy_reference_diagnostic/attempt_01/analysis.py | e577c9bb4763e7e404eac14021476bba0d02ae0cbde7b1b234e9dbb13028c491 |
| runs/hold_verification/group_5/torsion_restart_20260918/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_methyl_torsion20_minus_orbital_resume_20260918/20260918T095757_594190_343/orca_stdout.log | d52a71e66cc51b63ba412117967bd02ae045d5ffce01b2d76d2587523e9f4d97 |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/SOURCE_ROUTE_MATRIX.json | c0599ca1746da56d85c31110a9a50240e462e500e689cae9f165562f12a6e882 |
| docs/v2_verification/history/v2_reopened_verification_20261014/papers/paper_72822e4ddb5d9b11/thermal_definition_repair/attempt_001/THERMAL_DEFINITION_RESULTS.json | dc8087fb94ced51a143efde05b66dae9e804fc6cc5765d0ae53390b5480187fc |

## Preserved earlier reference

No root-level verified_computation_reference.md existed in the source package. Historical evaluation snapshots are preserved byte-for-byte in the external archive indexed by evaluation/history_archive_index.json; source/native computation records remain at the artifact paths above.


## Historical reference text — non-current, preserved verbatim

Original location: legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot. Historical PASS/pending, numeric windows, search matrices and scoring prescriptions below are not the current scientific scoring policy.

# 已验证成功计算过程：paper_72822e4ddb5d9b11 / autonomous_research

归档日期：2026-09-26。入库时科学计算证据支持所选子目标；2026-09-26 维护修订及当前验收结论见第7节和本包 task_provenance/maintenance_audit.md。**已迁入 final；本档案不等于运行时隔离或 LLM judge 发布认证。**

## 1. 本档案的用途和证据范围

本文件保存已经实际完成的作者知情验证计算，供维护者追溯任务科学结果的可计算性。验证者可以使用论文路线、SI 坐标和结果辅助验证；这不要求与被评估 agent 的搜索轨迹相同，也不证明已经完成公开输入盲测。评分仍以本包 evaluation 的关键点、结论和规则为准，reference 不是新增评分轴或要求 agent 模仿的标准步骤。本文及其所有原始日志/论文链接仅供私有评估和维护使用，不得挂载进 agent_input。

- 来源分组：Group 5；[当前已验证索引](../../../../docs/verification/all_verified_tasks/group_5.md)
- [正文](../../../../papers/paper_72822e4ddb5d9b11/documents/main.pdf)；[补充材料](../../../../papers/paper_72822e4ddb5d9b11/documents/supplementary_001.pdf)
- [实算核查记录](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/report/closure_audit.json)；[历史结构化结果](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/report/results.json)
- 当前规范：[该模式 task.md](../../../../tasks/final_verified_autonomous_research/paper_72822e4ddb5d9b11/agent_input/task.md)；[submission_schema](../../../../tasks/final_verified_autonomous_research/paper_72822e4ddb5d9b11/agent_input/submission_schema.json)

## 2. 研究对象、来源与实际方法

固定 complex4、165原子、中性，比较singlet/triplet两个自旋态。SI pp10–11规定几何优化和电子结构用ORCA、B3LYP/BP86、Ni及第一配位层Cl1/Cl2/N1/N2/C1/C2用def2-TZVP，其余def2-SVP；本链采用允许的B3LYP分支，不冒充BP86。源坐标见SI pp99–100。

真实 ORCA6.1.1、B3LYP、DEFGRID3、VeryTightSCF；TZVP原子索引为1、3、5、7、9、49、59（1-based，按实际输入）。主比较为电子能差，不是G或TDDFT/SMD甲苯子题；不把论文其他方法直接混入这一子任务。

## 3. 成功计算链与结果

正确SI原子身份（早期无效元素0已按O修复） → singlet甲基扭转后独立优化得到真实最低点 → 同一几何Hessian → triplet用相同网格/基组Opt+Hessian → 同原子图、配位第一层及状态核对 → 同方法电子能差。

singlet优化日志与其后独立Hessian是两个文件，不能因为Hessian日志没有Opt步骤而误判“未优化”。两个最终Hessian各495模，含6个整体零模，其余全正，最低有效振动为8.698285/9.178230 cm⁻¹。triplet `<S²>=2.063319`，如实保留；singlet为闭壳层。

| 状态 | 用于比较的 E，Eh |
|---|---:|
| singlet（最终Hessian点） | −5967.657038894920 |
| triplet | −5967.605693210459 |

`(Etriplet−Esinglet)×627.5094740631 = +32.219903 kcal/mol`，singlet明显更低。SI TableS1 的B3LYP由表内能量差得31.4，BP86为25.1；本次不是精确复现31.4，更不能称为复现25.1。正文支持triplet高于20，当前evaluator要求正gap及singlet最低，实算满足。

成功singlet优化34335.324s、独立Hessian46070.673s、tripletOpt/Hessian113182.348s，共约53.7745h elapsed之和，不代表并行日历时长。早期带负频的结构未作为最低点，也不是简单删掉负频；后续有效几何和Hessian替代该分支，历史日志仍保存。

### 原始有效计算步骤与输出

下表逐行链接真实输入和输出。E/G 为该原生日志的电子能/低层或本层 Gibbs 能，**不得把低层 G 与高层电子能混淆**；主结果以§3写明的组合公式为准。“0模”仅表示该步骤不是频率任务，不能自动解释为最低点。失败日志中的已接受路径前缀不使用失败尾部能量。

| 步骤 | 输入 / 原始输出 | E / G，Eh | 最终模式/数值验证 |
|---|---|---|---|
| singlet_state optimization | [输入](../../../../runs/hold_verification/group_5/torsion_restart_20260918/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_methyl_torsion20_minus_orbital_resume_20260918/20260918T095757_594190_343/input.inp) / [输出](../../../../runs/hold_verification/group_5/torsion_restart_20260918/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_methyl_torsion20_minus_orbital_resume_20260918/20260918T095757_594190_343/orca_stdout.log) | -5967.657035602952 / — | 无该步频率分析；按其单点/路径/稳定性角色使用；日志正常结束 |
| singlet_state Hessian | [输入](../../../../runs/hold_verification/group_5/complex4_endpoint_20260919/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_singlet_torsion_minimum_hessian_20260919/20260919T080601_476816_187/input.inp) / [输出](../../../../runs/hold_verification/group_5/complex4_endpoint_20260919/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_singlet_torsion_minimum_hessian_20260919/20260919T080601_476816_187/orca_stdout.log) | -5967.65703889492 / -5966.42074644 | 495 模；负模 无；最低正频 8.7 cm⁻¹；日志正常结束 |
| triplet_state optimization | [输入](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_triplet_matched_grid_stationarity_20260921/20260921T065101_137993_188/input.inp) / [输出](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/provenance/qzcli_hpc/complex4_triplet_matched_grid_stationarity_20260921/20260921T065101_137993_188/orca_stdout.log) | -5967.605693210459 / -5966.37414445 | 495 模；负模 无；最低正频 9.18 cm⁻¹；日志正常结束 |

### 输入参数与步骤关联

下列为对应输入的实际 route/ORCA方法行；完整电荷、多重度、坐标、基组/ECP、checkpoint 和约束指令以所链接的输入为准。采用 checkpoint 的成功续算保留原始继承路径，不要求 agent 取得维护者的 checkpoint。

- `singlet_state optimization`：`! B3LYP def2-SVP VeryTightSCF DEFGRID3 VeryTightOpt MOREAD`。
- `singlet_state Hessian`：`! B3LYP def2-SVP VeryTightSCF DEFGRID3 Freq MOREAD`。
- `triplet_state optimization`：`! B3LYP def2-SVP VeryTightSCF DEFGRID3 TightOpt Freq MOREAD`。

## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）

这是对原始输出和现有规则的科学适用性审查；本轮未调用付费 LLM judge、未生成或宣称完整自动评分。数值规则沿用现有参考与容差；语义规则以下述可追溯证据作人工核对。

| 类型 / ID | 当前要求 | 实际证据与范围 |
|---|---|---|
| 关键点 `kp_process_states` | Neutral complex 4 is compared in multiplicities 1 and 3 with consistent energies and state-specific convergence and stationarity evidence. | 165原子中性1/3两态，同网格及混合基组，优化与Hessian关联；495模无负频。 |
| 关键点 `kp_result_gap` | The triplet is substantially higher in energy than the closed-shell singlet. | Etriplet−Esinglet=+32.219903 kcal/mol，满足正gap与singlet更低，不新增数字硬靶。 |
| 结论 `c_final_ground_state` | Validated state ordering supports a closed-shell singlet ground-state interpretation for complex 4. | 指定两态比较支持闭壳层singlet解释，且量级与正文>20/B3LYP31.4一致。 |

| 评分规则 | 绑定字段 / 原标准 | 对应证据 |
|---|---|---|
| `r_process` | `$.states.singlet_state, $.states.triplet_state`；Named singlet/triplet calculations, consistent comparison, convergence and state-specific stationarity evidence are present. | `kp_process_states`：165原子中性1/3两态，同网格及混合基组，优化与Hessian关联；495模无负频。 |
| `r_gap` | `$.status, $.conclusion.claim, $.conclusion.limitations`；Completed output has singlet lower and positive gap; bounded failure has no fabricated gap and a specific limitation. | `kp_result_gap`：Etriplet−Esinglet=+32.219903 kcal/mol，满足正gap与singlet更低，不新增数字硬靶。 |
| `r_final` | `$.conclusion.claim, $.conclusion.validation_summary, $.conclusion.limitations`；Final conclusion connects validated ordering to the singlet interpretation and states limitations. | `c_final_ground_state`：指定两态比较支持闭壳层singlet解释，且量级与正文>20/B3LYP31.4一致。 |

## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）

两模式的指定自旋态比较和最终结论可计算。没有把该子问题扩展为其他化合物、所有自旋态的全局搜索、NICS/ACID或TDDFT。当前正gap标准不应被误写成新增的32.219903硬目标。

发布整理仍需单独检查作者优化结构作为固定物性对象输入的边界；本轮是保存既有源任务和证据，不宣称完成无泄漏发布审计，也不改动公开几何或评分。

本轮仅复制源包、新增本档案并刷新文件清单；没有改写公开任务、输入、五个 evaluator 文件或历史计算。来源辅助验证有效与公开输入是否适合发布是两项不同检查，本文件不替代完整泄漏/措辞/打包隔离审计。

## 6. 补充证据索引

- [supplementary_verification.md](../../../../runs/hold_verification/group_5/complex4_closure_20260921/paper_72822e4ddb5d9b11/report/supplementary_verification.md)

## 7. 2026-09-26 修订后的科学对应与验证适用范围

SI pp10–11两态分别优化/频率及分层基组、正文p4，SI复合物4坐标pp99–100。

实际修复：保留给定复合物的两态性质比较；明确分别弛豫后的电子Et−Es而非垂直或G能差；完成必须有两电子能/gap/lower_state，评分绑定实际数值与证据，不按免责声明给分。

验证适用性：不将B3LYP32.22声称为BP8625.1逐值复现；现行只评分方向，不新增数值容差或额外电子态搜索。

原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。

| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |
|---|---|---|
| `kp_process_states` | Both named states have explicit multiplicities, methods, relaxed electronic energies, convergence and stationarity evidence. Credit only states actually established; a failure explanation cannot replace missing state evidence. | ORCA3份有效日志覆盖singlet Opt+Freq及triplet OptFreq。两态无负模，Et−Es=+32.219903 kcal/mol，支持闭壳层singlet较低。 |
| `kp_result_gap` | Completed output identifies singlet as lower with a positive gap; bounded failure does not fabricate a gap. | ORCA3份有效日志覆盖singlet Opt+Freq及triplet OptFreq。两态无负模，Et−Es=+32.219903 kcal/mol，支持闭壳层singlet较低。 |
| `c_final_ground_state` | Traceable relaxed-state electronic energies give a positive Et−Es gap and lower closed-shell singlet in this two-state comparison. | ORCA3份有效日志覆盖singlet Opt+Freq及triplet OptFreq。两态无负模，Et−Es=+32.219903 kcal/mol，支持闭壳层singlet较低。 |

当前规则绑定（不改变原数值靶和容差）：

- `r_process` → `kp_process_states`；读取 `$.states.singlet_state, $.states.triplet_state`。
- `r_gap` → `kp_result_gap`；读取 `$.status, $.states, $.gap_kcal_mol, $.lower_state, $.conclusion.claim`。
- `r_final` → `c_final_ground_state`；读取 `$.conclusion.claim, $.states, $.gap_kcal_mol, $.lower_state`。
