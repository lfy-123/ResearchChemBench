# Verified computation reference — paper_60f4c45810428116 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 8 | `BLOCKED` | - 最终状态：**BLOCKED** |
| 123 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 132 | `PASS` | - 论文复现结论：`PASS` |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Reductive Generation of Anionic C1 Carbenoid Species Attached to Organosulfur Functional Groups
- DOI: `10.1002/asia.70525`
- Task package: `tasks/final_verified_paper_reproduction/paper_60f4c45810428116`
- Verification group: `docs/verification/group_1/paper_60f4c45810428116`
- Paper documents: `papers/paper_60f4c45810428116`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "conclusion": "The explicit-GD3/LANL08 endpoint campaign gives -1.7438 V (1a) and -2.8225 V (1h) using the SI 5.36-V Fc calibration, reproducing the reported -1.75/-2.81 V values and the approximately 1.06-V ordering.",
    "difference_V": -1.0786593507901028,
    "independent_lanl08_values_V": {
      "1a": -0.6163106870793116,
      "1h": -1.6949700378694144
    },
    "ordering": "reaction_1h is more negative than reaction_1a; 1a is easier to reduce in this model.",
    "paper_reported_values_V": {
      "1a": -1.75,
      "1h": -2.81
    }
  },
  "limitations": [
    "The primary reported potentials use the SI absolute Fc calibration (5.36 V); the independently calculated LANL08 Fc/Fc+ absolute value is retained separately and must not be conflated with that calibration.",
    "One deterministic starting conformer is represented for each molecular endpoint.",
    "Thermodynamic redox endpoints do not establish reaction kinetics or a unique mechanism."
  ],
  "method": {
    "electronic_structure_method": "B3LYP/6-311+G(d,p) with EmpiricalDispersion=GD3; Fe reference uses recovered LANL08 gen/ECP",
    "reference_construction": "Fc/Fc+ LANL08 Gaussian G298 reference; primary potentials use the SI-stated 5.36 V absolute Fc calibration, with the independently computed LANL08 reference retained as a sensitivity result",
    "software": "Gaussian 16",
    "solvation_model": "SMD(THF)",
    "thermal_convention": "Gaussian harmonic thermal corrections at 298.15 K"
  },
  "reaction_1a": {
    "coverage": "precursor_1a -> radical_fragment_1a + chloride; one-electron dissociative reduction.",
    "outcome": "computed",
    "potential_V_vs_Fc": -1.7438244589954084,
    "reaction_free_energy_kJ_mol": -348.9078980899821,
    "validation_summary": "GD3/SMD(THF) molecular endpoint logs and LANL08 Fc/Fc+ reference logs all terminate normally."
  },
  "reaction_1h": {
    "coverage": "precursor_1h -> radical_fragment_1h + benzenethiolate; one-electron dissociative reduction.",
    "outcome": "computed",
    "potential_V_vs_Fc": -2.822483809785511,
    "reaction_free_energy_kJ_mol": -244.8330923810959,
    "validation_summary": "GD3/SMD(THF) molecular endpoint logs and LANL08 Fc/Fc+ reference logs all terminate normally."
  },
  "status": "complete",
  "validation": {
    "conformer_coverage": "All eight named endpoints are archived: two precursors, two radicals, two leaving fragments and Fc/Fc+.",
    "convergence_criterion": "Gaussian normal termination and Opt+Freq completion where applicable; raw logs and hashes are retained in artifacts/provenance.",
    "minimum_validation": "All molecular endpoints and both Fe reference logs terminate normally; frequency-bearing endpoints have zero imaginary modes. Chloride is a monoatomic endpoint with no vibrational modes.",
    "state_checks": [
      {
        "charge": 0,
        "multiplicity": 1,
        "species_id": "precursor_1a",
        "stoichiometry_checked": true
      },
      {
        "charge": 0,
        "multiplicity": 1,
        "species_id": "precursor_1h",
        "stoichiometry_checked": true
      },
      {
        "charge": 0,
        "multiplicity": 2,
        "species_id": "radical_1a",
        "stoichiometry_checked": true
      },
      {
        "charge": 0,
        "multiplicity": 2,
        "species_id": "radical_1h",
        "stoichiometry_checked": true
      },
      {
        "charge": -1,
        "multiplicity": 1,
        "species_id": "chloride",
        "stoichiometry_checked": true
      },
      {
        "charge": -1,
        "multiplicity": 1,
        "species_id": "benzenethiolate",
        "stoichiometry_checked": true
      },
      {
        "charge": 0,
        "multiplicity": 1,
        "species_id": "ferrocene",
        "stoichiometry_checked": true
      },
      {
        "charge": 1,
        "multiplicity": 2,
        "species_id": "ferrocenium",
        "stoichiometry_checked": true
      }
    ]
  }
}
```

Paper/SI document hashes:

- `papers/paper_60f4c45810428116/documents/supplementary_001.pdf` — SHA-256 `5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62` (declared_match=True)
- `papers/paper_60f4c45810428116/documents/main.pdf` — SHA-256 `7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **154**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/status.json` — successful status record; SHA-256 `bebd77475633fdd8f5f9aea7a5f926668e4447d994bb4012dfc997796d94751b`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/benzenethiolate_b3lypd3_optfreq.xyz` — successful execution artifact; SHA-256 `1d79f03c312e8210991f0e9599e5d38ba749838636af8fc7cfd825f4a96495d3`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/benzenethiolate_b3lypd3_optfreq_summary.json` — successful execution artifact; SHA-256 `3abeaa9b5221cdd2f2e83d26e72c01a340d06a0af91d72b82c557ec4e472ff14`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/collection.json` — successful execution artifact; SHA-256 `4feea90ed54fd17eb6b0e1b8d26e30f366f24ed60fc4585d880d596024e79d2e`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/input.com` — successful execution artifact; SHA-256 `5296be6e4311034eb262c24f4e66bca3d662d01a97849d7a631b4fbbdb418dc6`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/status.json` — successful status record; SHA-256 `7f7f683516e888f34b28998635901f6eaaa8f2d8de2e9a0ddc7c79ac1810c0fd`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/benzenethiolate_b3lypd3_optfreq_gd3_summary.json` — successful execution artifact; SHA-256 `67ad64b005a509c13aa3eec0a462e6ac752e784a30e6c353bd79f125a9df3195`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/collection.json` — successful execution artifact; SHA-256 `4b869ae51b268a889586f0680de917c0dc17a657cd950d147bc6fc8fbb4e2f10`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/input.com` — successful execution artifact; SHA-256 `c28ca24daf9987854a833309a306bf56674d6701841848a51f16af4cbd555877`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/status.json` — successful status record; SHA-256 `78de73e739ea230a2796ca75dc385aa417c2a5150483aaba0b14be888eb44830`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/chloride_b3lypd3_optfreq.xyz` — successful execution artifact; SHA-256 `b3f5797275bffe3ee5c67953264a58c856bb4077e84fcf7b69dc9911e632b34f`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/chloride_b3lypd3_optfreq_summary.json` — successful execution artifact; SHA-256 `146250942387d7d8a3ec5cbeff05296275b8aeb8080b9cd99f314a5521c42151`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/collection.json` — successful execution artifact; SHA-256 `ad0014fee0bda06d85c70229aac7508e3f34daf3cbd12fafdebd01954df42dde`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/input.com` — successful execution artifact; SHA-256 `c49f01091b9eb08a8ca3d0a2e27f7f324fc16e38ef8e7bae3dc7fb9728c6e003`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/status.json` — successful status record; SHA-256 `bd61c41435285cadbc6ebf01efbd3b663349b005e7b76211a496b77f6a5af71b`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/gaussian.log` — successful execution artifact; SHA-256 `465d74524854b4249124ab82aed285b0ebced7b09c1dfd95d9e66391fa1ada6d`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/hpc_summary.json` — successful execution artifact; SHA-256 `7fe2588611479ab5d58698cd66ea2282e87ab72dd2f0ddb0dd0dc15d37f5bb35`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/input.com` — successful execution artifact; SHA-256 `ad3ecacbd93788af1e07284fab6124e1affec478c0b663242290eba5e1ae2b22`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/status.json` — successful status record; SHA-256 `3cefc44b8dab9cc4026f24d8401ce67e3e2134897624c5d67e94fa7c88374f18`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/collection.json` — successful execution artifact; SHA-256 `ab145d0f38b22bbb1ccf0fb7d0b93b19776e713699bf0e4eb3a4c7e56af9446b`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry_summary.json` — successful execution artifact; SHA-256 `f6ae0aa224da60893114d6e751567d5717da58547a5a4a12f63fb35dfa79e78d`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/input.com` — successful execution artifact; SHA-256 `c7bcd53ca4feabcf8b86a4fbeea9741efd7ed5175c7e7bad841b348444011e23`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/status.json` — successful status record; SHA-256 `292759fdefad367d7a9e5a754d1ca06ac10686a9d1f769525928baa298bf65d8`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/gaussian.log` — successful execution artifact; SHA-256 `743e89ada54059802f1d9a1fbc6070a8d3c703519973eb6fffe392ce6ad0364c`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/hpc_summary.json` — successful execution artifact; SHA-256 `1c403955537658d4c0953b7ce1ba3d25c31a0d53c2b67e3885cca35421930a9f`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/input.com` — successful execution artifact; SHA-256 `169ce38b12a1a75edf9ad6dadec6a7e961a8695db0c9fb919ab15416fcea7db8`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/status.json` — successful status record; SHA-256 `a571ec71753de629c0402f074a9db07c8248ebdbec22cc3049d4f19d6c6ff861`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/collection.json` — successful execution artifact; SHA-256 `e7c1c2b89be575ece5c513655f57bf22490cbdd05a0ba9944c3999f62a15bd6d`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry_summary.json` — successful execution artifact; SHA-256 `aa182a36da4139f461000e682d17696572196aab0aa31adb43744fa4ce81da2f`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/input.com` — successful execution artifact; SHA-256 `0eead401304ae7a44685605aaac6d4a00d61b6bf2c63016a2669775f9ffc35f6`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/status.json` — successful status record; SHA-256 `6a0a266475f52225fd51fb8eeb8cd42aa6d97d9f4d20592bb7eb6fab37a54c95`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/collection.json` — successful execution artifact; SHA-256 `8b0e1512eb9591a607fc2fb1851b8d93c1fe06f64bd9a7b85f28b240043933f0`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/input.com` — successful execution artifact; SHA-256 `52f2f3b514235a8421a555ccb8cfee41c816a9ff3d80cfa645f9640aa0b617d9`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/precursor_1a_b3lypd3_optfreq.xyz` — successful execution artifact; SHA-256 `e710602a96f2b89bd7da8a57deafce6cd346b22b5fa2853b21af3943573792cf`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/precursor_1a_b3lypd3_optfreq_summary.json` — successful execution artifact; SHA-256 `a3e34344658d09f58f3d7c0a535a1d2ce431be6daec347cd32169ff70e5d86f6`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/status.json` — successful status record; SHA-256 `0444c11bef939dad0f417ac0c53b8635dff297da7a145391c9c6f1002f6c8511`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/collection.json` — successful execution artifact; SHA-256 `6e464fce965ebfd5879dc5dabf5013b840261bca9733bdbaa8495fbb336d6583`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/input.com` — successful execution artifact; SHA-256 `3782367d390c1906f3c70f22ae200d8f23f9f10769b48be0e8d4a025b2037a0f`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/precursor_1a_b3lypd3_optfreq_gd3_summary.json` — successful execution artifact; SHA-256 `be5cb080ad566f5d517c4f3eefba0ba2c6cd081f01ca51553a87c1f2c7daa623`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/status.json` — successful status record; SHA-256 `bbeed078509be0db7dfa74f1b04d77c5e7eb4ce70d6b6f9553ada595b2f704dc`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/collection.json` — successful execution artifact; SHA-256 `6a2e19fb5f7810c958d24259eb73496a4d93a57a80f2f5f9176b2c7e6197abfd`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/input.com` — successful execution artifact; SHA-256 `f2bedcd5ad16f01432b78e7a2a1d94ee1931ff05daca178e47ef4292e3c6e2d6`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/precursor_1h_b3lypd3_optfreq.xyz` — successful execution artifact; SHA-256 `f7ead7050ee2734f49d9245252bb10992d22352b319147d16141d26498aa1afe`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/precursor_1h_b3lypd3_optfreq_summary.json` — successful execution artifact; SHA-256 `4e3a1bb5805da9f5bf9fd6b4f42a19bec456394c2af82e01005282b2630d2f94`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/status.json` — successful status record; SHA-256 `934c8e032490010d7782376bdc954f8030a1b7dc50297e6f2ecc6091bbe35a2b`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/collection.json` — successful execution artifact; SHA-256 `4e66ae78498fc6f137b5f99438fb717ab3626ab4db1bdcb09cfdd29393ab6737`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/input.com` — successful execution artifact; SHA-256 `97df0f9801c39f29633b1a626b354d192d178fe8d367cd5e5b29ac4c4dabb680`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/precursor_1h_b3lypd3_optfreq_gd3_summary.json` — successful execution artifact; SHA-256 `d18b955faf21a9c32de60239e354c3b355d9a590be02f3533c6ca9695266e41a`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/status.json` — successful status record; SHA-256 `a73a0769572f0677f12e350ca9a15aa64d802d1a8b18212a0e4738fd1c642610`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/collection.json` — successful execution artifact; SHA-256 `1fd25492b6958e2cc1f18fa4315f4f315217e3c198fccf5fd8bd28e90fe31157`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/input.com` — successful execution artifact; SHA-256 `c3cec83fa7bb8349aa9095f4c6367c7e1b0b76be677e3a10f1385eb50fd086b0`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/radical_fragment_1a_b3lypd3_optfreq.xyz` — successful execution artifact; SHA-256 `f7d72862c2cc1a74d03fa636d1574a325b1bcd458a697e6e178db0c2cc05fc68`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/radical_fragment_1a_b3lypd3_optfreq_summary.json` — successful execution artifact; SHA-256 `b2ff1b4d2b3d83ccc193b92868448d38cd389ff3b49ee3270ea4bde5b8966217`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/status.json` — successful status record; SHA-256 `b55d24fe2aa8c6f3c7b2b32897a76546f73e64fd78a025e6ad6a7716a522d58e`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/collection.json` — successful execution artifact; SHA-256 `d5da2c00174997cd976cefcba110db943f93f3ac35e39a5b6425f15647a434be`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/input.com` — successful execution artifact; SHA-256 `21031c4a1e44b9ba02788f9f0f96e9d0f832e6b5845ae0cdb1933f8a1488ac71`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/radical_fragment_1a_b3lypd3_optfreq_gd3_summary.json` — successful execution artifact; SHA-256 `6ca9821e35ac289e9885c3794ec780791c559b7acf9b8e0e066e16f2e99d0462`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/status.json` — successful status record; SHA-256 `338c01656680365dc335cae1e606a2aaede2eef07374f11976f60a3fb3a0def9`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/collection.json` — successful execution artifact; SHA-256 `f2cf6c7997287ad0cea2de30722bda2ba6f70bb1e43155e168256aa1c3bdd02c`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/input.com` — successful execution artifact; SHA-256 `2d172ac46b7bc8b0c6bb711bcef6ff8b9ba8a5dd63ed1e83f8294f1155305f25`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/radical_fragment_1h_b3lypd3_optfreq.xyz` — successful execution artifact; SHA-256 `dbcc3158f3ee942c823cca3784f9b1a6fb2ec833f0f3d05cf2d050336cd76465`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/radical_fragment_1h_b3lypd3_optfreq_summary.json` — successful execution artifact; SHA-256 `b3a6c96bdb3f78d51e0662d1dfb80c986feb002d6dd7b35d0e1bafa1bd97d4e1`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/status.json` — successful status record; SHA-256 `17f1b2605f1f78a96e67255f5f1af610729aa3502245b8958d163b6be0576224`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/collection.json` — successful execution artifact; SHA-256 `e8d64e745f2d48736e15a4f284fb8aabaf9c0cc3c7207a9408a47ec586e1f19f`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/input.com` — successful execution artifact; SHA-256 `04efd92721ee986088f98aa10da136549bdb7f695e274cf9ef801c6a4142aec9`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/radical_fragment_1h_b3lypd3_optfreq_gd3_summary.json` — successful execution artifact; SHA-256 `3f8f7e7c55d5550ffab34a3c33763b08bedba52e4e46478329c1c38fa89755f3`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/status.json` — successful status record; SHA-256 `5c22f56dc92be27bafd72bbbe4b5e2d87035892e080dd8c64ea3badfd8917667`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/collection.json` — successful execution artifact; SHA-256 `96cc15fdc810519f40a8c1ae0e69d783fb7127069d8e003b8d57a3408cd85a03`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/input.com` — successful execution artifact; SHA-256 `f1a1000a6393ca4af488bca41241a1977025b397aa1d58dcd3bb09895bdb585c`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/stdout.log` — successful execution artifact; SHA-256 `1853b49a736660b91f14c73407cca9329692b887360c220a97f0b3440e633c13`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_06b7023e9f084ebca394b5c3b4e676dc/status.json` — successful status record; SHA-256 `3cefc44b8dab9cc4026f24d8401ce67e3e2134897624c5d67e94fa7c88374f18`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_06b7023e9f084ebca394b5c3b4e676dc/collection.json` — successful execution artifact; SHA-256 `ab145d0f38b22bbb1ccf0fb7d0b93b19776e713699bf0e4eb3a4c7e56af9446b`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_06b7023e9f084ebca394b5c3b4e676dc/input.com` — successful execution artifact; SHA-256 `c7bcd53ca4feabcf8b86a4fbeea9741efd7ed5175c7e7bad841b348444011e23`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_06b7023e9f084ebca394b5c3b4e676dc/request.json` — successful execution artifact; SHA-256 `fba51a05ca45794483c0b660e51236d538bdac543f93fb80b33bf220fdf47ce8`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_06b7023e9f084ebca394b5c3b4e676dc/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_12ead2e6c13f4b698fe479186618faeb/status.json` — successful status record; SHA-256 `17f1b2605f1f78a96e67255f5f1af610729aa3502245b8958d163b6be0576224`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_12ead2e6c13f4b698fe479186618faeb/collection.json` — successful execution artifact; SHA-256 `e8d64e745f2d48736e15a4f284fb8aabaf9c0cc3c7207a9408a47ec586e1f19f`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_12ead2e6c13f4b698fe479186618faeb/input.com` — successful execution artifact; SHA-256 `04efd92721ee986088f98aa10da136549bdb7f695e274cf9ef801c6a4142aec9`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_12ead2e6c13f4b698fe479186618faeb/request.json` — successful execution artifact; SHA-256 `97475b841ff2fe9aa9f7e8a6a43db6ff37c35870a50226a37b290235b145b0f0`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_12ead2e6c13f4b698fe479186618faeb/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_270863313c2b4173a816f59aa797ad87/status.json` — successful status record; SHA-256 `338c01656680365dc335cae1e606a2aaede2eef07374f11976f60a3fb3a0def9`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_270863313c2b4173a816f59aa797ad87/collection.json` — successful execution artifact; SHA-256 `f2cf6c7997287ad0cea2de30722bda2ba6f70bb1e43155e168256aa1c3bdd02c`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_270863313c2b4173a816f59aa797ad87/input.com` — successful execution artifact; SHA-256 `2d172ac46b7bc8b0c6bb711bcef6ff8b9ba8a5dd63ed1e83f8294f1155305f25`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_270863313c2b4173a816f59aa797ad87/request.json` — successful execution artifact; SHA-256 `420cf6b3d772d9c23111daa8f5e30f0b2b250b3fc0f7e40e84879171002c9e48`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_270863313c2b4173a816f59aa797ad87/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_41a401342b014c6ea5a7d2dbfbe93d1e/status.json` — successful status record; SHA-256 `934c8e032490010d7782376bdc954f8030a1b7dc50297e6f2ecc6091bbe35a2b`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_41a401342b014c6ea5a7d2dbfbe93d1e/collection.json` — successful execution artifact; SHA-256 `4e66ae78498fc6f137b5f99438fb717ab3626ab4db1bdcb09cfdd29393ab6737`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_41a401342b014c6ea5a7d2dbfbe93d1e/input.com` — successful execution artifact; SHA-256 `97df0f9801c39f29633b1a626b354d192d178fe8d367cd5e5b29ac4c4dabb680`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_41a401342b014c6ea5a7d2dbfbe93d1e/request.json` — successful execution artifact; SHA-256 `87fae96eff447f5f11f13a8fe9de916faf6401a9769c96ab35fcbcafba9fed8d`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_41a401342b014c6ea5a7d2dbfbe93d1e/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_5e0bdf162c5c42909fdc33dbc351e197/status.json` — successful status record; SHA-256 `0444c11bef939dad0f417ac0c53b8635dff297da7a145391c9c6f1002f6c8511`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_5e0bdf162c5c42909fdc33dbc351e197/collection.json` — successful execution artifact; SHA-256 `6e464fce965ebfd5879dc5dabf5013b840261bca9733bdbaa8495fbb336d6583`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_5e0bdf162c5c42909fdc33dbc351e197/input.com` — successful execution artifact; SHA-256 `3782367d390c1906f3c70f22ae200d8f23f9f10769b48be0e8d4a025b2037a0f`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_5e0bdf162c5c42909fdc33dbc351e197/request.json` — successful execution artifact; SHA-256 `685aa3cc4cf6fca4083b33b9a976a24631f4ee4625ef5c9ec8134980712120ae`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_5e0bdf162c5c42909fdc33dbc351e197/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_84cc57b2b53f44a0a7e64f0374cbbeaf/status.json` — successful status record; SHA-256 `b55d24fe2aa8c6f3c7b2b32897a76546f73e64fd78a025e6ad6a7716a522d58e`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_84cc57b2b53f44a0a7e64f0374cbbeaf/collection.json` — successful execution artifact; SHA-256 `d5da2c00174997cd976cefcba110db943f93f3ac35e39a5b6425f15647a434be`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_84cc57b2b53f44a0a7e64f0374cbbeaf/input.com` — successful execution artifact; SHA-256 `21031c4a1e44b9ba02788f9f0f96e9d0f832e6b5845ae0cdb1933f8a1488ac71`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_84cc57b2b53f44a0a7e64f0374cbbeaf/request.json` — successful execution artifact; SHA-256 `4c5c3be224d33863c57d44cb5b107e513a58f8dd81615f4816610b0dc37bab00`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_84cc57b2b53f44a0a7e64f0374cbbeaf/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_86554aa99cf94a8387196a2fd2d2e505/status.json` — successful status record; SHA-256 `bebd77475633fdd8f5f9aea7a5f926668e4447d994bb4012dfc997796d94751b`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_86554aa99cf94a8387196a2fd2d2e505/collection.json` — successful execution artifact; SHA-256 `4feea90ed54fd17eb6b0e1b8d26e30f366f24ed60fc4585d880d596024e79d2e`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_86554aa99cf94a8387196a2fd2d2e505/input.com` — successful execution artifact; SHA-256 `5296be6e4311034eb262c24f4e66bca3d662d01a97849d7a631b4fbbdb418dc6`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_86554aa99cf94a8387196a2fd2d2e505/request.json` — successful execution artifact; SHA-256 `ebcb0c01c5d1209455294d331c43041e88ca4721a69b5e1a2c0535ef831c005c`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_86554aa99cf94a8387196a2fd2d2e505/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_889ea8187099434da8acb81db580825a/status.json` — successful status record; SHA-256 `bbeed078509be0db7dfa74f1b04d77c5e7eb4ce70d6b6f9553ada595b2f704dc`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_889ea8187099434da8acb81db580825a/collection.json` — successful execution artifact; SHA-256 `6a2e19fb5f7810c958d24259eb73496a4d93a57a80f2f5f9176b2c7e6197abfd`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_889ea8187099434da8acb81db580825a/input.com` — successful execution artifact; SHA-256 `f2bedcd5ad16f01432b78e7a2a1d94ee1931ff05daca178e47ef4292e3c6e2d6`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_889ea8187099434da8acb81db580825a/request.json` — successful execution artifact; SHA-256 `9318e2e6bb2926ff879eb90fe01582755430cfb5056d1d2366fe4e1ee26eafdb`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_889ea8187099434da8acb81db580825a/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_a572675a7dde447aad789cd94059daf8/status.json` — successful status record; SHA-256 `5c22f56dc92be27bafd72bbbe4b5e2d87035892e080dd8c64ea3badfd8917667`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_a572675a7dde447aad789cd94059daf8/collection.json` — successful execution artifact; SHA-256 `96cc15fdc810519f40a8c1ae0e69d783fb7127069d8e003b8d57a3408cd85a03`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_a572675a7dde447aad789cd94059daf8/input.com` — successful execution artifact; SHA-256 `f1a1000a6393ca4af488bca41241a1977025b397aa1d58dcd3bb09895bdb585c`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_a572675a7dde447aad789cd94059daf8/request.json` — successful execution artifact; SHA-256 `d8f121b590f4660578e8a53aff8662f3cfc4e93beb6c50a1beb09ba8938c9a32`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_a572675a7dde447aad789cd94059daf8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_d200be182e784753bda702ff57d9b796/status.json` — successful status record; SHA-256 `a73a0769572f0677f12e350ca9a15aa64d802d1a8b18212a0e4738fd1c642610`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_d200be182e784753bda702ff57d9b796/collection.json` — successful execution artifact; SHA-256 `1fd25492b6958e2cc1f18fa4315f4f315217e3c198fccf5fd8bd28e90fe31157`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_d200be182e784753bda702ff57d9b796/input.com` — successful execution artifact; SHA-256 `c3cec83fa7bb8349aa9095f4c6367c7e1b0b76be677e3a10f1385eb50fd086b0`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_d200be182e784753bda702ff57d9b796/request.json` — successful execution artifact; SHA-256 `03aeb451ddfdf2483712f648a6c27b8de6b045b7226086718005f8fce98bd96d`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_d200be182e784753bda702ff57d9b796/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_e23713396f53498b9bd03a33e9f93e37/status.json` — successful status record; SHA-256 `7f7f683516e888f34b28998635901f6eaaa8f2d8de2e9a0ddc7c79ac1810c0fd`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_e23713396f53498b9bd03a33e9f93e37/collection.json` — successful execution artifact; SHA-256 `4b869ae51b268a889586f0680de917c0dc17a657cd950d147bc6fc8fbb4e2f10`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_e23713396f53498b9bd03a33e9f93e37/input.com` — successful execution artifact; SHA-256 `c28ca24daf9987854a833309a306bf56674d6701841848a51f16af4cbd555877`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_e23713396f53498b9bd03a33e9f93e37/request.json` — successful execution artifact; SHA-256 `2b379db40aa9014aa4c8a71e769cfcd0d80b57197697e4f20cd9281da5c9d7b1`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_e23713396f53498b9bd03a33e9f93e37/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_f346038b66ea4826a0c5222e15917065/status.json` — successful status record; SHA-256 `6a0a266475f52225fd51fb8eeb8cd42aa6d97d9f4d20592bb7eb6fab37a54c95`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_f346038b66ea4826a0c5222e15917065/collection.json` — successful execution artifact; SHA-256 `8b0e1512eb9591a607fc2fb1851b8d93c1fe06f64bd9a7b85f28b240043933f0`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_f346038b66ea4826a0c5222e15917065/input.com` — successful execution artifact; SHA-256 `52f2f3b514235a8421a555ccb8cfee41c816a9ff3d80cfa645f9640aa0b617d9`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_f346038b66ea4826a0c5222e15917065/request.json` — successful execution artifact; SHA-256 `1fe8fe123b3c8f6b9713729f940e1295b8d4031bff026b9856aa7ff2ff03affb`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_f346038b66ea4826a0c5222e15917065/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_fec18c7195824597acac21698041dc90/status.json` — successful status record; SHA-256 `78de73e739ea230a2796ca75dc385aa417c2a5150483aaba0b14be888eb44830`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_fec18c7195824597acac21698041dc90/collection.json` — successful execution artifact; SHA-256 `ad0014fee0bda06d85c70229aac7508e3f34daf3cbd12fafdebd01954df42dde`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_fec18c7195824597acac21698041dc90/input.com` — successful execution artifact; SHA-256 `c49f01091b9eb08a8ca3d0a2e27f7f324fc16e38ef8e7bae3dc7fb9728c6e003`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_fec18c7195824597acac21698041dc90/request.json` — successful execution artifact; SHA-256 `18caea8c91783d45c672aa6e338346dea7195723d7f4765b78967a78b918120f`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_fec18c7195824597acac21698041dc90/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_ff7ea47a591c455295fa3f28cdd738a6/status.json` — successful status record; SHA-256 `a571ec71753de629c0402f074a9db07c8248ebdbec22cc3049d4f19d6c6ff861`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_ff7ea47a591c455295fa3f28cdd738a6/collection.json` — successful execution artifact; SHA-256 `e7c1c2b89be575ece5c513655f57bf22490cbdd05a0ba9944c3999f62a15bd6d`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_ff7ea47a591c455295fa3f28cdd738a6/input.com` — successful execution artifact; SHA-256 `0eead401304ae7a44685605aaac6d4a00d61b6bf2c63016a2669775f9ffc35f6`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_ff7ea47a591c455295fa3f28cdd738a6/request.json` — successful execution artifact; SHA-256 `d4dd48e34a37276fe5c7c41728f426aa9c0e78f7fb572f62983d4c581fa4639a`
- `docs/verification/group_1/paper_60f4c45810428116/native_workspace_batch/outputs/execution_jobs/job_ff7ea47a591c455295fa3f28cdd738a6/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/status.json` — successful status record; SHA-256 `bd61c41435285cadbc6ebf01efbd3b663349b005e7b76211a496b77f6a5af71b`
- `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/gaussian.log` — successful execution artifact; SHA-256 `465d74524854b4249124ab82aed285b0ebced7b09c1dfd95d9e66391fa1ada6d`
- `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/input.com` — successful execution artifact; SHA-256 `ad3ecacbd93788af1e07284fab6124e1affec478c0b663242290eba5e1ae2b22`
- `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/status.json` — successful status record; SHA-256 `292759fdefad367d7a9e5a754d1ca06ac10686a9d1f769525928baa298bf65d8`
- `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/gaussian.log` — successful execution artifact; SHA-256 `743e89ada54059802f1d9a1fbc6070a8d3c703519973eb6fffe392ce6ad0364c`
- `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/input.com` — successful execution artifact; SHA-256 `169ce38b12a1a75edf9ad6dadec6a7e961a8695db0c9fb919ab15416fcea7db8`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/status.json` — label=paper_60f4c45810428116 benzenethiolate_b3lypd3_optfreq unbounded_gaussian; submitted_at=2026-08-29T23:58:01.263069+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/benzenethiolate_b3lypd3_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/benzenethiolate_b3lypd3_optfreq.xyz`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/benzenethiolate_b3lypd3_optfreq_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq/stdout.log`
2. `artifacts/gaussian_batch/chloride_b3lypd3_optfreq/status.json` — label=paper_60f4c45810428116 chloride_b3lypd3_optfreq unbounded_gaussian; submitted_at=2026-08-30T00:10:02.236409+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/chloride_b3lypd3_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/chloride_b3lypd3_optfreq.xyz`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/chloride_b3lypd3_optfreq_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/chloride_b3lypd3_optfreq/stdout.log`
3. `artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/status.json` — label=paper_60f4c45810428116 precursor_1a_b3lypd3_optfreq unbounded_gaussian; submitted_at=2026-08-30T00:10:32.301320+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/precursor_1a_b3lypd3_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/precursor_1a_b3lypd3_optfreq.xyz`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/precursor_1a_b3lypd3_optfreq_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq/stdout.log`
4. `artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/status.json` — label=paper_60f4c45810428116 precursor_1h_b3lypd3_optfreq unbounded_gaussian; submitted_at=2026-08-30T00:29:03.946512+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/precursor_1h_b3lypd3_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/precursor_1h_b3lypd3_optfreq.xyz`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/precursor_1h_b3lypd3_optfreq_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq/stdout.log`
5. `artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/status.json` — label=paper_60f4c45810428116 radical_fragment_1a_b3lypd3_optfreq unbounded_gaussian; submitted_at=2026-08-30T00:33:04.333675+00:00; software=gaussian; intent=optimization_frequency; route=#p UB3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/radical_fragment_1a_b3lypd3_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/radical_fragment_1a_b3lypd3_optfreq.xyz`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/radical_fragment_1a_b3lypd3_optfreq_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq/stdout.log`
6. `artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/status.json` — label=paper_60f4c45810428116 radical_fragment_1h_b3lypd3_optfreq unbounded_gaussian; submitted_at=2026-08-30T00:49:35.664597+00:00; software=gaussian; intent=optimization_frequency; route=#p UB3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/radical_fragment_1h_b3lypd3_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/radical_fragment_1h_b3lypd3_optfreq.xyz`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/radical_fragment_1h_b3lypd3_optfreq_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq/stdout.log`
7. `artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/status.json` — label=paper_60f4c45810428116 benzenethiolate_b3lypd3_optfreq_gd3 route_consistency unbounded_gaussian; submitted_at=2026-08-30T12:10:54.214651+00:00; software=gaussian; intent=optimization_frequency; route=#p EmpiricalDispersion=GD3 B3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/benzenethiolate_b3lypd3_optfreq_gd3.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/benzenethiolate_b3lypd3_optfreq_gd3_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/benzenethiolate_b3lypd3_optfreq_gd3/stdout.log`
8. `artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/status.json` — label=paper_60f4c45810428116 precursor_1a_b3lypd3_optfreq_gd3 route_consistency unbounded_gaussian; submitted_at=2026-08-30T12:10:54.284062+00:00; software=gaussian; intent=optimization_frequency; route=#p EmpiricalDispersion=GD3 B3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/precursor_1a_b3lypd3_optfreq_gd3.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/precursor_1a_b3lypd3_optfreq_gd3_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1a_b3lypd3_optfreq_gd3/stdout.log`
9. `artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/status.json` — label=paper_60f4c45810428116 precursor_1h_b3lypd3_optfreq_gd3 route_consistency unbounded_gaussian; submitted_at=2026-08-30T12:10:54.305919+00:00; software=gaussian; intent=optimization_frequency; route=#p EmpiricalDispersion=GD3 B3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/precursor_1h_b3lypd3_optfreq_gd3.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/precursor_1h_b3lypd3_optfreq_gd3_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/precursor_1h_b3lypd3_optfreq_gd3/stdout.log`
10. `artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/status.json` — label=paper_60f4c45810428116 radical_fragment_1a_b3lypd3_optfreq_gd3 route_consistency unbounded_gaussian; submitted_at=2026-08-30T12:10:54.328054+00:00; software=gaussian; intent=optimization_frequency; route=#p EmpiricalDispersion=GD3 UB3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/radical_fragment_1a_b3lypd3_optfreq_gd3.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/radical_fragment_1a_b3lypd3_optfreq_gd3_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1a_b3lypd3_optfreq_gd3/stdout.log`
11. `artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/status.json` — label=paper_60f4c45810428116 radical_fragment_1h_b3lypd3_optfreq_gd3 route_consistency unbounded_gaussian; submitted_at=2026-08-30T12:10:54.349543+00:00; software=gaussian; intent=optimization_frequency; route=#p EmpiricalDispersion=GD3 UB3LYP/6-311+G(d,p) Opt Freq SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/radical_fragment_1h_b3lypd3_optfreq_gd3.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/radical_fragment_1h_b3lypd3_optfreq_gd3_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/radical_fragment_1h_b3lypd3_optfreq_gd3/stdout.log`
12. `artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/status.json` — label=paper_60f4c45810428116 ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry unbounded_gaussian; submitted_at=2026-08-30T12:13:18.094630+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/genecp EmpiricalDispersion=GD3 Opt=(CalcFC,MaxCycles=200) Freq NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512) SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl2dz_optfreq_genecp_retry/stdout.log`
13. `artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/status.json` — label=paper_60f4c45810428116 ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry unbounded_gaussian; submitted_at=2026-08-30T12:13:18.119181+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/genecp EmpiricalDispersion=GD3 Opt=(CalcFC,MaxCycles=200) Freq NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512) SCRF=(SMD,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl2dz_optfreq_genecp_retry/stdout.log`
14. `artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/status.json` — label=group_1 paper_60f4c45810428116 supp_sulfur_precursor_m062x_optfreq; submitted_at=2026-09-01T03:53:58.815466+00:00; software=gaussian; intent=optimization_frequency; route=#p M062X/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/stdout.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/supp_sulfur_precursor_m062x_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/supp_sulfur_precursor_m062x_optfreq/supp_sulfur_precursor_m062x_optfreq_summary.json`
15. `artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/status.json` — label=artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/status.json
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/ferrocene_b3lypd3_lanl08_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/gaussian.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/hpc_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocene_b3lypd3_lanl08_optfreq_hpc_ef523054/sha256sums.txt`
16. `artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/status.json` — label=artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/status.json
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/ferrocenium_b3lypd3_lanl08_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/gaussian.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/hpc_summary.json`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/artifacts/gaussian_batch/ferrocenium_b3lypd3_lanl08_optfreq_hpc_7970bffd/sha256sums.txt`
17. `provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/status.json` — label=provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/status.json
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/ferrocene_b3lypd3_lanl08_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/gaussian.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocene_b3lypd3_lanl08_optfreq/hpc_20260909T120030Z_4053455/sha256sums.txt`
18. `provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/status.json` — label=provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/status.json
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/ferrocenium_b3lypd3_lanl08_optfreq.chk`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/fort.7`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/gaussian.log`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/input.com`
   - output: `docs/verification/group_1/paper_60f4c45810428116/provenance/qzcli_hpc/ferrocenium_b3lypd3_lanl08_optfreq/hpc_20260909T120033Z_4053455/sha256sums.txt`

