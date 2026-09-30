# Verified computation reference — paper_3316e45a74258fb7 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `success` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 57 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 report/results.json、artifacts/gaussian/ 和 provenance/。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: High-efficiency red TADF OLEDs based on phenanthroline-pyrazine derivatives with tailored donor substitution
- DOI: `10.1016/j.dyepig.2025.113467`
- Task package: `tasks/final_verified_autonomous_research/paper_3316e45a74258fb7`
- Verification group: `docs/verification/group_3/paper_3316e45a74258fb7`
- Paper documents: `papers/paper_3316e45a74258fb7`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "Validated S0 and matched-geometry TD roots give S1=2.1404 eV, T1=1.8322 eV, ΔE_ST=0.3082 eV and S1 NTO D=4.9043 Å; the disclosed D>=2.0 Å rule classifies S1 as CT-like separation.",
  "excited_states": {
    "s1_dominant_configuration": {
      "coefficient": 0.69036,
      "direction": "->",
      "from_orbital": 265,
      "to_orbital": 266,
      "weight": 0.47659692959999994
    },
    "s1_energy_eV": 2.1404,
    "state_assignment_evidence": "S1 is first singlet TD root; T1 is first triplet root in the separate matched-geometry triplet TD run.",
    "t1_energy_eV": 1.8322
  },
  "gap": {
    "calculation": "E(S1)-E(T1) from matched TD-DFT roots.",
    "delta_est_eV": 0.30820000000000003
  },
  "limitations": "Gas-phase isolated molecule; one conformer; D-index threshold and TD-DFT model are diagnostics rather than proof of an experimental TADF rate.",
  "optimization": {
    "performed": true,
    "validation_evidence": "Gaussian Opt/Freq normal termination and a nonempty zero-imaginary-frequency Hessian."
  },
  "oscillator_strength": {
    "evidence": "First singlet root oscillator strength parsed from Gaussian TD output.",
    "status": "computed",
    "value": 0.7627
  },
  "state_character": {
    "assessment": "CT-like separation",
    "d_index_angstrom": 4.904347092502112,
    "evidence": {
      "distance_angstrom": 4.904347092502112,
      "electron_centroid_angstrom": [
        -2.6958170815872444,
        2.8201296726406224,
        -1.4323152827803352
      ],
      "electron_orbital_index_1based": 266,
      "evidence": [
        "artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_hole.cube",
        "artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_electron.cube",
        "artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto.fchk"
      ],
      "grid": "Gaussian cubegen coarse (-2), identical automatic box for the paired saved NTOs",
      "hole_centroid_angstrom": [
        1.8313239890140647,
        0.9341317125020752,
        -1.4573317765793337
      ],
      "hole_orbital_index_1based": 265
    },
    "method": "Gaussian S1 transition density, SaveNTO and cubegen hole/electron centroid integration"
  },
  "status": "success",
  "structure": {
    "conformer_coverage": "One generated conformer; no exhaustive search.",
    "geometry_source": "verification-stage OPSIN/RDKit conformer; artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated_optimized.xyz",
    "object_id": "TD-2T"
  }
}
```

Paper/SI document hashes:

- `papers/paper_3316e45a74258fb7/documents/main.pdf` — SHA-256 `0061ebb5bb7ee96d72e00f384ab0f89006a46759102ba391287f86108303c5a9` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **70**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/status.json` — successful status record; SHA-256 `2c435253a0be968a0b591f251ecd8f00de6cbe17206299e6c1476b2aaa74ba11`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_optimized.xyz` — successful execution artifact; SHA-256 `2f4cfa39e59a13c53d8c08ff1189eadcd14f251ea3b1d485383ae749680a80e9`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/formchk.log` — successful execution artifact; SHA-256 `2863ccf998d1877c9925f4f856e51ebd96649a7ce43cbbf08d8f36cf3f71de59`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/input.com` — successful execution artifact; SHA-256 `a751e773aca3ec3d70cd00bad4d849ae81ea9948c4ccfad0a3d287b3d6bca3c1`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/parsed_observables.json` — successful execution artifact; SHA-256 `171abb394df11892a1b7142473988add3c8d06fc06df5ee80262dbf48bd822c0`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/status.json` — successful status record; SHA-256 `3bcc87756bcd2d8dbff3e0e333ae793ce3a20246d404953a7708c96389492b81`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/TD_2T_author_b3lyp_retry2_unbounded64g_optimized.xyz` — successful execution artifact; SHA-256 `5b8ffedfa1472076eaac07dfb3ce52a34d1f91b5d607484433101a89f13d06cf`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/collection.json` — successful execution artifact; SHA-256 `3a71f34d1b57aa3cea9dbedf61384a06d0428ba6dc13404c9db3d2d1c4917521`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/formchk.log` — successful execution artifact; SHA-256 `e41ef14c386c6674cb918e0de8255b7c30cebc3af7366edb9d364711c7107d68`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/input.com` — successful execution artifact; SHA-256 `8ade34dde65ebbc5d4ba8cc9ce54ef072f5263de13bc84a45f5c99321992fa1d`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/status.json` — successful status record; SHA-256 `3f5ec79c2baaccdff50d1073176b0b9b17715a48752a04e7fb494f6562f4521b`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_optimized.xyz` — successful execution artifact; SHA-256 `a35748799e4fe893d7dd99d10c79742d5d02dd1fa504246193bf140407f1e7d1`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/formchk.log` — successful execution artifact; SHA-256 `912687be8732b47ffa0d9026a7a6f8ee3c37d335f1a450be744c9daa95816172`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/input.com` — successful execution artifact; SHA-256 `a751e773aca3ec3d70cd00bad4d849ae81ea9948c4ccfad0a3d287b3d6bca3c1`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/parsed_observables.json` — successful execution artifact; SHA-256 `b86b9829758fde0ce6ca515ddb91649207fa90e5a32ac77665e333d11f3ec9d8`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/status.json` — successful status record; SHA-256 `c41bef7a9a13269119d50524ea60d8803444edf31631ab088f7a40218b6b202f`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/TD_2T_b3lyp_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `2d8428af8340597e0933803fc5b193b781789a6927d338db2dd137604c7eb17a`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/collection.json` — successful execution artifact; SHA-256 `7c9f166642be550d02da65eda98cd084d24dfafcbec8ea2868a99ee3e7bcde44`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/formchk.log` — successful execution artifact; SHA-256 `628b558401965b8ef09b2a1486e855490655c6264877799dfd41b6e212f27269`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/input.com` — successful execution artifact; SHA-256 `6e32e19296efe34e9dd0557507df9cb96a5993657f01624b5facbb6f6caa38ea`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/status.json` — successful status record; SHA-256 `187ccfdb16cff927ebac01a31e03aea0fa701dfda72ba396c10b9f183418541c`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/TD_2T_b3lyp_opt_freq_unbounded_recovery96g_optimized.xyz` — successful execution artifact; SHA-256 `0565d12a546dbb666651c8121a7280011a2b7c5577eaf0a5e5b2d4aee4315284`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/collection.json` — successful execution artifact; SHA-256 `6de6f9cda6f2067919b94600732da01059eb4876a20a099f71deb751596bb194`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/formchk.log` — successful execution artifact; SHA-256 `0ca94aadd8a0c6e15c3225dd421e5be57a0e4be8deffcc0df2fc23fcba77cb87`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/input.com` — successful execution artifact; SHA-256 `62af829657b7fdd233e85d1b5dee126ab9bc257ea1867d180f4908b58a33a7a5`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/status.json` — successful status record; SHA-256 `85e394c3d44a6cd7734889457986922cb9373101c8a11c54183a3f34c1677c1f`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_optimized.xyz` — successful execution artifact; SHA-256 `a5cf5bf0d2fe90aac674436a701bfcb4763923b246ba053807ea12876cfedede`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/formchk.log` — successful execution artifact; SHA-256 `e2d2a02f1a8a1068935c70b8ed12e760af9922222f12892df2621e81780ac9fa`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/input.com` — successful execution artifact; SHA-256 `d005622380bb4b91b61de5560dfd7a0152d3c4677dfedacfc0308342200bde5e`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/parsed_observables.json` — successful execution artifact; SHA-256 `7bc736b1175f9852578d6b88a40e91ceab6d1af9c387bec07e63e65be4c89ec5`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/status.json` — successful status record; SHA-256 `7dcbc6098591c701dbe9a59dec05f3e7a1c2953007099160af10479f73d7f3c2`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/TD_2T_triplets7_optimized.xyz` — successful execution artifact; SHA-256 `d13d5ed1615c0b8aa619cac120b64416214e5f4c6e0301ead436123c14fa84ac`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/formchk.log` — successful execution artifact; SHA-256 `e2a7010bb60dda32494b84f4546b0eecb0a5bd4ecb8fb203983f722190a4796f`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/input.com` — successful execution artifact; SHA-256 `eedf207248b8e774296de1a0c7503ca398b8ad02e6bfb88708bc56ad3462a184`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/parsed_observables.json` — successful execution artifact; SHA-256 `e37e1f232e4678a212928191a0f7da1de594c8ca450745624fe1deb00f0b3d38`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_author_b3lyp_retry2_unbounded64g/outputs/execution_jobs/job_f0956e17f628430b9eb8265343917efb/status.json` — successful status record; SHA-256 `3bcc87756bcd2d8dbff3e0e333ae793ce3a20246d404953a7708c96389492b81`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_author_b3lyp_retry2_unbounded64g/outputs/execution_jobs/job_f0956e17f628430b9eb8265343917efb/collection.json` — successful execution artifact; SHA-256 `3a71f34d1b57aa3cea9dbedf61384a06d0428ba6dc13404c9db3d2d1c4917521`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_author_b3lyp_retry2_unbounded64g/outputs/execution_jobs/job_f0956e17f628430b9eb8265343917efb/input.com` — successful execution artifact; SHA-256 `8ade34dde65ebbc5d4ba8cc9ce54ef072f5263de13bc84a45f5c99321992fa1d`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_author_b3lyp_retry2_unbounded64g/outputs/execution_jobs/job_f0956e17f628430b9eb8265343917efb/request.json` — successful execution artifact; SHA-256 `db903d320dc1800b6748739b447fdeba63a247b857c7fb89d2430c1708714258`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_author_b3lyp_retry2_unbounded64g/outputs/execution_jobs/job_f0956e17f628430b9eb8265343917efb/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq/outputs/execution_jobs/job_8e11c30d31224f40bbdda9c9b20949c1/status.json` — successful status record; SHA-256 `c41bef7a9a13269119d50524ea60d8803444edf31631ab088f7a40218b6b202f`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq/outputs/execution_jobs/job_8e11c30d31224f40bbdda9c9b20949c1/collection.json` — successful execution artifact; SHA-256 `7c9f166642be550d02da65eda98cd084d24dfafcbec8ea2868a99ee3e7bcde44`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq/outputs/execution_jobs/job_8e11c30d31224f40bbdda9c9b20949c1/input.com` — successful execution artifact; SHA-256 `6e32e19296efe34e9dd0557507df9cb96a5993657f01624b5facbb6f6caa38ea`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq/outputs/execution_jobs/job_8e11c30d31224f40bbdda9c9b20949c1/request.json` — successful execution artifact; SHA-256 `d1f3d144e2406b22c0dd264e36e5489a6ebf8094ec361044f388d55f16edeb13`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq/outputs/execution_jobs/job_8e11c30d31224f40bbdda9c9b20949c1/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/outputs/execution_jobs/job_eb3fe6afe476413fa1925c9af09fb834/status.json` — successful status record; SHA-256 `187ccfdb16cff927ebac01a31e03aea0fa701dfda72ba396c10b9f183418541c`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/outputs/execution_jobs/job_eb3fe6afe476413fa1925c9af09fb834/collection.json` — successful execution artifact; SHA-256 `6de6f9cda6f2067919b94600732da01059eb4876a20a099f71deb751596bb194`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/outputs/execution_jobs/job_eb3fe6afe476413fa1925c9af09fb834/input.com` — successful execution artifact; SHA-256 `62af829657b7fdd233e85d1b5dee126ab9bc257ea1867d180f4908b58a33a7a5`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/outputs/execution_jobs/job_eb3fe6afe476413fa1925c9af09fb834/request.json` — successful execution artifact; SHA-256 `a7c0626d1e263c363662c637dfb4e817eebbc0af876e46c6899cdf53bf20ec4d`
- `docs/verification/group_3/paper_3316e45a74258fb7/native_workspace/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/outputs/execution_jobs/job_eb3fe6afe476413fa1925c9af09fb834/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/status.json` — successful status record; SHA-256 `303757baff4bb046b61b587a23ee20352a48278db3962c5f44490ab0b24eccdb`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/gaussian.log` — successful execution artifact; SHA-256 `521b5de36715031c6be57299eb44d257a8b00c149fc9d448ccd61efe7a0be231`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/hpc_stdout.log` — successful execution artifact; SHA-256 `b7d48885a5bb2be6b60c8c345a924841fe282732b55cf7767d6f35e85ab19a2e`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/input.com` — successful execution artifact; SHA-256 `a751e773aca3ec3d70cd00bad4d849ae81ea9948c4ccfad0a3d287b3d6bca3c1`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/resource_adjustment.json` — successful execution artifact; SHA-256 `0b91843034285e2aa8cb6a77a5ddceec54e4f07fa8c157e3d585ae684fa170a8`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/status.json` — successful status record; SHA-256 `bc87e7503a5446581e4ae3e539d00f1643f53ded4b213b304e7a9f1c26aafc65`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/gaussian.log` — successful execution artifact; SHA-256 `fba939744e93b14041670b0c52ada73411b8df6dff06f1790ef01d1f72f99bb8`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/hpc_stdout.log` — successful execution artifact; SHA-256 `1fe499762bfa43f2aef22156a686ad856dcee21113ec6983de5abc6eaf0b28d4`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/input.com` — successful execution artifact; SHA-256 `a751e773aca3ec3d70cd00bad4d849ae81ea9948c4ccfad0a3d287b3d6bca3c1`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/resource_adjustment.json` — successful execution artifact; SHA-256 `f53b8f32b0d1e1a88462e258a44dea44f5557fa01e38109991dc9cb96068e932`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/status.json` — successful status record; SHA-256 `47fd3b435ce294b2248f3597f101ca28081c2b0da9ff010ab33ee162deafb987`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/gaussian.log` — successful execution artifact; SHA-256 `3d6387a109d64507d20b85bde39d624e1cd3b1ace245d8f2443a9ea91aff93c9`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/hpc_stdout.log` — successful execution artifact; SHA-256 `b8ef93dc83b0c64a2f62b351bb714b05d37660270282f495d51cb6dbe114ab62`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/input.com` — successful execution artifact; SHA-256 `d005622380bb4b91b61de5560dfd7a0152d3c4677dfedacfc0308342200bde5e`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/resource_adjustment.json` — successful execution artifact; SHA-256 `beb8d35689311fab53a2da8dd40b5f787f6680702549216da01306561ed56745`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/status.json` — successful status record; SHA-256 `609642b3c33a3a27d6b39186e9f2dbd2359769f70eb1d5aabc840025f1bd4372`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/gaussian.log` — successful execution artifact; SHA-256 `3679692556f26f6fab225a17676ede49b8eda83632ef93d88caed4aaf02e28ff`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/hpc_stdout.log` — successful execution artifact; SHA-256 `2250b12b2e695f7f8fc1c90b77a29acc55a6bf9f548f67c415fbded5b2b1050e`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/input.com` — successful execution artifact; SHA-256 `eedf207248b8e774296de1a0c7503ca398b8ad02e6bfb88708bc56ad3462a184`
- `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/resource_adjustment.json` — successful execution artifact; SHA-256 `aada37db9a3ead6ba018dc19c1e948d2d1f79cceec6bc525b18d6a6654e83840`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/TD_2T_b3lyp_opt_freq/status.json` — label=group_3 paper_3316e45a74258fb7 TD_2T_b3lyp_opt_freq; submitted_at=2026-08-29T16:08:27.850419+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq Int=UltraFine NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/TD_2T_b3lyp_opt_freq.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/TD_2T_b3lyp_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/TD_2T_b3lyp_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq/stderr.log`
2. `artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/status.json` — label=group_3 paper_3316e45a74258fb7 TD_2T_author_b3lyp_retry2_unbounded64g; submitted_at=2026-09-01T01:30:29.059026+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Int=UltraFine Opt=(MaxCycles=256,MaxStep=5) Freq Pop=Full NoSymm SCF=(XQC,MaxCycle=2048); command=g16 < input.com
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/TD_2T_author_b3lyp_retry2_unbounded64g.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/TD_2T_author_b3lyp_retry2_unbounded64g.fchk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/TD_2T_author_b3lyp_retry2_unbounded64g_optimized.xyz`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/collection.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/formchk.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_b3lyp_retry2_unbounded64g/stderr.log`
3. `artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/status.json` — label=group_3 paper_3316e45a74258fb7 TD_2T_b3lyp_opt_freq_unbounded_recovery96g; submitted_at=2026-09-01T10:13:25.103285+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq Int=UltraFine NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/TD_2T_b3lyp_opt_freq_unbounded_recovery96g.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/TD_2T_b3lyp_opt_freq_unbounded_recovery96g.fchk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/TD_2T_b3lyp_opt_freq_unbounded_recovery96g_optimized.xyz`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/collection.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/formchk.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_b3lyp_opt_freq_unbounded_recovery96g/stderr.log`
4. `artifacts/gaussian/TD2T_author_exact_hpc20/status.json` — label=hpc-job-18780783-516e-4ac7-b67a-af7b12042ce0
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded.fchk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_optimized.xyz`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/formchk.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/parsed_observables.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD2T_author_exact_hpc20/stdout.log`
5. `artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/status.json` — label=hpc-job-6e385649-0c06-4c2f-be4f-0df4f09975bc
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded.fchk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_optimized.xyz`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/formchk.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/parsed_observables.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/stdout.log`
6. `artifacts/gaussian/TD_2T_td7_nto/status.json` — label=hpc-job-9798d6bb-f336-4d55-86ca-fd047283e6d2
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto.fchk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_electron.cube`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_hole.cube`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_optimized.xyz`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/formchk.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/parsed_observables.json`
7. `artifacts/gaussian/TD_2T_triplets7/status.json` — label=hpc-job-def95376-9695-41f3-8fcb-31bab1f2e385
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/TD_2T_triplets7.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/TD_2T_triplets7.fchk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/TD_2T_triplets7_optimized.xyz`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/formchk.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/parsed_observables.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_triplets7/stdout.log`
8. `provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/status.json` — label=provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/status.json
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/exit_code`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/gaussian.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/sha256sums.txt`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD2T_author_exact_hpc20/1/source_input.com`
9. `provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/status.json` — label=provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/status.json
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/exit_code`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/gaussian.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/sha256sums.txt`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/1/source_input.com`
10. `provenance/qzcli_hpc/TD_2T_td7_nto/1/status.json` — label=provenance/qzcli_hpc/TD_2T_td7_nto/1/status.json
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/TD_2T_td7_nto.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/exit_code`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/gaussian.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/sha256sums.txt`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_td7_nto/1/source_input.com`
11. `provenance/qzcli_hpc/TD_2T_triplets7/1/status.json` — label=provenance/qzcli_hpc/TD_2T_triplets7/1/status.json
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/TD_2T_triplets7.chk`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/exit_code`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/gaussian.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/input.com`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/sha256sums.txt`
   - output: `docs/verification/group_3/paper_3316e45a74258fb7/provenance/qzcli_hpc/TD_2T_triplets7/1/source_input.com`

