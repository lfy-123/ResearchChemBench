# V3 scope and evidence reuse — 2026-10-28

The same ten complete AZ molecules and C. albicans MIC column; explicit final orbital gaps and three descriptor/activity comparisons, with a bounded explanatory/predictive conclusion.

r_frontier_gap_az1–az10 reuse the ten literal-SI-coordinate B3LYP/6-31G(d) native single-point values and prior optimized comparisons: 4.417496443–4.428925225 eV, all inside unchanged individual source targets ±0.10 eV. Those single points are not relabelled optimizations. The three association rules and bounded_activity_information reuse AZ_literal_statistics_results.json: activity=-log2(MIC), dipole rho=0.394771 (prior optimized 0.315817), HOMO rho=0.427669, gap rho=-0.427669 (prior optimized -0.357467). Dipole discrepancies AZ4 +0.9999 D, AZ6 -0.6000 D and AZ10 +2.0300 D remain; source maximum AZ8 becomes literal-coordinate AZ10. Existing evidence supports descriptive information and concrete discordance, not external prediction or a biological mechanism.

Final rules: r_frontier_gap_az1, r_frontier_gap_az2, r_frontier_gap_az3, r_frontier_gap_az4, r_frontier_gap_az5, r_frontier_gap_az6, r_frontier_gap_az7, r_frontier_gap_az8, r_frontier_gap_az9, r_frontier_gap_az10, r_dipole_activity_association, r_frontier_activity_association, r_gap_activity_association, r_bounded_activity_information.

The following text is unchanged historical verification, including its old policy/status wording. It is not a declaration of a new V3 PASS. No new calculations were performed.

---

# Current computational verification and scoring reference — 2026-10-20

Acceptance: **ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**. The coordinator-approved scope has sufficient valid computations and matching key qualitative nodes/conclusions. Original strict numerical gates are not relabelled as passed. This acceptance does not assert exact historical inputs, whole-paper reproduction, blinded autonomous success or an online Judge score.

Current scoring: paper_science_v2, 100 fixed binary points, intermediate and final conclusions; formal_scoring_permitted=true. Publication/expert review remains separate and is not a runtime scoring freeze. The unchanged public PR contract continues to govern baseline reproduction or justified substitution, while AR chooses methods. Public legacy wording about process assessment is retained byte-for-byte but confers no process score.

## Scientific objects, conditions and completed verification

The ten complete neutral singlet AZ derivatives and the supplied C. albicans assay; descriptor values and descriptive information within n=10, not docking, clinical efficacy, permeability mechanism or prospective prediction.

描述符与MIC的描述性关联方向保留但强度减弱，十个真实对象的气相DFT及源坐标核查完成。当前任务不要求证明膜通透性、溶解度或抑菌因果机制；不把这些论文外推当成此次复现成果。

Gaussian16 C.01，B3LYP/6-31G(d)，气相中性单重态。
十个完整中性单重态，无D3/无溶剂；SI源坐标直接单点核查与既有优化/频率端点分开。
泛函、基组、气相、对象/电荷/多重度与披露一致。
6D/7F、SCF和网格实际值已记录，源未公开普通默认不单独否决。

- 十个SI坐标单点正常结束，既有优化/频率端点保留；不将单点称重优化。
- AZ4/6/10/8原生日志确认在受测扰动下波函数稳定；不声称遍历所有构象/所有电子解。

## Supported qualitative outcomes

- 以−log2 MIC定义活性，源及实际偶极与活性的rho均正，HOMO方向/等级关联保持；不能声称强度相同。
- AZ6/AZ9实验MIC较佳；AZ7仍最低偶极，AZ5/AZ9仍较强极性。
- 间隙约4.42 eV；窄描述符变化不足以单独识别可靠药效因果规律。

## Retained conflicts and boundaries

- 偶极冠军由源AZ8变实际AZ10；披露排序变化，任务不要求最大偶极对象成为活性机制必胜者。
- 源mu=−eta、omega=eta/2及gap符号问题与物理定义分开；不能以修正定义解释偶极偏差。
- 主文低LUMO文字与S12并非全相符，不交换行号掩盖。
- 接受仅描述性关联及边界，不复现或背书源通透性、溶解度、对接的因果外推；不新增p值阈值。