## Evaluator alignment

- Key-point IDs: `kp_pr_process, kp_pr_1a, kp_pr_1h, kp_pr_order`
- Conclusion IDs: `c_pr_final`
- Scoring-rule IDs: `r_pr_process, r_pr_1a, r_pr_1h, r_pr_order, r_pr_final`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_pr_process` → reference `kp_pr_process`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison of per-state validation evidence; evaluator_target_present=False
- rule `r_pr_1a` → reference `kp_pr_1a`; type=numeric; unit=V vs Fc/Fc+; tolerance=0.2; comparison=absolute difference for reaction_1a only when applicable; evaluator_target_present=True
- rule `r_pr_1h` → reference `kp_pr_1h`; type=numeric; unit=V vs Fc/Fc+; tolerance=0.2; comparison=absolute difference for reaction_1h only when applicable; evaluator_target_present=True
- rule `r_pr_order` → reference `kp_pr_order`; type=ordering; unit=not recorded; tolerance=not recorded; comparison=ordering and quantitative consistency when applicable; evaluator_target_present=False
- rule `r_pr_final` → reference `c_pr_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison with scope limitation and outcome branch; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_pr_1a` / reference `kp_pr_1a`: target=-1.75 V vs Fc/Fc+; tolerance=0.2; numeric result leaves=[-1.7438244589954084]; within_tolerance=True; applicability=applicable
- rule `r_pr_1h` / reference `kp_pr_1h`: target=-2.81 V vs Fc/Fc+; tolerance=0.2; numeric result leaves=[-2.822483809785511]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[0].species_id` = `"precursor_1a"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[0].charge` = `0`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[0].multiplicity` = `1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[0].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[1].species_id` = `"precursor_1h"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[1].charge` = `0`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[1].multiplicity` = `1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[1].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[2].species_id` = `"radical_1a"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[2].charge` = `0`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[2].multiplicity` = `2`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[2].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[3].species_id` = `"radical_1h"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[3].charge` = `0`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[3].multiplicity` = `2`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[3].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[4].species_id` = `"chloride"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[4].charge` = `-1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[4].multiplicity` = `1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[4].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[5].species_id` = `"benzenethiolate"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[5].charge` = `-1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[5].multiplicity` = `1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[5].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[6].species_id` = `"ferrocene"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[6].charge` = `0`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[6].multiplicity` = `1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[6].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[7].species_id` = `"ferrocenium"`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[7].charge` = `1`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[7].multiplicity` = `2`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.state_checks` / result path `$.validation.state_checks[7].stoichiometry_checked` = `true`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.conformer_coverage` / result path `$.validation.conformer_coverage` = `"All eight named endpoints are archived: two precursors, two radicals, two leaving fragments and Fc/Fc+."`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.validation.minimum_validation` / result path `$.validation.minimum_validation` = `"All molecular endpoints and both Fe reference logs terminate normally; frequency-bearing endpoints have zero imaginary modes. Chloride is a monoatomic endpoint with no vibrational modes."`
- rule `r_pr_process` / reference `kp_pr_process` / field `$.method.reference_construction` / result path `$.method.reference_construction` = `"Fc/Fc+ LANL08 Gaussian G298 reference; primary potentials use the SI-stated 5.36 V absolute Fc calibration, with the independently computed LANL08 reference retained as a sensitivity result"`
- rule `r_pr_1a` / reference `kp_pr_1a` / field `$.reaction_1a.potential_V_vs_Fc` / result path `$.reaction_1a.potential_V_vs_Fc` = `-1.7438244589954084`
- rule `r_pr_1h` / reference `kp_pr_1h` / field `$.reaction_1h.potential_V_vs_Fc` / result path `$.reaction_1h.potential_V_vs_Fc` = `-2.822483809785511`
- rule `r_pr_order` / reference `kp_pr_order` / field `$.comparison.ordering` / result path `$.comparison.ordering` = `"reaction_1h is more negative than reaction_1a; 1a is easier to reduce in this model."`
- rule `r_pr_order` / reference `kp_pr_order` / field `$.comparison.difference_V` / result path `$.comparison.difference_V` = `-1.0786593507901028`
- rule `r_pr_final` / reference `c_pr_final` / field `$.comparison.conclusion` / result path `$.comparison.conclusion` = `"The explicit-GD3/LANL08 endpoint campaign gives -1.7438 V (1a) and -2.8225 V (1h) using the SI 5.36-V Fc calibration, reproducing the reported -1.75/-2.81 V values and the approximately 1.06-V ordering."`
- rule `r_pr_final` / reference `c_pr_final` / field `$.limitations` / result path `$.limitations[0]` = `"The primary reported potentials use the SI absolute Fc calibration (5.36 V); the independently calculated LANL08 Fc/Fc+ absolute value is retained separately and must not be conflated with that calibration."`
- rule `r_pr_final` / reference `c_pr_final` / field `$.limitations` / result path `$.limitations[1]` = `"One deterministic starting conformer is represented for each molecular endpoint."`
- rule `r_pr_final` / reference `c_pr_final` / field `$.limitations` / result path `$.limitations[2]` = `"Thermodynamic redox endpoints do not establish reaction kinetics or a unique mechanism."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Explicit species identities, charges, multiplicities, and dissociative reaction definitions.

Public input files and hashes:

- `agent_input/data/inputs/species.json` — SHA-256 `c61c9a50d56bae318bf31a5648eac563bb46412906f9f753f17275ea89ef39d9`; size=1844 bytes; explicit_boundary_fields={"$.solvent": "tetrahydrofuran", "$.species[0].formal_charge": 0, "$.species[0].multiplicity": 1, "$.species[0].smiles": "ClCSCc1ccccc1", "$.species[1].formal_charge": 0, "$.species[1].multiplicity": 2, "$.species[1].smiles": "[CH2]SCc1ccccc1", "$.species[2].formal_charge": -1, "$.species[2].multiplicity": 1, "$.species[2].smiles": "[Cl-]", "$.species[3].formal_charge": 0, "$.species[3].multiplicity": 1, "$.species[3].smiles": "c1ccccc1SCSCc1ccccc1", "$.species[4].formal_charge": 0, "$.species[4].multiplicity": 2, "$.species[4].smiles": "[CH2]SCc1ccccc1", "$.species[5].formal_charge": -1, "$.species[5].multiplicity": 1, "$.species[5].smiles": "c1ccccc1[S-]", "$.species[6].formal_charge": 0, "$.species[6].multiplicity": 1, "$.species[6].smiles": "[Fe]1([cH]2[cH][cH][cH][cH]2)[cH]2[cH][cH][cH][cH]2", "$.species[7].formal_charge": 1, "$.species[7].multiplicity": 2, "$.species[7].smiles": "[Fe+]1([cH]2[cH][cH][cH][cH]2)[cH]2[cH][cH][cH][cH]2", "$.temperature_K": 298.15}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_1/paper_60f4c45810428116/verification_report.md` — verification record; SHA-256 `a5b9b83c0052b51d3e251c9d6d63a9cb74943bb56b54051c5df72864b627f0f1`
- `docs/verification/group_1/paper_60f4c45810428116/report/results.json` — verification record; SHA-256 `e16afcfeb879923e01a53cb062672968d112afd94ba12b3f52619d6fa09816d4`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
