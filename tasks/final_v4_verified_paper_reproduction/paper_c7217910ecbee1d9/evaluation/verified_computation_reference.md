# 2026-10-28 V3 final-results scope and evidence reuse

Retain the full gas-phase n=0,1,2 PAl12/B(C6F5)3 electron-acceptance family, its first/second ligand effects and electronic interpretation. Eight final propositions replace thirteen V2 nodes. Endpoint structures, contact counts and individual population/orbital projections become supporting evidence; the final explanation is separated into neutral-binding redistribution, acceptor stabilization and the specific shell-inference boundary. Neither mode requires a hidden spin/site grid or full angular-shell certification. PR retains the author PBE0/def2-SVP baseline and source AEA disclosure.

r_n0_electron_binding/r_n1_electron_binding/r_n2_electron_binding reuse SOURCE_COMPARISON.json and PAL_DIRECT_NATIVE_READBACK.json: lowest-supported AEA=1.9745564191/3.2191856338/3.9591693503 eV with own ZPE. r_first_ligand_affinity_gain/r_second_ligand_affinity_gain reuse increments +1.2446292147/+0.7399837164 eV. r_neutral_binding_redistribution reuses neutral Hirshfeld core +0.381449/+0.568455 e and full Al–B geometries; r_acceptor_stabilization reuses source-mapped alpha/beta/beta virtual levels -2.7556970851/-3.8120430992/-4.4060676610 eV plus full-fragment CDA contributions 26.45/68.06/35.66/16.61%. r_shell_scope reuses those limited projections and explicit full-fragment definitions; no complete angular-shell certification is claimed. Historical qualitative-with-numerical-deviation acceptance is retained, not relabelled strict or V3 full validation.

Evidence gaps / limits: Bare anion lower validated triplet gives AEA 1.9745564191 eV, +0.2145564191 above source 1.76; higher singlet gives 1.7591674124 but cannot be selected by source proximity; n2 AEA differs by +0.0291693503 eV from source 3.93 and has soft 2.5219/2.1650 cm^-1 modes; finite state/site search does not establish a universal global minimum; Selected CDA/level results do not certify all angular shells or universality across other cores; SI has no complete source Cartesian table

This edit performs no new calculation or scientific revalidation. Only scoring_rules.json defines current scoring. All historical text below is preserved verbatim; its PASS labels and earlier scoring policies are historical, not a new full V3 pass.

---

# PAl12 Lewis-acid ligation and electron acceptance: verified computation reference

## Current acceptance — 2026-10-20

**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**. Formal scoring is permitted for the unchanged bounded task. Original numerical gates have not been declared passed. No new quantum chemistry or HPC jobs were run during this scoring migration. This is a retrospective source/native verification, not an information-limited blind Agent experiment.

Current scientific scope: Full gas-phase n0/1/2 electron-acceptance family and a bounded local-binding electronic explanation; no graphene, other core, device or universal shell claim.

Current scoring is paper_science_v2: 100 points, independent binary intermediate and conclusion leaves, no process score or multiplier. AR retains method freedom; PR follows the disclosed baseline or substantiates an equivalent. The public contract is byte-frozen, including stale process/calibration wording; current private scoring supersedes those legacy evaluator statements.

## Molecular objects, states and disclosed method

Gas-phase full PAl12[B(C6F5)3]n for n=0,1,2, respectively13/47/81 atoms and neutral electron counts171/419/667; anions have172/420/668 electrons. Ligand is full neutral BC18F15 (34 atoms,248 electrons), not a truncated aryl group. AEA=(E+own ZPE)neutral−(E+own ZPE)anion at respective valid relaxed states; it is not a vertical affinity, LUMO energy or Gibbs energy. Lowest supported states must be selected from the actually investigated space, never by source-number proximity.

Source main physical pp2–4, Figs1–4 reportsAEA1.76/3.22/3.93eV and the local-binding interpretation. The actual SI is supplementary_001.docx, not a PDF: paragraphs5–6 contain computational details,8 contains Hirshfeld/ESP/MO/CDA,11/13/15/18/21 identify FigsS1/S2/S3/S4/S5. Paragraph numbers count all XML w:p elements. It discloses Gaussian16/PBE0/def2-SVP, spin/site searches, own-level frequencies and ZPE. No full source Cartesian table is provided. Source PAW/PBE-D3/AIMD, graphene and other cores are separate studies outside scope.