Verification sequence: identity-map all ten neutral singlets to the same C.albicans MIC column; retain valid existing optimized models; perform the already-completed literal SI-coordinate single points separately; recover raw frontier eigenvalues/dipole vectors, then inspect AZ4/6/10/8 wavefunction stability checks; derive physically defined descriptors separately from literal source formulas; analyze all ten MIC ties, source/literal/optimized descriptor sets without changing labels. No new quantum calls were made in this migration.


### All ten EHOMO_eV

| object | source S12 | literal SI-geometry actual | actual−source | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| AZ1 | -5.6907 | -5.690717206 | -1.720562347e-05 | 1.720562347e-05 | eV |
| AZ2 | -5.6183 | -5.618334918 | -3.491820914e-05 | 3.491820914e-05 | eV |
| AZ3 | -5.6901 | -5.689900864 | 0.0001991359639 | 0.0001991359639 | eV |
| AZ4 | -5.7094 | -5.709493062 | -9.30621332e-05 | 9.30621332e-05 | eV |
| AZ5 | -5.5984 | -5.598198492 | 0.0002015076129 | 0.0002015076129 | eV |
| AZ6 | -5.6577 | -5.657791428 | -9.142826582e-05 | 9.142826582e-05 | eV |
| AZ7 | -5.7045 | -5.704595013 | -9.501260892e-05 | 9.501260892e-05 | eV |
| AZ8 | -5.5775 | -5.577517839 | -1.783884016e-05 | 1.783884016e-05 | eV |
| AZ9 | -5.5758 | -5.575885156 | -8.51556654e-05 | 8.51556654e-05 | eV |
| AZ10 | -5.55 | -5.550034339 | -3.433873171e-05 | 3.433873171e-05 | eV |


### All ten ELUMO_eV

| object | source S12 | literal SI-geometry actual | actual−source | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| AZ1 | -1.2639 | -1.263968891 | -6.889112614e-05 | 6.889112614e-05 | eV |
| AZ2 | -1.1951 | -1.195124084 | -2.408392379e-05 | 2.408392379e-05 | eV |
| AZ3 | -1.2631 | -1.263424663 | -0.0003246634012 | 0.0003246634012 | eV |
| AZ4 | -1.2805 | -1.280567837 | -6.78367362e-05 | 6.78367362e-05 | eV |
| AZ5 | -1.1763 | -1.176348227 | -4.822741406e-05 | 4.822741406e-05 | eV |
| AZ6 | -1.2321 | -1.232131569 | -3.156921834e-05 | 3.156921834e-05 | eV |
| AZ7 | -1.2767 | -1.276758243 | -5.824266176e-05 | 5.824266176e-05 | eV |
| AZ8 | -1.1564 | -1.156483915 | -8.391545449e-05 | 8.391545449e-05 | eV |
| AZ9 | -1.1556 | -1.155667574 | -6.757386711e-05 | 6.757386711e-05 | eV |
| AZ10 | -1.1325 | -1.132537896 | -3.789555802e-05 | 3.789555802e-05 | eV |


### All ten gap_eV

| object | source S12 | literal SI-geometry actual | actual−source | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| AZ1 | 4.4268 | 4.426748314 | -5.168550267e-05 | 5.168550267e-05 | eV |
| AZ2 | 4.4232 | 4.423210834 | 1.083428535e-05 | 1.083428535e-05 | eV |
| AZ3 | 4.427 | 4.426476201 | -0.0005237993651 | 0.0005237993651 | eV |
| AZ4 | 4.4289 | 4.428925225 | 2.522539701e-05 | 2.522539701e-05 | eV |
| AZ5 | 4.4221 | 4.421850265 | -0.000249735027 | 0.000249735027 | eV |
| AZ6 | 4.4256 | 4.425659859 | 5.985904749e-05 | 5.985904749e-05 | eV |
| AZ7 | 4.4278 | 4.42783677 | 3.676994717e-05 | 3.676994717e-05 | eV |
| AZ8 | 4.4211 | 4.421033923 | -6.607661433e-05 | 6.607661433e-05 | eV |
| AZ9 | 4.4202 | 4.420217582 | 1.758179829e-05 | 1.758179829e-05 | eV |
| AZ10 | 4.4175 | 4.417496443 | -3.556826309e-06 | 3.556826309e-06 | eV |


