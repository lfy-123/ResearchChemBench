# paper_d8e5490cd9942f4f — paper-specific V2 plan

How does lanthanide identity affect the coordination and conformational preferences of [Ln-KHQ]+ in water for Ln = La, Tb and Lu, and how firmly can those preferences be established?

## source_documents

[
  {
    "path": "papers/paper_d8e5490cd9942f4f/documents/main.pdf",
    "sha256": "fb429f3736750e9ff6de3db9c2344f3d1d48ec30f2d02722847827935e1ea940",
    "pages": [
      3,
      5
    ],
    "total_pages": 9
  },
  {
    "path": "papers/paper_d8e5490cd9942f4f/documents/supplementary_001.pdf",
    "sha256": "5b3ec923bfc80b8f52bee9345254301777d3c07e79245f5d8f9ce976869030e7",
    "pages": [
      21,
      22
    ],
    "total_pages": 228
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_La_ECP46MWB.txt",
    "sha256": "017e317f666d45345552b816673a3b76498ae5baae2e4874803a5ae0a7374abc",
    "role": "Official originating-library molecular ECP/basis coefficients; parsed identity only."
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_La_basis.gbs",
    "sha256": "77b911a24ac8595da6c244cc71c7cbbf53a04678e40c997a86294667ee738680",
    "role": "Official originating-library molecular ECP/basis coefficients; parsed identity only."
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Lu_ECP60MWB.txt",
    "sha256": "fa929998b56ee1c544c777225d028d5fe6d36d87965282d318e1a4fa7fe085b2",
    "role": "Official originating-library molecular ECP/basis coefficients; parsed identity only."
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Lu_basis.gbs",
    "sha256": "0aa7060781e85dea1ef0e73c7b28b9af12edbf78688e2f0271e4d0943ff2df0c",
    "role": "Official originating-library molecular ECP/basis coefficients; parsed identity only."
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Tb_ECP54MWB.txt",
    "sha256": "5af4c632c405bfbf2715f2e22e67504a329ba512559986cb176891f65a96f449",
    "role": "Official originating-library molecular ECP/basis coefficients; parsed identity only."
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch5/source_review/cologne_Tb_basis.gbs",
    "sha256": "55407ce067188e5a7e06b5062eba7d7dbd4c38dfeda04cbe4fa551d8c4f3c8a8",
    "role": "Official originating-library molecular ECP/basis coefficients; parsed identity only."
  }
]

## source_scope

Main pp.3 and5 compares La/Tb/Lu solution chemistry, lanthanide binding, conformation and first-shell water; SI pp.21–22 gives the molecular free-energy protocol. The bounded task concerns the three source-tested ions with KHQ, not a new ligand library or absolute experimental pH speciation curve.

## old_task_diagnosis

{
  "public_and_private_fixed_panels": [
    "conformer_hydration_matrix",
    "replacement_and_cycles",
    "ecp_and_sensitivity"
  ],
  "fixed_schema_keys": {
    "conformer_hydration_matrix": [
      "La",
      "Tb",
      "Lu"
    ],
    "replacement_and_cycles": [
      "La",
      "Tb",
      "Lu"
    ],
    "ecp_and_sensitivity": [
      "metals",
      "thermochemistry_sensitivity",
      "water_placement_records",
      "conformation_vs_hydration_file",
      "evidence_files"
    ]
  },
  "required_hypotheses": 2,
  "diagnosis": "释放固定金属×syn/anti×0/1 水的完整矩阵、冻结 La 骨架和固定热化学路线；ECP 电子数、计量、标准态和候选解释所需能量守恒仍硬约束。",
  "files": [
    "agent_input/task.md",
    "agent_input/submission_schema.json",
    "agent_input/data/inputs",
    "evaluation/scoring_rules.json"
  ]
}

## agent_decisions

[
  "Generate chemically valid coordination arrangements and decide which conformational distinctions matter.",
  "Choose a treatment of water, electronic structure and free energy appropriate to the claimed aqueous preference.",
  "Determine whether the evidence resolves a unique preference, an accessible ensemble or a model-dependent ambiguity."
]

## public_input_changes

[
  "Replace syn/anti La endpoint XYZs and forced metal×conformer×water matrix with a complete coordinate-free KHQ graph plus complex stoichiometry.",
  "Keep optional verified ECP/basis numerical resources with their actual core-electron meanings; remove suggested water placements, frozen-La comparisons and prescribed radius/entropy controls.",
  "80-atom ligand identity verified by RDKit connectivity/valence recovery at net charge −2; original atom IDs retained, all coordinates omitted. No electronic calculation performed."
]

