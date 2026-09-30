# Verified computation reference — paper_6943bfe5eeaa42b8 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **HISTORICAL_RUNS_COMPLETE_BUT_WRONG_CONNECTIVITY**
- Group result status: `completed` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **NOT_VERIFIED_FOR_PAPER_OBJECT — NOT_RELEASE_READY**
- Applicability note (2026-09-18): Main-paper p. 2 Fig. 1(a) shows the six-membered imide ring of m-NH2 / N-butyl-3-amino-1,8-naphthalimide. The public identity now encodes this graph as `CCCCN1C(=O)c2cc(N)cc3cccc(C1=O)c23`. All three archived optimized XYZ files below, plus `provenance/retry_inputs/mnh2_td5_nto_retry.xyz`, instead recover `CCCCN1C(=O)c2ccc3c(N)cccc3c2C1=O`, a five-membered imide constitutional isomer. Equal formula C16H16N2O2 does not establish equal molecular identity.

The B3LYP geometry/frequency, B3LYP TD retry, and LC-BLYP TD/NTO calculations are real historical executions, but their D=2.194883674762385 Å and quoted `identity_verified: true` do **not** certify the paper object. No correct-object successful chain was found among these stored branches. Historical JSON, PASS wording and rule IDs below are quoted archival records, not current acceptance statements. Current scoring no longer has the independent `c_limitations`/`r_limits` claim; this removal does not resolve the identity gap. Per user confirmation, retain the paper object, mark this task not release ready, do not substitute the computed isomer, recalculate, or move its directory.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 3 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 report/results.json、artifacts/gaussian/ 和 provenance/。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Meta-amino substituted naphthalimides exhibit large charge transfer and strong N-H vibrations enabling use as ratiometric fluorescent probe
- DOI: `10.1016/j.cclet.2025.110971`
- Task package: `tasks/final_verified_paper_reproduction/paper_6943bfe5eeaa42b8`
- Verification group: `docs/verification/group_3/paper_6943bfe5eeaa42b8`
- Paper documents: `papers/paper_6943bfe5eeaa42b8`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "interpretation": {
    "conclusion": "S1 hole/electron centroid distance D=2.1949 Å is finite and positive, providing direct ICT descriptor evidence for the isolated m-NH2 dye; it does not establish an m-NH2 versus p-NH2 ordering without the matched p-NH2 calculation.",
    "scope": "Neutral isolated m-NH2 molecule in continuum water."
  },
  "result": {
    "d_index_angstrom": 2.194883674762385,
    "finite_positive": true,
    "uncertainty_or_sensitivity": "Dominant S1 NTO-pair centroid distance; rerun with cubegen fine/coarse grids for numerical sensitivity."
  },
  "status": "completed",
  "system": {
    "charge": 0,
    "compound_id": "m-NH2",
    "connectivity_smiles": "public m_nh2_identity.json SMILES",
    "formula": "C16H16N2O2",
    "multiplicity": 1
  },
  "validation": {
    "analysis_verified": true,
    "evidence": [
      "artifacts/gaussian/mnh2_b3lyp_corrected/stdout.log",
      "artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/stdout.log",
      "artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto.fchk",
      "artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_S1_hole.cube",
      "artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_S1_electron.cube"
    ],
    "geometry_converged": true,
    "identity_verified": true,
    "limitations": [
      "D-index uses dominant saved NTO pair and a finite cubegen grid; NTO truncation and grid sensitivity are reported model uncertainties."
    ],
    "state_verified": true
  },
  "workflow": {
    "excited_state": {
      "case": "mnh2_author_lc_blyp_w0232_td2_nto",
      "completed": true,
      "method": "optimally tuned LC-BLYP*/6-311+G(d,p), omega*=0.232 bohr^-1, TD=(Singlets,NStates=2,Root=1) in SMD water",
      "solvent_model": "SMD(Water)",
      "state_characterization": "Singlet-?Sym",
      "state_label": "S1 (lowest singlet root)",
      "strict_author_route": true
    },
    "geometry": {
      "conformer_selection": "single public-identity conformer",
      "converged": true,
      "frequency_check": "zero imaginary frequencies",
      "method": "B3LYP/6-311+G(d,p) EmpiricalDispersion=GD3BJ Opt/Freq"
    },
    "hole_electron_analysis": {
      "centroids_angstrom": {
        "electron": [
          0.3099970516378542,
          -0.19384953802713234,
          -0.318655174885083
        ],
        "hole": [
          2.4377711723990707,
          0.15765563534570953,
          0.08943274437912573
        ]
      },
      "completed": true,
      "integrated_weights": {
        "electron": 0.9999125647205619,
        "hole": 0.9999552565169679
      },
      "method": "Gaussian Density=(Transition=1) Pop=(NTO,SaveNTO,Full); cubegen MO density integration",
      "orbital_indices": {
        "electron_nto": 72,
        "hole_nto": 71
      },
      "same_excitation_as_state": true
    }
  }
}
```

Paper/SI document hashes:

- `papers/paper_6943bfe5eeaa42b8/documents/main.pdf` — SHA-256 `e8f4116848fed1cf3b6b0ed95eb1692337cb3a17cc68767936d88e6099c0cb59` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **30**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/status.json` — successful status record; SHA-256 `3dd3234d1c0238b5f4bda26c8b54f3e595f0f9342fca2845b67e051147ae9ca8`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/collection.json` — successful execution artifact; SHA-256 `945e65cf18440da7f1934e67dd842de25dc99642d589d61606e08cbe232b1dc4`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/formchk.log` — successful execution artifact; SHA-256 `ceed56e443ffa2f5876c53c41bac8dc7579469e7ddbb697318df4f1425a48732`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/input.com` — successful execution artifact; SHA-256 `43069b062d66182aa7a0748801f27f625be8c357a23367a59038edfb63e1fff5`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_optimized.xyz` — successful execution artifact; SHA-256 `ad2bf02d3cccbf612c78a486ecf3423677f42057b7dd714985b3170af9585708`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/status.json` — successful status record; SHA-256 `51de56b70b5fdc737808dfc0774c32752850e33162e2c06445e26acabe59c9b2`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/collection.json` — successful execution artifact; SHA-256 `e8e2e55dacf67e2ff9330315d695d076bdbae5ebab27af3658429db0683f247d`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/formchk.log` — successful execution artifact; SHA-256 `32c9bd6f9de7970720a1238954e810c19d7e54d53420ad0d9080783c66e5022f`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/input.com` — successful execution artifact; SHA-256 `8c90b0e814c25b3a212d0b06cea554ef2f5827212c9f76355463f55ec803adb0`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/mnh2_b3lyp_corrected_optimized.xyz` — successful execution artifact; SHA-256 `579d0ccf21fe6d26e464b78fff7986da8ecb5e435f7ccd1be66ca5b8c56dc286`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/status.json` — successful status record; SHA-256 `2a082a59bc9661f498eda1afeb09101e00c9dfec028a37882fbdb6f448987132`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/collection.json` — successful execution artifact; SHA-256 `fdcd85d57e0f7e5f7e5b3ba8e2ed309835bad0588dbbd1041ce947f9cbf28a8b`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/formchk.log` — successful execution artifact; SHA-256 `1ab7183f23253ca7e1a458aa70917a539ec85bd08e35a4d151b28490a6a35d47`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/input.com` — successful execution artifact; SHA-256 `5beba3a899cc3c5e2cc71deac01ee25c5e7d3f776836968bf65295c8640839ca`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/mnh2_td5_nto_retry_optimized.xyz` — successful execution artifact; SHA-256 `3c9dca47c66f75f80f3d47970cb68be1ba9b4e7ee954c4bfd965de6423496928`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_author_lc_blyp_w0232_td2_nto/outputs/execution_jobs/job_f99c1cff0f764f98a298e44433def5a9/status.json` — successful status record; SHA-256 `3dd3234d1c0238b5f4bda26c8b54f3e595f0f9342fca2845b67e051147ae9ca8`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_author_lc_blyp_w0232_td2_nto/outputs/execution_jobs/job_f99c1cff0f764f98a298e44433def5a9/collection.json` — successful execution artifact; SHA-256 `945e65cf18440da7f1934e67dd842de25dc99642d589d61606e08cbe232b1dc4`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_author_lc_blyp_w0232_td2_nto/outputs/execution_jobs/job_f99c1cff0f764f98a298e44433def5a9/input.com` — successful execution artifact; SHA-256 `43069b062d66182aa7a0748801f27f625be8c357a23367a59038edfb63e1fff5`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_author_lc_blyp_w0232_td2_nto/outputs/execution_jobs/job_f99c1cff0f764f98a298e44433def5a9/request.json` — successful execution artifact; SHA-256 `38366cbc0a02af9517f2ea81083e747b59852d3526e52f1037e87e9beb1b10dc`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_author_lc_blyp_w0232_td2_nto/outputs/execution_jobs/job_f99c1cff0f764f98a298e44433def5a9/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_b3lyp_corrected/outputs/execution_jobs/job_eb4bf5c2d272415aa659faa1c4aab60e/status.json` — successful status record; SHA-256 `51de56b70b5fdc737808dfc0774c32752850e33162e2c06445e26acabe59c9b2`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_b3lyp_corrected/outputs/execution_jobs/job_eb4bf5c2d272415aa659faa1c4aab60e/collection.json` — successful execution artifact; SHA-256 `e8e2e55dacf67e2ff9330315d695d076bdbae5ebab27af3658429db0683f247d`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_b3lyp_corrected/outputs/execution_jobs/job_eb4bf5c2d272415aa659faa1c4aab60e/input.com` — successful execution artifact; SHA-256 `8c90b0e814c25b3a212d0b06cea554ef2f5827212c9f76355463f55ec803adb0`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_b3lyp_corrected/outputs/execution_jobs/job_eb4bf5c2d272415aa659faa1c4aab60e/request.json` — successful execution artifact; SHA-256 `69936ee46df642b64a42f293d625264a7464d313f25f2dc0e585e2d04b74217a`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_b3lyp_corrected/outputs/execution_jobs/job_eb4bf5c2d272415aa659faa1c4aab60e/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_td5_nto_retry/outputs/execution_jobs/job_7d76651f054e4e8b9d6ddd4c8472b2f1/status.json` — successful status record; SHA-256 `2a082a59bc9661f498eda1afeb09101e00c9dfec028a37882fbdb6f448987132`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_td5_nto_retry/outputs/execution_jobs/job_7d76651f054e4e8b9d6ddd4c8472b2f1/collection.json` — successful execution artifact; SHA-256 `fdcd85d57e0f7e5f7e5b3ba8e2ed309835bad0588dbbd1041ce947f9cbf28a8b`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_td5_nto_retry/outputs/execution_jobs/job_7d76651f054e4e8b9d6ddd4c8472b2f1/input.com` — successful execution artifact; SHA-256 `5beba3a899cc3c5e2cc71deac01ee25c5e7d3f776836968bf65295c8640839ca`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_td5_nto_retry/outputs/execution_jobs/job_7d76651f054e4e8b9d6ddd4c8472b2f1/request.json` — successful execution artifact; SHA-256 `caa7191b10f2c8191d93f642893d3664fcf28905af4423d1eda21105071a893f`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/native_workspace/mnh2_td5_nto_retry/outputs/execution_jobs/job_7d76651f054e4e8b9d6ddd4c8472b2f1/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/mnh2_b3lyp_corrected/status.json` — label=group_3 paper_6943bfe5eeaa42b8 mnh2_b3lyp_corrected; submitted_at=2026-08-29T07:51:45.030813+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) EmpiricalDispersion=GD3BJ Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/collection.json`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/formchk.log`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/input.com`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/mnh2_b3lyp_corrected.chk`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/mnh2_b3lyp_corrected.fchk`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/mnh2_b3lyp_corrected_optimized.xyz`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/parsed_observables.json`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/stderr.log`
2. `artifacts/gaussian/mnh2_td5_nto_retry/status.json` — label=group_3 paper_6943bfe5eeaa42b8 mnh2_td5_nto_retry; submitted_at=2026-08-30T18:08:39.782538+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-311+G(d,p) TD=(Singlets,NStates=5,Root=1) Density=(Transition=1) Pop=(NTO,SaveNTO,Full) SCRF=(SMD,Solvent=Water) NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/collection.json`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/formchk.log`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/input.com`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/mnh2_td5_nto_retry.chk`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/mnh2_td5_nto_retry.fchk`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/mnh2_td5_nto_retry_S1_electron.cube`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/mnh2_td5_nto_retry_S1_hole.cube`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_td5_nto_retry/mnh2_td5_nto_retry_optimized.xyz`
3. `artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/status.json` — label=group_3 paper_6943bfe5eeaa42b8 mnh2_author_lc_blyp_w0232_td2_nto; submitted_at=2026-08-31T01:10:52.749558+00:00; software=gaussian; intent=single_point; route=#p LC-BLYP/6-311+G(d,p) TD=(Singlets,NStates=2,Root=1) Density=(Transition=1) Pop=(NTO,SaveNTO,Full) SCRF=(SMD,Solvent=Water) IOp(3/107=0232000000,3/108=0232000000) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/collection.json`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/formchk.log`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/input.com`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto.chk`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto.fchk`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_S1_electron.cube`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_S1_hole.cube`
   - output: `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_optimized.xyz`

