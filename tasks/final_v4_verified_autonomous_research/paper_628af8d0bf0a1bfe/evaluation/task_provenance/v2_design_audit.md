# paper_628af8d0bf0a1bfe: paper-specific V2 plan

Prepared 2026-09-28T16:29:31.375398+00:00. This plan precedes any V2 package copy/write.

## source documents

[
  {
    "path": "papers/paper_628af8d0bf0a1bfe/documents/main.pdf",
    "sha256": "327d99aeb6698b39bc1833dec1bb95f244445ee173fb51d060aa17ef6dcf52a1",
    "matches_audit": true,
    "declared_pages": 8,
    "material_type": "main_article",
    "pdf_pages_read_1_based": [
      5,
      6
    ]
  },
  {
    "path": "papers/paper_628af8d0bf0a1bfe/documents/supplementary_001.pdf",
    "sha256": "7d4e1b91fc4c4501b692d2b1804669e276daaf77502ac8755e5735dac565aec1",
    "matches_audit": true,
    "declared_pages": 56,
    "material_type": "true_supporting_information",
    "pdf_pages_read_1_based": [
      2,
      4,
      5,
      7,
      8,
      14,
      15,
      51,
      52,
      53,
      54
    ]
  }
]

## source scope

{
  "objects": "Full4a C36H14F12S2 and4c C34H22O2S2 neutral singlet molecules, not stripped pentalene or phenyl placeholders.",
  "conditions": "Isolated ground-state molecular comparison; no crystal-packing or finite-temperature population claim is required.",
  "question": "Substituent-associated molecular magnetic response and interpretation as antiaromatic character of the fused central pentalene.",
  "observation_status": "Published ordering is a computational result, not an independent experimental magnetic measurement; therefore it is withheld from AR.",
  "boundaries": "Do not generalize to every aromaticity criterion, arbitrary derivatives, bulk transport, reactivity or synthesis yield. Structural and electronic analyses may support the same magnetic interpretation."
}

## old task diagnosis

{
  "task.md": "Gave NICS tensor projection, both ring centroids, six signed heights, fixed-core vs relaxed controls, BLA and method sensitivity as full workflow.",
  "data/systems.json": "Observable_definition, geometry_comparison and model_boundary prescribed endpoint and measurement grid.",
  "schema": "geometries/probe_results/causal_comparison and constrained enums imposed matrix; two hypotheses minimum.",
  "evaluation": "Endpoint weights required same tensor grid and common-core controls instead of evidence appropriate to a claimed interpretation.",
  "history": "Earlier wrong small-molecule identities were excluded in V1 verification; V2 must retain complete identities rather than making input underspecified."
}

## proposed ar problem

Determine whether the two supplied benzothiophene-fused pentalenes differ in molecular magnetic response associated with their central pentalene unit. Develop and test an interpretation of any difference, or establish a defensible limit on what can be distinguished, and assess what your evidence supports about antiaromatic character within this pair. Neither a response ordering nor a substituent mechanism is given.

## agent decisions

[
  "Select a magnetic-response observable and how to localize or interpret it for the pentalene unit.",
  "Build valid full structures and decide what geometry, response or electronic comparisons are needed for the proposed attribution.",
  "Choose any scientifically adequate magnetic-response method and uncertainty analysis; current-density routes are not excluded by a NICS-only schema.",
  "Decide whether response association supports a causal substituent/antiaromatic interpretation and how far it generalizes."
]

## public input changes

{
  "retain": "Only systems list: complete names, neutral formula/charge/spin and substitution connectivity.",
  "remove": "observable_definition, probe heights, fixed_core geometry conditions, source target ordering and method.",
  "sufficiency": "Exact fused-ring nomenclature and both full substituent definitions determine constitutional identity; no crystal or optimized answer geometry is claimed supplied.",
  "metadata": "AR title and difficulty neutral; article title/DOI withheld. Source structural identities are not an answer to magnetic ordering."
}

## submission and scoring

