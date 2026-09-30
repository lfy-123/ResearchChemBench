# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "干syn/anti-La气相优化四标准全过，均237正频率；最低35.0859/16.5511cm⁻¹，能量-1942.42891623/-1942.41643622Eh。两源构象原子顺序不同，金属按元素定位。Tb冻结La几何ECP试算原生正常，316显式电子、54核及8项ECP系数验证。Tb弛豫已准备；Lu与水合/溶液矩阵未完成。",
    "unfinished_scientific_or_input_work": [
      "Tb/Lu实际弛豫及各金属两构象最低点",
      "完整水合矩阵、一致标准态/qRRHO",
      "定制半径溶剂、Lu半径核准、闭合水合循环与低频敏感性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_d8e5490cd9942f4f/evaluation/reference_validation_plan.md",
  "applicability": "已有 La 气相构象及 Tb ECP 原生试算；全水合/溶剂半径/低频校准待补。文件可读与引擎可算不等于溶液热力学正确。",
  "new_scientific_calculations_performed": false,
  "raw_evidence": [
    {
      "case_id": "ln_syn_la_gas_optfreq_v1",
      "job_id": "hpc-job-bb7b2afe-2b42-424d-9051-2e1ff2204556",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/outputs/ln_syn_la_gas_optfreq_v1",
      "normal_termination": true,
      "allocated_core_hours": 49.109000856605256
    },
    {
      "case_id": "ln_anti_la_gas_optfreq_v1",
      "job_id": "hpc-job-4e0c746b-d1b4-4736-b2b7-375828205b39",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/outputs/ln_anti_la_gas_optfreq_v1",
      "normal_termination": true,
      "allocated_core_hours": 58.393744814126855
    },
    {
      "case_id": "ln_syn_tb_on_la_ecp_pilot_v1",
      "job_id": "hpc-job-9e7a7f24-c31c-4599-a0d1-0ee4cb6f7cca",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/outputs/ln_syn_tb_on_la_ecp_pilot_v1",
      "normal_termination": true,
      "allocated_core_hours": 2.360387202497158
    }
  ],
  "evidence_audits": [
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/report/Tb_ECP_native_pilot_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/report/anti_La_gas_minimum_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/report/syn_La_gas_minimum_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/legacy/native_log_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/legacy/attempt_inventory.json"
  ]
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

Existing La gas-phase minima and a native Tb ECP pilot demonstrate partial feasibility only. Aqueous conformer/hydration inference requires its own consistent solvation, entropy and reference-cycle calibration; no all-metal aqueous PASS exists.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Source-specific method, identity and scope restrictions remain in source_scope_audit and the current scientific rules.
