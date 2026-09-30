# Verified computation reference — paper_2f2aa11ea61a32bb (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `validated` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 84 | `QUALIFIED` | 中，最终严格判定为 **QUALIFIED（scope-limited）**；该判定不表示作者方法或隐藏 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Development of unsymmetrical boron complexes bearing (iso)quinolylphenol ligands and their halogenated derivatives; crystal polymorphism for white-light-emitting properties
- DOI: `10.1039/d5cp04402b`
- Task package: `tasks/final_verified_paper_reproduction/paper_2f2aa11ea61a32bb`
- Verification group: `docs/verification/group_2/paper_2f2aa11ea61a32bb`
- Paper documents: `papers/paper_2f2aa11ea61a32bb`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "limitations": "No experimental maxima are provided in the task-visible inputs; no claim of numerical agreement with the paper is made. The author route is retained when available; legacy lower-cost calculations are diagnostic only.",
  "method_summary": "Gaussian 16 C.01 B3LYP/6-31+G(d,p) Opt/Freq followed by vertical TD(Singlets,NStates=20) at each optimized geometry; isolated gas phase, charge 0, multiplicity 1, NoSymm, SCF Tight/XQC.",
  "molecules": [
    {
      "calculation_status": "validated Opt/Freq and TD-DFT",
      "comparison": {
        "interpretation": "Experimental maxima are not supplied in the public task; computational series comparison only."
      },
      "id": "1a",
      "selected_feature": {
        "assignment_rule": "lowest-energy singlet with oscillator strength >= 1e-3",
        "excitation_energy_ev": 3.4292,
        "oscillator_strength": 0.1016,
        "state_label": "S1",
        "transition_character": "orbital transitions [{'from': 56, 'to': 57, 'coefficient': 0.69351}]",
        "wavelength_nm": 361.55
      },
      "validation": {
        "evidence": "artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20_summary.json",
        "geometry_status": "stationary minimum",
        "imaginary_frequency_count": 0
      }
    },
    {
      "calculation_status": "validated Opt/Freq and TD-DFT",
      "comparison": {
        "interpretation": "Experimental maxima are not supplied in the public task; computational series comparison only."
      },
      "id": "1b",
      "selected_feature": {
        "assignment_rule": "lowest-energy singlet with oscillator strength >= 1e-3",
        "excitation_energy_ev": 3.1282,
        "oscillator_strength": 0.1425,
        "state_label": "S1",
        "transition_character": "orbital transitions [{'from': 68, 'to': 70, 'coefficient': 0.1159}, {'from': 69, 'to': 70, 'coefficient': 0.69379}]",
        "wavelength_nm": 396.34
      },
      "validation": {
        "evidence": "artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20_summary.json",
        "geometry_status": "stationary minimum",
        "imaginary_frequency_count": 0
      }
    },
    {
      "calculation_status": "validated Opt/Freq and TD-DFT",
      "comparison": {
        "interpretation": "Experimental maxima are not supplied in the public task; computational series comparison only."
      },
      "id": "1c",
      "selected_feature": {
        "assignment_rule": "lowest-energy singlet with oscillator strength >= 1e-3",
        "excitation_energy_ev": 2.9485,
        "oscillator_strength": 0.008,
        "state_label": "S1",
        "transition_character": "orbital transitions [{'from': 69, 'to': 70, 'coefficient': 0.70036}]",
        "wavelength_nm": 420.49
      },
      "validation": {
        "evidence": "artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20_summary.json",
        "geometry_status": "stationary minimum",
        "imaginary_frequency_count": 0
      }
    },
    {
      "calculation_status": "validated Opt/Freq and TD-DFT",
      "comparison": {
        "interpretation": "Experimental maxima are not supplied in the public task; computational series comparison only."
      },
      "id": "1d",
      "selected_feature": {
        "assignment_rule": "lowest-energy singlet with oscillator strength >= 1e-3",
        "excitation_energy_ev": 3.0567,
        "oscillator_strength": 0.1348,
        "state_label": "S1",
        "transition_character": "orbital transitions [{'from': 69, 'to': 70, 'coefficient': 0.69988}]",
        "wavelength_nm": 405.62
      },
      "validation": {
        "evidence": "artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20_summary.json",
        "geometry_status": "stationary minimum",
        "imaginary_frequency_count": 0
      }
    }
  ],
  "overall_conclusion": "All four molecules have target-level Opt/Freq and TD-DFT evidence.",
  "series_comparison": "The four independently calculated lowest intense singlet features are compared by wavelength and oscillator strength after all jobs terminate; heteroaryl extension/connectivity is interpreted qualitatively only.",
  "status": "validated"
}
```

Paper/SI document hashes:

- `papers/paper_2f2aa11ea61a32bb/documents/supplementary_001.pdf` — SHA-256 `6187b34d441b880b245cbbbd3350b5a9ca926ba472f56bd2026bad2a0e174983` (declared_match=True)
- `papers/paper_2f2aa11ea61a32bb/documents/main.pdf` — SHA-256 `bfdb4129439627d7d651b864d72f7c08c512af56365e473b538a8460c1e6a694` (declared_match=True)

Report evidence lines retained:

- 已满足本任务的收口条件（四个分子均完成 Opt/Freq 和 20 态 TD-DFT）；`report/results.json` 使用 validated 分支。任务未提供实验最大吸收值，故仅报告计算系列比较。Gaussian 作业使用无人工 walltime 策略。
- ## 追加 Gaussian Opt/Freq + TD-DFT 收口（2026-08-29）
- - 对 1a–1d 使用 Gaussian 16 C.01 B3LYP/6-31G(d) Opt/Freq；完成的结构频率结果与原始 stdout、checkpoint、输入和状态均保留在 `artifacts/gaussian_batch/`。
- - 在各自优化几何上运行 TD(Singlets,NStates=20)，按最低能量且振子强度 `f >= 1e-3` 选择主吸收；当前已收口的 1a、1b、1d 分别为 357.980、394.600、403.570 nm。1c 仍待 Opt/Freq 自然终止。
- - 四个 1a–1d 对象的作者级 B3LYP/6-31+G(d,p) Opt/Freq 和 20 态 Singlet TD-DFT 均正常终止，0 个虚频；优化坐标的原子数、顺序、电荷和多重度记录在 `provenance/author_route_evaluation_audit.json`。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **200**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/status.json` — successful status record; SHA-256 `d44c55f29a60ff41b8966867e6d031f84d0fd988ae7799223ca8a9750d0bc188`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `a7fa8bbfa416c20dc8d994e66c0d67338bf1e19b277cc4d25f2fca1d9e0b8cab`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `64a0c28c28b504c25d799e30b12206a17eb994fa933ea1ceb2e17a5cde44dba3`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `151c985b66df76281ab3a9e5b40aa9c6967648e37373687a7b0e7a5a7b23a3a8`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/status.json` — successful status record; SHA-256 `e1d5cb1d86980f0972586400747e11400c7d304b35d8a64d057a4c11ebe152b6`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/collection.json` — successful execution artifact; SHA-256 `6ee81e610be638a0f5d3bd6841f53fef2d731228505c118e6addbb39e98cb6f4`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/input.com` — successful execution artifact; SHA-256 `baf03ad155319e023e495828196707a1678a0d5cc87c538caa96f48455c765c8`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/stdout.log` — successful execution artifact; SHA-256 `d52cc45c6c55e1b9cde7ac6220ba63a56069737bdd03bc8874c9057d69db1ae9`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/status.json` — successful status record; SHA-256 `5a9a0c03057734563ebef6fb582ad2df08b71018676239c888f1fda1d85d7e99`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `9d60de9035be7e5e0f8a1f41b1826b8588acb327dfa4a1a0621ba55eb3e94b6c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `bd813c4b800b319aeefcfed59426bd3fa9d69864e2ca1c3d81c6ed41ac933d85`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `cb3571ee2c2ba4d6602705919106b5d6a7a4b16cb39d4a6a84355b61387bc7e4`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/status.json` — successful status record; SHA-256 `f3b96f58759f635e78db9d29c3b5d786b60f0a0b1bfcee7919c33355d6671774`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/collection.json` — successful execution artifact; SHA-256 `2b1bad0f4e33022ff691c5a15063d1a8818037ffbd3530968ab92fa2272c64bd`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/input.com` — successful execution artifact; SHA-256 `8cde0871c89808fbe3ea42cbdc7500bf47fbd286edad481ba17cc748d2ffb1f3`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/stdout.log` — successful execution artifact; SHA-256 `a00a5c423c966df058ea51d2afd2f910c6c9a834fbff01f604088c4f316f1a1a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/status.json` — successful status record; SHA-256 `352c51da1520edfc2385f1632155d963c407cdc680a10e33a75ac602a5d2dca2`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `773b960bfdf6cba95d91314454faf27b8bafcaf4df1a4edfa0b0c7cfc5a461fa`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `9bbc1cdd4cb8a43c9da1e4d540bf40503d7cb2b722a5c78839c5bb70eeb7e432`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `e7ad7b58091a4a119834bfc8ca46cafa9a0a72d81c470864491250fd23825fbd`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/status.json` — successful status record; SHA-256 `f604f30af8102ed4427f1d331d321fa7f4c1f9500f9c5073c88de2a260caeecb`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/collection.json` — successful execution artifact; SHA-256 `1ba2d382a8e85d84c4ee41498cb62dff67e4feded9f1362fe0729587d00e6886`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/input.com` — successful execution artifact; SHA-256 `c5f2590c9e3d347e3af7c11c2d2e542eebd5fbabaa161b37a09825f4a298bb68`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/stdout.log` — successful execution artifact; SHA-256 `7332c5f6034efea2694e3e75e68650aff641547a83cf24f0b3618f5167f266a3`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/status.json` — successful status record; SHA-256 `e9cea167d9d6ef300bd5655e46888415cf1300b9ba46df28e0c827d5fa4ecda6`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `ebad2c729923436eb45b916912135853ee62b4363e96117a8d6f7b3fe3330722`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `ee4bd93cf8244f1a0bcec83080ac456b9ee4c0803f4a99be5832d37c34b1e60b`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `5730a9e76220c09eb50c4404cd2f9ed24c686c9b7841997551c53cede7f22d24`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/status.json` — successful status record; SHA-256 `47181eb7cbce701ceba5d6190324233811025e3c5738ec7c2b92061250a7cb75`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/collection.json` — successful execution artifact; SHA-256 `13a2415e1b804f966cc8c6a9665ae4897ffa717c38c092df8a739a4853b19a77`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/input.com` — successful execution artifact; SHA-256 `c91e92f1f3911a4fbed856a3c537f6557eaab257c032c38a95ba70d39b16b201`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/stdout.log` — successful execution artifact; SHA-256 `d7596c11a13dd70c776bf0ac3fab806c9e1e1ea9725551115bb8d4cdcc182959`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/status.json` — successful status record; SHA-256 `4561fd4e7f40a54fe3c344c4f3d4c8a0514ef1fdda6b8697cd510f076aeedecf`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/collection.json` — successful execution artifact; SHA-256 `90011e5cc237927d2f21b21753ca220884cb762005ddce84e33271cf5752d03e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/input.com` — successful execution artifact; SHA-256 `5976586310cb64061ad743614c56b2182f7cce2b091102a4964be892554d4b36`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stdout.log` — successful execution artifact; SHA-256 `94c395a9a61209e74fcdbe02e618bcb56ea204d2ca3897db0cf4fe9641a1647a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/status.json` — successful status record; SHA-256 `87c102ddf030b5de80b1e35dd19025e36c787c331615312800ba4b52e816dd3e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/collection.json` — successful execution artifact; SHA-256 `672674109b50f9e9fa09228a25a1b49f5996907c2fe457d1a4765d7ad2b40876`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/input.com` — successful execution artifact; SHA-256 `66a18e9f047903c7436059f67cd594cf41aa578649fb18eb8df2ed9a82ff8d5c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/stdout.log` — successful execution artifact; SHA-256 `88dd82774f0a83b2724444473c75f80b8f2484555e1fd99ba566ed527a3c293b`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/status.json` — successful status record; SHA-256 `fd3558662125b93c48d37fa7402673d2b57a4fe25ec55b023a885e5e7877378a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/collection.json` — successful execution artifact; SHA-256 `1fb347f1946ec40bd124ff4e86674dd171970e0c9e00be35bafef6af4e2c04ae`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/input.com` — successful execution artifact; SHA-256 `06a2b7e735334567c36b8f55c84adc207bcdc35e391ab6dd2ed0854247b2281c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/stdout.log` — successful execution artifact; SHA-256 `7951053f834ed636896295214d6044d11aa1261b6a3605e7768107337816e465`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/status.json` — successful status record; SHA-256 `302245ac54eca96d11ac1af4567fd07b7523de4dc5df8cd479939bfde86dc9aa`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/collection.json` — successful execution artifact; SHA-256 `ab7081a7fb2fd85dbb7d6da59f5e89d787c7ab7d28cbab874fd24215a3c2eb4e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/input.com` — successful execution artifact; SHA-256 `cc78772b540d9c34aa74784146c6a7ef3153af88e07b6ae998ed2e1d0c74cfb9`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stdout.log` — successful execution artifact; SHA-256 `deca7ac1e7a19bad9425d465681ae0d293557172bb2c3d8a6b853eeaa965470c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/status.json` — successful status record; SHA-256 `0e965bafa39305cc660b487bbccdc22f0febdd8d78ef34eba8a5512f377cb61e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/collection.json` — successful execution artifact; SHA-256 `1861a76146e210770858cc1d35054930110508bfa1a3e4c427404bb0b3b8f557`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/input.com` — successful execution artifact; SHA-256 `c0eb84acd5bc8d04dbec9ffd8aa03e59d16236ad33ff737084942ca5bd7723d1`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/stdout.log` — successful execution artifact; SHA-256 `f5725e0043b684a54f93b88544e3eecdf59599915cc682aefdbea3d96523dc07`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/status.json` — successful status record; SHA-256 `a0c6cbea370825ec50b768f37d5baeeee099401e1d99a6fe63e7821024c06db1`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/collection.json` — successful execution artifact; SHA-256 `a15e5dc90fcbfc1d1cf59a751c560f1b43a76da095b78344b99d17b712b15dcd`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/input.com` — successful execution artifact; SHA-256 `85df7a00135ac1e9fe4f823d0050df0dde251242b39feeae81e04fe5272d56d0`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/stdout.log` — successful execution artifact; SHA-256 `7a51003e727643bef8fb341f12b8715fe0c611c193ed42abeb095c0b5ecfe905`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/status.json` — successful status record; SHA-256 `42097ac1550d25889ab8301a8b98cb5dbaa497d30c3d5963a5ab3202de473c9a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/collection.json` — successful execution artifact; SHA-256 `3e65e9e2aaa473566165cb0aaec5d79bb1e55198b015a3176ff19422727ebaa4`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/input.com` — successful execution artifact; SHA-256 `9991cade4734493e4bd00135afaaa2e21206720bc20b68abfcd3b5a1980bedf0`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stdout.log` — successful execution artifact; SHA-256 `b3156268b074b4eba874c6104c6337e564f10554ff5c0627c7a5bbc9e3013f51`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/status.json` — successful status record; SHA-256 `de9a68c02c52f8fa35a8cea5fcaefd89a7605e9cfdcb6b064714c0064243bd3c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/collection.json` — successful execution artifact; SHA-256 `917a38cce071c1623af896a059811de0733226ca348a198d60daf86dbb76630c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/input.com` — successful execution artifact; SHA-256 `0696817dd0435b50fe85865c8c7979fe256b13ae9463e56210bbeba4c03a857a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/stdout.log` — successful execution artifact; SHA-256 `46f260a003c91ece871b2fd03de705a148acf31a7355386853a1452863fcc737`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/status.json` — successful status record; SHA-256 `691496773c045a56c3cecddf568e3fb374ae9eea397d859d45f3ed24057c353d`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/collection.json` — successful execution artifact; SHA-256 `d44840807ca57324e454133f21fbf63edb96ac735da8e27fb80a8e0e8397b404`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/input.com` — successful execution artifact; SHA-256 `6270da5ba61205ff32f581fa6ecd8bb62d535be66b93b00e7211c3cf2391aebf`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/stdout.log` — successful execution artifact; SHA-256 `cd119add62b5bf6a0672dbd16b687c2f7e07b3fb6d82da6a47fd9d803106c158`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/status.json` — successful status record; SHA-256 `00a14c29a6b58ac2cab163ab73558da869433ac131ea496a5dae313584887325`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/collection.json` — successful execution artifact; SHA-256 `3ea66dbdf3fab46b397b1d320c9108c33973922cbd364f07da217babdef122ee`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/input.com` — successful execution artifact; SHA-256 `726fe987323a0c15ee7263ffd53eed875576c15a57ae91df353254a67423b365`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stdout.log` — successful execution artifact; SHA-256 `3efa564059672b19cd18ad1c85a1c40b4c7db4897dcafad872d6c72fef00faf7`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/status.json` — successful status record; SHA-256 `9f41a16a9796f56410c8130dc34cf7a3de0dd3f9df1e4a0098d429ae311b1ccb`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/collection.json` — successful execution artifact; SHA-256 `63b1d7454b08ceb44453e69d1bdfabbaae5fa855e8b81185c2ec6667fd595be8`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/input.com` — successful execution artifact; SHA-256 `6d566c78ceb4ab65331eb699296dec3ad07c3a3cde7803ce9b965a95e2f074bf`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/stdout.log` — successful execution artifact; SHA-256 `47814555a224e34179759435de9d07189a3390d20e366c93ec947a6b27464521`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/status.json` — successful status record; SHA-256 `886a23a580468761ee7a9ca5f38f3225fea362fbb2349f5a0a6a7cd127707bec`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/collection.json` — successful execution artifact; SHA-256 `4503f1b91ea889f2ab9590240bcbcdf33bd1799bf40592245d22ccb5356074ad`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/input.com` — successful execution artifact; SHA-256 `6c9e56d41ae2a680a96056ed2abd258fb9da2342bb2ca455448a570c70b3b0ce`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/stdout.log` — successful execution artifact; SHA-256 `a85700f00fb635802335a7e367404e7650e738a2c0c5ef0f750e0efa0ee4a5a0`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_0127c8335361470792eff6a6be0b3856/status.json` — successful status record; SHA-256 `47181eb7cbce701ceba5d6190324233811025e3c5738ec7c2b92061250a7cb75`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_0127c8335361470792eff6a6be0b3856/collection.json` — successful execution artifact; SHA-256 `13a2415e1b804f966cc8c6a9665ae4897ffa717c38c092df8a739a4853b19a77`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_0127c8335361470792eff6a6be0b3856/input.com` — successful execution artifact; SHA-256 `c91e92f1f3911a4fbed856a3c537f6557eaab257c032c38a95ba70d39b16b201`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_0127c8335361470792eff6a6be0b3856/request.json` — successful execution artifact; SHA-256 `d5693b5169c2400e9d4ef66a321e4602bdec16d2781eea06af97db0772f279a0`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_0127c8335361470792eff6a6be0b3856/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_086602a5d69545fc9fc5f0ccbbe9a401/status.json` — successful status record; SHA-256 `de9a68c02c52f8fa35a8cea5fcaefd89a7605e9cfdcb6b064714c0064243bd3c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_086602a5d69545fc9fc5f0ccbbe9a401/collection.json` — successful execution artifact; SHA-256 `917a38cce071c1623af896a059811de0733226ca348a198d60daf86dbb76630c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_086602a5d69545fc9fc5f0ccbbe9a401/input.com` — successful execution artifact; SHA-256 `0696817dd0435b50fe85865c8c7979fe256b13ae9463e56210bbeba4c03a857a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_086602a5d69545fc9fc5f0ccbbe9a401/request.json` — successful execution artifact; SHA-256 `84d0446fdbdbcf624c9668be6f5b7c946497b70957983d85e6b764a7448d1d71`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_086602a5d69545fc9fc5f0ccbbe9a401/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_10b1f3a23b364011925a33c9a9578455/status.json` — successful status record; SHA-256 `00a14c29a6b58ac2cab163ab73558da869433ac131ea496a5dae313584887325`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_10b1f3a23b364011925a33c9a9578455/collection.json` — successful execution artifact; SHA-256 `3ea66dbdf3fab46b397b1d320c9108c33973922cbd364f07da217babdef122ee`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_10b1f3a23b364011925a33c9a9578455/input.com` — successful execution artifact; SHA-256 `726fe987323a0c15ee7263ffd53eed875576c15a57ae91df353254a67423b365`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_10b1f3a23b364011925a33c9a9578455/request.json` — successful execution artifact; SHA-256 `8afe7b2dcdcd037ff8d78a89415f94094e41d33ae8a7994d2dbcccda567a0485`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_10b1f3a23b364011925a33c9a9578455/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_133ba5e501b547c5965fb51f739f47aa/status.json` — successful status record; SHA-256 `352c51da1520edfc2385f1632155d963c407cdc680a10e33a75ac602a5d2dca2`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_133ba5e501b547c5965fb51f739f47aa/collection.json` — successful execution artifact; SHA-256 `773b960bfdf6cba95d91314454faf27b8bafcaf4df1a4edfa0b0c7cfc5a461fa`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_133ba5e501b547c5965fb51f739f47aa/input.com` — successful execution artifact; SHA-256 `9bbc1cdd4cb8a43c9da1e4d540bf40503d7cb2b722a5c78839c5bb70eeb7e432`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_133ba5e501b547c5965fb51f739f47aa/request.json` — successful execution artifact; SHA-256 `6181a5b7127ec04696ba52ef6085ce72a8a90e7eeecc9cb241938cc6f5f840e3`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_133ba5e501b547c5965fb51f739f47aa/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_352fb0f7ab46467b808482e560979d14/status.json` — successful status record; SHA-256 `691496773c045a56c3cecddf568e3fb374ae9eea397d859d45f3ed24057c353d`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_352fb0f7ab46467b808482e560979d14/collection.json` — successful execution artifact; SHA-256 `d44840807ca57324e454133f21fbf63edb96ac735da8e27fb80a8e0e8397b404`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_352fb0f7ab46467b808482e560979d14/input.com` — successful execution artifact; SHA-256 `6270da5ba61205ff32f581fa6ecd8bb62d535be66b93b00e7211c3cf2391aebf`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_352fb0f7ab46467b808482e560979d14/request.json` — successful execution artifact; SHA-256 `1a23a889b66a3e1e89c482332e5fb5b3985ce30af3a093a1110b3358eae3bf0b`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_352fb0f7ab46467b808482e560979d14/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_3b3b7f86b5a64ea9a881aaae93535eae/status.json` — successful status record; SHA-256 `4561fd4e7f40a54fe3c344c4f3d4c8a0514ef1fdda6b8697cd510f076aeedecf`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_3b3b7f86b5a64ea9a881aaae93535eae/collection.json` — successful execution artifact; SHA-256 `90011e5cc237927d2f21b21753ca220884cb762005ddce84e33271cf5752d03e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_3b3b7f86b5a64ea9a881aaae93535eae/input.com` — successful execution artifact; SHA-256 `5976586310cb64061ad743614c56b2182f7cce2b091102a4964be892554d4b36`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_3b3b7f86b5a64ea9a881aaae93535eae/request.json` — successful execution artifact; SHA-256 `766130ebf4065a89da780fabed20f333374fe23eb322c635328b10951527fa95`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_3b3b7f86b5a64ea9a881aaae93535eae/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_41538ccbf5b142f0b24b28938b67d1da/status.json` — successful status record; SHA-256 `87c102ddf030b5de80b1e35dd19025e36c787c331615312800ba4b52e816dd3e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_41538ccbf5b142f0b24b28938b67d1da/collection.json` — successful execution artifact; SHA-256 `672674109b50f9e9fa09228a25a1b49f5996907c2fe457d1a4765d7ad2b40876`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_41538ccbf5b142f0b24b28938b67d1da/input.com` — successful execution artifact; SHA-256 `66a18e9f047903c7436059f67cd594cf41aa578649fb18eb8df2ed9a82ff8d5c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_41538ccbf5b142f0b24b28938b67d1da/request.json` — successful execution artifact; SHA-256 `e2e11e0fb891560d5e104f1d31106c4acdebb9280111c5383ab9420dab39d7bc`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_41538ccbf5b142f0b24b28938b67d1da/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_45705c23210349bdbc9544108551c5b6/status.json` — successful status record; SHA-256 `f604f30af8102ed4427f1d331d321fa7f4c1f9500f9c5073c88de2a260caeecb`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_45705c23210349bdbc9544108551c5b6/collection.json` — successful execution artifact; SHA-256 `1ba2d382a8e85d84c4ee41498cb62dff67e4feded9f1362fe0729587d00e6886`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_45705c23210349bdbc9544108551c5b6/input.com` — successful execution artifact; SHA-256 `c5f2590c9e3d347e3af7c11c2d2e542eebd5fbabaa161b37a09825f4a298bb68`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_45705c23210349bdbc9544108551c5b6/request.json` — successful execution artifact; SHA-256 `c2ce243c31e2506fc3eb24eecb08d82b721423558d76b3efcc0332c7a195f03b`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_45705c23210349bdbc9544108551c5b6/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/status.json` — successful status record; SHA-256 `5a9a0c03057734563ebef6fb582ad2df08b71018676239c888f1fda1d85d7e99`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/collection.json` — successful execution artifact; SHA-256 `9d60de9035be7e5e0f8a1f41b1826b8588acb327dfa4a1a0621ba55eb3e94b6c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/input.com` — successful execution artifact; SHA-256 `bd813c4b800b319aeefcfed59426bd3fa9d69864e2ca1c3d81c6ed41ac933d85`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/request.json` — successful execution artifact; SHA-256 `9104cd1818a5e25147b09ebb25b5ef39768029976e47edb99d799d938e577573`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_48526662c922436996fc8ee3141898fb/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_4dae7e02f31e41ffadcc8305dabbf1fc/status.json` — successful status record; SHA-256 `9f41a16a9796f56410c8130dc34cf7a3de0dd3f9df1e4a0098d429ae311b1ccb`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_4dae7e02f31e41ffadcc8305dabbf1fc/collection.json` — successful execution artifact; SHA-256 `63b1d7454b08ceb44453e69d1bdfabbaae5fa855e8b81185c2ec6667fd595be8`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_4dae7e02f31e41ffadcc8305dabbf1fc/input.com` — successful execution artifact; SHA-256 `6d566c78ceb4ab65331eb699296dec3ad07c3a3cde7803ce9b965a95e2f074bf`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_4dae7e02f31e41ffadcc8305dabbf1fc/request.json` — successful execution artifact; SHA-256 `4153ca77fbde53d6da9226b9799bf5aa6cdba34bc9532e2acf3a71b644a199be`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_4dae7e02f31e41ffadcc8305dabbf1fc/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/status.json` — successful status record; SHA-256 `a0c6cbea370825ec50b768f37d5baeeee099401e1d99a6fe63e7821024c06db1`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/collection.json` — successful execution artifact; SHA-256 `a15e5dc90fcbfc1d1cf59a751c560f1b43a76da095b78344b99d17b712b15dcd`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/input.com` — successful execution artifact; SHA-256 `85df7a00135ac1e9fe4f823d0050df0dde251242b39feeae81e04fe5272d56d0`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/request.json` — successful execution artifact; SHA-256 `10feb1c3e10d0631da97f2ef9da59ae9a2bdb8399a748b712ea628a7cacca585`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_51d5f2773f514881ad4b1dd0a1ef5443/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/status.json` — successful status record; SHA-256 `f3b96f58759f635e78db9d29c3b5d786b60f0a0b1bfcee7919c33355d6671774`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/collection.json` — successful execution artifact; SHA-256 `2b1bad0f4e33022ff691c5a15063d1a8818037ffbd3530968ab92fa2272c64bd`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/input.com` — successful execution artifact; SHA-256 `8cde0871c89808fbe3ea42cbdc7500bf47fbd286edad481ba17cc748d2ffb1f3`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/request.json` — successful execution artifact; SHA-256 `43881891cb16274c7823b8ef29f3aa6537d624d47763c6204591b9fc4f1dc1b4`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_533be45a59fe4d7a97300260934cacf2/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/status.json` — successful status record; SHA-256 `302245ac54eca96d11ac1af4567fd07b7523de4dc5df8cd479939bfde86dc9aa`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/collection.json` — successful execution artifact; SHA-256 `ab7081a7fb2fd85dbb7d6da59f5e89d787c7ab7d28cbab874fd24215a3c2eb4e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/input.com` — successful execution artifact; SHA-256 `cc78772b540d9c34aa74784146c6a7ef3153af88e07b6ae998ed2e1d0c74cfb9`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/request.json` — successful execution artifact; SHA-256 `5fa7d3dd6a3243bdeea7118f188fc5d0426729a53fb442e7bba2fb994554c98c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_7b780d24e0a04796841b259ceb7711d6/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_9d4b5f2a501442b2b5649390b3ffdb1f/status.json` — successful status record; SHA-256 `fd3558662125b93c48d37fa7402673d2b57a4fe25ec55b023a885e5e7877378a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_9d4b5f2a501442b2b5649390b3ffdb1f/collection.json` — successful execution artifact; SHA-256 `1fb347f1946ec40bd124ff4e86674dd171970e0c9e00be35bafef6af4e2c04ae`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_9d4b5f2a501442b2b5649390b3ffdb1f/input.com` — successful execution artifact; SHA-256 `06a2b7e735334567c36b8f55c84adc207bcdc35e391ab6dd2ed0854247b2281c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_9d4b5f2a501442b2b5649390b3ffdb1f/request.json` — successful execution artifact; SHA-256 `a62ecd19d6c87784ac95a49dd44063b92e057b05c717a30687cfc243afd8fe4e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_9d4b5f2a501442b2b5649390b3ffdb1f/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_bbe599fff37d469abc336fbf7668d3e3/status.json` — successful status record; SHA-256 `42097ac1550d25889ab8301a8b98cb5dbaa497d30c3d5963a5ab3202de473c9a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_bbe599fff37d469abc336fbf7668d3e3/collection.json` — successful execution artifact; SHA-256 `3e65e9e2aaa473566165cb0aaec5d79bb1e55198b015a3176ff19422727ebaa4`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_bbe599fff37d469abc336fbf7668d3e3/input.com` — successful execution artifact; SHA-256 `9991cade4734493e4bd00135afaaa2e21206720bc20b68abfcd3b5a1980bedf0`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_bbe599fff37d469abc336fbf7668d3e3/request.json` — successful execution artifact; SHA-256 `c87051e876f55bf97a7f246a15f367b8b4f04fe2d6f0fe3dc771dbd37108919a`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_bbe599fff37d469abc336fbf7668d3e3/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_c74cbb60ef7d4f0ba0af5e419b1cd201/status.json` — successful status record; SHA-256 `886a23a580468761ee7a9ca5f38f3225fea362fbb2349f5a0a6a7cd127707bec`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_c74cbb60ef7d4f0ba0af5e419b1cd201/collection.json` — successful execution artifact; SHA-256 `4503f1b91ea889f2ab9590240bcbcdf33bd1799bf40592245d22ccb5356074ad`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_c74cbb60ef7d4f0ba0af5e419b1cd201/input.com` — successful execution artifact; SHA-256 `6c9e56d41ae2a680a96056ed2abd258fb9da2342bb2ca455448a570c70b3b0ce`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_c74cbb60ef7d4f0ba0af5e419b1cd201/request.json` — successful execution artifact; SHA-256 `bc5ea9774659dcd3ebe3fe210f73ef51234e16b7b6bd638c239bea91a998b0fb`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_c74cbb60ef7d4f0ba0af5e419b1cd201/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d5dc8decef6344b6b06566a55a710faf/status.json` — successful status record; SHA-256 `e9cea167d9d6ef300bd5655e46888415cf1300b9ba46df28e0c827d5fa4ecda6`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d5dc8decef6344b6b06566a55a710faf/collection.json` — successful execution artifact; SHA-256 `ebad2c729923436eb45b916912135853ee62b4363e96117a8d6f7b3fe3330722`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d5dc8decef6344b6b06566a55a710faf/input.com` — successful execution artifact; SHA-256 `ee4bd93cf8244f1a0bcec83080ac456b9ee4c0803f4a99be5832d37c34b1e60b`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d5dc8decef6344b6b06566a55a710faf/request.json` — successful execution artifact; SHA-256 `b7922827e9cbf94d392f0a40de3db8a771f45c7fdec161e3427768bb78a3b126`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d5dc8decef6344b6b06566a55a710faf/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d8c35ff2e6f44df48ad68ea8343ebd93/status.json` — successful status record; SHA-256 `d44c55f29a60ff41b8966867e6d031f84d0fd988ae7799223ca8a9750d0bc188`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d8c35ff2e6f44df48ad68ea8343ebd93/collection.json` — successful execution artifact; SHA-256 `a7fa8bbfa416c20dc8d994e66c0d67338bf1e19b277cc4d25f2fca1d9e0b8cab`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d8c35ff2e6f44df48ad68ea8343ebd93/input.com` — successful execution artifact; SHA-256 `64a0c28c28b504c25d799e30b12206a17eb994fa933ea1ceb2e17a5cde44dba3`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d8c35ff2e6f44df48ad68ea8343ebd93/request.json` — successful execution artifact; SHA-256 `71c751f9d915ee87ef7424a73bb40213289f26746d970dbc355e7b17c7f11606`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_d8c35ff2e6f44df48ad68ea8343ebd93/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_e469ede8edfd4b848d70e5a8bb811783/status.json` — successful status record; SHA-256 `e1d5cb1d86980f0972586400747e11400c7d304b35d8a64d057a4c11ebe152b6`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_e469ede8edfd4b848d70e5a8bb811783/collection.json` — successful execution artifact; SHA-256 `6ee81e610be638a0f5d3bd6841f53fef2d731228505c118e6addbb39e98cb6f4`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_e469ede8edfd4b848d70e5a8bb811783/input.com` — successful execution artifact; SHA-256 `baf03ad155319e023e495828196707a1678a0d5cc87c538caa96f48455c765c8`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_e469ede8edfd4b848d70e5a8bb811783/request.json` — successful execution artifact; SHA-256 `387e6da3f94d37a285bd786760ba59147d2aa16035d636276df5fff53a3fffb0`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_e469ede8edfd4b848d70e5a8bb811783/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/status.json` — successful status record; SHA-256 `0e965bafa39305cc660b487bbccdc22f0febdd8d78ef34eba8a5512f377cb61e`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/collection.json` — successful execution artifact; SHA-256 `1861a76146e210770858cc1d35054930110508bfa1a3e4c427404bb0b3b8f557`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/input.com` — successful execution artifact; SHA-256 `c0eb84acd5bc8d04dbec9ffd8aa03e59d16236ad33ff737084942ca5bd7723d1`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/request.json` — successful execution artifact; SHA-256 `8972bc656bb46bab1d84f07bcea9c562fc4f91ae592e4e5e7828b1944281113c`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/native_workspace_batch/outputs/execution_jobs/job_fd4fdab85e074b968c6df7f013ae30bc/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/1c_b3lyp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1c_b3lyp_optfreq; submitted_at=2026-08-29T16:02:13.728019+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/1c_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_optfreq/stdout.log`
2. `artifacts/gaussian_batch/1a_b3lyp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1a_b3lyp_optfreq; submitted_at=2026-08-29T16:02:13.729586+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/1a_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_optfreq/stdout.log`
3. `artifacts/gaussian_batch/1d_b3lyp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1d_b3lyp_optfreq; submitted_at=2026-08-29T16:02:13.732132+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/1d_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_optfreq/stdout.log`
4. `artifacts/gaussian_batch/1b_b3lyp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1b_b3lyp_optfreq; submitted_at=2026-08-29T16:02:13.734257+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/1b_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_optfreq/stdout.log`
5. `artifacts/gaussian_batch/1b_b3lyp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1b_b3lyp_td20; submitted_at=2026-08-29T16:26:02.698642+00:00; software=gaussian; intent=single_point; route=#p TD=(Singlets,NStates=20) B3LYP/6-31G(d) NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/1b_b3lyp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1b_b3lyp_td20/stdout.log`
6. `artifacts/gaussian_batch/1a_b3lyp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1a_b3lyp_td20; submitted_at=2026-08-29T16:32:36.106926+00:00; software=gaussian; intent=single_point; route=#p TD=(Singlets,NStates=20) B3LYP/6-31G(d) NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/1a_b3lyp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1a_b3lyp_td20/stdout.log`
7. `artifacts/gaussian_batch/1d_b3lyp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1d_b3lyp_td20; submitted_at=2026-08-29T16:37:39.342851+00:00; software=gaussian; intent=single_point; route=#p TD=(Singlets,NStates=20) B3LYP/6-31G(d) NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/1d_b3lyp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1d_b3lyp_td20/stdout.log`
8. `artifacts/gaussian_batch/1c_b3lyp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb 1c_b3lyp_td20; submitted_at=2026-08-29T16:47:37.382394+00:00; software=gaussian; intent=single_point; route=#p TD=(Singlets,NStates=20) B3LYP/6-31G(d) NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/1c_b3lyp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/1c_b3lyp_td20/stdout.log`
9. `artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1c_b3lyp_631pdp_optfreq; submitted_at=2026-08-30T16:52:41.557072+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/author_1c_b3lyp_631pdp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq/stdout.log`
10. `artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1b_b3lyp_631pdp_optfreq; submitted_at=2026-08-30T16:52:41.630933+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/author_1b_b3lyp_631pdp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq/stdout.log`
11. `artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1a_b3lyp_631pdp_optfreq; submitted_at=2026-08-30T16:52:41.863972+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/author_1a_b3lyp_631pdp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq/stdout.log`
12. `artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1d_b3lyp_631pdp_optfreq; submitted_at=2026-08-30T16:52:41.936452+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/author_1d_b3lyp_631pdp_optfreq.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq/stdout.log`
13. `artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1a_b3lyp_631pdp_td20; submitted_at=2026-08-31T16:24:18.321424+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-31+G(d,p) TD=(Singlets,NStates=20) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/author_1a_b3lyp_631pdp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20/stdout.log`
14. `artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1b_b3lyp_631pdp_td20; submitted_at=2026-08-31T16:24:19.809156+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-31+G(d,p) TD=(Singlets,NStates=20) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/author_1b_b3lyp_631pdp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20/stdout.log`
15. `artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1c_b3lyp_631pdp_td20; submitted_at=2026-08-31T16:24:21.278380+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-31+G(d,p) TD=(Singlets,NStates=20) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/author_1c_b3lyp_631pdp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20/stdout.log`
16. `artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1d_b3lyp_631pdp_td20; submitted_at=2026-08-31T16:24:22.746082+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-31+G(d,p) TD=(Singlets,NStates=20) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/author_1d_b3lyp_631pdp_td20.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20/stdout.log`
17. `artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1a_b3lyp_631pdp_td; submitted_at=2026-08-31T19:54:10.600668+00:00; software=gaussian; intent=single_point; route=#p TD(Singlets,NStates=20) B3LYP/6-31+G(d,p) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/author_1a_b3lyp_631pdp_td.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td/stdout.log`
18. `artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1b_b3lyp_631pdp_td; submitted_at=2026-08-31T19:54:11.080698+00:00; software=gaussian; intent=single_point; route=#p TD(Singlets,NStates=20) B3LYP/6-31+G(d,p) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/author_1b_b3lyp_631pdp_td.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td/stdout.log`
19. `artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1c_b3lyp_631pdp_td; submitted_at=2026-08-31T19:54:11.553673+00:00; software=gaussian; intent=single_point; route=#p TD(Singlets,NStates=20) B3LYP/6-31+G(d,p) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/author_1c_b3lyp_631pdp_td.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td/stdout.log`
20. `artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/status.json` — label=group_2 paper_2f2aa11ea61a32bb author_1d_b3lyp_631pdp_td; submitted_at=2026-08-31T19:54:12.030978+00:00; software=gaussian; intent=single_point; route=#p TD(Singlets,NStates=20) B3LYP/6-31+G(d,p) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/author_1d_b3lyp_631pdp_td.chk`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/collection.json`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/input.com`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/stderr.log`
   - output: `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td/stdout.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `c_limit`, `r_c_limit`.

- Key-point IDs: `kp_validation, kp_assignment, kp_shift`
- Conclusion IDs: `c_final, c_limit`
- Scoring-rule IDs: `r_kp_validation, r_kp_assignment, r_kp_shift, r_c_final, r_c_limit`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_kp_validation` → reference `kp_validation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_kp_assignment` → reference `kp_assignment`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_kp_shift` → reference `kp_shift`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_c_final` → reference `c_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_c_limit` → reference `c_limit`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_kp_validation` / reference `kp_validation` / field `$.molecules[].validation` / result path `$.molecules[].validation.geometry_status` = `"stationary minimum"`
- rule `r_kp_validation` / reference `kp_validation` / field `$.molecules[].validation` / result path `$.molecules[].validation.imaginary_frequency_count` = `0`
- rule `r_kp_validation` / reference `kp_validation` / field `$.molecules[].validation` / result path `$.molecules[].validation.evidence` = `"artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20_summary.json"`
- rule `r_kp_validation` / reference `kp_validation` / field `$.molecules[].validation` / result path `$.molecules[].validation.evidence` = `"artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20_summary.json"`
- rule `r_kp_validation` / reference `kp_validation` / field `$.molecules[].validation` / result path `$.molecules[].validation.evidence` = `"artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20_summary.json"`
- rule `r_kp_validation` / reference `kp_validation` / field `$.molecules[].validation` / result path `$.molecules[].validation.evidence` = `"artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq_summary.json; artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20_summary.json"`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.assignment_rule` = `"lowest-energy singlet with oscillator strength >= 1e-3"`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.state_label` = `"S1"`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.wavelength_nm` = `361.55`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.excitation_energy_ev` = `3.4292`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.oscillator_strength` = `0.1016`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.transition_character` = `"orbital transitions [{'from': 56, 'to': 57, 'coefficient': 0.69351}]"`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.wavelength_nm` = `396.34`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.excitation_energy_ev` = `3.1282`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.oscillator_strength` = `0.1425`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.transition_character` = `"orbital transitions [{'from': 68, 'to': 70, 'coefficient': 0.1159}, {'from': 69, 'to': 70, 'coefficient': 0.69379}]"`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.wavelength_nm` = `420.49`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.excitation_energy_ev` = `2.9485`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.oscillator_strength` = `0.008`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.transition_character` = `"orbital transitions [{'from': 69, 'to': 70, 'coefficient': 0.70036}]"`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.wavelength_nm` = `405.62`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.excitation_energy_ev` = `3.0567`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.oscillator_strength` = `0.1348`
- rule `r_kp_assignment` / reference `kp_assignment` / field `$.molecules[].selected_feature` / result path `$.molecules[].selected_feature.transition_character` = `"orbital transitions [{'from': 69, 'to': 70, 'coefficient': 0.69988}]"`
- rule `r_kp_shift` / reference `kp_shift` / field `$.series_comparison` / result path `$.series_comparison` = `"The four independently calculated lowest intense singlet features are compared by wavelength and oscillator strength after all jobs terminate; heteroaryl extension/connectivity is interpreted qualitatively only."`
- rule `r_c_final` / reference `c_final` / field `$.overall_conclusion` / result path `$.overall_conclusion` = `"All four molecules have target-level Opt/Freq and TD-DFT evidence."`
- rule `r_c_limit` / reference `c_limit` / field `$.limitations` / result path `$.limitations` = `"No experimental maxima are provided in the task-visible inputs; no claim of numerical agreement with the paper is made. The author route is retained when available; legacy lower-cost calculations are diagnostic only."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized/Cartesian result geometry provenance is not proven answer-neutral; confirm starting-vs-final status before release
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Four labeled XYZ starting geometries for neutral singlet complexes 1a–d.

Public input files and hashes:

- `agent_input/data/inputs/1a.xyz` — SHA-256 `4435a0b932a4a1235df2ce77a42c83cd384a1f10e672c5f433b4e3b99645a7ff`; size=860 bytes; xyz_atom_count=24; xyz_comment=1a public starting geometry; coordinates in Angstrom; explicit_boundary_fields={"units_hint": "explicit angstrom marker"}
- `agent_input/data/inputs/1b.xyz` — SHA-256 `81b54b65f613a4c6c69a6f996798e6ae7b55f2b3b4fa5f4321d6353b04aecba3`; size=1048 bytes; xyz_atom_count=30; xyz_comment=1b public starting geometry; coordinates in Angstrom; explicit_boundary_fields={"units_hint": "explicit angstrom marker"}
- `agent_input/data/inputs/1c.xyz` — SHA-256 `44c46e705af9dc905f903c78c9bb9682629f089c0cd4ae0e45faf3496d73f219`; size=1064 bytes; xyz_atom_count=30; xyz_comment=1c public starting geometry; coordinates in Angstrom; explicit_boundary_fields={"units_hint": "explicit angstrom marker"}
- `agent_input/data/inputs/1d.xyz` — SHA-256 `26e6c2d56f77f6b000882f719d5e554a859351d2de0be895225fce96c8f109d8`; size=1044 bytes; xyz_atom_count=30; xyz_comment=1d public starting geometry; coordinates in Angstrom; explicit_boundary_fields={"units_hint": "explicit angstrom marker"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_2/paper_2f2aa11ea61a32bb/verification_report.md` — verification record; SHA-256 `852bcfaabcbfb3b79cc62f488f8e8964b3582f4a683f5efc022b62ca59247254`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/report/results.json` — verification record; SHA-256 `9fe7e9e5f3f00d0c4ff916051a02fd354ddadcf49cafcb42dd14c4421c179961`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_optfreq_summary.json` — referenced successful evidence; SHA-256 `2edfd06c0b3915d1219b7a77fdbeda48597cd8c3350326eda51baab4e4309038`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1a_b3lyp_631pdp_td20_summary.json` — referenced successful evidence; SHA-256 `77729671febee60caf2d19c97b005d811d51bcfc23284867bf841c3f9b8481e1`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_optfreq_summary.json` — referenced successful evidence; SHA-256 `dad177be6593217001d8a89b7b87f380dd7426c67aea3d29de00a56e4eb43960`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1b_b3lyp_631pdp_td20_summary.json` — referenced successful evidence; SHA-256 `1ca979e6c9acd38989cc3e68cc3349e997c51c16a7123f88ab2658ef51d346ef`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_optfreq_summary.json` — referenced successful evidence; SHA-256 `bb8014d859eddfeafbd85d962b29fa22840c1838ed2f74608e28620648cba7ac`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1c_b3lyp_631pdp_td20_summary.json` — referenced successful evidence; SHA-256 `8820d12bf44636bed786138a8b9eccfe2d7bd64a9709e70ba850cf130d783527`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_optfreq_summary.json` — referenced successful evidence; SHA-256 `ad04bf5c14ad9a64ac35e6a5a673f1e380f0de526d2ee522c33c4a5d6ddc2d91`
- `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_1d_b3lyp_631pdp_td20_summary.json` — referenced successful evidence; SHA-256 `79d645c60c18d7175cc03127a1753ac322576f3ca97b9859674b5b62365eeefa`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.