## Evaluator alignment

- Key-point IDs: `kp_geometry, kp_state, kp_analysis, kp_result`
- Conclusion IDs: `c_final_ict, c_limitations`
- Scoring-rule IDs: `r_geometry, r_state, r_analysis, r_dindex, r_conclusion, r_limits`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_geometry` → reference `kp_geometry`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert verification; evaluator_target_present=False
- rule `r_state` → reference `kp_state`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert verification; evaluator_target_present=False
- rule `r_analysis` → reference `kp_analysis`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert verification; evaluator_target_present=False
- rule `r_dindex` → reference `kp_result`; type=numeric; unit=angstrom; tolerance=0.35; comparison=absolute difference for completed submissions; bounded-failure branch is accepted only with no fabricated result; evaluator_target_present=True
- rule `r_conclusion` → reference `c_final_ict`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_limits` → reference `c_limitations`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_dindex` / reference `kp_result`: target=2.25 angstrom; tolerance=0.35; numeric result leaves=[2.194883674762385]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_geometry` / reference `kp_geometry` / field `$.validation.geometry_converged` / result path `$.validation.geometry_converged` = `true`
- rule `r_geometry` / reference `kp_geometry` / field `$.workflow.geometry.converged` / result path `$.workflow.geometry.converged` = `true`
- rule `r_geometry` / reference `kp_geometry` / field `$.workflow.geometry.method` / result path `$.workflow.geometry.method` = `"B3LYP/6-311+G(d,p) EmpiricalDispersion=GD3BJ Opt/Freq"`
- rule `r_state` / reference `kp_state` / field `$.workflow.excited_state.state_label` / result path `$.workflow.excited_state.state_label` = `"S1 (lowest singlet root)"`
- rule `r_state` / reference `kp_state` / field `$.workflow.excited_state.state_characterization` / result path `$.workflow.excited_state.state_characterization` = `"Singlet-?Sym"`
- rule `r_state` / reference `kp_state` / field `$.workflow.excited_state.completed` / result path `$.workflow.excited_state.completed` = `true`
- rule `r_state` / reference `kp_state` / field `$.validation.state_verified` / result path `$.validation.state_verified` = `true`
- rule `r_analysis` / reference `kp_analysis` / field `$.workflow.hole_electron_analysis.same_excitation_as_state` / result path `$.workflow.hole_electron_analysis.same_excitation_as_state` = `true`
- rule `r_analysis` / reference `kp_analysis` / field `$.workflow.hole_electron_analysis.completed` / result path `$.workflow.hole_electron_analysis.completed` = `true`
- rule `r_analysis` / reference `kp_analysis` / field `$.validation.analysis_verified` / result path `$.validation.analysis_verified` = `true`
- rule `r_analysis` / reference `kp_analysis` / field `$.result.finite_positive` / result path `$.result.finite_positive` = `true`
- rule `r_dindex` / reference `kp_result` / field `$.result.d_index_angstrom` / result path `$.result.d_index_angstrom` = `2.194883674762385`
- rule `r_conclusion` / reference `c_final_ict` / field `$.interpretation.conclusion` / result path `$.interpretation.conclusion` = `"S1 hole/electron centroid distance D=2.1949 Å is finite and positive, providing direct ICT descriptor evidence for the isolated m-NH2 dye; it does not establish an m-NH2 versus p-NH2 ordering without the matched p-NH2 calculation."`
- rule `r_conclusion` / reference `c_final_ict` / field `$.interpretation.scope` / result path `$.interpretation.scope` = `"Neutral isolated m-NH2 molecule in continuum water."`
- rule `r_limits` / reference `c_limitations` / field `$.validation.limitations` / result path `$.validation.limitations[0]` = `"D-index uses dominant saved NTO pair and a finite cubegen grid; NTO truncation and grid sensitivity are reported model uncertainties."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Closed molecular identity and charge/multiplicity definition for neutral singlet m-NH2.

Public input files and hashes:

- `agent_input/data/inputs/m_nh2_identity.json` — SHA-256 `916f21bd749fb13f4deb1894238a160767379d00530b6b30229eff2bfc78188d`; size=568 bytes; explicit_boundary_fields={"$.charge": 0, "$.connectivity_smiles": "CCCCN1C(=O)c2cccc3c(N)cccc3c2C1=O", "$.formula": "C16H16N2O2", "$.multiplicity": 1}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_6943bfe5eeaa42b8/verification_report.md` — verification record; SHA-256 `22f2e68639cb7b9cf6f39cc513936e8bf416dd42a05a90a57b0a1fe1c6280b0b`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/report/results.json` — verification record; SHA-256 `72a15295a9c2ccf736f08ea6e1d4262bb261d470dc1979c2095e4a61e1115a8f`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto.fchk` — referenced successful evidence; SHA-256 `9b075ec5921ab2c193a5fe62629150e26ce5ab02571b1433b18a6096e430e074`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_S1_electron.cube` — referenced successful evidence; SHA-256 `587f2f8d1b50f3e7c55326fb33cc66d81358d3d37a4d631abe037d5e374d0a44`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/mnh2_author_lc_blyp_w0232_td2_nto_S1_hole.cube` — referenced successful evidence; SHA-256 `39f97d5bd25b6573c8bb0aedb094f5102d5e0f9779afcf471d7590262e5c6e5e`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_author_lc_blyp_w0232_td2_nto/stdout.log` — referenced successful evidence; SHA-256 `428bb9d1f6a9af98644ade201022832eb9290b661b65213a847c88c4f328b815`
- `docs/verification/group_3/paper_6943bfe5eeaa42b8/artifacts/gaussian/mnh2_b3lyp_corrected/stdout.log` — referenced successful evidence; SHA-256 `ec91fb3e54a8e60699bb62fc16332f589f43be62bbbf48ba8501509e75995f7f`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
