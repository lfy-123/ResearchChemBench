# paper_5d94285cfbd51973 — 特定V2方案

## paper_id

paper_5d94285cfbd51973

## batch

2

## created_at

2026-09-28T16:59:16.866565+00:00

## source_documents

[
  {
    "role": "main",
    "path": "papers/paper_5d94285cfbd51973/documents/main.pdf",
    "sha256": "9a4125a542a33af7128c39ebcf9df93cbe82923038415ed18e81bc77ca65e1a2",
    "material_type": "primary_article",
    "pdf_pages_1_based": [
      2,
      3,
      4,
      5,
      6,
      7
    ],
    "sections_figures_tables": "PDF pp2–3 synthesis/assay and SAR; pp4–7 DFT/frontier/MEP interpretation and its biological claims."
  },
  {
    "role": "si",
    "path": "papers/paper_5d94285cfbd51973/documents/supplementary_001.pdf",
    "sha256": "9c09e4819df88ab73a3551dca09e2c5b390e7a783dac0df4f633e06e5e227f0e",
    "material_type": "actual_supporting_information",
    "pdf_pages_1_based": [
      2,
      3,
      4,
      5,
      6,
      7,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      40,
      41,
      42
    ],
    "sections_figures_tables": "PDF pp3–7 identities; p31 TableS1 exact C.albicans column; pp31–40 source gas-phase coordinates; p41 TableS12 all-ten descriptors and printed formulas; p42 TableS13 calculated physicochemical properties."
  }
]

## source_scope

A bounded molecular-property/observed-activity subproblem in the source ten-compound study. Source docking and pharmacokinetic claims are background, not endpoints to reproduce or proof of the molecular-property relation.

## old_task_diagnosis

{
  "task_and_public_matrix": "十个明确图、C. albicans同列MIC，固定HOMO/偶极与logP/MW基线、ridge α=1、LOOCV与1000次置换。",
  "contract_panels": [
    "descriptor_series",
    "out_of_fold",
    "null_and_resolution"
  ],
  "fixed_hypothesis_count": "hypotheses.minItems=2 in V1; removed in V2",
  "private_rules": "V1 same mandatory panels were bound into scientific rules; supersede rather than conceal them.",
  "source_issues": [
    "Remove mandatory two-feature electronic model, fixed baseline features, ridge hyperparameter, LOOCV and permutation counts.",
    "Remove predefined ordinal bins and derived endpoint intervals; retain printed MIC values and finite-resolution limitations.",
    "Correct false implication that the authors studied onlyAZ9 and explicitly audit source descriptor formulas."
  ]
}

## proposed_ar_problem

Determine whether molecular properties of AZ1–AZ10 provide defensible explanatory or predictive information about the reported Candida albicans MIC differences. Investigate the relationship using evidence appropriate to this small measured series and state what can and cannot be inferred about activity.

## agent_decisions

[
  "Choose molecular properties/models and a testable relationship to the reported activity.",
  "Choose statistical or comparative evidence that can distinguish a meaningful relationship from the limited sample structure.",
  "Decide whether the data support prediction, only descriptive association, or no reliable relationship, and revise claims accordingly."
]

## public_input_changes

[
  "Keep all ten complete mapped molecular identities and the same actual C.albicans values.",
  "Replace operation/feature menus with definitions and measurement limits; computed source descriptors remain private.",
  "Source assay endpoints are available from the outset; no blind test claim is built into the contract."
]

## submission_and_scoring

