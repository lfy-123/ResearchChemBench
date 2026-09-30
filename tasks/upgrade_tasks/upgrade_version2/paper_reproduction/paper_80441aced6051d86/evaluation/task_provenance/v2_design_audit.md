# paper_80441aced6051d86 — paper-specific V2 plan

What molecular association structures are consistent with the supplied G1/CB[7]/CB[8] observations, and how far can those structures explain the observed changes in optical response?

## source_documents

[
  {
    "path": "papers/paper_80441aced6051d86/documents/main.pdf",
    "sha256": "b374267591176e59788c82cdd29c55adb2342d866624e6f30ad6f6cbfebed5ba",
    "pages": [
      3,
      4,
      5
    ],
    "total_pages": 9
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_80441aced6051d86.publisher_si.docx",
    "sha256": "ea6d654dd5c29fc7a7e246e7508e7114fcaaf4a99f1297997f09a4d82a5b790a",
    "sections": "Relevant methods, experimental observations and identity blocks; see source review."
  }
]

## source_scope

Main pp.2–4 studies G1 and cucurbituril recognition in water with NMR, calorimetry and DFT. True SI DOCX Sections B–D contains recognition evidence, spectral TableS1 and source structures. V2 uses the source CB7/CB8 subset; CB10 is not a required extension.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "host_matrix",
    "coupling_controls",
    "mechanism_comparison"
  ],
  "fixed_schema_keys": {
    "host_matrix": [
      "CB7_G1",
      "CB8_G1_2"
    ],
    "coupling_controls": [
      "CB8_partner_A_with_host",
      "CB8_partner_B_with_host",
      "CB8_partner_A_no_host",
      "CB8_partner_B_no_host",
      "free_G1",
      "free_G1_2",
      "placement_attempt_records"
    ],
    "mechanism_comparison": [
      "host_effect_CB7",
      "host_effect_CB8",
      "guest_coupling_CB8",
      "confinement_geometry_effect"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "释放自由/含主体/删除主体/删除伙伴固定路径与解释词表，保留真实计量、浓度/介质和可审计光谱量；源优化单体/二聚体坐标需逐项评估答案泄露。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose and assess association structures compatible with the known compositions and measurements.",
  "Determine which structural or electronic evidence can explain the optical changes.",
  "Identify uncertainty and the limits of a finite molecular model in aqueous solution."
]

## public_input_changes

[
  "Retain only component mapped chemical graphs; remove dimer starting pose, optimized host–guest arrangements and source H/J aggregate labels.",
  "Provide measured stoichiometry and emission facts with conditions; no packing answer or source coordinates.",
  "Remove required host deletion, partner deletion, independent starts count and bright/dark matrix; evidence design is agent-chosen."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors used NMR titration/integration and NOESY for aqueous recognition, and Gaussian16 B3LYP-D3/6-31G(d) with PCM water for molecular structures, reporting no imaginary frequencies. They interpreted dilute G1 as monomeric, concentrated free G1 as J-associated, CB7 as stabilizing one guest and CB8 as a two-guest H-type packing. Source main p.4 reports free-dimer versus CB8 packing distances/slip and SI D contains the optimized structures. These are reference interpretations to reproduce and assess, not guaranteed conclusions. The old explicit-host/host-deleted/partner-deleted excited-state matrix was a benchmark extension, not a disclosed author computational protocol. Follow the source structural baseline or explain justified alternatives; extra optical calculations are investigator-designed.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "旧自由G1及G1二聚端点完成图、电荷、原生优化及186/378正频率审查，最低10.8393/11.9969cm⁻¹；二聚微小力接受且最大位移略超阈值，保留限制。完整CB7-G1(+2,190原子)作者初始构型的PCM优化运行；CB8及删除控制尚缺。",
    "unfinished_scientific_or_input_work": [
      "CB7原生优化审查、CB7/CB8各独立结合初始构型",
      "自由/结合态矩阵及相同坐标的主体、伙伴删除",
      "对应态密度/光学强度与构型敏感性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_80441aced6051d86/evaluation/reference_validation_plan.md",
  "applicability": "自由客体历史证据和完整主体系部分在途结果可复用；完整 CB8/构型参考不齐仍单列 reference_pending。",
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
  "自由客体历史证据和完整主体系部分在途结果可复用；完整 CB8/构型参考不齐仍单列 reference_pending。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