{
  "minimum": "Actual relevant magnetic-response evidence on the full pair, mapped objects/coordinates and definitions, an evidence-based interpretation and limits.",
  "alternative": "NICS, current-density or another appropriate validated magnetic approach can be credited if it answers the bounded question; no required source method or sampling grid.",
  "conditional": "Tensor claims need a reproducible coordinate/sign convention; current claims need field/current/integration definitions; geometry-based attribution needs sufficient evidence that stated factors are separated.",
  "partial": "A genuine response contrast earns bounded finding credit without automatically earning a unique electronic-cause or universal aromaticity claim.",
  "schema_design": "Flexible systems/methods/models/records/results/claims with artifact hashes and locators, quantity definitions/units, claim-result-record IDs, partial/failure states; no fixed hypothesis count or result matrix."
}

## pr alignment

The authors report stronger paratropic response for4a than4c, interpreted with substituent electronic effects/topological charge stabilization (main p5 Figure5): NICS(1.7)zz about+23.6 and+19.2ppm. Reproduce the source response comparison and assess that interpretation. SI p14 uses M06-2X/6-31++G(d) optimization/frequencies with no symmetry assumption and NIMAG0, selected after4e-model bond-length benchmarking (SI p15). It specifies M06-2X/6-311+G(2d,p) NICS, probes1.7A above the five-carbon ring centroids, and a mean pentalene plane; main p5 instead prints6-31++G(2d,p), so declare which branch is reproduced. Source NICSzz is negative shielding along the molecular normal; retain reproducible coordinates and sign, not unaligned laboratory zz. Source ACID uses M06-2X/6-31G(d), a perpendicular field and pi-only contribution; it is complementary evidence, not permission to equate a picture with a universal aromaticity proof. X-ray structures are available for4b/4e, not4a/4c. The V1 multiheight/both-side grid and common-core interventions were benchmark extensions. They are not source protocol requirements or a uniquely acceptable test of the interpretation.

## existing evidence reuse

{
  "usable": "Identity-corrected full4a/4c minima,84 native shielding tensors and matched coordinate/BLA analyses. V1 relaxed ±1.7A mean contrast3.97640ppm and fixed-core contrast5.84716ppm support one feasible bounded NICS route and demonstrate that core geometry alone was insufficient in that particular design.",
  "not_usable": "Early truncated/wrong-identity data excluded. No proof of unique pure electronic causation: periphery differs in the frozen-core design. No universal aromaticity or reactivity validation, nor current-density route calibration.",
  "binding": {
    "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_628af8d0bf0a1bfe/evaluation/phase1_reference_binding.json",
    "sha256": "55c0f50f04fded102e83818998d9dfb025b446d38b7fbf4cf1e618a90671e40c",
    "evidence": {
      "report/scientific_acceptance.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/scientific_acceptance.json",
        "sha256": "3f9a43a186de439eb5093528fcdccb8824763995b62dc66deb3834295da42295"
      },
      "report/results.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/results.json",
        "sha256": "e72c64f2f69e862eba9e94898205369d78bf4cc2353a84dd42e7e2c51ba261da"
      },
      "report/verification_report.md": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/verification_report.md",
        "sha256": "83b0363bcfa764b0c97088021f8d270d9a5d9c516c8de7fd6cbd19873a020611"
      },
      "report/validation/contract_checks.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/validation/contract_checks.json",
        "sha256": "329fc1ce259a07d888c3db33174c356085dc97d6adc08df01a4e6de19edfa0c4"
      },
      "report/resource_summary.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/resource_summary.json",
        "sha256": "9f9345dc21f3b9054e6adf2dac12d0f70559cccfea7ae66b33e631d8e10c786d"
      },
      "evaluator_mapping.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/evaluator_mapping.json",
        "sha256": "e1dc9d0538e60e8ba74dbdb7c2c93441dba00049d2abdbdac8df1b2a12efdcbe"
      },
      "task_snapshot/manifest.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/task_snapshot/manifest.json",
        "sha256": "f9f17039b4730ebd761b66557b145d249feea8c5c9a9bb27c5f252f2b5b9d1c0"
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
  "No experimental magnetic-response target supplied for4a/4c.",
  "Published NICS basis descriptions differ; PR must disclose that ambiguity.",
  "One finite full-molecule NICS route is supported by historical evidence; other routes need their own validation.",
  "No new scientific jobs or judge calibration; actual runner isolation pending."
]


Historical classification is retained; openness changes arise from the public inputs, flexible contract and claim-conditioned rules. This document is evaluator-only.
