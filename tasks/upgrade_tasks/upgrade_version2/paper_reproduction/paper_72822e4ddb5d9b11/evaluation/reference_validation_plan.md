# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 6,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_6/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "733d1efabb39deac239f2318d48fc7385a9faa720b2a206bfeede892b4a158fa",
    "recorded_at_utc": "2026-09-28T15:08:44.745913+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "完整Ni 165原子B3LYP CS和T均完成独立梯度、同几何489正频和波函数稳定性；T RMS/MAX力3.9093e-6/2.46145e-5 Eh/bohr，最低9.17823cm-1。绝热T−CS=32.21792kcal/mol，垂直35.18214；BP86两独立BS与自由CS/T矩阵继续",
    "unfinished_scientific_or_input_work": "完成BP86独立BS、自由CS/T优化频率、各自稳定性与完整密度/态序对照；整篇仍needs_work",
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_72822e4ddb5d9b11/evaluation/reference_validation_plan.md",
  "applicability": "已有部分 B3LYP 结构/稳定性/489 模式证据；另一方法完整矩阵尚待校准，后续按新问题评估可复用性。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "paths": [
      "docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/report/CS_stability_result.json",
      "docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/report/BS_flipNi_result.json",
      "docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/report/B3LYP_adiabatic_gap.json"
    ],
    "scope": "State stability/collapse and matched-method energy audits are reusable at their exact geometry and settings; not proof of universal covalency or a new V2 reference."
  }
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

New BS starts, stability/occupation evidence, BP86/B3LYP matched controls and their uncertainty remain uncomputed.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Source-specific method, identity and scope restrictions remain in source_scope_audit and the current scientific rules.
