# Verified computation reference — paper_9aa6d5655edfeb52 (autonomous_research)

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
| 118 | `QUALIFIED` | 严格优化几何 TD-B3LYP/6-31G(d,p)/IEFPCM(THF) 作业正常终止。HOMO-LUMO gap `4.3511 eV`；S1 `3.9220 eV` / `316.13 nm`，`f=0.2356`；跃迁分量见 `artifacts/author_td_analysis.json`。论文复现结论：`PASS`；评估任务合格性结论：`QUALIFIED`。该结论仅限孤立分子/连续介质边界，不外推为固态发光证明。 |
| 136 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 145 | `PASS` | - 论文复现结论：`PASS` |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Arene-Fused o-Carboranes via C–B(3) Bond Formation: Synthesis and Properties
- DOI: `10.1021/acs.inorgchem.5c04459`
- Task package: `tasks/final_verified_autonomous_research/paper_9aa6d5655edfeb52`
- Verification group: `docs/verification/group_1/paper_9aa6d5655edfeb52`
- Paper documents: `papers/paper_9aa6d5655edfeb52`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "excitations": [
    {
      "contributions": [
        {
          "coefficient": 0.69565,
          "from_orbital": 89,
          "to_orbital": 90
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 3.922
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.2356,
      "state_label": "S1",
      "wavelength": {
        "unit": "nm",
        "value": 316.13
      }
    },
    {
      "contributions": [
        {
          "coefficient": 0.49984,
          "from_orbital": 88,
          "to_orbital": 90
        },
        {
          "coefficient": 0.41347,
          "from_orbital": 89,
          "to_orbital": 91
        },
        {
          "coefficient": 0.26138,
          "from_orbital": 89,
          "to_orbital": 92
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 4.2421
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.0105,
      "state_label": "S2",
      "wavelength": {
        "unit": "nm",
        "value": 292.27
      }
    },
    {
      "contributions": [
        {
          "coefficient": -0.31892,
          "from_orbital": 88,
          "to_orbital": 90
        },
        {
          "coefficient": 0.5637,
          "from_orbital": 89,
          "to_orbital": 91
        },
        {
          "coefficient": -0.27139,
          "from_orbital": 89,
          "to_orbital": 92
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 4.4707
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.0148,
      "state_label": "S3",
      "wavelength": {
        "unit": "nm",
        "value": 277.32
      }
    },
    {
      "contributions": [
        {
          "coefficient": 0.68408,
          "from_orbital": 87,
          "to_orbital": 90
        },
        {
          "coefficient": 0.12434,
          "from_orbital": 88,
          "to_orbital": 90
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 4.6033
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.0104,
      "state_label": "S4",
      "wavelength": {
        "unit": "nm",
        "value": 269.34
      }
    },
    {
      "contributions": [
        {
          "coefficient": 0.69955,
          "from_orbital": 86,
          "to_orbital": 90
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 4.6863
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.0098,
      "state_label": "S5",
      "wavelength": {
        "unit": "nm",
        "value": 264.57
      }
    },
    {
      "contributions": [
        {
          "coefficient": 0.53368,
          "from_orbital": 85,
          "to_orbital": 90
        },
        {
          "coefficient": 0.16618,
          "from_orbital": 88,
          "to_orbital": 90
        },
        {
          "coefficient": 0.17019,
          "from_orbital": 88,
          "to_orbital": 91
        },
        {
          "coefficient": -0.33493,
          "from_orbital": 89,
          "to_orbital": 92
        },
        {
          "coefficient": -0.14821,
          "from_orbital": 89,
          "to_orbital": 95
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 5.1107
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.0384,
      "state_label": "S6",
      "wavelength": {
        "unit": "nm",
        "value": 242.6
      }
    },
    {
      "contributions": [
        {
          "coefficient": 0.54271,
          "from_orbital": 86,
          "to_orbital": 91
        },
        {
          "coefficient": -0.10946,
          "from_orbital": 87,
          "to_orbital": 91
        },
        {
          "coefficient": -0.28609,
          "from_orbital": 87,
          "to_orbital": 93
        },
        {
          "coefficient": -0.19239,
          "from_orbital": 88,
          "to_orbital": 91
        },
        {
          "coefficient": -0.10593,
          "from_orbital": 88,
          "to_orbital": 93
        },
        {
          "coefficient": -0.19112,
          "from_orbital": 89,
          "to_orbital": 93
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 5.1993
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.0102,
      "state_label": "S7",
      "wavelength": {
        "unit": "nm",
        "value": 238.46
      }
    },
    {
      "contributions": [
        {
          "coefficient": -0.212,
          "from_orbital": 85,
          "to_orbital": 90
        },
        {
          "coefficient": 0.12697,
          "from_orbital": 86,
          "to_orbital": 91
        },
        {
          "coefficient": -0.11282,
          "from_orbital": 87,
          "to_orbital": 91
        },
        {
          "coefficient": 0.6289,
          "from_orbital": 88,
          "to_orbital": 91
        }
      ],
      "energy": {
        "unit": "eV",
        "value": 5.2178
      },
      "multiplicity": "singlet",
      "oscillator_strength": 0.0344,
      "state_label": "S8",
      "wavelength": {
        "unit": "nm",
        "value": 237.62
      }
    },
    "<success-only excerpt: 8 of 20 entries>"
  ],
  "interpretation": {
    "author_hypothesis_assessment": "frontier transition contribution assessed from explicit amplitudes",
    "conclusion": "Author-level isolated-molecule frontier gap and lowest singlet are reproduced within evaluator tolerances; this does not prove solid-state emission."
  },
  "limitations": [
    "isolated-molecule/continuum-solvent model",
    "solid-state aggregation and emission are outside this calculation"
  ],
  "method": {
    "excited_state": "TD-B3LYP/6-31G(d,p), IEFPCM(THF), 20 singlets",
    "geometry_protocol": "Vertical TD on the final PCM minimum, not the historical gas-phase geometry; reference SCF energy cross-checked",
    "ground_state": "B3LYP/6-31G(d,p), IEFPCM(THF), Opt/Freq",
    "software": "Gaussian 16"
  },
  "orbital_properties": {
    "gap": {
      "unit": "eV",
      "value": 4.351100660733481
    },
    "homo": {
      "unit": "hartree",
      "value": -0.2283
    },
    "lumo": {
      "unit": "hartree",
      "value": -0.0684
    }
  },
  "selected_excitation": {
    "contributions": [
      {
        "coefficient": 0.69565,
        "from_orbital": 89,
        "to_orbital": 90
      }
    ],
    "energy": {
      "unit": "eV",
      "value": 3.922
    },
    "multiplicity": "singlet",
    "oscillator_strength": 0.2356,
    "selection_basis": "lowest explicitly parsed singlet state",
    "state_label": "S1",
    "wavelength": {
      "unit": "nm",
      "value": 316.13
    }
  },
  "status": "complete",
  "structure": {
    "charge": 0,
    "formula": "C18H20B10",
    "multiplicity": 1,
    "system_id": "compound_2a"
  },
  "validation": {
    "electronic_state_check": "neutral singlet; 138 positive frequencies; Opt/Freq minimum followed by TD singlets",
    "evidence": [
      "artifacts/author_td_analysis.json",
      "artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/gaussian.log",
      "artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/gaussian.log",
      "provenance/pcm_td_retry_manifest_20260911.json"
    ],
    "geometry_converged": true,
    "sensitivity_check": {
      "gap_change_ev": -0.005714391111657946,
      "s1_change_ev": -0.005199999999999871,
      "type": "reference-geometry sensitivity; old gas-phase-geometry TD retained only as a check"
    }
  },
  "verification_status": {
    "active_jobs": 0,
    "evaluation_qualification": "QUALIFIED",
    "executability": "READY",
    "paper_reproduction": "PASS",
    "progress_class": "A_COMPLETE_QUALIFIED",
    "recorded_at": "2026-09-11T17:28:59.262176+00:00",
    "recorded_wall_seconds": 95692.4,
    "source_snapshot": "results_md/GROUP1_VERIFICATION_PROGRESS_CURRENT.md"
  }
}
```

Paper/SI document hashes:

- `papers/paper_9aa6d5655edfeb52/documents/supplementary_001.pdf` — SHA-256 `a9ac1730b24a478de5e980909e145583d9ef54c525e9ef7f20f5174003d733bc` (declared_match=True)
- `papers/paper_9aa6d5655edfeb52/documents/main.pdf` — SHA-256 `e318b656b7b6cc8b1814ad47956ce676db9c80f09b1c0516211a9e1fc601a0af` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **76**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/status.json` — successful status record; SHA-256 `f06532f4040b15ff93e2572d9d3011263b9d9f33956cf2483194713ec6c95ae0`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/gaussian.log` — successful execution artifact; SHA-256 `17d3863c9d8f39a95e7c4b69b77577ecf7b16b116a69e1b877314e491d8c416f`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/hpc_summary.json` — successful execution artifact; SHA-256 `71abfb544cfed51bacb01c6e01c34c9f267823f8ba05aa9cd24d34f307d9edd5`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/input.com` — successful execution artifact; SHA-256 `416484f207592392289edc42f420610b4ae66f9b3f6d32ce07acebb70a7dcea0`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/status.json` — successful status record; SHA-256 `45dbb763f61749a0a5653dafaf85c4baa40860f77387c0a055d75c15f2ad5932`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/gaussian.log` — successful execution artifact; SHA-256 `e32a7d455d2b8457741fb76e3bc12b6f600950b199ee9a010fbd247ab57f4341`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/hpc_summary.json` — successful execution artifact; SHA-256 `3086b52b3671f2061c5ee2717794366b4c1f8ef4ed30bb5683f429a244ce12c7`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/input.com` — successful execution artifact; SHA-256 `4566eab1cbbea8cf7286e89c5ddaf0ded2cd9902d9b16a96e8202f643286c9fa`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/status.json` — successful status record; SHA-256 `331a5e7377c73eff3c31d99faefff8cee991b0bc38dc91d6f4c663e189d5ed46`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/borane_b3lyp_optfreq_unbounded_retry_summary.json` — successful execution artifact; SHA-256 `1d47034ab4a209045bd47285eed1eefeb9fd519b0b2edddb3662382b2c8ac0d2`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/collection.json` — successful execution artifact; SHA-256 `4e1f950396d2d18a6d3f22353c67a424cf016e177f6d93d67263b0273152a5a0`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/input.com` — successful execution artifact; SHA-256 `462d7febb65787ddb8a13d89c9f4a29b3d7c7107eea9feae27ce957feeb220e1`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/status.json` — successful status record; SHA-256 `9662d1213e4d02f6f3a5da2eadbb4ca66a64b73478c7f2f83d74ff76bb652505`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/collection.json` — successful execution artifact; SHA-256 `24255e5ca60534476eb468d57e412a2a81acf211614ee6bdd8021f1d1f847267`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/input.com` — successful execution artifact; SHA-256 `cd6442f07d3ef02f8f0f9a0852e5a2ed75d23eb798b23211783ff4bd2502cf65`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/stdout.log` — successful execution artifact; SHA-256 `ea569ddc281a0e05b63ca89c13440f88e34fbc21ed44e229e8e52c133e477a7a`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf__3543d247/status.json` — successful status record; SHA-256 `9662d1213e4d02f6f3a5da2eadbb4ca66a64b73478c7f2f83d74ff76bb652505`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf__3543d247/carborane_td_b3lyp_pcm_thf__3543d247_summary.json` — successful execution artifact; SHA-256 `684fc27c1d265f37abf6ebcfccca9bf2bd031e9dd4e8d0dbe2fb8c53e45e9fb7`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf__3543d247/collection.json` — successful execution artifact; SHA-256 `1153da7ce62df0d04821b72fafc756483f99ebbbdd2bbfafceb082c38802ab6e`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf__3543d247/input.com` — successful execution artifact; SHA-256 `cd6442f07d3ef02f8f0f9a0852e5a2ed75d23eb798b23211783ff4bd2502cf65`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf__3543d247/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/status.json` — successful status record; SHA-256 `a664db8e0ce599e2a63df7926b2914d36a864c30a2b2d7e0b807603b76c45988`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/carborane_td_optimized_author.xyz` — successful execution artifact; SHA-256 `228276f60ea12c84d9abc27f5bb41a09b269ad4021d545abc4fe6b29763f5f1f`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/carborane_td_optimized_author_summary.json` — successful execution artifact; SHA-256 `5764ffbc1640e3df33b3fdb751ee8269d6461a475d5bf18dc68fa996b552180d`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/collection.json` — successful execution artifact; SHA-256 `89da6435f505c67fdd77d10f7f1ede26d93a764c4c709161d75bc1642da4fa97`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/input.com` — successful execution artifact; SHA-256 `7d13fddd77b09772008f2d93ead0ee167459d8818dcb751e99e56e637959d38f`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/status.json` — successful status record; SHA-256 `c65f762b65ec77506745731bf22db49aaba5a4fd93bc1fc3d75956eb75086682`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/gaussian.log` — successful execution artifact; SHA-256 `b3130b2d05b861ac8451fe3f062415e1a931a610457c6793e53045b6d83fe132`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/hpc_summary.json` — successful execution artifact; SHA-256 `7f1c72f0be4e4ed795e1b31e8587e2918578c085abf00085e61df31eee5e5654`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/input.com` — successful execution artifact; SHA-256 `7d13fddd77b09772008f2d93ead0ee167459d8818dcb751e99e56e637959d38f`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/status.json` — successful status record; SHA-256 `eaaa744c377655a997a0e844347f7af5c39fc39f9b7db647e67ccce54900e40a`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `ffbee5bc2915e4d450cf3553e7636c4f64dd9db1386c738b4138845fd9fe5c40`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `bbc9af341129b21891a50a578582fcb37244b9f37782bdb73a1e118305352e40`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/optimized_geometry.metadata.json` — successful execution artifact; SHA-256 `951909ce20ffed3a13a669bb518a32c757baa599e7b170b3e59e8f765052eb02`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/optimized_geometry.xyz` — successful execution artifact; SHA-256 `43c1865aa9f30573d6340507790e16aed41021a73973762ad12862025713c056`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/status.json` — successful status record; SHA-256 `7cb5badc48ddeaf379527453725f95ef59219553f47436cab1c50196d802fd32`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/collection.json` — successful execution artifact; SHA-256 `93b39da57da834cab72b847c0ee07dc198e775c21cd443df13c95f3c9f60271c`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/input.com` — successful execution artifact; SHA-256 `3c6ebcaf9496069efc2eada03beb01b260183360f7472a56dda103cc1ee6b733`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/stdout.log` — successful execution artifact; SHA-256 `fc1d2f92488ee70506380acaac4e7ab3d0638698da66d7d2af229622fde35623`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_3543d247a4db476d948dca86b751bda6/status.json` — successful status record; SHA-256 `9662d1213e4d02f6f3a5da2eadbb4ca66a64b73478c7f2f83d74ff76bb652505`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_3543d247a4db476d948dca86b751bda6/collection.json` — successful execution artifact; SHA-256 `1153da7ce62df0d04821b72fafc756483f99ebbbdd2bbfafceb082c38802ab6e`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_3543d247a4db476d948dca86b751bda6/input.com` — successful execution artifact; SHA-256 `cd6442f07d3ef02f8f0f9a0852e5a2ed75d23eb798b23211783ff4bd2502cf65`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_3543d247a4db476d948dca86b751bda6/request.json` — successful execution artifact; SHA-256 `ea0ad2790a6ce4696a8ac26bcb1174b26f99008761a21e0da126395d480ea8b4`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_3543d247a4db476d948dca86b751bda6/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_5a2997ab439a4a0bacb56b1acbc8fe08/status.json` — successful status record; SHA-256 `a664db8e0ce599e2a63df7926b2914d36a864c30a2b2d7e0b807603b76c45988`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_5a2997ab439a4a0bacb56b1acbc8fe08/collection.json` — successful execution artifact; SHA-256 `89da6435f505c67fdd77d10f7f1ede26d93a764c4c709161d75bc1642da4fa97`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_5a2997ab439a4a0bacb56b1acbc8fe08/input.com` — successful execution artifact; SHA-256 `7d13fddd77b09772008f2d93ead0ee167459d8818dcb751e99e56e637959d38f`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_5a2997ab439a4a0bacb56b1acbc8fe08/request.json` — successful execution artifact; SHA-256 `41548646119c4fef26c18803066d45c7f25931a1253efc9ba08bafbbefb253f1`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_5a2997ab439a4a0bacb56b1acbc8fe08/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_7191867ea41448f9b09043a932b319e0/status.json` — successful status record; SHA-256 `331a5e7377c73eff3c31d99faefff8cee991b0bc38dc91d6f4c663e189d5ed46`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_7191867ea41448f9b09043a932b319e0/collection.json` — successful execution artifact; SHA-256 `4e1f950396d2d18a6d3f22353c67a424cf016e177f6d93d67263b0273152a5a0`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_7191867ea41448f9b09043a932b319e0/input.com` — successful execution artifact; SHA-256 `462d7febb65787ddb8a13d89c9f4a29b3d7c7107eea9feae27ce957feeb220e1`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_7191867ea41448f9b09043a932b319e0/request.json` — successful execution artifact; SHA-256 `0a3c1e20072b21f65ba370492699674bb0f51fc4b1afb1cb76a9155d51c53910`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_7191867ea41448f9b09043a932b319e0/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_92e434e2c717487eb1f1af166b54426f/status.json` — successful status record; SHA-256 `7cb5badc48ddeaf379527453725f95ef59219553f47436cab1c50196d802fd32`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_92e434e2c717487eb1f1af166b54426f/collection.json` — successful execution artifact; SHA-256 `93b39da57da834cab72b847c0ee07dc198e775c21cd443df13c95f3c9f60271c`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_92e434e2c717487eb1f1af166b54426f/input.com` — successful execution artifact; SHA-256 `3c6ebcaf9496069efc2eada03beb01b260183360f7472a56dda103cc1ee6b733`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_92e434e2c717487eb1f1af166b54426f/request.json` — successful execution artifact; SHA-256 `e038c07ca09c5793ef944742e353f734835d02af0f8ea380bb1e208d1e355e82`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_92e434e2c717487eb1f1af166b54426f/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_afbd2c253e234e768412aad6f7fc0da5/status.json` — successful status record; SHA-256 `eaaa744c377655a997a0e844347f7af5c39fc39f9b7db647e67ccce54900e40a`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_afbd2c253e234e768412aad6f7fc0da5/collection.json` — successful execution artifact; SHA-256 `ffbee5bc2915e4d450cf3553e7636c4f64dd9db1386c738b4138845fd9fe5c40`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_afbd2c253e234e768412aad6f7fc0da5/input.com` — successful execution artifact; SHA-256 `bbc9af341129b21891a50a578582fcb37244b9f37782bdb73a1e118305352e40`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_afbd2c253e234e768412aad6f7fc0da5/request.json` — successful execution artifact; SHA-256 `4cb226f5c4cc9101514ad700337fb1f533bab0889f39f7714d377a8be53b99ee`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/native_workspace_batch/outputs/execution_jobs/job_afbd2c253e234e768412aad6f7fc0da5/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/status.json` — successful status record; SHA-256 `f06532f4040b15ff93e2572d9d3011263b9d9f33956cf2483194713ec6c95ae0`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/gaussian.log` — successful execution artifact; SHA-256 `17d3863c9d8f39a95e7c4b69b77577ecf7b16b116a69e1b877314e491d8c416f`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/input.com` — successful execution artifact; SHA-256 `416484f207592392289edc42f420610b4ae66f9b3f6d32ce07acebb70a7dcea0`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/status.json` — successful status record; SHA-256 `45dbb763f61749a0a5653dafaf85c4baa40860f77387c0a055d75c15f2ad5932`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/gaussian.log` — successful execution artifact; SHA-256 `e32a7d455d2b8457741fb76e3bc12b6f600950b199ee9a010fbd247ab57f4341`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/input.com` — successful execution artifact; SHA-256 `4566eab1cbbea8cf7286e89c5ddaf0ded2cd9902d9b16a96e8202f643286c9fa`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/status.json` — successful status record; SHA-256 `c65f762b65ec77506745731bf22db49aaba5a4fd93bc1fc3d75956eb75086682`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/gaussian.log` — successful execution artifact; SHA-256 `b3130b2d05b861ac8451fe3f062415e1a931a610457c6793e53045b6d83fe132`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/input.com` — successful execution artifact; SHA-256 `7d13fddd77b09772008f2d93ead0ee167459d8818dcb751e99e56e637959d38f`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/status.json` — label=group_1 paper_9aa6d5655edfeb52 supp_carborane_b3lyp_optfreq; submitted_at=2026-08-29T10:21:15.178494+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/optimized_geometry.metadata.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/optimized_geometry.xyz`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/stdout.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_b3lyp_optfreq/supp_carborane_b3lyp_optfreq.chk`
2. `artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/status.json` — label=paper_9aa6d5655edfeb52 supp_carborane_td_b3lyp_thf unbounded_gaussian; submitted_at=2026-08-30T14:39:03.570908+00:00; software=gaussian; intent=single_point; route=#p TD(NStates=6) B3LYP/6-31G(d,p) SCRF=(PCM,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/collection.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/stderr.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/stdout.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/supp_carborane_td_b3lyp_thf.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/supp_carborane_td_b3lyp_thf.xyz`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/supp_carborane_td_b3lyp_thf/supp_carborane_td_b3lyp_thf_summary.json`
3. `artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/status.json` — label=group_1 docs/verification/group_1/paper_9aa6d5655edfeb52 carborane_td_b3lyp_pcm_thf; submitted_at=2026-08-30T16:52:59.953225+00:00; software=gaussian; intent=single_point; route=#p TD(NStates=20) B3LYP/6-31G(d,p) SCRF=(IEFPCM,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/carborane_td_b3lyp_pcm_thf.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/collection.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/stderr.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_b3lyp_pcm_thf/stdout.log`
4. `artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/status.json` — label=group_1 paper_9aa6d5655edfeb52 borane_b3lyp_optfreq unbounded_timeout_retry; submitted_at=2026-09-01T04:26:42.068537+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt=(CalcFC,MaxCycles=150) Freq NoSymm SCF=(XQC,MaxCycle=256); command=g16 < input.com
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/borane_b3lyp_optfreq.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/borane_b3lyp_optfreq_unbounded_retry_summary.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/collection.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/stderr.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/borane_b3lyp_optfreq_unbounded_retry/stdout.log`
5. `artifacts/gaussian_batch/carborane_td_optimized_author/status.json` — label=paper_9aa6d5655edfeb52 carborane_td_optimized_author unbounded_gaussian; submitted_at=2026-09-02T21:42:10.968247+00:00; software=gaussian; intent=single_point; route=#p TD(NStates=20) B3LYP/6-31G(d,p) SCRF=(IEFPCM,Solvent=THF); command=g16 < input.com
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/carborane_td_optimized_author.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/carborane_td_optimized_author.xyz`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/carborane_td_optimized_author_summary.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/collection.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/sha256sums.txt`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author/stderr.log`
6. `artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/status.json` — label=artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/status.json
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/author_b3lyp_pcm_thf_optfreq.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/gaussian.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/hpc_summary.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/sha256sums.txt`
7. `artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/status.json` — label=artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/status.json
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/author_pcm_thf_td_vertical_retry.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/gaussian.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/hpc_summary.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/sha256sums.txt`
8. `artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/status.json` — label=artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/status.json
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/carborane_td_optimized_author.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/gaussian.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/hpc_summary.json`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/carborane_td_optimized_author_hpc_351a2bbc/sha256sums.txt`
9. `provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/status.json` — label=provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/status.json
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/author_b3lyp_pcm_thf_optfreq.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/gaussian.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_b3lyp_pcm_thf_optfreq/hpc_20260910T094230Z_1369716/sha256sums.txt`
10. `provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/status.json` — label=provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/status.json
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/author_pcm_thf_td_vertical_retry.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/gaussian.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/author_pcm_thf_td_vertical_retry/hpc_20260911T094452Z_4062615/sha256sums.txt`
11. `provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/status.json` — label=provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/status.json
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/carborane_td_optimized_author.chk`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/fort.7`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/gaussian.log`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/input.com`
   - output: `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/qzcli_hpc/carborane_td_optimized_author/hpc_20260902T090854Z_3023246/sha256sums.txt`

## Evaluator alignment

- Key-point IDs: `kp_ar_process_geometry, kp_ar_process_excitation, kp_ar_gap, kp_ar_excitation, kp_ar_interpretation`
- Conclusion IDs: `con_ar_final`
- Scoring-rule IDs: `r_ar_process_geometry, r_ar_process_excitation, r_ar_gap, r_ar_excitation, r_ar_conclusion, r_ar_interpretation`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_process_geometry` → reference `kp_ar_process_geometry`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_ar_process_excitation` → reference `kp_ar_process_excitation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `r_ar_gap` → reference `kp_ar_gap`; type=numeric; unit=eV; tolerance=0.25; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_excitation` → reference `kp_ar_excitation`; type=numeric; unit=eV; tolerance=0.25; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_conclusion` → reference `con_ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_interpretation` → reference `kp_ar_interpretation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_ar_gap` / reference `kp_ar_gap`: target=4.3 eV; tolerance=0.25; numeric result leaves=[4.351100660733481]; within_tolerance=True; applicability=applicable
- rule `r_ar_excitation` / reference `kp_ar_excitation`: target=3.8591 eV; tolerance=0.25; numeric result leaves=[3.922]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.structure` / result path `$.structure.system_id` = `"compound_2a"`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.structure` / result path `$.structure.formula` = `"C18H20B10"`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.structure` / result path `$.structure.charge` = `0`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.structure` / result path `$.structure.multiplicity` = `1`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.validation.geometry_converged` / result path `$.validation.geometry_converged` = `true`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.validation.evidence` / result path `$.validation.evidence[0]` = `"artifacts/author_td_analysis.json"`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.validation.evidence` / result path `$.validation.evidence[1]` = `"artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/gaussian.log"`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.validation.evidence` / result path `$.validation.evidence[2]` = `"artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/gaussian.log"`
- rule `r_ar_process_geometry` / reference `kp_ar_process_geometry` / field `$.validation.evidence` / result path `$.validation.evidence[3]` = `"provenance/pcm_td_retry_manifest_20260911.json"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].state_label` = `"S1"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].energy.value` = `3.922`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].wavelength.value` = `316.13`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].oscillator_strength` = `0.2356`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].contributions[0].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[0].contributions[0].coefficient` = `0.69565`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].state_label` = `"S2"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].energy.value` = `4.2421`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].wavelength.value` = `292.27`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].oscillator_strength` = `0.0105`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[0].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[0].coefficient` = `0.49984`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[1].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[1].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[1].coefficient` = `0.41347`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[2].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[2].to_orbital` = `92`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[1].contributions[2].coefficient` = `0.26138`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].state_label` = `"S3"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].energy.value` = `4.4707`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].wavelength.value` = `277.32`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].oscillator_strength` = `0.0148`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[0].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[0].coefficient` = `-0.31892`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[1].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[1].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[1].coefficient` = `0.5637`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[2].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[2].to_orbital` = `92`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[2].contributions[2].coefficient` = `-0.27139`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].state_label` = `"S4"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].energy.value` = `4.6033`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].wavelength.value` = `269.34`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].oscillator_strength` = `0.0104`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].contributions[0].from_orbital` = `87`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].contributions[0].coefficient` = `0.68408`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].contributions[1].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].contributions[1].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[3].contributions[1].coefficient` = `0.12434`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].state_label` = `"S5"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].energy.value` = `4.6863`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].wavelength.value` = `264.57`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].oscillator_strength` = `0.0098`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].contributions[0].from_orbital` = `86`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[4].contributions[0].coefficient` = `0.69955`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].state_label` = `"S6"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].energy.value` = `5.1107`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].wavelength.value` = `242.6`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].oscillator_strength` = `0.0384`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[0].from_orbital` = `85`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[0].coefficient` = `0.53368`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[1].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[1].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[1].coefficient` = `0.16618`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[2].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[2].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[2].coefficient` = `0.17019`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[3].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[3].to_orbital` = `92`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[3].coefficient` = `-0.33493`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[4].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[4].to_orbital` = `95`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[5].contributions[4].coefficient` = `-0.14821`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].state_label` = `"S7"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].energy.value` = `5.1993`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].wavelength.value` = `238.46`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].oscillator_strength` = `0.0102`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[0].from_orbital` = `86`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[0].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[0].coefficient` = `0.54271`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[1].from_orbital` = `87`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[1].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[1].coefficient` = `-0.10946`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[2].from_orbital` = `87`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[2].to_orbital` = `93`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[2].coefficient` = `-0.28609`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[3].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[3].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[3].coefficient` = `-0.19239`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[4].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[4].to_orbital` = `93`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[4].coefficient` = `-0.10593`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[5].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[5].to_orbital` = `93`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[6].contributions[5].coefficient` = `-0.19112`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].state_label` = `"S8"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].energy.value` = `5.2178`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].wavelength.value` = `237.62`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].oscillator_strength` = `0.0344`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[0].from_orbital` = `85`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[0].coefficient` = `-0.212`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[1].from_orbital` = `86`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[1].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[1].coefficient` = `0.12697`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[2].from_orbital` = `87`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[2].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[2].coefficient` = `-0.11282`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[3].from_orbital` = `88`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[3].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[7].contributions[3].coefficient` = `0.6289`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].state_label` = `"S9"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].energy.value` = `5.2423`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].wavelength.value` = `236.51`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].oscillator_strength` = `0.0019`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[0].from_orbital` = `86`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[0].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[0].coefficient` = `0.12574`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[1].from_orbital` = `87`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[1].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[1].coefficient` = `-0.1734`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[2].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[2].to_orbital` = `93`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[2].coefficient` = `0.6531`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[3].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[3].to_orbital` = `94`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[8].contributions[3].coefficient` = `0.1181`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].state_label` = `"S10"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].energy.value` = `5.4087`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].wavelength.value` = `229.23`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].oscillator_strength` = `0.0094`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].contributions[0].from_orbital` = `87`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].contributions[0].to_orbital` = `91`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.excitations` / result path `$.excitations[9].contributions[0].coefficient` = `0.14774`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.state_label` = `"S1"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.multiplicity` = `"singlet"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.energy.value` = `3.922`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.energy.unit` = `"eV"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.wavelength.value` = `316.13`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.wavelength.unit` = `"nm"`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.oscillator_strength` = `0.2356`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.contributions[0].from_orbital` = `89`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.contributions[0].to_orbital` = `90`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.contributions[0].coefficient` = `0.69565`
- rule `r_ar_process_excitation` / reference `kp_ar_process_excitation` / field `$.selected_excitation` / result path `$.selected_excitation.selection_basis` = `"lowest explicitly parsed singlet state"`
- rule `r_ar_gap` / reference `kp_ar_gap` / field `$.orbital_properties.gap.value` / result path `$.orbital_properties.gap.value` = `4.351100660733481`
- rule `r_ar_conclusion` / reference `con_ar_final` / field `$.interpretation.conclusion` / result path `$.interpretation.conclusion` = `"Author-level isolated-molecule frontier gap and lowest singlet are reproduced within evaluator tolerances; this does not prove solid-state emission."`
- rule `r_ar_conclusion` / reference `con_ar_final` / field `$.limitations` / result path `$.limitations[0]` = `"isolated-molecule/continuum-solvent model"`
- rule `r_ar_conclusion` / reference `con_ar_final` / field `$.limitations` / result path `$.limitations[1]` = `"solid-state aggregation and emission are outside this calculation"`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained identity, charge/multiplicity, and SI Cartesian coordinates for compound 2a.