### All ten dipole_D

| object | source S12 | literal SI-geometry actual | actual−source | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| AZ1 | 4.8228 | 4.8228 | 0 | 0 | D |
| AZ2 | 5.5423 | 5.5423 | 0 | 0 | D |
| AZ3 | 4.8216 | 4.8215 | -0.0001 | 0.0001 | D |
| AZ4 | 5.14 | 6.1399 | 0.9999 | 0.9999 | D |
| AZ5 | 5.8037 | 5.8037 | 0 | 0 | D |
| AZ6 | 5.6209 | 5.0209 | -0.6 | 0.6 | D |
| AZ7 | 3.7138 | 3.7138 | 0 | 0 | D |
| AZ8 | 7.0955 | 7.0955 | 0 | 0 | D |
| AZ9 | 5.847 | 5.847 | 0 | 0 | D |
| AZ10 | 5.4521 | 7.4821 | 2.03 | 2.03 | D |


### MIC observations and frontier-gap alternative geometry check

| object | MIC (µg/mL) | source gap | literal SI gap | prior optimized gap | prior optimized dipole (D) |
| --- | --- | --- | --- | --- | --- |
| AZ1 | 1000 | 4.4268 | 4.426748314 | 4.426748314 | 4.8249 |
| AZ2 | 1000 | 4.4232 | 4.423210834 | 4.423210834 | 5.5423 |
| AZ3 | 500 | 4.427 | 4.426476201 | 4.426748314 | 4.8236 |
| AZ4 | 500 | 4.4289 | 4.428925225 | 4.428653112 | 3.4012 |
| AZ5 | 500 | 4.4221 | 4.421850265 | 4.422122379 | 5.8046 |
| AZ6 | 250 | 4.4256 | 4.425659859 | 4.425931973 | 5.0246 |
| AZ7 | 1000 | 4.4278 | 4.42783677 | 4.428108884 | 3.7147 |
| AZ8 | 500 | 4.4211 | 4.421033923 | 4.420489696 | 5.1806 |
| AZ9 | 250 | 4.4202 | 4.420217582 | 4.421578151 | 6.0404 |
| AZ10 | 500 | 4.4175 | 4.417496443 | 4.420489696 | 5.1528 |


### Descriptive associations against activity=−log2(MIC)

| descriptor | dataset | rho | rho−source | absolute rho difference | exact p | leave-one-out rho range |
| --- | --- | --- | --- | --- | --- | --- |
| EHOMO_eV | source_printed | 0.4276686017 | 0 | 0 | 0.219047619 | [0.29814239699997197, 0.5434311918885962] |
| EHOMO_eV | descriptors | 0.4276686017 | 0 | 0 | 0.219047619 | [0.29814239699997197, 0.5434311918885962] |
| EHOMO_eV | previous_optimized_geometry | 0.4276686017 | 0 | 0 | 0.219047619 | [0.29814239699997197, 0.5434311918885962] |
| ELUMO_eV | source_printed | 0.4276686017 | 0 | 0 | 0.219047619 | [0.29814239699997197, 0.5434311918885962] |
| ELUMO_eV | descriptors | 0.4276686017 | 0 | 0 | 0.219047619 | [0.29814239699997197, 0.5434311918885962] |
| ELUMO_eV | previous_optimized_geometry | 0.4276686017 | 0 | 0 | 0.219047619 | [0.29814239699997197, 0.5434311918885962] |
| gap_eV | source_printed | -0.3750324661 | 0 | 0 | 0.2857142857 | [-0.48107023544236394, -0.22360679774997896] |
| gap_eV | descriptors | -0.4276686017 | -0.0526361356 | 0.0526361356 | 0.219047619 | [-0.5434311918885962, -0.29814239699997197] |
| gap_eV | previous_optimized_geometry | -0.357466987 | 0.01756547912 | 0.01756547912 | 0.3103174603 | [-0.46267025093219405, -0.22783059421644178] |
| dipole_D | source_printed | 0.5724179746 | 0 | 0 | 0.08888888889 | [0.451848057057532, 0.6503356886535661] |
| dipole_D | descriptors | 0.394771017 | -0.1776469576 | 0.1776469576 | 0.2611111111 | [0.19364916731037085, 0.5776508941874458] |
| dipole_D | previous_optimized_geometry | 0.3158168136 | -0.256601161 | 0.256601161 | 0.373015873 | [0.07453559924999299, 0.5163977794943222] |

