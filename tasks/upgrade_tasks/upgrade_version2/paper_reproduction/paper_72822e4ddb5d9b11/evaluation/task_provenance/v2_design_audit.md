# paper_72822e4ddb5d9b11 — paper-specific V2 plan

What electronic-state and metal–ligand bonding description is supported for the supplied nickel carbaporphyrin complex, and how securely can it be distinguished from competing descriptions?

## source_documents

[
  {
    "path": "papers/paper_72822e4ddb5d9b11/documents/main.pdf",
    "sha256": "69805929b078375456ecab8ac4c7dcc9f466b143f34fe8a29b9749bfefc6a7bb",
    "pages": [
      1,
      4,
      5
    ],
    "total_pages": 9
  },
  {
    "path": "papers/paper_72822e4ddb5d9b11/documents/supplementary_001.pdf",
    "sha256": "9a3e4f4ed9c562f45721aeab487b6df25be409086c6221fad642551526106ac1",
    "pages": [
      10,
      11
    ],
    "total_pages": 105
  }
]

## source_scope

Main pp.2–4 reports complex4 with two axial chloride ligands, structure/spectroscopy and electronic-state analysis. SI S10–S11 contains computational methods and metric/state comparisons. The source itself separates formal oxidation from a unique physical charge or covalency assignment.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "state_matrix",
    "geometry_control",
    "interpretation"
  ],
  "fixed_schema_keys": {
    "state_matrix": [
      "B3LYP",
      "BP86"
    ],
    "geometry_control": [
      "B3LYP",
      "BP86"
    ],
    "interpretation": [
      "method_gap_contrast",
      "metal_spin_comparison_file",
      "ligand_spin_comparison_file",
      "occupation_comparison_file",
      "electronic_description",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "保留实际组成和电子数，让电子态候选、波函数方法与比较设计开放；不把两泛函×三态固定矩阵继续作为私有必过路径。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Generate and test plausible electronic descriptions of the specified complex.",
  "Choose evidence that distinguishes state assignment from formal electron-counting labels.",
  "Determine which bonding conclusions are robust and which remain method-dependent."
]

## public_input_changes

[
  "Convert source optimized XYZ to atom-resolved connectivity only, preserving all 165 atoms and six Ni coordination neighbors; withhold coordinates that encode the author endpoint.",
  "Remove closed/open/triplet candidate menu, B3LYP/BP86 mandatory pair and copied experimental/theoretical winner annotations from public task and schema."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors tested closed-shell singlet, open-shell singlet and triplet initial guesses with B3LYP and BP86 in ORCA. SI S10 specifies def2-TZVP on Ni and its six directly coordinated Cl/N/C atoms, def2-SVP elsewhere; source geometries were checked by frequencies. Open-shell guesses collapsed to closed-shell singlets, and the BP86 triplet lay 25.1 kcal/mol higher; TableS1 compares bond lengths with crystallography. Main p.4 discusses occupied t2g-derived orbitals and covalent eg combinations, favors a formal Ni(IV) limiting description but explicitly cautions that physical oxidation/σ-noninnocence is not unequivocally resolved. Reproduce or justify deviations from this disclosed baseline; the shared result standard accepts scientifically supported refutation and does not impose its winner. TDDFT/SMD(toluene) and aromaticity analyses are source supplementary work, not mandatory additions to this electronic-state task.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 6,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_6/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "733d1efabb39deac239f2318d48fc7385a9faa720b2a206bfeede892b4a158fa",
    "recorded_at_utc": "2026-09-28T15:08:44.745913+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "完整Ni 165原子B3LYP CS和T均完成独立梯度、同几何489正频和波函数稳定性；T RMS/MAX力3.9093e-6/2.46145e-5 Eh/bohr，最低9.17823cm-1。绝热T−CS=32.21792kcal/mol，垂直35.18214；BP86两独立BS与自由CS/T矩阵继续",
    "unfinished_scientific_or_input_work": "完成BP86独立BS、自由CS/T优化频率、各自稳定性与完整密度/态序对照；整篇仍needs_work",
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_72822e4ddb5d9b11/evaluation/reference_validation_plan.md",
  "applicability": "已有部分 B3LYP 结构/稳定性/489 模式证据；另一方法完整矩阵尚待校准，后续按新问题评估可复用性。",
  "new_scientific_calculations_performed": false,
  "raw_reference": {
    "paths": [
      "docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/report/CS_stability_result.json",
      "docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/report/BS_flipNi_result.json",
      "docs/upgrade_tasks_verification/group_6/papers/paper_72822e4ddb5d9b11/report/B3LYP_adiabatic_gap.json"
    ],
    "scope": "State stability/collapse and matched-method energy audits are reusable at their exact geometry and settings; not proof of universal covalency or a new V2 reference."
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
  "已有部分 B3LYP 结构/稳定性/489 模式证据；另一方法完整矩阵尚待校准，后续按新问题评估可复用性。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
