# paper_c23cfabbd34b087f — paper-specific V2 plan

How do fused-ring topology and substituent identity affect the low-energy electronic character of the four supplied hydrocarbon models, and what evidence explains the differences or their absence?

## source_documents

[
  {
    "path": "papers/paper_c23cfabbd34b087f/documents/main.pdf",
    "sha256": "fa0290c1e392f81471dfc4de8404e81cadc095b86119e7b8193f3746515ac8ec",
    "pages": [
      4,
      5
    ],
    "total_pages": 7
  },
  {
    "path": "papers/paper_c23cfabbd34b087f/documents/supplementary_001.pdf",
    "sha256": "93321601c20e91238a1ce663f271a078697c3397402d7d5e6dd0c150a2a8402c",
    "pages": [
      42,
      43,
      50,
      56
    ],
    "total_pages": 60
  }
]

## source_scope

Main pp.4–5 and SI pp.42–56 distinguish unoxidized 1M/2M electronic structures, aromaticity and oxidized 2M-prime optical products. The task concerns the four source computational 1M/2M models only; source optical spectra of oxidized 2M-prime are not observations of unoxidized 2M.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "relaxed_series",
    "frozen_scaffold",
    "calibrated_interpretation"
  ],
  "fixed_schema_keys": {
    "relaxed_series": [
      "1M_OMe",
      "1M_TIPS",
      "2M_OMe",
      "2M_TIPS"
    ],
    "frozen_scaffold": [
      "1M_OMe",
      "1M_TIPS",
      "2M_OMe",
      "2M_TIPS"
    ],
    "calibrated_interpretation": [
      "calibration_object",
      "calibration_records",
      "active_space_or_independent_diagnostic",
      "diagnostic_file",
      "topology_effect",
      "substituent_relaxation_effect",
      "electronic_model_effect",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "移除固定 CS/BS/T、共同骨架冻结及指定高层校准路径；拓扑/取代范围和可比较量仍严格定义，允许证据支持的 BS 坍缩与不同自旋处理。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Determine a defensible description of electronic character and relevant low-energy states for these topologies.",
  "Choose comparisons that distinguish topology and substitution effects without comparing unequal-composition total energies.",
  "Decide how to establish the stability and uncertainty of the resulting electronic explanation."
]

## public_input_changes

[
  "Keep the four complete mapped graphs and explicit truncation meaning; remove allowed_multiplicities, answer coordinates and fixed common-scaffold freeze map.",
  "Remove CS/BS/T panel enums, prescribed two BS starts, compulsory frozen-geometry and active-space matrices from schema/evaluator."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors optimized the four truncated models using Gaussian09 (U)B3LYP-D3/def2-SVP and checked frequencies (SI p.42). Long alkoxy chains were replaced by OMe and the TIPS computational group by ethynyl-SiH3. They used GIAO NICS(1)zz and EDDB to interpret aromaticity. Main p.4 reports OSS below CS for 2M_OMe/2M_TIPS by 4.5/5.6 kcal/mol and above CS for 1M_OMe/1M_TIPS by 4.1/3.3 kcal/mol. These are conditional author results, not universal acceptance bounds. Coordinate-section energies include ZPVE and must not be conflated with raw SCF energies. The source TD-DFT optical comparison includes oxidized 2M-prime, a different molecule. V1 added fixed BS seeds, common-scaffold interventions and extra method controls; these were not the source protocol.

## existing_evidence_reuse

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
  "一部分历史最低点、稳定性和垂直三重态证据可参考；全模型弛豫/独立校准未完整，数值容差不可机械继承。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
