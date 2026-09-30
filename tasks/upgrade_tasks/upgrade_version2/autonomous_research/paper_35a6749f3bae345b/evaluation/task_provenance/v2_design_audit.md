# paper_35a6749f3bae345b — 特定V2方案

## paper_id

paper_35a6749f3bae345b

## batch

2

## created_at

2026-09-28T17:00:35.323898+00:00

## source_documents

[
  {
    "role": "main",
    "path": "papers/paper_35a6749f3bae345b/documents/main.pdf",
    "sha256": "8d9c00625c2bce148224c2bd64afdd9e50ce58c62013879e5a1bd37bc63e2345",
    "material_type": "primary_article",
    "pdf_pages_1_based": [
      3,
      4,
      5,
      6
    ],
    "sections_figures_tables": "PDF p3 optical/theoretical methods; p4 Scheme1 and discussion of closely similar spectra; p5 Table1/Fig.3 measured absorption/emission; p6 electronic interpretation."
  },
  {
    "role": "si",
    "path": "papers/paper_35a6749f3bae345b/documents/supplementary_001.pdf",
    "sha256": "c689ac62aab028b9263116896d5791a0222388c2afc0289dba4cf2d30ad4094f",
    "material_type": "actual_supporting_information",
    "pdf_pages_1_based": [
      11
    ],
    "sections_figures_tables": "PDF p11 TableS5 explicitly compares TD results at S0 and S1 optimized geometries, with TableS6 orbital contributions; geometry label is not an excited-state-absorption label."
  }
]

## source_scope

Three source DBC derivatives with solution absorption/fluorescence. The open question includes the possibility of little distinguishable spectral change and does not invent a transfer-prediction experiment.

## old_task_diagnosis

{
  "task_and_public_matrix": "Ph/Nap/Cbz完整分子、S0/S1四点循环、45°共同几何、Cbz转移检验；避免将S1几何上S0参考TD根误写ESA。",
  "contract_panels": [
    "relaxation_cycles",
    "twist_control",
    "Cbz_prediction"
  ],
  "fixed_hypothesis_count": "hypotheses.minItems=2 in V1; removed in V2",
  "private_rules": "V1 same mandatory panels were bound into scientific rules; supersede rather than conceal them.",
  "source_issues": [
    "Remove required S0/S1 four-point cycle, common45° core intervention and Cbz holdout.",
    "Do not assume a terminal substituent effect exists; frame the question around observed similarities and possible distinguishable changes.",
    "Remove inherited ESA language unsupported by the source TD reference-state definition."
  ]
}

## proposed_ar_problem

Explain the absorption and fluorescence behaviour of DBC-Ph, DBC-Nap and DBC-Cbz in oxygen-free toluene. Determine whether the different terminal substituents cause distinguishable molecular optical behaviour and what evidence supports the interpretation of the similarities or differences.

## agent_decisions

[
  "Choose the models and observables needed to explain the measured spectral similarities or differences.",
  "Decide how to establish the character and correspondence of relevant optical processes.",
  "Choose tests that can support or limit a substituent-based interpretation, and determine whether differences are resolvable."
]

## public_input_changes

[
  "Keep three complete graphs and add all three observed absorption/emission rows from Table1.",
  "Replace the Cbz-only heldout file with a common retrospective spectrum table.",
  "Retain state/geometry distinctions as physical definitions without prescribing an algorithm."
]

## submission_and_scoring

