# paper_e31cc7bc7b21b610 — paper-specific V2 plan

What electronic and structural features can account for the short Ir–Ir bond in the supplied iminoxolene dimer, and how far can a molecular model support that explanation?

## source_documents

[
  {
    "path": "papers/paper_e31cc7bc7b21b610/documents/main.pdf",
    "sha256": "d10f786f46a66110c6c194aac86b204d3e34dc8be7d608d5c2557be4dd91f5d0",
    "pages": [
      4,
      8,
      9,
      10
    ],
    "total_pages": 12
  },
  {
    "path": "papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf",
    "sha256": "8160f45b57e772b48642e1e20d0ddddb8e64c97146b96bb942b33584b6cae2ec",
    "pages": [
      20,
      22,
      27,
      28,
      29,
      30
    ],
    "total_pages": 30
  }
]

## source_scope

Main pp.4,8–9 and SI pp.20,22,27–30 investigate experimental (A,C)-(Egan)2Ir2 and a gas-phase54-atom (Hap)4Ir2 computational model. The task isolates metal–metal bonding and model adequacy; it does not require full metalation/reduction pathways or all source complexes.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "dimer_states",
    "fragment_interventions",
    "bonding_evidence"
  ],
  "fixed_schema_keys": {
    "dimer_states": [
      "Egan2Ir2",
      "egan2Ir2"
    ],
    "fragment_interventions": [
      "Egan2Ir2",
      "egan2Ir2"
    ],
    "bonding_evidence": [
      "retained_atom_mapping_file",
      "orbital_population_grid_file",
      "bond_order_grid_file",
      "density_rearrangement_grid_file",
      "truncation_effect",
      "twist_effect",
      "method_or_fragment_sensitivity",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "重新选择同源成键子问题，解除强制中性双重态分片、0.2/0.5 Å 距离、30° 扭转及两尺寸全集；保留真实二核身份、电子数和任何所采用分解的适用边界。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose a chemically faithful molecular representation and establish its limits for the observed bond.",
  "Develop an electronic explanation and choose evidence capable of discriminating it from a short-distance correlation.",
  "Determine which structural and electronic uncertainties materially affect the inference."
]

## public_input_changes

[
  "Retain full Egan chemical identity and add the actual source54-atom Hap core as coordinate-free connectivity. Remove114-atom paired-truncation requirement and retained-heavy control map.",
  "Remove predefined singlet/BS/triplet panel, neutral-doublet fragment decomposition and +0.2/+0.5 Å/30-degree interventions. Experimental bond length remains legitimate public evidence; source S4/C2h results stay PR/private."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

Source main p.4 used gas-phase Gaussian16 B3LYP, SDD on Ir and6-31G* on other atoms. For the dimer the actual calculated model is (A,C)-(Hap)4Ir2, Hap=1,2-C6H4(NH)O,54 atoms; egan truncations were used for other mononuclear complexes. Main pp.8–9 argues that ligand redox activity and relative orientation create net Ir–Ir π bonding. The source S4 minimum has Ir–Ir2.599 Å; the constrained C2h structure has2.724 Å and9.7 kcal/mol higher free energy. SI pp.22,29 identify C2h as a first-order saddle (17.1i cm−1), not a second stable conformer. Frequency plots use scaling0.9614; SI coordinate energies are raw optimized energies, not automatically the9.7 kcal/mol free-energy difference. The experimental2.5584(4) Å and crude MOS-derived2.34 bond-order estimate are conditional observations/interpretations, not mandatory computational truth. The V1 full/egan pair and fixed perturbations are benchmark additions, not the published Hap protocol.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 6,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_6/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "733d1efabb39deac239f2318d48fc7385a9faa720b2a206bfeede892b4a158fa",
    "recorded_at_utc": "2026-09-28T15:08:44.745913+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "正确114原子截短二核先导已从平台停止后的最后有效SCF几何恢复，作业3fbad7fc在运行；完整210原子模型及自旋对照已准备，受先导质量门约束",
    "unfinished_scientific_or_input_work": "先导验证后做完整/截短、关联及自旋矩阵",
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_e31cc7bc7b21b610/evaluation/reference_validation_plan.md",
  "applicability": "114 原子截短模型在途先导不应冒充源 Hap 或完整 210 原子验证；V2 模型取舍先做来源/资源论证，避免无必要增加整套计算。",
  "new_scientific_calculations_performed": false,
  "source_model_correction": "Historical114-atom work remains a benchmark-added model only; source54-atom Hap model and210-atom experiment are distinguished."
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
  "114 原子截短模型在途先导不应冒充源 Hap 或完整 210 原子验证；V2 模型取舍先做来源/资源论证，避免无必要增加整套计算。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
