# 2026-10-28 V3 scope and evidence reuse

Retain the original local TEA/DED/BF4–PC question and its qualitative acceptance boundary. Explicitly define the 1:1 gas-phase relaxed-fragment electronic observable. Score three independent attractive signs, two pairwise strength comparisons and one conditional solvent-competition interpretation; structures, frequencies and balanced subtraction support these final results without separate points. Both modes share six outcomes and weights; PR retains its disclosed two-layer author baseline.

- `r_association_tea`: TEA+–PC electronic binding relative to relaxed separated molecules; evidence: pc_main, pc_si, native_pc_decomposition, native_validation, validation_summary_3.
- `r_association_ded`: DED2+–PC electronic binding relative to relaxed separated molecules; evidence: pc_main, pc_si, native_pc_decomposition, native_validation, validation_summary_3.
- `r_association_bf4`: BF4−–PC electronic binding relative to relaxed separated molecules; evidence: pc_main, pc_si, native_pc_decomposition, native_validation, validation_summary_3.
- `r_ded_vs_bf4`: Relative local PC binding of DED2+ and BF4−; evidence: pc_main, pc_si, native_pc_decomposition, native_validation, validation_summary_3.
- `r_bf4_vs_tea`: Relative local PC binding of BF4− and TEA+; evidence: pc_main, pc_si, native_pc_decomposition, native_validation, validation_summary_3.
- `r_local_competition_account`: Conditional molecular explanation of the changed local PC environment; evidence: pc_main, pc_si, native_pc_decomposition, native_validation, validation_summary_3.

Known limits: Historical acceptance was qualitative with numerical deviation, not a strict numerical PASS: TEA/DED/BF4 binding differs from source by +4.2726/+5.4013/+3.5492 kcal/mol (24.47/15.22/17.67 percent); Exact source conformers and subtraction convention were not fully disclosed; frozen-fragment deformation does not explain all magnitude offsets; CP/BSSE correction was not calculated; Gaussian source A.01 versus native C.01 is a historical authorized version exception, not an established cause of deviation; Local gas-phase evidence does not identify bulk populations, concentration nonmonotonicity, a 0.2 M optimum or electrode/device properties; No new V3 calculation, blind run or judge calibration. No new calculation or V3 scientific PASS is asserted. All text below is preserved historical evidence, including obsolete scoring statements; the active V3 JSON files govern scoring.

---

# Current computational verification and scoring reference — 2026-10-20

Acceptance: **ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**. The coordinator-approved scope has sufficient valid computations and matching key qualitative nodes/conclusions. Original strict numerical gates are not relabelled as passed. This acceptance does not assert exact historical inputs, whole-paper reproduction, blinded autonomous success or an online Judge score.

Current scoring: paper_science_v2, 100 fixed binary points, intermediate and final conclusions; formal_scoring_permitted=true. Publication/expert review remains separate and is not a runtime scoring freeze. The unchanged public PR contract continues to govern baseline reproduction or justified substitution, while AR chooses methods. Public legacy wording about process assessment is retained byte-for-byte but confers no process score.

## Scientific objects, conditions and completed verification

Complete TEA+, bridged DED2+, BF4− and PC; local single-PC finite models with balanced references. No bulk MD,0.2M optimum, electrode or device claim is a score target.

TEA+=C8H20N+, DED2+=C10H22N2(2+) with the bridged doubly quaternized graph, BF4− and PC=C4H6O3; closed-shell singlet fragments and same-charge single-PC complexes. Gas-phase finite clusters; source does not identify one PC stereoisomer or full historical configurations.

Disclosed/implemented route: Gaussian16, B3LYP-D3BJ/def2-SVP geometry optimization and harmonic frequencies, followed by B3LYP/6-311+G(2d,p) electronic single points without silently carrying D3BJ to the stated binding SP. Installed C.01 versus source A.01 falls under the existing version exception, not a proof that version caused the residual. Electrode B3LYP-D3BJ/def2-TZVP, frontier B3LYP/6-311G** and GROMACS/GAFF/RESP are separate source protocols outside this local scoring target.

Completed sequence: graph/charge-map four monomers and three complexes; retain converged monomer and several orientation Opt/Freq endpoints; inspect positive curvature and normal termination (12 existing Opt/Freq logs in the retained readback); use same-layer relaxed monomer SP energies for electronic binding; independently retain frozen-fragment interaction/deformation cycle and a distinct DED d orientation. No bulk simulation or new quantum calculation is submitted here.