## submission_and_scoring

{
  "contract": "Question, objects, methods, optional unrestricted hypotheses, concise decisions, linked records, quantitative results, claims, raw artifacts and bounded conclusion. report/results.json and report/report.md are both required.",
  "results": "Paper-specific identity, quantities, inference, uncertainty and scope; alternative valid research designs permitted. No inherited matrix or author winner.",
  "process": "Actual dual_axis_100.open_research.v1 runtime; independent design/adaptation/resources for AR, disclosed protocol fidelity for PR. No chain-of-thought request.",
  "honest_limits": "Partial/bounded failure admissible without scientific completion; completed and evidenced non-identifiability can answer a genuinely unidentifiable question."
}

## pr_alignment

The authors started from syn crystalline [La-HKHQ]2+, removed H8 to obtain +1 [La-KHQ]+, substituted Ln and explored syn/anti plus eight C2-symmetric diastereomers for La/Tb/Lu. Gaussian16 C.01 used ωB97XD/def2SVP on CHNO and Dolg 4f-in-core LCRECP with (7s6p5d)/[5s4p3d] basis on Ln, pseudosinglet, nosymm and ultrafine integration. Gas-phase minima were checked by frequencies; aqueous SMD single points used parameterized Ln PCM radii. GoodVibes applied a 100 cm−1 quasi-harmonic cutoff at 298 K, scaling1.0, 1 M solute and55.5 M water. Source Table S2 reports syn preference and unfavorable one-water coordination; main p.5 also reports lower-energy solution diastereomers and multiple accessible structures. The authors themselves identify missing explicit ion solvation as a limitation of quantitative metal-selectivity predictions. Reproduce the disclosed assumptions or explain an applicable substitute; the V1 fixed 3×2×2 matrix and arbitrary water placements were later benchmark design.

## existing_evidence_reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "干syn/anti-La气相优化四标准全过，均237正频率；最低35.0859/16.5511cm⁻¹，能量-1942.42891623/-1942.41643622Eh。两源构象原子顺序不同，金属按元素定位。Tb冻结La几何ECP试算原生正常，316显式电子、54核及8项ECP系数验证。Tb弛豫已准备；Lu与水合/溶液矩阵未完成。",
    "unfinished_scientific_or_input_work": [
      "Tb/Lu实际弛豫及各金属两构象最低点",
      "完整水合矩阵、一致标准态/qRRHO",
      "定制半径溶剂、Lu半径核准、闭合水合循环与低频敏感性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_d8e5490cd9942f4f/evaluation/reference_validation_plan.md",
  "applicability": "已有 La 气相构象及 Tb ECP 原生试算；全水合/溶剂半径/低频校准待补。文件可读与引擎可算不等于溶液热力学正确。",
  "new_scientific_calculations_performed": false,
  "raw_evidence": [
    {
      "case_id": "ln_syn_la_gas_optfreq_v1",
      "job_id": "hpc-job-bb7b2afe-2b42-424d-9051-2e1ff2204556",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/outputs/ln_syn_la_gas_optfreq_v1",
      "normal_termination": true,
      "allocated_core_hours": 49.109000856605256
    },
    {
      "case_id": "ln_anti_la_gas_optfreq_v1",
      "job_id": "hpc-job-4e0c746b-d1b4-4736-b2b7-375828205b39",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/outputs/ln_anti_la_gas_optfreq_v1",
      "normal_termination": true,
      "allocated_core_hours": 58.393744814126855
    },
    {
      "case_id": "ln_syn_tb_on_la_ecp_pilot_v1",
      "job_id": "hpc-job-9e7a7f24-c31c-4599-a0d1-0ee4cb6f7cca",
      "status": "engine_finished",
      "path": "/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/outputs/ln_syn_tb_on_la_ecp_pilot_v1",
      "normal_termination": true,
      "allocated_core_hours": 2.360387202497158
    }
  ],
  "evidence_audits": [
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/report/Tb_ECP_native_pilot_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/report/anti_La_gas_minimum_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/report/syn_La_gas_minimum_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/legacy/native_log_audit.json",
    "docs/upgrade_tasks_verification/group_5/papers/paper_d8e5490cd9942f4f/legacy/attempt_inventory.json"
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
  "已有 La 气相构象及 Tb ECP 原生试算；全水合/溶剂半径/低频校准待补。文件可读与引擎可算不等于溶液热力学正确。",
  "Content authoring does not establish new numerical references, semantic judge calibration or runtime filesystem isolation."
]