## Evidence scope review (2026-09-19)

This is a retrospective comparison of the existing gas-phase TD20 outputs with the public toluene measurements; it does not change the historical result or certify quantitative reproduction. The original archive predates the experimental inputs. Main PDF pp. 2-3 / Table 1 and Fig. 3 report 345/375/383/381 nm and the additional 1c 339 nm band. The source attributes that additional band to S2/S3, not to whichever single root is nearest 339 nm.

| System / source assignment | State | Calculated nm | f | Measured nm | Calculated - measured nm |
|---|---:|---:|---:|---:|---:|
| 1a primary | S1 | 361.55 | 0.1016 | 345 | +16.55 |
| 1b primary | S1 | 396.34 | 0.1425 | 375 | +21.34 |
| 1c primary | S1 | 420.49 | 0.0080 | 383 | +37.49 |
| 1c additional band component | S2 | 350.76 | 0.2335 | 339 | +11.76 |
| 1c additional band component | S3 | 341.19 | 0.0719 | 339 | +2.19 |
| 1d primary | S1 | 405.62 | 0.1348 | 381 | +24.62 |

The two 1c entries describe components of one band, not two independent experimental measurements. No post hoc average or peak convolution is assumed. Assignment support, medium/model error, root coverage and absolute residuals remain separate. Full TD20 tables and transition coefficients are retained at `docs/verification/group_2/paper_2f2aa11ea61a32bb/artifacts/gaussian_batch/author_{1a,1b,1c,1d}_b3lyp_631pdp_td20/stdout.log`. No new calculation, numerical tolerance or mandatory method is introduced.
