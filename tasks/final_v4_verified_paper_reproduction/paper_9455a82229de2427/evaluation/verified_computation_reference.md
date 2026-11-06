# Second audit — candidate coverage

Second audit: the public comparison now explicitly addresses two inequivalent diene/SiN orientations, without supplying product graphs, ring size, entry atom or a winning mechanism. Existing evidence covers two specific P1/P2 endpoints and a finite P1 route, not the whole product space. Source-specific required endpoints versus independent AR alternatives remain an expert issue. Do not silently apply P1/P2 windows to another product or claim whole-space exclusion.

# V3 scope and evidence reuse — 2026-10-28

Same isolated-gas SiN/isoprene H-loss question: two source-supported products and their E0, a bounded connected formation explanation and product identifiability; no new network or control matrix.

r_p1_structure/p2_structure and r_p1_exoergicity/p2_exoergicity reuse P1/P2_CBS_verification and P1_P2_H_asymptote_comparison_20260930.json: E0=-156.4325195194/-150.5408983284 kJ/mol within unchanged [-189,-135]. r_formation_account reuses P1_ROUTE_EDGE_AUDIT.json and connected-edge native CBS/IRC/LQA/exit evidence, without making its author node sequence mandatory. r_product_identifiability follows from the overlap and bounded route coverage. The i2→i4 local barrier is 148.7503076 kJ/mol versus source prose140/Fig5-derived142; it is still -40.6059774 relative to reactants. This mismatch, finite exit/entry sampling and composite spin contamination remain unresolved limits. The full P2 network, all38 isomers and rates are not claimed.

Final rules: r_p1_structure, r_p2_structure, r_p1_exoergicity, r_p2_exoergicity, r_formation_account, r_product_identifiability.

The following text is unchanged historical verification, including its old policy/status wording. It is not a declaration of a new V3 PASS. No new calculations were performed.

---

# SiN plus isoprene H-loss channel: verified computation reference

## Current acceptance — 2026-10-20

**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**. Formal scoring is permitted for the unchanged bounded task. Original numerical gates have not been declared passed. No new quantum chemistry or HPC jobs were run during this scoring migration. This is a retrospective source/native verification, not an information-limited blind Agent experiment.

Current scientific scope: Product structures and a bounded formation account for the isolated-gas H-loss channel, with explicit distinction between product compatibility and connected route evidence.

Current scoring is paper_science_v2: 100 points, independent binary intermediate and conclusion leaves, no process score or multiplier. AR retains method freedom; PR follows the disclosed baseline or substantiates an equivalent. The public contract is byte-frozen, including stale process/calibration wording; current private scoring supersedes those legacy evaluator statements.

## Current numerical scoring definition

The P1 and P2 channel E0 leaves are numeric: target−162 kJ/mol, inclusive absolute tolerance27 kJ/mol. This is exactly the frozen public experimental uncertainty [−189,−135], not an author DFT accuracy estimate, residual-fitted tolerance, or permission to use ±27 for any local barrier. Native physical identity, state and energy-reference evidence is required before comparison; independent qualitative leaves remain independent.

## Objects, software and source-aligned method

Isolated gas-phase neutral SiN(doublet)+C5H8(singlet), 15 atoms/59 electrons in total and a neutral doublet PES. H-loss gives SiNC5H7 (14-atom singlet products) plus H(doublet). Compare 0 K E0=electronic+ZPVE relative to separated SiN+isoprene, at single-collision 25±1 kJ/mol conditions; the −162±27 kJ/mol observed channel energy is not a 298 K solution Gibbs energy. Preserve atoms and states.

Gaussian16 Revision C.01 implements CBS-QB3, with B3LYP/CBSB7 optimization/frequencies; native CBSB7 prints 6-311G(2d,d,p) with 5D/7F. Correlated composite steps include native CCSD(T)/6-31+G(d′), MP4SDQ/CBSB4 and MP2/CBSB3/extrapolation. No ECP, continuum solvent or RI/COSX replacement is applied. Native built-in E0 already includes the specified ZPVE convention; do not add it a second time. Full intermediates have 30 alpha/29 beta electrons. The source methods are main physical p3; Fig5 is p6; SI p3 contains distinct 0K/Energy/Enthalpy/Free Energy values.

## Actual verification workflow and connected scientific nodes

