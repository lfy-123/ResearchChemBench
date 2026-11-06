# V3 final-results scope and evidence reuse — 2026-10-28

Historical acceptance is ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION, not strict numerical reproduction. Existing six full-molecule computations give ring J (6a/6e/7a/7e/13a/13e) = -281.688/-331.176/-341.991/-412.557/-241.899/-185.191 Hz, with source absolute deviations 11.798/14.436/14.091/18.867/10.449/7.831 Hz. Mean butyl J = -210.0663/-233.6200/-204.1950/-240.8400/-238.0103/-229.7047 Hz. FC dominates each axial-minus-equatorial contrast but non-FC contributions remain. Correct 7a C–Sn donation is 6.56+6.34=12.90 kcal/mol, not the source 20.5; 10.29+10.22=20.51 belongs to C–O and cannot be relabeled. Main Table2 and SI descriptor entries conflict. The native response is nonrelativistic despite TZP-ZORA basis naming. No empirical -1.419 fit is used to force agreement. The recovered 6a Hessian supports the reused geometry, not a new full optimization.

- `r_ring_6`: SI S5–S6 → `docs/strict_author_route_validation_20261001/all_unfinished36_20261011T0650Z/papers/paper_a21b91f97ce3c68f/SOURCE_COMPARISON.json` six_ring_components；ax/eq=-281.688/-331.176 Hz；赤道绝对值更大。
- `r_butyl_6`: SI S5–S6 → 同SOURCE_COMPARISON的三个丁基映射及butyl_average_components_Hz；ax/eq=-210.0663/-233.6200 Hz，已覆盖。
- `r_response_6`: 正文FC讨论及原生spinspin输出 → 同SOURCE_COMPARISON，ΔJax−eq=49.488、ΔFC=47.523、非FC合计=1.965 Hz；FC主导但不等于总J。
- `r_ring_7`: SI S5–S6 → `docs/strict_author_route_validation_20261001/all_unfinished36_20261011T0650Z/papers/paper_a21b91f97ce3c68f/SOURCE_COMPARISON.json` six_ring_components；ax/eq=-341.991/-412.557 Hz；赤道绝对值更大。
- `r_butyl_7`: SI S5–S6 → 同SOURCE_COMPARISON的三个丁基映射及butyl_average_components_Hz；ax/eq=-204.195/-240.840 Hz，已覆盖。
- `r_response_7`: 正文FC讨论及原生spinspin输出 → 同SOURCE_COMPARISON，ΔJax−eq=70.566、ΔFC=64.183、非FC合计=6.383 Hz；FC主导但不等于总J。
- `r_ring_13`: SI S5–S6 → `docs/strict_author_route_validation_20261001/all_unfinished36_20261011T0650Z/papers/paper_a21b91f97ce3c68f/SOURCE_COMPARISON.json` six_ring_components；ax/eq=-241.899/-185.191 Hz；轴向绝对值更大。
- `r_butyl_13`: SI S5–S6 → 同SOURCE_COMPARISON的三个丁基映射及butyl_average_components_Hz；ax/eq=-238.0103/-229.7047 Hz，已覆盖。
- `r_response_13`: 正文FC讨论及原生spinspin输出 → 同SOURCE_COMPARISON，ΔJax−eq=-56.708、ΔFC=-53.869、非FC合计=-2.839 Hz；FC主导但不等于总J。
- `r_cross_scaffold_account`: 正文PDF4–7、SI S5–S6 → SOURCE_COMPARISON的真实C–Sn受体NBO：6a/e11.27/4.42，7a/e12.90/3.83，13a/e7.64/5.19 kcal/mol；三对轴向供电子更强，但13总J方向反转，排除普适单因果。

This update performs no new scientific calculation or validation. Historical PASS labels below are not a new V3 overall pass. The active rubric is `paper_science_v3` / `final_results_100`; all preceding versions and numerical conflicts remain archival evidence.

---

# Current computational verification and scoring reference — 2026-10-20

Acceptance: **ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**. The coordinator-approved scope has sufficient valid computations and matching key qualitative nodes/conclusions. Original strict numerical gates are not relabelled as passed. This acceptance does not assert exact historical inputs, whole-paper reproduction, blinded autonomous success or an online Judge score.

