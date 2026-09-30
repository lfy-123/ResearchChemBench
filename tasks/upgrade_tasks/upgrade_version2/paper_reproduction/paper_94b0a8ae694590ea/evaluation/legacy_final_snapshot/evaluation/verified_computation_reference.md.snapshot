# Verified computation reference — paper_94b0a8ae694590ea (paper_reproduction)

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
| 5 | `PASS` | 任务包直接提供三套 SI-derived XYZ 身份（2BT-TTA、2BF-TTA、2(C8Ph)-TTA）。两次恢复作业已正常终止并消除原始软虚频/运行中断；三套 B3LYP/6-31G(d) Opt/Freq 均为零虚频，HOMO/LUMO 已解析，排序和 evaluator 语义规则全部闭合，最终严格判定为 **PASS**。 |
| 54 | `PASS` | 本篇三套作者路线端点、HOMO/LUMO 排序和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。 |
| 65 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 report/results.json、artifacts/gaussian/ 和 provenance/。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Thermoelectric Composites of Single-Walled Carbon Nanotubes with Long-Alkylphenyl-Substituted 2,6-bis(4-Octylphenyl)thieno[2′,3′:4,5]thieno[3,2-b]thieno[2,3-d]thiophene
- DOI: `10.1021/acsami.5c23007`
- Task package: `tasks/final_verified_paper_reproduction/paper_94b0a8ae694590ea`
- Verification group: `docs/verification/group_3/paper_94b0a8ae694590ea`
- Paper documents: `papers/paper_94b0a8ae694590ea`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "completion_status": "complete",
  "conclusion": "The frontier-level ordering is reported directly from the three validated isolated-molecule calculations; this is qualitative alignment evidence and does not model explicit SWCNT charge transfer.",
  "coverage": "Exactly the three supplied XYZ structures; no additional conformers.",
  "limitations": "Gas-phase isolated molecules; method and conformer dependent; HOMO/LUMO alignment is not a charge-transfer calculation.",
  "molecules": [
    {
      "charge": 0,
      "homo_eV": -5.1263528295695,
      "lumo_eV": -2.0394933094975003,
      "multiplicity": 1,
      "name": "2BT-TTA",
      "status": "validated",
      "units": "eV",
      "validation_evidence": "Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2bt_tight_min_retry/stdout.log"
    },
    {
      "charge": 0,
      "homo_eV": -5.002541027592001,
      "lumo_eV": -2.0770450208665,
      "multiplicity": 1,
      "name": "2BF-TTA",
      "status": "validated",
      "units": "eV",
      "validation_evidence": "Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2bf/stdout.log"
    },
    {
      "charge": 0,
      "homo_eV": -4.9900237904689995,
      "lumo_eV": -1.645200340123,
      "multiplicity": 1,
      "name": "2(C8Ph)-TTA",
      "status": "validated",
      "units": "eV",
      "validation_evidence": "Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2c8_runtime_retry48g/stdout.log"
    }
  ],
  "ordering": "2BT-TTA HOMO=-5.1264 eV, LUMO=-2.0395 eV; 2BF-TTA HOMO=-5.0025 eV, LUMO=-2.0770 eV; 2(C8Ph)-TTA HOMO=-4.9900 eV, LUMO=-1.6452 eV",
  "stopping_rule": "Stopped after all three supplied structures were frequency-validated and frontier levels parsed.",
  "validation": "All three supplied neutral singlets completed B3LYP/6-31G(d,p) Opt/Freq with zero imaginary frequencies; frontier levels parsed from final alpha MO block."
}
```

Paper/SI document hashes:

- `papers/paper_94b0a8ae694590ea/documents/main.pdf` — SHA-256 `9fe1fcd47f0da4b843db4f058e7482a4ca3049b1e17b0a3117b6c4c7328f130d` (declared_match=True)
- `papers/paper_94b0a8ae694590ea/documents/supplementary_001.pdf` — SHA-256 `3a0f1cd4f04cb734daeb4c1cb4520edca7343964e00d8a594022193b87f659a9` (declared_match=True)

Report evidence lines retained:

- 任务包直接提供三套 SI-derived XYZ 身份（2BT-TTA、2BF-TTA、2(C8Ph)-TTA）。两次恢复作业已正常终止并消除原始软虚频/运行中断；三套 B3LYP/6-31G(d) Opt/Freq 均为零虚频，HOMO/LUMO 已解析，排序和 evaluator 语义规则全部闭合，最终严格判定为 **PASS**。
- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |
- 独立计算完成后才读取 evaluator 对照；三套作者结构、零虚频、HOMO/LUMO 和 2(C8Ph)-TTA 双能级最高的排序均已由原始输出闭合并与 evaluator 一致。
- 本篇三套作者路线端点、HOMO/LUMO 排序和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **80**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/status.json` — successful status record; SHA-256 `d5648ce0920929271548288e187c306980c4993b89776a9e13ce5ec54e598cac`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/collection.json` — successful execution artifact; SHA-256 `e47cc0122d39e8f3488e6cfaa2a53ceca7707e41b99fe1d004881e163b9c2679`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/formchk.log` — successful execution artifact; SHA-256 `a0552277e32686174e135bdbf4cbf8333d92f3ff0ef0d7ec1b9b991f17fd7d37`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/input.com` — successful execution artifact; SHA-256 `603f1bc25269f67271fba7c00dc09b369db3d2085ac138d9c16832b83bf4dad4`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/parsed_observables.json` — successful execution artifact; SHA-256 `95a5bf2c60a529c969b9453a2baf197e4f89effbf855b32241d954bdd7f8ca13`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/status.json` — successful status record; SHA-256 `12e986ef6e58acac06dd116e411063c051022b2046d83c497812794e1dc30b2a`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/collection.json` — successful execution artifact; SHA-256 `e5c8527a64306c4b237fc916f79e29dcce4e1034af57849e292486ef08dd0b50`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/formchk.log` — successful execution artifact; SHA-256 `a245994a3d5d2bcb1f28c31ec0fc6828a827766f60a9fad9d7bfc3ae0f214db9`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/input.com` — successful execution artifact; SHA-256 `d62c6e81f506310bb5d49569d1725c71cdb839f7596e931b8e0dccdf233fec00`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/parsed_observables.json` — successful execution artifact; SHA-256 `d3261c036ab74aca8ee06bde0cc5a8166cdfe7018d2c2ac28bf7a2818112f04b`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/status.json` — successful status record; SHA-256 `9f2f67b6952ae8aaba6f6ed64fc8505e35318b266fa28021ad3e83db78dd2980`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/collection.json` — successful execution artifact; SHA-256 `242609bd761972ba84fd3bea84febba6ba83d928c261f918fe80eaafd02a15ed`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/formchk.log` — successful execution artifact; SHA-256 `760381695d587f0f7251ac6e70bf6fc8e147809aa7617cea63ba26d1ccc21a70`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/input.com` — successful execution artifact; SHA-256 `1613d22f9c1785f24b6485294af97126b427f789e59c2066eac11bf84ff3a324`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/parsed_observables.json` — successful execution artifact; SHA-256 `24cef6c4c41c7a07439699b3790531c7ef9c1bba9387b0305122e5ee1d3f7453`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/status.json` — successful status record; SHA-256 `62cf4c2493eb9ff1961073ad07825ae22101720d755cf3e47748d4188917d968`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/collection.json` — successful execution artifact; SHA-256 `631e8d3124cb45c327e47b54b57cd4fc27f0892342d2355e941ccad77abed025`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/formchk.log` — successful execution artifact; SHA-256 `380f9fe4fe2427b0e9c35a827caa4d11ab3b34372eac6a78017fbd80951b0672`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/input.com` — successful execution artifact; SHA-256 `ecaf7ac42cb39312d8f7010fc2761fbe3aec58731d4272cc2bcd1a72b0ba9b91`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/parsed_observables.json` — successful execution artifact; SHA-256 `9c473a2e334355a784a914c04c78e0a2ad720b97d40f9839b11b66ea3f6540da`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/status.json` — successful status record; SHA-256 `67435f3d86355f7072075a44ae314110577d4851f7a6f412f87072e703862d86`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/collection.json` — successful execution artifact; SHA-256 `94ec3655c6bd67222ad5dc26b983529922f572c9ddc243b30308df4b4aaf562f`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/formchk.log` — successful execution artifact; SHA-256 `566bfb4390b26396e97470879f7e8f24ed319a97e7fb1d94eb2699dccd197fc0`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/input.com` — successful execution artifact; SHA-256 `10d6e1072cc59927aeebd59cd41c57e0e629d46e0117decc0941bd39151d2488`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/parsed_observables.json` — successful execution artifact; SHA-256 `914e71da79777dc208ba41328b80208dc3c76fe434d0b4979b745e1e1dcdd477`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/status.json` — successful status record; SHA-256 `1dc46107071c0890c9b35c299e6034fc9eaac8baff0a440440eb1a659016d05b`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/collection.json` — successful execution artifact; SHA-256 `e7f0f3680032affe2ffe5a0c1fb3dd6fb4c4e76bdd18e3b9d7a5215287df1ef7`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/formchk.log` — successful execution artifact; SHA-256 `5b9005142062e3d5d81377779a77670240e3ca1042715bb50f8071e06f82ef75`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/input.com` — successful execution artifact; SHA-256 `5934c028ac4fdfda3acb57f9b946253f3215f4bb9d21cc16601ffb1d28f27bfd`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/parsed_observables.json` — successful execution artifact; SHA-256 `a1f5b2c055a1d070cc6a1e71c40da2c056a13c8d44df9324cb1841542cf8fa77`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/status.json` — successful status record; SHA-256 `b0bcd84f690b0019372854a9f3a0b2bc4930659a768ae670cc979fd67c3cfc77`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/collection.json` — successful execution artifact; SHA-256 `f2cea1ea02026ccc73eb6aa59428e1510804143667b723edf593a4b108880552`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/formchk.log` — successful execution artifact; SHA-256 `b4c2845487f32b16e83aa911343d74a57b27670d881db2c56c69320011bd925d`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/input.com` — successful execution artifact; SHA-256 `339feb119b92d0ae134d4660ee47f8bdcb22e743883e004ab2f1007b105721fb`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/parsed_observables.json` — successful execution artifact; SHA-256 `d3017036a814ff0e0f5e9c43751aa1e8ab088ed4886e6f964bd58148e0836870`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/status.json` — successful status record; SHA-256 `87e25dc303fbc795eb49aa24921f20f9d260d904f2008f636d3dbf94ddc81a07`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/collection.json` — successful execution artifact; SHA-256 `c647f204e3e93049c1510cb6bf22c9cef29f4b116b579566a665d8cae48a05e1`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/formchk.log` — successful execution artifact; SHA-256 `35ca851099b576a770b5741a676d5e2c72fbc24949d9970dd912f1383fd9975a`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/input.com` — successful execution artifact; SHA-256 `fdab3677e3ed9519cb5fb3d4faeb4598287c0e6af25dfc8d9f0058348e07de40`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/parsed_observables.json` — successful execution artifact; SHA-256 `942f116f2fd03f35fbabe5e7a74a2c5a48068f713d917de651a411b12b9a4646`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf/outputs/execution_jobs/job_00ac0ce089b54c87a756705d8f1d3124/status.json` — successful status record; SHA-256 `d5648ce0920929271548288e187c306980c4993b89776a9e13ce5ec54e598cac`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf/outputs/execution_jobs/job_00ac0ce089b54c87a756705d8f1d3124/collection.json` — successful execution artifact; SHA-256 `e47cc0122d39e8f3488e6cfaa2a53ceca7707e41b99fe1d004881e163b9c2679`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf/outputs/execution_jobs/job_00ac0ce089b54c87a756705d8f1d3124/input.com` — successful execution artifact; SHA-256 `603f1bc25269f67271fba7c00dc09b369db3d2085ac138d9c16832b83bf4dad4`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf/outputs/execution_jobs/job_00ac0ce089b54c87a756705d8f1d3124/request.json` — successful execution artifact; SHA-256 `c33d678c2a056122d2914648514af0328429b5cc2f25163e2825c7ae14c3dc03`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf/outputs/execution_jobs/job_00ac0ce089b54c87a756705d8f1d3124/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf_td3/outputs/execution_jobs/job_49556f0bf2ab41759ddc07ca61d98698/status.json` — successful status record; SHA-256 `12e986ef6e58acac06dd116e411063c051022b2046d83c497812794e1dc30b2a`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf_td3/outputs/execution_jobs/job_49556f0bf2ab41759ddc07ca61d98698/collection.json` — successful execution artifact; SHA-256 `e5c8527a64306c4b237fc916f79e29dcce4e1034af57849e292486ef08dd0b50`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf_td3/outputs/execution_jobs/job_49556f0bf2ab41759ddc07ca61d98698/input.com` — successful execution artifact; SHA-256 `d62c6e81f506310bb5d49569d1725c71cdb839f7596e931b8e0dccdf233fec00`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf_td3/outputs/execution_jobs/job_49556f0bf2ab41759ddc07ca61d98698/request.json` — successful execution artifact; SHA-256 `c5542fcb3bb67e2a8b02ff3edd20576f4e77bcd458e96bf1067dda6aa0ffb837`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bf_td3/outputs/execution_jobs/job_49556f0bf2ab41759ddc07ca61d98698/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt/outputs/execution_jobs/job_0594af61c8454e358f5af852f46b8bb0/status.json` — successful status record; SHA-256 `9f2f67b6952ae8aaba6f6ed64fc8505e35318b266fa28021ad3e83db78dd2980`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt/outputs/execution_jobs/job_0594af61c8454e358f5af852f46b8bb0/collection.json` — successful execution artifact; SHA-256 `242609bd761972ba84fd3bea84febba6ba83d928c261f918fe80eaafd02a15ed`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt/outputs/execution_jobs/job_0594af61c8454e358f5af852f46b8bb0/input.com` — successful execution artifact; SHA-256 `1613d22f9c1785f24b6485294af97126b427f789e59c2066eac11bf84ff3a324`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt/outputs/execution_jobs/job_0594af61c8454e358f5af852f46b8bb0/request.json` — successful execution artifact; SHA-256 `3e50d0a110bc2ecec14018259e02303f30cdb2da1587e56b58116438b182c2a4`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt/outputs/execution_jobs/job_0594af61c8454e358f5af852f46b8bb0/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_td3/outputs/execution_jobs/job_f3a383bbb36a4568ac7000e7d27d0fb9/status.json` — successful status record; SHA-256 `62cf4c2493eb9ff1961073ad07825ae22101720d755cf3e47748d4188917d968`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_td3/outputs/execution_jobs/job_f3a383bbb36a4568ac7000e7d27d0fb9/collection.json` — successful execution artifact; SHA-256 `631e8d3124cb45c327e47b54b57cd4fc27f0892342d2355e941ccad77abed025`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_td3/outputs/execution_jobs/job_f3a383bbb36a4568ac7000e7d27d0fb9/input.com` — successful execution artifact; SHA-256 `ecaf7ac42cb39312d8f7010fc2761fbe3aec58731d4272cc2bcd1a72b0ba9b91`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_td3/outputs/execution_jobs/job_f3a383bbb36a4568ac7000e7d27d0fb9/request.json` — successful execution artifact; SHA-256 `46e55a1bae950bcd350914de0c9f83ec2364f7955296d752f65d2c1dc398fa8d`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_td3/outputs/execution_jobs/job_f3a383bbb36a4568ac7000e7d27d0fb9/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_tight_min_retry/outputs/execution_jobs/job_be90c7c8bbb9482aa27d57fd4e2ed315/status.json` — successful status record; SHA-256 `67435f3d86355f7072075a44ae314110577d4851f7a6f412f87072e703862d86`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_tight_min_retry/outputs/execution_jobs/job_be90c7c8bbb9482aa27d57fd4e2ed315/collection.json` — successful execution artifact; SHA-256 `94ec3655c6bd67222ad5dc26b983529922f572c9ddc243b30308df4b4aaf562f`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_tight_min_retry/outputs/execution_jobs/job_be90c7c8bbb9482aa27d57fd4e2ed315/input.com` — successful execution artifact; SHA-256 `10d6e1072cc59927aeebd59cd41c57e0e629d46e0117decc0941bd39151d2488`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_tight_min_retry/outputs/execution_jobs/job_be90c7c8bbb9482aa27d57fd4e2ed315/request.json` — successful execution artifact; SHA-256 `4fe553dbb48ce5de2f337aa69b3c6e72c80bd4522fefcfe4e71667cc491690b5`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2bt_tight_min_retry/outputs/execution_jobs/job_be90c7c8bbb9482aa27d57fd4e2ed315/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8/outputs/execution_jobs/job_b34e53f986e74fc3917b0f0319efe381/status.json` — successful status record; SHA-256 `1dc46107071c0890c9b35c299e6034fc9eaac8baff0a440440eb1a659016d05b`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8/outputs/execution_jobs/job_b34e53f986e74fc3917b0f0319efe381/collection.json` — successful execution artifact; SHA-256 `e7f0f3680032affe2ffe5a0c1fb3dd6fb4c4e76bdd18e3b9d7a5215287df1ef7`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8/outputs/execution_jobs/job_b34e53f986e74fc3917b0f0319efe381/input.com` — successful execution artifact; SHA-256 `5934c028ac4fdfda3acb57f9b946253f3215f4bb9d21cc16601ffb1d28f27bfd`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8/outputs/execution_jobs/job_b34e53f986e74fc3917b0f0319efe381/request.json` — successful execution artifact; SHA-256 `5a68c357fa2783a378033691367a3238ee77cb4f488ba67b5061510c08d7efb7`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8/outputs/execution_jobs/job_b34e53f986e74fc3917b0f0319efe381/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_runtime_retry48g/outputs/execution_jobs/job_75eb51d2088c4f5a930e9d353377ae54/status.json` — successful status record; SHA-256 `b0bcd84f690b0019372854a9f3a0b2bc4930659a768ae670cc979fd67c3cfc77`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_runtime_retry48g/outputs/execution_jobs/job_75eb51d2088c4f5a930e9d353377ae54/collection.json` — successful execution artifact; SHA-256 `f2cea1ea02026ccc73eb6aa59428e1510804143667b723edf593a4b108880552`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_runtime_retry48g/outputs/execution_jobs/job_75eb51d2088c4f5a930e9d353377ae54/input.com` — successful execution artifact; SHA-256 `339feb119b92d0ae134d4660ee47f8bdcb22e743883e004ab2f1007b105721fb`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_runtime_retry48g/outputs/execution_jobs/job_75eb51d2088c4f5a930e9d353377ae54/request.json` — successful execution artifact; SHA-256 `f97f86a1dfa669a71bb6499776779f66fc1725931f851c75bf84e61814a4d7f0`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_runtime_retry48g/outputs/execution_jobs/job_75eb51d2088c4f5a930e9d353377ae54/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_td3/outputs/execution_jobs/job_17d2e0b9c426480a853e1821cb3f412a/status.json` — successful status record; SHA-256 `87e25dc303fbc795eb49aa24921f20f9d260d904f2008f636d3dbf94ddc81a07`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_td3/outputs/execution_jobs/job_17d2e0b9c426480a853e1821cb3f412a/collection.json` — successful execution artifact; SHA-256 `c647f204e3e93049c1510cb6bf22c9cef29f4b116b579566a665d8cae48a05e1`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_td3/outputs/execution_jobs/job_17d2e0b9c426480a853e1821cb3f412a/input.com` — successful execution artifact; SHA-256 `fdab3677e3ed9519cb5fb3d4faeb4598287c0e6af25dfc8d9f0058348e07de40`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_td3/outputs/execution_jobs/job_17d2e0b9c426480a853e1821cb3f412a/request.json` — successful execution artifact; SHA-256 `288e90e4caacfa99455832d48b08886fc9048c9ce621f91332dd88aa8b71ab4f`
- `docs/verification/group_3/paper_94b0a8ae694590ea/native_workspace/tta_2c8_td3/outputs/execution_jobs/job_17d2e0b9c426480a853e1821cb3f412a/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/tta_2bf/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2bf; submitted_at=2026-08-29T07:45:04.876747+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/tta_2bf.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/tta_2bf.fchk`
2. `artifacts/gaussian/tta_2bt/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2bt; submitted_at=2026-08-29T07:45:05.650606+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/tta_2bt.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt/tta_2bt.fchk`
3. `artifacts/gaussian/tta_2c8/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2c8; submitted_at=2026-08-29T07:45:06.379071+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/tta_2c8.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8/tta_2c8.fchk`
4. `artifacts/gaussian/tta_2bf_td3/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2bf_td3; submitted_at=2026-08-29T15:53:48.421058+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=3) SCRF=(PCM,Solvent=Toluene) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/tta_2bf_td3.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf_td3/tta_2bf_td3.fchk`
5. `artifacts/gaussian/tta_2bt_td3/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2bt_td3; submitted_at=2026-08-29T15:53:49.222840+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=3) SCRF=(PCM,Solvent=Toluene) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/tta_2bt_td3.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_td3/tta_2bt_td3.fchk`
6. `artifacts/gaussian/tta_2c8_td3/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2c8_td3; submitted_at=2026-08-29T15:53:50.052922+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=3) SCRF=(PCM,Solvent=Toluene) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/tta_2c8_td3.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_td3/tta_2c8_td3.fchk`
7. `artifacts/gaussian/tta_2bt_tight_min_retry/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2bt_tight_min_retry; submitted_at=2026-08-31T01:39:40.199524+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Int=UltraFine Opt=(CalcFC,Tight,MaxCycles=512,MaxStep=8) Freq Pop=Full NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/tta_2bt_tight_min_retry.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/tta_2bt_tight_min_retry.fchk`
8. `artifacts/gaussian/tta_2c8_runtime_retry48g/status.json` — label=group_3 paper_94b0a8ae694590ea tta_2c8_runtime_retry48g; submitted_at=2026-08-31T01:39:40.290422+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Int=UltraFine Opt=(CalcFC,MaxCycles=512,MaxStep=8) Freq Pop=Full NoSymm SCF=(XQC,MaxCycle=2048); command=g16 < input.com
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/collection.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/formchk.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/input.com`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/stderr.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/stdout.log`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/tta_2c8_runtime_retry48g.chk`
   - output: `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/tta_2c8_runtime_retry48g.fchk`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `conclusion_limitations`, `r_lim`.