The baseline Eb is E(complex)−E(relaxed ion)−E(relaxed PC). Author Fig2d supplies energies but no explicit subtraction formula or full source conformers; this standard balanced definition is reconstructed and its limitation is retained. Source absolute values are not replaced by the frozen-fragment interaction or best numerical endpoint.

### Ion–PC binding energies

| ion | source Fig2d | actual relaxed-binding | actual−source | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| TEA | -17.46 | -13.18740276 | 4.272597238 | 4.272597238 | kcal/mol |
| DED | -35.49 | -30.08872662 | 5.401273379 | 5.401273379 | kcal/mol |
| BF4 | -20.09 | -16.54081088 | 3.549189119 | 3.549189119 | kcal/mol |


### Meaningful relative magnitude discrepancies

| ion | absolute deviation / absolute(source) (%) |
| --- | --- |
| TEA | 24.47077456 |
| DED | 15.21914167 |
| BF4 | 17.66644658 |


### Same-layer electronic energy components (Eh)

| ion | complex | relaxed ion | relaxed PC | frozen ion | frozen PC |
| --- | --- | --- | --- | --- | --- |
| TEA | -753.3950061 | -371.5285164 | -381.8454743 | -371.5282991 | -381.8448173 |
| DED | -885.2402612 | -503.3468375 | -381.8454743 | -503.3458183 | -381.8427395 |
| BF4 | -806.5654602 | -424.6936264 | -381.8454743 | -424.6933187 | -381.8448568 |


### Additional reference-cycle diagnostic (kcal/mol)

| ion | relaxed binding | frozen interaction | ion deformation | PC deformation | closure error |
| --- | --- | --- | --- | --- | --- |
| TEA | -13.18740276 | -13.73598723 | 0.136345886 | 0.4122385839 | 1.33226763e-15 |
| DED | -30.08872662 | -32.44439656 | 0.639560166 | 1.716109772 | 3.552713679e-15 |
| BF4 | -16.54081088 | -17.12140649 | 0.1931235707 | 0.38747204 | 1.110223025e-16 |


### Balanced PC transfer TEA·PC+DED→TEA+DED·PC

| quantity | derived from source pair values | derived from actual pair values | actual−source | absolute deviation | unit |
| --- | --- | --- | --- | --- | --- |
| electronic transfer energy | -18.03 | -16.90132386 | 1.128676141 | 1.128676141 | kcal/mol |

All three Eb values are attractive, with |Eb(DED)|>|Eb(BF4)|>|Eb(TEA)|. The balanced transfer favors DED in this local model; this supports the conditional local competition account without claiming equilibrium bulk populations. The retained DED d endpoint is slightly lower (about−30.0950808kcal/mol), preserving direction; it is a distinct computed configuration, not substituted into the author-like baseline to make the source closer. Deformation does not account for all residuals; no CP correction was computed, so deformation is not called BSSE correction.

Not reproduced/not scored: exact absolute binding magnitudes, unique historical source conformer/reference, MD solvation populations/RDFs, concentration reversal or0.2M optimum, electrode adsorption, electrochemical window, device energy/power. Do not infer these from a finite complex or orbital gap.

## Rule design and tolerance boundary

No numerical leaves. The source does not supply exact starting conformers or an explicit binding-energy subtraction definition; observed magnitude offsets do not justify a residue-fitted tolerance. Three attraction signs, two independent strength comparisons and a bounded local mechanistic synthesis are supported.

Evidence eligibility is checked per item; no independent points for software, convergence logs, report completeness or generic limitations. Wrong physical identity invalidates the affected result even if a number hits a window. Final inference must be explicitly supported in the submitted deliverable.

## Source location and independent readback

- papers/paper_c28b0a1c549f4575/documents/main.pdf; SHA256 4e3ad96c28503f3a100df2083569811eef0ee848ae6aca2def236523628f8909; 1-based PDF pages 3,4; Text and Fig2d local ion–PC binding.
- papers/paper_c28b0a1c549f4575/documents/supplementary_001.pdf; SHA256 51551c36ef22b1633c2ee346411edf4c5b5f3ec9edd9ea1ce7e923c011387546; 1-based PDF pages 5,6; Computational details, separate association/adsorption/frontier/MD protocols.

### Existing validation/analysis summaries (separate from primary sources)

