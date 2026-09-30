# Verified computation reference — paper_430b9cbe83c2c203 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Public-input maintenance note (2026-09-14)

The author-endpoint XYZ files were replaced by independently embedded topology-only starters. The successful calculation archive still documents the historical author route; no calculation from those new starters was performed, and the original endpoints remain evaluator-private.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **AUTHOR_ROUTE_ONLY_PUBLIC_STARTER_NOT_REPLAYED**
- Applicability note: Public cis/trans geometries were replaced by independently embedded topology-only starters; the group archive used the original author endpoints. Under the accepted author-route verification policy this starter difference is not itself a task/evaluator mismatch; no independent discovery or public-starter replay is claimed.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 7 | `QUALIFIED` | - evaluation 资格：`QUALIFIED`。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Direct Access to Fluorinated Organoselenium Compounds from Pentafluorobenzenes via One-Pot Na2Se-Based Synthesis: An Approach to Selenides and Diselenides
- DOI: `10.1021/acs.joc.5c02781`
- Task package: `tasks/final_verified_autonomous_research/paper_430b9cbe83c2c203`
- Verification group: `docs/verification/group_4/paper_430b9cbe83c2c203`
- Paper documents: `papers/paper_430b9cbe83c2c203`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "assignment": "The repaired exact-route B97-2/pcSseg-2 referenced shifts are compared site-by-site with the weak approximately 422 and 816 ppm features. This is semiquantitative corroboration only; it does not prove a unique exchange rate, population model, or mechanism.",
    "evidence": "{\"cis_shifts_ppm\": [460.1713, 930.0386000000001, 413.39920000000006], \"geometry_job_ids\": {\"cis\": \"hpc-job-1f81cb41-991f-4d4d-99fa-62532c8873e4\", \"trans\": \"hpc-job-6c3cf81e-e812-4e27-aa86-c0d4e77f8a5b\"}, \"nearest_deviation_to_422_ppm\": 8.600799999999936, \"nearest_deviation_to_816_ppm\": 109.33820000000003, \"nmr_job_ids\": {\"cis\": \"hpc-job-2f9ecefe-5d18-4520-a042-9afccc3cd70a\", \"trans\": \"hpc-job-11b69c79-eeae-4784-87f8-5e5a79e92438\"}, \"reference_job_id\": \"job_915855f7e15a43c480c873296724b8ea\", \"reference_stdout_sha256\": \"a6a0e479c55ad5a5d8dc31d205d49cdb151c14938fa44f4cc181f7e372e0fd36\", \"sigma_reference_ppm\": 1736.1401, \"signal_gate\": \"semiquantitative (<=50 ppm for 422 and <=120 ppm for 816); evaluator has no numeric tolerance\", \"trans_shifts_ppm\": [434.0228000000002, 925.3382, 433.98710000000005]}",
    "observed_features_ppm": [
      422,
      816
    ]
  },
  "conclusion": "The supplied cis and trans triselenide structures were tested with the SI geometry route and repaired exact B97-2/pcSseg-2 GIAO/reference route. Their calculated shifts and common-level energy are reported directly; the semiquantitative assignment is supported under the explicit deviation gate. The result remains corroborative and does not establish a unique exchange mechanism.",
  "conformers": [
    {
      "diagnostics": "Gaussian 16 PW6B95/def2-QZVP Opt/Freq normal termination; 69 frequencies; NImag=0; geometry_job_id=hpc-job-1f81cb41-991f-4d4d-99fa-62532c8873e4; geometry_output_sha256=76de01d8d294383537cf1c1ab559dae5b6cf41abdb2429dfffabf0562e9ebbcb",
      "name": "cis",
      "se_sites": [
        "Se atom 1 (input atom index 1)",
        "Se atom 2 (input atom index 2)",
        "Se atom 3 (input atom index 3)"
      ],
      "shifts_ppm": [
        460.1713,
        930.0386000000001,
        413.39920000000006
      ],
      "stationary": true
    },
    {
      "diagnostics": "Gaussian 16 PW6B95/def2-QZVP Opt/Freq normal termination; 69 frequencies; NImag=0; geometry_job_id=hpc-job-6c3cf81e-e812-4e27-aa86-c0d4e77f8a5b; geometry_output_sha256=326706bd6f78659f0534ba29a67d019e542fb381254c9ec49a0490848b11ba09",
      "name": "trans",
      "se_sites": [
        "Se atom 1 (input atom index 1)",
        "Se atom 2 (input atom index 2)",
        "Se atom 3 (input atom index 3)"
      ],
      "shifts_ppm": [
        434.0228000000002,
        925.3382,
        433.98710000000005
      ],
      "stationary": true
    }
  ],
  "limitations": "Two supplied conformers, isolated-molecule/vacuum model, no explicit CDCl3, no conformer ensemble, no population-weighted spectrum, and no exchange-rate calculation; ppm gate is an audit convention because the evaluator gives no numeric tolerance.",
  "methods": {
    "geometry": "Gaussian 16 C.01 PW6B95/def2-QZVP Opt=(Tight,MaxCycles=300) Freq, neutral singlet, vacuum; SI Tables S6/S7 geometries",
    "nmr": "Gaussian 16 C.01 B97-2/pcSseg-2 Gen NMR=GIAO, neutral singlet, vacuum, on PW6B95/def2-QZVP frequency-validated geometries; element blocks repaired only for absent elements",
    "reference": "delta = sigma(Me2Se) - sigma(triselenide); same B97-2/pcSseg-2 GIAO reference, sigma(Me2Se)=1736.140100 ppm"
  },
  "relative_energy": {
    "uncertainty": "single supplied conformer pair and one geometry level; source near-degeneracy criterion is 1 kcal/mol",
    "value_kcal_mol": 0.7567764262349671,
    "zero": "trans optimized conformer G=0 at 298 K; cis minus trans from the same PW6B95/def2-QZVP thermal Gibbs route"
  },
  "status": "complete"
}
```

Paper/SI document hashes:

- `papers/paper_430b9cbe83c2c203/documents/supplementary_001.pdf` — SHA-256 `4511da25c9be20692fbefb139dad54e0cdd347847abe4d9220e6d670cd714acc` (declared_match=True)
- `papers/paper_430b9cbe83c2c203/documents/main.pdf` — SHA-256 `07663d48c22a5bacf5f61642d2d29ef7089cbd72bb4b699f999d9f48cb9c8cb0` (declared_match=True)

Report evidence lines retained:

- 3. Me₂Se：同级 B97-2/Gen `Opt/Freq NMR=GIAO` basisfix1，job `job_915855f7e15a43c480c873296724b8ea`，解析 1 个 Se shielding `1736.140100` ppm。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **70**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/status.json` — successful status record; SHA-256 `b5cafae607c95e42257ea9ba3f0a14252f86f4f0f432316c3a391ae1c2b9f88f`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/cis_se_nmr_parsed.json` — successful execution artifact; SHA-256 `002f9484156c84e02e2ddce5b46a48daa8de2de39f920bb0d9d83caf037077d7`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/collection.json` — successful execution artifact; SHA-256 `3652c2f3736aa9737da713d24da1332f865f6768a8eca584d439d41254d48b75`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/input.com` — successful execution artifact; SHA-256 `ed2fc92c2be0ac46ce0e6882cdbcc0e12d3158705b018f3c24dadf1a547728c6`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/status.json` — successful status record; SHA-256 `6eb5ad304086b508e759705e21fcfc1e0e6f2e45e6f5c3579b7bd1676465b7f9`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/collection.json` — successful execution artifact; SHA-256 `574123b11ca686982a0ed1837f22e89304309a7407cafbee41fdd8c0e37c90e6`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/dimethyl_selenide_b972_nmr_reference_parsed.json` — successful execution artifact; SHA-256 `885a61e90bb83d72f35908bb08f2e2aa8fcafa03aaad0eb6b17e9ddd83d3f755`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/input.com` — successful execution artifact; SHA-256 `35ac16ad732fdf97a8f89a3f38c0a24f6f6a84fac11fef9897485f002c7990a6`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/status.json` — successful status record; SHA-256 `7f6b73a3975eb5a3ec8f66477118c011c25f159aa0f5e4b79924400f146e7971`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/collection.json` — successful execution artifact; SHA-256 `459c7ce91dd46884b9bbdb3f85047203a00b018e3fa95b48fb60a330ea8ca01e`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/input.com` — successful execution artifact; SHA-256 `5a16b4e948752014567bd3cff1f495a88c2f8eb0f0e2fa7b759f261d12ca0e60`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/stdout.log` — successful execution artifact; SHA-256 `a6a0e479c55ad5a5d8dc31d205d49cdb151c14938fa44f4cc181f7e372e0fd36`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/status.json` — successful status record; SHA-256 `834c7fc2758bf50c5ea9dfc32edcb11fd0e773e4c3427cc287cf63751068dd37`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/collection.json` — successful execution artifact; SHA-256 `e0875a4729b047c5bc09606c59b280da4c6168e184567a52ddeb73ce41973958`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/diselenide_cis_optfreq_parsed.json` — successful execution artifact; SHA-256 `d234c60c486d61e9299a1c2087f0e7338eaa63638b627ffb1bf6cade784c5c8e`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/input.com` — successful execution artifact; SHA-256 `252a64a3987024f3277054849ad93b578bff6de4493ec7c64db100e1b5f4169a`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/status.json` — successful status record; SHA-256 `667a195396c97ad79fc73363b9bd27d5b4c12e81eb484de1df9d71ffb91107d0`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/collection.json` — successful execution artifact; SHA-256 `58b549f83bd1d6c178ed7a3daa3fbd42f011e4d55b9830d1bdc796c030f9c0bf`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/diselenide_trans_optfreq_parsed.json` — successful execution artifact; SHA-256 `e7eb7fc75506033a757e5cb8d843aef6b38040fe550eb48f04f788a33d30c3f3`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/input.com` — successful execution artifact; SHA-256 `88b93f458d333c2b6eba913a94f1910b19c62567919e207235f376eb4e3afa0c`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/status.json` — successful status record; SHA-256 `8a9c72f61b03492e6918825e1dd38f6608951a285184bfc9589ec62ae6619733`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/collection.json` — successful execution artifact; SHA-256 `bbfb21b91561e507c9d1b37c49b61938413a62118b3706c589ca897bd6a677c5`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/input.com` — successful execution artifact; SHA-256 `34dd8a52ac3592a27d16fa8c17b002fcbc0d9976fbd3b16eecf656ea06d8868a`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/parsed.json` — successful execution artifact; SHA-256 `a821f92f5fe97966b22c7653492ef211c99964c6d2632e430631f575b3840c22`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/status.json` — successful status record; SHA-256 `2b8c48affed90e7367a95cf69b3f2746f399df4acb8345ba6f3da0d574df7ed1`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/collection.json` — successful execution artifact; SHA-256 `be7a25af529c8d49581c7bb1b1b5c76df788d21dd8896c83fd42a2b8a86b54e9`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/input.com` — successful execution artifact; SHA-256 `9d62d99e00dde367d0b1be830f19010f39d5bee9f22bdd5c69cc4f046564606a`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/stdout.log` — successful execution artifact; SHA-256 `45d26a70d1bc32fec0d04a3e2918a472832d4decf7f012cb87eecf94748a4e77`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_09ad39f20819423c824319e47d4f12f7/status.json` — successful status record; SHA-256 `6eb5ad304086b508e759705e21fcfc1e0e6f2e45e6f5c3579b7bd1676465b7f9`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_09ad39f20819423c824319e47d4f12f7/collection.json` — successful execution artifact; SHA-256 `574123b11ca686982a0ed1837f22e89304309a7407cafbee41fdd8c0e37c90e6`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_09ad39f20819423c824319e47d4f12f7/input.com` — successful execution artifact; SHA-256 `35ac16ad732fdf97a8f89a3f38c0a24f6f6a84fac11fef9897485f002c7990a6`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_09ad39f20819423c824319e47d4f12f7/request.json` — successful execution artifact; SHA-256 `61793bdcbcee168cb9db4c976c82df17240ec88fddfdd0b7777f1ff812ba9cda`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_09ad39f20819423c824319e47d4f12f7/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_12face5fedab4664b12523625fb53608/status.json` — successful status record; SHA-256 `2b8c48affed90e7367a95cf69b3f2746f399df4acb8345ba6f3da0d574df7ed1`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_12face5fedab4664b12523625fb53608/collection.json` — successful execution artifact; SHA-256 `be7a25af529c8d49581c7bb1b1b5c76df788d21dd8896c83fd42a2b8a86b54e9`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_12face5fedab4664b12523625fb53608/input.com` — successful execution artifact; SHA-256 `9d62d99e00dde367d0b1be830f19010f39d5bee9f22bdd5c69cc4f046564606a`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_12face5fedab4664b12523625fb53608/request.json` — successful execution artifact; SHA-256 `44c7504ef098a0278443bf9637b50c1ff456ebc61dedebd1839df42f637a5d6d`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_12face5fedab4664b12523625fb53608/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_483f7ee4025647e5ac2c24170b0c1478/status.json` — successful status record; SHA-256 `8a9c72f61b03492e6918825e1dd38f6608951a285184bfc9589ec62ae6619733`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_483f7ee4025647e5ac2c24170b0c1478/collection.json` — successful execution artifact; SHA-256 `bbfb21b91561e507c9d1b37c49b61938413a62118b3706c589ca897bd6a677c5`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_483f7ee4025647e5ac2c24170b0c1478/input.com` — successful execution artifact; SHA-256 `34dd8a52ac3592a27d16fa8c17b002fcbc0d9976fbd3b16eecf656ea06d8868a`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_483f7ee4025647e5ac2c24170b0c1478/request.json` — successful execution artifact; SHA-256 `b01ed2ce8f3e92157be19a3ac8859a4348f067057f674131dd5684c34d045e26`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_483f7ee4025647e5ac2c24170b0c1478/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_74d1bd285e6a4946b5cdf0a514ae95ff/status.json` — successful status record; SHA-256 `834c7fc2758bf50c5ea9dfc32edcb11fd0e773e4c3427cc287cf63751068dd37`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_74d1bd285e6a4946b5cdf0a514ae95ff/collection.json` — successful execution artifact; SHA-256 `e0875a4729b047c5bc09606c59b280da4c6168e184567a52ddeb73ce41973958`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_74d1bd285e6a4946b5cdf0a514ae95ff/input.com` — successful execution artifact; SHA-256 `252a64a3987024f3277054849ad93b578bff6de4493ec7c64db100e1b5f4169a`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_74d1bd285e6a4946b5cdf0a514ae95ff/request.json` — successful execution artifact; SHA-256 `cc19e77322333a3024484d57e2f064f3f03656be8e06ac57b74699c4f520c80c`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_74d1bd285e6a4946b5cdf0a514ae95ff/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_7ac12f5dc4e04b16ac31830f144704c5/status.json` — successful status record; SHA-256 `667a195396c97ad79fc73363b9bd27d5b4c12e81eb484de1df9d71ffb91107d0`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_7ac12f5dc4e04b16ac31830f144704c5/collection.json` — successful execution artifact; SHA-256 `58b549f83bd1d6c178ed7a3daa3fbd42f011e4d55b9830d1bdc796c030f9c0bf`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_7ac12f5dc4e04b16ac31830f144704c5/input.com` — successful execution artifact; SHA-256 `88b93f458d333c2b6eba913a94f1910b19c62567919e207235f376eb4e3afa0c`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_7ac12f5dc4e04b16ac31830f144704c5/request.json` — successful execution artifact; SHA-256 `97b419c70e4eab494f323423c6cf5066aa9327586c19b0ab8bd67cb02f9a82bb`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_7ac12f5dc4e04b16ac31830f144704c5/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_915855f7e15a43c480c873296724b8ea/status.json` — successful status record; SHA-256 `7f6b73a3975eb5a3ec8f66477118c011c25f159aa0f5e4b79924400f146e7971`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_915855f7e15a43c480c873296724b8ea/collection.json` — successful execution artifact; SHA-256 `459c7ce91dd46884b9bbdb3f85047203a00b018e3fa95b48fb60a330ea8ca01e`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_915855f7e15a43c480c873296724b8ea/input.com` — successful execution artifact; SHA-256 `5a16b4e948752014567bd3cff1f495a88c2f8eb0f0e2fa7b759f261d12ca0e60`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_915855f7e15a43c480c873296724b8ea/request.json` — successful execution artifact; SHA-256 `962b7b11b12bd702a46c4222669f45ea4c7a9a09c5f215327cfabcf9927f3d94`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_915855f7e15a43c480c873296724b8ea/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_ec69ba3f90ed46b0a7b73ba7f6bacdd1/status.json` — successful status record; SHA-256 `b5cafae607c95e42257ea9ba3f0a14252f86f4f0f432316c3a391ae1c2b9f88f`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_ec69ba3f90ed46b0a7b73ba7f6bacdd1/collection.json` — successful execution artifact; SHA-256 `3652c2f3736aa9737da713d24da1332f865f6768a8eca584d439d41254d48b75`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_ec69ba3f90ed46b0a7b73ba7f6bacdd1/input.com` — successful execution artifact; SHA-256 `ed2fc92c2be0ac46ce0e6882cdbcc0e12d3158705b018f3c24dadf1a547728c6`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_ec69ba3f90ed46b0a7b73ba7f6bacdd1/request.json` — successful execution artifact; SHA-256 `3c051b483b44cbe7972a38e8bedd94fe9c5f9670fb700a9aad122a7859ab27db`
- `docs/verification/group_4/paper_430b9cbe83c2c203/native_workspace_batch/outputs/execution_jobs/job_ec69ba3f90ed46b0a7b73ba7f6bacdd1/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/diselenide_cis_optfreq/status.json` — label=group_4 paper_430b9cbe83c2c203 diselenide_cis_optfreq; submitted_at=2026-08-29T16:02:23.501536+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311G(d,p) Opt=(Tight,MaxCycles=200) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/diselenide_cis_optfreq.chk`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/diselenide_cis_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/input.com`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_cis_optfreq/stdout.log`
2. `artifacts/gaussian_batch/diselenide_trans_optfreq/status.json` — label=group_4 paper_430b9cbe83c2c203 diselenide_trans_optfreq; submitted_at=2026-08-29T16:02:23.541758+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311G(d,p) Opt=(Tight,MaxCycles=200) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/diselenide_trans_optfreq.chk`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/diselenide_trans_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/input.com`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/diselenide_trans_optfreq/stdout.log`
3. `artifacts/gaussian_batch/cis_se_nmr/status.json` — label=group_4 paper_430b9cbe83c2c203 cis_se_nmr; submitted_at=2026-08-29T17:18:47.265850+00:00; software=gaussian; intent=single_point; route=#p B972/def2TZVP NMR=GIAO NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/cis_se_nmr.chk`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/cis_se_nmr_parsed.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/collection.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/input.com`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/stderr.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/cis_se_nmr/stdout.log`
4. `artifacts/gaussian_batch/trans_se_nmr/status.json` — label=group_4 paper_430b9cbe83c2c203 trans_se_nmr; submitted_at=2026-08-29T17:18:47.320523+00:00; software=gaussian; intent=single_point; route=#p B972/def2TZVP NMR=GIAO NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/collection.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/fort.7`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/input.com`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/parsed.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/stderr.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/stdout.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/trans_se_nmr.chk`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/trans_se_nmr/trans_se_nmr_parsed.json`
5. `artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/status.json` — label=group_4 paper_430b9cbe83c2c203 dimethyl_selenide_b972_nmr_reference; submitted_at=2026-08-30T19:27:17.668578+00:00; software=gaussian; intent=optimization_frequency; route=#p B972/def2TZVP Opt=(Tight,MaxCycles=300) Freq NMR=GIAO NoSymm Integral=UltraFine SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/collection.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/dimethyl_selenide_b972_nmr_reference.chk`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/dimethyl_selenide_b972_nmr_reference_parsed.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/input.com`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/stderr.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_nmr_reference/stdout.log`
6. `artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/status.json` — label=group_4 paper_430b9cbe83c2c203 triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1; submitted_at=2026-09-04T10:10:56.978435+00:00; software=gaussian; intent=single_point; route=#p B972/Gen NMR=GIAO NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/collection.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/input.com`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/stderr.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/stdout.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1/triselenide_trans_b972_pcsseg2_giao_author_route__basisfix1.chk`
7. `artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/status.json` — label=group_4 paper_430b9cbe83c2c203 dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1; submitted_at=2026-09-04T11:56:25.515167+00:00; software=gaussian; intent=optimization_frequency; route=#p B972/Gen Opt=(Tight,MaxCycles=300) Freq NMR=GIAO NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/collection.json`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1.chk`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/input.com`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/stderr.log`
   - output: `docs/verification/group_4/paper_430b9cbe83c2c203/artifacts/gaussian_batch/dimethyl_selenide_b972_pcsseg2_optfreq_author_route__basisfix1/stdout.log`