Actual calculations use Gaussian16 C.01 PBE1PBE=PBE0/def2SVP(5D,7F), UltraFine integration, Tight/XQC SCF and full gas-phase molecular objects. Neutral n0/n1/n2 retained states are doublets; n1/n2 retained anions are singlets, while the lowest validated n0 anion in the computed space is triplet. The valid n0 singlet is separately retained. Fragment-based neutral binding uses the full neutral PAl12 doublet171electrons and full neutral BC18F15 singlet248electrons, with frozen complex fragment geometry and a consistent basis convention in the CDA analysis. It is distinct from the one-electron neutral→anion comparison.

## Actual completed workflow and state ledger

The verifier constructed full objects, investigated finite spin/site alternatives, optimized neutral/anion structures, obtained same-level frequencies/ZPE, checked native state/stability evidence, calculated state-resolved AEA, and read neutral charges, frontier eigenvalues and full-fragment CDA. The original n0 singlet saddle had−16.8444cm−1; following both signs produced the same valid singlet basin. Those two directions do not constitute two independent ground states. The lower valid n0 triplet is retained. Full13/47/81-atom minima have33/135/237 positive modes.

| State/run | Charge | Multiplicity | Alpha/beta | E Eh | Own ZPE Eh | Minimum mode cm−1 | Native duration s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n0_doublet | 0 | 2 | 86/85 | -3248.25151875 | 0.01705 | 83.6026 | 267.1 |
| n0_quartet | 0 | 4 | 87/84 | -3248.19605288 | 0.015637 | 50.3111 | 1371.6 |
| n0_singlet_saddle | -1 | 1 | 86/86 | -3248.31541053 | 0.016255 | -16.8444 | 1049.2 |
| n0_singlet_plus | -1 | 1 | 86/86 | -3248.31541296 | 0.016296 | 23.8561 | 427.8 |
| n0_singlet_minus | -1 | 1 | 86/86 | -3248.31541296 | 0.016296 | 23.8741 | 398.0 |
| n0_triplet | -1 | 3 | 87/85 | -3248.32356936 | 0.016537 | 30.2938 | 3569.8 |
| n0_doublet_stable | 0 | 2 | 86/85 | -3248.25151875 | not a frequency run | stability-only | 217.4 |
| n0_quartet_stable | 0 | 4 | 87/84 | -3248.19605288 | not a frequency run | stability-only | 195.7 |
| n0_singlet_stable | -1 | 1 | 86/86 | -3248.31541296 | not a frequency run | stability-only | 147.8 |
| n0_triplet_stable | -1 | 3 | 87/85 | -3248.32356936 | not a frequency run | stability-only | 165.6 |
| n1_doublet | 0 | 2 | 210/209 | -5452.70268702 | 0.174374 | 4.438 | 13096.3 |
| n1_singlet | -1 | 1 | 210/210 | -5452.82050391 | 0.173888 | 4.6748 | 17689.7 |
| n2_doublet | 0 | 2 | 334/333 | -7657.13468088 | 0.331902 | 2.5219 | 65258.299999999996 |
| n2_singlet | -1 | 1 | 334/334 | -7657.27967667 | 0.331401 | 2.165 | 28469.3 |

The stability-only record has no Hessian; its false positive_curvature summary flag is not an imaginary-mode finding. Same-geometry n0 stability controls preserve coordinates and energies and report stable wavefunctions. Initial saddle and all valid singlet/triplet alternatives remain traceable. n2 low modes2.5219/2.1650cm−1 imply a soft structure and finite-search sensitivity; they are not silently discarded.

## AEA source comparison, including the actual lower n0 anion

Signed residual is actual minus source, absolute residual is its magnitude. AEA is an energy difference where relative discrepancy is meaningful as a diagnostic, but it is not an acceptance threshold.

