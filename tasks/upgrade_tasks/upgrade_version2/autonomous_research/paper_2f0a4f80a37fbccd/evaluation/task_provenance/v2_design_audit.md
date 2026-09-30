# paper_2f0a4f80a37fbccd: paper-specific V2 plan

Prepared 2026-09-28T16:32:37.940738+00:00. This plan precedes any V2 package copy/write.

## source documents

[
  {
    "path": "papers/paper_2f0a4f80a37fbccd/documents/main.pdf",
    "sha256": "76fe828053d735014dabbbcf20749bb2d180992ed7921df2190fc89bacca8438",
    "matches_audit": true,
    "declared_pages": 10,
    "material_type": "main_article",
    "pdf_pages_read_1_based": [
      3,
      4,
      5,
      6,
      7,
      8
    ]
  },
  {
    "path": "papers/paper_2f0a4f80a37fbccd/documents/supplementary_001.pdf",
    "sha256": "539d338737eddb8491b9e78f2202fc83f3495da450c4dd6c0a55c452b3f5c01e",
    "matches_audit": true,
    "declared_pages": 34,
    "material_type": "true_supporting_information",
    "pdf_pages_read_1_based": [
      1,
      15,
      26,
      29
    ]
  }
]

## source scope

{
  "objects": "Neutral singlet model of full IrCl2(NO3)(PPh3)2, C36H30Cl2IrNO3P2: one Ir, two chlorides, two intact triphenylphosphines and one nitrate.",
  "data": "KBr IR qualitative bands from main p8, with additional1561cm-1 in main pp3–4 discussion/Table2. No raw intensities or precise experimental errors supplied.",
  "source_question": "Structure and coordination characterization of the nitrato product; source uses IR, crystallography and DFT.",
  "bounded_task": "Investigate molecular structures compatible with composition/IR, with explicit model validity; exclude oxygen/nitrite formation network, CO/NO adducts, electroreduction products and crystal-packing calculation.",
  "difference_from_source": "AR withholds solved crystal answer and source assignment intentionally; PR discloses author structure/protocol. Inference from IR alone may be nonunique even though source crystal structure exists."
}

## old task diagnosis

{
  "task.md": "Supplied eta1 and eta2 candidates and mandated both plus ligand-arrangement alternatives, two band-list fits and quantified nitrate normal-mode fraction.",
  "data": "tested_nitrate_bindings enum and geometric_variation cue fixed search; four preselected nitrate-band observations erased the rest of the experimental spectrum.",
  "schema": "candidates/mode_assignments/spectral_comparison fixed route plus two hypotheses minimum.",
  "private": "Completion of the candidate/mode/scale matrix rewarded independently of the investigator actual scientific claims.",
  "metadata": "Paper title explicitly names dichloro-eta2-nitrato and reveals assignment."
}

## proposed ar problem

Investigate what molecular structures and nitrate coordination can be supported for the supplied iridium complex by its composition and reported IR observations. Develop an evidence-based structural interpretation, assess whether it is uniquely identifiable within the molecular model, and state which conclusions remain uncertain. The coordination topology and relative ligand arrangement are research questions, not supplied candidate answers.

## agent decisions

[
  "Generate defensible molecular structures from composition without a supplied hapticity or ligand geometry list.",
  "Choose which observations and molecular properties can discriminate their proposed assignment and assess nonuniqueness.",
  "Design and justify spectral assignment/error treatment; decide how the source discrepancy changes inference without prescribed four-vs-five fit tables.",
  "Select appropriate Ir electronic/relativistic models, structure search and validation, and decide when the evidence supports only a set of structures."
]

## public input changes

{
  "retain": "Full composition/charge/spin boundary and intact PPh3/nitrate identities; IR measurement medium.",
  "replace": "Remove tested_nitrate_bindings and geometry hints. Replace preassigned four-band subset with the entire main p8 peak list stripped of mode labels; preserve s/m/w exactly, with null where unreported.",
  "source_discrepancy": "Extra1561cm-1 shown as reported-in-discussion, not forced into an algorithm or candidate-specific subset.",
  "remove": "Source crystal geometry, hapticity, author structure title, required normal-mode fraction and spectral scaling matrix.",
  "sufficiency": "Public composition plus full spectral observations are enough to investigate bounded identifiability; uniqueness is not guaranteed."
}

## submission and scoring

{
  "minimum": "A real molecular investigation connecting generated structures or another valid representation to the IR observations and supported structural conclusions.",
  "alternative": "Any chemically suitable structural search/evidence/assignment strategy; no fixed eta labels or number of candidates, no required matching algorithm.",
  "conditional": "If unique structure is claimed, evidence must exclude relevant competing possibilities within stated scope; a failed optimizer does not prove basin absence. If assigning vibrations, identify their actual character and meaningful spectral comparison.",
  "partial": "Bounded nonuniqueness can earn strong credit when demonstrated. Historical stable eta1 and imperfect spectral discrimination show why agreement with the crystal is not the only acceptable scientific conclusion.",
  "schema_design": "Flexible systems/methods/models/records/results/claims with artifact hashes and locators, quantity definitions/units, claim-result-record IDs, partial/failure states; no fixed hypothesis count or result matrix."
}

## pr alignment