The printed-source rho values in this table are analysis of author S12 and assay data, not correlations claimed numerically by the authors. 2520 label permutations preserve ties; exchangeability is an analysis assumption, not new assay replication. No p threshold defines acceptance. The analysis elapsed0.6738004200160503s as recorded; quantum timing remains per-job native data below.

Source gap prose prints EHOMO−ELUMO but table values use positive ELUMO−EHOMO. Source μ=−η and ω=η/2 are not physical finite-difference μ=−(IP+EA)/2 and ω=μ²/(2η); source arithmetic is not a scientific correctness target. Source/literal HOMO and LUMO rankings support the same correlation, while rounded tiny gap ranks alter rho. Corrected descriptor definitions do not explain the real dipole changes. Source maximum-dipole AZ8 becomes AZ10 on literal source coordinates; prior optimized dipoles differ again, so no highest-dipole identity is scored.

Concrete inference support: AZ8 has a large dipole but MIC500, whereas AZ6/MIC250 has lower polarity; AZ10 becomes largest dipole with MIC500. Equal or similar descriptors span tied/different MICs. Positive retrospective associations therefore carry descriptive information while failing to uniquely determine biological activity. No docking, target-binding, membrane-permeability or clinical causal mechanism is validated.

## Rule design and tolerance boundary

Ten independently computable gas-phase frontier gaps each carry2 points,20 points total. Each uses its own author S12 positive ELUMO−EHOMO target and one fixed inclusive absolute class tolerance±0.10 eV. This is a provisional benchmark policy for approximate orbital-level separation (about4.42 eV), not an author uncertainty/error bar or a claim of universal DFT accuracy. A0.10 eV coarse scale distinguishes chemically materially different separations while avoiding false precision from table rounding and conformer sensitivity; it is deliberately much wider than the approximately0.0114 eV substituent spread and tiny current literal-coordinate residuals. It was not calculated as the largest observed residual plus margin and does not attempt to fit each compound. These ten independently completed molecular values earn only20% of the score; remaining polarity/association/synthesis leaves carry80%. Numerical window hits never establish fine frontier-gap ranking, HOMO/MIC or dipole/MIC relationships: qualitative leaves require actual all-ten raw values/ranks and assay ties; numerical misses do not erase them. Kohn–Sham ELUMO−EHOMO is not an optical/fundamental gap or source negative-sign arithmetic. Expert revision of this provisional class is a future version, not a current runtime freeze.

Evidence eligibility is checked per item; no independent points for software, convergence logs, report completeness or generic limitations. Wrong physical identity invalidates the affected result even if a number hits a window. Final inference must be explicitly supported in the submitted deliverable.

## Source location and independent readback

- papers/paper_5d94285cfbd51973/documents/main.pdf; SHA256 9a4125a542a33af7128c39ebcf9df93cbe82923038415ed18e81bc77ca65e1a2; 1-based PDF pages 4,5,6,7; C. albicans MIC table and molecular descriptor interpretation.
- papers/paper_5d94285cfbd51973/documents/supplementary_001.pdf; SHA256 9c09e4819df88ab73a3551dca09e2c5b390e7a783dac0df4f633e06e5e227f0e; 1-based PDF pages 7,41; Computational details and TableS12.

### Existing validation/analysis summaries (separate from primary sources)