## Evaluator alignment

- Key-point IDs: `kp_process_stationary, kp_process_observable, kp_result_energy, kp_result_signals`
- Conclusion IDs: `c_final_assignment`
- Scoring-rule IDs: `r_stationary, r_shifts, r_energy, r_assignment, r_final`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_stationary` → reference `kp_process_stationary`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert validation of per-conformer diagnostics; evaluator_target_present=False
- rule `r_shifts` → reference `kp_process_observable`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert validation of per-site shifts and observed-feature comparison; evaluator_target_present=False
- rule `r_energy` → reference `kp_result_energy`; type=condition; unit=not recorded; tolerance=not recorded; comparison=condition: near-degenerate within 1 kcal/mol or justified bounded failure; evaluator_target_present=False
- rule `r_assignment` → reference `kp_result_signals`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_final` → reference `c_final_assignment`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].name` = `"cis"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].stationary` = `true`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].se_sites[0]` = `"Se atom 1 (input atom index 1)"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].se_sites[1]` = `"Se atom 2 (input atom index 2)"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].se_sites[2]` = `"Se atom 3 (input atom index 3)"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].diagnostics` = `"Gaussian 16 PW6B95/def2-QZVP Opt/Freq normal termination; 69 frequencies; NImag=0; geometry_job_id=hpc-job-1f81cb41-991f-4d4d-99fa-62532c8873e4; geometry_output_sha256=76de01d8d294383537cf1c1ab559dae5b6cf41abdb2429dfffabf0562e9ebbcb"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].shifts_ppm[0]` = `460.1713`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].shifts_ppm[1]` = `930.0386000000001`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[0].shifts_ppm[2]` = `413.39920000000006`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].name` = `"trans"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].stationary` = `true`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].se_sites[0]` = `"Se atom 1 (input atom index 1)"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].se_sites[1]` = `"Se atom 2 (input atom index 2)"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].se_sites[2]` = `"Se atom 3 (input atom index 3)"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].diagnostics` = `"Gaussian 16 PW6B95/def2-QZVP Opt/Freq normal termination; 69 frequencies; NImag=0; geometry_job_id=hpc-job-6c3cf81e-e812-4e27-aa86-c0d4e77f8a5b; geometry_output_sha256=326706bd6f78659f0534ba29a67d019e542fb381254c9ec49a0490848b11ba09"`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].shifts_ppm[0]` = `434.0228000000002`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].shifts_ppm[1]` = `925.3382`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers` / result path `$.conformers[1].shifts_ppm[2]` = `433.98710000000005`
- rule `r_stationary` / reference `kp_process_stationary` / field `$.conformers[].stationary` / result path `$.conformers[].stationary` = `true`
- rule `r_shifts` / reference `kp_process_observable` / field `$.methods.reference` / result path `$.methods.reference` = `"delta = sigma(Me2Se) - sigma(triselenide); same B97-2/pcSseg-2 GIAO reference, sigma(Me2Se)=1736.140100 ppm"`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].se_sites` / result path `$.conformers[].se_sites[0]` = `"Se atom 1 (input atom index 1)"`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].se_sites` / result path `$.conformers[].se_sites[1]` = `"Se atom 2 (input atom index 2)"`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].se_sites` / result path `$.conformers[].se_sites[2]` = `"Se atom 3 (input atom index 3)"`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].shifts_ppm` / result path `$.conformers[].shifts_ppm[0]` = `460.1713`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].shifts_ppm` / result path `$.conformers[].shifts_ppm[1]` = `930.0386000000001`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].shifts_ppm` / result path `$.conformers[].shifts_ppm[2]` = `413.39920000000006`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].shifts_ppm` / result path `$.conformers[].shifts_ppm[0]` = `434.0228000000002`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].shifts_ppm` / result path `$.conformers[].shifts_ppm[1]` = `925.3382`
- rule `r_shifts` / reference `kp_process_observable` / field `$.conformers[].shifts_ppm` / result path `$.conformers[].shifts_ppm[2]` = `433.98710000000005`
- rule `r_shifts` / reference `kp_process_observable` / field `$.comparison` / result path `$.comparison.observed_features_ppm[0]` = `422`
- rule `r_shifts` / reference `kp_process_observable` / field `$.comparison` / result path `$.comparison.observed_features_ppm[1]` = `816`
- rule `r_shifts` / reference `kp_process_observable` / field `$.comparison` / result path `$.comparison.assignment` = `"The repaired exact-route B97-2/pcSseg-2 referenced shifts are compared site-by-site with the weak approximately 422 and 816 ppm features. This is semiquantitative corroboration only; it does not prove a unique exchange rate, population m..."`
- rule `r_shifts` / reference `kp_process_observable` / field `$.comparison` / result path `$.comparison.evidence` = `"{\"cis_shifts_ppm\": [460.1713, 930.0386000000001, 413.39920000000006], \"geometry_job_ids\": {\"cis\": \"hpc-job-1f81cb41-991f-4d4d-99fa-62532c8873e4\", \"trans\": \"hpc-job-6c3cf81e-e812-4e27-aa86-c0d4e77f8a5b\"}, \"nearest_deviation_to_422_ppm\": 8..."`
- rule `r_energy` / reference `kp_result_energy` / field `$.relative_energy.value_kcal_mol` / result path `$.relative_energy.value_kcal_mol` = `0.7567764262349671`
- rule `r_energy` / reference `kp_result_energy` / field `$.relative_energy.uncertainty` / result path `$.relative_energy.uncertainty` = `"single supplied conformer pair and one geometry level; source near-degeneracy criterion is 1 kcal/mol"`
- rule `r_assignment` / reference `kp_result_signals` / field `$.conclusion` / result path `$.conclusion` = `"The supplied cis and trans triselenide structures were tested with the SI geometry route and repaired exact B97-2/pcSseg-2 GIAO/reference route. Their calculated shifts and common-level energy are reported directly; the semiquantitative ..."`
- rule `r_assignment` / reference `kp_result_signals` / field `$.limitations` / result path `$.limitations` = `"Two supplied conformers, isolated-molecule/vacuum model, no explicit CDCl3, no conformer ensemble, no population-weighted spectrum, and no exchange-rate calculation; ppm gate is an audit convention because the evaluator gives no numeric ..."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Two complete XYZ triselenide conformers and experimental ^77Se boundary.

