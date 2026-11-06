# paper_9ec32e81e2826041: paper-specific V2 plan

Prepared 2026-09-28T16:38:45.221773+00:00. This plan precedes any V2 package copy/write.

## source documents

[
  {
    "path": "papers/paper_9ec32e81e2826041/documents/main.pdf",
    "sha256": "c494b9ed5388f0c6d968d8e80ce851426473aa9779a3c3930927445340195dec",
    "matches_audit": true,
    "declared_pages": 9,
    "material_type": "main_article",
    "pdf_pages_read_1_based": [
      3,
      4,
      5
    ]
  },
  {
    "path": "papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf",
    "sha256": "dbb8ec5153da3d86acde2fd320f01cc1bae86bf16cebf2fd2cf835280933d7cb",
    "matches_audit": true,
    "declared_pages": 23,
    "material_type": "true_supporting_information",
    "pdf_pages_read_1_based": [
      3,
      4,
      13,
      14,
      15,
      16,
      21,
      22
    ]
  }
]

## source scope

{
  "objects": "One full80-atom neutral singlet Z-cAACCy, C35H43NZn; not Z-SIP or Z-IP.",
  "observations": "Main p3 different colorless/yellow crystals: diffuse-reflectance onset about430nm and visible band extending about500nm respectively. Main p4 both give same yellow solution.",
  "molecular_question": "Configuration/stability and absorption with possible Zn electronic involvement; distinct thermodynamic and optical claims need their own evidence.",
  "boundary": "Isolated molecular ground-state and vertical optical interpretation; experimental crystalline edge is not identical to an isolated transition. No crystal populations, full packing, phosphorescence/SOC/lifetimes or Z-IP photocatalysis."
}

## old task diagnosis

{
  "task.md": "Fixed dispersion–conformation–absorption causal chain, PBE0,300K D3on/off, two named families, cross-geometry decomposition and TD5 matrix.",
  "data": "coplanar.xyz and perpendicular.xyz are source optimized answer conformations and labels; study_scope encodes method, families, D3 toggles and root window.",
  "schema": "conformers/energy_decomposition/transitions plus fixed families and minimum hypotheses.",
  "evaluation": "Required same D3 causal decomposition even for a valid nonauthor optical explanation.",
  "reference": "V1 partial D3 evidence exists, no completed four-family report; cannot use phase1 status as full science pass."
}

## proposed ar problem

Investigate the relationship between accessible molecular configurations and low-energy electronic absorption of the supplied Z-cAACCy complex. Determine what molecular evidence can explain the optical contrast between its reported crystal samples, what role the Zn center has in the relevant electronic response if any, and what cannot be inferred from an isolated-molecule study. Select and test your own account of the structure–property relationship without assuming a preferred geometry or metal contribution.

## agent decisions

[
  "Generate configurations and choose what stability question is necessary for the optical interpretation without two supplied geometry families.",
  "Choose the electronic-response method and evidence needed to quantify, challenge or reject a Zn-role claim.",
  "Choose how to study any energetic or optical cause; no obligatory dispersion switch, fixed cross-energy grid or root count.",
  "Decide which differences are molecular and which remain confounded by experimental solid/solution environments."
]

## public input changes

