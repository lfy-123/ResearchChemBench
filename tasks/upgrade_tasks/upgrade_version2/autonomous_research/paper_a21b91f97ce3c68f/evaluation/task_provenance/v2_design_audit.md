# paper_a21b91f97ce3c68f — paper-specific V2 plan

How does molecular conformation affect one-bond 119Sn–13C coupling in the three supplied stannyl heterocycles, and what evidence explains any differences between the scaffolds?

## source_documents

[
  {
    "path": "papers/paper_a21b91f97ce3c68f/documents/main.pdf",
    "sha256": "637bc5dd2d5d03773819f3cf73524d6c4c2b3fc7cdd4ff6b077b811ed0ea452b",
    "pages": [
      1,
      2,
      3
    ],
    "total_pages": 9
  },
  {
    "path": "papers/paper_a21b91f97ce3c68f/documents/supplementary_001.pdf",
    "sha256": "35c7bfcbb36da658670c057ed2e6ecdc3ac6c3707c0bd122469234fae020d12b",
    "pages": [
      2,
      3,
      4,
      5,
      6
    ],
    "total_pages": 58
  }
]

## source_scope

Main pp.2–3 and SI S2–S6 investigate stereoelectronic and structural correlations in organotin couplings. Source compounds6,7,13 are an actual bounded subset of a much larger scaffold study; no universal family-wide law is required.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "pair_matrix",
    "geometric_interventions",
    "mechanism_test"
  ],
  "fixed_schema_keys": {
    "pair_matrix": [
      "6",
      "7",
      "13"
    ],
    "geometric_interventions": [
      "6",
      "7",
      "13"
    ],
    "mechanism_test": [
      "ordinary_pair_6",
      "ordinary_pair_7",
      "sulfur_pair_13",
      "torsion_vs_distance_file",
      "orbital_coupling_comparison_file",
      "method_sensitivity",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "移除 ±30° 扭转、±0.03 Å 距离及预设超共轭/硫挑战路线；保留相同同位素、对象和实际耦合定义，由 agent 选择能区分解释的计算。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose representative conformations and decide whether they support a meaningful comparison.",
  "Select evidence that can explain coupling changes beyond a numerical correlation.",
  "Assess method and conformational uncertainty and limits of transfer across scaffolds."
]

## public_input_changes

[
  "Retain full mapped graphs and Sn/carbon measurement IDs; remove required_orientations as a submission enum and all intervention_torsion/held_distance definitions.",
  "Remove fixed ±30 degree/±0.03 angstrom interventions and compulsory NBO/coupling-component matrix.",
  "Do not disclose source coupling magnitudes, empirical scaling or proposed donor mechanism to AR."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors used CREST/GFN2-xTB conformer sampling, selected low-energy axial/equatorial structures, then Gaussian16 GD3-B3LYP/def2-TZVPP gas-phase optimizations/frequencies and NBO3.1. They computed spin–spin response with a TZP-ZORA basis, nmr=(spinspin,mixed,readatoms), and integral=NoXCTest; main p.2 explicitly calls the Hamiltonian nonrelativistic despite the basis label. They correlated antiperiplanar donation with coupling and applied a mean empirical factor −1.419 to some absolute Sn–C predictions (SI S5). This source factor is not a benchmark acceptance tolerance. Source6,7,13 occur in SI S5–S6. The fixed torsion/distance interventions in V1 were later controls, not author protocol; reproduce the disclosed baseline or justify alternatives and design extra tests independently.

## existing_evidence_reuse

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

## planned_changes

[
  "Save this source-specific plan before V2 copy; retain immutable V1 and legacy-final snapshots privately.",
  "Rewrite both scientific tasks and public data, release predetermined schema matrices, bind five paper-specific evaluators to auditable records.",
  "Use open_research policy; preserve bibliographic/route/answer material privately; refresh official payload hashes."
]

## acceptance_checks

{
  "mechanical": [
    "Official package/hash/runtime and policy load",
    "Public export exact allowlist, no evaluator or snapshot",
    "AR/PR data/schema/five-result-evaluator parity",
    "Schema positive, partial, failure and old-scalar/empty-evidence negatives",
    "All evaluator JSONPath roots refer to schema fields",
    "Raw artifacts and ID link audit on non-scientific temporary fixtures"
  ],
  "semantic": "Paper-specific counterexamples are defined in critical and criteria. Actual judge/science calibration remains pending."
}

## limitations

[
  "已有完整源图与中断恢复记录；全耦合分量和几何对照尚未校准，不能把作业启动算完成。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
