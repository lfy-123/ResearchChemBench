# paper_94b0a8ae694590ea — paper-specific V2 plan

What differences in the electronic properties of the three supplied TTA derivatives are relevant to their interaction with single-walled carbon nanotubes, and how far does the molecular evidence support an explanation of their differing composite behavior?

## source_documents

[
  {
    "path": "papers/paper_94b0a8ae694590ea/documents/main.pdf",
    "sha256": "9fe1fcd47f0da4b843db4f058e7482a4ca3049b1e17b0a3117b6c4c7328f130d",
    "pages": [
      3,
      4,
      5
    ],
    "total_pages": 12
  },
  {
    "path": "papers/paper_94b0a8ae694590ea/documents/supplementary_001.pdf",
    "sha256": "3a0f1cd4f04cb734daeb4c1cb4520edca7343964e00d8a594022193b87f659a9",
    "pages": [
      10,
      15,
      20
    ],
    "total_pages": 20
  }
]

## source_scope

Source main pp.2–5 reports three organic molecules blended with commercial SWCNT films, isolated-molecule B3LYP electronic calculations and film measurements. No definite tube chirality or NEGF transport simulation is established. V2 narrows the computational claim to molecular/interfacial evidence and its representativity.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "interface_matrix",
    "boundary_controls",
    "charge_mechanism"
  ],
  "fixed_schema_keys": {
    "interface_matrix": [
      "2BF-TTA",
      "2BT-TTA",
      "2C8Ph-TTA"
    ],
    "boundary_controls": [
      "representative",
      "length_same_coverage",
      "kpoint_convergence",
      "vacuum_convergence",
      "cells_file",
      "coverage_per_angstrom",
      "pose_attempt_records",
      "evidence_files"
    ],
    "charge_mechanism": [
      "charge_conservation_error_e",
      "work_function_differences_eV",
      "electron_gain_e",
      "dipole_profile_file",
      "orbital_or_projected_density_file",
      "energy_vs_charge_test",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "问题限定源分子/材料现象可支持的层次，管模型、吸附姿势、覆盖敏感性和电荷分析方案由 agent 论证；不强制特定 480C 周期单元或未支持 NEGF。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose molecular or interface descriptors that can test a relevant electronic explanation.",
  "Select and justify any microscopic representation of the heterogeneous nanotube material.",
  "Separate conclusions supported by molecular evidence from those requiring film-scale data."
]

## public_input_changes

[
  "Convert full source molecule coordinates to verified chemical graphs, retaining alkyl side chains and heteroatoms but withholding optimized geometry and frontier-energy answers.",
  "Remove the arbitrary 480-carbon (10,10) 12-repeat tube, fixed adsorption/separation/transport controls and implied NEGF requirement.",
  "Supply source tube distribution and measured film context with loading differences; no source HOMO ranking."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The source used Gaussian09W B3LYP/6-31G(d) calculations on the isolated organic molecules, reporting HOMO/LUMO levels of approximately −5.04/−2.14 eV for 2BT-TTA, −5.00/−2.08 eV for 2BF-TTA and −4.99/−1.65 eV for 2(C8Ph)-TTA. It compared these with a cited SWCNT energy level and proposed electronic/interfacial explanations of measured composite behavior. Source main pp.3–5 also describes loading-dependent morphology and transport, which isolated electronic calculations do not establish independently. Reproduce the disclosed molecular baseline and evaluate the limits of its interpretation. The fixed (10,10) periodic tube, adsorption and transport controls in V1 were added benchmark models, not author calculations; they are no longer mandatory.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "旧孤立分子日志已索引；尚无有效周期界面矩阵，不能从HOMO排序推出掺杂。",
    "unfinished_scientific_or_input_work": [
      "管/三种完整中性掺杂物与多吸附姿势",
      "恒覆盖加倍长度、k点与真空控制",
      "同网格密度差、势能/功函数与分区依赖"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_94b0a8ae694590ea/evaluation/reference_validation_plan.md",
  "applicability": "目前缺有效周期界面矩阵；可行性/预算及局域界面量到体相热电性能的边界需实查，不能由 HOMO 排序直接给掺杂结论。",
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
  "目前缺有效周期界面矩阵；可行性/预算及局域界面量到体相热电性能的边界需实查，不能由 HOMO 排序直接给掺杂结论。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
