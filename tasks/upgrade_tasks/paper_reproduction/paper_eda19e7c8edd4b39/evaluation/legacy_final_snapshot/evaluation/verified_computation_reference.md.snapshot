# Verified computation reference — paper_eda19e7c8edd4b39 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `completed` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `NOT_RECORDED` (NOT_ESTABLISHED)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

## Source identity

- Paper: Thermally driven surface phase separation in intermetallic alloys
- DOI: `10.1038/s41467-025-67397-x`
- Task package: `tasks/final_verified_paper_reproduction/paper_eda19e7c8edd4b39`
- Verification group: `docs/verification/group_5/paper_eda19e7c8edd4b39`
- Paper documents: `papers/paper_eda19e7c8edd4b39`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "difference_ni_minus_al": -0.09012176593749466,
    "lower_energy_species": "Ni",
    "statement": "Ni vacancy is lower under the explicit Ni-rich convention; 3x3x3 corroborates the ordering."
  },
  "conclusion": "Within the documented Ni-rich boundary, the real bulk-vacancy chain supports Ni<Al and the evaluator numeric range.",
  "energies": {
    "al_vacancy_formation_energy": 1.1884450059374592,
    "al_vacancy_total_energy": -667.83581488,
    "ni_vacancy_formation_energy": 1.0983232399999645,
    "ni_vacancy_total_energy": -667.63794354,
    "pristine_total_energy": -674.14703706,
    "unit": "eV"
  },
  "limitations": "The paper does not fully specify the chemical-potential boundary or input decks. Elemental Al diagnostic and the reservoir dependence are retained; not a unique all-boundaries author reproduction.",
  "method": {
    "charge_state": 0,
    "model": "PBE PAW spin-polarized fixed-cell neutral vacancy calculations",
    "provenance": "provenance/endpoint_reconciliation_20260914.json",
    "reservoir_convention": "Explicit Ni-rich beta-NiAl equilibrium: mu_Ni=fcc-Ni/4; mu_Al=beta-NiAl per formula minus mu_Ni. This is a disclosed calculation boundary, not asserted as an explicitly published author keyword.",
    "software_or_code": "VASP 6.3.2",
    "supercell": "4x4x4 B2 NiAl (128 pristine,127 vacancy atoms),3x3x3 sensitivity"
  },
  "qualification": "conditional_on_disclosed_reservoir_boundary",
  "reservoir_sensitivity": {
    "Al_vacancy_with_independent_fcc_Al_eV": 2.561213984999959,
    "Ni_rich_mu_Al": -5.1227771740625,
    "Ni_rich_mu_Ni": -5.41077028,
    "independent_fcc_Al_mu": -3.750008195
  },
  "status": "completed",
  "validation": {
    "convergence_or_sensitivity": "{\"ni_vacancy\": 1.0748487100000341, \"al_vacancy\": 1.2173003959375057, \"ni_minus_al\": -0.1424516859374716}; all eight raw OUTCARs rechecked for force convergence, SCF and normal timing.",
    "defect_identity_check": "Distinct pristine,Ni-vacancy,Al-vacancy and reservoir output identities preserved; charged defects not used.",
    "evidence": "artifacts/nial_vacancy_energy_ledger.json and provenance/endpoint_reconciliation_20260914.json"
  }
}
```

## Re-audit source-evidence drift

- Classification: **SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW**
- Previous `results.json` SHA-256: `51b1db1ae935e66a56f893fa2af5ab0dba2465fd285c7853b34c497ee59ead58`
- Current `results.json` SHA-256: `e1feb3f864cd056ff8e9b7098b4ff9f348ff753c1b75a94f9b50658451f91c38`
- Changed top-level result fields: `comparison, conclusion, energies, limitations, method, qualification, reservoir_sensitivity, status, validation`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["comparison", "conclusion", "energies", "limitations", "method", "qualification", "reservoir_sensitivity", "status", "validation"], "classification": "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW", "current_sha256": "e1feb3f864cd056ff8e9b7098b4ff9f348ff753c1b75a94f9b50658451f91c38", "detected": true, "previous_sha256": "51b1db1ae935e66a56f893fa2af5ab0dba2465fd285c7853b34c497ee59ead58"} -->

Paper/SI document hashes:

- `papers/paper_eda19e7c8edd4b39/documents/supplementary_001.pdf` — SHA-256 `49e63a4f958d08ccc03d3f3af9c2e8ce7fe4efc3f560cba342e92531b946b40e` (declared_match=True)
- `papers/paper_eda19e7c8edd4b39/documents/main.pdf` — SHA-256 `c9db7c7771ae5db69a41f10aa75967d88c1932e7146b1929d0f245a61e9da6bf` (declared_match=True)
- `papers/paper_eda19e7c8edd4b39/documents/supplementary_002.pdf` — SHA-256 `ebf28aa96aeb9e886c85775befcdb8952d54f89c8eaa8ee2776a0c8c93f5ee8b` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **75**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/status.json` — successful status record; SHA-256 `d1c284cd6b3d4cd59e490bb826419a5f90e093f42977bbf09152fdd1a96bef8f`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/collection.json` — successful execution artifact; SHA-256 `7f3203eeef17b54ec36b752d8cee1389ce25ec81246e862f949ad024e2e354b2`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/request.json` — successful execution artifact; SHA-256 `dd5dae0905d0dd0386a78a57955c7749a9413ed68ca00bf7f0e63e539539477b`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/stdout.log` — successful execution artifact; SHA-256 `1003a91687d0a61523303aeba9d5324dc4ddc9a6f5bf954f220588824b114b53`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/status.json` — successful status record; SHA-256 `cb77f7281719d5387400327df00abe5a459abccf5c20fbcf7d4a799aa10a6795`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/collection.json` — successful execution artifact; SHA-256 `de159d561f536b0ac28f2088d241c36561c72983c3034cb77ea28a1e0d429889`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/request.json` — successful execution artifact; SHA-256 `8e5e307707e6f6f006b2bd46112b7fb1267713fc61d4cf49983a444a7cd3c232`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/stdout.log` — successful execution artifact; SHA-256 `5b4357117a8273ca779d43531936352dcb4e9dbee0eada4dc70466d65b9ff0a4`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/status.json` — successful status record; SHA-256 `c7ec4cbd0b2cc8642d035f95d4bb45601030fdb177afdeeda7a9445c63fa6ea2`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/collection.json` — successful execution artifact; SHA-256 `7f73f7f03b615ba472a5bbb1fc139a6afe55e42bf4482edfaf7eb0f7a4f77072`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/request.json` — successful execution artifact; SHA-256 `0c25e6dab142b092730f293ce196271051887fd0514d7e5d9195bf5b0f21dc2f`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/stdout.log` — successful execution artifact; SHA-256 `eb5a876486523fec818cccefe2d60229918358cf271c7b7480d55b5030b4134e`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/status.json` — successful status record; SHA-256 `1f2cab64d10c7685aaba68c503861448356e12c86f83dd26b51aa96f8750da4d`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/collection.json` — successful execution artifact; SHA-256 `a9a2c46677212b70b21afcb0c35811811d7d8ec66b8e44ceb726cddecb7d08d6`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/request.json` — successful execution artifact; SHA-256 `2edf7835a034c2677654891153b841329b5b639d435df533f65e3e28378bc90d`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/stdout.log` — successful execution artifact; SHA-256 `c036403614e08308ebb38c91d18779d44a65c79ef72016dcfb1a536a959b1e43`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/status.json` — successful status record; SHA-256 `a805070346aba92a9ce5d6c0145c02596f8fd229c036893af98acff3cc04b8e6`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/collection.json` — successful execution artifact; SHA-256 `fae386c314de26f92e150eb0ac0780f781c66aa7cfc17860cb3461b0d13957fb`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/request.json` — successful execution artifact; SHA-256 `995e4fbc7856e1c89ddfb712ab04752d48fe0f96057e7987a61076d8eae61524`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/stdout.log` — successful execution artifact; SHA-256 `439b62e7e592ccd6d7fe7de5266367f8070e4207886897465b0f72d9e879eada`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/status.json` — successful status record; SHA-256 `9c405a6d3c45b4d08a6d4fe82162c008ac446d143a1cfc9c5dd81d4eac88dc7d`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/collection.json` — successful execution artifact; SHA-256 `ef10f6f82408bab38b73c148c641a2a4eb7e5eed30667201c1674bfb91479c81`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/request.json` — successful execution artifact; SHA-256 `9fd97acc30a8e6911cff6b3cacf9a4904957a5d4a6adf106c438b1e514691b87`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/stdout.log` — successful execution artifact; SHA-256 `61a62c050d6085851a51d292ceab7ee5a5ecd38107b308f2dd279de216a2a79b`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/status.json` — successful status record; SHA-256 `147749afe6a3d2c8ac3d61f1e06360b3caea8fbff0fe4852b239d22be201c863`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/resource_adjustment.json` — successful execution artifact; SHA-256 `ff398d244d86ef816f90ad8162c8c36f89913eb6cbad6136d846316144fa1c87`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/stdout.log` — successful execution artifact; SHA-256 `fbe53f79e6498a1e9c412bdabe38ed6909583d0a188fbbb1525b2afe5d8c2dd5`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/status.json` — successful status record; SHA-256 `7ae38a0744279c1701b76a1c5882f5df2ee4f0a929252ca784b69ca93393112c`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/resource_adjustment.json` — successful execution artifact; SHA-256 `59848d74f24223925cf6a862371f3977374515e69d28bffdab32dec4a8633ea0`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/stdout.log` — successful execution artifact; SHA-256 `a2d50ddd168d6bec728b0cdcfeb88645af0fdd707064c52cd28d954cf537a541`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/status.json` — successful status record; SHA-256 `8e31ef917e2fe04af7b8b6f618dbbd931399cc70b2e3787415f664873c31cecc`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/resource_adjustment.json` — successful execution artifact; SHA-256 `188c8393506368a646366b3e6bc056e27ffb2c1f1387bcde0620c8ee3b17851b`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/stdout.log` — successful execution artifact; SHA-256 `13022931c53c86fc528395ad890e45cb7bd521aa6474dc9acb1aff22377ad85f`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/status.json` — successful status record; SHA-256 `17223f000388f3674bbc6c5e39e9027a25e0cbe3706471cec17901e455b4b1f3`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/resource_adjustment.json` — successful execution artifact; SHA-256 `0fa43edac3623b921520157c20a38179871bbb457a93d1df49bdb8efffd25389`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/stdout.log` — successful execution artifact; SHA-256 `9d41ddaa61a735a8b1de673546a55df8fefbfd1f4bfe2b1fc15f3406f5f7127f`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/status.json` — successful status record; SHA-256 `bc9a55534a265c260bbf110cb3976f2df1d19b55de7eed64da1874daf33770ca`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/resource_adjustment.json` — successful execution artifact; SHA-256 `d9eaf8f028ef52c8986424a79851220bdf389b3d4d045f6a989f68c9d5a01097`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/stdout.log` — successful execution artifact; SHA-256 `bc7b04bc20f04db379672206504932117339a135e944c2747ffac7e90d20d305`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/status.json` — successful status record; SHA-256 `94339cedfc969bb147abe62648a6c5351d34b1fbfa0d7f8610d2083c3b277b93`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/resource_adjustment.json` — successful execution artifact; SHA-256 `e42e15f99fcaf5609bf01313c747dfffd44a3186fdd6dd8d40bd9795b30d3ea9`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/stdout.log` — successful execution artifact; SHA-256 `40f0d118fade20b9aa38a0d29f711db904fb44e6e606981ee9f6b4b730b235eb`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/status.json` — successful status record; SHA-256 `933dd1d7f688cd0bcead14b9bc7269ae9c30b1b20c6b3d1e6478a674ff812744`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/resource_adjustment.json` — successful execution artifact; SHA-256 `a9a586e1c3f67e1f1ae19808a04b7fb893d8ed2a437ec2fc29598914ccc1802b`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/stdout.log` — successful execution artifact; SHA-256 `46a796219f5b287e8c7c22d83c1557eb67ffa12f68a497cf9262be085b53dcf5`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/status.json` — successful status record; SHA-256 `7245851af53c946a528b991c7b0619d3aa4577ff8bda12145eb5b46f5d47a239`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/resource_adjustment.json` — successful execution artifact; SHA-256 `2fbd51e7d958a67f36939e47209cfdf0694915ae733379822d1d2f3601f9e3cb`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/stdout.log` — successful execution artifact; SHA-256 `3d0b2b7ea4929fddd6db3f546e3812f19b3fea3bd6a4fe3635389c64ab9cca08`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/status.json` — successful status record; SHA-256 `37004c59cc0ab634f55d8c964010700452aaf64b0d63857c3b580ec91303a0e1`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/resource_adjustment.json` — successful execution artifact; SHA-256 `311f445b0e08b67cbc4811189c77e476a74308ee6fa6ffe4c0a0c6608fea6c9d`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/stdout.log` — successful execution artifact; SHA-256 `df7ab7e7a94998b6eae8afe9084fc4c6623ad5c453f42c26058f15cba1264848`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/vasp_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/status.json` — label=group_5 paper_eda19e7c8edd4b39 beta_nial_bulk_relax; submitted_at=2026-09-01T03:13:16.713968+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_1a858c0c27c845f3984fb150227b1d1a/KPOINTS`
2. `native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/status.json` — label=group_5 paper_eda19e7c8edd4b39 nial_fcc_Ni_reservoir_relax; submitted_at=2026-09-01T11:15:48.582965+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_3025300378414f4bafaae41f69a48b3b/KPOINTS`
3. `native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/status.json` — label=group_5 paper_eda19e7c8edd4b39 nial_fcc_Al_reservoir_relax; submitted_at=2026-09-01T11:15:48.614762+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_213614b710cc428f891d5d28852a3394/KPOINTS`
4. `native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/status.json` — label=group_5 paper_eda19e7c8edd4b39 nial_4x4x4_ni_vacancy_relax_server2_resume; submitted_at=2026-09-01T14:25:24.788818+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_9d01d82d499a4ea7aeef92730f529735/KPOINTS`
5. `native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/status.json` — label=group_5 paper_eda19e7c8edd4b39 nial_4x4x4_pristine_relax_server2_resume; submitted_at=2026-09-01T14:25:25.426559+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_aad0cd5f74574ecc9a7a8eb6a850beb6/KPOINTS`
6. `native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/status.json` — label=group_5 paper_eda19e7c8edd4b39 nial_4x4x4_al_vacancy_relax_server2_resume; submitted_at=2026-09-01T14:25:26.115279+00:00; software=vasp; intent=ionic_relaxation; command=vasp_std
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/native_workspace/outputs/execution_jobs/job_4db9a620ddbb4b4fb194a93e525c6f47/KPOINTS`
7. `provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/status.json` — label=provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_localvalidated_20260909/1_20260909T181935653082512_267/KPOINTS`
8. `provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/status.json` — label=provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/KPOINTS`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/OSZICAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_al_vacancy_sensitivity_retry3/1_20260909T115501533777681_423/OUTCAR`
9. `provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/status.json` — label=provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_localvalidated_20260909/1_20260909T181924955363434_266/KPOINTS`
10. `provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/status.json` — label=provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/KPOINTS`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/OSZICAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_ni_vacancy_sensitivity_retry36/1_20260909T114425929184884_344/OUTCAR`
11. `provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/status.json` — label=provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260909T124250046153685_344/KPOINTS`
12. `provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/status.json` — label=provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_3x3x3_pristine_sensitivity_localvalidated_20260909/1_20260913T022640392804794_344/KPOINTS`
13. `provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/status.json` — label=provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_al_vacancy_relax_auto_retry9/1_20260905T192935054133649_111/KPOINTS`
14. `provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/status.json` — label=provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_ni_vacancy_relax_auto_retry3/1_20260905T175728614236234_111/KPOINTS`
15. `provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/status.json` — label=provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/status.json
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/CHG`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/CHGCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/CONTCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/DOSCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/EIGENVAL`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/IBZKPT`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/INCAR`
   - output: `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/qzcli_hpc/nial_4x4x4_pristine_relax/1/KPOINTS`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `pr_r_limit`, `pr_scope_limit`.

- Key-point IDs: `pr_process_setup, pr_process_validation, pr_result_ni, pr_result_al`
- Conclusion IDs: `pr_final_order, pr_scope_limit`
- Scoring-rule IDs: `pr_r_setup, pr_r_validation, pr_r_ni, pr_r_al, pr_r_order, pr_r_limit`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `NOT_RECORDED` (NOT_ESTABLISHED); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `pr_r_setup` → reference `pr_process_setup`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r_validation` → reference `pr_process_validation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r_ni` → reference `pr_result_ni`; type=numeric; unit=eV; tolerance=0.25; comparison=absolute difference; evaluator_target_present=True
- rule `pr_r_al` → reference `pr_result_al`; type=numeric; unit=eV; tolerance=0.25; comparison=absolute difference; evaluator_target_present=True
- rule `pr_r_order` → reference `pr_final_order`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r_limit` → reference `pr_scope_limit`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `pr_r_ni` / reference `pr_result_ni`: target=0.98 eV; tolerance=0.25; numeric result leaves=[1.0983232399999645]; within_tolerance=True; applicability=applicable
- rule `pr_r_al` / reference `pr_result_al`: target=1.2 eV; tolerance=0.25; numeric result leaves=[1.1884450059374592]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `pr_r_setup` / reference `pr_process_setup` / field `$.validation.defect_identity_check` / result path `$.validation.defect_identity_check` = `"Distinct pristine,Ni-vacancy,Al-vacancy and reservoir output identities preserved; charged defects not used."`
- rule `pr_r_validation` / reference `pr_process_validation` / field `$.validation.convergence_or_sensitivity` / result path `$.validation.convergence_or_sensitivity` = `"{\"ni_vacancy\": 1.0748487100000341, \"al_vacancy\": 1.2173003959375057, \"ni_minus_al\": -0.1424516859374716}; all eight raw OUTCARs rechecked for force convergence, SCF and normal timing."`
- rule `pr_r_validation` / reference `pr_process_validation` / field `$.validation.evidence` / result path `$.validation.evidence` = `"artifacts/nial_vacancy_energy_ledger.json and provenance/endpoint_reconciliation_20260914.json"`
- rule `pr_r_ni` / reference `pr_result_ni` / field `$.energies.ni_vacancy_formation_energy` / result path `$.energies.ni_vacancy_formation_energy` = `1.0983232399999645`
- rule `pr_r_al` / reference `pr_result_al` / field `$.energies.al_vacancy_formation_energy` / result path `$.energies.al_vacancy_formation_energy` = `1.1884450059374592`
- rule `pr_r_order` / reference `pr_final_order` / field `$.comparison.lower_energy_species` / result path `$.comparison.lower_energy_species` = `"Ni"`
- rule `pr_r_order` / reference `pr_final_order` / field `$.comparison.statement` / result path `$.comparison.statement` = `"Ni vacancy is lower under the explicit Ni-rich convention; 3x3x3 corroborates the ordering."`
- rule `pr_r_limit` / reference `pr_scope_limit` / field `$.limitations` / result path `$.limitations` = `"The paper does not fully specify the chemical-potential boundary or input decks. Elemental Al diagnostic and the reservoir dependence are retained; not a unique all-boundaries author reproduction."`
- rule `pr_r_limit` / reference `pr_scope_limit` / field `$.conclusion` / result path `$.conclusion` = `"Within the documented Ni-rich boundary, the real bulk-vacancy chain supports Ni<Al and the evaluator numeric range."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained B2 beta-NiAl POSCAR and system definition specifying sites, neutral defects and observables.