## Evaluator alignment

- Key-point IDs: `kp_ar_process_opt, kp_ar_process_states, kp_ar_result_gap, kp_ar_result_character`
- Conclusion IDs: `con_ar_final`
- Scoring-rule IDs: `r_ar_opt, r_ar_states, r_ar_gap, r_ar_char, r_ar_con`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_opt` → reference `kp_ar_process_opt`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_ar_states` → reference `kp_ar_process_states`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_ar_gap` → reference `kp_ar_result_gap`; type=numeric; unit=eV; tolerance=0.1; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_char` → reference `kp_ar_result_character`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_con` → reference `con_ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_ar_gap` / reference `kp_ar_result_gap`: target=0.34 eV; tolerance=0.1; numeric result leaves=[0.30820000000000003]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_opt` / reference `kp_ar_process_opt` / field `$.structure.object_id` / result path `$.structure.object_id` = `"TD-2T"`
- rule `r_ar_opt` / reference `kp_ar_process_opt` / field `$.structure.geometry_source` / result path `$.structure.geometry_source` = `"verification-stage OPSIN/RDKit conformer; artifacts/gaussian/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated/TD_2T_author_exact_b3lyp_631gdp_opt_freq_unbounded_hpc20_migrated_optimized.xyz"`
- rule `r_ar_opt` / reference `kp_ar_process_opt` / field `$.structure.conformer_coverage` / result path `$.structure.conformer_coverage` = `"One generated conformer; no exhaustive search."`
- rule `r_ar_opt` / reference `kp_ar_process_opt` / field `$.optimization.validation_evidence` / result path `$.optimization.validation_evidence` = `"Gaussian Opt/Freq normal termination and a nonempty zero-imaginary-frequency Hessian."`
- rule `r_ar_states` / reference `kp_ar_process_states` / field `$.excited_states.state_assignment_evidence` / result path `$.excited_states.state_assignment_evidence` = `"S1 is first singlet TD root; T1 is first triplet root in the separate matched-geometry triplet TD run."`
- rule `r_ar_gap` / reference `kp_ar_result_gap` / field `$.gap.delta_est_eV` / result path `$.gap.delta_est_eV` = `0.30820000000000003`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.method` = `"Gaussian S1 transition density, SaveNTO and cubegen hole/electron centroid integration"`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.d_index_angstrom` = `4.904347092502112`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.assessment` = `"CT-like separation"`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.distance_angstrom` = `4.904347092502112`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.hole_centroid_angstrom[0]` = `1.8313239890140647`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.hole_centroid_angstrom[1]` = `0.9341317125020752`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.hole_centroid_angstrom[2]` = `-1.4573317765793337`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.electron_centroid_angstrom[0]` = `-2.6958170815872444`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.electron_centroid_angstrom[1]` = `2.8201296726406224`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.electron_centroid_angstrom[2]` = `-1.4323152827803352`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.hole_orbital_index_1based` = `265`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.electron_orbital_index_1based` = `266`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.grid` = `"Gaussian cubegen coarse (-2), identical automatic box for the paired saved NTOs"`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.evidence[0]` = `"artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_hole.cube"`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.evidence[1]` = `"artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_electron.cube"`
- rule `r_ar_char` / reference `kp_ar_result_character` / field `$.state_character` / result path `$.state_character.evidence.evidence[2]` = `"artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto.fchk"`
- rule `r_ar_con` / reference `con_ar_final` / field `$.conclusion` / result path `$.conclusion` = `"Validated S0 and matched-geometry TD roots give S1=2.1404 eV, T1=1.8322 eV, ΔE_ST=0.3082 eV and S1 NTO D=4.9043 Å; the disclosed D>=2.0 Å rule classifies S1 as CT-like separation."`
- rule `r_ar_con` / reference `con_ar_final` / field `$.limitations` / result path `$.limitations` = `"Gas-phase isolated molecule; one conformer; D-index threshold and TD-DFT model are diagnostics rather than proof of an experimental TADF rate."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `none recorded`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — TD-2T identity, formula, charge and multiplicity.