The retained work optimized and frequency-checked full P1/P2 and reactants, formed consistent product+H asymptotes, located the P1 sequence saddles and endpoints, checked two-direction connections and wavefunction stability at geometry-level where applicable, obtained CBS0K energies for connected structures, and verified finite entrance and exit scans. It did not rerun all 38 products or require two entire networks.

| Connection | Actual retained result |
| --- | --- |
| SiN+isoprene → i1-trans | Reused intact source-oriented6.0/4.5/4.0/3.5/3.0A outerelectronic points; fromtheactual3.0A point, nativeLQA168markers(seed0+167nonzero) decreases−7.2000→−219.5153kJ/mol, net16.68483sqrt(amu)Bohr, preservesfragments exceptnewC5–N15. Actualminimumdetected; four-stepOptreturns i1trans with4criteriaYES, properRMSD0.00368153A andΔE2.497986e−6Eh vsoldpositiveStableminimum. |
| i1-trans ↔ i1-cis | Existing correctTS−210.2002cm−1 and early accepted9/10 IRC portions, followed from exactly those points by115/102 nativeLQA point markers. Net11.39640/10.01132 sqrt(amu)Bohr; nativePES-minimum detection on both sides. All sampled labelledgraphs remaini1. Trans/cis torsions177.1234/1.02986degrees; properRMSD0.0316134/0.0303992Å to existing endpoints;ΔE3.20085e−5/3.11555e−7Eh. Existing endpoint39positive modes/Stable reused. |
| i1-cis ↔ i2 | 实际两向IRC120/72点，端点释放/图/频率/稳定性核收；环化局部CBS0K势垒47.4060对Fig48kJ/mol。 |
| i2 ↔ i4 | 双向真实路径及正曲率/Stable端点回到i2/i4。CBS0K局部势垒148.7503，源正文140、Fig隐含142；相对反应物TS−40.606。 |
| i4 ↔ i5 | 两向IRC91/94点；i4/i5端点实际正曲率和Stable。局部CBS0K势垒89.87085对Fig90kJ/mol。 |
| i5 → P1+H | 从经过连接验收的i5沿Si14–H6坐标1.501439→4.001439Å的11个真实松弛点；P1 spectator图不变，源默认四判据均通过。B3LYP电子能采样单调上升至P1+H渐近线以下0.552586kJ/mol；残留P1片段与有效P1最低点pair-distance最大差0.001263Å。point5和11波函数稳定；CBS电子能相对同方法P1+H分别−18.4625/−0.714136kJ/mol。 |

The i1-trans/cis saddle has one mode −210.2002 cm−1; endpoints have 39 positive modes (minima16.7221 and8.6460 cm−1) and stability checks. The i2→i4 saddle has one mode −1736.3848 cm−1; i4 has39 positive modes, minimum44.0309 cm−1. Native correlated-reference spin contamination is retained (TS pre/post-annihilation values vary across links, up to1.1045/0.8435); a stable geometry-level DFT state does not certify a pure-spin composite wavefunction.

## Source versus native values and residuals

Signed residual is native−source. Absolute electronic-energy percentage residuals and comparison to an experimental central value as if it were an exact target are not meaningful relative errors.

| Quantity | Source | Actual | Signed residual | Absolute residual | Unit | Definition |
| --- | --- | --- | --- | --- | --- | --- |
| P1 CBS-QB3(0 K) | -538.081719 | -538.081716 | +0.0000030000 | 0.0000030000 | Eh | 同对象的完整复合0K能量 |
| P2 CBS-QB3(0 K) | -538.079462 | -538.079472 | -0.0000100000 | 0.0000100000 | Eh | 同上 |
| i7trans CBS0K | -538.608314 | -538.608321 | -0.0000070000 | 0.0000070000 | Eh | 完整CBS0K复用；不重复ZPE |
| i7trans/cis TS relative reactants | -161 | -161.8276848923005 | -0.8276848923 | 0.8276848923 | kJ/mol | CBS-SP电子能+0.99×原TS ZPE；同反应物0K参考 |
| i1cis→i2 local barrier | 48 | 47.40602149045276 | -0.5939785095 | 0.5939785095 | kJ/mol | CBS0K TS−cis |
| i4→i5 local barrier | 90 | 89.8708526593433 | -0.1291473407 | 0.1291473407 | kJ/mol | CBS0K TS−i4 |
| i7cis→i8 local barrier | 45 | 45.6734 | +0.6734000000 | 0.6734000000 | kJ/mol | 同定义CBS0K |

