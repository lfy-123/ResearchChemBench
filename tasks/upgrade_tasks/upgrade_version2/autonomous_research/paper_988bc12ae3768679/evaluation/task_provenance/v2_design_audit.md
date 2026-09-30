# paper_988bc12ae3768679 — paper-specific V2 plan

What molecular changes can account jointly for the supplied acid–base-dependent optical and NMR observations of dye 2a, and how uniquely do those observations identify the responsive species?

## source_documents

[
  {
    "path": "papers/paper_988bc12ae3768679/documents/main.pdf",
    "sha256": "8ee6c2620ae4107f7fd8043982eb478ffa01714734e69416a7b186e9ff32e189",
    "pages": [
      4,
      5,
      6
    ],
    "total_pages": 10
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_988bc12ae3768679.publisher_si.docx",
    "sha256": "b3633cc3dbdbae1fe21da6413596b8434189d1a6f4b55dafeeaa6975bc3acedf",
    "sections": "Relevant methods, experimental observations and identity blocks; see source review."
  }
]

## source_scope

Main pp.4–6 and true SI DOCX NMR simulation/TableS2 and TDDFT sections study the acid/base response of 2a. The parent is iso-DPP, not the usual DPP topology. The source proposes OH-centered protonation/deprotonation but reports an acid NMR discrepancy; V2 leaves species generation and explanation to the agent.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "candidate_registry",
    "joint_evidence",
    "thermodynamic_and_robustness"
  ],
  "fixed_schema_keys": {
    "candidate_registry": [
      "candidates",
      "parent_record",
      "atom_conservation_table_file"
    ],
    "joint_evidence": [
      "comparisons",
      "uncertainty_model_file",
      "shielding_calibration_file",
      "spectral_assignment_file",
      "populations",
      "joint_residual_analysis_file"
    ],
    "thermodynamic_and_robustness": [
      "proton_cycles",
      "solvent_or_reference_contrast",
      "candidate_ordering_file",
      "mixture_identifiability_file",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "candidate_seeds.json 和固定六标签直接规定解法，V2 需用父体、已知组成/环境和观测替换强制候选全集，允许自主生成候选/混合物及撤回；跨质子数比较仍须守恒和共同参考。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Generate chemically valid species and decide which conditions and observables can discriminate them.",
  "Choose a model that can connect both optical and NMR behavior to molecular change.",
  "Determine whether the data resolve a unique assignment or support only a family of explanations."
]

## public_input_changes

[
  "Retain parent mapped graph; remove all six mandatory candidate seeds, fixed ±2 proton/charge enum and two-conformer requirement.",
  "Publish measurement values with condition/source distinction; withhold author endpoint coordinates, calculated shifts/energies and site winner.",
  "Replace required joint-residual matrix with unconstrained record/quantity/claim fields and claim-triggered balance requirements."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors proposed protonation/deprotonation of phenolic OH groups and regarded neutral azo–hydrazone tautomerism as unimportant for the chromatic switch (main Fig3/pp.5–6). They used CAM-B3LYP/6-31+G(d), TDDFT in gas and cLR-PCM water, with B3LYP comparison in SI. NMR calculations used GIAO at CAM-B3LYP/6-31+G(d), PCM DMSO and δ=σ(TMS)−σ(compound), Gaussian16 B.01. The acid calculated shift 7.98 ppm differs from observed6.95 ppm, while the source retained its proposed interpretation. Reproduce this disclosed baseline where possible and assess rather than conceal that discrepancy. The old six-candidate, fixed-conformer and forced error-model design was a benchmark addition; alternatives and extra tests are now investigator-designed.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "六类原子映射候选各两套独立ETKDG/UFF初猜已生成并审查；12个UFF收敛仅属输入准备。首个水相CAM-B3LYP优化被平台中断，恢复01因checkpoint缺几何FileIO失败；恢复02保持原独立坐标和方法重新启动，已登记排队，未重复活跃作业。",
    "unfinished_scientific_or_input_work": [
      "酸碱不同位点/键型与构象的实际搜索、坍缩证据",
      "中性标定及所有保留候选DMSO NMR/水相UV",
      "配平质子热力学循环、溶剂/方法稳健性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_988bc12ae3768679/evaluation/reference_validation_plan.md",
  "applicability": "十二个力场初猜只证明输入可构建；溶剂优化、光谱和质子循环参考仍待补，不把 UFF 收敛当科学最低点。",
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
  "十二个力场初猜只证明输入可构建；溶剂优化、光谱和质子循环参考仍待补，不把 UFF 收敛当科学最低点。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
