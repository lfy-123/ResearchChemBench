# Verified computation reference — paper_b1467cd61ca8022d (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `success` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 6 | `CONDITIONAL` | - 论文复现结论：`CONDITIONAL`。 |
| 27 | `QUALIFIED` | 或凝聚相修正，最终严格判定为 **QUALIFIED（scope-limited）**；计算成功状态仍保持 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Rational electrolyte solvent screening for high-energy lithium metal batteries at low temperatures
- DOI: `10.1038/s41467-025-67290-7`
- Task package: `tasks/final_verified_autonomous_research/paper_b1467cd61ca8022d`
- Verification group: `docs/verification/group_4/paper_b1467cd61ca8022d`
- Paper documents: `papers/paper_b1467cd61ca8022d`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "binding_energy_eV": -2.1904573927989377,
  "candidates": [
    {
      "candidate_id": "baseline_li_tfpm_pair",
      "contacts_angstrom": {
        "Li-F_all": [
          5.682372400617897,
          6.073602191448663,
          4.964974260587259
        ],
        "Li-F_min": 4.964974260587259,
        "Li-O_A": 1.8126443839887627
      },
      "converged": true,
      "description": "initial Li near ether oxygen",
      "energy_eV": -14664.136068555803,
      "energy_hartree": -538.897060811,
      "frequency_count": 42,
      "imaginary_frequency_count": 0,
      "job_id": "job_8d7bda7a792348a0a34d02ab3d63b45d",
      "minimum_validated": true
    },
    {
      "candidate_id": "b146_chelate_side_a_optfreq",
      "contacts_angstrom": {
        "Li-F_all": [
          3.448127268509241,
          3.9323223774037146,
          1.8453724478470463
        ],
        "Li-F_min": 1.8453724478470463,
        "Li-O_A": 1.8530762669887604
      },
      "converged": true,
      "description": "Li placed between ether O and one F face (chelate A)",
      "energy_eV": -14664.799388545312,
      "energy_hartree": -538.921437371,
      "frequency_count": 42,
      "imaginary_frequency_count": 0,
      "job_id": "job_ea6ebe21bb9145a9b83b3500b3079310",
      "minimum_validated": true
    },
    {
      "candidate_id": "b146_chelate_side_b_optfreq",
      "contacts_angstrom": {
        "Li-F_all": [
          3.44782655576379,
          3.9322608755617936,
          1.8452627765838663
        ],
        "Li-F_min": 1.8452627765838663,
        "Li-O_A": 1.853033402933957
      },
      "converged": true,
      "description": "opposite Li O/F chelation orientation (chelate B)",
      "energy_eV": -14664.799371538196,
      "energy_hartree": -538.921436746,
      "frequency_count": 42,
      "imaginary_frequency_count": 0,
      "job_id": "job_98cc6cd3e70b4eb0870cd3ca4897d1bf",
      "minimum_validated": true
    },
    {
      "candidate_id": "b146_f_only_optfreq",
      "contacts_angstrom": {
        "Li-F_all": [
          1.7884795067237984,
          3.5297213247260757,
          3.298047557312356
        ],
        "Li-F_min": 1.7884795067237984,
        "Li-O_A": 5.937517171821064
      },
      "converged": true,
      "description": "Li initially near a fluorine atom without O contact",
      "energy_eV": -14663.769451644188,
      "energy_hartree": -538.883587888,
      "frequency_count": 42,
      "imaginary_frequency_count": 0,
      "job_id": "job_445032e020d74258942d6bfd72e02fc9",
      "minimum_validated": true
    },
    {
      "candidate_id": "b146_remote_optfreq",
      "contacts_angstrom": {
        "Li-F_all": [
          3.505235063265373,
          3.50526130984282,
          1.7806976072256064
        ],
        "Li-F_min": 1.7806976072256064,
        "Li-O_A": 6.519675813918128
      },
      "converged": true,
      "description": "remote Li placement outside O/F contact region",
      "energy_eV": -14663.795769843891,
      "energy_hartree": -538.884555064,
      "frequency_count": 42,
      "imaginary_frequency_count": 0,
      "job_id": "job_d21dd7d8ff5148338db4dbefe434e252",
      "minimum_validated": true
    }
  ],
  "conclusion": "The selected gas-phase minimum has Eb=-2.190457 eV under Eb=E(complex)−E(Li+)−E(TFPM). The computed contact pattern provides a bounded independent test of the proposed complementary Li–O/Li–F stabilization, without extrapolating to condensed-phase behavior.",
  "coverage": {
    "generation": "Five high-level orientations: O-near baseline, two complementary O/F chelation faces, F-only, and remote; an independent B3LYP/6-31G(d) coverage orientation was also retained.",
    "stopping": "The finite declared orientation set was exhausted; optimized candidates were deduplicated by 0.20 Å Li-O and nearest-Li-F contact signatures before energy selection."
  },
  "energies": {
    "complex_eV": -14664.799388545312,
    "lithium_eV": -198.23271163314075,
    "tfpm_eV": -14464.376219519374
  },
  "geometry_interpretation": "Selected optimized contacts are Li-O=1.853 Å and nearest Li-F=1.845 Å. These measured contacts determine whether the minimum is O-dominated, F-assisted, or remote; they do not by themselves establish bulk chelation.",
  "limitations": "Gas-phase electronic binding omits counterions, solvent, entropy and bulk packing; no global conformer search is claimed; basis-set superposition and thermal corrections are not applied.",
  "method": {
    "model_chemistry": "B3LYP/6-311+G(d,p) Opt(Tight)+Freq; neutral TFPM and Li+ reference at the same level; gas phase",
    "software": "Gaussian 16 C.01 native"
  },
  "selected_candidate_id": "b146_chelate_side_a_optfreq",
  "selected_candidate_rationale": "Selected b146_chelate_side_a_optfreq as the lowest electronic-energy member of the deduplicated, zero-imaginary-frequency candidate set.",
  "status": "success",
  "uncertainty": "Coverage uncertainty is represented by the explicit five-orientation set and lower-level coverage calculation; model, basis-set, gas-phase and conformer limitations remain.",
  "validation": {
    "details": "Every declared candidate completed Gaussian Opt/Freq with normal termination and zero imaginary frequencies; isolated TFPM likewise passed Opt/Freq and Li+ passed the same-level SP.",
    "frequency_or_equivalent": true
  }
}
```

Paper/SI document hashes:

- `papers/paper_b1467cd61ca8022d/documents/main.pdf` — SHA-256 `5d8206d63bf9546ab21cd825a8b6401671658eb2b405a2a6f4d2512b9079a058` (declared_match=True)
- `papers/paper_b1467cd61ca8022d/documents/supplementary_001.pdf` — SHA-256 `97ee5d6bc0d695d873487d596b7316d6fad02bd9d22b35244bb2358102520aea` (declared_match=True)
- `papers/paper_b1467cd61ca8022d/documents/supplementary_002.pdf` — SHA-256 `ad49080ae5954b466597b24007c956dfe5dbe89b3778a4d4f51856128a596048` (declared_match=True)

Report evidence lines retained:

- 五个高层候选、TFPM 片段和 Li⁺ 参考全部正常终止；候选均 Opt/Freq 零虚频。按最终 Li–O/nearest-Li–F 接触（0.20 Å 阈值）去重后选择最低电子能候选 **b146_chelate_side_a_optfreq**。
- 五个声明候选均已完成 Opt/Freq 且零虚频，最低能候选和 Li–O/Li–F 接触证据已由

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **80**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/status.json` — successful status record; SHA-256 `9b34d53b0a4933e994814133479e374ce3e7f6fc68f5d7dbc56acfd843bc1476`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/b146_chelate_side_a_optfreq_parsed.json` — successful execution artifact; SHA-256 `8927098b1f3d418f55b023bd1c0e1e35712dc0997e6eeb4e38d48f394a42d796`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/collection.json` — successful execution artifact; SHA-256 `bfd9b0ca5f718a0d936aa2f837de7f4181ce9ec4bcb78a0c4fb2ce235843d996`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/input.com` — successful execution artifact; SHA-256 `6cce882a48fa1dbcc38b8d97f0f4ca26269b0eac96cd895d4902f79215f33f4e`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/status.json` — successful status record; SHA-256 `16c66591226d9f50ef01f41512341f46a61ba03ea0002b59848303e6aa53500c`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/b146_chelate_side_b_optfreq_parsed.json` — successful execution artifact; SHA-256 `c5984e84425d1c807612d08640872f477c1c1893376d2edf70568dd2190955c6`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/collection.json` — successful execution artifact; SHA-256 `3b96f24efd7d1b1b0561d06ce91610c44375c6a42579ca28ba3f0546b91495ff`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/input.com` — successful execution artifact; SHA-256 `1f30b7c2da5c5380fec6b8ff7eb8463a1216877b1f89b449d1c4a8de3da2443f`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/status.json` — successful status record; SHA-256 `365187eae2dd4523852f4da290d2aea5379ccd04020424105e6ea4a976427422`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/b146_f_only_optfreq_parsed.json` — successful execution artifact; SHA-256 `576db4685b4c71095af9b9a294f758129fe0f0ea5b44787e581eaacb4285aa7d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/collection.json` — successful execution artifact; SHA-256 `07bf2588776e7ab5879891fe0fa99ce3c76a7b2b2b518921ddd0157efb525abe`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/input.com` — successful execution artifact; SHA-256 `5010184e93a6ddcef3ee74bb3ee71d26c79b37164582fd4384462d7bbc0157ee`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/status.json` — successful status record; SHA-256 `7e44ebc137a44dba188b968e3ba45f512020f49c61a2ff937e593265e1ea473a`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/b146_li_plus_sp_parsed.json` — successful execution artifact; SHA-256 `aad48dbebfb97e82ca575f27d9a4ae1af65dc2df58ebad76e1ec615309131a9d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/collection.json` — successful execution artifact; SHA-256 `7a999a3939ebb3fcd3fc7743e0d75e393748563ab6e0d6536f31e2995fec442a`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/input.com` — successful execution artifact; SHA-256 `e800da8602af8613b8ce230b0f3b860589fb97ea2344dcf583fa2a23ce27352d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/status.json` — successful status record; SHA-256 `1d7071741251ca1b158b8c4960d1040a11f2545c6329e85c203fa501e0064e38`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/b146_remote_optfreq_parsed.json` — successful execution artifact; SHA-256 `22c46f5be8fe2bc941c7e4894f9e2369c54f9f61053fa2a0a643bfaf524d4639`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/collection.json` — successful execution artifact; SHA-256 `99cbf8d7ae0d73a5587855880364a418897bcbfc5fcd7d1b57d258bc027fa08f`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/input.com` — successful execution artifact; SHA-256 `2c4af768683353cfeff39596c5a59f652458b6222e56b721386f4629360a9f24`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/status.json` — successful status record; SHA-256 `f2f77aeda77a2025cf130b4b0d3de24da8ca263447b42546c9c38dcc96d6c53b`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/b146_tfpm_fragment_optfreq_parsed.json` — successful execution artifact; SHA-256 `3671a0c169a174cb2a5ceea433b3aeb07f2444a763c422fdeca9be7daf0ddf9d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/collection.json` — successful execution artifact; SHA-256 `158cca2679aa0a73e029ce3d6ebb49b9f186a824c917d6d37a3d0825b47d99b5`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/input.com` — successful execution artifact; SHA-256 `ab13f81fe413b69cde4078060b4f98f5b7a2b21980e282d60e2bb75ed11ea7de`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/status.json` — successful status record; SHA-256 `ee48483ab4291637e9e6dfedb86525ba2f95602c8d630a6b6a73d7d84293604a`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/baseline_li_tfpm_pair_parsed.json` — successful execution artifact; SHA-256 `17edd3d2c1af1af91558953129264fccf6a4bdda73f6efb6a5f3c76e369faac2`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/collection.json` — successful execution artifact; SHA-256 `32ae7270c443533373ab6f299fff08c5ddab093f4b1cb47f8b5f6257fe31092d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/final.xyz` — successful execution artifact; SHA-256 `9cc17c04c9179d5905e1c2a3482679da0464a2b1d6e1e7ff7cf5584321b4616d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/final.xyz.json` — successful execution artifact; SHA-256 `4665450aee1207f9f7286be577614874edc906bc7e122441e205a92b3def9520`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/status.json` — successful status record; SHA-256 `1ed223efc911c26df3b2c78163015070b571c97e2fa7b90ac73c9041ef1bd4b4`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/collection.json` — successful execution artifact; SHA-256 `18410ba49c97081d1fc387c8946be3df922bea3a4f19f275e58318dae1bd38a0`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/coverage_li_tfpm_pair_parsed.json` — successful execution artifact; SHA-256 `a6fb2615eee36d28c023e8b583937d4d32dbe87c31727ab673016ffca66eac77`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/input.com` — successful execution artifact; SHA-256 `083a1dc337ac9851c6fad22dd46f3c56f8d6f0d41dbe4519f115c2db1312c118`
- `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_445032e020d74258942d6bfd72e02fc9/status.json` — successful status record; SHA-256 `365187eae2dd4523852f4da290d2aea5379ccd04020424105e6ea4a976427422`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_445032e020d74258942d6bfd72e02fc9/collection.json` — successful execution artifact; SHA-256 `07bf2588776e7ab5879891fe0fa99ce3c76a7b2b2b518921ddd0157efb525abe`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_445032e020d74258942d6bfd72e02fc9/input.com` — successful execution artifact; SHA-256 `5010184e93a6ddcef3ee74bb3ee71d26c79b37164582fd4384462d7bbc0157ee`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_445032e020d74258942d6bfd72e02fc9/request.json` — successful execution artifact; SHA-256 `6872afd280024437afd05cb800b88666a8e2e2725d0511bd08fb41018aa9a9d7`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_445032e020d74258942d6bfd72e02fc9/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8c3876aa9d75482189e9cf9977570cd2/status.json` — successful status record; SHA-256 `7e44ebc137a44dba188b968e3ba45f512020f49c61a2ff937e593265e1ea473a`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8c3876aa9d75482189e9cf9977570cd2/collection.json` — successful execution artifact; SHA-256 `7a999a3939ebb3fcd3fc7743e0d75e393748563ab6e0d6536f31e2995fec442a`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8c3876aa9d75482189e9cf9977570cd2/input.com` — successful execution artifact; SHA-256 `e800da8602af8613b8ce230b0f3b860589fb97ea2344dcf583fa2a23ce27352d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8c3876aa9d75482189e9cf9977570cd2/request.json` — successful execution artifact; SHA-256 `450444bfaff5555b8dcc377f90ee7981e3c582e9e06b2eaf7389ac3a4372dfe9`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8c3876aa9d75482189e9cf9977570cd2/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8d7bda7a792348a0a34d02ab3d63b45d/status.json` — successful status record; SHA-256 `ee48483ab4291637e9e6dfedb86525ba2f95602c8d630a6b6a73d7d84293604a`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8d7bda7a792348a0a34d02ab3d63b45d/collection.json` — successful execution artifact; SHA-256 `32ae7270c443533373ab6f299fff08c5ddab093f4b1cb47f8b5f6257fe31092d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8d7bda7a792348a0a34d02ab3d63b45d/input.com` — successful execution artifact; SHA-256 `66e4d981efe52300f852b82fe1d5f9129e66e60c90931df50374d6ab901ff863`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8d7bda7a792348a0a34d02ab3d63b45d/request.json` — successful execution artifact; SHA-256 `24b913545d7ad05e583a7a0b1f11c7117f3103fd8d530a4b4120edfdc3df4f66`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_8d7bda7a792348a0a34d02ab3d63b45d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_98cc6cd3e70b4eb0870cd3ca4897d1bf/status.json` — successful status record; SHA-256 `16c66591226d9f50ef01f41512341f46a61ba03ea0002b59848303e6aa53500c`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_98cc6cd3e70b4eb0870cd3ca4897d1bf/collection.json` — successful execution artifact; SHA-256 `3b96f24efd7d1b1b0561d06ce91610c44375c6a42579ca28ba3f0546b91495ff`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_98cc6cd3e70b4eb0870cd3ca4897d1bf/input.com` — successful execution artifact; SHA-256 `1f30b7c2da5c5380fec6b8ff7eb8463a1216877b1f89b449d1c4a8de3da2443f`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_98cc6cd3e70b4eb0870cd3ca4897d1bf/request.json` — successful execution artifact; SHA-256 `d8ad39f0fc483e614240256997e3a0d3faaa73650e707e70c7b5bf8ca7fd883f`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_98cc6cd3e70b4eb0870cd3ca4897d1bf/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_bc9c74a78eb04017be5ccd246e20f253/status.json` — successful status record; SHA-256 `f2f77aeda77a2025cf130b4b0d3de24da8ca263447b42546c9c38dcc96d6c53b`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_bc9c74a78eb04017be5ccd246e20f253/collection.json` — successful execution artifact; SHA-256 `158cca2679aa0a73e029ce3d6ebb49b9f186a824c917d6d37a3d0825b47d99b5`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_bc9c74a78eb04017be5ccd246e20f253/input.com` — successful execution artifact; SHA-256 `ab13f81fe413b69cde4078060b4f98f5b7a2b21980e282d60e2bb75ed11ea7de`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_bc9c74a78eb04017be5ccd246e20f253/request.json` — successful execution artifact; SHA-256 `de9d790f71596e35bc94c3b604f802550dce01b9edf5d5fc0f9da4f4249a1bfd`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_bc9c74a78eb04017be5ccd246e20f253/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d21dd7d8ff5148338db4dbefe434e252/status.json` — successful status record; SHA-256 `1d7071741251ca1b158b8c4960d1040a11f2545c6329e85c203fa501e0064e38`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d21dd7d8ff5148338db4dbefe434e252/collection.json` — successful execution artifact; SHA-256 `99cbf8d7ae0d73a5587855880364a418897bcbfc5fcd7d1b57d258bc027fa08f`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d21dd7d8ff5148338db4dbefe434e252/input.com` — successful execution artifact; SHA-256 `2c4af768683353cfeff39596c5a59f652458b6222e56b721386f4629360a9f24`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d21dd7d8ff5148338db4dbefe434e252/request.json` — successful execution artifact; SHA-256 `1694ea9c5158b403ec10f6edfd42b298167184f6f3386ce597a3178367510148`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d21dd7d8ff5148338db4dbefe434e252/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d4000a3ed11144f786690d6571f0f6e8/status.json` — successful status record; SHA-256 `1ed223efc911c26df3b2c78163015070b571c97e2fa7b90ac73c9041ef1bd4b4`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d4000a3ed11144f786690d6571f0f6e8/collection.json` — successful execution artifact; SHA-256 `18410ba49c97081d1fc387c8946be3df922bea3a4f19f275e58318dae1bd38a0`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d4000a3ed11144f786690d6571f0f6e8/input.com` — successful execution artifact; SHA-256 `083a1dc337ac9851c6fad22dd46f3c56f8d6f0d41dbe4519f115c2db1312c118`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d4000a3ed11144f786690d6571f0f6e8/request.json` — successful execution artifact; SHA-256 `25abf7a428bb64f8621e4e4d9f5abeef965372bc119c19aeee13d67f5599687d`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_d4000a3ed11144f786690d6571f0f6e8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_ea6ebe21bb9145a9b83b3500b3079310/status.json` — successful status record; SHA-256 `9b34d53b0a4933e994814133479e374ce3e7f6fc68f5d7dbc56acfd843bc1476`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_ea6ebe21bb9145a9b83b3500b3079310/collection.json` — successful execution artifact; SHA-256 `bfd9b0ca5f718a0d936aa2f837de7f4181ce9ec4bcb78a0c4fb2ce235843d996`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_ea6ebe21bb9145a9b83b3500b3079310/input.com` — successful execution artifact; SHA-256 `6cce882a48fa1dbcc38b8d97f0f4ca26269b0eac96cd895d4902f79215f33f4e`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_ea6ebe21bb9145a9b83b3500b3079310/request.json` — successful execution artifact; SHA-256 `0110f46efef072d2f65353e39b67a289a31428d135719d85290664f7b17d80ef`
- `docs/verification/group_4/paper_b1467cd61ca8022d/native_workspace_batch/outputs/execution_jobs/job_ea6ebe21bb9145a9b83b3500b3079310/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/coverage_li_tfpm_pair/status.json` — label=group_4 paper_b1467cd61ca8022d coverage_li_tfpm_pair; submitted_at=2026-08-29T17:10:14.354253+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt=(Tight,MaxCycles=200) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/coverage_li_tfpm_pair.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/coverage_li_tfpm_pair_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/coverage_li_tfpm_pair/stdout.log`
2. `artifacts/gaussian_batch/baseline_li_tfpm_pair/status.json` — label=group_4 paper_b1467cd61ca8022d baseline_li_tfpm_pair; submitted_at=2026-08-29T17:12:20.326695+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(Tight,MaxCycles=200) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/baseline_li_tfpm_pair.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/baseline_li_tfpm_pair_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/final.xyz`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/final.xyz.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/baseline_li_tfpm_pair/stdout.log`
3. `artifacts/gaussian_batch/b146_chelate_side_a_optfreq/status.json` — label=group_4 paper_b1467cd61ca8022d b146_chelate_side_a_optfreq; submitted_at=2026-08-30T02:21:51.206502+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/b146_chelate_side_a_optfreq.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/b146_chelate_side_a_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_a_optfreq/stdout.log`
4. `artifacts/gaussian_batch/b146_chelate_side_b_optfreq/status.json` — label=group_4 paper_b1467cd61ca8022d b146_chelate_side_b_optfreq; submitted_at=2026-08-30T02:21:51.241073+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/b146_chelate_side_b_optfreq.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/b146_chelate_side_b_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_chelate_side_b_optfreq/stdout.log`
5. `artifacts/gaussian_batch/b146_f_only_optfreq/status.json` — label=group_4 paper_b1467cd61ca8022d b146_f_only_optfreq; submitted_at=2026-08-30T02:21:51.274296+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/b146_f_only_optfreq.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/b146_f_only_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_f_only_optfreq/stdout.log`
6. `artifacts/gaussian_batch/b146_remote_optfreq/status.json` — label=group_4 paper_b1467cd61ca8022d b146_remote_optfreq; submitted_at=2026-08-30T02:21:51.306801+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/b146_remote_optfreq.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/b146_remote_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_remote_optfreq/stdout.log`
7. `artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/status.json` — label=group_4 paper_b1467cd61ca8022d b146_tfpm_fragment_optfreq; submitted_at=2026-08-30T02:21:51.340517+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/b146_tfpm_fragment_optfreq.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/b146_tfpm_fragment_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_tfpm_fragment_optfreq/stdout.log`
8. `artifacts/gaussian_batch/b146_li_plus_sp/status.json` — label=group_4 paper_b1467cd61ca8022d b146_li_plus_sp; submitted_at=2026-08-30T02:21:51.382269+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-311+G(d,p) SP NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/b146_li_plus_sp.chk`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/b146_li_plus_sp_parsed.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/collection.json`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/input.com`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/stderr.log`
   - output: `docs/verification/group_4/paper_b1467cd61ca8022d/artifacts/gaussian_batch/b146_li_plus_sp/stdout.log`

## Evaluator alignment

- Key-point IDs: `ar_process_minimum, ar_process_coverage, ar_result_binding, ar_result_conclusion`
- Conclusion IDs: `ar_final`
- Scoring-rule IDs: `ar_r1, ar_r2, ar_r3, ar_r4, ar_r5`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `ar_r1` → reference `ar_process_minimum`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert check of process evidence; evaluator_target_present=False
- rule `ar_r2` → reference `ar_process_coverage`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r3` → reference `ar_result_binding`; type=numeric; unit=eV; tolerance=0.25; comparison=absolute difference; evaluator_target_present=True
- rule `ar_r4` → reference `ar_result_conclusion`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r5` → reference `ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `ar_r3` / reference `ar_result_binding`: target=-2.16 eV; tolerance=0.25; numeric result leaves=[-2.1904573927989377]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `ar_r1` / reference `ar_process_minimum` / field `$.validation` / result path `$.validation.frequency_or_equivalent` = `true`
- rule `ar_r1` / reference `ar_process_minimum` / field `$.validation` / result path `$.validation.details` = `"Every declared candidate completed Gaussian Opt/Freq with normal termination and zero imaginary frequencies; isolated TFPM likewise passed Opt/Freq and Li+ passed the same-level SP."`
- rule `ar_r1` / reference `ar_process_minimum` / field `$.energies` / result path `$.energies.complex_eV` = `-14664.799388545312`
- rule `ar_r1` / reference `ar_process_minimum` / field `$.energies` / result path `$.energies.lithium_eV` = `-198.23271163314075`
- rule `ar_r1` / reference `ar_process_minimum` / field `$.energies` / result path `$.energies.tfpm_eV` = `-14464.376219519374`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].candidate_id` = `"baseline_li_tfpm_pair"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].description` = `"initial Li near ether oxygen"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].converged` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].minimum_validated` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].energy_hartree` = `-538.897060811`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].frequency_count` = `42`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].imaginary_frequency_count` = `0`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].job_id` = `"job_8d7bda7a792348a0a34d02ab3d63b45d"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].contacts_angstrom.Li-O_A` = `1.8126443839887627`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].contacts_angstrom.Li-F_min` = `4.964974260587259`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].contacts_angstrom.Li-F_all[0]` = `5.682372400617897`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].contacts_angstrom.Li-F_all[1]` = `6.073602191448663`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].contacts_angstrom.Li-F_all[2]` = `4.964974260587259`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[0].energy_eV` = `-14664.136068555803`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].candidate_id` = `"b146_chelate_side_a_optfreq"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].description` = `"Li placed between ether O and one F face (chelate A)"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].converged` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].minimum_validated` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].energy_hartree` = `-538.921437371`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].frequency_count` = `42`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].imaginary_frequency_count` = `0`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].job_id` = `"job_ea6ebe21bb9145a9b83b3500b3079310"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].contacts_angstrom.Li-O_A` = `1.8530762669887604`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].contacts_angstrom.Li-F_min` = `1.8453724478470463`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].contacts_angstrom.Li-F_all[0]` = `3.448127268509241`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].contacts_angstrom.Li-F_all[1]` = `3.9323223774037146`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].contacts_angstrom.Li-F_all[2]` = `1.8453724478470463`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[1].energy_eV` = `-14664.799388545312`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].candidate_id` = `"b146_chelate_side_b_optfreq"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].description` = `"opposite Li O/F chelation orientation (chelate B)"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].converged` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].minimum_validated` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].energy_hartree` = `-538.921436746`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].frequency_count` = `42`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].imaginary_frequency_count` = `0`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].job_id` = `"job_98cc6cd3e70b4eb0870cd3ca4897d1bf"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].contacts_angstrom.Li-O_A` = `1.853033402933957`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].contacts_angstrom.Li-F_min` = `1.8452627765838663`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].contacts_angstrom.Li-F_all[0]` = `3.44782655576379`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].contacts_angstrom.Li-F_all[1]` = `3.9322608755617936`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].contacts_angstrom.Li-F_all[2]` = `1.8452627765838663`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[2].energy_eV` = `-14664.799371538196`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].candidate_id` = `"b146_f_only_optfreq"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].description` = `"Li initially near a fluorine atom without O contact"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].converged` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].minimum_validated` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].energy_hartree` = `-538.883587888`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].frequency_count` = `42`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].imaginary_frequency_count` = `0`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].job_id` = `"job_445032e020d74258942d6bfd72e02fc9"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].contacts_angstrom.Li-O_A` = `5.937517171821064`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].contacts_angstrom.Li-F_min` = `1.7884795067237984`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].contacts_angstrom.Li-F_all[0]` = `1.7884795067237984`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].contacts_angstrom.Li-F_all[1]` = `3.5297213247260757`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].contacts_angstrom.Li-F_all[2]` = `3.298047557312356`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[3].energy_eV` = `-14663.769451644188`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].candidate_id` = `"b146_remote_optfreq"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].description` = `"remote Li placement outside O/F contact region"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].converged` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].minimum_validated` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].energy_hartree` = `-538.884555064`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].frequency_count` = `42`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].imaginary_frequency_count` = `0`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].job_id` = `"job_d21dd7d8ff5148338db4dbefe434e252"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].contacts_angstrom.Li-O_A` = `6.519675813918128`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].contacts_angstrom.Li-F_min` = `1.7806976072256064`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].contacts_angstrom.Li-F_all[0]` = `3.505235063265373`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].contacts_angstrom.Li-F_all[1]` = `3.50526130984282`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].contacts_angstrom.Li-F_all[2]` = `1.7806976072256064`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.candidates` / result path `$.candidates[4].energy_eV` = `-14663.795769843891`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.coverage` / result path `$.coverage.generation` = `"Five high-level orientations: O-near baseline, two complementary O/F chelation faces, F-only, and remote; an independent B3LYP/6-31G(d) coverage orientation was also retained."`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.coverage` / result path `$.coverage.stopping` = `"The finite declared orientation set was exhausted; optimized candidates were deduplicated by 0.20 Å Li-O and nearest-Li-F contact signatures before energy selection."`
- rule `ar_r3` / reference `ar_result_binding` / field `$.binding_energy_eV` / result path `$.binding_energy_eV` = `-2.1904573927989377`
- rule `ar_r4` / reference `ar_result_conclusion` / field `$.conclusion` / result path `$.conclusion` = `"The selected gas-phase minimum has Eb=-2.190457 eV under Eb=E(complex)−E(Li+)−E(TFPM). The computed contact pattern provides a bounded independent test of the proposed complementary Li–O/Li–F stabilization, without extrapolating to conde..."`
- rule `ar_r4` / reference `ar_result_conclusion` / field `$.limitations` / result path `$.limitations` = `"Gas-phase electronic binding omits counterions, solvent, entropy and bulk packing; no global conformer search is claimed; basis-set superposition and thermal corrections are not applied."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Explicit TFPM connectivity and charge/state definitions for the isolated Li+-TFPM system.

Public input files and hashes:

- `agent_input/data/inputs/tfpm_system.json` — SHA-256 `ec3e75b3a9a18d66d85584f5a2e29180669e154a761d798850e7b1513737f006`; size=503 bytes; explicit_boundary_fields={"$.complex_charge": 1, "$.complex_multiplicity": 1, "$.lithium_charge": 1, "$.lithium_multiplicity": 1, "$.solvent_name": "3,3,3-trifluoropropyl-1-methyl ether (TFPM)", "$.tfpm_charge": 0, "$.tfpm_multiplicity": 1, "$.tfpm_smiles": "COCCC(F)(F)F"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_4/paper_b1467cd61ca8022d/verification_report.md` — verification record; SHA-256 `d2022aef627de9db2973bdb87d6634f6a69d31680b9c77ba6b43c7feb218a2d5`
- `docs/verification/group_4/paper_b1467cd61ca8022d/report/results.json` — verification record; SHA-256 `5e348c6924f771dfeb26599003e0b1cfb8461d7eecc19eb0ca62f74240f1cb1f`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
