# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "两笼优化已有原生结果及各收敛条件审查。原20核Hessian在平台STOPPED且未写完；保留全部日志/GBW/释放证据。相同PBE/def2-TZVP、VeryTightSCF、DEFGRID3的40核/200GiB恢复尝试已排队，复用收敛GBW，不宣称已有新最低点。",
    "unfinished_scientific_or_input_work": [
      "两笼Hessian和质量归一化模式投影",
      "三类模式中心/±h/±h/2共同坐标系g/A张量与电子态/数值噪声检查",
      "方向/刚性控制、基组敏感性与温度权重"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_3d1d9b7f6df049da/evaluation/reference_validation_plan.md",
  "applicability": "两笼优化和 Hessian 在途记录属于验证证据；不接管作业、不把不完整 Hessian 认作最低点或寿命验证。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "paths": [
      "docs/upgrade_tasks_verification/group_5/papers/paper_3d1d9b7f6df049da/report/ih_strictgrid_optimization_audit.json",
      "docs/upgrade_tasks_verification/group_5/papers/paper_3d1d9b7f6df049da/report/d5h_strictgrid_optimization_audit.json"
    ],
    "scope": "Historical stringent-grid optimization audits delimit stationarity; not the expanded spin response or calibrated T1."
  }
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

No new mode projection matrix, negative-control derivatives or frame/step uncertainty reference has been run.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

The derivative example is Figure S16 on SI PDF p.20; Table S3a–d occupies pp.21–24. Coordinate blocks are pp.18–19. The p.19 heading repeats Ih, but its distinct 80-carbon cage graph has 20 automorphisms while p.18 has120; both are cubic connected graphs and both public coordinate arrays match their source blocks exactly. Thus the inherited D5h label is supported by topology rather than the duplicated heading.