Current scoring: paper_science_v2, 100 fixed binary points, intermediate and final conclusions; formal_scoring_permitted=true. Publication/expert review remains separate and is not a runtime scoring freeze. The unchanged public PR contract continues to govern baseline reproduction or justified substitution, while AR chooses methods. Public legacy wording about process assessment is retained byte-for-byte but confers no process score.

## Scientific objects, conditions and completed verification

Complete neutral SnBu3 derivatives6/7/13, axial/equatorial forms; separately mapped ring and mean butyl total J, and an evidence-based cross-scaffold electronic interpretation.

六对象环/丁基耦合的构象方向及AP供受体强弱保持；6/7与13相反的关键趋势、FC主导而非唯一贡献，与任务限定的非因果结论一致。数值偏差和7a受体标签问题不隐去，但不推翻当前任务的配对定性结论。

Gaussian16 C.01；气相GD3-B3LYP/def2-TZVPP Opt/Freq/NBO3.1；B3LYP与TZP-ZORA命名基组的耦合响应。
完整六个中性单重态；NMR=(SpinSpin,Mixed,ReadAtoms)、Integral=NoXCTest；显式119Sn/13C，环Sn5–C14，丁基C4/C6/C10平均。TZP-ZORA基组名不意味着相对论哈密顿量；当前耦合为非相对论。
已披露关键理论层级、对象、同一定义响应相符；源文后段相对论措辞冲突保留，不冒充相对论计算。未应用−1.419经验缩放凑数。
网格、SCF/优化阈值等部分未完整披露，实际值已记录；不因此机械否决。

- 六个响应日志正常结束；五个Opt/Freq端点正频率。
- 6a早期Opt失败保留；既有几何新鲜Hessian正常结束，159正频率、min12.1348 cm−1，max/RMS力0.000003/0.000001 Eh/bohr、位移检查均YES。此为复用几何频率证明，不称另一次完整优化。

## Supported qualitative outcomes

- 6/7环及丁基的equatorial |J| > axial；13两个观测均反向。
- FC主导构象差值，但非FC非零。
- 三对AP NBO强弱均axial > equatorial；硫13的J反向保留，排除普适单因果解释。

## Retained conflicts and boundaries

- 7a实际LP2→C–Sn为6.56+6.34=12.90 kcal/mol；源SI20.5未数值复现。10.29+10.22=20.51属于C–O受体，禁止重标为C–Sn。
- 主文Table2与SI条目冲突，当前明确比较SI；不能宣称精确描述符回归或全部源标签正确。
- 接受限定对象配对方向，不扩展为普适有机锡规律或相对论结论。

Verification sequence: retain full source conformers and atom maps; inspect gas-phase geometry/frequency/NBO outputs; recover the valid6a NBO segment and new Hessian without calling it a new full optimization; inspect six isotope-resolved spin-spin response jobs; separately extract FC, SD, PSO, DSO, total J and mean over three butyl bonds; compare paired differences and acceptor-specific AP donor terms. Existing controls and failures are preserved, not rerun.


### All source versus actual total couplings

| object | source | actual | actual−source | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| 6a ring | -269.89 | -281.688 | -11.798 | 11.798 | Hz |
| 6a mean butyl | -200 | -210.0663333 | -10.06633333 | 10.06633333 | Hz |
| 6e ring | -316.74 | -331.176 | -14.436 | 14.436 | Hz |
| 6e mean butyl | -223 | -233.62 | -10.62 | 10.62 | Hz |
| 7a ring | -327.9 | -341.991 | -14.091 | 14.091 | Hz |
| 7a mean butyl | -194 | -204.195 | -10.195 | 10.195 | Hz |
| 7e ring | -393.69 | -412.557 | -18.867 | 18.867 | Hz |
| 7e mean butyl | -230 | -240.84 | -10.84 | 10.84 | Hz |
| 13a ring | -231.45 | -241.899 | -10.449 | 10.449 | Hz |
| 13a mean butyl | -227 | -238.0103333 | -11.01033333 | 11.01033333 | Hz |
| 13e ring | -177.36 | -185.191 | -7.831 | 7.831 | Hz |
| 13e mean butyl | -220 | -229.7046667 | -9.704666667 | 9.704666667 | Hz |