{
  "evidence_required": "Provide the numerical molecular and spectral quantities that support your answer, including electronic-state/geometry definitions, solvent treatment, raw outputs and reproducible spectral or other analysis. Address both the reported absorption and fluorescence observations to the extent claimed. Evidence for relaxation, state character or a substituent effect must substantiate that specific interpretation. A supported lack of distinguishable change is acceptable; it must follow from evidence and resolution, not omission of the comparison.",
  "scientific_criteria": [
    "Verify complete DBC_Ph/Nap/Cbz connectivity and state/charge definitions. Do not substitute the Ant/Pyr derivatives or a truncated common core without a justified relation to the actual full molecules.",
    "Assess auditable quantities corresponding to solution absorption and fluorescence, with correct initial/final states, geometry and medium. Neither a state label on a geometry nor an orbital gap establishes an optical process. Raw transition/spectral and analysis artifacts must support the reported results.",
    "Evaluate whether the molecular explanation accounts for the nearly coincident observed spectra and any proposed differences. Require claim-relevant evidence for electronic/structural attribution while allowing a justified alternative route, negative result or unresolved attribution.",
    "Assess numerical/model uncertainty and the resolution of the experimental peak list. Do not treat rounded1nm differences or an uncalibrated computed splitting as definitive. Source S0/S1 geometry tables need correct interpretation rather than a forced optical match.",
    "State what is supported about terminal-substituent influence on Ph/Nap/Cbz molecular absorption and fluorescence in toluene. Keep similarity, lack of resolving power and equality of all molecular properties distinct; avoid material/device extrapolation."
  ],
  "contract": "Structured methods, chosen models, executions, numerical measurements, evidence hashes, findings, concise decision records and limitations; self-defined ideas with no minimum count; complete/partial/failed/blocked distinguished. No fixed panel.",
  "runtime": "dual_axis_100.open_research.v1; common result criteria; AR independent research and PR disclosed-source reproduction process differ. Semantic calibration remains pending."
}

## pr_alignment

The authors optimize ground(S0) and first-singlet-excited(S1) geometries with B3LYP/6-31+G(d,p) in Gaussian16 and use TD-B3LYP and GaussSum orbital-fragment analysis (main pp3–6; SI TableS5–S6 in toluene). They interpret the similar Ph/Nap/Cbz spectra largely through DBC-local contributions with partial charge transfer and report no strong terminal-substituent shift for this subset. SI labels calculated transitions at both S0 and S1 optimized geometries; these should not be relabeled genuine S1→Sn excited-state absorption. The V1 four-point relaxation matrix,45° intervention and Cbz frozen prediction were additional benchmark design, not the authors’ stated experiment.

## existing_evidence_reuse

V1 private legacy_final_snapshot contains older source-geometry calculations and narrow scalar endpoints. These may support method/state sanity checks, not the full open optical explanation. Main Table1 is reusable experimental evidence for all three members; SI TableS5–S6 provides private calculated-state and geometry context. The old expanded four-point/intervention reference remains incomplete and is no longer mandatory.

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
  "All three Table1 optical rows and source1e-5M condition are preserved.",
  "No Cbz-holdout or forced45°/four-point panel in active files.",
  "State-versus-geometry error is explicitly rejected without prescribing one alternative method.",
  "Official package/hash/runtime/open_research policy and two-axis weights",
  "Public materialize exact set; no private snapshot or PR guidance in AR export",
  "AR/PR common facts/schema/scientific evaluator parity",
  "Official output_contract positive/negative fixtures; semantic verdict fixtures documented separately, not claimed as judge calibration",
  "Frozen V1 and source hashes unchanged; no new scientific calculations"
]

## limitations

No new comparative excited-state reference has been calculated. Raw experimental traces/errors are not supplied and the source’s S1-geometry labels cannot resolve every process assignment. Alternative-route scientific/semantic calibration and environment isolation remain pending.

## feasibility

The source and older Gaussian records demonstrate a molecular DFT/TD route. Existing raw outputs can first be checked for their exact electronic reference, geometry and solvent; additional claim-specific validation is a separate scientific activity. Registered Gaussian/ORCA and Python spectroscopy analysis are potential tools, not a fixed workflow.

## review_status

ready_for_implementation_not_coordinator_approved

## exact_legacy_artifact_inventory

evaluation/task_provenance/reference_artifact_inventory.json

## post_implementation_provenance_addendum

{
  "at": "2026-09-28T17:43:04.942520+00:00",
  "reason": "Resolve exact archived summary and available historical raw/report paths after source-bounded plan was implemented; scientific design unchanged.",
  "previous_plan_sha256": "21d1a945fd5c15a4fb00b479d04d7514406a4d4370aee577428ad221db70239c",
  "found_files": 14,
  "unresolved_links": 0
}

