# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "6a原优化在第23步被平台STOPPED；55原子checkpoint经formchk验证含几何、能量及Hessian。恢复01以同方法Cartesian/ReadFC保留SCF与已有曲率继续运行，避免重做初始CalcFC。六椅式完整源图已映射；J分量尚未完成。",
    "unfinished_scientific_or_input_work": [
      "6a收敛后其他椅式与构象检查",
      "119Sn–13C四分量耦合、同位素及局域轨道",
      "扭转/键长干预、硫挑战与方法敏感性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_a21b91f97ce3c68f/evaluation/reference_validation_plan.md",
  "applicability": "已有完整源图与中断恢复记录；全耦合分量和几何对照尚未校准，不能把作业启动算完成。",
  "new_scientific_calculations_performed": false
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

Historical6a preparation/checkpoint recovery establishes a route but not a completed three-scaffold coupling reference. Later require genuine response outputs and verify isotope/sign/component parsing. Alternative orbital analyses must be assessed by scientific adequacy rather than NBO availability.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

SI p.2 TZP-ZORA is a basis name. Main p.2 explicitly states a nonrelativistic Hamiltonian. No rule accepts a basis name as evidence of a relativistic response calculation. Source empirical factor −1.419 is not a universal tolerance.
