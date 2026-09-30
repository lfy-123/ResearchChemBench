# paper_9d091f4337662e78 — 特定V2方案

## paper_id

paper_9d091f4337662e78

## batch

2

## created_at

2026-09-28T16:50:34.466303+00:00

## source_documents

[
  {
    "role": "main",
    "path": "papers/paper_9d091f4337662e78/documents/main.pdf",
    "sha256": "77662fc70c44424324935577c2f687f8dd7e380d928c34d07550ffaa7f64e2db",
    "material_type": "primary_article",
    "pdf_pages_1_based": [
      3,
      4,
      6,
      7
    ],
    "sections_figures_tables": "PDF pp3–4 structure elucidation and Figure2 compound1 experimental black ECD trace; p6 experimental compound1 data; p7 full ECD computational method."
  },
  {
    "role": "si",
    "path": "papers/paper_9d091f4337662e78/documents/supplementary_001.pdf",
    "sha256": "48e92302a3a0bbc6b0ed8d6db613911ea165365d2a2b5f87ac35fbd4954f0cfc",
    "material_type": "actual_supporting_information",
    "pdf_pages_1_based": [
      5
    ],
    "sections_figures_tables": "PDF p5 TableS1 lists16 computed conformers and source populations; it is private evidence for ensemble complexity, not public starting structures."
  }
]

## source_scope

A configurational assignment problem for only compound1, using known constitution and methanol ECD. The source assigned this centre by a computed/experimental spectral comparison; the new question permits evidence-supported ambiguity.

## old_task_diagnosis

{
  "task_and_public_matrix": "完整分子与未定中心17、独立R/S系综、镜像与ECD、数字化实验谱；旧三构象不足以覆盖系综，不公开作者终态。",
  "contract_panels": [
    "ensemble_search",
    "ensemble_ECD",
    "configuration_discrimination"
  ],
  "fixed_hypothesis_count": "hypotheses.minItems=2 in V1; removed in V2",
  "private_rules": "V1 same mandatory panels were bound into scientific rules; supersede rather than conceal them.",
  "source_issues": [
    "Remove R/S candidate enumeration and mandatory independently searched pair from the public input.",
    "Remove fixed qRRHO cutoffs, broadening widths, no-shift algorithm and spectral held-out partition.",
    "Retain the unassigned centre and E alkene as necessary identity facts; no author S label appears in AR."
  ]
}

## proposed_ar_problem

Determine what absolute configuration, if any, is supported at the unresolved stereocentre of compound 1 by its known constitution and experimental ECD in methanol. Design an investigation that distinguishes a defensible configurational assignment from an assignment that the available spectral and molecular evidence cannot resolve.

## agent_decisions

[
  "Decide how to generate and evaluate stereochemical/conformational models without supplied author geometries.",
  "Choose how to connect computed or other physically justified evidence to the experimental ECD and quantify discrimination.",
  "Decide whether the sampled models and data support one assignment, an unresolved set or a narrower conclusion."
]

## public_input_changes

[
  "Replace both candidate graphs with one unassigned mapped constitution.",
  "Retain all93 measured-curve points, units and digitization bounds; delete the partition column.",
  "Retain observation provenance without author curves, answer labels or tuning instructions."
]

## submission_and_scoring

