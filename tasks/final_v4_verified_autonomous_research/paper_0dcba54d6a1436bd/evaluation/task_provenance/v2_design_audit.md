# paper_0dcba54d6a1436bd: paper-specific V2 plan

Prepared 2026-09-28T16:45:15.888596+00:00. This plan precedes any V2 package copy/write.

## source documents

[
  {
    "path": "papers/paper_0dcba54d6a1436bd/documents/main.pdf",
    "sha256": "1f5313ccf56ae62c57d8601e056099404ee5a1080b2d31189c5c7b9365b8e6ff",
    "matches_audit": true,
    "declared_pages": 11,
    "material_type": "main_article",
    "pdf_pages_read_1_based": [
      6,
      7,
      8
    ]
  },
  {
    "path": "papers/paper_0dcba54d6a1436bd/documents/supplementary_001.pdf",
    "sha256": "3f9dab0079efd4f0e2879bf457db34f03f8e6cee529e9fd1c2cbe17e43795198",
    "matches_audit": true,
    "declared_pages": 30,
    "material_type": "true_supporting_information",
    "pdf_pages_read_1_based": [
      4,
      5,
      6,
      7,
      17,
      26,
      27,
      28,
      29
    ]
  }
]

## source scope

{
  "objects": "Full Z NPCZCS C43H39N3O2, AQCZCS C41H32N2O2 and PQCZCS C41H32N2O2; neutral singlet ground states with complete hexyl/butyl substituents. This is a three-compound subset of the four-compound source series.",
  "conditions": "Ground-state molecular structures and vertical singlet excitation/absorption in dichloromethane; the representation of solvation and conformational scope are chosen and justified by the agent.",
  "question": "Differences in low-energy absorption and excitation character associated with the appended molecular groups, including the limits of a proposed structural explanation.",
  "observation_status": "No source optimized geometry, orbital ordering, excitation label or numerical spectral target is an AR input. Source computed state assignments are claims for PR reproduction, not observed facts that AR must assume.",
  "boundaries": "Single-molecule electronic/vertical optical properties. No claim of excited-state relaxation, radiative/nonradiative rates, fluorescence quantum yield, aggregate-induced emission/quenching, grinding response, crystal packing or device efficiency follows from this task."
}

## old task diagnosis

{
  "task.md": "Specified common torsions, a five-root minimum, state tracking, fixed fragments and two functionals; supplied the discriminating research program instead of leaving it to the agent.",
  "data/inputs/systems.json": "model_boundary.minimum_root_window=5 and torsion_control defined a common three-angle grid and three fragments; primary_vertical_excitation_medium prescribed a continuum representation rather than only the physical solvent.",
  "schema": "Fixed excitation/torsion/state-comparison panels, fragment/state labels and minimum hypotheses privileged one CT diagnostic design.",
  "evaluation": "Full credit depended on the reference comparison matrix rather than evidence adequate for whichever molecular explanation is claimed.",
  "scope_risk": "The source studies bulk emission too, but molecular vertical absorption cannot establish its aggregate, quantum-yield or grinding claims. State energy, bright transition, orbital gap and emission maximum must remain distinct."
}

## proposed ar problem

Determine whether and how the three supplied molecules differ in low-energy singlet absorption and in the spatial character of the associated electronic excitations in dichloromethane. Develop and test a molecular explanation for any established differences, or establish a defensible limit on what can be distinguished. Assess what the evidence supports about the relation between molecular structure and these excitation properties. No spectral ordering or state assignment is supplied.

## agent decisions

[
  "Construct the full Z molecules and choose defensible conformational and solvation representations for the stated molecular question.",
  "Select the relevant low-energy states and observable definitions; decide how much state space is needed to support the specific conclusion without a prescribed root count.",
  "Develop a molecular explanation and choose comparisons or interventions that discriminate it from relevant geometric, electronic or modeling effects.",
  "Choose suitable electronic-structure and excitation-character analyses, with any state correspondence justified at the resolution actually claimed.",
  "Revise the explanation or report a bounded inconclusive/negative result when evidence cannot distinguish the proposed effects."
]

## public input changes

{
  "retain": "Only the three exact full molecular identities, neutral charge/spin and Z stereochemistry.",
  "remove": "minimum_root_window, torsion_control.junction/grid/fragments, mandatory continuum model, method pair and numerical/source state targets.",
  "replace": "State dichloromethane as the physical medium and single-molecule vertical-excitation scope without dictating a computational solvation method.",
  "sufficiency": "Full systematic names specify the constitutional graphs and Z isomers, including all alkyl chains; no supplied spectral value or source geometry is required to define this computational comparison. Prospective independent construction/solution remains untested.",
  "metadata": "Neutral AR title/difficulty; paper bibliographic answers withheld. Molecular acronyms remain identity labels only."
}

## submission and scoring

