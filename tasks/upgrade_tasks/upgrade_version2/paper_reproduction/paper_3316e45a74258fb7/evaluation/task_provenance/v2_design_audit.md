# paper_3316e45a74258fb7 — paper-specific V2 plan

How does the donor substitution pattern affect the molecular excited-state behavior of TD-2T, CD-2T and TD-2C, and which aspects of their differing optical response can be supported by molecular evidence?

## source_documents

[
  {
    "path": "papers/paper_3316e45a74258fb7/documents/main.pdf",
    "sha256": "0061ebb5bb7ee96d72e00f384ab0f89006a46759102ba391287f86108303c5a9",
    "pages": [
      2,
      3,
      4
    ],
    "total_pages": 7
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_3316e45a74258fb7.publisher_si.docx",
    "sha256": "68ab54b52aaf11ee797b532d7460dcef01195e48d43dc9abf1897f82b7cbe2e1",
    "sections": "Relevant methods, experimental observations and identity blocks; see source review."
  }
]

## source_scope

Main pp.2–4 defines three DCTP derivatives and connects donor substitution to orbital/state character and solution photophysics. True publisher SI DOCX Experimental/Synthesis and Figures S3–S6 specify identities and calculations. The molecular analysis is a bounded part of a larger OLED study.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "vertical_matrix",
    "relaxation_matrix",
    "causal_comparison"
  ],
  "fixed_schema_keys": {
    "vertical_matrix": [
      "TD_2T",
      "CD_2T",
      "TD_2C"
    ],
    "relaxation_matrix": [
      "TD_2T",
      "CD_2T",
      "TD_2C"
    ],
    "causal_comparison": [
      "donor_change_at_11",
      "donor_change_at_3_6",
      "torsion_relaxation_effect"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "移除统一 45° 扭转、六格 SOC、预先固定根窗和 S1/T1 路线；供体身份保留，态窗口、构象搜索和判别由 agent 选择，声称的物理态仍须可追踪。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose relevant molecular representations and electronic states for the optical question.",
  "Select evidence to connect donor placement with observed differences.",
  "Determine which inferences survive uncertainty and which require environmental or kinetic information."
]

## public_input_changes

[
  "Retain complete mapped graphs and systematic chemical names; remove source coordinate claims, fixed excitation multiplicities and computational fragment assignments.",
  "Remove torsion_control_mapping.json, 45-degree interventions, minimum conformer count and six-cell output matrix.",
  "Supply measured absorption/PL context without theoretical state labels, computed gaps or author winner."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

Main pp.2–4 describes Gaussian09 B3LYP/6-31G(d,p) S0 optimization and TD-DFT S1/T1 energies, with Multiwfn3.8 NTO analysis. The SI Experimental section instead writes B3LYP/6-31(d); this basis-description discrepancy must be recorded rather than silently erased. The authors attribute donor-dependent optical behavior to donor–acceptor geometry, charge-transfer character and low singlet–triplet separations. Main p.4 reports calculated TD-2T gap 0.34 eV and discusses CT/LE/HLCT characters; spectroscopic gaps at 77 K are a separate experiment, not identical to vertical TDDFT. The source also discusses device performance, which exceeds what a molecular calculation alone can reproduce. Reproduce a clearly stated interpretation of the disclosed molecular baseline and explain deviations. The old fixed-45-degree and paired-conformer benchmark design was added later and is not an author requirement.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "TD2T旧128原子S0端点图与378个正频率已审，最低5.1761cm⁻¹；Gaussian微小力接受但最大位移阈值未过。复用后5S/5T原生SOC完成，S1=2.142275eV、f=0.76363396；S1/T1 SOC在0.01cm⁻¹打印精度为零，不能当物理精确零。完整三模型矩阵未完成。",
    "unfinished_scientific_or_input_work": [
      "三布局完整图、构象及基线端点精审",
      "S1/T1弛豫及曲率，垂直/绝热分列",
      "同扭转SOC/NTO干预及CT敏感方法控制"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_3316e45a74258fb7/evaluation/reference_validation_plan.md",
  "applicability": "可复用经审计的 TD2T 基态及部分 SOC；三布局激发态弛豫与方法稳健性未完整，不强制先算齐再开发。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "path": "docs/upgrade_tasks_verification/group_5/papers/paper_3316e45a74258fb7/report/td2t_soc5_native_audit.json",
    "scope": "Existing TD-2T native excited-state/SOC parsing can establish feasibility for that object; it does not validate the other structures or source basis discrepancy."
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
  "可复用经审计的 TD2T 基态及部分 SOC；三布局激发态弛豫与方法稳健性未完整，不强制先算齐再开发。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
