# Verified computation reference — paper_d3b4575397179146 (paper_reproduction)

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
| 8 | `BLOCKED` | - 最终状态：**BLOCKED** |
| 200 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 209 | `PASS` | - 论文复现结论：`PASS` |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Triaryl-Heptazine Photocatalysts for the Oxidation of C–H and C–C Bonds in Nitrogen-Containing Molecules
- DOI: `10.1021/acscatal.5c08082`
- Task package: `tasks/final_verified_paper_reproduction/paper_d3b4575397179146`
- Verification group: `docs/verification/group_1/paper_d3b4575397179146`
- Paper documents: `papers/paper_d3b4575397179146`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "limitations": "The conclusion is limited to isolated-molecule vertical singlet excitations. The initial literal PBE0 decks failed because Gaussian rejects PBE0 as a TD post-SCF method; the successful PBE1PBE keyword is the Gaussian implementation of PBE0 and its input/logs are retained. Cube localization is a stated partition diagnostic, not a solid-state or catalytic prediction.",
  "overall_conclusion": "Within the isolated-molecule vertical-excitation scope, the four neutral singlets have completed B3LYP ground-state minimum checks and 18-state TD-PBE0 calculations. Gaussian represents PBE0 as the PBE1PBE keyword; the parsed PBE1PBE outputs support the reported HOMO-to-LUMO assignment for dFHeptZ/dClHeptZ/dMeHeptZ and the distinct HOMO-3-to-LUMO assignment and substituent-localized HOMO for dOMeHeptZ.",
  "provenance": {
    "methods": "B3LYP/6-311+G(d,p) Opt+Freq; TD(Singlets,NStates=18) PBE1PBE/6-311+G(d,p), the Gaussian keyword for PBE0",
    "software_or_code": "Gaussian 16 C.01; paper-local Gaussian log parser and cube localization parser",
    "solvent": "IEFPCM acetonitrile for TD-DFT",
    "state_count_or_scope": "Four neutral singlets; 18 vertical singlet states per molecule"
  },
  "status": "complete",
  "systems": [
    {
      "identity": {
        "charge": 0,
        "evidence": [
          "tasks/paper_reproduction/paper_d3b4575397179146/agent_input/data/inputs/heptazines.json"
        ],
        "formula": "C24H9F6N7",
        "multiplicity": 1,
        "name": "2,5,8-tris(2,4-difluorophenyl)-1,3,3a1,4,6,7,9-heptaazaphenalene",
        "smiles": "Fc1ccc(C2=NC3=NC(c4ccc(F)cc4F)=NC4=NC(c5ccc(F)cc5F)=NC(=N2)N34)c(F)c1"
      },
      "orbital_localization": {
        "criterion": "squared cube amplitude assigned by the recorded core/substituent atom partition",
        "evidence": [
          "artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/gaussian.log",
          "artifacts/orbital_cubes_repaired/dFHeptZ/homo.cube",
          "artifacts/orbital_cubes_repaired/dFHeptZ/lumo.cube"
        ],
        "homo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.978589121735564,
          "core_fraction_above_isovalue_0_02": 1.0,
          "cube": "artifacts/orbital_cubes_repaired/dFHeptZ/homo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 1.0001563769061048,
          "orbital_ids": "<nested value omitted>",
          "sha256": "89ab49f23f286edc2ae9a82776b15b264b491ebe9226cc756447612d517ec65e"
        },
        "lumo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.7138885055243387,
          "core_fraction_above_isovalue_0_02": 0.7743559581009175,
          "cube": "artifacts/orbital_cubes_repaired/dFHeptZ/lumo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 1.000182034087841,
          "orbital_ids": "<nested value omitted>",
          "sha256": "a9fcf7079821c02dba3545464996a8877d2d0dce6a61df35301296cbbf9a9053"
        }
      },
      "system_conclusion": "dFHeptZ: 18 singlet TD states were parsed. The lowest visible/near-visible state is 2.9647 eV (418.21 nm); the dominant orbital assignment and the recorded HOMO localization distinguish dOMeHeptZ from the other three.",
      "system_id": "dFHeptZ",
      "transitions": [
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 2.9647,
          "oscillator_strength": 0.0,
          "state_number": 1,
          "wavelength_nm": 418.21
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7374,
          "oscillator_strength": 0.1363,
          "state_number": 2,
          "wavelength_nm": 331.74
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7599,
          "oscillator_strength": 0.64,
          "state_number": 3,
          "wavelength_nm": 329.76
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7719,
          "oscillator_strength": 0.5533,
          "state_number": 4,
          "wavelength_nm": 328.7
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.8394,
          "oscillator_strength": 0.0142,
          "state_number": 5,
          "wavelength_nm": 322.92
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.8454,
          "oscillator_strength": 0.058,
          "state_number": 6,
          "wavelength_nm": 322.42
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.9792,
          "oscillator_strength": 0.0,
          "state_number": 7,
          "wavelength_nm": 311.58
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 4.0917,
          "oscillator_strength": 0.1107,
          "state_number": 8,
          "wavelength_nm": 303.01
        },
        "<success-only excerpt: 8 of 18 entries>"
      ],
      "validation": {
        "charge": 0,
        "evidence": [
          "artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json"
        ],
        "imaginary_frequency_count": 0,
        "multiplicity": 1,
        "normal_termination": true,
        "optimization_converged": true
      }
    },
    {
      "identity": {
        "charge": 0,
        "evidence": [
          "tasks/paper_reproduction/paper_d3b4575397179146/agent_input/data/inputs/heptazines.json"
        ],
        "formula": "C24H9Cl6N7",
        "multiplicity": 1,
        "name": "2,5,8-tris(2,4-dichlorophenyl)-1,3,3a1,4,6,7,9-heptaazaphenalene",
        "smiles": "Clc1ccc(C2=NC3=NC(c4ccc(Cl)cc4Cl)=NC4=NC(c5ccc(Cl)cc5Cl)=NC(=N2)N34)c(Cl)c1"
      },
      "orbital_localization": {
        "criterion": "squared cube amplitude assigned by the recorded core/substituent atom partition",
        "evidence": [
          "artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/gaussian.log",
          "artifacts/orbital_cubes_repaired/dClHeptZ/homo.cube",
          "artifacts/orbital_cubes_repaired/dClHeptZ/lumo.cube"
        ],
        "homo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.9485213782179684,
          "core_fraction_above_isovalue_0_02": 0.9868347099803526,
          "cube": "artifacts/orbital_cubes_repaired/dClHeptZ/homo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 1.0010806542571344,
          "orbital_ids": "<nested value omitted>",
          "sha256": "3b7fe36f1f007ce9dd41a1ccbd3ac1f9a569200fa0efef3d2637ba0209455fcc"
        },
        "lumo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.7357683560155353,
          "core_fraction_above_isovalue_0_02": 0.8152076673778994,
          "cube": "artifacts/orbital_cubes_repaired/dClHeptZ/lumo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 0.9989072089197097,
          "orbital_ids": "<nested value omitted>",
          "sha256": "fba92f42a173e9efd136c3e07efaaec8d4ee9f2fe32def6297ae4154b4b0a9b3"
        }
      },
      "system_conclusion": "dClHeptZ: 18 singlet TD states were parsed. The lowest visible/near-visible state is 2.9085 eV (426.28 nm); the dominant orbital assignment and the recorded HOMO localization distinguish dOMeHeptZ from the other three.",
      "system_id": "dClHeptZ",
      "transitions": [
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 2.9085,
          "oscillator_strength": 0.0,
          "state_number": 1,
          "wavelength_nm": 426.28
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.5641,
          "oscillator_strength": 0.4988,
          "state_number": 2,
          "wavelength_nm": 347.87
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.5683,
          "oscillator_strength": 0.5296,
          "state_number": 3,
          "wavelength_nm": 347.46
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.6568,
          "oscillator_strength": 0.0552,
          "state_number": 4,
          "wavelength_nm": 339.05
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.6977,
          "oscillator_strength": 0.0237,
          "state_number": 5,
          "wavelength_nm": 335.3
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7101,
          "oscillator_strength": 0.0251,
          "state_number": 6,
          "wavelength_nm": 334.18
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7507,
          "oscillator_strength": 0.0011,
          "state_number": 7,
          "wavelength_nm": 330.56
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.9386,
          "oscillator_strength": 0.184,
          "state_number": 8,
          "wavelength_nm": 314.79
        },
        "<success-only excerpt: 8 of 18 entries>"
      ],
      "validation": {
        "charge": 0,
        "evidence": [
          "artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json"
        ],
        "imaginary_frequency_count": 0,
        "multiplicity": 1,
        "normal_termination": true,
        "optimization_converged": true
      }
    },
    {
      "identity": {
        "charge": 0,
        "evidence": [
          "tasks/paper_reproduction/paper_d3b4575397179146/agent_input/data/inputs/heptazines.json"
        ],
        "formula": "C30H27N7",
        "multiplicity": 1,
        "name": "2,5,8-tris(2,4-dimethylphenyl)-1,3,3a1,4,6,7,9-heptaazaphenalene",
        "smiles": "Cc1ccc(C2=NC3=NC(c4ccc(C)cc4C)=NC4=NC(c5ccc(C)cc5C)=NC(=N2)N34)c(C)c1"
      },
      "orbital_localization": {
        "criterion": "squared cube amplitude assigned by the recorded core/substituent atom partition",
        "evidence": [
          "artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/gaussian.log",
          "artifacts/orbital_cubes_repaired/dMeHeptZ/homo.cube",
          "artifacts/orbital_cubes_repaired/dMeHeptZ/lumo.cube"
        ],
        "homo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.9569317538914491,
          "core_fraction_above_isovalue_0_02": 0.9990410843681918,
          "cube": "artifacts/orbital_cubes_repaired/dMeHeptZ/homo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 0.9976923839884171,
          "orbital_ids": "<nested value omitted>",
          "sha256": "22d391d5d9ed5edbf8d08bc251cdf542fef3f9d570f149e21188c990a8c8c891"
        },
        "lumo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.7030055125998458,
          "core_fraction_above_isovalue_0_02": 0.7822710680358468,
          "cube": "artifacts/orbital_cubes_repaired/dMeHeptZ/lumo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 0.9986024973068841,
          "orbital_ids": "<nested value omitted>",
          "sha256": "386217caaf5fee2b5669bb62691b8adfc1942a5b9a47332a0798578a2c67016d"
        }
      },
      "system_conclusion": "dMeHeptZ: 18 singlet TD states were parsed. The lowest visible/near-visible state is 3.0233 eV (410.1 nm); the dominant orbital assignment and the recorded HOMO localization distinguish dOMeHeptZ from the other three.",
      "system_id": "dMeHeptZ",
      "transitions": [
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.0233,
          "oscillator_strength": 0.0,
          "state_number": 1,
          "wavelength_nm": 410.1
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.5464,
          "oscillator_strength": 0.7367,
          "state_number": 2,
          "wavelength_nm": 349.6
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.5484,
          "oscillator_strength": 0.7408,
          "state_number": 3,
          "wavelength_nm": 349.41
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7059,
          "oscillator_strength": 0.001,
          "state_number": 4,
          "wavelength_nm": 334.56
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7574,
          "oscillator_strength": 0.0723,
          "state_number": 5,
          "wavelength_nm": 329.97
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7602,
          "oscillator_strength": 0.0764,
          "state_number": 6,
          "wavelength_nm": 329.72
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7647,
          "oscillator_strength": 0.0014,
          "state_number": 7,
          "wavelength_nm": 329.34
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.8762,
          "oscillator_strength": 0.0674,
          "state_number": 8,
          "wavelength_nm": 319.86
        },
        "<success-only excerpt: 8 of 18 entries>"
      ],
      "validation": {
        "charge": 0,
        "evidence": [
          "artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/hpc_summary.json"
        ],
        "imaginary_frequency_count": 0,
        "multiplicity": 1,
        "normal_termination": true,
        "optimization_converged": true
      }
    },
    {
      "identity": {
        "charge": 0,
        "evidence": [
          "tasks/paper_reproduction/paper_d3b4575397179146/agent_input/data/inputs/heptazines.json"
        ],
        "formula": "C30H27N7O6",
        "multiplicity": 1,
        "name": "2,5,8-tris(2,4-dimethoxyphenyl)-1,3,3a1,4,6,7,9-heptaazaphenalene",
        "smiles": "COc1ccc(C2=NC3=NC(c4ccc(OC)cc4OC)=NC4=NC(c5ccc(OC)cc5OC)=NC(=N2)N34)c(OC)c1"
      },
      "orbital_localization": {
        "criterion": "squared cube amplitude assigned by the recorded core/substituent atom partition",
        "evidence": [
          "artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/gaussian.log",
          "artifacts/orbital_cubes_repaired/dOMeHeptZ/homo.cube",
          "artifacts/orbital_cubes_repaired/dOMeHeptZ/lumo.cube"
        ],
        "homo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.1085719340482921,
          "core_fraction_above_isovalue_0_02": 0.0813698224433404,
          "cube": "artifacts/orbital_cubes_repaired/dOMeHeptZ/homo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 1.0007901844564218,
          "orbital_ids": "<nested value omitted>",
          "sha256": "96ed337dcd797ea92f74d6bb92894b4e0c26aeea8f345e55bd5e80eec2975859"
        },
        "lumo": {
          "core_atom_indices_1based": "<nested value omitted>",
          "core_fraction": 0.716519735734289,
          "core_fraction_above_isovalue_0_02": 0.7914277658934045,
          "cube": "artifacts/orbital_cubes_repaired/dOMeHeptZ/lumo.cube",
          "grid_shape": "<nested value omitted>",
          "integral": 1.0002121012244016,
          "orbital_ids": "<nested value omitted>",
          "sha256": "92ad3d527ba8cc98ccc4447b2531e190c4594fa91a7bc11572103860aaabac81"
        }
      },
      "system_conclusion": "dOMeHeptZ: 18 singlet TD states were parsed. The lowest visible/near-visible state is 3.0642 eV (404.63 nm); the dominant orbital assignment and the recorded HOMO localization distinguish dOMeHeptZ from the other three.",
      "system_id": "dOMeHeptZ",
      "transitions": [
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.0642,
          "oscillator_strength": 0.0001,
          "state_number": 1,
          "wavelength_nm": 404.63
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.2094,
          "oscillator_strength": 0.69,
          "state_number": 2,
          "wavelength_nm": 386.32
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.2121,
          "oscillator_strength": 0.6841,
          "state_number": 3,
          "wavelength_nm": 385.99
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.4582,
          "oscillator_strength": 0.0003,
          "state_number": 4,
          "wavelength_nm": 358.52
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.6847,
          "oscillator_strength": 0.1153,
          "state_number": 5,
          "wavelength_nm": 336.49
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.6932,
          "oscillator_strength": 0.1037,
          "state_number": 6,
          "wavelength_nm": 335.71
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.7507,
          "oscillator_strength": 0.0008,
          "state_number": 7,
          "wavelength_nm": 330.56
        },
        {
          "dominant_orbitals": "<nested value omitted>",
          "energy_eV": 3.8892,
          "oscillator_strength": 0.014,
          "state_number": 8,
          "wavelength_nm": 318.79
        },
        "<success-only excerpt: 8 of 18 entries>"
      ],
      "validation": {
        "charge": 0,
        "evidence": [
          "artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/hpc_summary.json"
        ],
        "imaginary_frequency_count": 0,
        "multiplicity": 1,
        "normal_termination": true,
        "optimization_converged": true
      }
    }
  ]
}
```

Paper/SI document hashes:

- `papers/paper_d3b4575397179146/documents/supplementary_001.pdf` — SHA-256 `1b9598869e850445e58e1ae41e64fee1f5cd1b6ae49ab9f63bf06143c9e7aee5` (declared_match=True)
- `papers/paper_d3b4575397179146/documents/main.pdf` — SHA-256 `da7d8a332e3db06579fabefe3cebeeebac3f61e58a0cb964b9e91a70eb54a22b` (declared_match=True)

Report evidence lines retained:

- | 2 | Verify a true minimum | Optimized geometry | Gaussian 16 frequency calculation | Same level; zero imaginary frequencies required | Frequency-validated minimum | ev_doc_2b68f45a212f_000247_eb97a539c3c1; ev_doc_2b68f45a212f_000257_81d2bdb3a80f |

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **74**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/status.json` — successful status record; SHA-256 `2cf121605f25bfa9aef485af22e9bce835fad71cc0e933997810c75b0e1a7836`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/collection.json` — successful execution artifact; SHA-256 `d69606cb66562fff14c6cdf3b63de024ef8e87b4bfb31bf9c1883aa983ed1376`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2.xyz` — successful execution artifact; SHA-256 `10d5ecd6c9b583051ea862161cffef1b47ee9f89c1c7cf078c63fa4e261fc770`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json` — successful execution artifact; SHA-256 `582c3fd7872c41798de4fccd79352b7ade2f1f2ce57912c9e90464603a3e02ad`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/input.com` — successful execution artifact; SHA-256 `3dbfe320a174b7280ade1152aaa5b14fcd756fea1d6f19f98e3b9ea7843364df`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/status.json` — successful status record; SHA-256 `b99dc456ad333a28cb8bc1963ff4c334a25670f832fe0baf658cb937b0124d5c`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/gaussian.log` — successful execution artifact; SHA-256 `bbef029098ab00899befc1ad399a8d34ad1c9f5bde39a1c8592b6f5a0bea714c`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/hpc_summary.json` — successful execution artifact; SHA-256 `c7baf35b741b303a34254f2c6601430b434c0dcde8cadbf4a380b59d5ef2efd3`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/input.com` — successful execution artifact; SHA-256 `d04ee4a440f2062cee277938ef7504e2be4d25c5af9460e4d2785d2a14cc45d7`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/status.json` — successful status record; SHA-256 `fa1ccbfe124c62478c4dee7192d318204458d7cacce5456cd34a67d6495f6a0b`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/collection.json` — successful execution artifact; SHA-256 `26990dac92b517327c22489d109f881681b22ae9a3967ba858f383e8ccf5d9d4`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2.xyz` — successful execution artifact; SHA-256 `950c1d6fd0f894f4991574854d6e103a417450c09b11cc83380b5861e94e5a1c`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json` — successful execution artifact; SHA-256 `f417526df0dcf107e7b00796c68b5c65cb644024d2f7f586566155e28aab8cc4`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/input.com` — successful execution artifact; SHA-256 `19eba0e4560e8dbdff6e54dfc0856376c6e56e221f497170f1e6aea6a010b146`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/status.json` — successful status record; SHA-256 `6f81bca50c8aea7a0c60b19ac7be0752a2ac4d5d79549865c7b4aff6fbae4c2c`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/gaussian.log` — successful execution artifact; SHA-256 `e6fa18e3a5b0712f6d478e31344b9927b7084cf1a9a50271a84934d8db80c1a7`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/hpc_summary.json` — successful execution artifact; SHA-256 `73b76710ed5c122358caf4588d471a73d1897a782bcfd7d697322bedc063faf3`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/input.com` — successful execution artifact; SHA-256 `00676f34595756b9801f50de0cad79bccc429d719e65369c6fa8efc949d1edef`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/status.json` — successful status record; SHA-256 `4e01ecd6c74603795e1908fae698e633f198f227f16258e626c4bace40206347`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/gaussian.log` — successful execution artifact; SHA-256 `4cef5d6b231bb1fa23ba59238b779cdf9a1904f0a2eba249df1692cef6e772f0`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/hpc_summary.json` — successful execution artifact; SHA-256 `bd0a845eed0a68da0fd61041d4e5df543f998dc402030a2ecf72e70da99eda13`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/input.com` — successful execution artifact; SHA-256 `d01608ca9e6056b7f63659c5b395f6f3fc7c580e0f317737bee7180bc02c2060`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/status.json` — successful status record; SHA-256 `88df5fa218dbc650e15c59c478aa82ab475daf11b741ed43ea3f6a213859572b`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/gaussian.log` — successful execution artifact; SHA-256 `b64b00a5a7aae4f720b09dff46d573e726e431b10d32735ffe3dcf513215a7f6`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/hpc_summary.json` — successful execution artifact; SHA-256 `2746a616247860e85386eeaffc8a5f0096494ecfd6151dea6a855d87740b4650`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/input.com` — successful execution artifact; SHA-256 `d78bbade1f067e9de13afcce28245b2df8a3947b728564f687e7cc16e0c42f21`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/status.json` — successful status record; SHA-256 `5d38761fa7ad8c214f0c65f3e6a8979cf10a43a2cbf4c04fa7d61080a075cfb4`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/gaussian.log` — successful execution artifact; SHA-256 `25a793be7fbf42f52139ac9b023e7f00a7d664bcf92f90ce4fb301a83b0fc448`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/hpc_summary.json` — successful execution artifact; SHA-256 `1df06ea11d5c7dddd0a4d73cfaa15e26f2650b63b23e3ca6a83d79de06b1fd69`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/input.com` — successful execution artifact; SHA-256 `230d262f5489c493e76a8d9b3faa984ef7b903672f229a2813e1c509753854b4`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/status.json` — successful status record; SHA-256 `74fd8c0d13d518b53d5a931212df0b6e6f99f2994bfb8b588f79083b9fc59f36`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/gaussian.log` — successful execution artifact; SHA-256 `5b9bd03ae8dc328ddf37da179b202d11d5b982b8f48b7b95c0bbf505c0779e68`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/hpc_summary.json` — successful execution artifact; SHA-256 `8b50bbcfe06a03bb580136d2941baf363314b463e1910d717301fb4125bbf81a`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/input.com` — successful execution artifact; SHA-256 `e794e972b1346cd46fa5e5f45bf30d06b43e05aa25d21dc179797b2a9f825f89`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_39f98abb48fa4fff811091e0d9040c4d/status.json` — successful status record; SHA-256 `2cf121605f25bfa9aef485af22e9bce835fad71cc0e933997810c75b0e1a7836`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_39f98abb48fa4fff811091e0d9040c4d/collection.json` — successful execution artifact; SHA-256 `d69606cb66562fff14c6cdf3b63de024ef8e87b4bfb31bf9c1883aa983ed1376`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_39f98abb48fa4fff811091e0d9040c4d/input.com` — successful execution artifact; SHA-256 `3dbfe320a174b7280ade1152aaa5b14fcd756fea1d6f19f98e3b9ea7843364df`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_39f98abb48fa4fff811091e0d9040c4d/request.json` — successful execution artifact; SHA-256 `3d5a2dc682c893fbd6f02192b8c5a1654b6da4f577eb14ec49f70951475ce2e7`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_39f98abb48fa4fff811091e0d9040c4d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_47206a1be103472b9e8c4078efa70c7c/status.json` — successful status record; SHA-256 `fa1ccbfe124c62478c4dee7192d318204458d7cacce5456cd34a67d6495f6a0b`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_47206a1be103472b9e8c4078efa70c7c/collection.json` — successful execution artifact; SHA-256 `26990dac92b517327c22489d109f881681b22ae9a3967ba858f383e8ccf5d9d4`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_47206a1be103472b9e8c4078efa70c7c/input.com` — successful execution artifact; SHA-256 `19eba0e4560e8dbdff6e54dfc0856376c6e56e221f497170f1e6aea6a010b146`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_47206a1be103472b9e8c4078efa70c7c/request.json` — successful execution artifact; SHA-256 `77cfbffca7f739ca4f5fa9859dd083d30390ebbc35519b09215c08ef4608e5a3`
- `docs/verification/group_1/paper_d3b4575397179146/native_workspace_batch/outputs/execution_jobs/job_47206a1be103472b9e8c4078efa70c7c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dClHeptZ/status.json` — successful status record; SHA-256 `1a2643bb6a4aeeec4b77065049e818d3b7b84d623a08d691d9f0b6dd3dc673b5`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dClHeptZ/gaussian.log` — successful execution artifact; SHA-256 `9b78c717b5ae6cbbbdec65f9f7ea02864495be328cc5a06e99f400315cc6020b`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dClHeptZ/input.com` — successful execution artifact; SHA-256 `4fd198070d0be4e001ee9dcc05e10c0944aacc61975f00184d50311745135ae6`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dFHeptZ/status.json` — successful status record; SHA-256 `53b47f8a0c43406ecb6015ad271f896529f90952d2620dba9be7dd22d780ca3a`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dFHeptZ/gaussian.log` — successful execution artifact; SHA-256 `f20e078a5b5caafdc4d3776d481f105083c78228ecea0572d426d23362aef5b4`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dFHeptZ/input.com` — successful execution artifact; SHA-256 `1a25ec2ec852b3ba90b87d819cc4e7d15537596695b4ea62848bd01b20fdffe6`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dMeHeptZ/status.json` — successful status record; SHA-256 `2d90db0565b9d7bf874c1768843f69a692e3cc88c7cbe8979683f6b72420a38b`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dMeHeptZ/gaussian.log` — successful execution artifact; SHA-256 `f34341fce4e76e81b0db319aded4da7b094726dc72c176c0d8832a508ae034c1`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dMeHeptZ/input.com` — successful execution artifact; SHA-256 `dae0fd35e1526bd234a992d03a4b3cefc32a1646465609c790686bf4e758ab2d`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dOMeHeptZ/status.json` — successful status record; SHA-256 `3c4c4a3eb8da0ab16b7a35cf29af974535bb8592fb2c9dd91d42e99aa442d0cf`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dOMeHeptZ/gaussian.log` — successful execution artifact; SHA-256 `d3b7cb8b09d53c11aaa3e6358a3915bf5f7f109f57686c628906ea79dc35eb2a`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dOMeHeptZ/input.com` — successful execution artifact; SHA-256 `c4bfd251b5a1835b8ce7012d9b71e3a0e7a10560802014e8447bb8565f9b9819`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/status.json` — successful status record; SHA-256 `b99dc456ad333a28cb8bc1963ff4c334a25670f832fe0baf658cb937b0124d5c`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/gaussian.log` — successful execution artifact; SHA-256 `bbef029098ab00899befc1ad399a8d34ad1c9f5bde39a1c8592b6f5a0bea714c`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/input.com` — successful execution artifact; SHA-256 `d04ee4a440f2062cee277938ef7504e2be4d25c5af9460e4d2785d2a14cc45d7`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/status.json` — successful status record; SHA-256 `6f81bca50c8aea7a0c60b19ac7be0752a2ac4d5d79549865c7b4aff6fbae4c2c`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/gaussian.log` — successful execution artifact; SHA-256 `e6fa18e3a5b0712f6d478e31344b9927b7084cf1a9a50271a84934d8db80c1a7`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/input.com` — successful execution artifact; SHA-256 `00676f34595756b9801f50de0cad79bccc429d719e65369c6fa8efc949d1edef`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/status.json` — successful status record; SHA-256 `4e01ecd6c74603795e1908fae698e633f198f227f16258e626c4bace40206347`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/gaussian.log` — successful execution artifact; SHA-256 `4cef5d6b231bb1fa23ba59238b779cdf9a1904f0a2eba249df1692cef6e772f0`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/input.com` — successful execution artifact; SHA-256 `d01608ca9e6056b7f63659c5b395f6f3fc7c580e0f317737bee7180bc02c2060`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/status.json` — successful status record; SHA-256 `88df5fa218dbc650e15c59c478aa82ab475daf11b741ed43ea3f6a213859572b`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/gaussian.log` — successful execution artifact; SHA-256 `b64b00a5a7aae4f720b09dff46d573e726e431b10d32735ffe3dcf513215a7f6`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/input.com` — successful execution artifact; SHA-256 `d78bbade1f067e9de13afcce28245b2df8a3947b728564f687e7cc16e0c42f21`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/status.json` — successful status record; SHA-256 `5d38761fa7ad8c214f0c65f3e6a8979cf10a43a2cbf4c04fa7d61080a075cfb4`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/gaussian.log` — successful execution artifact; SHA-256 `25a793be7fbf42f52139ac9b023e7f00a7d664bcf92f90ce4fb301a83b0fc448`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/input.com` — successful execution artifact; SHA-256 `230d262f5489c493e76a8d9b3faa984ef7b903672f229a2813e1c509753854b4`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/status.json` — successful status record; SHA-256 `74fd8c0d13d518b53d5a931212df0b6e6f99f2994bfb8b588f79083b9fc59f36`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/gaussian.log` — successful execution artifact; SHA-256 `5b9bd03ae8dc328ddf37da179b202d11d5b982b8f48b7b95c0bbf505c0779e68`
- `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/input.com` — successful execution artifact; SHA-256 `e794e972b1346cd46fa5e5f45bf30d06b43e05aa25d21dc179797b2a9f825f89`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/status.json` — label=paper_d3b4575397179146 dFHeptZ_author_b3lyp_631plus_optfreq_v2 unbounded_gaussian; submitted_at=2026-09-02T03:14:24.983849+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(CalcFC,MaxCycles=150) Freq NoSymm SCF=(XQC,MaxCycle=256); command=g16 < input.com
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/collection.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2.xyz`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/stderr.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/stdout.log`
2. `artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/status.json` — label=paper_d3b4575397179146 dClHeptZ_author_b3lyp_631plus_optfreq_v2 unbounded_gaussian; submitted_at=2026-09-03T02:24:32.669215+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311+G(d,p) Opt=(CalcFC,MaxCycles=150) Freq NoSymm SCF=(XQC,MaxCycle=256); command=g16 < input.com
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/collection.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2.xyz`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/stderr.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/stdout.log`
3. `provenance/local_d3_td_validation_20260909/dFHeptZ/status.json` — label=provenance/local_d3_td_validation_20260909/dFHeptZ/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dFHeptZ/dFHeptZ_td_pbe1pbe.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dFHeptZ/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dFHeptZ/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dFHeptZ/input.com`
4. `provenance/local_d3_td_validation_20260909/dClHeptZ/status.json` — label=provenance/local_d3_td_validation_20260909/dClHeptZ/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dClHeptZ/dClHeptZ_td_pbe1pbe.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dClHeptZ/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dClHeptZ/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dClHeptZ/input.com`
5. `provenance/local_d3_td_validation_20260909/dMeHeptZ/status.json` — label=provenance/local_d3_td_validation_20260909/dMeHeptZ/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dMeHeptZ/dMeHeptZ_td_pbe1pbe.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dMeHeptZ/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dMeHeptZ/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dMeHeptZ/input.com`
6. `provenance/local_d3_td_validation_20260909/dOMeHeptZ/status.json` — label=provenance/local_d3_td_validation_20260909/dOMeHeptZ/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dOMeHeptZ/dOMeHeptZ_td_pbe1pbe.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dOMeHeptZ/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dOMeHeptZ/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/local_d3_td_validation_20260909/dOMeHeptZ/input.com`
7. `artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/status.json` — label=artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/dClHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/hpc_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/source_local_checkpoint.chk`
8. `artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/status.json` — label=artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/dFHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/hpc_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/source_local_checkpoint.chk`
9. `artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/status.json` — label=artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/hpc_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/sha256sums.txt`
10. `artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/status.json` — label=artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/dMeHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/hpc_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/source_local_checkpoint.chk`
11. `artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/status.json` — label=artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/hpc_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/source_local_checkpoint.chk`
12. `artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/status.json` — label=artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/dOMeHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/hpc_summary.json`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/source_local_checkpoint.chk`
13. `provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/status.json` — label=provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/dClHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202845Z_2839746/source_local_checkpoint.chk`
14. `provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/status.json` — label=provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/dFHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202852Z_2839746/source_local_checkpoint.chk`
15. `provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/status.json` — label=provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart/hpc_20260906T022859Z_1656375/sha256sums.txt`
16. `provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/status.json` — label=provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/dMeHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202857Z_2839746/source_local_checkpoint.chk`
17. `provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/status.json` — label=provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff/hpc_20260905T124036Z_128211/source_local_checkpoint.chk`
18. `provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/status.json` — label=provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/status.json
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/dOMeHeptZ_td_pbe1pbe_localvalidated.chk`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/fort.7`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/gaussian.log`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/input.com`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/sha256sums.txt`
   - output: `docs/verification/group_1/paper_d3b4575397179146/provenance/qzcli_hpc/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated/hpc_20260909T202903Z_2839746/source_local_checkpoint.chk`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `c_pr_2`, `r_pr_6`.

- Key-point IDs: `kp_pr_1, kp_pr_2, kp_pr_3, kp_pr_4`
- Conclusion IDs: `c_pr_1, c_pr_2`
- Scoring-rule IDs: `r_pr_1, r_pr_2, r_pr_3, r_pr_4, r_pr_5, r_pr_6`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_pr_1` → reference `kp_pr_1`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert verification; evaluator_target_present=False
- rule `r_pr_2` → reference `kp_pr_2`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert verification; evaluator_target_present=False
- rule `r_pr_3` → reference `kp_pr_3`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_pr_4` → reference `kp_pr_4`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_pr_5` → reference `c_pr_1`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_pr_6` → reference `c_pr_2`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.charge` = `0`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.multiplicity` = `1`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.optimization_converged` = `true`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.normal_termination` = `true`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.imaginary_frequency_count` = `0`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.evidence[0]` = `"artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json"`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.evidence[0]` = `"artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json"`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.evidence[0]` = `"artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/hpc_summary.json"`
- rule `r_pr_1` / reference `kp_pr_1` / field `$.systems[].validation` / result path `$.systems[].validation.evidence[0]` = `"artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/hpc_summary.json"`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `1`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `2.9647`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `418.21`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `128`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].to` = `129`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.69949`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `2`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.7374`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `331.74`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.1363`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `121`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.59403`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `126`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].to` = `129`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.23406`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `127`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].to` = `129`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.2003`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].from` = `119`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].to` = `131`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].coefficient` = `0.11366`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].from` = `124`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].to` = `129`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].coefficient` = `0.10548`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[5].from` = `120`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[5].to` = `130`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[5].coefficient` = `-0.10495`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `3`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.7599`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `329.76`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.64`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `126`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.51496`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `127`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.42044`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `120`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.18082`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `4`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.7719`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `328.7`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.5533`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `127`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.50219`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.36266`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `121`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `-0.28917`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `5`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.8394`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `322.92`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0142`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `119`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.63773`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `121`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].to` = `131`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.14765`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `122`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.14332`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `6`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.8454`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `322.42`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.058`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `120`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.61741`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.18168`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].to` = `130`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `-0.14468`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].from` = `123`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].to` = `129`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].coefficient` = `-0.13724`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `7`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.9792`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `311.58`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `125`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.64211`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `122`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.25771`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `8`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.0917`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `303.01`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.1107`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `124`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.55101`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `123`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.37093`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `-0.1374`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `9`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.093`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `302.92`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.1134`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `123`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.54878`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `124`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.36873`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.16526`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `10`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.2002`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `295.19`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0001`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `122`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.60923`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `125`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.27502`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `119`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `-0.15225`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `11`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.3142`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `287.39`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.287`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].to` = `130`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.69209`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `12`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.3153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `287.32`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.2874`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].to` = `131`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.69218`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `13`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.5911`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `270.05`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0005`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.3554`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.34682`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.32921`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].from` = `127`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].coefficient` = `-0.32621`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `14`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.6094`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `268.98`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.3572`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.42064`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].to` = `130`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.40178`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `125`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].to` = `131`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.24948`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].from` = `126`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].coefficient` = `-0.17776`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].from` = `127`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].to` = `130`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].coefficient` = `0.15756`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `15`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.6101`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `268.94`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.3553`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.42289`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.40293`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `-0.24715`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].from` = `126`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].coefficient` = `-0.15757`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `16`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.6705`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `265.46`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0072`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.62968`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `119`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.14512`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `124`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.10533`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `17`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.6735`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `265.29`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.006`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.63324`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `120`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.14083`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.11817`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].state_number` = `18`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `4.696`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `264.02`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0033`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.35728`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.33006`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `126`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `0.31132`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].coefficient` = `0.29139`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].from` = `122`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].coefficient` = `0.10716`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `2.9085`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `426.28`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `152`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].to` = `153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.6987`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.5641`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `347.87`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.4988`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `150`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.49028`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `151`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].to` = `153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `-0.4692`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.5683`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `347.46`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.5296`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `151`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.50208`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `150`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.47065`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.6568`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `339.05`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0552`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `145`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.5184`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `147`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.35898`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `149`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].to` = `153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `-0.16649`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].from` = `146`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].to` = `153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].coefficient` = `-0.14664`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].energy_eV` = `3.6977`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].wavelength_nm` = `335.3`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].oscillator_strength` = `0.0237`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].from` = `149`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[0].coefficient` = `0.36421`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].from` = `148`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[1].coefficient` = `0.34553`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].from` = `144`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[2].coefficient` = `-0.33192`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].from` = `143`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[3].coefficient` = `-0.17812`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].from` = `146`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].to` = `153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[4].coefficient` = `0.16774`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[5].from` = `147`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[5].to` = `153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[5].coefficient` = `0.13565`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[6].from` = `145`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[6].to` = `153`
- rule `r_pr_2` / reference `kp_pr_2` / field `$.systems[].transitions[]` / result path `$.systems[].transitions[].dominant_orbitals[6].coefficient` = `0.11024`
- rule `r_pr_3` / reference `kp_pr_3` / field `$.systems[].system_conclusion` / result path `$.systems[].system_conclusion` = `"dFHeptZ: 18 singlet TD states were parsed. The lowest visible/near-visible state is 2.9647 eV (418.21 nm); the dominant orbital assignment and the recorded HOMO localization distinguish dOMeHeptZ from the other three."`
- rule `r_pr_4` / reference `kp_pr_4` / field `$.systems[].orbital_localization` / result path `$.systems[].orbital_localization.criterion` = `"squared cube amplitude assigned by the recorded core/substituent atom partition"`
- rule `r_pr_5` / reference `c_pr_1` / field `$.overall_conclusion` / result path `$.overall_conclusion` = `"Within the isolated-molecule vertical-excitation scope, the four neutral singlets have completed B3LYP ground-state minimum checks and 18-state TD-PBE0 calculations. Gaussian represents PBE0 as the PBE1PBE keyword; the parsed PBE1PBE out..."`
- rule `r_pr_6` / reference `c_pr_2` / field `$.limitations` / result path `$.limitations` = `"The conclusion is limited to isolated-molecule vertical singlet excitations. The initial literal PBE0 decks failed because Gaussian rejects PBE0 as a TD post-SCF method; the successful PBE1PBE keyword is the Gaussian implementation of PB..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: heptazine identities changed
- Files changed in that review: `agent_input/data/inputs/heptazines.json, agent_input/submission_schema.json, agent_input/task.md, package_manifest.json, task_info.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Four source-supported, RDKit/Open Babel-validated neutral-singlet identities with formulas and parseable SMILES; 3-D coordinates remain agent-generated.

