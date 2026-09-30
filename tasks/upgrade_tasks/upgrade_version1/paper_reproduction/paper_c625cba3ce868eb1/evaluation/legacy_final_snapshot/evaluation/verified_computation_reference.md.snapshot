# Verified computation reference — paper_c625cba3ce868eb1 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 6 | `PASS` | - 论文复现结论：`PASS`（在定义的反应物态 MEP/MK 电荷比较范围内）。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Stereocontrolled Synthesis of α-Branched Tetrahydropyrans by a One-Pot-Two-Step Photobiocatalytic Cascade of Citronellol
- DOI: `10.1021/acs.jnatprod.5c01352`
- Task package: `tasks/final_verified_paper_reproduction/paper_c625cba3ce868eb1`
- Verification group: `docs/verification/group_4/paper_c625cba3ce868eb1`
- Paper documents: `papers/paper_c625cba3ce868eb1`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "alkene_charge_differences": {
      "absolute_difference_ratio_R4_to_7": 8.815506415506421,
      "compound_4_R_proximal_minus_distal": -0.484368,
      "compound_7_site8_minus_site10": -0.054944999999999966
    },
    "polarization_statement": "The hydroperoxide-containing compound 4-R has a substantially larger signed proximal/distal alkene charge separation (−0.484368 e) than hydroperoxide-free compound 7 (−0.054945 e), supporting stronger adjacent-alkene polarization under this common MK/CPCM model."
  },
  "coverage": {
    "conformer_or_method_scope": "One supplied conformer per molecule; same B3LYP/CBSB7 Pop=MK/CPCM-water protocol; no geometry optimization or conformer search was used because the task explicitly permits fixed-conformer reactant-state descriptors.",
    "structures_evaluated": [
      "supplied compound_4_R.xyz",
      "supplied compound_7.xyz"
    ]
  },
  "limitations": [
    "MK charges and MEP are model-dependent; the comparison is internally consistent but not an experimental charge measurement.",
    "Only the supplied conformers were evaluated; no global conformer ranking is claimed.",
    "The Gaussian native output contains the ESP fit and atom charges, but no transition-state or product calculation was requested."
  ],
  "molecules": {
    "compound_4_R": {
      "alkene_carbon_indices": [
        2,
        4
      ],
      "atom_count": 33,
      "charge_definition": "Gaussian 16 C.01 Merz-Kollman ESP-fit (Pop=MK) charges; atom-indexed 1-based, hydrogens explicit.",
      "charges": [
        0.788307,
        -0.534,
        0.190467,
        -0.049632,
        0.112078,
        -0.151048,
        0.085055,
        0.054875,
        "<success-only excerpt: 8 of 33 entries>"
      ],
      "method": "B3LYP/CBSB7, CPCM water, single-point ESP/MK fit on supplied neutral singlet conformer.",
      "validation": {
        "evidence": "{\"case\": \"R4_esp_mk\", \"duration_seconds\": 470.294112, \"esp_fit_rms\": 0.00132, \"esp_fit_rrms\": 0.07328, \"input_sha256\": \"1a14db78f3ab71b774685d1171eaae0564c4581e4156bc9dbcd9a9523e44b65d\", \"job_id\": \"job_52e2e4c150a04ff0a9fe31039996cd35\", \"normal_termination\": true, \"scf_done\": true, \"status\": \"success\", \"stdout_sha256\": \"0bb004fd7b10ab6354d62d5a1cb4e087682edb207346d74d77a045e7c3db1bc4\", \"walltime_seconds\": null}",
        "status": "passed"
      }
    },
    "compound_7": {
      "alkene_carbon_indices": [
        8,
        10
      ],
      "atom_count": 25,
      "charge_definition": "Gaussian 16 C.01 Merz-Kollman ESP-fit (Pop=MK) charges; atom-indexed 1-based, hydrogens explicit.",
      "charges": [
        -0.18176,
        0.047419,
        0.046638,
        0.036983,
        0.198744,
        -0.006369,
        -0.005925,
        -0.313368,
        "<success-only excerpt: 8 of 25 entries>"
      ],
      "method": "B3LYP/CBSB7, CPCM water, single-point ESP/MK fit on supplied neutral singlet conformer.",
      "validation": {
        "evidence": "{\"case\": \"alkenol7_esp_mk\", \"duration_seconds\": 124.143234, \"esp_fit_rms\": 0.0017, \"esp_fit_rrms\": 0.15435, \"input_sha256\": \"c85a66cbeb0b7938729750f448670368dac669f1174d1728d699a51ed41a8d81\", \"job_id\": \"job_184df5885a3e4b978c062f5ab144dc8f\", \"normal_termination\": true, \"scf_done\": true, \"status\": \"success\", \"stdout_sha256\": \"fe902d2eedf870f2ff10eca31b35be6388e85275a2f2bfbdb41f11e2fc69d106\", \"walltime_seconds\": null}",
        "status": "passed"
      }
    }
  },
  "provenance": {
    "charge_definition": "Merz-Kollman electrostatic-potential fit charges from Gaussian Pop=MK",
    "method": "B3LYP/CBSB7 Pop=MK SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512)",
    "software": "Gaussian 16 C.01 native"
  },
  "status": "complete"
}
```

Paper/SI document hashes:

- `papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf` — SHA-256 `19d3e128aae61e6d8f4904d7f5f3cc8cd31230ccb210eb81ba15402de096e4db` (declared_match=True)
- `papers/paper_c625cba3ce868eb1/documents/main.pdf` — SHA-256 `44b374957665d941b519f781fe9341f1632c84a6c7b975c4cd231874281e0ef8` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **90**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/status.json` — successful status record; SHA-256 `80e19ed9c8f1f5dfad0118341a16e907fd78fdb068d2f96d90c4788756f7e13e`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/R4_esp_mk_parsed.json` — successful execution artifact; SHA-256 `226a84160fb78dcbe41f7d0f282acf960fe070148bd6677024542864bc7be6a5`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/collection.json` — successful execution artifact; SHA-256 `8a181717996df78cbb3e2a0463e6e3c0e0f545e951451c6e4be401d1fa7f0be5`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/input.com` — successful execution artifact; SHA-256 `1a14db78f3ab71b774685d1171eaae0564c4581e4156bc9dbcd9a9523e44b65d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/parsed.json` — successful execution artifact; SHA-256 `6d06bce88ddbfe9b432fb1990fe86f81adf8bcfe2e0bd38c28db188376b0d150`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/status.json` — successful status record; SHA-256 `35882222acbcd9e3e9286fe02c8bc8710c31a13bffc7f96d3d67e1f113edb64e`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/alkenol7_esp_mk_parsed.json` — successful execution artifact; SHA-256 `3c9b2280e09d0fcbae8875185f01eef72a1471e56e3e3483e83bb2a93cde0c74`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/collection.json` — successful execution artifact; SHA-256 `8f5a54c15d77f72082838bea78ccca4bc46722947d3da7441d930d433334be49`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/input.com` — successful execution artifact; SHA-256 `c85a66cbeb0b7938729750f448670368dac669f1174d1728d699a51ed41a8d81`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/parsed.json` — successful execution artifact; SHA-256 `bcb123d70931499be5729e4cd3aaab3b8f5802132f5c110cc0d35d8612a31102`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/status.json` — successful status record; SHA-256 `3e33fbd967795f9d3faa941d7215027e21cb509d43ac762137f746375e954ef6`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/baseline_compound_4_R__resource_retry_parsed.json` — successful execution artifact; SHA-256 `b117ced83a25ce36dc038679d9166b804c1f58e35bc90c9f3b2189f047621cb8`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/collection.json` — successful execution artifact; SHA-256 `fb849065c3e80ea80ead67982b8c9fce73246de38f126f223f812c4d73c2d8fd`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/input.com` — successful execution artifact; SHA-256 `84a52165175ab0c92acf0ac0f5a914b090fec09e33ee0a1c2ca43e9879a97d1d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/status.json` — successful status record; SHA-256 `1e8cdcbf224830455482617a0075aa38d6c192ee5aa97569e1018b791a894a70`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/baseline_compound_7_parsed.json` — successful execution artifact; SHA-256 `6fad2f9f3a8059e3f413ad71386ddefd1093d2041b0670708e30e388eb7248a5`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/collection.json` — successful execution artifact; SHA-256 `a9643867ab0fff7c6b0ec3e0f55dd69fadb74f5cd3b485feb6483b71065ef5da`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/input.com` — successful execution artifact; SHA-256 `e8000ef83c034645059636937705c7dde8a23b6586228f7481b8f04a7af859b2`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/parsed.json` — successful execution artifact; SHA-256 `5c8170074718234c212852cae9395f5dc60477dcf2db861e13b7619758354623`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/status.json` — successful status record; SHA-256 `8a98868165ac7505bb2cd1a44feacce1325f3745d0262fc57d27d007f7b2844b`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/c625_author_4R_esp_mk_parsed.json` — successful execution artifact; SHA-256 `ecb7ce29e72149e810b0e6d4669e1de745f4ab972642cae420f89f0fcae10198`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/collection.json` — successful execution artifact; SHA-256 `5f24e4f3589022b2db1d888009482956acc15d6d96aa5094fae4a68f7977ad5f`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/input.com` — successful execution artifact; SHA-256 `3d48b391aa4bb82aec9b81bae912ad4c4ac51eea83a080eef3e522915e5d79e0`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/status.json` — successful status record; SHA-256 `c028eb994c5c3ccf8ad67e7da4e738e932cf9b600c22262304db5799883ba401`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/c625_author_4R_optfreq_parsed.json` — successful execution artifact; SHA-256 `298a13e5ca5299415bb9e86c4628d782a1cd601dd70082013c544e9d7033bec8`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/collection.json` — successful execution artifact; SHA-256 `c9422b7a5a6303d4efc95f422c43704cadcaaf191289f3f4c1239193f3ac183a`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/input.com` — successful execution artifact; SHA-256 `69b2d70979a3d010c0a32fc0957840609b564358212050d807910460af80b7aa`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/status.json` — successful status record; SHA-256 `9a0befee72eb829ee217aeb099087efea4c621a3d5ab388f3b63718087bd588d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/c625_author_7_esp_mk_parsed.json` — successful execution artifact; SHA-256 `5b71c90564bc3bb965ed320665eb418cea4da4f5188e7ad34a4538cffcaf257c`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/collection.json` — successful execution artifact; SHA-256 `02526997d913542313145b2e7169e939101b5c0538206b13f53d4c23e868bd5f`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/input.com` — successful execution artifact; SHA-256 `5ff2cc2ed0573074385f29bd4efac874dea67a227444d2b26cfaa57ebf36ee83`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/status.json` — successful status record; SHA-256 `6ddd4e0ed42cccb5ddb07a6074c9f065e0eec3c7dfd2ef523d1ff609f531b990`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/c625_author_7_optfreq_parsed.json` — successful execution artifact; SHA-256 `c4a38526e270b6a0afb410f6a1de0b90a6d066efa7ae02003b1dfba184add90b`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/collection.json` — successful execution artifact; SHA-256 `a30cf559baa9c891d91943202e4401a04e4db67e76b4a3a1eee3fa7985f10cb2`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/input.com` — successful execution artifact; SHA-256 `9eaf09bac2596ff6a465d6f77928ecd4f2b372a7823a4190ac961794ae3f2590`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/status.json` — successful status record; SHA-256 `4036dc441b84b84344f49ffc751092200cd3a9e9b8d1e3d976e71bd69b5704f4`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/collection.json` — successful execution artifact; SHA-256 `40508fade69b1ce9fbdca4968ce4921bf48e9a3c6c131d162e9e235ff912af8f`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/coverage_compound_4_R_parsed.json` — successful execution artifact; SHA-256 `3f18bd147a7487f0e7c39ae55e866e22e3c75a4169a6d6cb5364eea4f84999ef`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/input.com` — successful execution artifact; SHA-256 `7134d0b0862a9393dea58f0149604ee03fbc5c9fbe7dd1d68ba0b1ae0735c65d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_184df5885a3e4b978c062f5ab144dc8f/status.json` — successful status record; SHA-256 `35882222acbcd9e3e9286fe02c8bc8710c31a13bffc7f96d3d67e1f113edb64e`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_184df5885a3e4b978c062f5ab144dc8f/collection.json` — successful execution artifact; SHA-256 `8f5a54c15d77f72082838bea78ccca4bc46722947d3da7441d930d433334be49`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_184df5885a3e4b978c062f5ab144dc8f/input.com` — successful execution artifact; SHA-256 `c85a66cbeb0b7938729750f448670368dac669f1174d1728d699a51ed41a8d81`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_184df5885a3e4b978c062f5ab144dc8f/request.json` — successful execution artifact; SHA-256 `f4572e9a92deccc4a3b03d1c2bab5f8d1408d10c72b02b5453f85fcd14cedcba`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_184df5885a3e4b978c062f5ab144dc8f/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_262323bbb5d74327a63c4faae32ee4cd/status.json` — successful status record; SHA-256 `1e8cdcbf224830455482617a0075aa38d6c192ee5aa97569e1018b791a894a70`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_262323bbb5d74327a63c4faae32ee4cd/collection.json` — successful execution artifact; SHA-256 `a9643867ab0fff7c6b0ec3e0f55dd69fadb74f5cd3b485feb6483b71065ef5da`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_262323bbb5d74327a63c4faae32ee4cd/input.com` — successful execution artifact; SHA-256 `e8000ef83c034645059636937705c7dde8a23b6586228f7481b8f04a7af859b2`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_262323bbb5d74327a63c4faae32ee4cd/request.json` — successful execution artifact; SHA-256 `4c2eeb11db071c26ef79e9f807edca51a6e574777945e28e8f00d4dc17def631`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_262323bbb5d74327a63c4faae32ee4cd/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/status.json` — successful status record; SHA-256 `9a0befee72eb829ee217aeb099087efea4c621a3d5ab388f3b63718087bd588d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/collection.json` — successful execution artifact; SHA-256 `02526997d913542313145b2e7169e939101b5c0538206b13f53d4c23e868bd5f`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/input.com` — successful execution artifact; SHA-256 `5ff2cc2ed0573074385f29bd4efac874dea67a227444d2b26cfaa57ebf36ee83`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/request.json` — successful execution artifact; SHA-256 `d1eb450c301d3c59ef3384e50b709adeeda05c7a05926e6aae5a140d81772180`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_2b9b02fae1144ff59c02afcb72793dbc/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/status.json` — successful status record; SHA-256 `c028eb994c5c3ccf8ad67e7da4e738e932cf9b600c22262304db5799883ba401`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/collection.json` — successful execution artifact; SHA-256 `c9422b7a5a6303d4efc95f422c43704cadcaaf191289f3f4c1239193f3ac183a`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/input.com` — successful execution artifact; SHA-256 `69b2d70979a3d010c0a32fc0957840609b564358212050d807910460af80b7aa`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/request.json` — successful execution artifact; SHA-256 `df7f461a1306467cbef9779f6648e6d475fdc9467938c77221e3854feaf369bd`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_473a36ad38d341958b02aed35c740048/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_52e2e4c150a04ff0a9fe31039996cd35/status.json` — successful status record; SHA-256 `80e19ed9c8f1f5dfad0118341a16e907fd78fdb068d2f96d90c4788756f7e13e`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_52e2e4c150a04ff0a9fe31039996cd35/collection.json` — successful execution artifact; SHA-256 `8a181717996df78cbb3e2a0463e6e3c0e0f545e951451c6e4be401d1fa7f0be5`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_52e2e4c150a04ff0a9fe31039996cd35/input.com` — successful execution artifact; SHA-256 `1a14db78f3ab71b774685d1171eaae0564c4581e4156bc9dbcd9a9523e44b65d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_52e2e4c150a04ff0a9fe31039996cd35/request.json` — successful execution artifact; SHA-256 `b50431187c1a130456c4b266d4093aaf04480f1b1be26e9428f8bc6944a173d8`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_52e2e4c150a04ff0a9fe31039996cd35/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/status.json` — successful status record; SHA-256 `8a98868165ac7505bb2cd1a44feacce1325f3745d0262fc57d27d007f7b2844b`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/collection.json` — successful execution artifact; SHA-256 `5f24e4f3589022b2db1d888009482956acc15d6d96aa5094fae4a68f7977ad5f`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/input.com` — successful execution artifact; SHA-256 `3d48b391aa4bb82aec9b81bae912ad4c4ac51eea83a080eef3e522915e5d79e0`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/request.json` — successful execution artifact; SHA-256 `4b1fe00a50f535a7c41f12dd1673a8e43561b8ea13051562ec37fd9b2953f060`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_75bc460f20924dbcb98c93557fa6edfe/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_7ffe1ca633794f38b968cc7714534227/status.json` — successful status record; SHA-256 `4036dc441b84b84344f49ffc751092200cd3a9e9b8d1e3d976e71bd69b5704f4`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_7ffe1ca633794f38b968cc7714534227/collection.json` — successful execution artifact; SHA-256 `40508fade69b1ce9fbdca4968ce4921bf48e9a3c6c131d162e9e235ff912af8f`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_7ffe1ca633794f38b968cc7714534227/input.com` — successful execution artifact; SHA-256 `7134d0b0862a9393dea58f0149604ee03fbc5c9fbe7dd1d68ba0b1ae0735c65d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_7ffe1ca633794f38b968cc7714534227/request.json` — successful execution artifact; SHA-256 `b6b49b7994c0f0732f4e34324694b65decbb94ab6426363a8a484de197af660b`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_7ffe1ca633794f38b968cc7714534227/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/status.json` — successful status record; SHA-256 `6ddd4e0ed42cccb5ddb07a6074c9f065e0eec3c7dfd2ef523d1ff609f531b990`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/collection.json` — successful execution artifact; SHA-256 `a30cf559baa9c891d91943202e4401a04e4db67e76b4a3a1eee3fa7985f10cb2`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/input.com` — successful execution artifact; SHA-256 `9eaf09bac2596ff6a465d6f77928ecd4f2b372a7823a4190ac961794ae3f2590`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/request.json` — successful execution artifact; SHA-256 `36499e6948902bf7a2e1edd53dc741d9233e71c353db7b61332ce4887be3ee9f`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_c20aa070178144a7b9da10ec8f730eba/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_f7ce2a7e218443e4822db8428f4432b7/status.json` — successful status record; SHA-256 `3e33fbd967795f9d3faa941d7215027e21cb509d43ac762137f746375e954ef6`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_f7ce2a7e218443e4822db8428f4432b7/collection.json` — successful execution artifact; SHA-256 `fb849065c3e80ea80ead67982b8c9fce73246de38f126f223f812c4d73c2d8fd`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_f7ce2a7e218443e4822db8428f4432b7/input.com` — successful execution artifact; SHA-256 `84a52165175ab0c92acf0ac0f5a914b090fec09e33ee0a1c2ca43e9879a97d1d`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_f7ce2a7e218443e4822db8428f4432b7/request.json` — successful execution artifact; SHA-256 `b5ca4f63ed6c99d8651d2f4fcfb3edb8fd84d584534d62a6cee1a776d241c081`
- `docs/verification/group_4/paper_c625cba3ce868eb1/native_workspace_batch/outputs/execution_jobs/job_f7ce2a7e218443e4822db8428f4432b7/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/coverage_compound_4_R/status.json` — label=group_4 paper_c625cba3ce868eb1 coverage_compound_4_R; submitted_at=2026-08-29T17:10:22.506521+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt=(Tight,MaxCycles=200) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/coverage_compound_4_R.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/coverage_compound_4_R_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/coverage_compound_4_R/stdout.log`
2. `artifacts/gaussian_batch/baseline_compound_7/status.json` — label=group_4 paper_c625cba3ce868eb1 baseline_compound_7; submitted_at=2026-08-29T17:12:30.509419+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/CBSB7 Opt=(Tight,MaxCycles=200) Freq SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/baseline_compound_7.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/baseline_compound_7_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_7/stdout.log`
3. `artifacts/gaussian_batch/R4_esp_mk/status.json` — label=group_4 paper_c625cba3ce868eb1 R4_esp_mk; submitted_at=2026-08-29T17:18:58.404399+00:00; software=gaussian; intent=single_point; route=#p B3LYP/CBSB7 Pop=MK SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/R4_esp_mk.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/R4_esp_mk_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/R4_esp_mk/stdout.log`
4. `artifacts/gaussian_batch/alkenol7_esp_mk/status.json` — label=group_4 paper_c625cba3ce868eb1 alkenol7_esp_mk; submitted_at=2026-08-29T17:18:58.447600+00:00; software=gaussian; intent=single_point; route=#p B3LYP/CBSB7 Pop=MK SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/alkenol7_esp_mk.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/alkenol7_esp_mk_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/alkenol7_esp_mk/stdout.log`
5. `artifacts/gaussian_batch/c625_author_4R_optfreq/status.json` — label=group_4 paper_c625cba3ce868eb1 c625_author_4R_optfreq; submitted_at=2026-08-30T19:19:34.903735+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/CBSB7 Opt=(Tight,MaxCycles=300) Freq SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/c625_author_4R_optfreq.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/c625_author_4R_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_optfreq/stdout.log`
6. `artifacts/gaussian_batch/c625_author_7_optfreq/status.json` — label=group_4 paper_c625cba3ce868eb1 c625_author_7_optfreq; submitted_at=2026-08-30T19:19:34.977334+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/CBSB7 Opt=(Tight,MaxCycles=300) Freq SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/c625_author_7_optfreq.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/c625_author_7_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_optfreq/stdout.log`
7. `artifacts/gaussian_batch/c625_author_4R_esp_mk/status.json` — label=group_4 paper_c625cba3ce868eb1 c625_author_4R_esp_mk; submitted_at=2026-08-31T01:31:45.267241+00:00; software=gaussian; intent=single_point; route=#p B3LYP/CBSB7 Pop=MK SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/c625_author_4R_esp_mk.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/c625_author_4R_esp_mk_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_4R_esp_mk/stdout.log`
8. `artifacts/gaussian_batch/c625_author_7_esp_mk/status.json` — label=group_4 paper_c625cba3ce868eb1 c625_author_7_esp_mk; submitted_at=2026-08-31T01:31:45.310346+00:00; software=gaussian; intent=single_point; route=#p B3LYP/CBSB7 Pop=MK SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/c625_author_7_esp_mk.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/c625_author_7_esp_mk_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/c625_author_7_esp_mk/stdout.log`
9. `artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/status.json` — label=group_4 paper_c625cba3ce868eb1 baseline_compound_4_R__resource_retry; submitted_at=2026-08-31T01:51:02.950726+00:00; software=gaussian; intent=optimization_frequency; route=#p  B3LYP/CBSB7 Opt=(Tight,MaxCycles=200) Freq SCRF=(CPCM,Solvent=Water) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/baseline_compound_4_R__resource_retry.chk`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/baseline_compound_4_R__resource_retry_parsed.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/collection.json`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/input.com`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/stderr.log`
   - output: `docs/verification/group_4/paper_c625cba3ce868eb1/artifacts/gaussian_batch/baseline_compound_4_R__resource_retry/stdout.log`