| i2→i4 comparison | Source local barrier | Actual local barrier | Signed residual | Absolute residual |
| --- | --- | --- | --- | --- |
| Main prose physical p7 | 140 | 148.7503075743086 | 8.7503075743086 | 8.7503075743086 |
| Fig5-derived physical p6 | 142 | 148.7503075743086 | 6.7503075743086 | 6.7503075743086 |

All entries in the last table are kJ/mol. Neither source value is chosen by proximity. The actual saddle is −40.6059774241 kJ/mol relative to reactants and remains submerged; i4 is −297.9653285848 kJ/mol and i4−i2=−108.6090435865 kJ/mol. The source TS Cartesian coordinates/complete CBS components are not uniquely mapped, so the residual cause is unassigned. Experimental ±27 kJ/mol must never be repurposed as a local-barrier tolerance.

P1+H and P2+H E0 are −156.4325195194 and −150.5408983284 kJ/mol, respectively, relative to separated reactants. Against the measured center−162 these differ by +5.5674804806 and +11.4591016716 kJ/mol (absolute differences the same), both inside the actual experimental interval [−189,−135]. Against source rounded theoretical values−156/−150, signed residuals are −0.4325195194/−0.5408983284 kJ/mol. Energetic compatibility alone does not prove either branching or a second entire path.

## Runtime, raw inputs/outputs and residual scope

The connected-edge CBS support records report TS wall508.45140165 s and i4 wall496.42826372 s. Those are individual completed jobs; total pipeline elapsed/queue time, cumulative allocation and peak memory are not fully recorded here. No total is inferred. Input.com, stdout.log/gaussian.log, checkpoint files and analysis hashes are inventoried below. The source’s broad barrierless language is accepted only as the bounded finite approach/exit evidence actually computed; no infinite-distance global proof is claimed.

## Remaining limits

- The source itself gives i2→i4 barrier140 in prose versus142 from Fig5, while actual is148.7503075743 kJ/mol; the gap remains a disclosed mismatch with no fitted window or invented causal explanation.
- Finite source-oriented entry and exit connections are supported. Infinite-separation barrierlessness, all38 isomers, a complete P2 network, absolute rates and branching fractions are outside the accepted result.
- The experimental energy interval tests channel compatibility, not thermodynamic 298 K equilibrium or local barrier accuracy. Composite spin contamination and unavailable source TS definition remain visible.

## Auditable raw/source artifact inventory

