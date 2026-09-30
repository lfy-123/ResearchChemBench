# Reference validation and reuse

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

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

Existing converged Ni/Al/B2/L12 native outputs and nine magnetic/k-mesh/smearing checks support bulk-reference feasibility. Ferromagnetic Ni differs materially from an earlier near-zero-moment reference; reusing an old reservoir is unsafe without state matching. Genuine surface/pathway validation and semantic calibration remain pending; no new runs are launched.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Main p.9 larger-than9 Å supercells,43 Bohr effective crystal size and GW-PAW/Lightshow/core-hole settings describe Ni L-edge NEXAFS. They are not a full disclosed NEB/defect protocol. The800 °C/0.001 Torr H2 ex-situ condition and900 °C in-situ preparation condition on p.9 are distinct, as is UHV NiAl(100) annealing. Source endpoint files are unavailable; transparent source-bounded model construction remains possible.
