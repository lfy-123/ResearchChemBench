# paper_2c439196c2f349c9 — paper-specific V2 plan

What can the supplied time- and intensity-dependent diffraction-ring observations establish about the nonlinear optical response of INP in chloroform, and which physical properties remain unidentifiable from those observations?

## source_documents

[
  {
    "path": "papers/paper_2c439196c2f349c9/documents/main.pdf",
    "sha256": "1470f926af7414723c25e43c91ebe0fc964aa269e3943752deb4d469907ae3e7",
    "pages": [
      3,
      9,
      10,
      11
    ],
    "total_pages": 12
  },
  {
    "path": "papers/paper_2c439196c2f349c9/documents/supplementary_001.pdf",
    "sha256": "2f1a3ca284a417a10d01c535fe535c5fcfc4d3f39d1ad9391a835f06094b2669",
    "pages": [
      6,
      7
    ],
    "total_pages": 7
  }
]

## source_scope

Main pp.2–3 specify INP, chloroform concentrations, 532 nm CW excitation and a 1 mm solution cell. Main pp.9–10 Figures 6 and 10 report intensity and time observations; SI S7–S8 distinguishes absorption and Z-scan data. The source attributes temporal distortion to heating; this task tests what the accessible data actually justify.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "observations",
    "model_comparison",
    "identifiability"
  ],
  "fixed_schema_keys": {
    "observations": [
      "measured_points",
      "beam_waist_m",
      "thickness_m",
      "instrument_response_file",
      "thermal_parameter_bounds_file"
    ],
    "model_comparison": [
      "instantaneous",
      "thermal",
      "mixed"
    ],
    "identifiability": [
      "parameter_profile_file",
      "correlation_matrix",
      "electronic_fraction_interval",
      "held_out_predictions_file",
      "held_out_residuals_file",
      "memory_test",
      "identified",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "不强制瞬时/热/混合三个模型或固定分数剖面。围绕源观测提出可辨识的有限问题，让 agent 自选模型和检验；公开数据全可读时只计回顾验证，不宣称盲测。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose response models justified by the observed variables and experimental conditions.",
  "Decide which fitted properties are identifiable given calibration and measurement limits.",
  "Select tests of predictive adequacy and uncertainty appropriate to the available observations."
]

## public_input_changes

[
  "Preserve Fig.10 measurement markers and reading uncertainty while removing fixed instantaneous/thermal/mixed model menu, compulsory held-out protocol and old blocked matrix.",
  "Add already-digitized Fig.6 discrete measurements from the read-only verification archive with source/provenance; remove absolute source path and inference-oriented input_gate.",
  "Keep neutral INP chemical identity and actual experiment conditions; no author fitted time constants or fitted curves."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors measured SSPM ring counts under 532 nm CW illumination and related phase to rings approximately by Δφ≈2πN and Δφ=k d Δn. They studied intensity dependence and temporal growth at 50 mW for three solution concentrations and interpreted delayed growth/vertical distortion as thermal effects. Main p.9 reports fitted time constants of 67.7, 78.2 and 107.5 ms; these are fit outputs, not additional observations. The authors compared SSPM apparent nonlinear index (about 10^-6 cm²/W) with Z-scan values (about 10^-8 cm²/W). Reproduce the disclosed data analysis as far as its inputs permit and identify uncertainty from unavailable calibration. The old benchmark three-way model menu and compulsory hold-out were later additions, not the original procedure. Source main pp.2–3,9–10; SI S7–S8.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "blocked_with_evidence",
    "completed_evidence_summary": "27个时间标记及22个功率标记已溯源；条件拟合、残差/参数剖面/保留点检查已实算。独立开光/仪器响应、束腰关联及热校准缺失，不能给唯一物理电子比例。",
    "unfinished_scientific_or_input_work": [
      "独立SSPM开光/仪器响应及束腰约定与测量条件关联",
      "热扩散/吸收/热光参数与实验误差独立校准；目前正式源材料不足"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_2c439196c2f349c9/evaluation/reference_validation_plan.md",
  "applicability": "验证目录已有 Figure 6 的 22 个功率标记，V1 尚未纳入；独立开光/响应、束腰关联、热参数及测量误差仍缺，不能把数据增加当作唯一物理比例已可识别。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "path": "docs/upgrade_tasks_verification/group_5/papers/paper_2c439196c2f349c9/report/results.json",
    "scope": "Existing model fits and identifiability analysis are conditional benchmarks, not a unique physical decomposition or a required model menu."
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
  "验证目录已有 Figure 6 的 22 个功率标记，V1 尚未纳入；独立开光/响应、束腰关联、热参数及测量误差仍缺，不能把数据增加当作唯一物理比例已可识别。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