| Artifact | SHA-256 |
| --- | --- |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i1_entrance_preparation_20260930.json | 5bbe84d20c2a12179426c1604a1e9107fbc584ca15dc0636f218a58251c77a9e |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i1_entrance_recovered_point8_verification_20261001.json | 4cf39f805cf99eb160aaece958dc2bfa68ae2e2505db7bdbeda1a3e07b1fbd20 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i1trans_C5_N15_reverse_entrance_scan16_source_default_v2a1/stdout.log | bca67a3672bf1b43e70e344e1cefee077e864bf37577031bdc8fb68b430ea21c |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_returned_profiles_trial_energy_diagnosis_20261002_a3/RESULT.json | 9086a4c04c241078ce4fccf49afc5f7d2880cd070ff9c90c899f7163b8465163 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/INTERPOLATION_DEFORMATION_AUDIT.json | e23afe846f2fb977041e981133ef7e50a381e700dcedd0a6713f97e02fa29ba9 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/ENTRANCE_CONNECTION.json | 4000a8961ec9d1e4755908b70b93c99596219f4ba91dbb5f49fd83a97311a59b |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_entry3A_downhill240_i1TSCBS_20261009/spec.json | 99702f5ec4fdbaaa601d62455eea26d52c8311bbf53756d5036dce08ad67a5f0 |
| docs/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_9455a82229de2427/events/39c11bc652c19ef4/RETURNED_JOB_INTAKE.json | 5c840bd1ab4325a5b201d30c11d0f2e0d3cd81e9c3f0c75b127a95dd8cf73f77 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_entry3A_downhill240_i1TSCBS_20261009/outputs/ENTRANCE_DOWNHILL_AUDIT.json | 6cedeed8465c134bbe04ab97792ddf46dcbedb0cb3a50a8c9efd7aa85637f777 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_entry3A_downhill240_i1TSCBS_20261009/outputs/entrance_downhill_LQA/gaussian.log | 9c69befef139eb97f7d1c14e1e5741e507c53090fe8b423b98d4945b984ce322 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_entry3A_downhill240_i1TSCBS_20261009/outputs/entrance_cap_free_opt/gaussian.log | a04e37dd80fbb58796a165d3407ee4c1b8bbcda7e95b2c2dd61b5c32f5b35005 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i1_transcis_native90_saddle_verification_20261001.json | eadd8003868b709fdc5ccc2e85376990bbaa9dd633e2b0a3136a86cf1498c66c |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_GS2_ninepoint_trajectory_diagnosis_strict_a2/RESULT.json | e282f7c504de3fbe6a0b271cf8d443da451cb500de614fad4717bf236f9f055c |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i1_transcis_GS2_CalcFC_step10_strict_a1/stdout.log | e872f4e58d2fb4cc068f106d31575d85a89516bffddcc899adad83dff101fd42 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_transcis_reverse_only_GS2_strict_a1/stdout.log | 7fce7b66fc30b976fe64f30a4e8730b80746cc5cf96eba1151ec29036279620a |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_transcis_forward_point9_released_optfreq_strict_a1/stdout.log | cc14999150fb353515291cdf51fd853faf55e264a91be0395efb0576a03aef36 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_reverse_lastvalid_released_optfreq_20261002_a1/stdout.log | fba9a36a355dd4e238de3f4a7f7ef0ecbf3b449c63864182620e48fdbea4b8a7 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/i1_forward_PATH_AUDIT.json | 0fb5b2f1fe3fb51e2bf79da515cada0684b00e74ad2321a38d9597d07d49a49b |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/i1_reverse_PATH_AUDIT.json | 051cc8f1a30460200bf1653aa523c3ae5a67e4c4c51124d4b7856f9d4f073d7c |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/i1_forward_LQA/gaussian.log | cb2387bce754330c418c0af3e0cebbb7d913f37d653cc3c8ebef60c217702164 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/i1_reverse_LQA/gaussian.log | 6455e9334dcdcd757f36f13069f31bc552030700b0e8d222431f3704c46333c7 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_entry3A_downhill240_i1TSCBS_20261009/outputs/I1_TS_CBS_RESULT.json | 87bc2062e8355d583a3636ea9230c5ff08c7ac467a080dc0071be1a0bcc1381a |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/ringclosure_connected_edge_20261001.json | b7f4bc659d59c362995e857a8042f94d1176733d33cd03c40e9498028b48b4f9 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i1cis_i2_ringclosure_IRC_native_paths_20260930.json | 26ee42d2cbfc18886c453795bd36cea45df96a8edddf8d275ef59dbcdffd183d |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i1cis_i2_ringclosure_both_IRC_step5_recalc5_v2a1/stdout.log | 62df7028779b740686ed593a0a057df8104fbd8efd3685e7a3ddd4648e167597 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/ringclosure_IRC_forward_i1cis_candidate_endpoint_optfreq_stability_v2a1/stdout.log | 319072f53a027488e152a2fc4d5fdb7a5a7450adeda891408f1951ed6fc53fad |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/ringclosure_IRC_reverse_i2_endpoint_optfreq_stability_v2a1/stdout.log | 7e0b4244045c9a215050fefe74ab9008f6589819c7044aa68e57af00c1c40098 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/ringclosure_CBS_edge_verification_20261001.json | aeebe9dc85172e9ab286f0b8c4cbb3e7a97f737acf68d86d8685183b1bc479ce |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/IRC_connected_edge_20260930.json | 0a9eb45b8f4843b9581a736fc7cd009d864b9e4d81664a6e19c72055d8cceeaa |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/IRC_native_paths_20260930.json | c78cef3cab6712feb1ba43aa458943d62d92164e7151bddeff93e2bcf3c75056 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i2_i4_TS_both_IRC_step5_recalc5_v2a2/stdout.log | 496eb0e8be808d19a56ed2ee04bab29f030bbb5304700e4d011e2f5de8dbe417 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/IRC_forward_i4_endpoint_optfreq_stability_v2a1/stdout.log | 6d8b64318bab358e83d9502a7db9887320dc3f06d4a75e10ec4f79762ccfc778 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/IRC_reverse_i2_endpoint_optfreq_stability_v2a1/stdout.log | ddc90add429d7ebd7f99ad9158c6fcc523f0ed97752323f7df9e142e697aa295 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/connected_edge_CBS_verification_20260930.json | d03af0872219999d20d25272e9d546cb9ac6fd57e640213f69cae08e541471f9 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i4_i5_connected_edge_20260930.json | 7839ad5bd16ef729612770d19139489af149026477a0c220f814f2a8499a7d37 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i4_i5_IRC_native_paths_20260930.json | fd186bbe856ff882fa7ab27dc6cdbf705c7ea612f393eb94d5e1e1d9bd76b761 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i4_i5_TS_both_IRC_step5_recalc5_v2a1/stdout.log | ca8038ff805963b161ef6a4987aff504ba83fccd8f3cf6be622aaad61f299e21 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i4_i5_IRC_forward_i5_endpoint_optfreq_stability_v2a1/stdout.log | 30d33ed603c99b096c84cbba44e5c792683b77e1e0991e4359eb700a5b5f96e0 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i4_i5_IRC_reverse_i4_endpoint_optfreq_stability_v2a1/stdout.log | 04174f27c8b8b95c7383d648d1d37857a3c54a5aee79e89f7732a1c3c85cb0a8 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i4_i5_CBS_edge_verification_20260930.json | edb17e95f87f867de7e61c9b6c6bb4bfaf26be352765ef28b0ab86235c192c03 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i5_Hloss_scan_verification_20260930.json | 6f9f7adafd6acf6b66162e49910be36f3d78c1dab4385a84cebb33d27438c859 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i5_Si14_H6_relaxed_exit_scan10_B3LYP_CBSB7_v2a1/stdout.log | 93aae264f750d34c8a32470093798b0d8797c0476e43b9eb23d8b037cb3b8f64 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/i5_Hloss_stability_verification_20260930.json | c69fdb9fda2a2f24f7018bae204334d175e83d23f1ae7481c52fea5c4306a937 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i5_Hloss_scan_peakspin_and_far_stability_v2a1/stdout.log | 5432c8a3d1503edda78f520e254bcb6414b86ee0ed15df6a0c286510b6397f3b |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_P1_exit_two_CBS_matched_electronic_readback_20261002_a1/RESULT.json | 3fb3ad0214be8f9cbb5ecc4213ecc2a02517f7adcfa211074a74acb3769dd315 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_P1_exit_point05_CBS_electronic_control_20261002_a1/stdout.log | 2f11780c0250794d6179af35a88e1103af99d775ac27f8d093a289290a40460b |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/SiN_P1_exit_point11_CBS_electronic_control_20261002_a1/stdout.log | 2effe0d91d49549add74546e602678fbaa9007e71a9f6cc067f0f3d0dc6325ca |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/P1_P2_H_asymptote_comparison_20260930.json | 6d6ba2cebf8e79421a4f36224fcd6d9449fb9ee7bd9983055560b1e74d94e56b |
| docs/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_9455a82229de2427/P1_ROUTE_EDGE_AUDIT.json | 225e96121831ddc969a3a322fbdbf9d3cf8da799ccf3892a18af98cddb8189ba |
| docs/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_9455a82229de2427/events/39c11bc652c19ef4/CAUSE_ASSESSMENT.json | c8fdfbcf5cbc3f0470b00ca9b21171f6821862c3ee6473bbddd19b0d1f50e906 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/TS_connected_edge_CBSQB3_NoOpt_0K_v2a1/stdout.log | 9585e7a07ee7b345d9dc028cf66af7bfecad7a488846dbe0b8d027c9756d8c6c |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/TS_connected_edge_CBSQB3_NoOpt_0K_v2a1/input.com | e63b882d14dc407ac5117b0ecd9e6bd446591fbf1c7b1b1ec8c2e5041744042e |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/TS_connected_edge_CBSQB3_NoOpt_0K_v2a1/run_status.json | 397085de6a1adc1a54221e2b00732ccedc04b0056a74505b574df69a3138bdc8 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/TS_connected_edge_CBSQB3_NoOpt_0K_v2a1/calculation.fchk | 8f5089bcae323819045ab988e73df6a89fd06809c1fd3e65e029c6a61263dd2b |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/TS_connected_edge_CBSQB3_NoOpt_0K_v2a1/checkpoint_revalidation.json | 224aca3746e4dbfd545bddf461875a9227d4b530c4a85d25a62ca7db23195d70 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/TS_connected_edge_CBSQB3_NoOpt_0K_v2a1/checkpoint_revalidation.fchk | 53acbe15c9ec3c4b4245bd9c9a10333cb4d7fbbc146444957e09e3bdf8bbfede |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i4_connected_edge_CBSQB3_NoOpt_0K_v2a1/stdout.log | ac8acebbafa5df3cb8833c0a30476e06d765468ef6337c77dc9fdae4a13c9a4a |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i4_connected_edge_CBSQB3_NoOpt_0K_v2a1/input.com | e167b678e8668b1868338051cd913a3710c0fa1e377a78573ac819bc6b4a03aa |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i4_connected_edge_CBSQB3_NoOpt_0K_v2a1/run_status.json | 0f049ef3ad727f865d1ab870dbda85aeacf375ca40d593f2cd59b8aec48405bf |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i4_connected_edge_CBSQB3_NoOpt_0K_v2a1/calculation.fchk | c4fa06740e04fa03374eed3d92a64887845c49388e62142387baadcf130a2925 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/i4_connected_edge_CBSQB3_NoOpt_0K_v2a1/checkpoint_revalidation.json | 16b8b182ae6362aa292966f03772f18393d2b7e3f07f9d01763da2d8cd2b7716 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/outputs/IRC_forward_i4_endpoint_optfreq_stability_v2a1/calculation.fchk | 5df2522e188a908797885ab0b6bc2bce4d6a1cf01630b07ea9ef5ccc0216015e |
| docs/upgrade_tasks_verification/group_3/papers/paper_9455a82229de2427/sources/main.txt | 61da8c1340729e3926d0c2aa12f3cfa7048d99228fae783e527ced1233a6e867 |
| docs/upgrade_tasks_verification/group_3/papers/paper_9455a82229de2427/outputs/i2_source_mapped_CBSQB3_optfreq_local4_a3/stdout.log | e3575e3983f936f2dd1797bc55969f1c9ca4d491e369df9985eb6dca5c272339 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/P1_CBS_verification_20260930.json | f9a7d1c8a73813ca4e240ce9ea17388156514f84159ac82fe187ff23ba59611b |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/P2_CBS_verification_20260930.json | fcd7ab039226a3476b44c482fc09152de760d57ee49da9a70945d77c3c503c8b |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/H_atom_CBS_verification_20260930.json | e9eaed163c8eafa414221c3ff5b8bbba2ec08567a19da6bdc767914827ee747a |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/native_verification.json | bcc27f3919c0bc06af3995088dce0e04a1557e9a053f78011c996f757484ba48 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/P1_H_asymptote_verification_20260930.json | b0d05965402520b21f79bb2d332131c8a5c6b79aa370def478d729623376c868 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/contracts/paper_9455a82229de2427/paper_reproduction/agent_input/task.md | 60c7d7258859f4bbba94a5d9b821f7a8f57a02e3c0529000ab33ee017915a237 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i1trans_C5_N15_reverse_entrance_scan16_source_default_v2a1/input.com | 0bdb457358ac47a64b1ca2ed7eb2a8c3ba8fcc45494b9cbf180d75df652bd9d5 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_entry3A_downhill240_i1TSCBS_20261009/outputs/entrance_downhill_LQA/input.com | 4e971efd9b18e02a647d3607c8e0038d86966c390b439c7374773116a95c6791 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_entry3A_downhill240_i1TSCBS_20261009/outputs/entrance_cap_free_opt/input.com | 1c3fb49657902b25cb0373ae5c382c56d6689e85b3eebf1da31db072bc8b0a58 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i1_transcis_GS2_CalcFC_step10_strict_a1/input.com | e05247c272176643e219b7aba0602174184f977f2038ec9a73c5bc26786dbac7 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/SiN_transcis_reverse_only_GS2_strict_a1/input.com | 4fdbbea9d5d5848fe45789618302fc0fb4c1e49363c22cf452ecfeb1eccd6500 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/SiN_transcis_forward_point9_released_optfreq_strict_a1/input.com | d59e951032876bec137a06cd8aee253a62868494051d5d1143ee78281c093a60 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/SiN_reverse_lastvalid_released_optfreq_20261002_a1/input.com | ed0bd7050dde75f14e2ad6db8ee7bf1361524298c5f27f0d5e51421cba2bae3f |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/i1_forward_LQA/input.com | 6743d39a0d31a4823d5ebbc918359d7eaed18465b49118283e9340084fd02f82 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W05/papers/paper_9455a82229de2427/SiN_P1_rigid_entry_LQA_savedpoints_20261009/outputs/i1_reverse_LQA/input.com | d645bbe2133815bc3a7addb0a9ef8bc8b27b08d1bb402182eaa3098931070c27 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i1cis_i2_ringclosure_both_IRC_step5_recalc5_v2a1/input.com | cd41e47552defa81340f924f1bf0c930b5343f2aef1d798634a921177f591e7e |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/ringclosure_IRC_forward_i1cis_candidate_endpoint_optfreq_stability_v2a1/input.com | 5e854c28bad39082473dd3b3c5a8e0a6af2ee1cd9f1cceb616608caecfc9a08d |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/ringclosure_IRC_reverse_i2_endpoint_optfreq_stability_v2a1/input.com | c3c60d133a7e9cd35b8afc0844fe28b75dc5f20f4d0aa9d0378a0a92df4f02a4 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i2_i4_TS_both_IRC_step5_recalc5_v2a2/input.com | e09de69135684fa16839eb747fe2f46cab3e54bdac7c6e84d2941bc9901c6023 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/IRC_forward_i4_endpoint_optfreq_stability_v2a1/input.com | a28e6aaa782ccabf9bc4f4dbf97c73b6a83f33cf9a003e13c2214dea4579dcab |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/IRC_reverse_i2_endpoint_optfreq_stability_v2a1/input.com | b787f73bec2e1046d354216c5601106e76ad177a7f6878c8f573da09b10c1b0d |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i4_i5_TS_both_IRC_step5_recalc5_v2a1/input.com | 986ed40064e32b64fd11b86fbbd6b60f782a5704bb6c7600a6655d3a900b1574 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i4_i5_IRC_forward_i5_endpoint_optfreq_stability_v2a1/input.com | 2935505d964162acbef6ad6cfa2009e37f6c1fc1065f2e82b2f00b6e8e7dd89b |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i4_i5_IRC_reverse_i4_endpoint_optfreq_stability_v2a1/input.com | 7cc0bf22e26c5c7002ce3ebbca9f45844aa2358bcb40fe7dd28760eef3b12055 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i5_Si14_H6_relaxed_exit_scan10_B3LYP_CBSB7_v2a1/input.com | e6283b9403f198aea53ae343e38250f60c9b7c65de3f94062f3d47e47c104fb8 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/i5_Hloss_scan_peakspin_and_far_stability_v2a1/input.com | 1225f6f8df23665481491fa185e0d9e6554324a89ccbde88b74acb527beec289 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/SiN_P1_exit_point05_CBS_electronic_control_20261002_a1/input.com | b6b4bffc53b248f9cd4ffa93c5cdf50bd5b49f5ef042f22094f1e3661f8089b6 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/inputs/SiN_P1_exit_point11_CBS_electronic_control_20261002_a1/input.com | 0afa8e5e39bae2222b0266d9c7a80afbe9868ccff1eb68d690dc11afc0a2971c |
| docs/upgrade_tasks_verification/group_3/papers/paper_9455a82229de2427/inputs/i2_source_mapped_CBSQB3_optfreq_local4_a3/input.com | ea0c18a63e8f615114d53eed326c7b03eab58fb04805dad648fa7d31b713410a |
| docs/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_9455a82229de2427/P1_ROUTE_EDGE_AUDIT.json | 576fd9374588220b53b4b2e9fd3ab8d820978fecf5f08f150337130c96715bcd |
| docs/strict_author_route_validation_20261001/resume_closeout_20261010T1000Z/papers/paper_9455a82229de2427/SOURCE_COMPARISON.json | 07b7ec527b4548b8e553481aca7420742c8f092ddfd801c10394334e7b18917f |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/connected_edge_CBS_verification_20260930.json | d03af0872219999d20d25272e9d546cb9ac6fd57e640213f69cae08e541471f9 |
| docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9455a82229de2427/analysis/P1_P2_H_asymptote_comparison_20260930.json | 6d6ba2cebf8e79421a4f36224fcd6d9449fb9ee7bd9983055560b1e74d94e56b |
| docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_9455a82229de2427/ROUTE_ALIGNMENT.json | 6cd17a32aae49d6f8c1b9ecc6f290861a74c2b94a2afa89f32c8ba417aa70128 |