Public input files and hashes:

- `agent_input/data/inputs/cis.xyz` — SHA-256 `28c6a82e8591172196f730fb1139307466ecf1ed3ca30a794a7700afd22997c0`; size=1018 bytes; xyz_atom_count=25; xyz_comment=Independent ETKDG topology-only starter cis; unoptimized; charge 0 multiplicity 1; atom order retained; explicit_boundary_fields={"charge": "0", "multiplicity": "1"}
- `agent_input/data/inputs/experimental_boundary.json` — SHA-256 `50da1c148902eed1ad19ac2cfe3183dab6131101e283be82e0ceff794d3f13b9`; size=223 bytes; explicit_boundary_fields={"$.charge": 0, "$.multiplicity": 1, "$.solvent": "CDCl3", "$.temperature_C": 25}
- `agent_input/data/inputs/starting_geometry_definition.json` — SHA-256 `a0dbda093969c05131b422cf4dc86622e6af7c590e7cb6336e29707580c889f1`; size=1594 bytes; explicit_boundary_fields={"$.atom_count": 25, "$.charge": 0, "$.formula": "C12F10Se3", "$.mapped_smiles": "[Se:1]([Se:2][Se:3][c:10]1[c:11]([F:19])[c:13]([F:18])[c:15]([F:17])[c:14]([F:16])[c:12]1[F:20])[c:4]1[c:5]([F:25])[c:7]([F:24])[c:9]([F:23])[c:8]([F:22])[c:6]1[F:21]", "$.multiplicity": 1}
- `agent_input/data/inputs/trans.xyz` — SHA-256 `3eaaa1a067ef820818fdcf8a75227db22a62bb98a758b59a0134ce5e92f0e232`; size=1026 bytes; xyz_atom_count=25; xyz_comment=Independent ETKDG topology-only starter trans; unoptimized; charge 0 multiplicity 1; atom order retained; explicit_boundary_fields={"charge": "0", "multiplicity": "1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_4/paper_430b9cbe83c2c203/verification_report.md` — verification record; SHA-256 `4f0a0deb2407a601440d3636e99c70e05ce2fe6bdb1fb61717207ef07a15d7ea`
- `docs/verification/group_4/paper_430b9cbe83c2c203/report/results.json` — verification record; SHA-256 `09b1335ddf1bfca16314f661ff6f0ebc51ff8ed1b1b3d7547e96a2190478dbe5`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
