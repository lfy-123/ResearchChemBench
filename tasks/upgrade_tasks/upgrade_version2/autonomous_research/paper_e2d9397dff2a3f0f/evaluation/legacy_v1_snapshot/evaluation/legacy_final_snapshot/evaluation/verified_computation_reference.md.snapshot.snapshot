# Verified computation reference — paper_e2d9397dff2a3f0f (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `completed` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: Public TS target.xyz was removed as an answer-bearing input; the strict-v2 group PASS uses the same reference/evaluator and retains the target only under evaluator-private inputs, with the group report stating no new Gaussian calculation is required.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 4 | `PASS` | 最终判定：**PASS（严格作者路线，评估任务范围内）** |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Cooperation of Carboxylate and Sulfonate Ligands in a High-Efficiency Ru Catalyst for Electrocatalytic Ammonia Oxidation
- DOI: `10.1021/jacs.5c18855`
- Task package: `tasks/final_verified_autonomous_research/paper_e2d9397dff2a3f0f`
- Verification group: `docs/verification/group_3/paper_e2d9397dff2a3f0f`
- Paper documents: `papers/paper_e2d9397dff2a3f0f`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "barrier": {
    "evidence": "Strict-v2 raw Gaussian outputs: reference E_SP=-1518.20029179 Eh, Gcorr_gas=0.296711 Eh; TS E_SP=-1518.18874360 Eh, Gcorr_gas=0.295488 Eh; 1 Eh=627.509474 kcal/mol; both stdout.log files SHA-256 match their provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log and provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log.",
    "mode_assignment": "N10-O5 cleavage candidate; TS has one imaginary mode at -82.8205 cm^-1 with opposite N10/O5 displacement, documented in provenance/TS3bda_author_route_strict_v2_mode_analysis.json",
    "value_kcal_mol": 6.4791545
  },
  "limitations": "This is the evaluator-scoped fixed 5bda/TS3bda endpoint calculation, not a full mechanism search. The historical 7.1753198314 kcal/mol value is retained in report/results.pre_strict_v2.json and provenance only as a diagnostic from the older all-atom SDD/SMD-optimization route; it is not the strict-v2 result. IRC is not required by this evaluator. No new Gaussian calculation is required for this synchronization.",
  "method": {
    "barrier_equation": "[E_SP(SMD,TS)+Gcorr_gas(TS)]-[E_SP(SMD,reference)+Gcorr_gas(reference)]",
    "electronic_structure": "B3LYP-D3(BJ)/GenECP gas-phase Opt/Freq (Ru=SDD; C,H,N,O=6-31G(d,p)), followed by B3LYP-D3(BJ)/def2-TZVP SMD(acetonitrile) single points",
    "software": "Gaussian 16 C.01",
    "solvent": "SMD(acetonitrile) for the matched def2-TZVP single points; gas phase for the Opt/Freq step",
    "temperature_K": 298.15
  },
  "status": "completed",
  "structures": {
    "reference": {
      "evidence": "artifacts/gaussian/5bda_author_route_strict_v2/parsed_observables.json; artifacts/gaussian/5bda_author_route_strict_v2/stdout.log; provenance/qzcli_hpc/5bda_author_route_strict_v2/1/status.json",
      "imaginary_frequency_count": 0,
      "optimized": true
    },
    "target": {
      "evidence": "artifacts/gaussian/TS3bda_author_route_strict_v2/parsed_observables.json; artifacts/gaussian/TS3bda_author_route_strict_v2/stdout.log; provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/status.json; provenance/TS3bda_author_route_strict_v2_mode_analysis.json",
      "imaginary_frequency_count": 1,
      "optimized": true
    }
  },
  "system": {
    "charge": 1,
    "multiplicity": 1,
    "reference_structure": "artifacts/gaussian/5bda_author_route_strict_v2/input.com",
    "target_structure": "artifacts/gaussian/TS3bda_author_route_strict_v2/input.com"
  }
}
```

Paper/SI document hashes:

- `papers/paper_e2d9397dff2a3f0f/documents/main.pdf` — SHA-256 `c24bbaae86761a8d40104b001d415708990565d075c29789011a3c8104993875` (declared_match=True)
- `papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf` — SHA-256 `1f4f524a63c1856d741bc9b9016079f9fe8ba2eea9117df6a2df9f72bd626975` (declared_match=True)

Report evidence lines retained:

- 本次只复现 evaluator 指定的 5bda/TS3bda 固定反应对和 N–O 断裂势垒，不扩展为整篇论文的机理搜索。正文/SI 路线为：`+1` 单重态；气相 B3LYP-D3(BJ) Opt/Freq，Ru 使用 SDD、C/H/N/O 使用 6-31G(d,p)；随后在优化结构上用 B3LYP-D3(BJ)/def2-TZVP/SMD(acetonitrile) 单点。strict-v2 输入用 Gaussian GenECP 明确实现了这一混合基组。
- 这与 evaluator 的 `6.2 ± 2.0 kcal/mol` 一致。N–O 模式、单一 TS 虚频和势垒三项关键点均闭合。
- 此前的 7.1753 kcal/mol 使用了全原子 SDD，并在 Opt/Freq 阶段加入 SMD，未实现 Ru/SDD 与 C/H/N/O/6-31G(d,p) 的混合基组；它只是方法不匹配诊断。strict-v2 结果已替代该记录，旧输入和日志仍在 provenance 中保留用于审计。evaluator 的 `+1` 单重态、固定 5bda/TS3bda 目标与 SI 一致，无需修改 evaluator。
- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **70**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/status.json` — successful status record; SHA-256 `588cbbeb77cb73602d383df79708004b56b4523dac7e54741e8db607cdfe1b31`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/5bda_SI_b3d3_cation_singlet_optimized.xyz` — successful execution artifact; SHA-256 `a17303e92edba35d4ffb7404fe0b9d05ae2e065dc601fec7a616555104fd273e`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/collection.json` — successful execution artifact; SHA-256 `79b9600e17be64dcf517652c53097357067697f7cefc3699282f1eb72ed1cc2e`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/formchk.log` — successful execution artifact; SHA-256 `ab224c3347fab85172b87ecf325bde69587017ee9790c2d1cd2b0b018591a7a7`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/input.com` — successful execution artifact; SHA-256 `23fc69170beaaec2316f0413914bc0da69ad4098aac38961e96495914bf9e3f2`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/status.json` — successful status record; SHA-256 `0d603d69921a377295c58a3a288657f9ac831a656ed6855a5a201fd64beb6458`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/5bda_SI_b3d3_doublet_diag_optimized.xyz` — successful execution artifact; SHA-256 `ca71601c75fda4284cbf4f0b891874441a6f1728839ad4210949354e31d2a302`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/collection.json` — successful execution artifact; SHA-256 `0daed98e18267b24ce989d6efcd8e84379fd0673464c189142289198cbb5b381`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/formchk.log` — successful execution artifact; SHA-256 `fcbec2cf6709b6e25a21a9f9610ca65117d36b35904b5e34d28da0d834c70aa1`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/input.com` — successful execution artifact; SHA-256 `057b93a4ea7c9e46bebd9aa6808d0ef23ba688fa569a8c239c55aa21fd7ceb5c`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/status.json` — successful status record; SHA-256 `4fecbeb289fd27d8598a4c2bd3ba61ceebe08956de46bf90a8e78638a229fbfb`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/5bda_SI_b3d3_doublet_retry_optimized.xyz` — successful execution artifact; SHA-256 `cb5bd066c24cc0947928bb4e0662a372d61c529ec1e790e6b74a69f1b47fa1b7`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/collection.json` — successful execution artifact; SHA-256 `97772d6ff537ca8f5ed397cb2df520cf80ec316ab9ec3148e69a0e1f74aac4ec`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/formchk.log` — successful execution artifact; SHA-256 `56ca41824782d435ee086c7ca856c6af315ebf35fc6c9c5aac6c137aa518865b`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/input.com` — successful execution artifact; SHA-256 `6e38a338652edbf01e376dc48e1f1b884871d9ef5b578fc238899e4042591f16`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/status.json` — successful status record; SHA-256 `b1ada006bb6bd2e238286abe72bb59174b9ed5d97f5d5e93d12907b394d5434f`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/5bda_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `a5c1e0951e16995a9d4d9cdbcbf0f1f4c2d9cdf197fcc36b948e1caf9fcda294`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `1e9076f349c2a9bfab6e922bb8d3a974c6637ad58013b3b753999f0a467a48b3`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `d903c563af24537d673d832313d4b289cc4d737df528f002fea8716db4262570`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `58c4aea3c20f595945d5d4b3a7964f9becac3f53585ff38f92440ee7be86b7c0`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/status.json` — successful status record; SHA-256 `4e94195c65d89b4a42232992b2f18c00368be79687d6823f1e00211d7d50eb94`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/TS3bda_SI_b3d3_cation_singlet_TS_optimized.xyz` — successful execution artifact; SHA-256 `0b59596be28154ade12c21c7ca2f3329ad2465098358fb1858c363a71b6a3045`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/collection.json` — successful execution artifact; SHA-256 `60bce8b037a9cfba12060ab476c3f462b018888186368ee4f5f869a79c2489c4`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/formchk.log` — successful execution artifact; SHA-256 `aa4a066a87136d9e2e2f8fc28c00dbf5c8b68956a88115783307064fbf5b8539`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/input.com` — successful execution artifact; SHA-256 `c68521450881a028b08a105c743b6eb422cb66b197adc720544952264aa8a789`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/status.json` — successful status record; SHA-256 `912022ac3e10e0449dd542936297b8ea0f8434d011fc3186f112b33464f2d1cf`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/TS3bda_SI_b3d3_doublet_ts_optimized.xyz` — successful execution artifact; SHA-256 `d0e1574313789ee908b80ba28fa6a3ab6cd65d83fb50057ef5d06fc8178a2d97`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/collection.json` — successful execution artifact; SHA-256 `808e837577c596edca3e4e24c8a5b8d7cb2842169ae1f15c81ed926d85a15871`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/formchk.log` — successful execution artifact; SHA-256 `824e688d5d7347236c58dd5a6cd0b6149b4ae65427dc2f93b132c6495c3dd8e2`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/input.com` — successful execution artifact; SHA-256 `aaa529f3409c5e0a62ef8493cd26899a9360e03d9ab681f2e6a91437b438b07f`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_author_route_strict_v2/status.json` — successful status record; SHA-256 `3867a8111fa323fda24822a94776faa7d022d5f06ee541aa5b57b6360abb2a49`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_author_route_strict_v2/TS3bda_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `cb9624744ff298e003a8a0dfed6b8770913a93f88888f009b9162c3d9c9fab8c`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `91725cc28d0518b66b1254da4c83364272802050d382ce9184e89e8a894aa9aa`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `c0e5d24af061f57bba9a3189c5aabd56e31515b4951fd151fc03840bb1a2b004`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `0da1938c30025882f421d185c367f6ff302d64ac46079b37cf348c6c810d2af5`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_cation_singlet/outputs/execution_jobs/job_5b45c8de70e64ae2b44b349204a34d21/status.json` — successful status record; SHA-256 `588cbbeb77cb73602d383df79708004b56b4523dac7e54741e8db607cdfe1b31`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_cation_singlet/outputs/execution_jobs/job_5b45c8de70e64ae2b44b349204a34d21/collection.json` — successful execution artifact; SHA-256 `79b9600e17be64dcf517652c53097357067697f7cefc3699282f1eb72ed1cc2e`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_cation_singlet/outputs/execution_jobs/job_5b45c8de70e64ae2b44b349204a34d21/input.com` — successful execution artifact; SHA-256 `23fc69170beaaec2316f0413914bc0da69ad4098aac38961e96495914bf9e3f2`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_cation_singlet/outputs/execution_jobs/job_5b45c8de70e64ae2b44b349204a34d21/request.json` — successful execution artifact; SHA-256 `15049c0956640d80f9807b7ef18bc0b0fcbe78b0313ee1dec9197a0871cc2a39`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_cation_singlet/outputs/execution_jobs/job_5b45c8de70e64ae2b44b349204a34d21/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_diag/outputs/execution_jobs/job_9bd8bf8e8cdf409dbc9fa11d4011ab55/status.json` — successful status record; SHA-256 `0d603d69921a377295c58a3a288657f9ac831a656ed6855a5a201fd64beb6458`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_diag/outputs/execution_jobs/job_9bd8bf8e8cdf409dbc9fa11d4011ab55/collection.json` — successful execution artifact; SHA-256 `0daed98e18267b24ce989d6efcd8e84379fd0673464c189142289198cbb5b381`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_diag/outputs/execution_jobs/job_9bd8bf8e8cdf409dbc9fa11d4011ab55/input.com` — successful execution artifact; SHA-256 `057b93a4ea7c9e46bebd9aa6808d0ef23ba688fa569a8c239c55aa21fd7ceb5c`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_diag/outputs/execution_jobs/job_9bd8bf8e8cdf409dbc9fa11d4011ab55/request.json` — successful execution artifact; SHA-256 `5e9a4072ab5420e2ee4a7d5cb2b120b8858e347254d6e54f91c293c889c4df01`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_diag/outputs/execution_jobs/job_9bd8bf8e8cdf409dbc9fa11d4011ab55/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_retry/outputs/execution_jobs/job_435c5157ab8e45bc83d3b51a63b83d53/status.json` — successful status record; SHA-256 `4fecbeb289fd27d8598a4c2bd3ba61ceebe08956de46bf90a8e78638a229fbfb`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_retry/outputs/execution_jobs/job_435c5157ab8e45bc83d3b51a63b83d53/collection.json` — successful execution artifact; SHA-256 `97772d6ff537ca8f5ed397cb2df520cf80ec316ab9ec3148e69a0e1f74aac4ec`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_retry/outputs/execution_jobs/job_435c5157ab8e45bc83d3b51a63b83d53/input.com` — successful execution artifact; SHA-256 `6e38a338652edbf01e376dc48e1f1b884871d9ef5b578fc238899e4042591f16`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_retry/outputs/execution_jobs/job_435c5157ab8e45bc83d3b51a63b83d53/request.json` — successful execution artifact; SHA-256 `bb7b7c2c026de62eb6b90e124822f083d6a07e94a9d0408cfdb415d1fadf6621`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/5bda_SI_b3d3_doublet_retry/outputs/execution_jobs/job_435c5157ab8e45bc83d3b51a63b83d53/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_cation_singlet_TS/outputs/execution_jobs/job_29170c4482d34b6a80f1908119f56dbd/status.json` — successful status record; SHA-256 `4e94195c65d89b4a42232992b2f18c00368be79687d6823f1e00211d7d50eb94`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_cation_singlet_TS/outputs/execution_jobs/job_29170c4482d34b6a80f1908119f56dbd/collection.json` — successful execution artifact; SHA-256 `60bce8b037a9cfba12060ab476c3f462b018888186368ee4f5f869a79c2489c4`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_cation_singlet_TS/outputs/execution_jobs/job_29170c4482d34b6a80f1908119f56dbd/input.com` — successful execution artifact; SHA-256 `c68521450881a028b08a105c743b6eb422cb66b197adc720544952264aa8a789`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_cation_singlet_TS/outputs/execution_jobs/job_29170c4482d34b6a80f1908119f56dbd/request.json` — successful execution artifact; SHA-256 `ab1b3457988826916a8edbb797bfa43574bca20e8c3296081718e4c17d80e488`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_cation_singlet_TS/outputs/execution_jobs/job_29170c4482d34b6a80f1908119f56dbd/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_doublet_ts/outputs/execution_jobs/job_713eb6df738345579203fbd39befff52/status.json` — successful status record; SHA-256 `912022ac3e10e0449dd542936297b8ea0f8434d011fc3186f112b33464f2d1cf`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_doublet_ts/outputs/execution_jobs/job_713eb6df738345579203fbd39befff52/collection.json` — successful execution artifact; SHA-256 `808e837577c596edca3e4e24c8a5b8d7cb2842169ae1f15c81ed926d85a15871`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_doublet_ts/outputs/execution_jobs/job_713eb6df738345579203fbd39befff52/input.com` — successful execution artifact; SHA-256 `aaa529f3409c5e0a62ef8493cd26899a9360e03d9ab681f2e6a91437b438b07f`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_doublet_ts/outputs/execution_jobs/job_713eb6df738345579203fbd39befff52/request.json` — successful execution artifact; SHA-256 `6e823d5abde99c00878e164b01d6444981b72f526758b029b859508bb5fbb0ce`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/native_workspace/TS3bda_SI_b3d3_doublet_ts/outputs/execution_jobs/job_713eb6df738345579203fbd39befff52/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/status.json` — successful status record; SHA-256 `6da2bf03c0cacd1290b211f8056fe65b745f0d759d33678a8d35bca4ce0d3278`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log` — successful execution artifact; SHA-256 `89942fd590f3732d69a458347f099236dcc17021d5ef8260441b80e6b5fc93a7`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/hpc_stdout.log` — successful execution artifact; SHA-256 `049872834f4532d28cc9f229bbc2bae377978f60241c4f42ff86f79dc2d01e1c`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/input.com` — successful execution artifact; SHA-256 `d903c563af24537d673d832313d4b289cc4d737df528f002fea8716db4262570`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/resource_adjustment.json` — successful execution artifact; SHA-256 `741ca319666f50d184308de40894b89944fab00be990f00f186b499e5a63a34c`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/status.json` — successful status record; SHA-256 `9414befde1b4f6e71ec1f54add791d98fb3739fb17a63a536bea8c312de4a3ba`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log` — successful execution artifact; SHA-256 `c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/hpc_stdout.log` — successful execution artifact; SHA-256 `c11a5ee32af9ef5d76381cf7f45a5edb0b1a02d9d76e106f3ae8297f752df94c`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/input.com` — successful execution artifact; SHA-256 `c0e5d24af061f57bba9a3189c5aabd56e31515b4951fd151fc03840bb1a2b004`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/resource_adjustment.json` — successful execution artifact; SHA-256 `95368e4d5d745326f7dc3e21110223de0c14856509446dc9f3cded20f673de75`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/5bda_SI_b3d3_doublet_diag/status.json` — label=group_3 paper_e2d9397dff2a3f0f 5bda_SI_b3d3_doublet_diag; submitted_at=2026-08-29T16:43:54.417957+00:00; software=gaussian; intent=optimization_frequency; route=#p UB3LYP/SDD EmpiricalDispersion=GD3BJ Opt Freq Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile) NoSymm Guess=Mix SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/5bda_SI_b3d3_doublet_diag_optimized.xyz`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/collection.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/formchk.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/parsed_observables.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/stderr.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_diag/stdout.log`
2. `artifacts/gaussian/5bda_SI_b3d3_doublet_retry/status.json` — label=group_3 paper_e2d9397dff2a3f0f 5bda_SI_b3d3_doublet_retry; submitted_at=2026-08-29T18:22:50.659623+00:00; software=gaussian; intent=optimization_frequency; route=#p UB3LYP/SDD EmpiricalDispersion=GD3BJ Opt Freq Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile) NoSymm Guess=Mix SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/5bda_SI_b3d3_doublet_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/collection.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/formchk.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/stderr.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_doublet_retry/stdout.log`
3. `artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/status.json` — label=group_3 paper_e2d9397dff2a3f0f TS3bda_SI_b3d3_doublet_ts; submitted_at=2026-08-29T18:23:14.434202+00:00; software=gaussian; intent=transition_state; route=#p UB3LYP/SDD EmpiricalDispersion=GD3BJ Opt=(TS,CalcFC,NoEigenTest) Freq Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile) NoSymm Guess=Mix SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/TS3bda_SI_b3d3_doublet_ts_optimized.xyz`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/collection.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/formchk.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/parsed_observables.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/stderr.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_doublet_ts/stdout.log`
4. `artifacts/gaussian/5bda_SI_b3d3_cation_singlet/status.json` — label=group_3 paper_e2d9397dff2a3f0f 5bda_SI_b3d3_cation_singlet; submitted_at=2026-08-30T01:38:37.866089+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/SDD EmpiricalDispersion=GD3BJ Opt Freq Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/5bda_SI_b3d3_cation_singlet_optimized.xyz`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/collection.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/formchk.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/parsed_observables.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/stderr.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_SI_b3d3_cation_singlet/stdout.log`
5. `artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/status.json` — label=group_3 paper_e2d9397dff2a3f0f TS3bda_SI_b3d3_cation_singlet_TS; submitted_at=2026-08-30T03:14:13.474525+00:00; software=gaussian; intent=transition_state; route=#p B3LYP/SDD EmpiricalDispersion=GD3BJ Opt=(TS,CalcFC,NoEigenTest,MaxStep=5) Freq Int=UltraFine SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/TS3bda_SI_b3d3_cation_singlet_TS_optimized.xyz`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/collection.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/formchk.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/parsed_observables.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/stderr.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_SI_b3d3_cation_singlet_TS/stdout.log`
6. `artifacts/gaussian/5bda_author_route_strict_v2/status.json` — label=None
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/5bda_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/5bda_author_route_strict_v2.fchk`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/5bda_author_route_strict_v2_optimized.xyz`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/formchk.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/parsed_observables.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/stdout.log`
7. `provenance/qzcli_hpc/5bda_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/5bda_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/5bda_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/sha256sums.txt`
8. `provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/TS3bda_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/sha256sums.txt`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `c_ar_limit`, `r_ar_limit`.

- Key-point IDs: `kp_ar_process_freq, kp_ar_process_ts, kp_ar_result_barrier`
- Conclusion IDs: `c_ar_final, c_ar_limit`
- Scoring-rule IDs: `r_ar_freq, r_ar_ts, r_ar_barrier, r_ar_final, r_ar_limit`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_freq` → reference `kp_ar_process_freq`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert validation; evaluator_target_present=False
- rule `r_ar_ts` → reference `kp_ar_process_ts`; type=condition; unit=not recorded; tolerance=not recorded; comparison=exact count plus expert mode assessment; evaluator_target_present=False
- rule `r_ar_barrier` → reference `kp_ar_result_barrier`; type=numeric; unit=kcal/mol; tolerance=2.0; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_final` → reference `c_ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_limit` → reference `c_ar_limit`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_ar_barrier` / reference `kp_ar_result_barrier`: target=6.2 kcal/mol; tolerance=2.0; numeric result leaves=[6.4791545]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.structures.reference` / result path `$.structures.reference.optimized` = `true`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.structures.reference` / result path `$.structures.reference.imaginary_frequency_count` = `0`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.structures.reference` / result path `$.structures.reference.evidence` = `"artifacts/gaussian/5bda_author_route_strict_v2/parsed_observables.json; artifacts/gaussian/5bda_author_route_strict_v2/stdout.log; provenance/qzcli_hpc/5bda_author_route_strict_v2/1/status.json"`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.structures.target` / result path `$.structures.target.optimized` = `true`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.structures.target` / result path `$.structures.target.imaginary_frequency_count` = `1`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.structures.target` / result path `$.structures.target.evidence` = `"artifacts/gaussian/TS3bda_author_route_strict_v2/parsed_observables.json; artifacts/gaussian/TS3bda_author_route_strict_v2/stdout.log; provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/status.json; provenance/TS3bda_author_route_stric..."`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.method` / result path `$.method.software` = `"Gaussian 16 C.01"`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.method` / result path `$.method.electronic_structure` = `"B3LYP-D3(BJ)/GenECP gas-phase Opt/Freq (Ru=SDD; C,H,N,O=6-31G(d,p)), followed by B3LYP-D3(BJ)/def2-TZVP SMD(acetonitrile) single points"`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.method` / result path `$.method.solvent` = `"SMD(acetonitrile) for the matched def2-TZVP single points; gas phase for the Opt/Freq step"`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.method` / result path `$.method.temperature_K` = `298.15`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.method` / result path `$.method.barrier_equation` = `"[E_SP(SMD,TS)+Gcorr_gas(TS)]-[E_SP(SMD,reference)+Gcorr_gas(reference)]"`
- rule `r_ar_freq` / reference `kp_ar_process_freq` / field `$.method` / result path `$.method.electrochemical_reference` = `null`
- rule `r_ar_ts` / reference `kp_ar_process_ts` / field `$.barrier.mode_assignment` / result path `$.barrier.mode_assignment` = `"N10-O5 cleavage candidate; TS has one imaginary mode at -82.8205 cm^-1 with opposite N10/O5 displacement, documented in provenance/TS3bda_author_route_strict_v2_mode_analysis.json"`
- rule `r_ar_barrier` / reference `kp_ar_result_barrier` / field `$.barrier.value_kcal_mol` / result path `$.barrier.value_kcal_mol` = `6.4791545`
- rule `r_ar_final` / reference `c_ar_final` / field `$.barrier.evidence` / result path `$.barrier.evidence` = `"Strict-v2 raw Gaussian outputs: reference E_SP=-1518.20029179 Eh, Gcorr_gas=0.296711 Eh; TS E_SP=-1518.18874360 Eh, Gcorr_gas=0.295488 Eh; 1 Eh=627.509474 kcal/mol; both stdout.log files SHA-256 match their provenance/qzcli_hpc/*/1/gauss..."`
- rule `r_ar_final` / reference `c_ar_final` / field `$.limitations` / result path `$.limitations` = `"This is the evaluator-scoped fixed 5bda/TS3bda endpoint calculation, not a full mechanism search. The historical 7.1753198314 kcal/mol value is retained in report/results.pre_strict_v2.json and provenance only as a diagnostic from the ol..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: charge/atom identity changed plus TS leakage
- Files changed in that review: `agent_input/data/inputs/reference.xyz, agent_input/data/inputs/target.xyz, agent_input/task.md, package_manifest.json, paper_route.md, task_info.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Public 48-atom XYZ reference starter for charge +1 singlet Ru-bda-Py; the transition-state coordinate is not agent-visible and must be generated independently.

Public input files and hashes:

- `agent_input/data/inputs/reference.xyz` — SHA-256 `e2575b0992397004a6f77a02a9ecab7552ae3595251e67bb359f915c05e157b4`; size=1537 bytes; xyz_atom_count=48; xyz_comment=charge +1 singlet Ru-bda-Py reference-side starter; preserve atom order; explicit_boundary_fields={"charge": "+1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_e2d9397dff2a3f0f/verification_report.md` — verification record; SHA-256 `54d2bd3181c62e352dc5abe81aa57ae005ad10fbc9201634601d56b1a26ef91f`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/report/results.json` — verification record; SHA-256 `5917944952fab7b1fafb776ea5cf14d457bbd9f8f70f44d464c8608f0ca1a028`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/parsed_observables.json` — referenced successful evidence; SHA-256 `58c4aea3c20f595945d5d4b3a7964f9becac3f53585ff38f92440ee7be86b7c0`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/5bda_author_route_strict_v2/stdout.log` — referenced successful evidence; SHA-256 `89942fd590f3732d69a458347f099236dcc17021d5ef8260441b80e6b5fc93a7`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_author_route_strict_v2/parsed_observables.json` — referenced successful evidence; SHA-256 `0da1938c30025882f421d185c367f6ff302d64ac46079b37cf348c6c810d2af5`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/artifacts/gaussian/TS3bda_author_route_strict_v2/stdout.log` — referenced successful evidence; SHA-256 `c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/TS3bda_author_route_strict_v2_mode_analysis.json` — referenced successful evidence; SHA-256 `a0e8da823d11d943f0de1c8ff8b317cdab2b81ba2a27e0d70ea5ffc4875f39a3`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log` — referenced successful evidence; SHA-256 `c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log` — referenced successful evidence; SHA-256 `89942fd590f3732d69a458347f099236dcc17021d5ef8260441b80e6b5fc93a7`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/status.json` — referenced successful evidence; SHA-256 `6da2bf03c0cacd1290b211f8056fe65b745f0d759d33678a8d35bca4ce0d3278`
- `docs/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/status.json` — referenced successful evidence; SHA-256 `9414befde1b4f6e71ec1f54add791d98fb3739fb17a63a536bea8c312de4a3ba`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