| State pair | Source AEA eV | Electronic AEA eV | Own ZPE contribution eV | Actual AEA eV | Signed residual eV | Absolute residual eV | Relative diagnostic |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n0_doublet→n0_singlet_plus | 1.76 | 1.738650027190745 | 0.02051738522947489 | 1.75916741242022 | -0.0008325876 | 0.0008325876 | -0.047% |
| n0_doublet→n0_singlet_minus | 1.76 | 1.738650027190745 | 0.02051738522947489 | 1.75916741242022 | -0.0008325876 | 0.0008325876 | -0.047% |
| n0_doublet→n0_triplet | 1.76 | 1.960596977972665 | 0.013959441144191832 | 1.974556419116857 | +0.2145564191 | 0.2145564191 | +12.191% |
| n1_doublet→n1_singlet | 3.22 | 3.2059609001057834 | 0.013224733715550554 | 3.219185633821334 | -0.0008143662 | 0.0008143662 | -0.025% |
| n2_doublet→n2_singlet | 3.93 | 3.9455364457428788 | 0.013632904509239272 | 3.959169350252118 | +0.0291693503 | 0.0291693503 | +0.742% |

**Current actual lowest-supported series is1.9745564191/3.2191856338/3.9591693503eV.** The n0 singlet branch1.7591674124eV happens to approach source1.76 but is not selected as the lowest state. The triplet anion is lower by0.2219469508eV electronic, partly offset by−0.0065579441eV singlet-minus-triplet ZPE, giving0.2153890067eV lower E+ZPE. The source does not restrict n0 anion to singlet. This discrepancy remains and cannot be attributed wholly to software or dismissed using unrelated Al13 AEA/PAl12 AIP calibration. The actual AEA increments are+1.2446292147 and+0.7399837164eV; ligation enhancement persists with the lower triplet.

## Structural and electronic source comparisons

| Quantity/component | Source | Actual | Signed residual | Absolute residual | Unit |
| --- | --- | --- | --- | --- | --- |
| n2 neutral mean P-Al / two Al-B distances [1] | 2.63 | 2.6331789459949912 | +0.003178946 | 0.003178946 | angstrom |
| n2 neutral mean P-Al / two Al-B distances [2] | 2.51 | 2.5112164024944166 | +0.001216402 | 0.001216402 | angstrom |
| n2 neutral mean P-Al / two Al-B distances [3] | 2.51 | 2.513336910829108 | +0.003336911 | 0.003336911 | angstrom |
| n1 CDA core FO70 to alpha MO179 / MO180; ligand FO125 to alpha MO210 / MO203 [1] | 26 | 26.45 | +0.450000000 | 0.450000000 | percent |
| n1 CDA core FO70 to alpha MO179 / MO180; ligand FO125 to alpha MO210 / MO203 [2] | 68 | 68.06 | +0.060000000 | 0.060000000 | percent |
| n1 CDA core FO70 to alpha MO179 / MO180; ligand FO125 to alpha MO210 / MO203 [3] | 36 | 35.66 | -0.340000000 | 0.340000000 | percent |
| n1 CDA core FO70 to alpha MO179 / MO180; ligand FO125 to alpha MO210 / MO203 [4] | 17 | 16.61 | -0.390000000 | 0.390000000 | percent |
| source-marked neutral LUMO for n0/n1/n2 (alpha/beta/beta) [1] | -2.76 | -2.755697085131205 | +0.004302915 | 0.004302915 | eV |
| source-marked neutral LUMO for n0/n1/n2 (alpha/beta/beta) [2] | -3.81 | -3.8120430992004586 | -0.002043099 | 0.002043099 | eV |
| source-marked neutral LUMO for n0/n1/n2 (alpha/beta/beta) [3] | -4.41 | -4.406067660950377 | +0.003932339 | 0.003932339 | eV |

Source Fig4b marks the n0 alpha first virtual and n1/n2 beta first virtual. The reported matched series−2.7556970851/−3.8120430992/−4.4060676610eV follows those actual source arrows rather than whichever channel is closer. The alternative n0 beta value−2.7505269217eV is a different retained spin channel. LUMO energy is not AEA.

