# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "Cy2非相对论SOC pilot已原生完成并解析，初次MPI失败保留。尚未完成相对论/方法校准及敏化剂和rubrene矩阵。",
    "unfinished_scientific_or_input_work": [
      "IR780/Cy1及Cy2态密度对应",
      "同条件rubrene/供体绝热能量循环",
      "重元素算符与冻结几何/方法敏感性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_e0791c047a731974/evaluation/reference_validation_plan.md",
  "applicability": "仅 Cy2 非相对论先导不覆盖重元素方法或整套受体循环；已有记录仅按其适用范围复用。",
  "new_scientific_calculations_performed": false,
  "raw_evidence": [
    {
      "case_id": "cy2_soc_nr_pilot_v1",
      "job_id": "hpc-job-c00cf410-6f3e-4680-9dda-645f21e91985",
      "status": "engine_failed",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/outputs/cy2_soc_nr_pilot",
      "normal_termination": false,
      "allocated_core_hours": 0.004425713344891038
    },
    {
      "case_id": "cy2_soc_nr_pilot_v1_a02",
      "job_id": "hpc-job-b626567d-c05e-4962-a404-5b0f5c5ef34c",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/outputs/cy2_soc_nr_pilot_v1_a02",
      "normal_termination": true,
      "allocated_core_hours": 1.6260992548531956
    }
  ],
  "evidence_audits": [
    "docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/report/cy2_soc_nr_pilot_v1_a02_native_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/legacy/native_log_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/legacy/attempt_inventory.json"
  ]
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

Existing native Cy2 nonrelativistic SOC pilot is a feasibility datum, not calibrated heavy-element response or full donor/rubrene energetics. Later validate state identification and consistent donor/acceptor energies and test whether claimed significance exceeds method uncertainty.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Source-specific method, identity and scope restrictions remain in source_scope_audit and the current scientific rules.