## Preserved earlier reference

No root-level verified_computation_reference.md existed in the source package. Historical evaluation snapshots are preserved byte-for-byte in the external archive indexed by evaluation/history_archive_index.json; source/native computation records remain at the artifact paths above.


## Historical reference text — non-current, preserved verbatim

Original location: legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot. Historical PASS/pending, numeric windows, search matrices and scoring prescriptions below are not the current scientific scoring policy.

# 已验证成功计算参考 — paper_9455a82229de2427 / paper_reproduction

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 1）

正文 PDF pp3–5、SI PDF p3，CBS-QB3/0 K 反应能和原子 H 损失通道。

[论文正文](../../../../papers/paper_9455a82229de2427/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_1/paper_9455a82229de2427/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_9455a82229de2427/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. SiN 中性 doublet、isoprene 中性 singlet 和原子 H doublet 分开计算；最终有效链采用独立图构建的两个 14 原子 SiNC5H7 singlet 六元环候选，不采用早期 SI 产物作为这条链的输入。
2. Gaussian16 CBS-QB3 优化/频率及完整复合能步骤：SiN 1 个正频、isoprene 33 个正频、每个产物 36 个正频；产物最低频率分别 118.4519 和 84.6768 cm⁻¹，图连接在优化前后不变。
3. 使用已含 ZPE 的 CBS-QB3(0 K)：SiN −343.624010、isoprene −194.897942、H −0.499818 Eh；两产物 −538.079465 和 −538.081724 Eh。ΔE0=[E0(product)+E0(H)−E0(SiN)−E0(isoprene)]×2625.499638，得到 −150.52251975 与 −156.45352343 kJ/mol，均位于实验 −162±27 的窗口。
4. 两独立产物的身份、最低点和热化学支持当前产物兼容性目标。此链没有 TS/IRC/PES 连接，不将能量兼容性写成分支比或反应路径已证明。

## 3. 有效产物与原始输入/输出

- [provenance/independent_cbs_raw_audit_20260918.json](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/independent_cbs_raw_audit_20260918.json)
- [provenance/independent_cbs_closure_audit_20260918.json](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/independent_cbs_closure_audit_20260918.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [execution_jobs/job_a50efe6b34614f4586674f56311b3659/stdout.log](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a50efe6b34614f4586674f56311b3659/stdout.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a50efe6b34614f4586674f56311b3659/input.com)
- [execution_jobs/job_a900b32bde494cb09e422e5eb6ff4f0d/stdout.log](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a900b32bde494cb09e422e5eb6ff4f0d/stdout.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a900b32bde494cb09e422e5eb6ff4f0d/input.com)
- [local_recovery_20260916/atomic_H_CBSQB3_reference_20260916/gaussian.log](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/local_recovery_20260916/atomic_H_CBSQB3_reference_20260916/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/local_recovery_20260916/atomic_H_CBSQB3_reference_20260916/input.com)
- [public_ring_orientation_1_CBSQB3_20260916/repair_20260918T035154Z/gaussian.log](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_1_CBSQB3_20260916/repair_20260918T035154Z/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_1_CBSQB3_20260916/repair_20260918T035154Z/input.com)
- [public_ring_orientation_2_CBSQB3_20260916/repair_20260918T035249Z/gaussian.log](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_2_CBSQB3_20260916/repair_20260918T035249Z/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_2_CBSQB3_20260916/repair_20260918T035249Z/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `pr_process_validation` | Each advanced candidate is uniquely identified and its optimized stationary point is validated as a minimum or transition state using frequency evidence; claimed TS connectivity is checked. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_product_identity` | The investigation identifies neutral singlet SiNC5H7 cyclic product structures among the validated candidates. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_energy_compatibility` | The cyclic product reaction energies are compatible with the experimental atomic-H-loss exoergicity window. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_final_conclusion` | The independently validated cyclic candidates provide computational support for the authors' qualitative terminal-addition/cyclization hypothesis, while energetic agreement supports compatibility with the observed channel rather than a measured branching ratio. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

公开新增的是实验比较窗口和反应能定义，不是产物几何/计算答案；共享作者知情验证不等同 AR 盲测。历史字段 atomic_H_product_energy_hartree 在私有契约检查中无损映射为 h_energy_hartree。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。


## Historical reference text — non-current, preserved verbatim

Original location: v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot. Historical PASS/pending, numeric windows, search matrices and scoring prescriptions below are not the current scientific scoring policy.

# Development reference status

No expanded scientific reference has been certified. Status: implemented_pending_expanded_reference.

See `reference_validation_plan.md` and private `legacy_final_snapshot/` for historical material. The old PASS does not apply. New quantum calculations: 0.
