# Verified computation reference — paper_6492e1e5d38d23ae (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Current arithmetic reconciliation (2026-09-15)

Source definitions were rechecked in the [main PDF](../../../../papers/paper_6492e1e5d38d23ae/documents/main.pdf), PDF pp.5–6 Fig.5/discussion, and the existing publisher [SI DOCX](../../../../docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/source_additions_20260915/1-s2.0-S1001841725006084-mmc1.docx), TextS5. TextS5 specifies VASP/PBE, 400 eV, a 0.03 eV/Å force criterion and relaxed structures; it does not uniquely specify termination, slab layer count, vacuum width or k mesh. The public six-layer/18 Å construction is a benchmark convention, not an author-specified unique termination.

The historical JSON and field excerpts below are retained unchanged as source snapshots. Their `comparison.difference_eV = -0.8193502067943825` uses **anatase minus rutile**, whereas both final evaluators already define **rutile minus anatase**. The public task, submission-schema field description and ordering rule now explicitly use the latter convention. This is a sign/definition correction, not a new calculation or a change of termination, target or tolerance.

From the unchanged primary values, `W_anatase = 6.36999978845305 eV` and `W_rutile = 7.189349995247433 eV`:

- Current-convention difference: `W_rutile − W_anatase = +0.8193502067943825 eV`.
- The primary anatase value is below `6.871 − 0.5 = 6.371 eV` by `0.00100021154695 eV`. It does **not** pass the current numeric rule; rounding is not an exemption.
- The sign supports rutile > anatase. The magnitude is not the paper difference `7.009 − 6.871 = 0.138 eV` and must not be described as reproducing that magnitude.
- The separate anatase termination gives `7.173123045896127 eV`; it remains sensitivity evidence, not an answer-selected replacement for the primary branch.

Source: [group results](../../../../docs/verification/group_5/paper_6492e1e5d38d23ae/report/results.json) and the per-termination planar-potential files cited in the snapshot. The actual vacuum/Fermi subtractions and branch provenance below remain valid. `docs/verification` is unchanged. **D1 remains open:** specify the physical termination independently of its agreement with the answer, then assess that branch under the unchanged targets. Neither switching branch nor relaxing tolerance is authorized by this correction.

## Historical archive status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `NOT_RECORDED` (NOT_ESTABLISHED)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

## Source identity

