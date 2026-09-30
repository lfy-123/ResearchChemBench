# Verified computation reference — paper_db6c4e0558113873 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 54 | `PASS` | 本篇 syn/anti 作者路线端点、结构映射和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Photo- and Copper Dual-Catalyzed Z-Selective Chlorosulfonylation of Allenes for Tetrasubstituted Alkenes
- DOI: `10.1021/jacs.5c17536`
- Task package: `tasks/final_verified_autonomous_research/paper_db6c4e0558113873`
- Verification group: `docs/verification/group_3/paper_db6c4e0558113873`
- Paper documents: `papers/paper_db6c4e0558113873`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "Validated author-route solution-phase comparison gives anti-minus-syn DeltaG=2.293 kcal/mol; the lower-energy state is syn_syn_Cu_Int_I_6b. Both C2-C3-C4 angles are measured from final atom-order-preserving geometries.",
  "conformer_handling": "The two fixed supplied structures were retained as distinct named states; no extra conformer was silently substituted.",
  "coverage": "Exactly the two public named 65-atom Cu/Cl intermediates.",
  "delta_g_kcal_mol": 2.29269998978067,
  "limitations": "One supplied conformer per named endpoint; composite gas-thermal/SMD-electronic free energies and DFT method choice are model dependent.",
  "protocol": {
    "basis": "LANL2DZ/ECP(Cu)+6-31G(d,p)(others) Opt/Freq; SDD/ECP(Cu)+6-311+G(d,p)(others) solution SP",
    "charge": 0,
    "frequency_validation": "Both gas minima have normal termination and zero imaginary modes.",
    "geometry_convergence": "Both named structures independently optimized.",
    "method": "B3LYP-D3BJ gas minimum plus M06 solution single point",
    "multiplicity": 1,
    "software": "Gaussian 16 C.01; cclib parser",
    "solvent": "SMD acetonitrile",
    "standard_state": "Gaussian 1 atm harmonic thermal correction combined with matched SMD electronic energy",
    "temperature_K": 298.15
  },
  "provenance": "Public SI XYZ -> author B3LYP-D3BJ mixed-basis Opt/Freq -> author M06/SDD+6-311+G(d,p)/SMD(acetonitrile) SP; raw decks, outputs and parsed JSON are archived.",
  "states": [
    {
      "angle_deg": 121.31748829129604,
      "atom_mapping": "C2-C3-C4 are carbon entries 2, 3 and 4 among the first four carbon rows (1-based public convention).",
      "energy": -2514.9180462599998,
      "evidence": [
        "artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log",
        "artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/stdout.log"
      ],
      "final_geometry": "artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/synsyn_author_b3d3_genecp_opt_freq_v2_optimized.xyz",
      "imaginary_modes": "zero",
      "name": "syn_syn_Cu_Int_I_6b",
      "outcome": "validated",
      "validation_status": "gas minimum plus matched solution single point"
    },
    {
      "angle_deg": 129.71190518794643,
      "atom_mapping": "C2-C3-C4 are carbon entries 2, 3 and 4 among the first four carbon rows (1-based public convention).",
      "energy": -2514.9143926099996,
      "evidence": [
        "artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log",
        "artifacts/gaussian/synanti_author_m06_sdd_acn_sp/stdout.log"
      ],
      "final_geometry": "artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/synanti_author_b3d3_genecp_opt_freq_v2_optimized.xyz",
      "imaginary_modes": "zero",
      "name": "syn_anti_Cu_Int_I_6b",
      "outcome": "validated",
      "validation_status": "gas minimum plus matched solution single point"
    }
  ],
  "uncertainty": "Estimated method/conformer sensitivity is several kcal/mol; no reference value is inserted."
}
```

Paper/SI document hashes:

- `papers/paper_db6c4e0558113873/documents/main.pdf` — SHA-256 `9b9d8841f0eb5ec7561cb770ad3bd43d0820639e443412d5da1bc74842318c8c` (declared_match=True)
- `papers/paper_db6c4e0558113873/documents/supplementary_001.pdf` — SHA-256 `a6585fbc4d364923517f436132456b23b012d972eeecb7a818a8a4259c1a6608` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |
- 独立计算完成后才读取 evaluator 对照；syn/anti 两态作者 composite route、零虚频、ΔG 差异、键角映射和稳定性趋势均已由原始输出闭合并与 evaluator 一致。
- 本篇 syn/anti 作者路线端点、结构映射和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **60**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/status.json` — successful status record; SHA-256 `31f1bad57f4a893378b8fe9ebe43e1c957d5a6488821918c276c5c81aaa60aa4`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/collection.json` — successful execution artifact; SHA-256 `e25b82b2f1e6a4f50f50b8806274cd3be723158f3a281981cd57190be5f6c22b`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/formchk.log` — successful execution artifact; SHA-256 `334507b681e9875b30014b3bec34338ca39aab8c35ab27a2d37022c9ae26937b`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/input.com` — successful execution artifact; SHA-256 `86e3b338fbf09489715bc90705f6121a811e29d4fa446e78a0e99138048734ed`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/parsed_observables.json` — successful execution artifact; SHA-256 `b8939c92cf0b43b69f0614c8e730015b67f2e619479b2226564bafdbf22691fd`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/status.json` — successful status record; SHA-256 `78784ab6c27c7d4fef0e4f8f9ba7ad10e85da96ff0f71f73573672cb031bc556`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/collection.json` — successful execution artifact; SHA-256 `9a09c02afbbff8c2e54cbe7ab9cd4b6bebeb1eca7b620c3360cd3c992dc0da1f`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/formchk.log` — successful execution artifact; SHA-256 `df5130739d20226673023bc02c8b3bc031c0b58c672ba454bfbace2649085689`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/input.com` — successful execution artifact; SHA-256 `0e344d0435149ca094cc96b1990ff8ccedb41aef32b9282648306672602994d5`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/parsed_observables.json` — successful execution artifact; SHA-256 `42bb9b0f2493ffb9281b1bc08612989519f53300acd964b10940855afbf27268`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/status.json` — successful status record; SHA-256 `e255764aca750f2a4f09d56d47d16e385aa234c172e2d8f723aedc954f090fc8`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/collection.json` — successful execution artifact; SHA-256 `687a11b06930a28de93dfcc42b868c65f3521525cfb77e41828ddc68f052638b`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/formchk.log` — successful execution artifact; SHA-256 `ac3f80fc6b6081f6ff465ee9161237963cf38a843384089ef5578ddb00eac33c`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/input.com` — successful execution artifact; SHA-256 `0a2be46216f572ebfd7e620b839331efa2ac1ed85066ced56bf67abc39a67e10`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/parsed_observables.json` — successful execution artifact; SHA-256 `7df3d98bf4b8b2c4662248fdeef3dae89f65b7007fc5ba4c352d04c6ea508316`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/status.json` — successful status record; SHA-256 `d4d8f23209c6d0660319f1570701bc4359a54192681be946a907e7d28053cbbd`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/collection.json` — successful execution artifact; SHA-256 `5a821b0cb5cffb993720754bac360a32c6388e0ecbb0086df11bc1e517767905`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/formchk.log` — successful execution artifact; SHA-256 `609f6d4cf20656e378da4ab00dbf17f16fafdc5390df549cca99c4d0f76eacfb`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/input.com` — successful execution artifact; SHA-256 `495f5e91edb6d0b78e4c1911a168a08f924868fea3ce93d2622277058abe9106`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/parsed_observables.json` — successful execution artifact; SHA-256 `8699a62a1a31e84c24a05354e7cb8c8fd85d523bd4e5d616ecdc0e540fab1fb3`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/status.json` — successful status record; SHA-256 `3290e7f70aa5badfbf6e1c9e6ef6b06e87761a0fb4498c64a715ac731be02745`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/collection.json` — successful execution artifact; SHA-256 `82adda407fd384411057d771eedaf84f1a27fa3aa884135f9dc16966e2169b67`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/formchk.log` — successful execution artifact; SHA-256 `3d176f40933dc59ee6940d2f5b15f04ae78392f11f9d4da7384102decf00ad45`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/input.com` — successful execution artifact; SHA-256 `c6f07f00fc283bceedfb1b0102de2b248c457f1675f702fc2315f72f951ed150`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/parsed_observables.json` — successful execution artifact; SHA-256 `ebd3c40583dff5775ba2ce02f10bf603750750c0598b9148dbc11f6df5ea1bb1`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/status.json` — successful status record; SHA-256 `a298620797bf9c6260b4c8cdcbdaa0a9fd313628dd20af61319bc810ac6efe0b`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/collection.json` — successful execution artifact; SHA-256 `dfdd092532421f5465ac65a1b76e6ee10b07ba73eafde8e888a4b0408d5f6a9e`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/formchk.log` — successful execution artifact; SHA-256 `74a6a35327c5210909f67189ec2c2cf2dddfe510d077ed808f7276e778777282`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/input.com` — successful execution artifact; SHA-256 `52b7730f81dbe8e2c77fe340001dab32a63241f80667710fc3fcb7ee718b6f38`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/parsed_observables.json` — successful execution artifact; SHA-256 `34b2cc72c373ead535ea7568e2e3c86c400c78b7bd08d87cc1a735e5f7c85c31`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_e938cee4fd4e495f99dd5c5a8d5ec29b/status.json` — successful status record; SHA-256 `31f1bad57f4a893378b8fe9ebe43e1c957d5a6488821918c276c5c81aaa60aa4`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_e938cee4fd4e495f99dd5c5a8d5ec29b/collection.json` — successful execution artifact; SHA-256 `e25b82b2f1e6a4f50f50b8806274cd3be723158f3a281981cd57190be5f6c22b`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_e938cee4fd4e495f99dd5c5a8d5ec29b/input.com` — successful execution artifact; SHA-256 `86e3b338fbf09489715bc90705f6121a811e29d4fa446e78a0e99138048734ed`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_e938cee4fd4e495f99dd5c5a8d5ec29b/request.json` — successful execution artifact; SHA-256 `a95dbf8de173a2b39f73082ddfe8d271fface967b272aac4b7e7690d4a95defc`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_e938cee4fd4e495f99dd5c5a8d5ec29b/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_m06_sdd_acn_sp/outputs/execution_jobs/job_28e41b9f123a4d348dadf0c6867cb835/status.json` — successful status record; SHA-256 `78784ab6c27c7d4fef0e4f8f9ba7ad10e85da96ff0f71f73573672cb031bc556`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_m06_sdd_acn_sp/outputs/execution_jobs/job_28e41b9f123a4d348dadf0c6867cb835/collection.json` — successful execution artifact; SHA-256 `9a09c02afbbff8c2e54cbe7ab9cd4b6bebeb1eca7b620c3360cd3c992dc0da1f`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_m06_sdd_acn_sp/outputs/execution_jobs/job_28e41b9f123a4d348dadf0c6867cb835/input.com` — successful execution artifact; SHA-256 `0e344d0435149ca094cc96b1990ff8ccedb41aef32b9282648306672602994d5`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_m06_sdd_acn_sp/outputs/execution_jobs/job_28e41b9f123a4d348dadf0c6867cb835/request.json` — successful execution artifact; SHA-256 `770e4c7260ff58989eb74964f0fe3122e7a3d05fbbc5a0a0d047cdff11a1ac88`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_author_m06_sdd_acn_sp/outputs/execution_jobs/job_28e41b9f123a4d348dadf0c6867cb835/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_b3lyp/outputs/execution_jobs/job_2322e012b0454ba2b7a73cd7565c3b9c/status.json` — successful status record; SHA-256 `e255764aca750f2a4f09d56d47d16e385aa234c172e2d8f723aedc954f090fc8`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_b3lyp/outputs/execution_jobs/job_2322e012b0454ba2b7a73cd7565c3b9c/collection.json` — successful execution artifact; SHA-256 `687a11b06930a28de93dfcc42b868c65f3521525cfb77e41828ddc68f052638b`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_b3lyp/outputs/execution_jobs/job_2322e012b0454ba2b7a73cd7565c3b9c/input.com` — successful execution artifact; SHA-256 `0a2be46216f572ebfd7e620b839331efa2ac1ed85066ced56bf67abc39a67e10`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_b3lyp/outputs/execution_jobs/job_2322e012b0454ba2b7a73cd7565c3b9c/request.json` — successful execution artifact; SHA-256 `e76182c1be80ce723e8b90b96ea22e76a18416651cbf9c8f34c342572e811c82`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synanti_b3lyp/outputs/execution_jobs/job_2322e012b0454ba2b7a73cd7565c3b9c/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_c525c6fe10414e68ba9c5cca95c8a652/status.json` — successful status record; SHA-256 `d4d8f23209c6d0660319f1570701bc4359a54192681be946a907e7d28053cbbd`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_c525c6fe10414e68ba9c5cca95c8a652/collection.json` — successful execution artifact; SHA-256 `5a821b0cb5cffb993720754bac360a32c6388e0ecbb0086df11bc1e517767905`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_c525c6fe10414e68ba9c5cca95c8a652/input.com` — successful execution artifact; SHA-256 `495f5e91edb6d0b78e4c1911a168a08f924868fea3ce93d2622277058abe9106`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_c525c6fe10414e68ba9c5cca95c8a652/request.json` — successful execution artifact; SHA-256 `46b0b5dac83c061e4b0e734223c1497085535c9cb2bb0cb4bc831dc5970ce8aa`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_b3d3_genecp_opt_freq_v2/outputs/execution_jobs/job_c525c6fe10414e68ba9c5cca95c8a652/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_m06_sdd_acn_sp/outputs/execution_jobs/job_09a06f533f2a4c84b239831818ec5256/status.json` — successful status record; SHA-256 `3290e7f70aa5badfbf6e1c9e6ef6b06e87761a0fb4498c64a715ac731be02745`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_m06_sdd_acn_sp/outputs/execution_jobs/job_09a06f533f2a4c84b239831818ec5256/collection.json` — successful execution artifact; SHA-256 `82adda407fd384411057d771eedaf84f1a27fa3aa884135f9dc16966e2169b67`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_m06_sdd_acn_sp/outputs/execution_jobs/job_09a06f533f2a4c84b239831818ec5256/input.com` — successful execution artifact; SHA-256 `c6f07f00fc283bceedfb1b0102de2b248c457f1675f702fc2315f72f951ed150`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_m06_sdd_acn_sp/outputs/execution_jobs/job_09a06f533f2a4c84b239831818ec5256/request.json` — successful execution artifact; SHA-256 `58b12f10d1e3a0f0ad99b4a5757de66a50e0bc8b097f914a74f9b1e65281dce6`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_author_m06_sdd_acn_sp/outputs/execution_jobs/job_09a06f533f2a4c84b239831818ec5256/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_b3lyp/outputs/execution_jobs/job_0dd89c4a5ab840d78db22cd16856f5c5/status.json` — successful status record; SHA-256 `a298620797bf9c6260b4c8cdcbdaa0a9fd313628dd20af61319bc810ac6efe0b`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_b3lyp/outputs/execution_jobs/job_0dd89c4a5ab840d78db22cd16856f5c5/collection.json` — successful execution artifact; SHA-256 `dfdd092532421f5465ac65a1b76e6ee10b07ba73eafde8e888a4b0408d5f6a9e`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_b3lyp/outputs/execution_jobs/job_0dd89c4a5ab840d78db22cd16856f5c5/input.com` — successful execution artifact; SHA-256 `52b7730f81dbe8e2c77fe340001dab32a63241f80667710fc3fcb7ee718b6f38`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_b3lyp/outputs/execution_jobs/job_0dd89c4a5ab840d78db22cd16856f5c5/request.json` — successful execution artifact; SHA-256 `1617941a1c88eac21a2fb7b0036befa45df53350b2e5cc546789f271ab923d6b`
- `docs/verification/group_3/paper_db6c4e0558113873/native_workspace/synsyn_b3lyp/outputs/execution_jobs/job_0dd89c4a5ab840d78db22cd16856f5c5/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/synanti_b3lyp/status.json` — label=group_3 paper_db6c4e0558113873 synanti_b3lyp; submitted_at=2026-08-29T07:43:29.708883+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/collection.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/formchk.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/input.com`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/stderr.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/stdout.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/synanti_b3lyp.chk`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_b3lyp/synanti_b3lyp.fchk`
2. `artifacts/gaussian/synsyn_b3lyp/status.json` — label=group_3 paper_db6c4e0558113873 synsyn_b3lyp; submitted_at=2026-08-29T07:43:30.469267+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/collection.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/formchk.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/input.com`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/stderr.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/stdout.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/synsyn_b3lyp.chk`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_b3lyp/synsyn_b3lyp.fchk`
3. `artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/status.json` — label=group_3 paper_db6c4e0558113873 synsyn_author_b3d3_genecp_opt_freq_v2; submitted_at=2026-08-31T02:41:31.418303+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/GenECP EmpiricalDispersion=GD3BJ Int=UltraFine Opt=(CalcFC,MaxCycles=512,MaxStep=8) Freq NoSymm SCF=(XQC,MaxCycle=4096); command=g16 < input.com
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/collection.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/formchk.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/input.com`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/parsed_observables.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stderr.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/synsyn_author_b3d3_genecp_opt_freq_v2.chk`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/synsyn_author_b3d3_genecp_opt_freq_v2.fchk`
4. `artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/status.json` — label=group_3 paper_db6c4e0558113873 synanti_author_b3d3_genecp_opt_freq_v2; submitted_at=2026-08-31T02:41:32.498971+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/GenECP EmpiricalDispersion=GD3BJ Int=UltraFine Opt=(CalcFC,MaxCycles=512,MaxStep=8) Freq NoSymm SCF=(XQC,MaxCycle=4096); command=g16 < input.com
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/collection.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/formchk.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/input.com`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/parsed_observables.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stderr.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/synanti_author_b3d3_genecp_opt_freq_v2.chk`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/synanti_author_b3d3_genecp_opt_freq_v2.fchk`
5. `artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/status.json` — label=group_3 paper_db6c4e0558113873 synsyn_author_m06_sdd_acn_sp; submitted_at=2026-09-01T01:57:30.074427+00:00; software=gaussian; intent=single_point; route=#p M06/GenECP SCRF=(SMD,Solvent=Acetonitrile) Int=UltraFine NoSymm SCF=(XQC,MaxCycle=4096); command=g16 < input.com
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/collection.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/formchk.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/input.com`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/stderr.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/stdout.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/synsyn_author_m06_sdd_acn_sp.chk`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/synsyn_author_m06_sdd_acn_sp.fchk`
6. `artifacts/gaussian/synanti_author_m06_sdd_acn_sp/status.json` — label=group_3 paper_db6c4e0558113873 synanti_author_m06_sdd_acn_sp; submitted_at=2026-09-01T01:57:32.135135+00:00; software=gaussian; intent=single_point; route=#p M06/GenECP SCRF=(SMD,Solvent=Acetonitrile) Int=UltraFine NoSymm SCF=(XQC,MaxCycle=4096); command=g16 < input.com
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/collection.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/formchk.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/input.com`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/stderr.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/stdout.log`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/synanti_author_m06_sdd_acn_sp.chk`
   - output: `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/synanti_author_m06_sdd_acn_sp.fchk`

## Evaluator alignment

- Key-point IDs: `kp_proc_minima, kp_energy, kp_angle`
- Conclusion IDs: `c_final_stability, c_final_distortion`
- Scoring-rule IDs: `r_proc, r_energy, r_angle_syn, r_angle_anti, r_conc_stability, r_conc_distortion`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_proc` → reference `kp_proc_minima`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert check of both named state records; evaluator_target_present=False
- rule `r_energy` → reference `kp_energy`; type=numeric; unit=kcal/mol; tolerance=1.0; comparison=absolute difference; sign anti minus syn; evaluator_target_present=True
- rule `r_angle_syn` → reference `kp_angle`; type=numeric; unit=degrees; tolerance=3.0; comparison=object-identified comparison for syn_syn_Cu_Int_I_6b; evaluator_target_present=True
- rule `r_angle_anti` → reference `kp_angle`; type=numeric; unit=degrees; tolerance=3.0; comparison=object-identified comparison for syn_anti_Cu_Int_I_6b; evaluator_target_present=True
- rule `r_conc_stability` → reference `c_final_stability`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_conc_distortion` → reference `c_final_distortion`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_energy` / reference `kp_energy`: target=2.3 kcal/mol; tolerance=1.0; numeric result leaves=[2.29269998978067]; within_tolerance=True; applicability=applicable
- rule `r_angle_syn` / reference `kp_angle`: target=123.7 degrees; tolerance=3.0; numeric result leaves=[121.31748829129604, 129.71190518794643]; within_tolerance=True; applicability=applicable
- rule `r_angle_anti` / reference `kp_angle`: target=129.7 degrees; tolerance=3.0; numeric result leaves=[121.31748829129604, 129.71190518794643]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_proc` / reference `kp_proc_minima` / field `$.states[].outcome` / result path `$.states[].outcome` = `"validated"`
- rule `r_proc` / reference `kp_proc_minima` / field `$.states[].evidence` / result path `$.states[].evidence[0]` = `"artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log"`
- rule `r_proc` / reference `kp_proc_minima` / field `$.states[].evidence` / result path `$.states[].evidence[1]` = `"artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/stdout.log"`
- rule `r_proc` / reference `kp_proc_minima` / field `$.states[].evidence` / result path `$.states[].evidence[0]` = `"artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log"`
- rule `r_proc` / reference `kp_proc_minima` / field `$.states[].evidence` / result path `$.states[].evidence[1]` = `"artifacts/gaussian/synanti_author_m06_sdd_acn_sp/stdout.log"`
- rule `r_energy` / reference `kp_energy` / field `$.delta_g_kcal_mol` / result path `$.delta_g_kcal_mol` = `2.29269998978067`
- rule `r_angle_syn` / reference `kp_angle` / field `$.states[].angle_deg` / result path `$.states[].angle_deg` = `121.31748829129604`
- rule `r_angle_syn` / reference `kp_angle` / field `$.states[].angle_deg` / result path `$.states[].angle_deg` = `129.71190518794643`
- rule `r_conc_stability` / reference `c_final_stability` / field `$.conclusion` / result path `$.conclusion` = `"Validated author-route solution-phase comparison gives anti-minus-syn DeltaG=2.293 kcal/mol; the lower-energy state is syn_syn_Cu_Int_I_6b. Both C2-C3-C4 angles are measured from final atom-order-preserving geometries."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized scored endpoints leakage
- Files changed in that review: `none recorded`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Two labeled 65-atom XYZ structures for the named neutral singlet model intermediates.