Public input files and hashes:

- `agent_input/data/inputs/2a.xyz` — SHA-256 `abf39525460bd67e3327bc6298b415f3f530d28b5bb00038302fbc7e72b763aa`; size=1805 bytes; xyz_atom_count=48; xyz_comment=compound 2a; neutral singlet; coordinates from SI; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/system.json` — SHA-256 `551e6a03c37f26bffafb1ea1ef8cbeb9fcae08686f5a3e6c74b3d82fe21131df`; size=397 bytes; explicit_boundary_fields={"$.charge": 0, "$.formula": "C18H20B10", "$.multiplicity": 1, "$.solvent_boundary": "isolated molecule; optional implicit solvent may be used and must be reported"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `agent_input/data/inputs/2a.xyz`

## Evidence files

- `docs/verification/group_1/paper_9aa6d5655edfeb52/verification_report.md` — verification record; SHA-256 `4784ac8158d90c1c1bfc3e8449a024cbcfb95a51ad5dfb93051e2ac0f049aea0`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/report/results.json` — verification record; SHA-256 `b8b2ee59164d8ae53549471a0c41a9ad271ccb865ec79c3616d2ead2b45e4c92`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/author_td_analysis.json` — referenced successful evidence; SHA-256 `1bac8363b4b41f4da7eb8cc0e31a42c21a2562a242f44de9187990d12362d2f3`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_b3lyp_pcm_thf_optfreq_hpc_08f2e6c7/gaussian.log` — referenced successful evidence; SHA-256 `17d3863c9d8f39a95e7c4b69b77577ecf7b16b116a69e1b877314e491d8c416f`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/artifacts/gaussian_batch/author_pcm_thf_td_vertical_retry_hpc_04714ad7/gaussian.log` — referenced successful evidence; SHA-256 `e32a7d455d2b8457741fb76e3bc12b6f600950b199ee9a010fbd247ab57f4341`
- `docs/verification/group_1/paper_9aa6d5655edfeb52/provenance/pcm_td_retry_manifest_20260911.json` — referenced successful evidence; SHA-256 `232c7448aab79be43a3081aa12f411b4fe191c367a76d13dde3e9e5d5d69d185`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