Public input files and hashes:

- `agent_input/data/inputs/heptazines.json` — SHA-256 `14ef87a605bde97442db9beaa94d5a14cab431ea4565a057bb9c8b2034b54d05`; size=1334 bytes; explicit_boundary_fields={"$.solvent": "acetonitrile (implicit solvent model or stated alternative)", "$.systems[0].charge": 0, "$.systems[0].formula": "C24H9F6N7", "$.systems[0].multiplicity": 1, "$.systems[0].smiles": "Fc1ccc(C2=NC3=NC(c4ccc(F)cc4F)=NC4=NC(c5ccc(F)cc5F)=NC(=N2)N34)c(F)c1", "$.systems[1].charge": 0, "$.systems[1].formula": "C24H9Cl6N7", "$.systems[1].multiplicity": 1, "$.systems[1].smiles": "Clc1ccc(C2=NC3=NC(c4ccc(Cl)cc4Cl)=NC4=NC(c5ccc(Cl)cc5Cl)=NC(=N2)N34)c(Cl)c1", "$.systems[2].charge": 0, "$.systems[2].formula": "C30H27N7O6", "$.systems[2].multiplicity": 1, "$.systems[2].smiles": "COc1ccc(C2=NC3=NC(c4ccc(OC)cc4OC)=NC4=NC(c5ccc(OC)cc5OC)=NC(=N2)N34)c(OC)c1", "$.systems[3].charge": 0, "$.systems[3].formula": "C30H27N7", "$.systems[3].multiplicity": 1, "$.systems[3].smiles": "Cc1ccc(C2=NC3=NC(c4ccc(C)cc4C)=NC4=NC(c5ccc(C)cc5C)=NC(=N2)N34)c(C)c1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_1/paper_d3b4575397179146/verification_report.md` — verification record; SHA-256 `37a61cdaa32d8186d5479c6a9d17256292fc9d97dc68366674689b5655b1f0ca`
- `docs/verification/group_1/paper_d3b4575397179146/report/results.json` — verification record; SHA-256 `81002df2b8a1c72599b531cf409afea743a9c9c3529766847df9aa3071f60e9c`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_b3lyp_631plus_optfreq_v2/dClHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json` — referenced successful evidence; SHA-256 `582c3fd7872c41798de4fccd79352b7ade2f1f2ce57912c9e90464603a3e02ad`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dClHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_f787427a/gaussian.log` — referenced successful evidence; SHA-256 `bbef029098ab00899befc1ad399a8d34ad1c9f5bde39a1c8592b6f5a0bea714c`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_b3lyp_631plus_optfreq_v2/dFHeptZ_author_b3lyp_631plus_optfreq_v2_summary.json` — referenced successful evidence; SHA-256 `f417526df0dcf107e7b00796c68b5c65cb644024d2f7f586566155e28aab8cc4`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dFHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_af4a1f1d/gaussian.log` — referenced successful evidence; SHA-256 `e6fa18e3a5b0712f6d478e31344b9927b7084cf1a9a50271a84934d8db80c1a7`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_b3lyp_631plus_optfreq_v2_fresh_restart_hpc_8e4bf3a7/hpc_summary.json` — referenced successful evidence; SHA-256 `bd0a845eed0a68da0fd61041d4e5df543f998dc402030a2ecf72e70da99eda13`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_adb2e390/gaussian.log` — referenced successful evidence; SHA-256 `b64b00a5a7aae4f720b09dff46d573e726e431b10d32735ffe3dcf513215a7f6`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_b3lyp_631plus_optfreq_v2_hpc_checkpoint_handoff_hpc_eff1a632/hpc_summary.json` — referenced successful evidence; SHA-256 `1df06ea11d5c7dddd0a4d73cfaa15e26f2650b63b23e3ca6a83d79de06b1fd69`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/gaussian_batch/dOMeHeptZ_author_td_pbe1pbe_631plus_pcm_acn_localvalidated_hpc_a5c11e9a/gaussian.log` — referenced successful evidence; SHA-256 `5b9bd03ae8dc328ddf37da179b202d11d5b982b8f48b7b95c0bbf505c0779e68`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dClHeptZ/homo.cube` — referenced successful evidence; SHA-256 `3b7fe36f1f007ce9dd41a1ccbd3ac1f9a569200fa0efef3d2637ba0209455fcc`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dClHeptZ/lumo.cube` — referenced successful evidence; SHA-256 `fba92f42a173e9efd136c3e07efaaec8d4ee9f2fe32def6297ae4154b4b0a9b3`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dFHeptZ/homo.cube` — referenced successful evidence; SHA-256 `89ab49f23f286edc2ae9a82776b15b264b491ebe9226cc756447612d517ec65e`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dFHeptZ/lumo.cube` — referenced successful evidence; SHA-256 `a9fcf7079821c02dba3545464996a8877d2d0dce6a61df35301296cbbf9a9053`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dMeHeptZ/homo.cube` — referenced successful evidence; SHA-256 `22d391d5d9ed5edbf8d08bc251cdf542fef3f9d570f149e21188c990a8c8c891`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dMeHeptZ/lumo.cube` — referenced successful evidence; SHA-256 `386217caaf5fee2b5669bb62691b8adfc1942a5b9a47332a0798578a2c67016d`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dOMeHeptZ/homo.cube` — referenced successful evidence; SHA-256 `96ed337dcd797ea92f74d6bb92894b4e0c26aeea8f345e55bd5e80eec2975859`
- `docs/verification/group_1/paper_d3b4575397179146/artifacts/orbital_cubes_repaired/dOMeHeptZ/lumo.cube` — referenced successful evidence; SHA-256 `92ad3d527ba8cc98ccc4447b2531e190c4594fa91a7bc11572103860aaabac81`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
