# paper_3d1d9b7f6df049da — paper-specific V2 plan

Does cage isomerism change the molecular spin response to vibrations in the supplied Y2@C80(CH2Ph) radicals, and what can that evidence explain about differences in spin-lattice relaxation?

## source_documents

[
  {
    "path": "papers/paper_3d1d9b7f6df049da/documents/main.pdf",
    "sha256": "767499d77d3e48a8377ff6668eb0ea6263ba5d3ed7a11dbc62b323f2d6a24fb4",
    "pages": [
      3,
      8,
      9,
      10
    ],
    "total_pages": 19
  },
  {
    "path": "papers/paper_3d1d9b7f6df049da/documents/supplementary_001.pdf",
    "sha256": "9506646b763e5856fe966b7523096ce523255d105cf4f0f792c45769dfaf4568",
    "pages": [
      2,
      20,
      21,
      22,
      23,
      24,
      25,
      26
    ],
    "total_pages": 32
  }
]

## source_scope

Main pp.3,8–10 and SI S2,S20–S26 describe the neutral Ih/D5h Y2 radicals, vibrations and derivatives of spin Hamiltonian tensors. The source explicitly limits its derivative analysis to trends rather than exact relaxation times.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "mode_assignment",
    "tensor_derivatives",
    "thermal_and_frame_controls"
  ],
  "fixed_schema_keys": {
    "mode_assignment": [
      "Ih",
      "D5h"
    ],
    "tensor_derivatives": [
      "Ih",
      "D5h"
    ],
    "thermal_and_frame_controls": [
      "temperature_rows",
      "rotation_matrix",
      "back_rotated_tensor",
      "original_tensor",
      "rotation_error",
      "rotation_records",
      "lateral_vs_longitudinal",
      "lateral_vs_cage",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "解除三类模式、±h/±h/2、20/100 K 和指定张量导数方案的强制性；保留坐标系/单位/质量归一化及支持自旋响应主张所需证据。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose a model connecting molecular motion to spin response.",
  "Decide which motions and observables are informative and how to establish their reliability.",
  "Determine what molecular evidence can support about relaxation and its limitations."
]

## public_input_changes

[
  "Retain the two full source-computed geometries solely as chemical/structural inputs, with transparent provenance; no g/A tensors or mode answers are supplied.",
  "Remove mandatory named mode classes, fixed ±h/±h/2 stencil, thermal temperatures and complete displacement matrix. The research design is agent-chosen."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The source used ORCA PBE/def2-TZVP with a Dolg Y ECP for structures and Hessians, and PBE-ZORA with ZORA-adjusted def2-TZVP for g and hyperfine tensors. It differentiated tensor components numerically along 23 low-frequency modes, fitting a quadratic response (SI S16/TableS3). Main pp.8–10 associates low-frequency metal motion with relaxation and uses thermal weighting; it reports lower lateral frequencies for Ih than D5h and a qualitative faster Ih relaxation. The source explicitly omits expensive mixed derivatives and electronic excitations and does not claim exact T1 prediction. Reproduce this disclosed baseline where feasible, or explain justified substitutions. The old benchmark three-class ±h/±h/2 and fixed-temperature matrix was a later validation design, not a source requirement.

## existing_evidence_reuse

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
  "两笼优化和 Hessian 在途记录属于验证证据；不接管作业、不把不完整 Hessian 认作最低点或寿命验证。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