{
  "minimum": "Actual mapped structural and excitation evidence for the supplied set, defined optical/state-character results, and a conclusion supported at its stated molecular scope.",
  "alternative": "A suitable wavefunction, response, transition-density or other validated excitation analysis may be credited; no NTO, fragment partition, functional pair, torsion grid or hypothesis number is compulsory.",
  "conditional": "Comparing corresponding states requires a defensible characterization/correspondence criterion; a causal torsion or substituent claim requires evidence that relevant confounding factors were assessed. Absorption maxima, S1, orbital gaps and emission energies cannot be interchanged.",
  "partial": "Supported excitation differences can earn finding credit even if their cause remains unresolved; a failed calculation or unexplored conformer space is not evidence that no distinction exists.",
  "schema_design": "Flexible systems/methods/models/records/results/claims with artifact hashes and locators, quantity definitions/units, claim-result-record IDs, partial/failure states; no fixed hypothesis count or result matrix."
}

## pr alignment

The source optimizes gas-phase ground states with B3LYP/6-31G(d,p), without symmetry constraints, and reports frequency checks with no imaginary modes (main p7). Its TD-DFT comparison uses Gaussian 09W, 6-31G(d,p) and PCM dichloromethane. B3LYP, CAM-B3LYP, M06, M06-2X, M06-HF and omegaB97XD are compared for NPCZCS/AQCZCS; the authors select M06 for subsequent analysis, including PQCZCS. Reproduce the disclosed structural and M06 excitation baseline, addressing the source functional-selection comparison where relevant to a claim about that selection. SI Tables S7–S9 give S1 energies/oscillator strengths of 2.9521 eV/0.4988 for NPCZCS, 2.5853 eV/0.1928 for AQCZCS and 2.4342 eV/0.0116 for PQCZCS. Tables S5/S6 instead list major bright transitions: 375.88 nm/0.8847 (NP, S2), 382.38 nm/1.0178 (AQ, S4), and 379.86 nm/1.0397 (PQ, S5); these are not S1 values. Main p8 and Figure5 interpret NP/AQ S1 NTO hole density on the carbazole–cyanostilbene region and particle density on the appended group as ICT, while PQ S1 is described as locally excited on phenanthraquinone. This distinction qualifies the broader ICT wording in the preceding discussion; assess it rather than assuming every low state is CT. Source ground-state HOMO–LUMO gaps are different observables from these excitation energies. Fixed-angle scans, ten-state windows, a common three-fragment partition and a mandatory second functional were V1 benchmark extensions, not a source reproduction protocol. Neither those extensions nor source numerical agreement alone establishes the broader solid-state emission mechanisms.

## existing evidence reuse

{
  "usable": "The bound V1 full-molecule study contains 30 native logs, three free and nine frozen-angle geometries, 18 TD calculations and 180 transition records. It supports a feasible molecular-excitation route and examples of changed state character/root order. For its specific M06 15-to-75-degree design, tracked CT energies change by approximately +0.2215, +0.0642 and +0.0404 eV for NP/AQ/PQ; a PQ localized state changes by about -0.0018 eV and swaps root order with the CT state. These are V1 computed findings, not publication targets.",
  "not_usable": "A finite constrained grid is not a conformer ensemble or whole potential-energy surface. Three-fragment transfer-probability similarity is not phase-preserving many-electron wavefunction overlap; across different molecules it compares excitation types, not literally the same many-body state. V1 does not validate emission rates, AIE/ACQ, quantum yield or device claims, nor all valid alternative excitation methods.",
  "binding": {
    "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_0dcba54d6a1436bd/evaluation/phase1_reference_binding.json",
    "sha256": "82c4e526284821bc29f9957c49cfc173ac7f52f838b7a002032652e15f2a3544",
    "evidence": {
      "report/scientific_acceptance.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/report/scientific_acceptance.json",
        "sha256": "582382b77e8beafbb73ecfd1bce197e2705281d3da2264385c9fb762c8ae4f35"
      },
      "report/results.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/report/results.json",
        "sha256": "02c95854adc7d4957496535e02d193283472c2fa436c5884e523bba6dd6eb947"
      },
      "report/verification_report.md": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/report/verification_report.md",
        "sha256": "92285fa82d16b72272e4ab8af76955113330e8623786efec4dedd6fe72e4efa0"
      },
      "report/validation/contract_checks.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/report/validation/contract_checks.json",
        "sha256": "36e8349ee3a832f8d168fd05d61bcf6b4ad7e4848e9ba4d22c21dd1293a126e4"
      },
      "report/resource_summary.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/report/resource_summary.json",
        "sha256": "5b507a5fefd808ce4571a3b4a6e1baddc366e0e3f01e35dcd7e8c25126631e6c"
      },
      "evaluator_mapping.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/evaluator_mapping.json",
        "sha256": "97d5a39964855b1c0a589f022446d6cb9ef1a590d73b6a3199437c6bc939b68e"
      },
      "task_snapshot/manifest.json": {
        "path": "docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/task_snapshot/manifest.json",
        "sha256": "9f1e8f6fc85d8356e9e10615b58a1ca79b50661c4dc64c9000cb11be469f7f88"
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
  "Source scope is deliberately restricted to three named compounds and molecular vertical absorption; the fourth source compound and bulk photophysics are not required.",
  "The source uses both broad ICT language and an explicit PQ S1 LE assignment; PR must preserve that distinction.",
  "Historical constrained-state calculations support only their stated structures, methods and finite grid, not all conformations or methods.",
  "Independent end-to-end AR construction/solution, alternative-route semantic calibration and runtime isolation remain pending."
]


Historical classification is retained; openness changes arise from the public inputs, flexible contract and claim-conditioned rules. This document is evaluator-only.