Neutral core Hirshfeld charges are+0.381449e(n1) and+0.568455e(n2), supporting electron redistribution toward ligands. Source text describes the one-ligand series up to about+0.36e and an increasing trend; plots are not promoted to invented exact PAl targets. The discrepancy is retained rather than claiming exact charge reproduction. Full-fragment CDA gives core FO70 contributions26.45/68.06% to alpha MO179/180 and ligand FO125 contributions35.66/16.61% to alpha MO210/203 versus source26/68/36/17%. Source2S/1G/1F labels are annotations, and these four projections do not certify all angular shells. Source Fig4 caption abbreviation does not justify truncating BC18F15.

## Recorded resources, timing and history

The state table gives recorded per-job native durations, not total elapsed project time. The inspected n0 triplet input requests4CPU threads and12GB; other requests are available in the linked native inputs and are not assumed equal. Complete cumulative allocation/queue time/peak memory/cost were not recorded here. No new quantum or HPC calculation was performed for this migration. Full previous root verification text is appended below without byte changes, including older numeric gates and failures that are historical rather than current formal-scoring blockers.

## Remaining limits

- The n0 source AEA1.76eV does not match the lower validated triplet-based1.9745564191eV. The near-source singlet remains an excited calculated alternative and is not selected by numerical proximity.
- Only the actually investigated spin/site space is bounded; no universal global-minimum or exact undisclosed source-coordinate reproduction is asserted. n2AEA residual+0.0291693503eV is retained.
- Neutral-fragment redistribution, LUMO shifts and CDA mixing support a local-binding explanation. They do not constitute neutral-to-anion attachment density, a full superatomic angular-shell certification, or universal shell-independent control.
- No numerical tolerance is constructed from the residuals; the source AEA, level and CDA values remain contextual, with explicit definitions and differences. Full13/47/81-atom family coverage is needed for whole-family inference.

## Auditable raw/source artifact inventory

