# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 6,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_6/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "733d1efabb39deac239f2318d48fc7385a9faa720b2a206bfeede892b4a158fa",
    "recorded_at_utc": "2026-09-28T15:08:44.745913+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "已有H同几何独立BS/泛函校准与SF历史复用。原自由T平台停止并完全释放后，保留精确配体图与轨道恢复；恢复作业70f6b162正在推进梯度。H/Me/OMe自由/固定核心矩阵待补",
    "unfinished_scientific_or_input_work": "H/Me/OMe 自由及固定核心矩阵和其余方法敏感性",
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_validation_plan.md",
  "applicability": "现有 H 同几何 BS/方法记录可作有条件参考；三元系列和方法误差未齐不等于开发未完成。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "path": "docs/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/report/H_VWN5_HS_BS_result.json",
    "scope": "Stable HS/BS and independent spin-flipped BS on the H source geometry; its linked raw outputs are usable only for that object/method. VWN5 versus source VWN3 and independent geometry remain limitations; not a three-member validation."
  }
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

Later calibrate alternative valid routes on source-family evidence and source-specific uncertainty. Existing H-only stable BS outputs establish a feasible ORCA route, not a resolved H/Me/OMe effect. PySCF-forge availability is not assumed.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Source-specific method, identity and scope restrictions remain in source_scope_audit and the current scientific rules.
