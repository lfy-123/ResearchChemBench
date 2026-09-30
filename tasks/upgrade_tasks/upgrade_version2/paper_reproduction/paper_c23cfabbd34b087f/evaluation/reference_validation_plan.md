# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "复用1M_TIPS CS局部正曲率最低点。同几何RKS及单个混合UKS稳定性测试均正常，UKS回到CS。垂直三重态稳定，E=-2812.82825259Eh，S²从2.0357湮灭至2.0008，T-CS=0.83384694eV；这不替代三重态弛豫或独立BS初猜。",
    "unfinished_scientific_or_input_work": [
      "三重态弛豫/曲率、独立BS初猜和构象",
      "四模型CS/BS/T比较与溶液低态",
      "共同骨架控制和独立活性空间/方法校准"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_c23cfabbd34b087f/evaluation/reference_validation_plan.md",
  "applicability": "一部分历史最低点、稳定性和垂直三重态证据可参考；全模型弛豫/独立校准未完整，数值容差不可机械继承。",
  "new_scientific_calculations_performed": false,
  "raw_evidence": [
    {
      "case_id": "pah_1m_tips_cs_bs_stability_v1",
      "job_id": "hpc-job-65c72cb9-428a-4d10-ba12-e893f189b00c",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_c23cfabbd34b087f/outputs/pah_1m_tips_cs_bs_stability_v1",
      "normal_termination": true,
      "allocated_core_hours": 8.329263550700206
    },
    {
      "case_id": "pah_1m_tips_vertical_triplet_stability_v1",
      "job_id": "hpc-job-4ce8b508-a8c6-4703-bc81-c057b9452eb8",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_c23cfabbd34b087f/outputs/pah_1m_tips_vertical_triplet_stability_v1",
      "normal_termination": true,
      "allocated_core_hours": 5.278827075171284
    }
  ],
  "evidence_audits": [
    "docs/upgrade_tasks_verification/group_5/papers/paper_c23cfabbd34b087f/report/1M_TIPS_stability_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_c23cfabbd34b087f/report/1M_TIPS_vertical_triplet_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_c23cfabbd34b087f/legacy/validated_1M_TIPS_CS_minimum.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_c23cfabbd34b087f/legacy/native_log_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_c23cfabbd34b087f/legacy/attempt_inventory.json"
  ]
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

The existing 1M_TIPS closed-shell positive-curvature minimum, RKS/UKS stability and vertical triplet provide one feasible route. UKS collapse from one seed is not exhaustive absence of another solution; the vertical triplet is not an adiabatic gap. Other models, alternative descriptions and uncertainty require later calibrated evidence.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Source-specific method, identity and scope restrictions remain in source_scope_audit and the current scientific rules.
