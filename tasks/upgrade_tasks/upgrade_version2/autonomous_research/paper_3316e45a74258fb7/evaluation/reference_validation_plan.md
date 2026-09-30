# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "TD2T旧128原子S0端点图与378个正频率已审，最低5.1761cm⁻¹；Gaussian微小力接受但最大位移阈值未过。复用后5S/5T原生SOC完成，S1=2.142275eV、f=0.76363396；S1/T1 SOC在0.01cm⁻¹打印精度为零，不能当物理精确零。完整三模型矩阵未完成。",
    "unfinished_scientific_or_input_work": [
      "三布局完整图、构象及基线端点精审",
      "S1/T1弛豫及曲率，垂直/绝热分列",
      "同扭转SOC/NTO干预及CT敏感方法控制"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_3316e45a74258fb7/evaluation/reference_validation_plan.md",
  "applicability": "可复用经审计的 TD2T 基态及部分 SOC；三布局激发态弛豫与方法稳健性未完整，不强制先算齐再开发。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "path": "docs/upgrade_tasks_verification/group_5/papers/paper_3316e45a74258fb7/report/td2t_soc5_native_audit.json",
    "scope": "Existing TD-2T native excited-state/SOC parsing can establish feasibility for that object; it does not validate the other structures or source basis discrepancy."
  }
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

No new fixed-torsion, conformer, SOC or adiabatic reference matrix has been calculated.; Resolve basis shorthand explicitly and calibrate CT-state/method uncertainty.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Source-specific method, identity and scope restrictions remain in source_scope_audit and the current scientific rules.