### Actual ring response components; same isotope and atom pair

| object | FC | SD | PSO | DSO | total J (Hz) |
| --- | --- | --- | --- | --- | --- |
| 6a | -269.824 | -19.6306 | 8.04503 | -0.278252 | -281.688 |
| 6e | -317.347 | -21.8774 | 8.33069 | -0.281603 | -331.176 |
| 7a | -329.957 | -17.8543 | 6.11983 | -0.298998 | -341.991 |
| 7e | -394.14 | -23.484 | 5.36373 | -0.297054 | -412.557 |
| 13a | -231.661 | -18.772 | 8.81286 | -0.278698 | -241.899 |
| 13e | -177.792 | -18.962 | 11.8337 | -0.271015 | -185.191 |


### Axial-minus-equatorial contrasts (Hz)

| scaffold | ring total | ring FC | ring non-FC total | butyl total |
| --- | --- | --- | --- | --- |
| 6 | 49.488 | 47.523 | 1.965 | 23.55366667 |
| 7 | 70.566 | 64.183 | 6.383 | 36.645 |
| 13 | -56.708 | -53.869 | -2.839 | -8.305666667 |


### AP donor interaction into correctly mapped C–Sn acceptor

| object | SI source | actual | actual−SI | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| 6a | 11.3 | 11.27 | -0.03 | 0.03 | kcal/mol |
| 6e | 4.4 | 4.42 | 0.02 | 0.02 | kcal/mol |
| 7a | 20.5 | 12.9 | -7.6 | 7.6 | kcal/mol |
| 7e | 3.8 | 3.83 | 0.03 | 0.03 | kcal/mol |
| 13a | 7.6 | 7.64 | 0.04 | 0.04 | kcal/mol |
| 13e | 5.2 | 5.19 | -0.01 | 0.01 | kcal/mol |


### Conflicting main-table entries retained, not silently repaired

| object | main E2 | SI E2 | actual C–Sn E2 |
| --- | --- | --- | --- |
| 6a | 4.5 | 11.3 | 11.27 |
| 6e | 10.7 | 4.4 | 4.42 |
| 7a | 10.7 | 20.5 | 12.9 |
| 7e | 4.5 | 3.8 | 3.83 |
| 13a | 20.5 | 7.6 | 7.64 |
| 13e | 3.8 | 5.2 | 5.19 |

Source SI S5–S6 is used to identify the six scaffold/conformer rows; main Table2 is inconsistent. For7a the correct C–Sn terms6.56+6.34=12.90 differ from20.5. The numerically tempting10.29+10.22=20.51 is C–O acceptor donation and is never substituted. Source SI labels “J” are not relabelled as FC merely because FC lies closer. The Hamiltonian is nonrelativistic despite the TZP-ZORA basis name; source later relativistic prose is retained as a conflict. No −1.419 empirical scaling is applied to force a match.


## Rule design and tolerance boundary

No numerical leaves. Absolute J offsets, source table conflicts and 7a acceptor mismatch preclude a defensible universal magnitude window; do not fit tolerances to current residuals. Qualitative pair contrasts and the supported electronic explanation remain independently testable.

Evidence eligibility is checked per item; no independent points for software, convergence logs, report completeness or generic limitations. Wrong physical identity invalidates the affected result even if a number hits a window. Final inference must be explicitly supported in the submitted deliverable.

## Source location and independent readback

- papers/paper_a21b91f97ce3c68f/documents/main.pdf; SHA256 637bc5dd2d5d03773819f3cf73524d6c4c2b3fc7cdd4ff6b077b811ed0ea452b; 1-based PDF pages 2,4,5,6,7; Hamiltonian paragraph, Table2 and stereoelectronic conclusions.
- papers/paper_a21b91f97ce3c68f/documents/supplementary_001.pdf; SHA256 35c7bfcbb36da658670c057ed2e6ecdc3ac6c3707c0bd122469234fae020d12b; 1-based PDF pages 2,5,6; Computational details and SI S5–S6 six conformer rows.