- docs/strict_author_route_validation_20261001/advance_remaining_20261012T1245Z/papers/paper_c28b0a1c549f4575/ACTION_RESULT.json; SHA256 c355ee9ad7fe9930eed6d670294bd1fd7c3250c31296bb8d2716628ff42abd84. Historical status labels in these unchanged files are retained; current acceptance above supersedes them.
- docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_c28b0a1c549f4575/PARAMETER_READBACK.json; SHA256 bc1345d4956a10b81792733521714470ef366de1bd7595e2c56e8b1ee32ff287. Historical status labels in these unchanged files are retained; current acceptance above supersedes them.
- docs/v2_verification/maintenance/qualitative_acceptance_review_20261020/PC_DIRECT_FREQUENCY_READBACK.json; SHA256 4617166cea074c82283074dc65fed75e3d65dbbc9740c0911c8df7b8bdc5c756. Historical status labels in these unchanged files are retained; current acceptance above supersedes them.

## Native artifact index, real resources and completeness

Paths below are workspace-relative on the shared server. They identify actual existing inputs/outputs; this migration only reads and hashes them. Normal termination alone does not establish the right molecule/state. Any errors or reused frequency-only recoveries remain in the index and are not erased. Resource lines are the individual logs’ recorded quantities; absent/all-job wall time and CPU cost are **not recorded as a reliable total** and are not inferred from allocations.