- Key-point IDs: `kp_process_identity, kp_process_validation, kp_result_levels, kp_result_ordering`
- Conclusion IDs: `conclusion_final_levels, conclusion_limitations`
- Scoring-rule IDs: `r_identity, r_validation, r_levels, r_order, r_final, r_lim`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_identity` → reference `kp_process_identity`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_validation` → reference `kp_process_validation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_levels` → reference `kp_result_levels`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert numeric comparison; evaluator_target_present=False
- rule `r_order` → reference `kp_result_ordering`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_final` → reference `conclusion_final_levels`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_lim` → reference `conclusion_limitations`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].name` = `"2BT-TTA"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].charge` = `0`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].multiplicity` = `1`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].status` = `"validated"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].homo_eV` = `-5.1263528295695`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].lumo_eV` = `-2.0394933094975003`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].units` = `"eV"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[0].validation_evidence` = `"Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2bt_tight_min_retry/stdout.log"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].name` = `"2BF-TTA"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].charge` = `0`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].multiplicity` = `1`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].status` = `"validated"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].homo_eV` = `-5.002541027592001`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].lumo_eV` = `-2.0770450208665`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].units` = `"eV"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[1].validation_evidence` = `"Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2bf/stdout.log"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].name` = `"2(C8Ph)-TTA"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].charge` = `0`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].multiplicity` = `1`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].status` = `"validated"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].homo_eV` = `-4.9900237904689995`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].lumo_eV` = `-1.645200340123`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].units` = `"eV"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules` / result path `$.molecules[2].validation_evidence` = `"Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2c8_runtime_retry48g/stdout.log"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules[].name` / result path `$.molecules[].name` = `"2BT-TTA"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules[].name` / result path `$.molecules[].name` = `"2BF-TTA"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules[].name` / result path `$.molecules[].name` = `"2(C8Ph)-TTA"`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules[].charge` / result path `$.molecules[].charge` = `0`
- rule `r_identity` / reference `kp_process_identity` / field `$.molecules[].multiplicity` / result path `$.molecules[].multiplicity` = `1`
- rule `r_identity` / reference `kp_process_identity` / field `$.coverage` / result path `$.coverage` = `"Exactly the three supplied XYZ structures; no additional conformers."`
- rule `r_validation` / reference `kp_process_validation` / field `$.validation` / result path `$.validation` = `"All three supplied neutral singlets completed B3LYP/6-31G(d,p) Opt/Freq with zero imaginary frequencies; frontier levels parsed from final alpha MO block."`
- rule `r_validation` / reference `kp_process_validation` / field `$.molecules[].validation_evidence` / result path `$.molecules[].validation_evidence` = `"Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2bt_tight_min_retry/stdout.log"`
- rule `r_validation` / reference `kp_process_validation` / field `$.molecules[].validation_evidence` / result path `$.molecules[].validation_evidence` = `"Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2bf/stdout.log"`
- rule `r_validation` / reference `kp_process_validation` / field `$.molecules[].validation_evidence` / result path `$.molecules[].validation_evidence` = `"Gaussian normal termination, Opt/Freq, zero imaginary frequencies; artifact artifacts/gaussian/tta_2c8_runtime_retry48g/stdout.log"`
- rule `r_validation` / reference `kp_process_validation` / field `$.stopping_rule` / result path `$.stopping_rule` = `"Stopped after all three supplied structures were frequency-validated and frontier levels parsed."`
- rule `r_levels` / reference `kp_result_levels` / field `$.molecules[].homo_eV` / result path `$.molecules[].homo_eV` = `-5.1263528295695`
- rule `r_levels` / reference `kp_result_levels` / field `$.molecules[].homo_eV` / result path `$.molecules[].homo_eV` = `-5.002541027592001`
- rule `r_levels` / reference `kp_result_levels` / field `$.molecules[].homo_eV` / result path `$.molecules[].homo_eV` = `-4.9900237904689995`
- rule `r_levels` / reference `kp_result_levels` / field `$.molecules[].lumo_eV` / result path `$.molecules[].lumo_eV` = `-2.0394933094975003`
- rule `r_levels` / reference `kp_result_levels` / field `$.molecules[].lumo_eV` / result path `$.molecules[].lumo_eV` = `-2.0770450208665`
- rule `r_levels` / reference `kp_result_levels` / field `$.molecules[].lumo_eV` / result path `$.molecules[].lumo_eV` = `-1.645200340123`
- rule `r_levels` / reference `kp_result_levels` / field `$.molecules[].units` / result path `$.molecules[].units` = `"eV"`
- rule `r_order` / reference `kp_result_ordering` / field `$.ordering` / result path `$.ordering` = `"2BT-TTA HOMO=-5.1264 eV, LUMO=-2.0395 eV; 2BF-TTA HOMO=-5.0025 eV, LUMO=-2.0770 eV; 2(C8Ph)-TTA HOMO=-4.9900 eV, LUMO=-1.6452 eV"`
- rule `r_order` / reference `kp_result_ordering` / field `$.conclusion` / result path `$.conclusion` = `"The frontier-level ordering is reported directly from the three validated isolated-molecule calculations; this is qualitative alignment evidence and does not model explicit SWCNT charge transfer."`
- rule `r_order` / reference `kp_result_ordering` / field `$.limitations` / result path `$.limitations` = `"Gas-phase isolated molecules; method and conformer dependent; HOMO/LUMO alignment is not a charge-transfer calculation."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized/final structure is exposed as agent input for a scored comparison; redesign with neutral or independently generated starting geometry
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Three SI-derived XYZ coordinate files.

Public input files and hashes:

- `agent_input/data/inputs/2BF-TTA.xyz` — SHA-256 `415ce7f5baedd7790c4da78fcc507ae32988cc959ee3b9f9c15cbe1488d1656e`; size=1682 bytes; xyz_atom_count=44; xyz_comment=SI-derived coordinate input; use as supplied and independently validate; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/2BT-TTA.xyz` — SHA-256 `8cdea648ac98ef086366a4485d6cbfd31fbeaafd3dd7a4539ed592814652033f`; size=1681 bytes; xyz_atom_count=44; xyz_comment=SI-derived coordinate input; use as supplied and independently validate; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/2C8Ph-TTA.xyz` — SHA-256 `269236c4de4fd0dc19ea2834161b36905b324dbefa7b449c6290a10f057010c4`; size=3258 bytes; xyz_atom_count=86; xyz_comment=SI-derived coordinate input; use as supplied and independently validate; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `agent_input/data/inputs/2BF-TTA.xyz, agent_input/data/inputs/2BT-TTA.xyz, agent_input/data/inputs/2C8Ph-TTA.xyz`

## Evidence files

- `docs/verification/group_3/paper_94b0a8ae694590ea/verification_report.md` — verification record; SHA-256 `34a605ceedff6264a1e2a7916df2de4fa0909855aba78cd2510530c1c6dc4711`
- `docs/verification/group_3/paper_94b0a8ae694590ea/report/results.json` — verification record; SHA-256 `e6d2bc47303a700776098d4d059fa2e97e0f7236dc84aa5a12eb6daadd20bced`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bf/stdout.log` — referenced successful evidence; SHA-256 `1e11451a94b2c9ec13ac5159538c693c48bdf2d8e470076e1ae3e24ba5b99284`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2bt_tight_min_retry/stdout.log` — referenced successful evidence; SHA-256 `f0fd684df0c137bf9721359a9618200eafdf993319d3f1a91c796d1ff4fdd1af`
- `docs/verification/group_3/paper_94b0a8ae694590ea/artifacts/gaussian/tta_2c8_runtime_retry48g/stdout.log` — referenced successful evidence; SHA-256 `7b3cb892f2e703e149290c98f6bda8cda347026077eac67e3b12287e54322006`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
