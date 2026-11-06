# paper_8d8940710de08f7f — 特定V2方案

## paper_id

paper_8d8940710de08f7f

## batch

2

## created_at

2026-09-28T17:05:15.191964+00:00

## source_documents

[
  {
    "role": "main",
    "path": "papers/paper_8d8940710de08f7f/documents/main.pdf",
    "sha256": "a69619c718ff7d48e4dd23ce129bb8ea5a7cb58e4fcb0114ab68587d688fe9bc",
    "material_type": "primary_article",
    "pdf_pages_1_based": [
      5,
      7,
      8,
      9,
      10
    ],
    "sections_figures_tables": "PDF p5 computational protocol; pp7–8 distinguish molecular/protolytic and material observations; pp9–10 conformational discussion, Fig.7–8 torsion results and Table4."
  },
  {
    "role": "si",
    "path": "papers/paper_8d8940710de08f7f/documents/supplementary_001.pdf",
    "sha256": "d903b517aab2dfd6c2a223020cb7d93ae6d66dc85eb489ab86c4aa854561bd13",
    "material_type": "actual_supporting_information",
    "pdf_pages_1_based": [
      8,
      9,
      10
    ],
    "sections_figures_tables": "PDF pp8–10 TableS8 is explicitly in-vacuo electronic/Gibbs energy and coordinate evidence; it is not a methanol free-energy table."
  }
]

## source_scope

The neutral-molecule conformational subproblem of the source sulfonamide study, bounded to two identities and in-vacuo/methanol representation. Biological, protonation and octanol/water partition endpoints are not requested.

## old_task_diagnosis

{
  "task_and_public_matrix": "V+/V−/Z、真空/甲醇、D3开关、接触反事实和低频热化学；接受盆地坍缩、近简并而不造人口。",
  "contract_panels": [
    "basins",
    "interventions",
    "thermochemical_robustness"
  ],
  "fixed_hypothesis_count": "hypotheses.minItems=2 in V1; removed in V2",
  "private_rules": "V1 same mandatory panels were bound into scientific rules; supersede rather than conceal them.",
  "source_issues": [
    "Remove named V+/V−/Z starting ranges and mandatory basin count.",
    "Remove required D3 on/off switch, fixed/relaxed contact-control pair and specified qRRHO comparisons.",
    "Retain physical energy/ensemble definitions and fair handling of collapsed or nearly degenerate structures."
  ]
}

## proposed_ar_problem

Determine the conformational preferences of neutral SNaft and SAntr and develop an evidence-supported explanation of their molecular stability and flexibility. Assess how far the interpretation can be maintained between the source in-vacuo and methanol molecular settings.

## agent_decisions

[
  "Choose how to identify the conformational structures relevant to the neutral molecules.",
  "Choose evidence capable of testing a proposed source of relative stability or flexibility.",
  "Decide whether sampling, thermochemical and environmental limitations permit a definite ordering or only a bounded conclusion."
]

## public_input_changes

[
  "Keep only two full neutral graphs and physical conditions/definitions.",
  "Remove source minimum coordinates, torsion menu and nominated contact atoms from public inputs.",
  "Keep source R2SCAN and separate density-analysis details in PR/private provenance."
]

## submission_and_scoring