- Paper: In-situ Z-scheme hetero-phase homojunction significantly enhances the carrier separation efficiency of TiO2 nanotube arrays: Key role of crystal phase engineering
- DOI: `10.1016/j.cclet.2025.111424`
- Task package: `tasks/final_verified_paper_reproduction/paper_6492e1e5d38d23ae`
- Verification group: `docs/verification/group_5/paper_6492e1e5d38d23ae`
- Paper documents: `papers/paper_6492e1e5d38d23ae`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "difference_eV": -0.8193502067943825,
    "interpretation_basis": "Both sampled anatase terminations have lower W than rutile; comparison is clean-facet only, not the full heterojunction mechanism.",
    "ordering": "anatase < rutile"
  },
  "conclusion": "The computed ordering supports anatase-to-rutile electron transfer in the stated facet model; unresolved numeric/termination boundaries remain explicit.",
  "qualification": "calculation_complete_not_automatic_strict_pass",
  "sensitivity_surfaces": [
    {
      "diagnostics": "Actual relaxation and static SCF completed; see raw hashes and distinct timings in provenance/endpoint_reconciliation_20260914.json.",
      "facet": "(101)",
      "fermi_energy_eV": -3.10675031,
      "force_converged": true,
      "name": "anatase TiO2(101)",
      "status": "success",
      "vacuum_plateau_evidence": "{\"left_mean_eV\": 4.0663733316113015, \"right_mean_eV\": 4.066372140180953, \"left_std_eV\": 3.1828128696103187e-05, \"right_std_eV\": 3.20351853965509e-05, \"mean_eV\": 4.0663727358961275, \"side_difference_eV\": 1.1914303481574962e-06}; docs/verification/group_5/paper_6492e1e5d38d23ae/artifacts/anatase_101_termination2_planar_potential_20260914.json",
      "work_function_eV": 7.173123045896127
    }
  ],
  "status": "complete",
  "surfaces": {
    "anatase_101": {
      "diagnostics": "Actual relaxation and static SCF completed; see raw hashes and distinct timings in provenance/endpoint_reconciliation_20260914.json.",
      "facet": "(101)",
      "fermi_energy_eV": -2.59805644,
      "force_converged": true,
      "name": "anatase TiO2(101)",
      "status": "success",
      "vacuum_plateau_evidence": "{\"left_mean_eV\": 3.771948878628736, \"right_mean_eV\": 3.7719378182773635, \"left_std_eV\": 0.00012444133635951967, \"right_std_eV\": 0.00012623155618611185, \"mean_eV\": 3.77194334845305, \"side_difference_eV\": 1.1060351372549349e-05}; docs/verification/group_5/paper_6492e1e5d38d23ae/artifacts/anatase_101_termination1_planar_potential_20260914.json",
      "work_function_eV": 6.36999978845305
    },
    "rutile_110": {
      "diagnostics": "Actual relaxation and static SCF completed; see raw hashes and distinct timings in provenance/endpoint_reconciliation_20260914.json.",
      "facet": "(110)",
      "fermi_energy_eV": -2.53184201,
      "force_converged": true,
      "name": "rutile TiO2(110)",
      "status": "success",
      "vacuum_plateau_evidence": "{\"left_mean_eV\": 4.657513695317764, \"right_mean_eV\": 4.657502503579915, \"left_std_eV\": 9.612494150989911e-05, \"right_std_eV\": 0.00010457170508679258, \"mean_eV\": 4.657507985247433, \"side_difference_eV\": 1.1191737849358674e-05}; docs/verification/group_5/paper_6492e1e5d38d23ae/artifacts/rutile_110_termination1_planar_potential_20260914.json",
      "work_function_eV": 7.189349995247433
    }
  },
  "validation": {
    "limitations": "Author-exact termination/geometry are not fully disclosed. Database identity repair retained. Numeric evaluator agreement is assessed separately; a converged calculation is not automatically a numeric PASS.",
    "method": "VASP PBE, ENCUT400 eV, relax force0.03 eV/A; electrostatic LOCPOT minus vasprun.xml E_F.",
    "sensitivity": "Anatase terminations: 6.369999788, 7.173123046 eV; spread 0.803123257 eV. Primary remains termination1; no reference-driven switching."
  }
}
```

## Re-audit source-evidence drift

- Classification: **SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW**
- Previous `results.json` SHA-256: `fdf1f27726331127c4b7cdb88c755dd2382786a2c446eaf20e38cb124eb35a90`
- Current `results.json` SHA-256: `cad0cffc6a47f3ae01d915552ea7d85b08dddcedb23cd48e7b53d88705df907a`
- Changed top-level result fields: `comparison, conclusion, qualification, sensitivity_surfaces, status, surfaces, validation`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["comparison", "conclusion", "qualification", "sensitivity_surfaces", "status", "surfaces", "validation"], "classification": "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW", "current_sha256": "cad0cffc6a47f3ae01d915552ea7d85b08dddcedb23cd48e7b53d88705df907a", "detected": true, "previous_sha256": "fdf1f27726331127c4b7cdb88c755dd2382786a2c446eaf20e38cb124eb35a90"} -->

Paper/SI document hashes:

- `papers/paper_6492e1e5d38d23ae/documents/main.pdf` — SHA-256 `26f27b5142e65b158884965c416b8ee46c9827e4fa54ed73aa52c60c7e2cbeaf` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **45**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/status.json` — successful status record; SHA-256 `52cbdd180dc084120f739bdc3550e04b1f2b609249df3e989156c416fe135943`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/collection.json` — successful execution artifact; SHA-256 `556481f45e15f297bed58b9d78692c1e49d631d2b7ca408a00efb932990d3690`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/request.json` — successful execution artifact; SHA-256 `83234b4987505c46bc700d92b766cf8516755c7d025ea8a908a76643d88b71f4`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/stdout.log` — successful execution artifact; SHA-256 `ae9884462a6c004c78aa22a9fe9bf8b774ee710bdc7f86ddc9d368d04f2040b2`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/status.json` — successful status record; SHA-256 `9fd6a14455bfc518781d6896c8132662445e3ac2d6bae841e736e7c67286614c`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/collection.json` — successful execution artifact; SHA-256 `a11e915a546ebe85cc62d0f1656560d71a72b83d81943c262d6f99e375b302bf`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/request.json` — successful execution artifact; SHA-256 `93ee447b806a568e18904c389b2de4019f005e9a753f092c97286e33e869f484`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/stdout.log` — successful execution artifact; SHA-256 `5ee8030b48857888e6a9cd1cacfe3256c84871cc87454f40d3894865a7a47c33`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/status.json` — successful status record; SHA-256 `7a765d971d7c9dd798f87b4b4150c93123cebf1d7f3eefd01b2050212f5c6804`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/collection.json` — successful execution artifact; SHA-256 `babd6e337a559756392e0cc6f60e6deb319ebb91083ffceb8f4e540efa12458f`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/request.json` — successful execution artifact; SHA-256 `8d0ba7f6fc3408c8040df7b09447d983e2c108cd8f72dd452bad778da372f29e`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/stdout.log` — successful execution artifact; SHA-256 `1883ca167ad1331be10f45a5f5f954f44263375fcab46b8a9f94b4e1404e26bb`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/status.json` — successful status record; SHA-256 `c5f7fe0e051a65055f9de36eef91f8f55dcadd12f10366345e02932567071266`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/resource_adjustment.json` — successful execution artifact; SHA-256 `3ad66ade58f9fcf6d11febe1b2469234c857ea333bc3a7adb0171558fd1f4e2b`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/stdout.log` — successful execution artifact; SHA-256 `b684175778af8276457f72a550de9043f54f1f7416400ca84cee95398f190abc`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/status.json` — successful status record; SHA-256 `e08e7dec9943a6e657707d0d7e26924e2e72d78c933f73229abc920195eb201b`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/resource_adjustment.json` — successful execution artifact; SHA-256 `00bb3225d2d15dcdffd1ad783f817d5b4c0d97fa2a904324f7b9ba8d2aefe747`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/stdout.log` — successful execution artifact; SHA-256 `fd6d7fd8dcc824da1d6f566c84dc8f99cceec1a599615dc5d1b3d62f3fc84304`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/status.json` — successful status record; SHA-256 `749d3a944f9dcfd9a69614cb1dec0658609ff76bfdac9d675cd7ee8d211db306`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/resource_adjustment.json` — successful execution artifact; SHA-256 `b635dad7dcf30f9c7f5ceabb76bb2b2e26e34637ad63dd38717aeb227ad66446`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/stdout.log` — successful execution artifact; SHA-256 `d8c27b72574c07fe4363097205e39b67e3e66dadffd4cf1bc3894e64612cdd80`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/status.json` — successful status record; SHA-256 `390411fbe0045cc601f263aeee7f5b6a58cbea5edc826f0d430cd3395cd1bb99`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/resource_adjustment.json` — successful execution artifact; SHA-256 `0b0a7d81e239a467fa273515e170ad73926aa4d2ae56b01cf6aebe3dbd1be8dc`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/stdout.log` — successful execution artifact; SHA-256 `0d6dd7103562bfc2156c5c71f7e049c7219fa67a9e4318217bdf530929c289a3`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/status.json` — successful status record; SHA-256 `e373bb74999173699724257bf28c1d9ae6b2e98d64ca5bb7332c6646212890d6`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/resource_adjustment.json` — successful execution artifact; SHA-256 `4a219dd714f32a4aa49f9e78e19328c37d0744a1c68886113820de3c63eb462b`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/stdout.log` — successful execution artifact; SHA-256 `da6232678291814e6240b1cdd51557bd4f63ae68c14ac83b878c6204a345ba04`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/status.json` — successful status record; SHA-256 `e47f44e26b6f055686ca325a7874c6bee18182ab21bbeb400297b64b41b96324`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/resource_adjustment.json` — successful execution artifact; SHA-256 `061fd1bbd4d1b077d93b888d3f6b5abebbe363965b57178053e881bf954a6c94`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/stdout.log` — successful execution artifact; SHA-256 `a601a734ad6fee8c096bfc3b5d1e0c0256b372cb5123bfdbe42f2ec9225befa9`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/status.json` — label=group_5 paper_6492e1e5d38d23ae anatase_bulk_relax; submitted_at=2026-09-01T03:13:16.457235+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_eb914a87eabd4dc98a3d1ef329f7e085/KPOINTS`
2. `native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/status.json` — label=group_5 paper_6492e1e5d38d23ae rutile_bulk_relax; submitted_at=2026-09-01T03:13:16.499132+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_7fd35dad7e244d82b0fcb06d2b2b3f02/KPOINTS`
3. `native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/status.json` — label=group_5 paper_6492e1e5d38d23ae rutile_110_termination1_relax_server2_resume; submitted_at=2026-09-01T14:29:25.850799+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/native_workspace/outputs/execution_jobs/job_2d6498dfcedc4205bcc3736172039e50/KPOINTS`
4. `provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/status.json` — label=provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/status.json
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_relax_hpc_migration/1_20260905T080146617621026_265/KPOINTS`
5. `provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/status.json` — label=provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/status.json
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination1_workfunction_static_auto_retry3/1_20260908T042657587713601_266/KPOINTS`
6. `provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/status.json` — label=provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/status.json
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_relax_hpc_migration/1_20260905T081150642181047_265/KPOINTS`
7. `provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/status.json` — label=provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/status.json
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/anatase_101_termination2_workfunction_static_auto_retry3/1_20260908T042656866159660_344/KPOINTS`
8. `provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/status.json` — label=provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/status.json
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/KPOINTS`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/OSZICAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_relax_hpc_migration/1_20260905T090234094126129_188/OUTCAR`
9. `provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/status.json` — label=provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/status.json
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/CHG`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/CHGCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/CONTCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/DOSCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/EIGENVAL`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/IBZKPT`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/INCAR`
   - output: `docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/qzcli_hpc/rutile_110_termination1_workfunction_static_auto_retry3/1_20260908T042659016238083_344/KPOINTS`

## Evaluator alignment

- Key-point IDs: `pr_process_relax, pr_process_plateau, pr_anatase_wf, pr_rutile_wf, pr_ordering`
- Conclusion IDs: `pr_final_charge_transfer`
- Scoring-rule IDs: `pr_r1, pr_r2, pr_r3, pr_r4, pr_r5, pr_r6`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `NOT_RECORDED` (NOT_ESTABLISHED); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `pr_r1` → reference `pr_process_relax`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process comparison; evaluator_target_present=False
- rule `pr_r2` → reference `pr_process_plateau`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process comparison; evaluator_target_present=False
- rule `pr_r3` → reference `pr_anatase_wf`; type=numeric; unit=eV; tolerance=0.5; comparison=absolute difference for anatase-named record; evaluator_target_present=True
- rule `pr_r4` → reference `pr_rutile_wf`; type=numeric; unit=eV; tolerance=0.5; comparison=absolute difference for rutile-named record; evaluator_target_present=True
- rule `pr_r5` → reference `pr_ordering`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert ordering comparison; evaluator_target_present=False
- rule `pr_r6` → reference `pr_final_charge_transfer`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `pr_r3` / reference `pr_anatase_wf`: target=6.871 eV; tolerance=0.5; numeric result leaves=[6.36999978845305]; within_tolerance=False; applicability=applicable
- rule `pr_r4` / reference `pr_rutile_wf`: target=7.009 eV; tolerance=0.5; numeric result leaves=[7.189349995247433]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `pr_r1` / reference `pr_process_relax` / field `$.surfaces.anatase_101.force_converged` / result path `$.surfaces.anatase_101.force_converged` = `true`
- rule `pr_r1` / reference `pr_process_relax` / field `$.surfaces.rutile_110.force_converged` / result path `$.surfaces.rutile_110.force_converged` = `true`
- rule `pr_r1` / reference `pr_process_relax` / field `$.surfaces.anatase_101.facet` / result path `$.surfaces.anatase_101.facet` = `"(101)"`
- rule `pr_r1` / reference `pr_process_relax` / field `$.surfaces.rutile_110.facet` / result path `$.surfaces.rutile_110.facet` = `"(110)"`
- rule `pr_r2` / reference `pr_process_plateau` / field `$.surfaces.anatase_101.vacuum_plateau_evidence` / result path `$.surfaces.anatase_101.vacuum_plateau_evidence` = `"{\"left_mean_eV\": 3.771948878628736, \"right_mean_eV\": 3.7719378182773635, \"left_std_eV\": 0.00012444133635951967, \"right_std_eV\": 0.00012623155618611185, \"mean_eV\": 3.77194334845305, \"side_difference_eV\": 1.1060351372549349e-05}; docs/veri..."`
- rule `pr_r2` / reference `pr_process_plateau` / field `$.surfaces.rutile_110.vacuum_plateau_evidence` / result path `$.surfaces.rutile_110.vacuum_plateau_evidence` = `"{\"left_mean_eV\": 4.657513695317764, \"right_mean_eV\": 4.657502503579915, \"left_std_eV\": 9.612494150989911e-05, \"right_std_eV\": 0.00010457170508679258, \"mean_eV\": 4.657507985247433, \"side_difference_eV\": 1.1191737849358674e-05}; docs/verif..."`
- rule `pr_r2` / reference `pr_process_plateau` / field `$.validation.sensitivity` / result path `$.validation.sensitivity` = `"Anatase terminations: 6.369999788, 7.173123046 eV; spread 0.803123257 eV. Primary remains termination1; no reference-driven switching."`
- rule `pr_r3` / reference `pr_anatase_wf` / field `$.surfaces.anatase_101.work_function_eV` / result path `$.surfaces.anatase_101.work_function_eV` = `6.36999978845305`
- rule `pr_r4` / reference `pr_rutile_wf` / field `$.surfaces.rutile_110.work_function_eV` / result path `$.surfaces.rutile_110.work_function_eV` = `7.189349995247433`
- rule `pr_r5` / reference `pr_ordering` / field `$.comparison.ordering` / result path `$.comparison.ordering` = `"anatase < rutile"`
- rule `pr_r5` / reference `pr_ordering` / field `$.comparison.difference_eV` / result path `$.comparison.difference_eV` = `-0.8193502067943825`
- rule `pr_r6` / reference `pr_final_charge_transfer` / field `$.conclusion` / result path `$.conclusion` = `"The computed ordering supports anatase-to-rutile electron transfer in the stated facet model; unresolved numeric/termination boundaries remain explicit."`
- rule `pr_r6` / reference `pr_final_charge_transfer` / field `$.comparison.interpretation_basis` / result path `$.comparison.interpretation_basis` = `"Both sampled anatase terminations have lower W than rutile; comparison is clean-facet only, not the full heterojunction mechanism."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: POSCAR identity changed
- Files changed in that review: `agent_input/data/inputs/anatase_bulk.POSCAR, agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained anatase and rutile POSCAR bulk cells plus deterministic facet/slab protocol.

Public input files and hashes:

- `agent_input/data/inputs/anatase_bulk.POSCAR` — SHA-256 `cde0243b8a3c559a984851c7cd02234a1c4501e04929b5539d33ece39fbcf0df`; size=948 bytes; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/rutile_bulk.POSCAR` — SHA-256 `c4562b5444ee99f08f8b87eabaf1edb9e53a413fd3e140102d7456c8f17378f9`; size=292 bytes; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/slab_protocol.json` — SHA-256 `d2c62d6a4e66d072460542972901ca2dce19d963da940286dd5054edaa2ac77a`; size=807 bytes; explicit_boundary_fields={"$.charge": 0, "$.multiplicity": 1}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_5/paper_6492e1e5d38d23ae/verification_report.md` — verification record; SHA-256 `19a9bdc7646da0c33eadf4e16baee36c0826799ef72c3c3dfd29258948d1286c`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/report/results.json` — verification record; SHA-256 `cad0cffc6a47f3ae01d915552ea7d85b08dddcedb23cd48e7b53d88705df907a`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/artifacts/anatase_101_termination1_planar_potential_20260914.json` — referenced successful evidence; SHA-256 `764cc9be8ebb7fc5618a527b8f8d39c2f609d18734980709245e4ed692a20ed5`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/artifacts/anatase_101_termination2_planar_potential_20260914.json` — referenced successful evidence; SHA-256 `284c91326a355891f98726b2d48c1f33f4335dca46edb6d5c4adf37d312efabd`
- `docs/verification/group_5/paper_6492e1e5d38d23ae/artifacts/rutile_110_termination1_planar_potential_20260914.json` — referenced successful evidence; SHA-256 `1e3f1094e55e785fc9e9522b5cd9bd3fbff69c37fb75146d63a1fa47cf8c1e0a`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
