# paper_eda19e7c8edd4b39 — paper-specific V2 plan

What atomistic energetic explanation is consistent with Ni-rich surface precipitation during annealing of near-stoichiometric B2 NiAl, and what can that explanation establish about bulk–surface coupling?

## source_documents

[
  {
    "path": "papers/paper_eda19e7c8edd4b39/documents/main.pdf",
    "sha256": "c9db7c7771ae5db69a41f10aa75967d88c1932e7146b1929d0f245a61e9da6bf",
    "pages": [
      4,
      5,
      6,
      7,
      8,
      9
    ],
    "total_pages": 11
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_eda19e7c8edd4b39.publisher_si.pdf",
    "sha256": "59d72a5ef0ce8a23a1aeb442f43e5c69e8b78eca9bae8db3ab84ff48185e1239",
    "sections": "Actual publisher supplementary figures S1–S6; papers-directory supplementary_001 is a peer-review file and is not used as the scientific SI.",
    "pages": [
      1,
      2,
      3,
      4,
      5,
      6,
      7
    ]
  }
]

## source_scope

Main pp.4–9 and genuine publisher SI Figs.S3–S6 report NiAl surface enrichment/precipitation and model defect/surface energetics. The bounded task concerns a defensible atomistic explanation of the observed phenomenon, not a full finite-temperature growth simulation, oxidation mechanism or fitted experimental diffusion rate.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "bulk_vacancies",
    "surface_cycles",
    "phase_and_convergence"
  ],
  "fixed_schema_keys": {
    "bulk_vacancies": [
      "reservoirs",
      "cells"
    ],
    "surface_cycles": [
      "100_Ni",
      "100_Al",
      "110_mixed"
    ],
    "phase_and_convergence": [
      "Ni3Al_record",
      "Ni3Al_E_per_formula_eV",
      "Ni3Al_grand_potential_eV",
      "phase_reference_ledger_file",
      "thickness_sensitivity",
      "vacuum_sensitivity",
      "kpoint_or_cutoff_sensitivity",
      "bulk_vs_surface_comparison_file",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "不强制 Ni-rich 储库、三种终止、7/9 层、15/20 Å 真空和指定吸附位点全集；agent 自选合理表面/相模型并验证主张，守恒、磁性和共同能量口径保留。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Choose atomistic models and comparisons that can explain enrichment despite the starting surface composition.",
  "Determine energy references and which aspects of bulk–surface coupling are actually distinguishable.",
  "Decide whether the evidence supports a thermodynamic tendency, a kinetic route or only a narrower conditional claim."
]

## public_input_changes

[
  "Retain only ideal crystal identity/start resources and measured setting; remove named defect/surface-control matrix, forced Ni-rich reservoir, supercell/layer/vacuum counts and adsorption-site search list.",
  "Rewrite the lattice metadata to identify benchmark guesses honestly; remove the old POSCAR header implying an exact source structure. Phase identity remains legitimate experimental fact, while source energetics and exchange pathway are PR/private."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

Main pp.7–9 uses VASP to interpret lower Ni than Al vacancy formation energy (source0.98 versus1.20 eV), and an Al adatom replacing a surface Ni antisite on Al-terminated NiAl(100) (−0.31 eV change,0.55 eV NEB barrier). Source bulk diffusion pathways do not simply imply universally faster Ni motion; local vacancies/antisites matter. The main methods describe VASP, NEB and ELF/VESTA; the detailed PBE/GW-PAW/core-hole/Lightshow settings on p.9 specifically concern NEXAFS and must not be falsely claimed as a complete disclosed defect-energy protocol. The provided genuine SI contains experimental Figs.S1–S6, not a full slab input archive. The source author endpoint files are not supplied here; reproduce the disclosed baseline with transparently generated models or explain a justified substitute. V1 slab counts, forced reservoir window and phase-control matrix are later benchmark additions.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "旧八VASP端点已审；同晶胞铁磁Ni比旧近零磁态低0.06086eV/atom。新Ni/Al/B2/L12四种520eV/k12晶胞全收敛，残余压力≤0.01kbar；全部九个k16/展宽/独立Ni磁种子静态控制原生完成。需要合并数值收敛及相稳定审查，尚无新表面矩阵。",
    "unfinished_scientific_or_input_work": [
      "Ni/Al/B2/L12晶胞、磁性与统一能量/展宽/k点校准",
      "两尺寸空位与合格Ni-rich储库；旧3³/4³等价控制映射",
      "三终止表面守恒循环、位点搜索、层数/真空/k点和L12比较"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_eda19e7c8edd4b39/evaluation/reference_validation_plan.md",
  "applicability": "已有统一晶胞/磁种子和收敛控制原生输出，尚缺有效表面矩阵；静态能量不证明有限温度动力学。",
  "new_scientific_calculations_performed": false,
  "raw_evidence": [
    {
      "case_id": "nial_fcc_ni_fm_fixedcell450_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_fcc_ni_fm_fixedcell450_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.044719240326020454
    },
    {
      "case_id": "nial_ni_fm_cell520_k12_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_ni_fm_cell520_k12_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.19631422899249526
    },
    {
      "case_id": "nial_al_cell520_k12_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_al_cell520_k12_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.05398976450579034
    },
    {
      "case_id": "nial_b2_cell520_k12_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_b2_cell520_k12_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.06865401623149713
    },
    {
      "case_id": "nial_l12_cell520_k12_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_l12_cell520_k12_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.18729868717698586
    },
    {
      "case_id": "nial_common_cell_audit_v1",
      "job_id": null,
      "status": "finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_common_cell_audit_v1",
      "normal_termination": null,
      "allocated_core_hours": 5.7351796680854425e-05
    },
    {
      "case_id": "nial_ni_fm_static520_k16_s010_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_ni_fm_static520_k16_s010_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.14869979952565499
    },
    {
      "case_id": "nial_ni_fm_static520_k16_s005_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_ni_fm_static520_k16_s005_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.14999788981344964
    },
    {
      "case_id": "nial_ni_fm_static520_k16_s010_seed05_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_ni_fm_static520_k16_s010_seed05_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.15213155133028824
    },
    {
      "case_id": "nial_al_static520_k16_s010_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_al_static520_k16_s010_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.05945872850923074
    },
    {
      "case_id": "nial_al_static520_k16_s005_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_al_static520_k16_s005_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.053020772172345056
    },
    {
      "case_id": "nial_b2_static520_k16_s010_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_b2_static520_k16_s010_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.051269600292046864
    },
    {
      "case_id": "nial_b2_static520_k16_s005_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_b2_static520_k16_s005_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.05045512754884031
    },
    {
      "case_id": "nial_l12_static520_k16_s010_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_l12_static520_k16_s010_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.14179921874569523
    },
    {
      "case_id": "nial_l12_static520_k16_s005_v1",
      "job_id": null,
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/outputs/nial_l12_static520_k16_s005_v1",
      "normal_termination": true,
      "allocated_core_hours": 0.13757194204255938
    }
  ],
  "evidence_audits": [
    "docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/report/common_cell_native_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/report/fcc_Ni_magnetic_start_control.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/report/fcc_Ni_reservoir_impact.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/legacy/eight_vasp_endpoint_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/legacy/native_log_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_eda19e7c8edd4b39/legacy/attempt_inventory.json"
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
  "已有统一晶胞/磁种子和收敛控制原生输出，尚缺有效表面矩阵；静态能量不证明有限温度动力学。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