Public input files and hashes:

- `agent_input/data/inputs/beta_nial_b2_primitive.poscar` — SHA-256 `fa9155e2fbc232d911539aa2271a57ea4f5881676246f47d1f8b375a8695e5d7`; size=231 bytes; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/system_definition.json` — SHA-256 `60a38ac6b91a27b06d52154267bfb30e7150af9661dd20367d42ca75f82294c3`; size=580 bytes; explicit_boundary_fields={"$.charge_state": 0, "$.lattice_parameter_angstrom": 2.89, "$.spin_state": "Agent must state and justify"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_5/paper_eda19e7c8edd4b39/verification_report.md` — verification record; SHA-256 `d5ebbdd7d7655a3d5c0a59a675725ea5f7bbf8f18dcf4a7639c11cc4d585cbe1`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/report/results.json` — verification record; SHA-256 `e1feb3f864cd056ff8e9b7098b4ff9f348ff753c1b75a94f9b50658451f91c38`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/artifacts/nial_vacancy_energy_ledger.json` — referenced successful evidence; SHA-256 `b3b347faf773b75dd1edec8c0021de86160e6102a493b1f76d18a74f6a075179`
- `docs/verification/group_5/paper_eda19e7c8edd4b39/provenance/endpoint_reconciliation_20260914.json` — referenced successful evidence; SHA-256 `b843432655aa2266511673208f5a3ae6ed394824e7fb582ba1b0fe057dd53543`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