- docs/strict_author_route_validation_20261001/groups/group2/reopen_20261002T1212Z/AZ_literal_statistics/attempt_001/AZ_literal_statistics_results.json; SHA256 cb39a419d7bed141cbfd09fd51c4ea18a5e679700990360e647a13ad041cb121. Historical status labels in these unchanged files are retained; current acceptance above supersedes them.
- docs/v2_verification/maintenance/qualitative_acceptance_review_20261020/INDEPENDENT_OTHER_NATIVE_SUPPLEMENT.json; SHA256 5f2ac9d3e1874077e3a9fbc7eda6c2020d36de0ae07dd915074a76fa73f6fea7. Historical status labels in these unchanged files are retained; current acceptance above supersedes them.

## Native artifact index, real resources and completeness

Paths below are workspace-relative on the shared server. They identify actual existing inputs/outputs; this migration only reads and hashes them. Normal termination alone does not establish the right molecule/state. Any errors or reused frequency-only recoveries remain in the index and are not erased. Resource lines are the individual logs’ recorded quantities; absent/all-job wall time and CPU cost are **not recorded as a reliable total** and are not inferred from allocations.

- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ6_10_8_local_scratch_repair03/AZ10/formchk.log; SHA256 f6b95eb2bbe94a36ebf0b15d2fc4e7abd38499b317b4900a5e65a992c1d7e475; 620 bytes.
  last_scf: []
  normal_termination_count: 0
  error_termination_count: 0
  reported_resources: []
- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ6_10_8_local_scratch_repair03/AZ10/stability.log; SHA256 19e13a793d660d069d3532b7588f6ee43b48aaa781b5293059b7e95ed308cf9b; 101889 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1696.65542000     A.U. after    1 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 38 minutes 26.5 seconds.", "Elapsed time:       0 days  0 hours  9 minutes 38.3 seconds.", "Normal termination of Gaussian 16 at Sun Oct 11 08:37:43 2026."]
- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ6_10_8_local_scratch_repair03/AZ6/formchk.log; SHA256 2cd3d009f0088ee5564eba6bb7f3726c4e4f895ccda8c8cdc52ed0d56be07263; 618 bytes.
  last_scf: []
  normal_termination_count: 0
  error_termination_count: 0
  reported_resources: []
- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ6_10_8_local_scratch_repair03/AZ6/stability.log; SHA256 e1657bd118b91a9b83d2fa7b64622f067014e8492ff71f978a20726759b43040; 99463 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1740.53590744     A.U. after    1 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 36 minutes 37.1 seconds.", "Elapsed time:       0 days  0 hours  9 minutes 11.1 seconds.", "Normal termination of Gaussian 16 at Sun Oct 11 08:28:01 2026."]
- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ6_10_8_local_scratch_repair03/AZ8/formchk.log; SHA256 d03803abc58eee19adb3dea8717d98cf82e972bcd6d554cdf351c970930a1b89; 618 bytes.
  last_scf: []
  normal_termination_count: 0
  error_termination_count: 0
  reported_resources: []
- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ6_10_8_local_scratch_repair03/AZ8/stability.log; SHA256 3c11d89f0b01babe8b584cac4c08459a6b720d1041df63872846948108488f9f; 52642 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1755.82529897     A.U. after    1 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 36 minutes 15.5 seconds.", "Elapsed time:       0 days  0 hours  9 minutes  5.5 seconds.", "Normal termination of Gaussian 16 at Sun Oct 11 08:46:53 2026."]
- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ_stability_storage_recovery02/AZ4/formchk.log; SHA256 3f31a6fbb7f8b3795c17e8a3826d09110e4bd970bb242919a789f351daa0991c; 618 bytes.
  last_scf: []
  normal_termination_count: 0
  error_termination_count: 0
  reported_resources: []
- docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_5d94285cfbd51973/cases/reopen20261011_AZ_stability_storage_recovery02/AZ4/stability.log; SHA256 febfa9f5d94ec7690b882ed19be21e8d6071b6d12f87620dd25119061fdd78cd; 97624 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -2200.12714132     A.U. after    1 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 33 minutes 27.0 seconds.", "Elapsed time:       0 days  0 hours  8 minutes 25.3 seconds.", "Normal termination of Gaussian 16 at Sun Oct 11 07:31:36 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/AZ4_screened_basin1_source_optfreq/attempt_001/input.com; SHA256 1cbbc491b6bdf4ad9643bc576248c7cf3be5f290195b9883f6c7a48276228c71; 2143 bytes.
  input_route: ["#p B3LYP/6-31G(d) Opt=(Tight,MaxCycle=200) Freq NoSymm Integral=UltraFine SCF=(XQC,Tight,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/AZ4_screened_basin1_source_optfreq/attempt_001/stdout.log; SHA256 da21bee1ab4ded07bd8c1655375a289e3de3692392667582f51b09143b553a25; 23378613 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -2200.12604856     A.U. after    1 cycles"]
  frequencies: {"count": 135, "minimum_cm1": 9.547, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  2 hours 55 minutes 12.7 seconds.", "Elapsed time:       0 days  0 hours  8 minutes 52.9 seconds.", "Normal termination of Gaussian 16 at Mon Sep 28 07:19:00 2026.", "Job cpu time:       0 days  1 hours 47 minutes  8.1 seconds.", "Elapsed time:       0 days  0 hours  5 minutes 24.2 seconds.", "Normal termination of Gaussian 16 at Mon Sep 28 07:24:26 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/AZ4_verified_basin2_source_optfreq/attempt_001/input.com; SHA256 e1d246dce2da26d487b1233746325b0f8b7aba269f98d70becd2a146a82b003f; 2133 bytes.
  input_route: ["#p B3LYP/6-31G(d) Opt=(Tight,MaxCycle=200) Freq NoSymm Integral=UltraFine SCF=(XQC,Tight,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/AZ4_verified_basin2_source_optfreq/attempt_001/stdout.log; SHA256 f32a38f1fd3752a32680c2a06d5a4296792f61142cb23bbad57ae5ea712085b1; 23745767 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -2200.12731060     A.U. after    1 cycles"]
  frequencies: {"count": 135, "minimum_cm1": 7.561, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  3 hours 57 minutes 55.3 seconds.", "Elapsed time:       0 days  0 hours 12 minutes 12.6 seconds.", "Normal termination of Gaussian 16 at Mon Sep 28 16:48:22 2026.", "Job cpu time:       0 days  1 hours 46 minutes 58.6 seconds.", "Elapsed time:       0 days  0 hours  5 minutes 22.4 seconds.", "Normal termination of Gaussian 16 at Mon Sep 28 16:53:46 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ4_literal_SI_geometry_B3LYP_descriptor_SP/attempt_001/input.com; SHA256 b0ee7f945193064a83db6449569242ac3cf5b13df80d1f738b620c20e7186e7e; 2075 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ4_literal_SI_geometry_B3LYP_descriptor_SP/attempt_001/stdout.log; SHA256 8956c435775166dc6d10d9f7f124fc1e6c2cc6a30531279e8a8901685ad315a2; 7165565 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -2200.12714132     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  7 minutes 53.8 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 24.4 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 06:58:08 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ8_literal_SI_geometry_B3LYP_descriptor_SP/attempt_001/input.com; SHA256 e50fe74eb9dea1cde9ca7582b5106bc009e89facc0422b917ac89ba60cee654a; 2238 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ8_literal_SI_geometry_B3LYP_descriptor_SP/attempt_001/stdout.log; SHA256 34376f5824040eb0f582ebea4097930ff7ff1436cc3ffac839b161dce5aa239a; 7238814 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1755.82529897     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  6 minutes 38.9 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 20.6 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 06:58:01 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ1/input.com; SHA256 9ec58783df818c3f67b750a5d94b84b9e8a4b1b7b59d733196aecd3ca5d82311; 2048 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ1/stdout.log; SHA256 2c617997fc2200e2fb641279f357a121afcde45fc1ade9554d0d2ae963612f50; 6794600 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -2100.89913859     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 10 minutes 40.4 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 33.1 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:15:15 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ10/input.com; SHA256 9b0aa5e6c874047abe24a0494f7358b5c5eaa1a12694144be91dac5321b17259; 2132 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ10/stdout.log; SHA256 8f63661c0267765cd6260b1ecf488f41f8233a50e2ae9c3d52b9fd11f9ae5856; 6799254 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1696.65542000     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  9 minutes 25.1 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 28.9 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:18:54 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ2/input.com; SHA256 b5775aa7d32d6ea26aee54130624bdf2454bc3d8f25898209da42d31225fb679; 2053 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ2/stdout.log; SHA256 033ce69079633db0c8c6a38db205a8286bc8503d0566a591c8a9f25b0235a4ae; 6334343 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1641.30385366     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  9 minutes 52.9 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 30.8 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:15:47 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ3/input.com; SHA256 0f32ee3d16c86122a91d850226c0c53c67493f88a927e98ae2c61b78e32ee58d; 2054 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ3/stdout.log; SHA256 2846d82605823a60d58018c6a82bfd58e1ffea313b5545636634b9aa609e9787; 7100936 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -4212.40799355     A.U. after   15 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 10 minutes 17.9 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 31.4 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:16:20 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ5/input.com; SHA256 2eecb908f3770707f8937736dd1c17a3a7e2690235eb4e52bd42ea7944f5442a; 2171 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ5/stdout.log; SHA256 92b0d67deb28fec7d4f9265956afe2a224090256a117d3a79ef7b0f8669cf26d; 6863630 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1680.62178998     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 10 minutes 35.5 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 32.4 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:16:53 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ6/input.com; SHA256 fe5a337402e246006218dd05aa9f2d805bf63bf658021f0df6880f69eb3192d2; 2052 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ6/stdout.log; SHA256 8107c506318baab26bbfe45380739f91fcff65fed43b7b15e99e860855b1be3b; 6681751 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1740.53590744     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  8 minutes 53.4 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 27.3 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:17:22 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ7/input.com; SHA256 70f45a30af618b79894c73f5fc7270515d1138fde57f50de14ffd7090687160c; 2052 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ7/stdout.log; SHA256 bb8ed5ce5a3834236b9f550bbf93a47b5773ec23c02ee85572693b7380cb13d7; 7049319 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1839.76175745     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  9 minutes 41.1 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 29.5 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:17:52 2026."]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ9/input.com; SHA256 13bedde38e248ed4d27e79eb548b108461f7d48c6d220dbe59c4140479bc0f1a; 2290 bytes.
  input_route: ["#p B3LYP/6-31G(d) NoSymm Integral=UltraFine SCF=(Tight,XQC,MaxCycle=512) Pop=Full"]
  input_resources: ["%nprocshared=20", "%mem=80GB"]
- docs/upgrade_tasks_verification/group_2/papers/paper_5d94285cfbd51973/outputs/strict_AZ_remaining8_literal_SI_geometry_SP_batch/attempt_001/AZ9/stdout.log; SHA256 c0e9be94d4a047abbb448f0ca38e85c586622497af352f7a8b715014e44459e6; 7345921 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -1719.93557884     A.U. after   16 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 10 minutes  7.3 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 30.8 seconds.", "Normal termination of Gaussian 16 at Thu Oct  1 07:18:24 2026."]

## Historical verification retained verbatim; superseded status labels are noncurrent

The following historical narrow-task/legacy reference segments are retained as facts, not active rubric or qualification. Current acceptance and scoring at the top governs this version. Original full evaluator snapshots are indexed in evaluation/history_archive_index.json.

### Historical source legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot

# 已验证成功计算链：AZ9 九构象电子描述符

- 论文 ID：`paper_5d94285cfbd51973`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1002/slct.202505650`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_4](../../../../docs/verification/group_4/paper_5d94285cfbd51973)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_4.md)
- 最新已归档科学状态：READY / PASS / MATCH / QUALIFIED（AZ9 气相描述符及有限构象范围）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_autonomous_research`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_5d94285cfbd51973)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 确认 AZ9 为 C23H23ClN4O2、53 原子中性单重态。用 ETKDG/MMFF94s 生成候选，档案包含 12 轮及 611 个池内构象；TFD/Butina 截止 0.03 聚成 9 个盆地，盆地数自第 3 轮后稳定。该有限饱和记录不等于穷尽全局构象空间。

2. 每个盆地各选一个代表，独立执行作者主层级 Gaussian 16 B3LYP/6-31G(d) 气相 Opt/Freq。九条均正常终止，分子图均为 AZ9，每条 153 实频、0 虚频。

3. 从九个主层级末态电子能选出 basin04，E = −1719.93864109 Eh；不按 MMFF 排名或与目标数值的接近程度选择。

4. 从所选主层级波函数提取 HOMO、LUMO、能隙和偶极矩；按任务公式推导 IP=−HOMO，EA=−LUMO，η=(LUMO−HOMO)/2，S=1/(2η)，μ_chem=(HOMO+LUMO)/2，χ=−μ_chem，ω=μ_chem²/(2η)。

5. 九条作业均包含同几何 B3LYP/6-311+G(d,p) linked SP；将所选 basin04 的大基组结果作为敏感性检查，与主层级数值分开报告，不用敏感性层级替换评分层级。

6. 对主量、派生量、结构身份、有限搜索停止依据与结论逐项核对 evaluator；明确区分论文 SI 的非常规化学势/亲电指数公式与任务公开的常规公式。

## 3. 实际结果与支持的结论

| 主层级量 | 计算值 | evaluator 参考 |
|---|---:|---:|
| HOMO / eV | −5.5913956458 | −5.5758 ± 0.35 |
| LUMO / eV | −1.1698174947 | −1.1556 ± 0.35 |
| gap / eV | 4.4215781511 | 4.4202 ± 0.35 |
| 偶极矩 / D | 6.0404 | 5.847 ± 1.0 |

派生量：IP=5.5913956 eV，EA=1.1698175 eV，η=2.2107891 eV，S=0.226163593 eV⁻¹，μ_chem=−3.38060657 eV，χ=3.38060657 eV，ω=2.5847108 eV。

大基组减主层级：ΔHOMO=−0.3496663 eV，ΔLUMO=−0.4106198 eV，Δgap=−0.0609535 eV，Δdipole=+0.3157 D。描述符在既定模型内支持任务比较，不能单独证明生物活性。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| az9_tfd_basin_01 Opt/Freq + SP | [input.com (1)](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_01_optfreq_hpc20/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_01_optfreq_hpc20/source_input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_01_optfreq_hpc20/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_02 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_02_optfreq_larger_basis_sp_hpc20_p3/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_02_optfreq_larger_basis_sp_hpc20_p3/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_03 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_03_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_03_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_04 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_04_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_04_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_05 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_05_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_05_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_06 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_06_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_06_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_07 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_03d6a2def6f24a09be35908207102514/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_03d6a2def6f24a09be35908207102514/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_08 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_641925d42de64bb9b98c1d9a7fbea070/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_641925d42de64bb9b98c1d9a7fbea070/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_09 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_d00eed6e3253451dae3ff6e77d29a36a/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_d00eed6e3253451dae3ff6e77d29a36a/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_descriptor_closure_20260914.json](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/author_descriptor_closure_20260914.json)
- [provenance/evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/evaluation_task_qualification.json)
- [report/results.json](../../../../docs/verification/group_4/paper_5d94285cfbd51973/report/results.json)
- [verification_report.md](../../../../docs/verification/group_4/paper_5d94285cfbd51973/verification_report.md)
- [provenance/generate_az9_conformer_ensemble.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/generate_az9_conformer_ensemble.py)
- [provenance/cluster_az9_tfd_ensemble.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/cluster_az9_tfd_ensemble.py)
- [provenance/prepare_az9_dft_specs.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/prepare_az9_dft_specs.py)
- [finalize_author_descriptors_20260914.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/finalize_author_descriptors_20260914.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- SI 非常规公式与任务常规公式的区别需要保留；没有通过换公式、改容差来迎合原目标。
- 九个盆地给出有限候选集合内的最低点证据，不声称数学上的全局最低点或真实溶液种群。
- 抗菌、ADMET、docking 及完整药理结论不属于此计算链的验证范围。

## 7. 成功阶段计时

六组成功 HPC 使用 20 CPU，三组成功 native 使用 1 CPU。成功日志累计 CPU 251821.2 s（69.9503 核时），wall 1048282.3 s（291.1895 h）；并行作业 wall 之和不是日历工期。

本次归档没有提交、重启或停止任何计算作业。

