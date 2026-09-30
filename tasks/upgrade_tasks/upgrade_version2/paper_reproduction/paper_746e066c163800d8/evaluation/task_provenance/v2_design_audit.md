# paper_746e066c163800d8 — 特定V2方案

## paper_id

paper_746e066c163800d8

## batch

2

## created_at

2026-09-28T16:48:40.117133+00:00

## source_documents

[
  {
    "role": "main",
    "path": "papers/paper_746e066c163800d8/documents/main.pdf",
    "sha256": "2f0a280dbcadb2f19ed3222e4419f69854743c7440e834b3137b27c323643570",
    "material_type": "primary_article",
    "pdf_pages_1_based": [
      2,
      3
    ],
    "sections_figures_tables": "PDF p2 Fig.1 defines the helicene series; pp2–3 give geometry/response methodology and p3 equations15–18 define HRS and orientational averages."
  },
  {
    "role": "si",
    "path": "papers/paper_746e066c163800d8/documents/supplementary_001.pdf",
    "sha256": "6c9e2983aa14070df612bb3a6f6ca6a4c6d0394454f93d076a6b091e625d7403",
    "material_type": "actual_supporting_information",
    "pdf_pages_1_based": [
      16,
      26,
      37,
      40,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48
    ],
    "sections_figures_tables": "PDF p16 TableS2 geometric definitions; p26 method comparison; p37 TableS9 functional sensitivity; pp40–48 full coordinate entries for the chosen structures."
  }
]

## source_scope

A four-member subset of the source computational helicene study, restricted to static molecular HRS and its structural interpretation. The source also treats optical/transport/dynamic properties, which are not required here.

## old_task_diagnosis

{
  "task_and_public_matrix": "1/3/5/7完整27分量静态β张量、HRS/DR、5/7共同五扭角及响应校准。后续schema已补公开允许的解析/有限场路线。",
  "contract_panels": [
    "static_series",
    "twist_control",
    "response_calibration"
  ],
  "fixed_hypothesis_count": "hypotheses.minItems=2 in V1; removed in V2",
  "private_rules": "V1 same mandatory panels were bound into scientific rules; supersede rather than conceal them.",
  "source_issues": [
    "Remove the fixed 1→3 and5→7 attribution panels, preset common-core torsions, mandatory charge-transfer diagnostic and field-step count.",
    "Keep HRS definition and static frequency as the scientific observable, not as a prescribed computational algorithm."
  ]
}

## proposed_ar_problem

Determine whether and how the static molecular hyper-Rayleigh response differs among helicene compounds 1, 3, 5 and 7, and develop an evidence-supported explanation of the behaviour across these structures. Establish the scope and reliability of any structure–response relationship you infer.

## agent_decisions

[
  "Select physically relevant geometries/models and the response method.",
  "Decide which structural features or other explanations deserve testing and choose discriminating evidence.",
  "Choose how much numerical/model validation is needed to support the observed ordering or a limited conclusion."
]

## public_input_changes

[
  "Replace the fixed research_matrix with four full graphs and physical HRS definitions.",
  "Retain source numerical responses and coordinates only in private historical references."
]

## submission_and_scoring

{
  "evidence_required": "Report the static HRS quantities that support your comparison, their units and orientation convention, the actual molecular models and raw response/analysis artifacts. Retain enough numerical response data and executable transformations to reconstruct the reported observable. Link the explanation to evidence beyond merely ordering four scalar values. Any claimed geometric cause, numerical convergence or state assignment needs evidence specific to that claim; no particular diagnostic or intervention is compulsory.",
  "scientific_criteria": [
    "Verify complete compound1/3/5/7 connectivity, atom correspondence, charge and spin, and the molecular gas-phase static boundary. A reduced model must disclose its relation to the full structure and limits.",
    "Assess quantitative static HRS comparisons from auditable native response data and correct averaging/units. A scalar Cartesian beta, beta_total or finite-frequency response cannot silently substitute for isotropic static HRS. Evaluate the validity of the chosen computation/analysis without requiring one tensor-generation algorithm.",
    "Judge how well evidence supports or challenges the proposed structure–response explanation for this four-member family, including consequential confounds. An observed ranking alone is not a causal explanation. A supported nonmonotonic relation or inability to isolate a cause is eligible.",
    "Require uncertainty appropriate to response magnitudes and the claimed interpretation, including numerical convention, geometry or electronic-model limitations when material. A selected stability check does not establish universal functional accuracy. No fixed step count or source-value tolerance applies.",
    "Answer how the four source identities compare in static molecular HRS and what can be concluded about the relationship between structure and response. Do not extrapolate to all helicenes or bulk NLO performance without evidence."
  ],
  "contract": "Structured methods, chosen models, executions, numerical measurements, evidence hashes, findings, concise decision records and limitations; self-defined ideas with no minimum count; complete/partial/failed/blocked distinguished. No fixed panel.",
  "runtime": "dual_axis_100.open_research.v1; common result criteria; AR independent research and PR disclosed-source reproduction process differ. Semantic calibration remains pending."
}