{
  "replace": "Replace both labeled optimized XYZs and study_scope with complete system.json atom/bond topology and observations.json.",
  "identity_audit": {
    "coplanar_source_sha256": "59df86e6cda55163e57b02200ef2882b7af55f76d1f7adfd1d33172b641d8814",
    "perpendicular_source_sha256": "60f033c21debfdf44fa1ae4ce97e0dd01c1376397792b8beddbfc3df3bfc0be9",
    "atoms": 80,
    "bonds": 85,
    "three_aromatic_cycles": [
      [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      [
        7,
        8,
        9,
        10,
        11,
        12
      ],
      [
        26,
        27,
        28,
        29,
        30,
        31
      ]
    ],
    "checks": "Both exact full source graphs agree with independently inferred covalent/metal connectivity; graph isomorphism true; no geometry variables exported."
  },
  "retain": "All35C43H1N1Zn, full Dipp/isopropyl and cyclic substituents; source charge/multiplicity and optical observations.",
  "remove": "Planarity labels/angles, source geometries, dispersion mechanism, energies, roots and orbital composition answers from AR."
}

## submission and scoring

{
  "minimum": "Traceable relevant configurations/states and optical evidence, explanatory assessment of Zn participation or its absence, limitations connecting molecular model to observed samples.",
  "alternative": "Valid electronic-structure or other suitable quantum analysis is allowed without PBE0/D3 toggles, fixed geometry family names or TD root count.",
  "conditional": "Claimed stable configurations need minimum evidence; free-energy/population statements need coherent thermodynamics; state comparison needs physically justified correspondence rather than matching root numbers; causal dispersion assertions need disentanglement appropriate to that claim.",
  "partial": "D3 source minima support feasibility only; genuinely partial optical or thermochemical findings remain partial. Missing Hessians/transition validation cannot become a proof of ambiguity.",
  "schema_design": "Flexible systems/methods/models/records/results/claims with artifact hashes and locators, quantity definitions/units, claim-result-record IDs, partial/failure states; no fixed hypothesis count or result matrix."
}

## pr alignment

The source reports colorless/perpendicular and yellow/more-coplanar crystal forms, with angles between carbene/zincafluorene ring planes83.1 and23.9degrees (main p3 Figure1). Its interpretation is that coplanarity stabilizes a C–Zn pi-type LUMO and enables lower-energy absorption; source Zn4p LUMO contributions are2.1% versus8.5% (main p4 Figure2). Reconstruct the full molecular conformations and reproduce/assess this baseline. SI p3 uses PBE0/6-311+G** with D3BJ for ground-state optimizations and frequencies, also separately omits D3BJ to examine dispersion; G is at300K. TableS7 gives Gcoplanar−Gperpendicular−0.1kJ/mol withD3BJ and+4.8without forZ-cAACCy. TD-PBE0/6-311+G** on the optimized ground states gives five lowest singlets; TablesS8/S9 report S1=3.1097eV,f0.0883 versus2.4526eV,f0.0132. Source NAO/Multiwfn orbital analysis is one metal-character definition, not a unique physical population observable. Thermal low-frequency treatment and population implications require scrutiny; identical yellow solutions do not measure a gas free-energy difference. Fixed cross-geometry decompositions, alternative root-matching diagnostics and broader sensitivities are benchmark additions. Z-IP SOC/phosphorescence calculations are not part of this molecule reproduction.

## existing evidence reuse

{
  "usable": "Two exact D3 full-molecule native minima with234 positive internal modes and mapped graphs; native300K RRHO deltaG about−0.0473kJ/mol, with historical entropy-only sensitivity changing magnitude. This supports full-system optimization feasibility but cautions against overprecise population inference.",
  "artifacts": [
    {
      "path": "docs/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/zinc_thermochemistry_audit.json",
      "sha256": "6d5763ba79f428c087635c27aaa4b71890071c6fcc46296f072672cb5d00e3c1",
      "role": "partial_V1_evidence_not_final_acceptance"
    },
    {
      "path": "docs/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/vibrational_evidence.json",
      "sha256": "99fafa23967873f1fb8c1b78aa13040307adad72a5dee7692ac7ee0da17ecc91",
      "role": "partial_V1_evidence_not_final_acceptance"
    },
    {
      "path": "docs/upgrade_tasks_verification/group_1/papers/paper_9ec32e81e2826041/report/zinc_native_fragment_maps.json",
      "sha256": "f26b3cdc7616439f44bf34fd2d3989dce7ca4234caf8b7b00afe1b32420248a1",
      "role": "partial_V1_evidence_not_final_acceptance"
    },
    {
      "path": "docs/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_coplanar_corrected_SI_internal_SCF_restart_20260918/20260918T110817412108Z_hpc-job-2097366-cluster-slurmd-0/gaussian.log",
      "sha256": "b8eb48e3c1acfe26873c67d4c0ce7397d124fcfab3dae31c521a0f26040f94ec",
      "role": "native_D3_minimum_log"
    },
    {
      "path": "docs/verification/group_3/paper_9ec32e81e2826041/provenance/qzcli_hpc/ZcAAC_perpendicular_corrected_SI_internal_SCF_restart_20260918/20260918T110428423529Z_hpc-job-2097255-cluster-slurmd-0/gaussian.log",
      "sha256": "8c26b5d46ba1e846e010db7baf99f5883b41ead5b53d14726788a7e6f64404f1",
      "role": "native_D3_minimum_log"
    }
  ],
  "not_usable": "No final noD3 Hessian acceptance, complete cross-geometry decomposition, TD reciprocal correspondence/sensitivity or final scientific report exists at freeze.11 active jobs in the15:09UTC frozen inventory are not polled, resumed or counted successful here. No all-route/V2 acceptance."
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
  "V1 science status remains needs_work; there is no full reference binding or final accepted optical/stability matrix.",
  "Public graph supplies identity without source conformations; independent end-to-end AR construction/search feasibility has not been tested.",
  "The public optical data are approximate and lack digitized spectra/packing.",
  "Actual judge calibration, new-route reference completion and filesystem isolation remain pending; no new science jobs run."
]


Historical classification is retained; openness changes arise from the public inputs, flexible contract and claim-conditioned rules. This document is evaluator-only.
