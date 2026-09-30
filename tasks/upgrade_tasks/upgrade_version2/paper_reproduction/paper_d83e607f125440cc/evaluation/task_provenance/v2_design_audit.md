# paper_d83e607f125440cc: paper-specific V2 plan

Prepared 2026-09-28T16:23:56.843722+00:00. This plan precedes any V2 package copy/write.

## source documents

[
  {
    "path": "papers/paper_d83e607f125440cc/documents/main.pdf",
    "sha256": "d63064511e76ff3931ee92587cddf3e8cc5c9b3eb90ec95e717ab9ce7d838b2c",
    "matches_audit": true,
    "declared_pages": 5,
    "material_type": "main_article",
    "pdf_pages_read_1_based": [
      2,
      3,
      4
    ]
  },
  {
    "path": "papers/paper_d83e607f125440cc/documents/supplementary_001.pdf",
    "sha256": "2f5e58e7475452312c03fef41f7156127656bc4ea3a7d83f138b6c0772c540c8",
    "matches_audit": true,
    "declared_pages": 50,
    "material_type": "true_supporting_information",
    "pdf_pages_read_1_based": [
      34,
      35,
      36
    ]
  }
]

## source scope

{
  "objects": "Five full benzyl-alcohol molecules, para H/Cl/Me/OMe/SMe, with neutral starting identities. Reaction-state choices belong to the investigation, with explicit atom/electron accounting.",
  "observed": "Main p3 reports high or quantitative conversion for para OMe/Me/Cl and relatively low hydroxyl oxidation for para SMe in the preparative study. No common quantitative yield table is fabricated.",
  "conditions": "Flavin-mediated visible-light electrophotochemical oxidation; main p2 Table1 analytical context uses 450 nm,25 C,argon,MeCN or9:1MeCN/water,0.3V applied vs Ag wire. These are context, not calculated electrode references or automatically the entire preparative protocol.",
  "question_boundary": "Molecular origin and explanatory limits of the substituent dependence within the source oxidation problem.",
  "excluded": "Full flavin/electrode/oxygen reaction networks, catalytic rates, yields or proof of a complete mechanism from isolated molecular descriptors."
}

## old task diagnosis

{
  "task.md": "Preselected electron-removal then benzylic-H-loss causal chain; all five I_e/D_e, fixed Hirshfeld, SMe/OMe conformers+continuum and prediction challenge mandatory.",
  "data/inputs/study_scope.json": "states/channel/primary_observables/primary_phase fields fixed the mechanism and energy convention before research.",
  "public_XYZ": "SI-derived SMe radical-cation answer geometry leaked one selected state.",
  "submission_schema.json": "species enum, two-hypothesis minimum and series/pair_controls/prediction_test panels encoded the route.",
  "evaluation": "Weights rewarded completion of same control matrix; source numbers and old partial validation prose could be mistaken for V2 universal truth.",
  "task_info.json": "Title explicitly named radical-cation hydrogen loss, paper DOI/title enabled answer lookup."
}

## proposed ar problem

Investigate what can be established at the molecular level about the different oxidation behavior of the supplied para-substituted benzyl alcohols. Develop and test an explanation for the comparatively poor conversion of the methylsulfanyl alcohol toward its aldehyde under the reported flavin-mediated electrophotochemical conditions. Determine which parts of that explanation your evidence supports, which remain unresolved, and whether the molecular evidence is sufficient to explain the observation.

## agent decisions

[
  "Choose scientifically justified molecular states, observables and explanation instead of being assigned radical-cation hydrogen loss.",
  "Decide which comparisons within the supplied five identities are informative and how to distinguish a causal claim from a descriptor correlation.",
  "Select methods, treatment of environment and search/validation depth appropriate to the claims; decide whether evidence is insufficient.",
  "Choose follow-up or stop after actual observations; no mandatory retrospective pseudo-heldout challenge."
]

## public input changes

{
  "retain": "Neutral SMILES, formula and member labels; source qualitative observation and explicitly qualified experimental context.",
  "replace": "study_scope with systems.json and observations.json, with no state/channel/observable recipe.",
  "remove_from_AR": "SMe radical-cation XYZ, author mechanism, spin targets, dissociation targets, method and fixed control matrix. Source version preserved in evaluator-only historical archive.",
  "metadata": "Neutral scientific title; AR paper fields empty.",
  "sufficiency": "Neutral SMILES determine all five full molecules without using optimized answer structures; agent builds states it elects to study."
}

## submission and scoring

