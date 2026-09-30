# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "四成员10S/10T SOC及完整响应已完成；Ph/An扩根20对重叠均>0.99。两者45°约束优化和10根SOC、CAM-B3LYP十根SOC及响应分析均完成。Ph约束Hessian经坐标帧旋转和Lagrangian投影后173个允许模式全正，最低18.8547cm⁻¹；An Hessian排队。Ph/An45的S1分别3.550722/2.909039eV；相应自定义归一化CT幅度0.512895/0.356431。Gaussian5D同几何校准已完成；作者6D/Multiwfn度量与An干预态对应仍未完成。 Ph/An同几何Gaussian5D与ORCA20态校准已完成：最低响应重叠分别0.9998431764/0.9998109611，最大能量差0.0004731012/0.0005930097 eV。支持本次5D实现一致性，不替代作者6D/Multiwfn度量校准、An跨扭转物理态对应或整篇科学验收。",
    "unfinished_scientific_or_input_work": [
      "An45约束曲率与几何干预的物理态对应",
      "作者6D基组约定和Multiwfn片段度量校准仍待完成；Ph/An同几何Gaussian5D/ORCA校准现已完成",
      "综合四成员相邻态竞争与所有干预的有限机制推断"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_b5c446c7067dd511/evaluation/reference_validation_plan.md",
  "applicability": "已有原生 SOC/响应及 5D 跨实现校准；作者 6D/度量约定、跨扭转态对应和整篇机制验收仍待补。修复来源和前后哈希必须随基线保留。",
  "new_scientific_calculations_performed": false,
  "precise_review_record": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/papers/paper_b5c446c7067dd511/progress.json"
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

Existing four-member native ten-state SOC/response outputs and Ph/An twenty-state and Gaussian5D/ORCA overlap checks provide a feasible analysis route. They do not calibrate author 6D/Multiwfn metrics, all geometry-dependent state mappings or kinetic claims. Later semantic calibration must distinguish proximity, electronic coupling and actual rate evidence.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Main p.3 S1 Py CT/LE=57.23/45.77 sums to103; triplet An=50.09/49.01 sums to99.10. Neither pair is an enforced reference. The other printed pairs on this page sum to100. Require the actual metric and normalization; do not silently repair the source numbers or call them measured kinetic rates.