{
  "evidence_required": "Supply the molecular quantities actually investigated, their definitions/settings and reproducible raw calculation or graph-analysis evidence, together with the numerical activity analysis. Include data transformations, model/analysis choices, fitted quantities and any validation outputs needed to support the claim you make. For predictive claims, retain the actual separation of fitting/selection from assessment and per-compound predictions where applicable. A descriptive or negative result remains useful if its limits are evidenced; ten descriptor values plus an unsupported activity narrative are insufficient.",
  "scientific_criteria": [
    "Verify the ten source derivative identities and substitution positions, model charge/state and correspondence to the C.albicans assay rows. Do not mix bacterial columns, docking scores or another strain into this endpoint.",
    "Assess reproducible molecular descriptors and numerical relationship estimates with the ten MIC observations. Feature/target transformations, units and descriptor formulas must be explicit and physically meaningful. Source-formula reproduction must be distinguished from corrected definitions. No fixed descriptor set or regression algorithm is mandatory.",
    "Judge whether the evidence establishes an association or prediction beyond an unsupported ordering, and whether selection, small-sample structure and alternative explanations undermine that claim. Any predictive/generalization claim requires appropriate separation of fit and assessment. Supported absence of a useful relationship is equally eligible.",
    "Assess limited sample size, discrete MIC levels, missing replicate information and consequential descriptor/model uncertainty. Do not invent continuous assay error bars, rank equal MIC compounds by assumed exact potency or equate a high training fit with reliable prediction.",
    "State whether and how molecular properties inform the reported C.albicans differences, with an evidence-proportionate scope. No clinical, permeability, target-mechanistic or broad antimicrobial conclusion follows solely from these molecular/statistical data."
  ],
  "contract": "Structured methods, chosen models, executions, numerical measurements, evidence hashes, findings, concise decision records and limitations; self-defined ideas with no minimum count; complete/partial/failed/blocked distinguished. No fixed panel.",
  "runtime": "dual_axis_100.open_research.v1; common result criteria; AR independent research and PR disclosed-source reproduction process differ. Semantic calibration remains pending."
}

## pr_alignment

The source calculates molecular properties for AZ1–AZ10, not only AZ9: SI TableS12 contains frontier energies, derived descriptors and dipoles for all ten at gas-phase B3LYP/6-31G(d); Gaussian16 is the disclosed program. Main pp4–7 links frontier/MEP/polarity descriptors to activity and docking, with selected geometry/orbital figures. The old benchmark’s isolated AZ9 reference was only a narrow task, not the scope of the author study. Source formulas require scrutiny: TableS12 prints ΔE=EHOMO−ELUMO but tabulates positive ELUMO−EHOMO differences; it defines μ=−η and ω=η/2, which do not implement the usual finite-difference chemical-potential/electrophilicity definitions μ=−(IP+EA)/2 and ω=μ²/(2η). Label any source-formula reproduction explicitly and distinguish corrected physical definitions; source arithmetic is not a correctness target. Fixed HOMO/dipole versus logP/MW features, ridgeα=1, LOOCV and1000 permutations were V1 additions, not an author validation protocol.

## existing_evidence_reuse

Private legacy_final_snapshot contains the prior AZ9 molecular calculation only; it supports feasibility for that identity and method, not a validated ten-compound relationship. Source SI TableS12 is all-ten author computational evidence but has explicit formula inconsistencies. Source SI TableS1 is the reusable experimental activity column. TableS13 contains model-derived physicochemical estimates, not measured permeability. These sources are distinct from independently validated V2 analyses.

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
  "Ten MIC values exactly preserve the C.albicans source column and no derived outcome bins remain.",
  "All ten graphs retain substitutions and complete molecular formula.",
  "Active scoring permits other justified features/methods and explicitly rejects unsupported biological extrapolation.",
  "Official package/hash/runtime/open_research policy and two-axis weights",
  "Public materialize exact set; no private snapshot or PR guidance in AR export",
  "AR/PR common facts/schema/scientific evaluator parity",
  "Official output_contract positive/negative fixtures; semantic verdict fixtures documented separately, not claimed as judge calibration",
  "Frozen V1 and source hashes unchanged; no new scientific calculations"
]

## limitations

No new all-ten quantum or statistical reference was produced. MIC replicate distributions/strain accession are absent in inspected records; the sample cannot establish broad predictive or causal biology. Source descriptor errors limit literal reuse. V2 judge calibration and environment isolation remain pending.

## feasibility

Ten chemically explicit graphs and an actual assay column suffice for a bounded computational/statistical investigation; a source gas-phase DFT route and cheaper graph-derived analyses are feasible options, depending on the claim. The toolbox provides Gaussian/ORCA/native routes and Python analysis after capability inspection. A future reference review can first audit source descriptor arithmetic and matching raw legacy outputs without launching new science.

## review_status

ready_for_implementation_not_coordinator_approved

## exact_legacy_artifact_inventory

evaluation/task_provenance/reference_artifact_inventory.json

## post_implementation_provenance_addendum

{
  "at": "2026-09-28T17:43:04.640188+00:00",
  "reason": "Resolve exact archived summary and available historical raw/report paths after source-bounded plan was implemented; scientific design unchanged.",
  "previous_plan_sha256": "319876b9f2a6247522a7c9d4f487554b2abd875e5043e74d1a16d5abd087c5a1",
  "found_files": 28,
  "unresolved_links": 0
}