{
  "evidence_required": "Supply the molecular structures actually investigated and numerical stability/flexibility evidence, with atom correspondence, states, conditions and raw artifacts. For equilibrium/population claims, retain the thermal terms and executable weighting analysis; for an interaction-based explanation, provide evidence that supports its role rather than only naming a short distance. Record failed searches and coincident endpoints honestly, and explain how the investigated region limits the conclusion.",
  "scientific_criteria": [
    "Verify complete SNaft/SAntr neutral graphs, charge/spin, model environments and atom correspondence. Do not mix charged species or different environments in an unqualified conformational population.",
    "Assess auditable structures, energies and any other claim-relevant conformational quantities. Distinguish an electronic-energy difference from a free-energy difference, constrained points from minima and repeated endpoints from distinct states. No source torsion bin or predetermined family count is mandatory.",
    "Judge whether the proposed explanation of stability/flexibility is supported by meaningful evidence and whether consequential alternatives or environmental limitations are addressed. A contact picture alone is insufficient for energetic attribution. Evidence-supported near-degeneracy, collapse or lack of unique attribution can be a full bounded scientific conclusion.",
    "Assess sampling and claim-relevant numerical, low-frequency/thermochemical or solvent-model uncertainty. Do not infer a robust tiny ordering from uncalibrated energy digits, or convert the source vacuum table into methanol targets. No fixed correction toggle or acceptance interval applies.",
    "State the supported conformational preferences and their explanation within the neutral molecular settings, distinguishing resolved preferences from approximate equivalence or incomplete coverage. Do not infer pharmacological potency, membrane transport or crystal equilibrium from these isolated-molecule findings."
  ],
  "contract": "Structured methods, chosen models, executions, numerical measurements, evidence hashes, findings, concise decision records and limitations; self-defined ideas with no minimum count; complete/partial/failed/blocked distinguished. No fixed panel.",
  "runtime": "dual_axis_100.open_research.v1; common result criteria; AR independent research and PR disclosed-source reproduction process differ. Semantic calibration remains pending."
}

## pr_alignment

The source uses ORCA6.0.1 R2SCAN/def2-TZVP with def2/J, split-RI-J, relaxed C–S–N–C scans, optimizations and vibrational checks; C-PCM represents specified solvents (main p5). No extra D3 correction is declared for this R2SCAN route. The authors describe near-equivalent V(+)/V(−) and a less favourable Z geometry and discuss an aromatic C–H···O contact in the neutral molecules (pp9–10). Their QTAIM and dipole analyses instead use ωB97M-V/methanol wavefunctions; do not merge this with the geometry functional or the explicitly in-vacuo SI TableS8 energies. V1 D3 toggles, contact-disfavoring restraints, forced initial torsion bins and paired thermal panels were later benchmark interventions, not source protocols.

## existing_evidence_reuse

V1 evaluation/legacy_final_snapshot preserves older neutral/constrained source-method evidence. Source main Fig.8 and SI TableS8 give conditional source conformational/energy information, not an exhaustive independently validated ensemble. The source ωB97M-V density analysis belongs to a separate methanol calculation. No V1 mandatory dispersion/contact/environment matrix was completed by batch2; those operations are not active V2 criteria.

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
  "Public graphs carry no V/Z name, target torsion or selected contact.",
  "R2SCAN baseline does not silently acquireD3; vacuum/methanol source roles stay distinct.",
  "Active criteria accept documented collapse/near-degeneracy without rewarding skipped research.",
  "Official package/hash/runtime/open_research policy and two-axis weights",
  "Public materialize exact set; no private snapshot or PR guidance in AR export",
  "AR/PR common facts/schema/scientific evaluator parity",
  "Official output_contract positive/negative fixtures; semantic verdict fixtures documented separately, not claimed as judge calibration",
  "Frozen V1 and source hashes unchanged; no new scientific calculations"
]

## limitations

No new full conformational reference or calibrated free-energy uncertainty has been obtained. Source labels and coordinates do not prove global sampling, and no experimental conformer fractions are supplied. Alternative-route scientific/semantic calibration and environment isolation remain pending.

## feasibility

The source ORCA relaxed scans/optimization/frequency and existing neutral-molecule evidence demonstrate a feasible molecular route. ORCA/native and Python thermochemistry tools may support a chosen investigation after checking availability. First future review should reparse matching neutral raw outputs and verify source medium/functional labels before proposing new reference science.

## review_status

ready_for_implementation_not_coordinator_approved

## exact_legacy_artifact_inventory

evaluation/task_provenance/reference_artifact_inventory.json

## post_implementation_provenance_addendum

{
  "at": "2026-09-28T17:43:05.322832+00:00",
  "reason": "Resolve exact archived summary and available historical raw/report paths after source-bounded plan was implemented; scientific design unchanged.",
  "previous_plan_sha256": "4ecb3e1fb7e905f995ecc948a7ee1c4f700aa6ebfb5a47ab063f97f205e2ca2e",
  "found_files": 8,
  "unresolved_links": 0
}

