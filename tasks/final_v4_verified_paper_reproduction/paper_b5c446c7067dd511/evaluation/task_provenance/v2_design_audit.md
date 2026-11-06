# paper_b5c446c7067dd511 — paper-specific V2 plan

Which excited-state relaxation pathways are supported by molecular electronic evidence for the four supplied emitters, and how does aromatic substitution affect that assessment?

## source_documents

[
  {
    "path": "papers/paper_b5c446c7067dd511/documents/main.pdf",
    "sha256": "e14eba4b6b741eec2e479177d88173fd688caa63c7a5f9bce461d441b7f5e09d",
    "pages": [
      3,
      4,
      5
    ],
    "total_pages": 13
  },
  {
    "path": "papers/paper_b5c446c7067dd511/documents/supplementary_001.pdf",
    "sha256": "d8ea0572e3bcb3543cfcba2de0e31c9a4001e9f72925f9adf5caf7d0454238f0",
    "pages": [
      2,
      3,
      4,
      5,
      6
    ],
    "total_pages": 37
  }
]

## source_scope

Main pp.3–5, Fig.3 and SI pp.2–6 investigate four phenanthrimidazole molecules and interpret their singlet/triplet manifolds and emission. This task is the molecular electronic explanation, not prediction of device EQE or a complete excited-state kinetic simulation.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "series_states",
    "representative_controls",
    "channel_competition"
  ],
  "fixed_schema_keys": {
    "series_states": [
      "Ph-mP",
      "Na-mP",
      "An-mP",
      "Py-mP"
    ],
    "representative_controls": [
      "Ph-mP",
      "An-mP"
    ],
    "channel_competition": [
      "Ph-mP",
      "An-mP"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "移除固定 Ph/An 代表、45° 扭转、5→10 根和预设高三重态通道；允许自主态窗口/竞争路径，不能按作者根号或小能隙直接认定速率。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Decide which excited states and molecular geometries are relevant to the relaxation question.",
  "Choose a defensible characterization and evidence capable of distinguishing pathway plausibility from mere energy proximity.",
  "Revise assignments or delimit conclusions when state identity, method or environmental uncertainty matters."
]

## public_input_changes

[
  "Retain four complete molecular graphs; remove source optimized geometries, fixed three-fragment partitions, prescribed torsion intervention and root/state winners.",
  "Remove required 10/20-root panels, fixed SOC/CT metric and minimum hypothesis count from schema and private rules."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors used Gaussian09W gas-phase TD-B3LYP/6-31G(d,p), then Multiwfn NTO/IFCT analysis with phenanthrimidazole, methylphenyl and appended aromatic/benzene-bridge fragments. SI pp.2–6 reports ten singlet and ten triplet states. Main p.3 interprets the S1 states as mixed local/charge-transfer and proposes high-lying-triplet RISC: T4 for Ph/Na and T3 for An/Py; reported S1–T1 gaps are 0.88, 0.89, 1.34 and 1.11 eV. These are author hypotheses/references, not measured rates. Main p.3 prints Py CT/LE percentages 57.23/45.77, which do not sum to 100; reproduce definitions and report the inconsistency rather than enforce those numbers as truth. Later benchmark SOC, 20-state overlap, 45-degree constraints and CAM-B3LYP calculations are additional validation, not the original protocol.

## existing_evidence_reuse

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
  "已有原生 SOC/响应及 5D 跨实现校准；作者 6D/度量约定、跨扭转态对应和整篇机制验收仍待补。修复来源和前后哈希必须随基线保留。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