| Artifact | SHA-256 |
| --- | --- |
| docs/strict_author_route_validation_20261001/advance_nojob_20261011T1742Z/papers/paper_c7217910ecbee1d9/NATIVE_OPT_MARKER_CORRECTION.json | 9db0496f6567590827ef3ff705ac12318e058ae96b8126e9cc454565872c2ac2 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W11/papers/paper_c7217910ecbee1d9/outputs/pal_state_reference_control_20261009_a01/state_reference_control.json | 8248124628b85f7007d92abd082a20af219bc7cb128dd40dc447adceafcc8938 |
| docs/strict_author_route_validation_20261001/all_unfinished36_20261011T0650Z/papers/paper_c7217910ecbee1d9/SOURCE_COMPARISON.json | cc7948b8f17f11e945982c84763cbd00e68c86289e3182c0865020ea26c0d6c2 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/strict_CDA_submenu_startup_repair/attempt_01/native_CDA.log | 1799253f3d3f73400fa1de117b0f16e03c23164a4ce013e8e44d37966904dae2 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_d_source_optfreq/attempt_01/gaussian.log | 051c9e052c002842ea41f29fc46b93254b0fffcc07aa7a9cdc721382cea19afb |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_q_source_optfreq/attempt_01/gaussian.log | 788d0870d28364b451472a36db5c02eb245965f32b1d38fa529451e8a070ebbe |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_source_optfreq/attempt_01/gaussian.log | 98d6f58f38c26695ea3d4ff52358ff696719993b343fd61edea7659101baa796 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_mode_plus_optfreq/attempt_01/gaussian.log | b05b32c1931a2809a991ecde922d80693f0187d72ace3e447a47df95e4d7f571 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_mode_minus_optfreq/attempt_01/gaussian.log | 56e4ff299fb6652bfeb7dcdd10ac081a862b90a4140535fae1447989b21cb0ee |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_t_source_optfreq/attempt_01/stdout.log | bd4e64efd40cbf9ded00567ca52a7a2619394f91ee8f7e53a8c2c2135d513f0c |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_d_stability/attempt_01/stdout.log | 82e165e6df1558ce9806595eef7bda4b7d59279f4f8d90e4f3a4b179a6b34d03 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_q_stability/attempt_01/stdout.log | a7accddc461886f96cba223068aa31ee8b40676d0ecf3edda260de93ded8263d |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_recovered_stability/attempt_01/gaussian.log | 4c4e9f9061c3075bdde6878041aec181ef76712f274ceffe0f815ed12e9763c3 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_t_recovered_stability/attempt_01/stdout.log | 002dd31acf00625a4bf971f58c8961d5cbec5cbb0885ea3e31919add366a1541 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n1_neutral_d_source_optfreq/attempt_01/gaussian.log | 414a08f684f61c989dcf388d425df85ccf840db7c88d948b97402596d417ba69 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n1_anion_s_free_from_stable_vertical/attempt_01/gaussian.log | 207a180b180fb3260b9d2548a0dbce941b5dc0a468ab016df88ff6f7a336d05e |
| docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/stdout.log | fed8f6c4c9db933546a3347985b5e6a66191560ab638631ba2c208e37a54d5b0 |
| docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/stdout.log | 2e6a023a1ea77881664309e08d1ba227180db0ad6a2d34fcd7313e63dc68b02a |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_d_source_optfreq/attempt_01/input.com | a9dfcc3f434ce3a29c8e17d6f489a920d1720431cb90036ae69fc5b595e30b03 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_q_source_optfreq/attempt_01/input.com | 97bc00a924bc73c9e0e0030b56884024c8e61cd9bc74e8e6ccfe779152a155c1 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_source_optfreq/attempt_01/input.com | acca87b18e147ec98529949efdbf1d7e9bbd8602470ef68c3cbfafaab97dbd8f |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_mode_plus_optfreq/attempt_01/input.com | 9e5dfd8f741239da76b7b77ebef5e37c5e033403a0648ab35d6b0ed4e8232583 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_mode_minus_optfreq/attempt_01/input.com | 78c296946309b9b0babfe3873b734d01344cb680bd62ced35335a494a6449df0 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_t_source_optfreq/attempt_01/input.com | 24710037805a79fad5eb14c8f69448c7ff095447b8213f11eeb54799858b8e81 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_d_stability/attempt_01/input.com | 93d632d45de8c082b03c62090de65977a06767cc619d025990a1c7e3ae6cb0b9 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_neutral_q_stability/attempt_01/input.com | a0497d92ae281bc344e973a238d3606a2f82dcdbe7ed5d6902f09c7ee1c5a226 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_s_recovered_stability/attempt_01/input.com | 45df02da1dd04d085a1ec6d6a13fb2ac3119a7783e17d0e13cf4bc993924221e |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n0_anion_t_recovered_stability/attempt_01/input.com | 499941f1eeba9b45596907e9f07af43ff93dda620b80b2078d9f46a7d9dea748 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n1_neutral_d_source_optfreq/attempt_01/input.com | 868c00cf702a2b40e533f13aa28ce04ce9f07103d19453de7bc18dc69992017e |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n1_anion_s_free_from_stable_vertical/attempt_01/input.com | c382b8c502c55b26c6ab1cb078d0abeedcefa39c25122eec8ac540aa5f1ee434 |
| docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/input.com | 1aecd5cc036ed22f12c636d0876d176cf85de2bfdb93156c0fa935d26438ebe0 |
| docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/source_input.com | 1aecd5cc036ed22f12c636d0876d176cf85de2bfdb93156c0fa935d26438ebe0 |
| docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/input.com | 3c0971209c03e0af9f4c367d5454ba99be158e955c7125dc4031aef7d96f34b7 |
| docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/source_input.com | 3c0971209c03e0af9f4c367d5454ba99be158e955c7125dc4031aef7d96f34b7 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n2_neutral_source_stability/attempt_01/gaussian.log | fa739b91e8ac96ffe3853be97c50e7b1a6bc666dd39e293d2eaebfd8943394f7 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/n2_neutral_source_stability/attempt_01/input.com | fdce5417acaabb4fb9df65d8e7437ba90d6c5345e3c6d25b2b451101dcab0df2 |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/v2_n2_free_opposite_anion_checkpoint_stability/attempt_01/gaussian.log | af4c9a493367cf39020c1963cd13ac4298bab2b2a22766cfbb82fd08873e287c |
| docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/outputs/v2_n2_free_opposite_anion_checkpoint_stability/attempt_01/input.com | e31d51d4e51169f4d0fdd0ff300d2e86e925826f60056299446d59e6107b4376 |
| docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_c7217910ecbee1d9/ACTION_RESULT.json | cf60532b4946aba7aa128114365ef184bc6490a97c21deba56e639a7c3205da3 |
| docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_c7217910ecbee1d9/RAW_NATIVE_READBACK.json | 0b8880339a47b8c7fcca786db26b463951ec63ef54c0a2f0a804d08259341e05 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W11/papers/paper_c7217910ecbee1d9/outputs/pal_state_reference_control_20261009_a01/state_reference_control.json | 8248124628b85f7007d92abd082a20af219bc7cb128dd40dc447adceafcc8938 |
| docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_c7217910ecbee1d9/NATIVE_PARAMETER_READBACK.json | 808bd395e3f6b64466ac00a2418f6e6a9af71569421572f1292916f02d5b4c92 |
| docs/v2_verification/maintenance/qualitative_acceptance_review_20261020/PAL_DIRECT_NATIVE_READBACK.json | 45e9887e35197ab82b0df5ba3b4e4d627c9c52422b1a2f8d3284f995ddfe9fd0 |