The authors assign a bidentate eta2-nitrato Ir(III) complex using crystallography together with spectroscopy (main pp3–4 Figure4/Table2; SI p15). Crystal Ir–O distances are2.173(2)/2.174(2)A, O–Ir–O60.02(9)degrees and nitrate N–O about1.294/1.291/1.209A. Reproduce the full-complex source molecular characterization and assess its evidential relationship to the supplied IR. Main p7 reports Gaussian09/WebMO B3LYP/LANL2DZ geometry optimization and IR with a frequency correction factor but does not state an unambiguous numerical factor. Main p3 reports calculated nitrate frequencies1541,1102,926cm-1. Label source frequencies and crystal data as source references; do not present them as your computed outputs. The detailed experimental list has1532/1261/1223/802cm-1 among other bands, while discussion/Table2 additionally includes1561; retain this discrepancy. Source crystal geometry establishes its own experimental assignment; it does not prove IR alone is unique. The V1 eta1 competition, relative-ligand search, mode-fraction thresholds and scaling residual matrix are benchmark extensions, not source protocol. Main p5 FMO species naming differs from Figure11 on p6; do not use this as unqualified evidence for the present nitrato complex.

## existing evidence reuse

{
  "usable": "V1 full75-atom five-structure B3LYP/LANL2DZ study retains genuine eta1 minima and eta2 minima,219 positive internal modes each, full1095 modes and uniform spectral comparisons. Lowest sampled eta2 is65.2637kJ/mol below lowest sampled eta1, but residuals/unmatched peaks support nonunique inference from the sparse IR.",
  "not_usable": "Finite five-start search is not global exhaustive search; gas electronic ordering is not crystal population. The known crystal answer is not blind AR discovery. Historical selected-band analyses do not automatically validate use of the newly supplied full peak list.",
  "binding": {
    "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_2f0a4f80a37fbccd/evaluation/phase1_reference_binding.json",
    "sha256": "16d3d9fbdf84a57058d2f13be8f9ef904bbb1f8fce643517b0e70c71f0ff0ca7",
    "evidence": {
      "report/scientific_acceptance.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/scientific_acceptance.json",
        "sha256": "93501ca1bd4a3bcf4de3a17b30da50c859d24833bdc3b12b7cf04f905d303b4c"
      },
      "report/results.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/results.json",
        "sha256": "9e5f196f310831cf9b83c9d0b61028d3ccaeceba47d2a625825dab8359d81c8d"
      },
      "report/verification_report.md": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/verification_report.md",
        "sha256": "59fb112db4efb677065d5223a1a425dbec324a7f2e8276ede84f4ce860338705"
      },
      "report/validation/contract_checks.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/validation/contract_checks.json",
        "sha256": "256fdec4b4702da0d5d1ebb9725fffdbbae477c910d3f557805e380dd3d877a2"
      },
      "report/resource_summary.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/resource_summary.json",
        "sha256": "b5bf2f99525518df4a7b4f22a9099551a8f529863db49cc7b0acad0575d5b2fb"
      },
      "evaluator_mapping.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/evaluator_mapping.json",
        "sha256": "b74ca0861847647f7e4e1c2e8dd53660c4004d5dfacb7536a735a1a5cd602876"
      },
      "task_snapshot/manifest.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/task_snapshot/manifest.json",
        "sha256": "fc71f1cae1c678e3d5a8816104bf78c021e035ec46961b3791a9f09045b03931"
      }
    },
    "role": "author_informed_V1_reference_not_V2_acceptance"
  }
}

## planned changes

[
  "Replace task.md and every old public data file with the neutral input inventory in this plan.",
  "Replace submission_schema.json and submission_guide.md; normalize visible task_info title, paper metadata and difficulty wording.",
  "Rewrite five live evaluator JSONs with paper-specific, claim-conditional evidence criteria and open_research policy; archive V1 ancillary reference documents as historical only.",
  "Write source_scope_audit.json/.md, v2_design_audit.md, visibility_scoring_audit.json/.md, reference reuse/validation documents and updated paper_route.md.",
  "Regenerate official manifests and perform package, runtime, export, schema, reference-ID and artifact integrity checks."
]

## acceptance checks

[
  "Source files and frozen baseline hashes remain exact.",
  "AR exports only planned neutral inputs; no author route/target/title or fixed matrix in public schema/metadata.",
  "AR and PR share the scientific schema, data and result rubric; only PR has explicit author guidance.",
  "Official validation and hashes pass; actual runtime loads dual_axis_100.open_research.v1 and two 100-point axes/product; AR and PR process rubrics differ.",
  "Synthetic positive alternative/negative/partial/failure fixtures pass format and declared IDs/artifact hashes; empty-complete, wrong numeric type/unit absence, missing artifact, broken ID/hash and old panel submissions are detected at appropriate layer.",
  "Scientific adversarial cases are documented for actual judge calibration, not declared passed by schema tests."
]

## limitations

[
  "Full raw experimental spectral intensities and measurement errors are unavailable; qualitative s/m/w labels are supplied without numeric conversion.",
  "The paper does not unambiguously report the frequency correction factor.",
  "V1 finite gas calculations do not establish global search or crystal thermodynamics.",
  "Source crystalline answer is disclosed only to PR; AR/PR information asymmetry is deliberate and process scores differ.",
  "Scientific judge calibration and runner isolation remain pending."
]


Historical classification is retained; openness changes arise from the public inputs, flexible contract and claim-conditioned rules. This document is evaluator-only.
