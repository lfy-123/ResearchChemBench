# paper_2f302589e5e9e420: paper-specific V2 plan

Prepared 2026-09-28T16:27:43.129319+00:00. This plan precedes any V2 package copy/write.

## source documents

[
  {
    "path": "papers/paper_2f302589e5e9e420/documents/main.pdf",
    "sha256": "a97be22902a7ec8a348c8112368e5422ea2af4782e0d4af6f818237fa2a30563",
    "matches_audit": true,
    "declared_pages": 9,
    "material_type": "main_article",
    "pdf_pages_read_1_based": [
      4,
      6,
      7
    ]
  },
  {
    "path": "papers/paper_2f302589e5e9e420/documents/supplementary_001.pdf",
    "sha256": "d4a715bfc18bff524f50298937739473903e9fb1012e7cdd5daf9692e42ae942",
    "matches_audit": true,
    "declared_pages": 26,
    "material_type": "true_supporting_information",
    "pdf_pages_read_1_based": [
      22,
      23,
      24,
      25,
      26
    ]
  }
]

## source scope

{
  "objects": "Full neutral singlet source model fragments EPI1 C13H21NO2 and EPI2 C14H23NO3, not polymer chains or epoxy monomers.",
  "conditions": "Isolated molecular models; source computational methods omit explicit bulk polymer environment. Agent states any model temperature/environment. Experimental cured resins are a separate scale.",
  "observations": "Main p6 reports lower dielectric constant for methoxy-containing cured analogues; main p7 reports thermal OH-band shift for methoxy-containing resin, while SI p22 FigureS34 lacks analogous blue shift without methoxy. These observations do not prove the molecular cause.",
  "boundary": "Substitution, conformation, molecular polarity and interpretive reach within these exact source fragments; no quantitative bulk dielectric prediction."
}

## old task diagnosis

{
  "task.md": "Required OH orientation interventions, a common-backbone control and gas298.15K ensemble mu-squared.",
  "data": "SI-derived EPI1_start.xyz/EPI2_start.xyz were mislabeled not declared minima; EPI2 visibly supplies the claimed Hbond geometry. study_scope primary_ensemble_descriptor and required_controls disclose route.",
  "schema": "conformers/ensembles/interventions and minimum two hypotheses impose search and analysis design.",
  "private_rules": "Control-matrix coverage and fixed observable dominate, despite a valid alternate ensemble trend.",
  "metadata": "Article title explicitly discloses intramolecular Hbond mechanism and Dk reduction."
}

## proposed ar problem

Determine whether, and under what molecular conditions, adding the ortho-methoxy group changes the polarity of the supplied EPI1/EPI2 model fragments. Develop a defensible molecular explanation of the behavior you find and assess how far it can inform interpretation of the reported dielectric behavior of the corresponding cured resins. The sign, magnitude and generality of the molecular effect are to be established, not assumed.

## agent decisions

[
  "Choose a meaningful molecular definition of polarity and explain its relevance/limits for dielectric interpretation.",
  "Choose structural sampling or other evidence sufficient to determine whether a substitution effect is conformation-dependent, and justify scope.",
  "Propose and challenge a molecular explanation without being handed OH rotation/common-backbone controls.",
  "Determine the appropriate treatment of medium, statistical weights and uncertainty if those quantities are claimed; no fixed temperature or estimator is imposed."
]

## public input changes

{
  "replace": "Replace both source optimized XYZs and the fixed study_scope with systems.json topology and observations.json.",
  "identity_derivation": "RDKit bond perception on exact frozen XYZs yielded CCN(C)C[C@H](O)COc1cccc(C)c1 and CCN(C)C[C@H](O)COc1cc(C)ccc1OC. Heavy-atom graph checked against SI coordinate connectivity and formula. This is representation conversion, not a geometry calculation.",
  "stereochemistry": "The @ form retains the same representative stereochemistry encoded in the source model coordinates; it is not an experimental claim of enantiopurity. Cartesian conformational information is discarded.",
  "retain": "Full N-ethyl/N-methyl substituents, ring methyl positions, ortho methoxy, charge/multiplicity and legitimate macroscopic context.",
  "remove": "Hbond labels, optimized geometry, dipole target, required OH/common-backbone axes and default ensemble definition from all AR surfaces."
}

## submission and scoring