Public input files and hashes:

- `agent_input/data/inputs/syn_anti_Cu_Int_I_6b.xyz` — SHA-256 `a6897d63ebf04a81e24a0d3219ffd224783f29e6d4fbc953c2b48e575a90ff14`; size=2444 bytes; xyz_atom_count=65; xyz_comment=syn_anti_Cu_Int_I_6b; provided fixed-property input; neutral singlet; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/syn_syn_Cu_Int_I_6b.xyz` — SHA-256 `5631b796c6a37957338657964037c7897e3bf61c91821d3931124a5f4c67b6b3`; size=2443 bytes; xyz_atom_count=65; xyz_comment=syn_syn_Cu_Int_I_6b; provided fixed-property input; neutral singlet; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_db6c4e0558113873/verification_report.md` — verification record; SHA-256 `04d60eb59151c9e95801bd564a92a67dc52eff5ce32421ee597e7bcef08ae909`
- `docs/verification/group_3/paper_db6c4e0558113873/report/results.json` — verification record; SHA-256 `f2327675cafb44942e3069181fdb1723474e20690b1360ceb68bf3bfe6d5263e`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_b3d3_genecp_opt_freq_v2/stdout.log` — referenced successful evidence; SHA-256 `2738665dd6c4b30c506c3dbe047fe181581217981174be57b220b555ae378c50`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synanti_author_m06_sdd_acn_sp/stdout.log` — referenced successful evidence; SHA-256 `f4ce8acf91ae31dfddc30890b2cf39e7f9a41cf53f6d1beeade3538f8d8a5243`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_b3d3_genecp_opt_freq_v2/stdout.log` — referenced successful evidence; SHA-256 `7fe04537820456a5bf3ba387734df00dcc4d4d435a183b91b23b332ad473944e`
- `docs/verification/group_3/paper_db6c4e0558113873/artifacts/gaussian/synsyn_author_m06_sdd_acn_sp/stdout.log` — referenced successful evidence; SHA-256 `eb935229fce76ed80b61adf443c078c0e99f3a8f37fc494f83aece515a149158`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