## Preserved earlier reference

# V2 reference boundary — not scientifically certified

There are authentic full-size historical n2 DFT candidates and selected later vertical/density records. The old claim that no intact DFT object exists is not a current blocker. Existing records support bounded feasibility and conditional comparisons; expanded scientific references, uncertainty and semantic acceptance remain uncalibrated. Source AEA values and source shell assignments are not mandatory answers.

The original-final and V1 snapshots preserve history only. Their PASS labels and matrices are not V2 acceptance rules. The task accepts well-supported non-author routes and refutations; evidence sufficiency is evaluated for the submitted claims. No new quantum calculation or universal tolerance was produced by this content upgrade.

## Repair boundary (2026-09-30)

Reuse existing full-size opt/frequency and energy outputs only with their actual n, charge, multiplicity, geometry and reference definitions. The selected n1-anion stationarity log is locally useful, but positive modes at one endpoint do not establish the lowest state, all n=0/1/2 electron acceptance or the neutral-binding explanation. Preserve the observed lower triplet n0 anion versus a source-like singlet as a comparison requiring interpretation. Future validation must justify composition/state/structure coverage, attachment definitions and relevant uncertainty, and test the stated electronic explanation. A source-neutral binding explanation needs evidence for neutral fragments/complexes; attachment density alone is insufficient. CDA is conditional on the analysis claimed, with complete fragments and explicit conventions; no new hidden control grid is imposed. The SI does not supply complete Cartesian coordinates, so reconstructed starts remain reconstructions.

Dated raw-artifact hashes are recorded in task_provenance/integrity_repair_20260930.json. No new scientific calculation was performed; the whole revised question remains unvalidated.


## Historical reference text — non-current, preserved verbatim

Original location: legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot. Historical PASS/pending, numeric windows, search matrices and scoring prescriptions below are not the current scientific scoring policy.

# 已验证成功计算参考 — paper_c7217910ecbee1d9 / paper_reproduction

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 2）

正文及 SI DOCX Computational details 的 PAl12[B(C6F5)3]2 对象和 PBE0/def2-SVP 路线。

[论文正文](../../../../papers/paper_c7217910ecbee1d9/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/report/results.json)。
[补充材料 supplementary_001.docx](../../../../papers/paper_c7217910ecbee1d9/documents/supplementary_001.docx)

## 2. 真实有效计算流程

1. 完整对象 PAl12B2C36F30，共 81 原子。构建两种配位位置/取向（opposite、obtuse），每种中性取 doublet/quartet、阴离子取 singlet/triplet，共八个候选；不是 52 原子简化模型。
2. Gaussian16 PBE0/def2-SVP 气相 Opt/Freq，对八候选均取得完整 237 模、无虚频结果，保留同电荷/自旋下去重、能量和配体连接检查。一条脱离接触的候选没有作为所选 endpoint。
3. 各电荷态分别取最低 E+ZPE：opposite 中性 doublet E=−7657.13468088/ZPE=.331902 Eh；opposite anion singlet E=−7657.27967667/ZPE=.331401 Eh。AEA=(E0neutral−E0anion)×27.211386245988=3.959169350 eV；纯电子值 3.945536446 eV。
4. 检查所选两态的 P–Al、30 条 Al12 icosahedral 边、Al–B 接触、两配体和 30 个 C–F 键，支持框架保留与 3.93±0.30 eV 的 AEA 比较。结构框架保留不伪称完整 superatomic 电子壳层分析。