### Existing validation/analysis summaries (separate from primary sources)

- docs/strict_author_route_validation_20261001/all_unfinished36_20261011T0650Z/papers/paper_a21b91f97ce3c68f/SOURCE_COMPARISON.json; SHA256 bc54f7aeca411d12e4bd32f06894851f912f004a25e4e3ef82f5df1c6c733787. Historical status labels in these unchanged files are retained; current acceptance above supersedes them.
- docs/v2_verification/maintenance/qualitative_acceptance_review_20261020/INDEPENDENT_OTHER_NATIVE_SUPPLEMENT.json; SHA256 5f2ac9d3e1874077e3a9fbc7eda6c2020d36de0ae07dd915074a76fa73f6fea7. Historical status labels in these unchanged files are retained; current acceptance above supersedes them.

## Native artifact index, real resources and completeness

Paths below are workspace-relative on the shared server. They identify actual existing inputs/outputs; this migration only reads and hashes them. Normal termination alone does not establish the right molecule/state. Any errors or reused frequency-only recoveries remain in the index and are not erased. Resource lines are the individual logs’ recorded quantities; absent/all-job wall time and CPU cost are **not recorded as a reliable total** and are not inferred from allocations.

- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13a_source_optfreq_nbo_strict_v1_a01/input.com; SHA256 e8e3b7e59637c2800c1bcfbccaf1eae57d7a5eefa938ca79cacc508c1b70b4e8; 2512 bytes.
  input_route: ["#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 Opt=(Tight,CalcFC,MaxCycles=180) Freq Pop=NBO NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) 5D 7F"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13a_source_optfreq_nbo_strict_v1_a01/stdout.log; SHA256 f0d847cd220d6d03975b079f1e22982a44477e137f5dfe081cabd4cb6f62fb83; 2667853 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1641.30422103     A.U. after    3 cycles"]
  frequencies: {"count": 153, "minimum_cm1": 22.1846, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 17 hours 48 minutes 50.3 seconds.", "Elapsed time:       0 days  2 hours  6 minutes 37.6 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 09:08:27 2026.", "Job cpu time:       1 days 12 hours 34 minutes 14.5 seconds.", "Elapsed time:       0 days  1 hours 50 minutes 45.7 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 10:59:14 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13a_spinspin_element_repair_20261002_a01/input.com; SHA256 5e14d9c844d49776d25df4a2f72773db3781cd4261ca6131507ff15c4eaee5ba; 7166 bytes.
  input_route: ["#p B3LYP/Gen EmpiricalDispersion=GD3 NMR=(SpinSpin,Mixed,ReadAtoms) Integral=NoXCTest NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13a_spinspin_element_repair_20261002_a01/stdout.log; SHA256 af62056dd4c30a75853ac6c86aedbb4915da69efa9918ca41318f53003e68b58; 435826 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -7434.81367614     A.U. after   12 cycles"]
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 12 hours 38 minutes 41.0 seconds.", "Elapsed time:       0 days  1 hours 50 minutes 54.8 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 06:12:00 2026.", "Job cpu time:       0 days 17 hours 50 minutes 36.1 seconds.", "Elapsed time:       0 days  0 hours 55 minutes 18.8 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 07:07:19 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13e_source_optfreq_nbo_strict_v1_a01/input.com; SHA256 a5feab81ae73d13e517d113d29b626988e7412f06a974264f2ca00184d507999; 2502 bytes.
  input_route: ["#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 Opt=(Tight,CalcFC,MaxCycles=180) Freq Pop=NBO NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) 5D 7F"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13e_source_optfreq_nbo_strict_v1_a01/stdout.log; SHA256 48a353003bd4a06cfcb1dbc3bf42efcaef502a0931870511bffee57535902ec3; 2518098 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1641.30331893     A.U. after    1 cycles"]
  frequencies: {"count": 153, "minimum_cm1": 19.345, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 12 hours 36 minutes 34.3 seconds.", "Elapsed time:       0 days  1 hours 50 minutes 48.6 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 08:52:52 2026.", "Job cpu time:       1 days 11 hours 10 minutes 46.0 seconds.", "Elapsed time:       0 days  1 hours 46 minutes 31.0 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 10:39:25 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13e_spinspin_element_repair_20261002_freshstopresume_a01/input.com; SHA256 ddc781f9bfa6ab4271771755541a8c5a764f6e3de9280a98012b0c1e3c92f6c5; 7233 bytes.
  input_route: ["#p B3LYP/Gen EmpiricalDispersion=GD3 NMR=(SpinSpin,Mixed,ReadAtoms) Integral=NoXCTest NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn13e_spinspin_element_repair_20261002_freshstopresume_a01/stdout.log; SHA256 3ad0dea8fa7c473781ee963058602c428e385a2f58e8fc271beef1039de5bdc4; 436220 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -7434.81361378     A.U. after   12 cycles"]
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 11 hours 52 minutes 38.5 seconds.", "Elapsed time:       0 days  1 hours 48 minutes 25.3 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 08:56:07 2026.", "Job cpu time:       0 days 17 hours 40 minutes  5.3 seconds.", "Elapsed time:       0 days  0 hours 54 minutes 47.2 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 09:50:55 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6a_first_nbo_reuse_audit_v2_a02/first_completed_nbo_segment.txt; SHA256 b9a07e58eeaed969742e4a7d830df44f978af523b9ab4670bb8c68e354d20b8c; 568248 bytes.
  last_scf: []
  normal_termination_count: 0
  error_termination_count: 0
  reported_resources: []
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6a_recovery_initial_fresh_hessian_v2_a01/stdout.log; SHA256 fcd70868b34377ae5d7bf719fddb0fb42c1921dc72e17ea16058e89196083d37; 545081 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -959.433469024     A.U. after   12 cycles"]
  frequencies: {"count": 159, "minimum_cm1": 12.1348, "negative_count": 0}
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 15 hours 23 minutes  8.0 seconds.", "Elapsed time:       0 days  1 hours 59 minutes 14.7 seconds.", "Normal termination of Gaussian 16 at Wed Sep 30 10:34:37 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6a_source_spinspin_pause_v1_a01/input.com; SHA256 cdc5b775e8cf3ec790c3ff6a0908756eb4b5c601560127e1c67f3f70eff158ae; 6405 bytes.
  input_route: ["#p B3LYP/Gen EmpiricalDispersion=GD3 NMR=(SpinSpin,Mixed,ReadAtoms) Integral=NoXCTest NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6a_source_spinspin_pause_v1_a01/stdout.log; SHA256 08e3d25a8ea7d887f1588f2fb21980c1683b9adbe70913bf13761a8424905476; 460169 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -6752.94253252     A.U. after   12 cycles"]
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 18 hours 15 minutes 56.9 seconds.", "Elapsed time:       0 days  2 hours  7 minutes 42.9 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 10:57:00 2026.", "Job cpu time:       0 days 19 hours 12 minutes  6.1 seconds.", "Elapsed time:       0 days  0 hours 59 minutes 33.4 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 11:56:33 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6e_source_optfreq_nbo_strict_v1_a01/input.com; SHA256 4f27d7567796fe026c72695fb177aa7f5688b4c4fb0c184c491b38441dab9ff6; 2594 bytes.
  input_route: ["#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 Opt=(Tight,CalcFC,MaxCycles=180) Freq Pop=NBO NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) 5D 7F"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6e_source_optfreq_nbo_strict_v1_a01/stdout.log; SHA256 109390eb338ca2393df20a5bc16de0fc98ad45e88189adf0fe43c57a07b4f63d; 2633577 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -959.436359797     A.U. after    1 cycles"]
  frequencies: {"count": 159, "minimum_cm1": 17.6464, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 19 hours 59 minutes 41.3 seconds.", "Elapsed time:       0 days  2 hours 13 minutes 16.0 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 09:14:23 2026.", "Job cpu time:       1 days 13 hours 34 minutes 25.9 seconds.", "Elapsed time:       0 days  1 hours 53 minutes 48.1 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 11:08:12 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6e_spinspin_element_repair_20261002_freshstopresume_a01/input.com; SHA256 9ff5657c3a7692c8b1ac086210ea0fbaaa20b9e4d93d433b67072cfce1be8838; 6977 bytes.
  input_route: ["#p B3LYP/Gen EmpiricalDispersion=GD3 NMR=(SpinSpin,Mixed,ReadAtoms) Integral=NoXCTest NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn6e_spinspin_element_repair_20261002_freshstopresume_a01/stdout.log; SHA256 7b0de4c3247e52659c77d00803dcb8ab95185464e48fdc711b508a4ab634f81e; 458284 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -6752.94523152     A.U. after   12 cycles"]
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 14 hours 56 minutes  9.6 seconds.", "Elapsed time:       0 days  1 hours 57 minutes 49.6 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 09:04:27 2026.", "Job cpu time:       0 days 19 hours 14 minutes 28.0 seconds.", "Elapsed time:       0 days  0 hours 59 minutes 49.3 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 10:04:16 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7a_source_optfreq_nbo_strict_v1_a01/input.com; SHA256 49443df456c642ee1da3bb0636a7b7f255922994a3244f143c49008766d3a332; 2519 bytes.
  input_route: ["#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 Opt=(Tight,CalcFC,MaxCycles=180) Freq Pop=NBO NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) 5D 7F"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7a_source_optfreq_nbo_strict_v1_a01/stdout.log; SHA256 a6b12e3252bcf3bb9aa0f8c4666043689fda135da7402256e868282e10ed5d93; 2556660 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -995.346144210     A.U. after    3 cycles"]
  frequencies: {"count": 153, "minimum_cm1": 26.8016, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 14 hours 50 minutes 20.7 seconds.", "Elapsed time:       0 days  1 hours 57 minutes 15.3 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 08:58:26 2026.", "Job cpu time:       1 days 10 hours 21 minutes 17.5 seconds.", "Elapsed time:       0 days  1 hours 43 minutes 45.3 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 10:42:14 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7a_spinspin_element_repair_20261002_freshstopresume_a01/input.com; SHA256 f4db66694d3cb43a4b3ab004b3f8f3395a6f7c624bdf6789f614002b4adcb5da; 6900 bytes.
  input_route: ["#p B3LYP/Gen EmpiricalDispersion=GD3 NMR=(SpinSpin,Mixed,ReadAtoms) Integral=NoXCTest NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7a_spinspin_element_repair_20261002_freshstopresume_a01/stdout.log; SHA256 15b469a59d0eeb57919adb6485bdf825c7f06d9db3ac4fb6142f228723a07bc6; 436000 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -6788.85129019     A.U. after   12 cycles"]
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 12 hours 36 minutes 13.4 seconds.", "Elapsed time:       0 days  1 hours 50 minutes 41.8 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 08:58:05 2026.", "Job cpu time:       0 days 17 hours 17 minutes 11.2 seconds.", "Elapsed time:       0 days  0 hours 53 minutes 38.3 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 09:51:43 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7e_source_optfreq_nbo_strict_v1_a01/input.com; SHA256 5f411804064c87fe70f70478e92973bdade5e6b61deb699319c36319a407ccb3; 2506 bytes.
  input_route: ["#p B3LYP/def2TZVPP EmpiricalDispersion=GD3 Opt=(Tight,CalcFC,MaxCycles=180) Freq Pop=NBO NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) 5D 7F"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7e_source_optfreq_nbo_strict_v1_a01/stdout.log; SHA256 eb772de3d34a53271b1fc51bfbdc723183f70708c6a2c7f82a290e1cef8e0fc9; 2642356 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -995.349732195     A.U. after    1 cycles"]
  frequencies: {"count": 153, "minimum_cm1": 16.8765, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days 15 hours 49 minutes 40.0 seconds.", "Elapsed time:       0 days  2 hours  0 minutes 29.4 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 09:01:59 2026.", "Job cpu time:       1 days  8 hours 40 minutes 16.0 seconds.", "Elapsed time:       0 days  1 hours 38 minutes 53.4 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 10:40:54 2026."]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7e_spinspin_element_repair_20261002_a01/input.com; SHA256 7073f32a0cf56bb2884c07d333203acf91242183c3c28a3b1374a106f78c92a4; 6819 bytes.
  input_route: ["#p B3LYP/Gen EmpiricalDispersion=GD3 NMR=(SpinSpin,Mixed,ReadAtoms) Integral=NoXCTest NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/upgrade_tasks_verification/group_5/papers/paper_a21b91f97ce3c68f/v2_execution_20260929/outputs/sn7e_spinspin_element_repair_20261002_a01/stdout.log; SHA256 e034c1af476d497091a50d9f7cbcde9724742909238b8cff3115f9f35868398e; 433287 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -6788.85245900     A.U. after   11 cycles"]
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       1 days  9 hours 47 minutes 41.9 seconds.", "Elapsed time:       0 days  1 hours 42 minutes 16.3 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 06:03:36 2026.", "Job cpu time:       0 days 16 hours 18 minutes 27.9 seconds.", "Elapsed time:       0 days  0 hours 50 minutes 41.4 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 06:54:18 2026."]

## Historical verification retained verbatim; superseded status labels are noncurrent

The following historical narrow-task/legacy reference segments are retained as facts, not active rubric or qualification. Current acceptance and scoring at the top governs this version. Original full evaluator snapshots are indexed in evaluation/history_archive_index.json.

### Historical source legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot

# 已验证成功计算参考 — paper_a21b91f97ce3c68f / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文与 SI S2 方法、S5 理论 J、S10–11 的 1a 坐标。

[论文正文](../../../../papers/paper_a21b91f97ce3c68f/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_a21b91f97ce3c68f/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 给定 axial-1a，完整 62 原子中性 singlet；任务本来就是该对象的 Sn–C coupling，几何不是待发现的答案。Gaussian16 B3LYP-GD3/def2TZVPP 气相 Opt/Freq，180 正频，最低 14.6467 cm⁻¹。
2. 配对该最低点和 NMR 输入/输出，保留原子顺序，Sn index1、butyl carbon indices2/3/7。B3LYP-GD3/TZP-ZORA，NMR=(SpinSpin,Mixed,ReadAtoms)，Integral=NoXCTest，指定 119Sn/13C。TZP-ZORA 是基组名，不据此虚称 Gaussian 启用了 ZORA Hamiltonian。
3. 从 FC+SD+PSO+DSO 的完整 signed J 提取 −249.688、−223.744、−205.060 Hz，算术均值 −226.164 Hz；与理论 −217±15 Hz 比较，不取绝对值、不乘作者面向实验的经验校准因子。
4. 三个键距离约 2.1844/2.1891 Å 等身份/几何数据和 native NMR isotopes、分量表作为过程证据；该单结构链不证明整个 axial/equatorial 系列或 NBO 因果。

## 3. 有效产物与原始输入/输出

- [provenance/sn_coupling_closure_20260918.json](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/sn_coupling_closure_20260918.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [local_stage_tests_20260914/compound_1a_computed_parent_tzp_zora_sn119_c13_spinspin_20260916/stdout.log](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_computed_parent_tzp_zora_sn119_c13_spinspin_20260916/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_computed_parent_tzp_zora_sn119_c13_spinspin_20260916/input.com)
- [local_stage_tests_20260914/compound_1a_full62_si_optfreq_20260915/stdout.log](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_full62_si_optfreq_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_full62_si_optfreq_20260915/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_ar_process_minimum` | The final reported geometry is checked for stationarity and the report states the imaginary-frequency evidence. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_process_pairs` | The three Sn–butyl carbon pairs are identified explicitly from the final geometry and retained with per-pair context. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_result_mean` | The submission reports the signed average one-bond 119Sn–13C_Bu coupling for the supplied structure in Hz. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `c_ar_final` | The validated calculation yields a defensible signed average Sn–C_Bu coupling, and any electronic-structure interpretation is presented as an inference bounded by the single-system calculation. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

不新增 equatorial/NBO 必评工作；保留当前 signed-mean 科学目标。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。