## Evaluator alignment

- Key-point IDs: `pr_process_minima, pr_process_charges, pr_result_4_polarized, pr_result_7_symmetric, pr_result_limit`
- Conclusion IDs: `pr_final_conclusion`
- Scoring-rule IDs: `pr_r1, pr_r2, pr_r3, pr_r4, pr_r5, pr_r6`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `pr_r1` → reference `pr_process_minima`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r2` → reference `pr_process_charges`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r3` → reference `pr_result_4_polarized`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r4` → reference `pr_result_7_symmetric`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r5` → reference `pr_result_limit`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r6` → reference `pr_final_conclusion`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.atom_count` = `33`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.alkene_carbon_indices[0]` = `2`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.alkene_carbon_indices[1]` = `4`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[0]` = `0.788307`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[1]` = `-0.534`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[2]` = `0.190467`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[3]` = `-0.049632`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[4]` = `0.112078`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[5]` = `-0.151048`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[6]` = `0.085055`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[7]` = `0.054875`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[8]` = `0.271476`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[9]` = `0.004253`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[10]` = `-0.549293`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[11]` = `0.129929`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[12]` = `0.128061`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[13]` = `0.130956`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[14]` = `-0.019516`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[15]` = `0.015341`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[16]` = `0.0276`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[17]` = `0.236187`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[18]` = `-0.015127`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[19]` = `0.001221`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[20]` = `-0.695723`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[21]` = `0.431992`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[22]` = `-0.357368`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[23]` = `-0.442745`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[24]` = `0.432395`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[25]` = `-0.510968`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[26]` = `0.13032`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[27]` = `0.127483`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[28]` = `0.110114`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[29]` = `-0.29548`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[30]` = `0.074713`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charges[31]` = `0.077126`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.charge_definition` = `"Gaussian 16 C.01 Merz-Kollman ESP-fit (Pop=MK) charges; atom-indexed 1-based, hydrogens explicit."`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.validation.status` = `"passed"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.validation.evidence` = `"{\"case\": \"R4_esp_mk\", \"duration_seconds\": 470.294112, \"esp_fit_rms\": 0.00132, \"esp_fit_rrms\": 0.07328, \"input_sha256\": \"1a14db78f3ab71b774685d1171eaae0564c4581e4156bc9dbcd9a9523e44b65d\", \"job_id\": \"job_52e2e4c150a04ff0a9fe31039996cd35\", ..."`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_4_R.method` = `"B3LYP/CBSB7, CPCM water, single-point ESP/MK fit on supplied neutral singlet conformer."`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.atom_count` = `25`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.alkene_carbon_indices[0]` = `8`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.alkene_carbon_indices[1]` = `10`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[0]` = `-0.18176`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[1]` = `0.047419`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[2]` = `0.046638`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[3]` = `0.036983`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[4]` = `0.198744`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[5]` = `-0.006369`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[6]` = `-0.005925`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[7]` = `-0.313368`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[8]` = `0.171444`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[9]` = `-0.258423`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[10]` = `0.154942`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[11]` = `0.096857`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[12]` = `0.003861`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[13]` = `0.005321`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[14]` = `-0.022764`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[15]` = `0.012022`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[16]` = `0.008747`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[17]` = `-0.010251`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[18]` = `0.023907`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[19]` = `0.024633`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[20]` = `0.244049`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[21]` = `-0.006634`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[22]` = `-0.004498`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[23]` = `-0.695686`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charges[24]` = `0.43011`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.charge_definition` = `"Gaussian 16 C.01 Merz-Kollman ESP-fit (Pop=MK) charges; atom-indexed 1-based, hydrogens explicit."`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.validation.status` = `"passed"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.validation.evidence` = `"{\"case\": \"alkenol7_esp_mk\", \"duration_seconds\": 124.143234, \"esp_fit_rms\": 0.0017, \"esp_fit_rrms\": 0.15435, \"input_sha256\": \"c85a66cbeb0b7938729750f448670368dac669f1174d1728d699a51ed41a8d81\", \"job_id\": \"job_184df5885a3e4b978c062f5ab144dc..."`
- rule `pr_r1` / reference `pr_process_minima` / field `$.molecules` / result path `$.molecules.compound_7.method` = `"B3LYP/CBSB7, CPCM water, single-point ESP/MK fit on supplied neutral singlet conformer."`
- rule `pr_r3` / reference `pr_result_4_polarized` / field `$.comparison` / result path `$.comparison.alkene_charge_differences.compound_4_R_proximal_minus_distal` = `-0.484368`
- rule `pr_r3` / reference `pr_result_4_polarized` / field `$.comparison` / result path `$.comparison.alkene_charge_differences.compound_7_site8_minus_site10` = `-0.054944999999999966`
- rule `pr_r3` / reference `pr_result_4_polarized` / field `$.comparison` / result path `$.comparison.alkene_charge_differences.absolute_difference_ratio_R4_to_7` = `8.815506415506421`
- rule `pr_r3` / reference `pr_result_4_polarized` / field `$.comparison` / result path `$.comparison.polarization_statement` = `"The hydroperoxide-containing compound 4-R has a substantially larger signed proximal/distal alkene charge separation (−0.484368 e) than hydroperoxide-free compound 7 (−0.054945 e), supporting stronger adjacent-alkene polarization under t..."`
- rule `pr_r5` / reference `pr_result_limit` / field `$.limitations` / result path `$.limitations[0]` = `"MK charges and MEP are model-dependent; the comparison is internally consistent but not an experimental charge measurement."`
- rule `pr_r5` / reference `pr_result_limit` / field `$.limitations` / result path `$.limitations[1]` = `"Only the supplied conformers were evaluated; no global conformer ranking is claimed."`
- rule `pr_r5` / reference `pr_result_limit` / field `$.limitations` / result path `$.limitations[2]` = `"The Gaussian native output contains the ESP fit and atom charges, but no transition-state or product calculation was requested."`
- rule `pr_r6` / reference `pr_final_conclusion` / field `$.coverage` / result path `$.coverage.structures_evaluated[0]` = `"supplied compound_4_R.xyz"`
- rule `pr_r6` / reference `pr_final_conclusion` / field `$.coverage` / result path `$.coverage.structures_evaluated[1]` = `"supplied compound_7.xyz"`
- rule `pr_r6` / reference `pr_final_conclusion` / field `$.coverage` / result path `$.coverage.conformer_or_method_scope` = `"One supplied conformer per molecule; same B3LYP/CBSB7 Pop=MK/CPCM-water protocol; no geometry optimization or conformer search was used because the task explicitly permits fixed-conformer reactant-state descriptors."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Atom-ordered XYZ geometries for neutral singlet (R)-4 and alkenol 7.

Public input files and hashes:

- `agent_input/data/inputs/compound_4_R.xyz` — SHA-256 `def5088f208ea702a62daa1417047075d28a5a760a02020cdbc9e4105e5b6587`; size=1084 bytes; xyz_atom_count=33; xyz_comment=(R)-4; source SI#4.2; neutral singlet; atom order is benchmark identity; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/compound_7.xyz` — SHA-256 `dc05b11a09f7d2f89a060e45ccedfe774ab73cb7848b42cedbfe11098b385e24`; size=833 bytes; xyz_atom_count=25; xyz_comment=7; source SI#4.2; neutral singlet; atom order is benchmark identity; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `agent_input/data/inputs/compound_4_R.xyz, agent_input/data/inputs/compound_7.xyz`

## Evidence files

- `docs/verification/group_4/paper_c625cba3ce868eb1/verification_report.md` — verification record; SHA-256 `482e05d4e2c553682cbd0f7b6286e76f16c2fec1deb12e6d6391c3b30f35dfdd`
- `docs/verification/group_4/paper_c625cba3ce868eb1/report/results.json` — verification record; SHA-256 `e243fcb56ab6cc9639b3cfca9955181e8dcf3541e8afde49b913d8b0794618d5`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