- docs/strict_author_route_validation_20261001/reopen_excluded6_20261011T0615Z/papers/paper_c28b0a1c549f4575/cases/w12_c28b_retained_d_author_sp_20261011_a01/gaussian.log; SHA256 09bb2e5d5c9427e39ca1b09d762e5e8d0a0a45cc8acf6873ba59f00493db27f5; 94475 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -885.240271336     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 36 minutes 37.6 seconds.", "Elapsed time:       0 days  0 hours  9 minutes 11.2 seconds.", "Normal termination of Gaussian 16 at Sun Oct 11 07:03:06 2026."]
- docs/strict_author_route_validation_20261001/reopen_excluded6_20261011T0615Z/papers/paper_c28b0a1c549f4575/cases/w12_c28b_retained_d_author_sp_20261011_a01/input.com; SHA256 4836faea218dd28813df37f135aefeb7069c5e2b62a13dafe1efed94f97cead3; 1626 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=4", "%Mem=8GB"]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_BF4_frozen_PC_reference_chain_timestamp_fix/attempt_01/PC/gaussian.log; SHA256 d6e6d21285b68173716cf73ebe67678cea49c53bb13916e8177ea50fc7bb787a; 35230 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -381.844856805     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  1 minutes  1.1 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 19.8 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 07:02:57 2026."]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_BF4_frozen_PC_reference_chain_timestamp_fix/attempt_01/PC/input.com; SHA256 2271b18f5623c77c0d21c38ff33e992e2e66311e51b448790750bdf7b0e0ca42; 570 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) SP NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%mem=12GB", "%nprocshared=4"]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_BF4_frozen_PC_reference_chain_timestamp_fix/attempt_01/ion/gaussian.log; SHA256 406265391ee0763a7973fff865d7d8c3f8bad7588c53d90eab1a9c782363e7c7; 26312 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -424.693318658     A.U. after   10 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  0 minutes 13.5 seconds.", "Elapsed time:       0 days  0 hours  0 minutes  4.1 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 07:02:37 2026."]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_BF4_frozen_PC_reference_chain_timestamp_fix/attempt_01/ion/input.com; SHA256 dec315858dd2732d8a811ef1fc6b72bc3f6421ce83e5ad43d0d6b296df7a873b; 332 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) SP NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%mem=12GB", "%nprocshared=4"]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_DED_frozen_PC_reference_chain_timestamp_fix/attempt_01/PC/gaussian.log; SHA256 5fd5e1d3f198969b184ef972d0131c59f49f5e08a733afcd2ee65433632fc341; 35085 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -381.842739486     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  1 minutes  6.1 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 22.2 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 07:05:45 2026."]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_DED_frozen_PC_reference_chain_timestamp_fix/attempt_01/PC/input.com; SHA256 c721e343d27d53d22ac87eb77e06d849c2ad3855e40e30358a6773bcc3426054; 572 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) SP NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%mem=12GB", "%nprocshared=4"]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_DED_frozen_PC_reference_chain_timestamp_fix/attempt_01/ion/gaussian.log; SHA256 387f163005e1dd3f1a8e45ef51e8ef1f9c8834c564c1b7cdf7b38ddd6ff435fe; 64438 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -503.345818287     A.U. after   11 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 11 minutes 34.2 seconds.", "Elapsed time:       0 days  0 hours  2 minutes 59.2 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 07:05:22 2026."]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_DED_frozen_PC_reference_chain_timestamp_fix/attempt_01/ion/input.com; SHA256 e34183780697931c0843a2521503ead9dff9eb8ba7af997dfee0bd91b4e82f89; 1223 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) SP NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%mem=12GB", "%nprocshared=4"]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_TEA_frozen_PC_reference_chain_timestamp_fix/attempt_01/PC/gaussian.log; SHA256 e78c15ff0511461373c635c3ce1c54c2f67d4731f2bc5c56ca664b215f7425ba; 35040 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -381.844817337     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  0 minutes 58.1 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 19.1 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 07:03:25 2026."]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_TEA_frozen_PC_reference_chain_timestamp_fix/attempt_01/PC/input.com; SHA256 8b5c6146251e31a66006189cd4653128c48d551287a5c98b5920f61fbe1573e2; 566 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) SP NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%mem=12GB", "%nprocshared=4"]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_TEA_frozen_PC_reference_chain_timestamp_fix/attempt_01/ion/gaussian.log; SHA256 6fa4d0c8cc654cbb8e269a39a0ba2f3aa17f17e28c2f82f1ed91465b6f781d77; 55037 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -371.528299121     A.U. after   11 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  5 minutes 49.1 seconds.", "Elapsed time:       0 days  0 hours  1 minutes 31.5 seconds.", "Normal termination of Gaussian 16 at Fri Oct  2 07:03:06 2026."]
- docs/upgrade_tasks_verification/group_6/papers/paper_c28b0a1c549f4575/outputs/author_route_TEA_frozen_PC_reference_chain_timestamp_fix/attempt_01/ion/input.com; SHA256 1ba5603d2d7a4daf6205658b9ace3dfeb5cab6e41b96ac9524b6a6fa32e5e972; 1061 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) SP NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%mem=12GB", "%nprocshared=4"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/bf4_monomer_optfreq/input.com; SHA256 57f8785593811b5ddf866cd0202ad139917d723f910f6c2cbc469e22e1cf6754; 430 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=2", "%Mem=8000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/bf4_monomer_optfreq/stdout.log; SHA256 d7bc471a2a07870ae1b68d7c8feb7b8b9361027fe169a05c2f72ee454c45233b; 130708 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -424.198829720     A.U. after    1 cycles"]
  frequencies: {"count": 9, "minimum_cm1": 352.0216, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  0 minutes 27.2 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 18.1 seconds.", "Normal termination of Gaussian 16 at Sat Aug 29 23:18:51 2026.", "Job cpu time:       0 days  0 hours  0 minutes 25.3 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 13.3 seconds.", "Normal termination of Gaussian 16 at Sat Aug 29 23:19:06 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/bf4_pc_orientation_a_author_optfreq/input.com; SHA256 d9b886dbfba3879fa8cd3f3b27c288a66af3e799ed0e060d3362b0b1e66f6c75; 1012 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=4", "%Mem=24000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/bf4_pc_orientation_a_author_optfreq/stdout.log; SHA256 9e73981a6ea48749eae1aa1595443d69f2c0fac35c318360a480934b1f96d8d4; 2377485 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -805.696181189     A.U. after    1 cycles"]
  frequencies: {"count": 48, "minimum_cm1": 25.6032, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  1 hours 54 minutes 59.9 seconds.", "Elapsed time:       0 days  8 hours 38 minutes 18.9 seconds.", "Normal termination of Gaussian 16 at Fri Sep  4 01:59:35 2026.", "Job cpu time:       0 days  0 hours  9 minutes 12.7 seconds.", "Elapsed time:       0 days  0 hours 31 minutes 40.8 seconds.", "Normal termination of Gaussian 16 at Fri Sep  4 02:31:25 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/bf4_pc_orientation_b_author_optfreq/input.com; SHA256 188d5be63200994bc4004bb19f15e6546912c159c336d0de0645eee693180932; 1009 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=4", "%Mem=24000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/bf4_pc_orientation_b_author_optfreq/stdout.log; SHA256 9e304672b55ce7bb40918d6f8e96ed8b44504fce0e86de45102fedc8d156655f; 2838773 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -805.696175678     A.U. after    1 cycles"]
  frequencies: {"count": 48, "minimum_cm1": 25.0227, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  2 hours 16 minutes 22.3 seconds.", "Elapsed time:       0 days  3 hours 40 minutes 11.8 seconds.", "Normal termination of Gaussian 16 at Thu Sep  3 20:59:02 2026.", "Job cpu time:       0 days  0 hours  9 minutes 14.8 seconds.", "Elapsed time:       0 days  0 hours 13 minutes 53.0 seconds.", "Normal termination of Gaussian 16 at Thu Sep  3 21:12:58 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_monomer_optfreq/input.com; SHA256 c5e5eab6a229dd17a1d3ca1025725606d4f3d4d45f87a4730a23016c7122204e; 1664 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=2", "%Mem=8000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_monomer_optfreq/stdout.log; SHA256 15770063b2762838120501911f706a77ecdee333262c95c070b5f568c2b8e195; 1746174 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -502.903682523     A.U. after    1 cycles"]
  frequencies: {"count": 96, "minimum_cm1": 90.5735, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  1 hours 23 minutes 11.2 seconds.", "Elapsed time:       0 days  0 hours 44 minutes  3.0 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 00:02:55 2026.", "Job cpu time:       0 days  0 hours 36 minutes 34.6 seconds.", "Elapsed time:       0 days  0 hours 18 minutes 20.2 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 00:21:17 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_pc_orientation_a_optfreq/input.com; SHA256 5fc7b76121f92c6b3f655e61d6857f4787279056ab69df667660a6fcbc62a80b; 2231 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=4", "%Mem=24000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_pc_orientation_a_optfreq/stdout.log; SHA256 882e05046c6b829516796843654e0b0c1739732a0b63cd1479e21aa3794f3a5f; 9326964 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -884.417921872     A.U. after    1 cycles"]
  frequencies: {"count": 135, "minimum_cm1": 11.4863, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days 21 hours 39 minutes 42.9 seconds.", "Elapsed time:       2 days  4 hours 50 minutes 38.8 seconds.", "Normal termination of Gaussian 16 at Tue Sep  1 03:40:06 2026.", "Job cpu time:       0 days  1 hours 44 minutes 30.4 seconds.", "Elapsed time:       0 days  2 hours 56 minutes  9.3 seconds.", "Normal termination of Gaussian 16 at Tue Sep  1 06:36:22 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_pc_orientation_c_corrected_optfreq/input.com; SHA256 74bf3bb2b108ce44a84f28a4a188958fa2060f948f12cf2a56504445135163c4; 2252 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=4", "%Mem=24000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_pc_orientation_c_corrected_optfreq/stdout.log; SHA256 e9975ee332b1598f7d7871bd02be400cd86080f94dc5a449e1c43bbfbddea6a6; 7145279 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -884.418425648     A.U. after    1 cycles"]
  frequencies: {"count": 135, "minimum_cm1": 5.358, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days 17 hours 24 minutes 49.3 seconds.", "Elapsed time:       0 days 19 hours 44 minutes 57.4 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 18:56:02 2026.", "Job cpu time:       0 days  1 hours 42 minutes 17.9 seconds.", "Elapsed time:       0 days  1 hours 28 minutes 13.7 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 20:24:19 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_pc_orientation_d_corrected_optfreq/input.com; SHA256 9c26578b87fb48910eb3549b133c265fb4382dd88459c2c593d9dc7282cd9d0d; 2247 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=4", "%Mem=24000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/ded2_pc_orientation_d_corrected_optfreq/stdout.log; SHA256 1ed84a359f7410df31b768ba8741d1b4889cb1be05c33433a3ba411a448356af; 5263150 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -884.417950026     A.U. after    1 cycles"]
  frequencies: {"count": 135, "minimum_cm1": 9.9075, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  9 hours 56 minutes 41.6 seconds.", "Elapsed time:       0 days  3 hours 36 minutes 30.4 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 02:46:40 2026.", "Job cpu time:       0 days  1 hours 44 minutes 43.3 seconds.", "Elapsed time:       0 days  0 hours 52 minutes 36.8 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 03:39:20 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/pc_monomer_optfreq_retry_resources/input.com; SHA256 e7bfab71132c1cc7c1bac218d41022ab1b174d00861ca235a5c4793e74579ac7; 797 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=1", "%Mem=4000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/pc_monomer_optfreq_retry_resources/stdout.log; SHA256 55afe4c5e3ebe9be42e732cf8743a16645b2894fb914e0b077515f574a1e4ae3; 417598 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -381.455105114     A.U. after    1 cycles"]
  frequencies: {"count": 33, "minimum_cm1": 102.769, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  4 minutes 54.7 seconds.", "Elapsed time:       0 days  0 hours 52 minutes 35.0 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 20:18:48 2026.", "Job cpu time:       0 days  0 hours  3 minutes 12.6 seconds.", "Elapsed time:       0 days  0 hours 37 minutes 20.0 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 20:56:12 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/tea_monomer_optfreq/input.com; SHA256 8c58d38370d319ec89f09ad1e87c0d69bc1322faa0b27802de572bc35fe6c375; 1451 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=2", "%Mem=8000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/tea_monomer_optfreq/stdout.log; SHA256 3fecf5d6ea6fb152c43b1417134ffc8ffe8071eb52fe87225aeb59600c67b3a9; 814048 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -371.195799611     A.U. after    1 cycles"]
  frequencies: {"count": 81, "minimum_cm1": 93.3936, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 23 minutes 32.1 seconds.", "Elapsed time:       0 days  0 hours 46 minutes  8.5 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 00:04:55 2026.", "Job cpu time:       0 days  0 hours 22 minutes  4.8 seconds.", "Elapsed time:       0 days  0 hours 42 minutes 11.1 seconds.", "Normal termination of Gaussian 16 at Sun Aug 30 00:47:08 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/tea_pc_orientation_b_author_optfreq/input.com; SHA256 dd4a1984bda9dd5187b6c2337f599aab2e25460226b02482a827f08872d5012c; 2031 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq"]
  input_resources: ["%NProcShared=4", "%Mem=24000MB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/artifacts/gaussian_batch/tea_pc_orientation_b_author_optfreq/stdout.log; SHA256 7a85f886f2e5cd2eec7f757b60e7415784470e385b3787b42fa9f1005eedb233; 4991817 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -752.680882551     A.U. after    1 cycles"]
  frequencies: {"count": 120, "minimum_cm1": 12.07, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  8 hours 46 minutes 24.8 seconds.", "Elapsed time:       0 days 11 hours 20 minutes 25.9 seconds.", "Normal termination of Gaussian 16 at Fri Sep  4 04:41:43 2026.", "Job cpu time:       0 days  0 hours 56 minutes 24.3 seconds.", "Elapsed time:       0 days  0 hours 59 minutes  5.6 seconds.", "Normal termination of Gaussian 16 at Fri Sep  4 05:40:58 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/pc_monomer_optfreq_hpc20_p3/input.com; SHA256 65795527b7aeea42466069762703a61e2686743d62919f3bfae75cf7032f938b; 764 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=100GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/pc_monomer_optfreq_hpc20_p3/stdout.log; SHA256 970add105d87663c04aa585cca89c873cb95dce1cffc8641ad737890f14b52a7; 425048 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -381.455105114     A.U. after    1 cycles"]
  frequencies: {"count": 33, "minimum_cm1": 102.769, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 13 minutes 55.2 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 47.6 seconds.", "Normal termination of Gaussian 16 at Tue Sep  8 04:33:47 2026.", "Job cpu time:       0 days  0 hours  4 minutes 21.1 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 13.9 seconds.", "Normal termination of Gaussian 16 at Tue Sep  8 04:34:02 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/input.com; SHA256 473e10a2a80d3e6fe5846035ed11f34d93568704b0a4fd48b95de1a5e5db6d38; 2083 bytes.
  input_route: ["#p B3LYP/def2SVP EmpiricalDispersion=GD3BJ Opt=(CalcFC,Tight,MaxCycles=400,MaxStep=5) Freq NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=80GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/stdout.log; SHA256 97398d169de4dd4a5f35742e68b7b631115441315faa4ca68ffc1ad808ddfefd; 1992401 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -752.681236449     A.U. after    1 cycles"]
  frequencies: {"count": 120, "minimum_cm1": 13.4108, "negative_count": 0}
  normal_termination_count: 2
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  3 hours 18 minutes 59.5 seconds.", "Elapsed time:       0 days  0 hours 10 minutes  1.0 seconds.", "Normal termination of Gaussian 16 at Wed Sep 16 13:31:41 2026.", "Job cpu time:       0 days  0 hours 55 minutes  4.4 seconds.", "Elapsed time:       0 days  0 hours  2 minutes 48.0 seconds.", "Normal termination of Gaussian 16 at Wed Sep 16 13:34:33 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/input.com; SHA256 82f1a68e3b9f8188e92c107a9f0c5b0c677d17ed4cb3add3ccf46036d334f67a; 960 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/stdout.log; SHA256 9f3616e82c5accbd785e4cfb5ef12d6fa7d07cf3b9f96ac07e3d34194f7358ae; 41854 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -806.565460161     A.U. after   12 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  8 minutes 17.0 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 25.5 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 21:21:17 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/input.com; SHA256 24a9d91c505e9458dc2d49e4e5d60fad2d26dd64262fd4775f8ea536a0a5cd6b; 956 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/stdout.log; SHA256 d41dde02b07c64345b58debf577f483f199f6c63bf66244a80fd5c0ee33a386c; 42069 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -806.565458116     A.U. after   12 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  8 minutes 10.3 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 25.3 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 21:21:42 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_source_binding_sp_20260915/input.com; SHA256 57b3971442e13a09de65f111985fbbdfed11738fd9f93c6dc7462c3fb26bda99; 399 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_source_binding_sp_20260915/stdout.log; SHA256 c93dee67fbf3190ff3117fa863ff2e0ecb187657b4e22f6608ff0b4ecd896699; 24214 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -424.693626420     A.U. after    8 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  0 minutes 51.1 seconds.", "Elapsed time:       0 days  0 hours  0 minutes  3.6 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 20:59:58 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/input.com; SHA256 f3540629dcb791a35c4b02f573e507ba574e61c5d2c36b14082b0d7adb616662; 2203 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/stdout.log; SHA256 ea83ea3e4df00a18891e69aabeadbae793ab2f243d7a3d3deb64e6b2ea33d4b3; 94147 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -885.240261210     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  1 hours 11 minutes 55.6 seconds.", "Elapsed time:       0 days  0 hours  4 minutes 10.9 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 21:04:22 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/input.com; SHA256 40df03d47ffbf3215286b16d9764a6d0d3373384fca159a84fe2c16c0e218903; 2188 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/stdout.log; SHA256 3829617e6e13336fc62f79e6655363fb6d67ffeeb35e20d2312734bb9238ba0d; 94255 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -885.239558114     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  1 hours 12 minutes 25.1 seconds.", "Elapsed time:       0 days  0 hours  4 minutes  6.8 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 21:08:30 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_source_binding_sp_20260915/input.com; SHA256 d1480dc7d7323f83ca40978fd30d9cb095e97c61207dca2f76eab16ccdd073c2; 1633 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_source_binding_sp_20260915/stdout.log; SHA256 7e212ff5b4079d751bde4185bb1606772db66bb1da73844247532c0bc5d40408; 63814 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -503.346837491     A.U. after   11 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 24 minutes 47.0 seconds.", "Elapsed time:       0 days  0 hours  1 minutes 31.5 seconds.", "Normal termination of Gaussian 16 at Wed Sep 16 11:57:14 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/pc_source_binding_sp_20260915/input.com; SHA256 8e1ff8619de5bde34525983201a99e5c1c0be9ef768e80cbeb9096c1e4595114; 732 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/pc_source_binding_sp_20260915/stdout.log; SHA256 c0102cf620d10fad7de05b82d8e03eef2d9b79387ee99503057cc5d44f4ad25e; 36034 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -381.845474281     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours  3 minutes 43.0 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 13.2 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 21:00:11 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/input.com; SHA256 5b02401f77e61ed4047ed4c21928ff3b6d1a715db1beeab0c146cad6a225e3cd; 1973 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/stdout.log; SHA256 4f1b5373ecdedcd1d4b6ecb251a74041517587c98e8933182f12870e5cc02a81; 82293 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -753.395006147     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 38 minutes 40.5 seconds.", "Elapsed time:       0 days  0 hours  1 minutes 56.3 seconds.", "Normal termination of Gaussian 16 at Thu Sep 17 00:23:52 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/input.com; SHA256 636281f083ec7063ac8aa6b6e3784ee09d0a9f1c49b83d52c6299af55f614f3a; 1973 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/stdout.log; SHA256 6d7544db533ddd38441bb074fef36ac9c4f15e1c1c2a680c4a2cc6c10d86c311; 82277 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -753.394423820     A.U. after   13 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 41 minutes 42.1 seconds.", "Elapsed time:       0 days  0 hours  2 minutes  9.1 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 21:20:51 2026."]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_source_binding_sp_20260915/input.com; SHA256 a43696aa1932be256ba4e41e313d8f1ad7c5d1195ea41e74b29658ab8186df76; 1420 bytes.
  input_route: ["#p B3LYP/6-311+G(2d,p) NoSymm SCF=(XQC,MaxCycle=512)"]
  input_resources: ["%NProcShared=20", "%Mem=24GB"]
- docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_source_binding_sp_20260915/stdout.log; SHA256 3356b2ce1c24e18f032945284f3df6efe5b3fe47d182b67ea05763945d417a41; 59277 bytes.
  last_scf: ["SCF Done:  E(RB3LYP) =  -371.528516402     A.U. after   11 cycles"]
  normal_termination_count: 1
  error_termination_count: 0
  reported_resources: ["Job cpu time:       0 days  0 hours 13 minutes 31.7 seconds.", "Elapsed time:       0 days  0 hours  0 minutes 47.5 seconds.", "Normal termination of Gaussian 16 at Tue Sep 15 20:59:54 2026."]

## Historical verification retained verbatim; superseded status labels are noncurrent

The following historical narrow-task/legacy reference segments are retained as facts, not active rubric or qualification. Current acceptance and scoring at the top governs this version. Original full evaluator snapshots are indexed in evaluation/history_archive_index.json.

### Historical source legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot

# 已验证成功计算参考 — paper_c28b0a1c549f4575 / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文 PDF pp3–4/Fig.2；历史验证索引 SI §5 路线，本地 SI 原件未取得，不冒称本轮直接核对原件。

[论文正文](../../../../papers/paper_c28b0a1c549f4575/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/report/results.json)。

## 2. 真实有效计算流程

1. 四个完整分子图（DED2²⁺、TEA⁺、BF4⁻、PC），三种 ion–PC 对，每对两个独立初始方向。先气相 B3LYP-D3BJ/def2-SVP Opt/Freq：四单体和六复合物，共十个最低点前驱。
2. 六复合物按映射检查初始方向区别、终态去重、频率和 parent→SP 坐标一致。随后十个 B3LYP/6-311+G(2d,p) 气相电子单点，不能用 SP 正常结束代替 parent 最低点验证。
3. Ebind=Ecomplex−Eion−EPC，同一单体 convention，×627.509474 kcal/mol/Eh。两方向区间：DED2_PC [−30.088727,−29.647527]；TEA_PC [−13.187403,−12.821987]；BF4_PC [−16.540811,−16.539528]。
4. 替代方向是真实敏感性对照，最弱 DED2 仍比最强 TEA 更负。结论是孤立电子结合能排序，不等同体相溶剂自由能。

## 3. 有效产物与原始输入/输出

- [provenance/binding_progress_20260916/results.json](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/binding_progress_20260916/results.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/input.com)
- [execution_jobs/job_28cdaf0cae20404dbf3f940e50074422/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_28cdaf0cae20404dbf3f940e50074422/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_28cdaf0cae20404dbf3f940e50074422/input.com)
- [execution_jobs/job_33c5aa59eb6f4886b5fc50c54d0a2ef0/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_33c5aa59eb6f4886b5fc50c54d0a2ef0/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_33c5aa59eb6f4886b5fc50c54d0a2ef0/input.com)
- [execution_jobs/job_36c9fefc561e4d4589a66716cddf72ab/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_36c9fefc561e4d4589a66716cddf72ab/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_36c9fefc561e4d4589a66716cddf72ab/input.com)
- [execution_jobs/job_5fbb4248998841a9808963257d3f6182/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_5fbb4248998841a9808963257d3f6182/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_5fbb4248998841a9808963257d3f6182/input.com)
- [execution_jobs/job_716585773558490d9262333e55c3314f/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_716585773558490d9262333e55c3314f/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_716585773558490d9262333e55c3314f/input.com)
- [execution_jobs/job_7a5016db085b41d99ea79a0638186dff/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7a5016db085b41d99ea79a0638186dff/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7a5016db085b41d99ea79a0638186dff/input.com)
- [execution_jobs/job_7b1fb25d5e7d4d458e1ccd8fe9ec817a/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7b1fb25d5e7d4d458e1ccd8fe9ec817a/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7b1fb25d5e7d4d458e1ccd8fe9ec817a/input.com)
- [execution_jobs/job_979fd675c06f4e57bb3b328ad15edba2/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_979fd675c06f4e57bb3b328ad15edba2/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_979fd675c06f4e57bb3b328ad15edba2/input.com)
- [execution_jobs/job_f0d22d8cee914269b8a5b650e460af56/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_f0d22d8cee914269b8a5b650e460af56/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_f0d22d8cee914269b8a5b650e460af56/input.com)
- [local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/bf4_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/ded2_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/pc_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/pc_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/pc_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/tea_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_source_binding_sp_20260915/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `ar_kp_process_minima` | All three public pair identities are explored with multiple orientations and validated minima. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_kp_process_bookkeeping` | The comparison is based on consistent component-energy bookkeeping. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_kp_order` | DED2+-PC is stronger-binding than TEA+-PC. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_c_final` | The public-system calculation supports stronger competitive PC association by DED2+ than TEA+. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

AR 额外路线构思字段不在共享历史报告中，软件回归仅标明该差异，不能补造当时自主发现轨迹。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。


### Historical source v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot

# Development reference status

No expanded scientific reference has been certified. Status: implemented_pending_expanded_reference.

See `reference_validation_plan.md` and private `legacy_final_snapshot/` for historical material. The old PASS does not apply. New quantum calculations: 0.