## pr_alignment

The authors use B3LYP/6-31G(d) unconstrained ground-state optimization with frequency checks, followed by CAM-B3LYP/6-31+G(d) response calculations; SI TableS9 compares BHandHLYP and M06-2X for selected compounds. Main equations15–18 relate complete tensors to isotropic HRS, DR and dipolar/octupolar components. The source investigates where π extension changes nonlinear response across a larger designed family; it does not establish that every extension must increase the static response. The previous benchmark’s paired five-torsion +20° control and analytic/finite-field calibration are later investigations, not the author protocol. Limit reproduction to the four identities and static observable here.

## existing_evidence_reuse

Existing author-informed artifacts at docs/upgrade_tasks_verification/group_2/papers/paper_746e066c163800d8/report/results.json (SHA256403269cce7be0b59a86da0e068103d0aca2209930530eb1a9c22612eb6a2f891), report/report.md, analysis/, outputs/ and structures/ establish a feasible source-method four-member static response route, response reconstruction and limited numerical controls. Additional +20° intervention and NTO/finite-field checks are conditional evidence, not V2 completion requirements. V1 verified_computation_reference.md is preserved in private snapshots; its historical pass is not a V2 score.

## planned_changes

[
  "agent_input/task.md",
  "all public data to neutral systems/problem_facts/observations",
  "submission_schema.json and submission_guide.md",
  "task_info.json metadata",
  "all five active evaluator files",
  "source_scope_audit.json/md + v2_design_audit.md + reference_validation_plan",
  "paper_route and official package hashes"
]

## acceptance_checks

[
  "Full graphs retained; response values and source geometries absent from public inputs.",
  "Static HRS definition retained without fixed tensor algorithm/torsion matrix.",
  "Negative scientific cases cover dynamic/static and Cartesian/isotropic substitutions.",
  "Official package/hash/runtime/open_research policy and two-axis weights",
  "Public materialize exact set; no private snapshot or PR guidance in AR export",
  "AR/PR common facts/schema/scientific evaluator parity",
  "Official output_contract positive/negative fixtures; semantic verdict fixtures documented separately, not claimed as judge calibration",
  "Frozen V1 and source hashes unchanged; no new scientific calculations"
]

## limitations

Existing validation covers an author-informed limited method/geometry route, not all admissible alternative explanations or correlated accuracy. Existing interventions do not uniquely identify a mechanism. V2 semantic calibration and private-file isolation remain pending.

## feasibility

Real source-level Gaussian opt/frequency and response artifacts exist for these identities, including a failed-attempt record and independent tensor analysis. A first future reference audit can reparse these artifacts, verify tensor conventions and review the supported scope. Gaussian/ORCA native routes and Python response processing are potential resources after checking installed capability. No new science was launched.

## review_status

ready_for_implementation_not_coordinator_approved

## exact_legacy_artifact_inventory

evaluation/task_provenance/reference_artifact_inventory.json

## post_implementation_provenance_addendum

{
  "at": "2026-09-28T17:43:01.566201+00:00",
  "reason": "Resolve exact archived summary and available historical raw/report paths after source-bounded plan was implemented; scientific design unchanged.",
  "previous_plan_sha256": "c2b31f52bcaa18d148698ae9527700bc2d8d115661221406a0af1e69b38f3cbd",
  "found_files": 582,
  "unresolved_links": 0
}