## 3. 有效产物与原始输入/输出

- [provenance/final_closure_20260919/independent_results.json](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/final_closure_20260919/independent_results.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m1_nonclashing_optfreq_20260916_20260917T033059Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m1_nonclashing_optfreq_20260916_20260917T033059Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m1_nonclashing_optfreq_20260916_20260917T033059Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m3_nonclashing_optfreq_20260916_20260917T045136Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m3_nonclashing_optfreq_20260916_20260917T045136Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m3_nonclashing_optfreq_20260916_20260917T045136Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m2_nonclashing_optfreq_20260916_20260917T024030Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m2_nonclashing_optfreq_20260916_20260917T024030Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m2_nonclashing_optfreq_20260916_20260917T024030Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m4_nonclashing_optfreq_20260916_20260917T040114Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m4_nonclashing_optfreq_20260916_20260917T040114Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m4_nonclashing_optfreq_20260916_20260917T040114Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_anion_m3_nonclashing_optfreq_20260916_20260917T033053Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m3_nonclashing_optfreq_20260916_20260917T033053Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m3_nonclashing_optfreq_20260916_20260917T033053Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m4_nonclashing_optfreq_20260916_20260917T021003Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m4_nonclashing_optfreq_20260916_20260917T021003Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m4_nonclashing_optfreq_20260916_20260917T021003Z/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `pr_process_minimum` | The report identifies independently optimized neutral and anion endpoints and supplies frequency or equivalent stationary-point validation plus candidate coverage. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_process_aea_definition` | AEA is formed from the adiabatic neutral/anionic endpoint energies with an explicit unit and zero-point convention. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_result_aea` | The isolated PAl12[B(C6F5)3]2 endpoint has a source-reported AEA of 3.93 eV. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_result_framework` | The ligated cluster retains the PAl12 metal-core structural framework after optimization within the stated model boundary. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_final_claim` | Within the submitted method and searched coverage, the validated adiabatic electron affinity of PAl12[B(C6F5)3]2 is consistent with the paper endpoint and the report distinguishes computed evidence from global-minimum claims. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

完整 site/spin 有限链支持现有 AEA 与结构框架目标，不要求全球构象穷举或未评的 AIMD。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。


## Historical reference text — non-current, preserved verbatim

Original location: legacy_v1_snapshot/evaluation/verified_computation_reference.md.snapshot. Historical PASS/pending, numeric windows, search matrices and scoring prescriptions below are not the current scientific scoring policy.

# Historical reference boundary

The exact previous file is retained at `legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot`. It describes the old scalar scope only and is NOT an expanded reference.

The 2026-09-27 verification inventory recovered eight historical Gaussian PBE0/def2SVP n2 local-minimum candidates with 81 atoms and 237 positive frequencies. An independent supervisor parse checks raw log/input hashes, stationarity, the P-centered icosahedral Al12 adjacency and both element-labelled ligand graphs. The selected opposite-site neutral doublet and anion singlet retain the complete object; their electronic AEA is 3.9455364457428788 eV and ZPE-corrected AEA is 3.959169350252118 eV. These are historical baseline values, never expanded acceptance targets or tolerances. Native atom order differs from the public map; use the explicit graph mapping in task_provenance/historical_n2_reaudit.json. Other local minima include long Al-B contacts and require candidate-specific attachment interpretation. No global-minimum or shell-orbital claim follows. The later AR GFN2 reconstructed aggregate and unconverged PBEh-3c runs remain invalid intact endpoints, but do not erase the earlier valid Gaussian evidence. The full expanded reference remains pending.

Current status: implemented_pending_expanded_reference; expanded reference not validated. See `reference_validation_plan.md` and `task_provenance/source_review.json`. No new scientific reference calculations.