{
  "minimum": "Actual molecular findings on the polarity difference and its conditions, auditable identity/method/output records, an explanation with evidence and restricted relation to resin data.",
  "alternative": "Validated electronic-structure, justified analytical/statistical or other suitable molecular routes are allowed; a chosen polarity descriptor must be defined and relevant.",
  "conditional": "If ensemble results are claimed, justify energies, populations, temperature, deduplication and sampling uncertainty. If a hydrogen bond or causal orientation effect is claimed, provide evidence discriminating that interpretation rather than a label.",
  "partial": "A source-like single conformer can support a conformer-specific finding, not universal substitution or bulk Dk; evidence showing reversal/uncertainty can receive appropriate full criteria credit.",
  "schema_design": "Flexible systems/methods/models/records/results/claims with artifact hashes and locators, quantity definitions/units, claim-result-record IDs, partial/failure states; no fixed hypothesis count or result matrix."
}

## pr alignment

The paper assigns the lower polarity of one EPI2 model conformation to an intramolecular hydrogen bond between the curing-generated OH and ortho-methoxy group (main pp6–7, Figure4D–E), reporting dipoles EPI1=2.2223D and EPI2=1.9036D, about14.3% lower. Reconstruct the exact full models from the supplied identities and reproduce/assess this source single-structure comparison. Main p4 specifies Gaussian16 A.03, B3LYP-D3(BJ)/6-31G* geometry/frequency calculations and ma-def2-TZVPP dipole calculations, with Multiwfn ESP analysis. Figure4 caption instead names CAM-B3LYP/6-311G(d,p); report this conflict and identify which protocol you reproduce rather than silently combining them. SI pp23–26 gives the source structures. The source resin FTIR association does not constitute a measured isolated-molecule IR spectrum. Conformational population analyses, OH-rotation and common-backbone interventions in the V1 benchmark were added tests, not mandatory author procedures. Additional tests should be distinguished from faithful reproduction and may contradict the source single-structure generalization.

## existing evidence reuse

{
  "usable": "Bound V1 source-like minima/dipoles, finite five-conformer/deduplicated ensemble, actual OH mode evidence and matched diagnostic structures. Source-like dipoles2.223986/1.899047D decrease, but sampled <mu²>3.426299/3.606752D² increases about5.27%, with low-frequency treatments +5.36/+5.43%. This concretely supports accepting a bounded contrary conclusion.",
  "not_usable": "Finite local sampling is not a complete conformational partition function or bulk polymer Dk. Fixed OH nonstationary structures do not yield directly experimental IR. No V2 blind/judge calibration.",
  "binding": {
    "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_2f302589e5e9e420/evaluation/phase1_reference_binding.json",
    "sha256": "8cdca0810303cf35f079177082705306a8ee03262aa6d67625da76ccc8c12fd3",
    "evidence": {
      "report/scientific_acceptance.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/report/scientific_acceptance.json",
        "sha256": "97d5456f09c735b7daee9654d49af32f84b1e425a290ff14c2d334f07d77b24d"
      },
      "report/results.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/report/results.json",
        "sha256": "30f211cdb050db555de1b53e6dac767044f48228b360739cd7f3bcfcb1fe3ae4"
      },
      "report/verification_report.md": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/report/verification_report.md",
        "sha256": "b86a311aa48d054e4ce13d53dd7c23a9d972037727ea50eb3ab9b1da15fccc4e"
      },
      "report/validation/contract_checks.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/report/validation/contract_checks.json",
        "sha256": "c165136fa0d97d07efae43418539bf65ce64fa5d8597f45dcbccc395e336b164"
      },
      "report/resource_summary.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/report/resource_summary.json",
        "sha256": "3e63542605e65aa9aed46581c92cb5885bf23352198043add5e339deb715ec6f"
      },
      "evaluator_mapping.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/evaluator_mapping.json",
        "sha256": "c8afe04e888da14e547a0575eba6272212a49da4bc7a7f5ed818ad415ab748bf"
      },
      "task_snapshot/manifest.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/task_snapshot/manifest.json",
        "sha256": "14d3ee08883cf98e4da86c170275e3dddcbc14ace13d0b4f8bf32f3d6189a7c9"
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
  "Source method paragraph and Figure4 caption conflict.",
  "Source stereochemistry is a representative coordinate choice, not evidence of enantiomeric preparation.",
  "Available raw science only samples finite local molecular structures, not polymer ensembles.",
  "Actual semantic calibration and runner isolation remain pending; this round performs no new simulations."
]


Historical classification is retained; openness changes arise from the public inputs, flexible contract and claim-conditioned rules. This document is evaluator-only.