{
  "minimum": "Reproducible molecular investigation addressing the SMe contrast, actual identities/states, meaningful numerical or otherwise testable findings with raw evidence, explicit evidential support and limits.",
  "valid_alternatives": "Any suitable molecular explanation and validated evidence design within scope; no required descriptor, spin partition, solvent pair or hypothesis count.",
  "conditional_validity": "Reaction energies require balanced atom/electron references; electron removal is not electrode potential; dissociation is not activation barrier; a claimed spin site requires a defined analysis.",
  "partial": "Supported bounded findings receive their earned criterion credit. A validated counterexample/insufficiency result is eligible; not performing tests is not proof of insufficiency.",
  "schema_design": "Flexible systems/methods/models/records/results/claims with artifact hashes and locators, quantity definitions/units, claim-result-record IDs, partial/failure states; no fixed hypothesis count or result matrix."
}

## pr alignment

The article (main pp3–4, Figure3) proposes substrate-to-photoexcited-flavin electron transfer and discusses relatively sulfur-localized radical-cation spin and difficult benzylic H-atom loss for SMe. Reproduce the source molecular evidence before assessing that interpretation. SI S6 (p34) reports B3LYP/6-311+G(d) optimizations in vacuum and CPCM water/MeCN, frequency validation of minima, and Hirshfeld spin analysis. TableS8 gives SMe sulfur spin about0.401. TableS16 (p36) reports gas-phase benzylic C–H electronic dissociation energies H/Cl/Me/OMe/SMe=139.4/157.3/152.8/173.7/198.5 kJ/mol. For this reference channel distinguish loss of neutral H from proton loss: parent radical cation(+1,doublet), dehydrogenated cation(+1,singlet), H(0,doublet); use E(product)+E(H)−E(parent), with no ZPE/thermal addition to the stated electronic quantity. SI TableS11 prints a positive SMe water electronic energy; flag it as a source inconsistency rather than adopting it unquestioningly. These source anchors do not establish a kinetic mechanism or yield. The V1 complete neutral-ionization matrix, paired conformer challenges and retrospective Cl test were benchmark additions, not source requirements.

## existing evidence reuse

{
  "usable": "The exact bound V1 report contains five gas electronic comparisons, mapped spin, curvature, finite gas conformers/common CPCM and a retrospective Cl cross-check. It establishes one feasible molecular route and supports auditing channel bookkeeping and numerical limitations.",
  "not_usable": "No blind AR performance, no complete mechanism, activation barrier/yield prediction, global conformational guarantee, general functional error interval or acceptance of a different V2 route.",
  "binding": {
    "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_d83e607f125440cc/evaluation/phase1_reference_binding.json",
    "sha256": "635bf0b066af8892849f4ccf344faac508044a85d62cc2b9588a7933f7a6f6b2",
    "evidence": {
      "report/scientific_acceptance.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/report/scientific_acceptance.json",
        "sha256": "49e18b9121831ce3124bf46b69e5d920702a010602026d9665de3019bc79c814"
      },
      "report/results.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/report/results.json",
        "sha256": "70060d9972a807edf7043f6c36b6b4e4a8ac360e6486c5a29a9524ac5e264ab8"
      },
      "report/verification_report.md": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/report/verification_report.md",
        "sha256": "86f9eb89a015d957bb92e9f7474860d8c474028d2b9d54c85492556202f40b53"
      },
      "report/validation/contract_checks.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/report/validation/contract_checks.json",
        "sha256": "57ba85d278458a69502dcdcb0e863b8674d5d6435ec53c1d530619333e21c91c"
      },
      "report/resource_summary.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/report/resource_summary.json",
        "sha256": "1e21130c422d68be48c9af1977e93abbd5bda22450df07dfdc054d8daa890b4a"
      },
      "evaluator_mapping.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/evaluator_mapping.json",
        "sha256": "9fd729d8a1f3a65b13b5ea35ab6b0f95f09989194048ddb89addedc211ae4973"
      },
      "task_snapshot/manifest.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/task_snapshot/manifest.json",
        "sha256": "0fcbbd7ffd7acb6183344d4e0037218da4ad37430e46594a7983bc70be4cb936"
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
  "Qualitative experimental contrast only; neither complete reaction kinetics nor a common numerical yield dataset is supplied.",
  "No new scientific calculations, semantic judge or blind AR run in this authoring round.",
  "Full runner isolation and trace-based prospective chronology require coordinator integration.",
  "SI SMe water energy contains a sign inconsistency; it is not silently treated as a reliable numerical target."
]


Historical classification is retained; openness changes arise from the public inputs, flexible contract and claim-conditioned rules. This document is evaluator-only.