Public input files and hashes:

- `agent_input/data/inputs/td_2t_identity.json` — SHA-256 `7bce54a20edf7eedc838a0ade3ed4a2f823f3e39a5fa8729bfc2b8bce7b0e6ad`; size=483 bytes; explicit_boundary_fields={"$.connectivity_boundary": "DCTP fused-ring acceptor substituted at positions 3, 6 and 11 by three para-N,N-diphenylamino phenyl groups; no counterions, solvent or protonation.", "$.formula": "C72H49N7", "$.ground_state_multiplicity": 1, "$.neutral_charge": 0}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_3316e45a74258fb7/verification_report.md` — verification record; SHA-256 `7c4d44ed0ee500acb12e349117c3ead1988dbf3b0993ff53e2349bf16130d6e3`
- `docs/verification/group_3/paper_3316e45a74258fb7/report/results.json` — verification record; SHA-256 `0bca157c2af4c1e35b6a8ed0f9ec998ccc7f62ea35a5c898106b6dc9aea695a0`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto.fchk` — referenced successful evidence; SHA-256 `a50b83fc49abd636965ce66c30564fdd62e4e26e42d67976d9bcfa2ec18dfba5`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_electron.cube` — referenced successful evidence; SHA-256 `683bc427370774dad25239d470307e268c4b209202032cc4c7328729320b1a38`
- `docs/verification/group_3/paper_3316e45a74258fb7/artifacts/gaussian/TD_2T_td7_nto/TD_2T_td7_nto_S1_hole.cube` — referenced successful evidence; SHA-256 `fe0cf0a3935274a8f6c15b434632208753d9545a965a32977c20ed7a1486809e`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
