# paper_0cd74ae20ab933f3 — paper-specific V2 plan

Determine whether axial-pyridine substitution produces resolvable changes in the molecular magnetic exchange of the three supplied copper dimers, and what the evidence supports about that dependence.

## source_documents

[
  {
    "path": "papers/paper_0cd74ae20ab933f3/documents/main.pdf",
    "sha256": "e74146ea380e78e6bca3a1ca6eeb56ec4a16487ac58d2f169c0f92f64efea2aa",
    "pages": [
      6,
      7
    ],
    "total_pages": 10
  },
  {
    "path": "papers/paper_0cd74ae20ab933f3/documents/supplementary_001.pdf",
    "sha256": "dd357023aa433eeb80376b2b8f11e44a332edd2d95cdc8809838e6f3a448c222",
    "pages": [
      5,
      6,
      35,
      36
    ],
    "total_pages": 38
  }
]

## source_scope

The source compares H, methyl and methoxy axial pyridines in Cu2(AnCOO)4(4-RPy)2 molecular surrogates for 2R materials. Main PDF pp.6–7 and SI pp.S5–S6,S35–S36 establish spin exchange and methodological sensitivity. This task addresses molecular exchange, not thermochromism or collective MOF properties.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "exchange_matrix",
    "spin_calibration",
    "effect_comparison"
  ],
  "fixed_schema_keys": {
    "exchange_matrix": [
      "R_H",
      "R_CH3",
      "R_OCH3"
    ],
    "spin_calibration": [
      "representative",
      "geometry_record",
      "bs_record",
      "high_level_record",
      "bs_J_cm1",
      "high_level_J_cm1",
      "difference_cm1",
      "active_electrons",
      "active_orbitals",
      "natural_occupations",
      "orbital_file",
      "spin_definition",
      "evidence_files",
      "calibration_kind"
    ],
    "effect_comparison": [
      "Me_minus_H_relaxed",
      "OMe_minus_H_relaxed",
      "Me_minus_H_common_core",
      "OMe_minus_H_common_core",
      "OMe_minus_Me_common_core"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "将共同核心、固定 R_H 校准顺序和预设电子/几何二分从公开题面、study_scope、schema 和评分中释放；保留计量、自旋映射、J 的符号/倍数/简并度定义及主张对应的可靠性证据。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose an appropriate representation of the spin-coupled molecular states.",
  "Determine what evidence can resolve substitution dependence relative to uncertainty.",
  "Choose a defensible explanation, relevant tests and stopping conditions."
]

## public_input_changes

[
  "Retain H/Me/OMe molecular identities and four-bridge stoichiometry. Replace spin-multiplicity-3 starting instruction with formal ion accounting and unspecified molecular electronic-state determination.",
  "Remove study_scope, prescribed common-core/relaxed matrix, representative calibration and population target from public inputs and schema. Remove source outcomes/title/DOI from public metadata."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The source used Cu2(AnCOO)4(4-RPy)2 models for H/Me/OMe. It approximated the open-shell singlet geometry by triplet DFT optimization with B3LYP-D3BJ/def2-SVP in ORCA (RIJCOSX and def2/J). It obtained singlet/triplet spin-flip energies using multicollinear SF-TDDFT in PySCF-forge, with the same main functional/basis and def2-svp-jkfit; the reference is the Sz=1 triplet. The source defines J=E_S−E_T and reports approximately −335, −342 and −345 cm−1, with more electron-rich axial pyridines associated with stronger antiferromagnetic coupling. SI S35–S36 examines functional, TDA, basis and geometry dependence; these small differences are conditional, not universal tolerances. The experimental material fits are distinct from the molecular calculations. The old benchmark common-core decomposition and independent calibration matrix were later task additions, not the author protocol. These operations are not a mandatory route in this version. Source: main PDF pp.6–7; SI S5–S6 and S35–S36.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 6,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_6/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "733d1efabb39deac239f2318d48fc7385a9faa720b2a206bfeede892b4a158fa",
    "recorded_at_utc": "2026-09-28T15:08:44.745913+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "已有H同几何独立BS/泛函校准与SF历史复用。原自由T平台停止并完全释放后，保留精确配体图与轨道恢复；恢复作业70f6b162正在推进梯度。H/Me/OMe自由/固定核心矩阵待补",
    "unfinished_scientific_or_input_work": "H/Me/OMe 自由及固定核心矩阵和其余方法敏感性",
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_0cd74ae20ab933f3/evaluation/reference_validation_plan.md",
  "applicability": "现有 H 同几何 BS/方法记录可作有条件参考；三元系列和方法误差未齐不等于开发未完成。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "path": "docs/upgrade_tasks_verification/group_6/papers/paper_0cd74ae20ab933f3/report/H_VWN5_HS_BS_result.json",
    "scope": "Stable HS/BS and independent spin-flipped BS on the H source geometry; its linked raw outputs are usable only for that object/method. VWN5 versus source VWN3 and independent geometry remain limitations; not a three-member validation."
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
  "现有 H 同几何 BS/方法记录可作有条件参考；三元系列和方法误差未齐不等于开发未完成。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