{
  "evidence_required": "Provide the stereochemical models actually investigated, their mapping to atom17 and the known constitution, and numerical spectral or other assignment evidence with auditable raw artifacts. If using molecular ECD calculations, preserve transitions/rotatory quantities and the executable spectrum construction; if claiming an ensemble, retain the evidence for its composition and weighting. Explain how the supplied methanol trace supports or fails to support the assignment, including material sampling, spectral-processing and measurement limits. Do not substitute an author label or one attractive overlay for an auditable configurational argument.",
  "scientific_criteria": [
    "Check C24H24N2O4 constitution, E alkene, map17 stereochemical correspondence, charge/multiplicity and medium. Assigned models must state the actual stereochemistry after generation/optimization rather than relying on input filenames.",
    "Evaluate numerical evidence relevant to configuration and its reproducibility from spectra or other valid artifacts. ECD sign/units and any spectral transformations must be explicit. Ensemble claims require justified models/weights and honest sampling scope, but no fixed conformer count or preset broadening is required.",
    "Judge whether the investigation distinguishes the proposed configuration from relevant unresolved alternatives and whether apparent agreement survives the identified limitations. Credit an evidenced unresolved assignment as fairly as a supported unique one. No source absolute label is a required winner.",
    "Assess the impact of available plot precision and consequential molecular/spectral-model uncertainty. Reject certainty based on arbitrary candidate-specific fitting or untested ensemble truncation. An unperformed search cannot be relabeled a demonstrated nonidentifiability result.",
    "State the supported absolute-configurational inference at map17 and its evidential limits in methanol, using the known constitution. Confidence must follow the achieved discrimination; source agreement and historical three-conformer results are not completion criteria."
  ],
  "contract": "Structured methods, chosen models, executions, numerical measurements, evidence hashes, findings, concise decision records and limitations; self-defined ideas with no minimum count; complete/partial/failed/blocked distinguished. No fixed panel.",
  "runtime": "dual_axis_100.open_research.v1; common result criteria; AR independent research and PR disclosed-source reproduction process differ. Semantic calibration remains pending."
}

## pr_alignment

The authors assigned compound1 as 1′S by comparison with experimental ECD (main p4 Figure2). Main p7 reports Spartan14/MMFF94 initial sampling, a10kcal/mol window, M06-2X-GD3/6-311G(d,p) optimizations and frequency checks, gas-phase M06-2X-GD3/6-311+G(2d,p) energies with thermal corrections, and298.15K Boltzmann populations. Conformers over1% were retained for CAM-B3LYP/6-31+G(2d,p) TD-ECD in methanol IEFPCM and SpecDis1.70.1 averaging. SI TableS1 lists16 source conformers; the gas-phase weighting and solution excitation calculations are distinct steps. The former benchmark’s independent dual search, fixed broadening/energy windows and held-out band were added controls, not a disclosed author protocol. Reproduction must evaluate rather than simply repeat the S label.

## existing_evidence_reuse

Source main Figure2 provides a true experimental observation, while SI TableS1 provides private author conformer evidence. The original final task and run metadata preserved under evaluation/legacy_final_snapshot contain a three-conformer reference; their source populations sum to52.06%, so renormalizing those three does not establish complete sampling. These energies/geometries may inform future pilot feasibility privately but are not authorized public starting answers or an expanded V2 reference.

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
  "Graph centre17 is unspecified and E alkene is retained.",
  "Exactly93 ECD points retain values and bounds while partition is removed.",
  "No public absolute answer, fixed candidate enum or fixed spectral-processing panel.",
  "Official package/hash/runtime/open_research policy and two-axis weights",
  "Public materialize exact set; no private snapshot or PR guidance in AR export",
  "AR/PR common facts/schema/scientific evaluator parity",
  "Official output_contract positive/negative fixtures; semantic verdict fixtures documented separately, not claimed as judge calibration",
  "Frozen V1 and source hashes unchanged; no new scientific calculations"
]

## limitations

No new full conformational or spectral reference has been calculated. Digitized experimental data have finite precision and lack original instrumental uncertainties. Source gas-phase populations/solution TD are model-dependent. V2 semantic judge calibration and execution isolation remain pending.

## feasibility

The source demonstrates a molecular conformer/TD-ECD route and the toolbox exposes native Gaussian/ORCA plus graph/Python workflows; optional sampling software must be checked in the actual tool catalog. First reuse checks can inspect known constitution, the93-point extraction and historical molecular outputs. Future expanded scientific work would need evidence sufficient for whichever representation/spectral strategy is chosen, without a mandated dual-search matrix.

## review_status

ready_for_implementation_not_coordinator_approved

## exact_legacy_artifact_inventory

evaluation/task_provenance/reference_artifact_inventory.json

## post_implementation_provenance_addendum

{
  "at": "2026-09-28T17:43:01.884436+00:00",
  "reason": "Resolve exact archived summary and available historical raw/report paths after source-bounded plan was implemented; scientific design unchanged.",
  "previous_plan_sha256": "d8c57493c83a08512960ea1d9f8e3c1943d4a645cb3180a885db24f97c541233",
  "found_files": 6,
  "unresolved_links": 0
}

