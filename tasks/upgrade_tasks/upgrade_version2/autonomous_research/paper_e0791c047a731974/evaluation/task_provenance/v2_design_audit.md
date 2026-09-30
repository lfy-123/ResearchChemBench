# paper_e0791c047a731974 — paper-specific V2 plan

What molecular electronic evidence can explain differences in triplet sensitization among IR780, Cy1 and Cy2, and does it support their energetic compatibility with rubrene in chloroform?

## source_documents

[
  {
    "path": "papers/paper_e0791c047a731974/documents/main.pdf",
    "sha256": "4d136fb1b060c26a81c3dacdb397eed6c4c913f61d95b8ada7262e801a1a91c1",
    "pages": [
      4,
      5,
      6
    ],
    "total_pages": 9
  },
  {
    "path": "papers/paper_e0791c047a731974/documents/supplementary_001.pdf",
    "sha256": "06893f8d0c9056eba31a55a3c726a76bba621a0d20c80d6eb9fe11f9d35f1d02",
    "pages": [
      7,
      8,
      24,
      30
    ],
    "total_pages": 45
  }
]

## source_scope

Main pp.4–6 and SI pp.7–8 compare cyanine excited states and rubrene triplet matching. The bounded study uses the three electronically investigated source sensitizers plus rubrene, not the full Cy3/IR806 device/material study or an absolute upconversion-yield prediction.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "sensitizer_states",
    "rubrene_energy_cycle",
    "geometry_and_method_test"
  ],
  "fixed_schema_keys": {
    "sensitizer_states": [
      "IR780",
      "Cy1",
      "Cy2"
    ],
    "rubrene_energy_cycle": [
      "rubrene_S0_record",
      "rubrene_S1_record",
      "rubrene_T1_record",
      "rubrene_E_S1_eV",
      "rubrene_E_T1_eV",
      "annihilation_balance_eV",
      "sensitizers",
      "state_following_file",
      "evidence_files"
    ],
    "geometry_and_method_test": [
      "Cy2_frozen",
      "Cy2_released_record",
      "torsion_mapping_file",
      "geometry_effect",
      "relativistic_basis_effect",
      "heavy_atom_density_file",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "去除 Cy2 六扭角平面化、固定 SOC 根窗/方法和全矩阵；让 agent 选择支持源范围内敏化主张的能量/态/动力学证据，局部量不能直接证明量子产率。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose a molecular description and electronic evidence capable of explaining the observed sensitization differences.",
  "Determine what state identities and energy definitions can support donor–acceptor compatibility.",
  "Assess whether an inferred molecular effect is distinguishable from structural, environmental or method differences."
]

## public_input_changes

[
  "Keep complete sensitizer/rubrene atom-mapped identities and necessary experimental context.",
  "Remove Cy2_planar_control, fixed state/SOC/adiabatic panels and prescribed geometry/method perturbations. Do not expose source T2 pathway assignment or predicted triplet energies to AR."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

Gaussian16 calculations used B3LYP/6-31G(d,p) with SMD chloroform, SDD for iodine and def2TZVP for selenium; iodide counterions were omitted (SI pp.7–8). The authors used DFT ground-state structures, TDDFT excited-state calculations and Multiwfn electron–hole analysis, emphasizing selenium contributions. Main p.6 reports UDFT adiabatic T1 energies1.02,1.02,1.09 eV for IR780,Cy1,Cy2 and1.00 eV for rubrene, noting systematic underestimation relative to rubrene experiment1.14 eV. The authors propose S1→T2 ISC from energy gaps and a heavy-atom SOC argument; the cited source does not provide a direct molecular SOC matrix proving the rate. Reproduce this disclosed baseline or justify substitutes; explicit SOC, planar constraints and matched extra controls in V1 were later validation, not source measurements.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "Cy2非相对论SOC pilot已原生完成并解析，初次MPI失败保留。尚未完成相对论/方法校准及敏化剂和rubrene矩阵。",
    "unfinished_scientific_or_input_work": [
      "IR780/Cy1及Cy2态密度对应",
      "同条件rubrene/供体绝热能量循环",
      "重元素算符与冻结几何/方法敏感性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_e0791c047a731974/evaluation/reference_validation_plan.md",
  "applicability": "仅 Cy2 非相对论先导不覆盖重元素方法或整套受体循环；已有记录仅按其适用范围复用。",
  "new_scientific_calculations_performed": false,
  "raw_evidence": [
    {
      "case_id": "cy2_soc_nr_pilot_v1",
      "job_id": "hpc-job-c00cf410-6f3e-4680-9dda-645f21e91985",
      "status": "engine_failed",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/outputs/cy2_soc_nr_pilot",
      "normal_termination": false,
      "allocated_core_hours": 0.004425713344891038
    },
    {
      "case_id": "cy2_soc_nr_pilot_v1_a02",
      "job_id": "hpc-job-b626567d-c05e-4962-a404-5b0f5c5ef34c",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/outputs/cy2_soc_nr_pilot_v1_a02",
      "normal_termination": true,
      "allocated_core_hours": 1.6260992548531956
    }
  ],
  "evidence_audits": [
    "docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/report/cy2_soc_nr_pilot_v1_a02_native_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/legacy/native_log_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/legacy/attempt_inventory.json"
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
  "仅 Cy2 非相对论先导不覆盖重元素方法或整套受体循环；已有记录仅按其适用范围复用。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
