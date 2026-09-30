# Verified computation reference — paper_0a62b797f51de2c0 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 5 | `CONDITIONAL` | 追加验证后论文复现结论为 **CONDITIONAL**：三种单体均完成 Gaussian Opt/Freq、偶极和 Multiwfn 分子表面 ESP 极值/范围；采用独立 B3LYP/6-31G(d) 协议，未宣称作者路线的数值精确复现。 |
| 109 | `QUALIFIED` | 最终严格判定：**QUALIFIED（scope-limited）**。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Identity and property-stage correction (2026-09-23)

Historical filenames 1CN/2CN are crossed; see identity_correction.json. The corrected excerpt uses chemical identities and final optimized-geometry dipoles. SI Fig. S11 values are 0.5921, 4.1644, 6.6147 D; they are distinct from both local computational protocols. Original paths, labels and raw logs remain unchanged. No calculation was rerun.

## Source identity

- Paper: Promoting charge separation via edge activation strategy in conjugated polymers for efficient photocatalytic reaction
- DOI: `10.1016/j.cej.2026.173514`
- Task package: `tasks/final_verified_paper_reproduction/paper_0a62b797f51de2c0`
- Verification group: `docs/verification/group_2/paper_0a62b797f51de2c0`
- Paper documents: `papers/paper_0a62b797f51de2c0`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "author_route_reproduction": {
    "dipole": "Gaussian 16 C.01 CAM-B3LYP/6-311G(d,p) SP Pop=Full",
    "dipole_totals_debye": [
      1.1744,
      3.3867,
      6.0547
    ],
    "esp": "Multiwfn 2026.7.15 mapped ESP, density 0.001 a.u., grid 0.15 Bohr",
    "esp_ranges_kcal_mol": [
      30.95,
      64.43,
      68.08
    ],
    "evaluation_audit": {
      "audit_path": "provenance/author_route_evaluation_audit.json",
      "author_route_match": true,
      "evaluation_match": true
    },
    "geometry": "Gaussian 16 C.01 B3LYP/6-311G(d,p) Opt=(CalcFC,MaxCycles=300) Freq",
    "route_complete": true,
    "rows": [
      {
        "checkpoint_sha256": "ffd8751b1b8e0cca5d26bc4208eba7558fc6a8b43b2c772c0756feccef6e0b6e",
        "dipole_debye": {
          "total": 1.1744,
          "x": -0.0222,
          "y": -1.1738,
          "z": 0.0303
        },
        "esp": {
          "extrema_count": 19,
          "maxima_points": "<nested value omitted>",
          "maximum_kcal_mol": 23.43,
          "minima_points": "<nested value omitted>",
          "minimum_kcal_mol": -7.52,
          "range_kcal_mol": 30.95,
          "settings": "<nested value omitted>",
          "surface": "artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/esp/surfanalysis.pdb",
          "surface_sha256": "22cbc4b9d70ea8d0eeb43d08b742a23cfc22992b37e93d6072081a61e5a13488"
        },
        "geometry_case": "author_M_Th_0CN_b3lyp_6311gddp_optfreq",
        "geometry_job_id": "job_5f0e4bef446e493ea95787fd17acbf18",
        "geometry_summary_sha256": "121d15d2b5a3b1a0069b3362882093a1f8846032e3719932d8a6d457619d923d",
        "geometry_valid_minimum": true,
        "id": "M-Th-0CN",
        "multiwfn_marker_sha256": "670f044fe74ae36a7f7d2167322d072ee23596d105c412e1a45bf6de1414b7b3",
        "sp_case": "author_M_Th_0CN_cam_b3lyp_6311gddp_sp",
        "sp_job_id": "job_5d7c59b001b54676a7fa1bcc3cd04621",
        "sp_normal_termination": true,
        "sp_summary_sha256": "e185b7755faa178f8b57b0ba9332d77a313894bd74abbec22736f02c1f659a66",
        "source_label": "M-Th-0CN"
      },
      {
        "checkpoint_sha256": "46ebb22d425219a7af4e2013d86851b4ca48cf6cf812e4edfb973072ed0382bd",
        "dipole_debye": {
          "total": 3.3867,
          "x": 2.4432,
          "y": -2.0568,
          "z": 1.1269
        },
        "esp": {
          "extrema_count": 18,
          "maxima_points": "<nested value omitted>",
          "maximum_kcal_mol": 28.59,
          "minima_points": "<nested value omitted>",
          "minimum_kcal_mol": -35.84,
          "range_kcal_mol": 64.43,
          "settings": "<nested value omitted>",
          "surface": "artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/esp/surfanalysis.pdb",
          "surface_sha256": "8e93a1811566778f1a6f597d788a531911d696e13b4875632719a5206ce13966"
        },
        "geometry_case": "author_M_Th_2CN_b3lyp_6311gddp_optfreq",
        "geometry_job_id": "job_b41ad92920304ab0888fd23a4d627d32",
        "geometry_summary_sha256": "13236ea723b3deb102459d4bf512e9dded3c25b4da789226daed82b88ffa2f79",
        "geometry_valid_minimum": true,
        "id": "M-Th-1CN",
        "multiwfn_marker_sha256": "ebaefc5794e23c317f95d5e7465c875cc35ff465eeed624dee39117f0eedc37d",
        "sp_case": "author_M_Th_2CN_cam_b3lyp_6311gddp_sp",
        "sp_job_id": "job_2df87fb5ba3a406cae81bc5fd8edb656",
        "sp_normal_termination": true,
        "sp_summary_sha256": "f700c1dfb4c5aa13d70f2c509ceeaa6e2cf8f5960174b8ab0b0059d30f3eb690",
        "source_label": "M-Th-2CN",
        "name": "2,5-dibromo-3-cyanothiophene",
        "cyano_count": 1
      },
      {
        "checkpoint_sha256": "730d15a42bb651d8e6a227981e55a1b2017a403971ef019fab90025f5e8c2e5d",
        "dipole_debye": {
          "total": 6.0547,
          "x": 0.0971,
          "y": 5.8209,
          "z": 1.6632
        },
        "esp": {
          "extrema_count": 20,
          "maxima_points": "<nested value omitted>",
          "maximum_kcal_mol": 34.41,
          "minima_points": "<nested value omitted>",
          "minimum_kcal_mol": -33.67,
          "range_kcal_mol": 68.08,
          "settings": "<nested value omitted>",
          "surface": "artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/esp/surfanalysis.pdb",
          "surface_sha256": "85cf328c3423e6c0a4f8792f032f23b977474e5aecd1d4e92b229a61f93d6cae"
        },
        "geometry_case": "author_M_Th_1CN_b3lyp_6311gddp_optfreq",
        "geometry_job_id": "job_5b010c33434c4a5585bf3e320f664df9",
        "geometry_summary_sha256": "2d1cbe2890e85bad4c92f1ce2dd691adb359acdce79675f52f19885c1ee63cf8",
        "geometry_valid_minimum": true,
        "id": "M-Th-2CN",
        "multiwfn_marker_sha256": "e9ad0d26591ac7de5d4b6ee2c422b41b473a53d3b28cd90b8c7d3bd1c26ef199",
        "sp_case": "author_M_Th_1CN_cam_b3lyp_6311gddp_sp",
        "sp_job_id": "job_541e5c98f7234951acae8d74d72a521d",
        "sp_normal_termination": true,
        "sp_summary_sha256": "11c1a23e0964b80b2399d9b3d7dc7ceb37c9563751c10990801106d940bc2b51",
        "source_label": "M-Th-1CN",
        "name": "2,5-dibromo-3,4-dicyanothiophene",
        "cyano_count": 2
      }
    ]
  },
  "comparison": {
    "author_route_dipole_totals_debye": [
      1.1744,
      3.3867,
      6.0547
    ],
    "author_route_esp_ranges_kcal_mol": [
      30.95,
      64.43,
      68.08
    ],
    "author_route_trend_statement": "Author-route CAM-B3LYP dipoles are 1.174, 3.387 and 6.055 D for corrected 0/1/2CN identities; corresponding ESP ranges are 30.95, 64.43 and 68.08 kcal/mol, both increasing across the series.",
    "dipole_ordering": [
      "M-Th-0CN",
      "M-Th-1CN",
      "M-Th-2CN"
    ],
    "esp_ordering": [
      "M-Th-0CN",
      "M-Th-1CN",
      "M-Th-2CN"
    ],
    "trend_statement": "Final optimized-geometry B3LYP/6-31G(d) dipoles are 1.1570, 3.3674, 5.9387 D for corrected 0/1/2 CN identities; corresponding surface ESP ranges are 29.16, 62.65, 66.23 kcal/mol. Both increase across the corrected series. These are local calculations, not the SI Fig. S11 values."
  },
  "conclusion": "Gaussian optimizations, harmonic frequencies and Multiwfn molecular-surface ESP extrema completed for all three neutral singlet monomers. Dipole and surface-ESP trends support cyano-driven polarization qualitatively; the independent B3LYP/6-31G(d) protocol remains conditional relative to the paper method.",
  "limitations": "B3LYP/6-31G(d) differs from the paper B3LYP/6-311G** plus CAM-B3LYP/Multiwfn; one conformer per constitutional isomer; no polymer extension. Surface ESP extrema use an electron-density isosurface of 0.001 a.u. with grid spacing 0.15 Bohr and are reported as a range in kcal/mol.",
  "molecules": [
    {
      "cyano_count": 0,
      "dipole": {
        "value": 1.157,
        "unit": "Debye",
        "components": [
          -0.0219,
          -1.1564,
          0.0298
        ],
        "calculation_stage": "final optimized geometry; frequency-link dipole",
        "source_label": "M-Th-0CN",
        "source_log": "docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/stdout.log",
        "source_line": 28574
      },
      "esp": {
        "definition": "Multiwfn molecular-surface ESP extrema on electron-density isosurface 0.001 a.u., grid spacing 0.15 Bohr; maximum minus minimum in kcal/mol",
        "maximum_kcal_mol": 21.42,
        "minimum_kcal_mol": -7.74,
        "negative_region": "minimum surface ESP = -7.74 kcal/mol",
        "positive_region": "maximum surface ESP = 21.42 kcal/mol",
        "software": "Multiwfn 2026.7.15",
        "surface_file": "artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/esp/surfanalysis.pdb",
        "unit": "kcal/mol (surface ESP range)",
        "value": 29.160000000000004
      },
      "id": "M-Th-0CN",
      "method": {
        "basis": "6-31G(d)",
        "charge": 0,
        "convergence": "Opt+Freq; Gaussian normal termination; 0 imaginary frequencies",
        "method": "B3LYP",
        "multiplicity": 1,
        "software": "Gaussian 16 C.01"
      },
      "name": "2,5-dibromothiophene",
      "structure": {
        "file": "provenance/M-Th-0CN_xtbopt.xyz",
        "smiles": "s1c(Br)ccc1Br",
        "chemical_identity": "M-Th-0CN"
      },
      "validation": {
        "conformer_coverage": "one RDKit ETKDG conformer, xTB-GFN2 preoptimization, then Gaussian optimization",
        "identity_checked": true,
        "notes": "21 frequencies; minimum 90.4846 cm^-1; job job_9482d08d8c01464097d7a4dca1c20b85 duration 126.501011 s",
        "optimization_validated": true
      },
      "source_label": "M-Th-0CN"
    },
    {
      "cyano_count": 1,
      "dipole": {
        "value": 3.3674,
        "unit": "Debye",
        "components": [
          2.4613,
          -2.0137,
          1.1073
        ],
        "calculation_stage": "final optimized geometry; frequency-link dipole",
        "source_label": "M-Th-2CN",
        "source_log": "docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/stdout.log",
        "source_line": 40156
      },
      "esp": {
        "definition": "Multiwfn molecular-surface ESP extrema on electron-density isosurface 0.001 a.u., grid spacing 0.15 Bohr; maximum minus minimum in kcal/mol",
        "maximum_kcal_mol": 26.56,
        "minimum_kcal_mol": -36.09,
        "negative_region": "minimum surface ESP = -36.09 kcal/mol",
        "positive_region": "maximum surface ESP = 26.56 kcal/mol",
        "software": "Multiwfn 2026.7.15",
        "surface_file": "artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/esp/surfanalysis.pdb",
        "unit": "kcal/mol (surface ESP range)",
        "value": 62.650000000000006
      },
      "id": "M-Th-1CN",
      "method": {
        "basis": "6-31G(d)",
        "charge": 0,
        "convergence": "Opt+Freq; Gaussian normal termination; 0 imaginary frequencies",
        "method": "B3LYP",
        "multiplicity": 1,
        "software": "Gaussian 16 C.01"
      },
      "name": "2,5-dibromo-3-cyanothiophene",
      "structure": {
        "file": "provenance/M-Th-2CN_xtbopt.xyz",
        "smiles": "s1c(Br)c(C#N)cc1Br",
        "chemical_identity": "M-Th-1CN"
      },
      "validation": {
        "conformer_coverage": "one RDKit ETKDG conformer, xTB-GFN2 preoptimization, then Gaussian optimization",
        "identity_checked": true,
        "notes": "24 frequencies; minimum 90.2762 cm^-1; job job_c5e2eb68f3c6402a9058f6eedf6aa72b duration 163.78354 s",
        "optimization_validated": true
      },
      "source_label": "M-Th-2CN"
    },
    {
      "cyano_count": 2,
      "dipole": {
        "value": 5.9387,
        "unit": "Debye",
        "components": [
          0.0952,
          5.7095,
          1.6312
        ],
        "calculation_stage": "final optimized geometry; frequency-link dipole",
        "source_label": "M-Th-1CN",
        "source_log": "docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/stdout.log",
        "source_line": 52418
      },
      "esp": {
        "definition": "Multiwfn molecular-surface ESP extrema on electron-density isosurface 0.001 a.u., grid spacing 0.15 Bohr; maximum minus minimum in kcal/mol",
        "maximum_kcal_mol": 32.48,
        "minimum_kcal_mol": -33.75,
        "negative_region": "minimum surface ESP = -33.75 kcal/mol",
        "positive_region": "maximum surface ESP = 32.48 kcal/mol",
        "software": "Multiwfn 2026.7.15",
        "surface_file": "artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/esp/surfanalysis.pdb",
        "unit": "kcal/mol (surface ESP range)",
        "value": 66.22999999999999
      },
      "id": "M-Th-2CN",
      "method": {
        "basis": "6-31G(d)",
        "charge": 0,
        "convergence": "Opt+Freq; Gaussian normal termination; 0 imaginary frequencies",
        "method": "B3LYP",
        "multiplicity": 1,
        "software": "Gaussian 16 C.01"
      },
      "name": "2,5-dibromo-3,4-dicyanothiophene",
      "structure": {
        "file": "provenance/M-Th-1CN_xtbopt.xyz",
        "smiles": "s1c(Br)c(C#N)c(C#N)c1Br",
        "chemical_identity": "M-Th-2CN"
      },
      "validation": {
        "conformer_coverage": "one RDKit ETKDG conformer, xTB-GFN2 preoptimization, then Gaussian optimization",
        "identity_checked": true,
        "notes": "27 frequencies; minimum 70.7869 cm^-1; job job_91ee33e3b31348d099e2a708a6e6a4b0 duration 173.135029 s",
        "optimization_validated": true
      },
      "source_label": "M-Th-1CN"
    }
  ],
  "polymer_extension": {
    "notes": "Not performed; only the three public monomers were evaluated.",
    "performed": false
  },
  "status": "complete",
  "identity_correction": {
    "paper_id": "paper_0a62b797f51de2c0",
    "correction_type": "source_identity_mapping",
    "status": "confirmed",
    "basis": [
      "The file labelled M-Th-1CN contains C6Br2N2S (two cyano nitrogens).",
      "The file labelled M-Th-2CN contains C5HBr2NS (one cyano nitrogen).",
      "The same swap is present in the author-route 1CN/2CN filenames."
    ],
    "mapping": [
      {
        "source_label": "M-Th-0CN",
        "chemical_identity": "M-Th-0CN",
        "formula": "C4H2Br2S",
        "cyano_count": 0
      },
      {
        "source_label": "M-Th-1CN",
        "chemical_identity": "M-Th-2CN",
        "formula": "C6Br2N2S",
        "cyano_count": 2
      },
      {
        "source_label": "M-Th-2CN",
        "chemical_identity": "M-Th-1CN",
        "formula": "C5HBr2NS",
        "cyano_count": 1
      },
      {
        "source_label": "author_M_Th_1CN",
        "chemical_identity": "M-Th-2CN",
        "formula": "C6Br2N2S",
        "cyano_count": 2
      },
      {
        "source_label": "author_M_Th_2CN",
        "chemical_identity": "M-Th-1CN",
        "formula": "C5HBr2NS",
        "cyano_count": 1
      }
    ],
    "policy": {
      "raw_artifacts": "preserved",
      "paths_and_job_ids": "preserved",
      "quantum_calculation": "not rerun",
      "interpretation": "all identity-dependent values are read using chemical_identity, not the historical source_label"
    }
  },
  "property_stage_correction": {
    "source": "Original Opt/Freq stdout.log final dipole blocks, checked 2026-09-23",
    "previous_initial_geometry_dipoles": {
      "M-Th-0CN": {
        "value": 1.1334,
        "unit": "Debye",
        "components": [
          -0.0214,
          -1.1328,
          0.0292
        ]
      },
      "M-Th-1CN": {
        "value": 3.3406,
        "unit": "Debye",
        "components": [
          2.4453,
          -1.9954,
          1.0949
        ]
      },
      "M-Th-2CN": {
        "value": 5.9017,
        "unit": "Debye",
        "components": [
          0.0917,
          5.6743,
          1.6202
        ]
      }
    },
    "raw_artifacts": "unchanged; no calculation rerun"
  }
}
```

Paper/SI document hashes:

- `papers/paper_0a62b797f51de2c0/documents/main.pdf` — SHA-256 `8faf62fe4d34371ac12d6c414dec1a19ecd0a08656bd4a9d692b3d0dd08f3b4a` (declared_match=True)
- `papers/paper_0a62b797f51de2c0/documents/supplementary_001.pdf` — SHA-256 `cec193840ebff26c59e3ce19abee827e02a953fafc2b62ce34761586a0039b8d` (declared_match=True)

Report evidence lines retained:

- 追加验证后论文复现结论为 **CONDITIONAL**：三种单体均完成 Gaussian Opt/Freq、偶极和 Multiwfn 分子表面 ESP 极值/范围；采用独立 B3LYP/6-31G(d) 协议，未宣称作者路线的数值精确复现。
- 通用 `generate_3d_structure`（RDKit）和 `optimize_geometry`（xTB）成功；Gaussian16 C.01 native runner 通过 `validate_native_job`，设置 8 CPU/24 GB、无 walltime 上限策略。采用 B3LYP/6-31G(d) Opt Freq Pop=Full NoSymm，作为可审查的独立 DFT 路线；该基组与作者不完全等价。
- | M-Th-0CN | `job_9482d08d8c01464097d7a4dca1c20b85` | normal termination/converged | 126.501 | 21 / 0 | 1.1570 |
- | M-Th-1CN | `job_c5e2eb68f3c6402a9058f6eedf6aa72b` | normal termination/converged | 163.784 | 24 / 0 | 3.3674 |
- | M-Th-2CN | `job_91ee33e3b31348d099e2a708a6e6a4b0` | normal termination/converged | 173.135 | 27 / 0 | 5.9387 |
- - 作者路线端点：3/3 个 B3LYP/6-311G(d,p) Opt/Freq 与 3/3 个 CAM-B3LYP/6-311G(d,p) SP 正常终止；三套 Multiwfn ESP 表面均生成并记录哈希。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **90**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/status.json` — successful status record; SHA-256 `87c3297fbea110e03ac0548bc061cece4054083bb6302c1ef67115796e0ca8c6`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `43f9e4cebe1e55782ccd8202c648d3e6da62de99226eb988e9cf80b008cf4c11`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `c947f128fa104208ae71d5019cf8365392abeb2f909bacc4ddc4ee7b90d06625`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `d940d2141c6894806cb3c7f11c3fcc3a0510c1d9a5b7c4ff28ffc9161fd09c8c`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/status.json` — successful status record; SHA-256 `86d34b7b471b55567214ea99f45d52e81fef660309517a9f4dd061cad6edc471`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `6feaf4c478903512194c77864cef881a3e7b5a8ae0978683d8437cd6c3a14329`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `58c04791a32b887980609198ce29263845e2909cfb9136663d1f6b985efd7291`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `d8075b5eaf4ac269642604203ee41f9793c2f237af3520c7dab731cb5657d3d7`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/status.json` — successful status record; SHA-256 `6c252eb78d2e21dec6e99b34d54aeb3af25aed1d1f0fb1a71705d5decdb1ad04`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `67b58245524f5aee78769250bbb3addd434b9a3cc6344b5f67b74c1374734502`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `70b2412498f4a98181264bbc8e66388addcd4066dec6052e614a851532aa5b1a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `25a20e005dd658e42ca7c4a9ab25634690d0a807ef25a72124fc2673a2618c55`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/status.json` — successful status record; SHA-256 `1374a49650cf1331c16420c5ffb417e3479865e6e687eb6df1cc4d0e4c34282a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/collection.json` — successful execution artifact; SHA-256 `f37fa0f29fd3f89d6014a14500f570f8c0bb2caad6615f769ecc90f319c8ce72`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/input.com` — successful execution artifact; SHA-256 `ae43bd834fa935b857c3c98eae3975c87a2350e805263887d1f5470a711a7b4d`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/stdout.log` — successful execution artifact; SHA-256 `c3c27d8030fdc0a4914d6127c9a905663d811dba9456835d65df6b83b230ad66`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/status.json` — successful status record; SHA-256 `51d253067289267a4a23d22e8bd9a37f5e01397264a9bc185bddca1d748b63b2`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/collection.json` — successful execution artifact; SHA-256 `dbdcc1b470722e8e968968adcf882565a624cb319f652e2a20af1eb98bd7af1a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/input.com` — successful execution artifact; SHA-256 `ca7f8535587fbcdec7821a4d4d51ba4ec76326e01851b9bcef1933294fbba92f`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/stdout.log` — successful execution artifact; SHA-256 `3588b3282fc4b453dee59a6f1d49564cf5693a3045d22445d724d8272846fb40`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/status.json` — successful status record; SHA-256 `c860ed82f76fa816118945dd84fd3d64beaf4fd22263f4a5c4e5cb1290b856ee`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/collection.json` — successful execution artifact; SHA-256 `9fdc1076a082ada4d6a7d1232ecf0e614fbeda3405c5c10c2d4b430b0f6b4503`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/input.com` — successful execution artifact; SHA-256 `56de3b8c84be01adc5ea26fa494342be8586aed3947ccf5c84e4f00076c22c9a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/stdout.log` — successful execution artifact; SHA-256 `6bb4838f8514337269ee07d4256deb2bcfc44cfce94028c40e15bceb78d41db5`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/status.json` — successful status record; SHA-256 `1e3b3686899c51393c2ac450f52cbbcce172239aa5920ae6b51790aa8cce1114`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/collection.json` — successful execution artifact; SHA-256 `570cecb5cbc4c59885203d89cfe7af35648464dee5ae07258178e4692a08be90`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/input.com` — successful execution artifact; SHA-256 `6acda114b958988b63f7dbb51ba3804ea55ded94ca6711b605f7089235195387`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/stdout.log` — successful execution artifact; SHA-256 `d16fc5f3c5a3a04e1b441bc54f6289614866e4e023db76282182bff406ab1823`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/status.json` — successful status record; SHA-256 `477e97d8109442d3dc0f3e345394e4a2e48841916e309ad52d403647cf80286a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/collection.json` — successful execution artifact; SHA-256 `5fee9c8b53103d5b224d92310bc44839a6c96d51e83f3a3f08e4ffa60c618126`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/input.com` — successful execution artifact; SHA-256 `26583aa745a2c5304c52f0c1b81d33d381371285a239d051c76c3d32a784f5fe`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/stdout.log` — successful execution artifact; SHA-256 `86f18d64ae001ddb0469bfef26d2dfe5ba1b46e26f544acfea1c70ab0c8e3ab0`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/status.json` — successful status record; SHA-256 `cbe697c5004e8fbd777efdfb7c15011122479c85524a5e72782b7373a6f32299`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/collection.json` — successful execution artifact; SHA-256 `2c7e18d898cd78215bf8c5a19bdf9307d7d0fff6ca713ed9ed428c2aead18770`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/input.com` — successful execution artifact; SHA-256 `62fec4e8926ee931fe5d046c19e91e2a84c3df1f586d99b685788c74153d129b`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/stdout.log` — successful execution artifact; SHA-256 `4d14881356759327ee940db36aeaed97abeff979148f2f7a2372b653746c9741`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_2df87fb5ba3a406cae81bc5fd8edb656/status.json` — successful status record; SHA-256 `cbe697c5004e8fbd777efdfb7c15011122479c85524a5e72782b7373a6f32299`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_2df87fb5ba3a406cae81bc5fd8edb656/collection.json` — successful execution artifact; SHA-256 `2c7e18d898cd78215bf8c5a19bdf9307d7d0fff6ca713ed9ed428c2aead18770`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_2df87fb5ba3a406cae81bc5fd8edb656/input.com` — successful execution artifact; SHA-256 `62fec4e8926ee931fe5d046c19e91e2a84c3df1f586d99b685788c74153d129b`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_2df87fb5ba3a406cae81bc5fd8edb656/request.json` — successful execution artifact; SHA-256 `a2734af25d352fcd2e222868f160f7e95f78a569f8440a9a0f6754109da83d22`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_2df87fb5ba3a406cae81bc5fd8edb656/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_541e5c98f7234951acae8d74d72a521d/status.json` — successful status record; SHA-256 `1e3b3686899c51393c2ac450f52cbbcce172239aa5920ae6b51790aa8cce1114`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_541e5c98f7234951acae8d74d72a521d/collection.json` — successful execution artifact; SHA-256 `570cecb5cbc4c59885203d89cfe7af35648464dee5ae07258178e4692a08be90`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_541e5c98f7234951acae8d74d72a521d/input.com` — successful execution artifact; SHA-256 `6acda114b958988b63f7dbb51ba3804ea55ded94ca6711b605f7089235195387`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_541e5c98f7234951acae8d74d72a521d/request.json` — successful execution artifact; SHA-256 `eaa1293fa63c9258c46bffcdcfbe427c9d05d9f913d955db79ca258261c9cb70`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_541e5c98f7234951acae8d74d72a521d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5b010c33434c4a5585bf3e320f664df9/status.json` — successful status record; SHA-256 `c860ed82f76fa816118945dd84fd3d64beaf4fd22263f4a5c4e5cb1290b856ee`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5b010c33434c4a5585bf3e320f664df9/collection.json` — successful execution artifact; SHA-256 `9fdc1076a082ada4d6a7d1232ecf0e614fbeda3405c5c10c2d4b430b0f6b4503`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5b010c33434c4a5585bf3e320f664df9/input.com` — successful execution artifact; SHA-256 `56de3b8c84be01adc5ea26fa494342be8586aed3947ccf5c84e4f00076c22c9a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5b010c33434c4a5585bf3e320f664df9/request.json` — successful execution artifact; SHA-256 `93d1253557d59b242e509255a8d733bde5571e2ae6f9900641abea74092f49c4`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5b010c33434c4a5585bf3e320f664df9/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5d7c59b001b54676a7fa1bcc3cd04621/status.json` — successful status record; SHA-256 `51d253067289267a4a23d22e8bd9a37f5e01397264a9bc185bddca1d748b63b2`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5d7c59b001b54676a7fa1bcc3cd04621/collection.json` — successful execution artifact; SHA-256 `dbdcc1b470722e8e968968adcf882565a624cb319f652e2a20af1eb98bd7af1a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5d7c59b001b54676a7fa1bcc3cd04621/input.com` — successful execution artifact; SHA-256 `ca7f8535587fbcdec7821a4d4d51ba4ec76326e01851b9bcef1933294fbba92f`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5d7c59b001b54676a7fa1bcc3cd04621/request.json` — successful execution artifact; SHA-256 `3128022f9f0dc8d5a12313137c6058f6e739e56000f4dc6d6cc156c3dbfe3556`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5d7c59b001b54676a7fa1bcc3cd04621/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5f0e4bef446e493ea95787fd17acbf18/status.json` — successful status record; SHA-256 `1374a49650cf1331c16420c5ffb417e3479865e6e687eb6df1cc4d0e4c34282a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5f0e4bef446e493ea95787fd17acbf18/collection.json` — successful execution artifact; SHA-256 `f37fa0f29fd3f89d6014a14500f570f8c0bb2caad6615f769ecc90f319c8ce72`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5f0e4bef446e493ea95787fd17acbf18/input.com` — successful execution artifact; SHA-256 `ae43bd834fa935b857c3c98eae3975c87a2350e805263887d1f5470a711a7b4d`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5f0e4bef446e493ea95787fd17acbf18/request.json` — successful execution artifact; SHA-256 `db2d7e156ab63e798e208914d3318f6acdacc5da3e99cdfe795384cabd5aab55`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_5f0e4bef446e493ea95787fd17acbf18/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_91ee33e3b31348d099e2a708a6e6a4b0/status.json` — successful status record; SHA-256 `86d34b7b471b55567214ea99f45d52e81fef660309517a9f4dd061cad6edc471`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_91ee33e3b31348d099e2a708a6e6a4b0/collection.json` — successful execution artifact; SHA-256 `6feaf4c478903512194c77864cef881a3e7b5a8ae0978683d8437cd6c3a14329`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_91ee33e3b31348d099e2a708a6e6a4b0/input.com` — successful execution artifact; SHA-256 `58c04791a32b887980609198ce29263845e2909cfb9136663d1f6b985efd7291`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_91ee33e3b31348d099e2a708a6e6a4b0/request.json` — successful execution artifact; SHA-256 `c5d7d918b071b56bbc660d115b6963e20f0d4946a0b7fc1415df618d3b975357`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_91ee33e3b31348d099e2a708a6e6a4b0/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_9482d08d8c01464097d7a4dca1c20b85/status.json` — successful status record; SHA-256 `87c3297fbea110e03ac0548bc061cece4054083bb6302c1ef67115796e0ca8c6`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_9482d08d8c01464097d7a4dca1c20b85/collection.json` — successful execution artifact; SHA-256 `43f9e4cebe1e55782ccd8202c648d3e6da62de99226eb988e9cf80b008cf4c11`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_9482d08d8c01464097d7a4dca1c20b85/input.com` — successful execution artifact; SHA-256 `c947f128fa104208ae71d5019cf8365392abeb2f909bacc4ddc4ee7b90d06625`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_9482d08d8c01464097d7a4dca1c20b85/request.json` — successful execution artifact; SHA-256 `86b346f7e940e37a50e2973b19d3fc8803f118a6d46692666e65dc9c3be7b37f`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_9482d08d8c01464097d7a4dca1c20b85/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_b41ad92920304ab0888fd23a4d627d32/status.json` — successful status record; SHA-256 `477e97d8109442d3dc0f3e345394e4a2e48841916e309ad52d403647cf80286a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_b41ad92920304ab0888fd23a4d627d32/collection.json` — successful execution artifact; SHA-256 `5fee9c8b53103d5b224d92310bc44839a6c96d51e83f3a3f08e4ffa60c618126`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_b41ad92920304ab0888fd23a4d627d32/input.com` — successful execution artifact; SHA-256 `26583aa745a2c5304c52f0c1b81d33d381371285a239d051c76c3d32a784f5fe`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_b41ad92920304ab0888fd23a4d627d32/request.json` — successful execution artifact; SHA-256 `ec7300f02e9313de9d159e8b43e89d2b6fcd747c6a9d08262f6bb0a57432ef2a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_b41ad92920304ab0888fd23a4d627d32/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_c5e2eb68f3c6402a9058f6eedf6aa72b/status.json` — successful status record; SHA-256 `6c252eb78d2e21dec6e99b34d54aeb3af25aed1d1f0fb1a71705d5decdb1ad04`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_c5e2eb68f3c6402a9058f6eedf6aa72b/collection.json` — successful execution artifact; SHA-256 `67b58245524f5aee78769250bbb3addd434b9a3cc6344b5f67b74c1374734502`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_c5e2eb68f3c6402a9058f6eedf6aa72b/input.com` — successful execution artifact; SHA-256 `70b2412498f4a98181264bbc8e66388addcd4066dec6052e614a851532aa5b1a`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_c5e2eb68f3c6402a9058f6eedf6aa72b/request.json` — successful execution artifact; SHA-256 `64980ff6a1a56bac3cd889468628dfca5073e69d3b67fd155eba92803958a20b`
- `docs/verification/group_2/paper_0a62b797f51de2c0/native_workspace_batch/outputs/execution_jobs/job_c5e2eb68f3c6402a9058f6eedf6aa72b/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/status.json` — label=group_2 paper_0a62b797f51de2c0 M-Th-0CN_b3lyp_optfreq; submitted_at=2026-08-29T09:14:44.626121+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/M-Th-0CN_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/stdout.log`
2. `artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/status.json` — label=group_2 paper_0a62b797f51de2c0 M-Th-1CN_b3lyp_optfreq; submitted_at=2026-08-29T09:16:09.071883+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/M-Th-1CN_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/stdout.log`
3. `artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/status.json` — label=group_2 paper_0a62b797f51de2c0 M-Th-2CN_b3lyp_optfreq; submitted_at=2026-08-29T09:19:53.471803+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/M-Th-2CN_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/stdout.log`
4. `artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/status.json` — label=group_2 paper_0a62b797f51de2c0 author_M_Th_0CN_b3lyp_6311gddp_optfreq; submitted_at=2026-08-30T16:52:41.475942+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/author_M_Th_0CN_b3lyp_6311gddp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_b3lyp_6311gddp_optfreq/stdout.log`
5. `artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/status.json` — label=group_2 paper_0a62b797f51de2c0 author_M_Th_1CN_b3lyp_6311gddp_optfreq; submitted_at=2026-08-30T16:52:41.537292+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/author_M_Th_1CN_b3lyp_6311gddp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_b3lyp_6311gddp_optfreq/stdout.log`
6. `artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/status.json` — label=group_2 paper_0a62b797f51de2c0 author_M_Th_2CN_b3lyp_6311gddp_optfreq; submitted_at=2026-08-30T16:52:41.621109+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/author_M_Th_2CN_b3lyp_6311gddp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_b3lyp_6311gddp_optfreq/stdout.log`
7. `artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/status.json` — label=group_2 paper_0a62b797f51de2c0 author_M_Th_0CN_cam_b3lyp_6311gddp_sp; submitted_at=2026-08-31T16:22:58.541351+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-311G(d,p) SP Pop=Full NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/author_M_Th_0CN_cam_b3lyp_6311gddp_sp.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_0CN_cam_b3lyp_6311gddp_sp/stdout.log`
8. `artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/status.json` — label=group_2 paper_0a62b797f51de2c0 author_M_Th_1CN_cam_b3lyp_6311gddp_sp; submitted_at=2026-08-31T16:27:59.105912+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-311G(d,p) SP Pop=Full NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/author_M_Th_1CN_cam_b3lyp_6311gddp_sp.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_1CN_cam_b3lyp_6311gddp_sp/stdout.log`
9. `artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/status.json` — label=group_2 paper_0a62b797f51de2c0 author_M_Th_2CN_cam_b3lyp_6311gddp_sp; submitted_at=2026-08-31T16:32:59.687604+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-311G(d,p) SP Pop=Full NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/author_M_Th_2CN_cam_b3lyp_6311gddp_sp.chk`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/collection.json`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/input.com`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/stderr.log`
   - output: `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/author_M_Th_2CN_cam_b3lyp_6311gddp_sp/stdout.log`

## Evaluator alignment

- Key-point IDs: `pr_process_identity, pr_process_esp, pr_result_trend, pr_result_pattern`
- Conclusion IDs: `pr_final_conclusion`
- Scoring-rule IDs: `pr_rule_identity, pr_rule_esp, pr_rule_dipole_trend, pr_rule_pattern, pr_rule_final`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `pr_rule_identity` → reference `pr_process_identity`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process comparison; evaluator_target_present=False
- rule `pr_rule_esp` → reference `pr_process_esp`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process comparison; evaluator_target_present=False
- rule `pr_rule_dipole_trend` → reference `pr_result_trend`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=reported ordering compared with source-supported trend; evaluator_target_present=False
- rule `pr_rule_pattern` → reference `pr_result_pattern`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_rule_final` → reference `pr_final_conclusion`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].id` / result path `$.molecules[].id` = `"M-Th-0CN"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].id` / result path `$.molecules[].id` = `"M-Th-1CN"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].id` / result path `$.molecules[].id` = `"M-Th-2CN"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].structure.smiles` / result path `$.molecules[].structure.smiles` = `"s1c(Br)ccc1Br"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].structure.smiles` / result path `$.molecules[].structure.smiles` = `"s1c(Br)c(C#N)cc1Br"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].structure.smiles` / result path `$.molecules[].structure.smiles` = `"s1c(Br)c(C#N)c(C#N)c1Br"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].method.charge` / result path `$.molecules[].method.charge` = `0`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].method.multiplicity` / result path `$.molecules[].method.multiplicity` = `1`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].validation.notes` / result path `$.molecules[].validation.notes` = `"21 frequencies; minimum 90.4846 cm^-1; job job_9482d08d8c01464097d7a4dca1c20b85 duration 126.501011 s"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].validation.notes` / result path `$.molecules[].validation.notes` = `"27 frequencies; minimum 70.7869 cm^-1; job job_91ee33e3b31348d099e2a708a6e6a4b0 duration 173.135029 s"`
- rule `pr_rule_identity` / reference `pr_process_identity` / field `$.molecules[].validation.notes` / result path `$.molecules[].validation.notes` = `"24 frequencies; minimum 90.2762 cm^-1; job job_c5e2eb68f3c6402a9058f6eedf6aa72b duration 163.78354 s"`
- rule `pr_rule_esp` / reference `pr_process_esp` / field `$.molecules[].esp.definition` / result path `$.molecules[].esp.definition` = `"Multiwfn ESP extrema on electron-density isosurface 0.001 a.u., grid spacing 0.15 Bohr; value is maximum minus minimum over reported surface extrema"`
- rule `pr_rule_dipole_trend` / reference `pr_result_trend` / field `$.comparison.dipole_ordering` / result path `$.comparison.dipole_ordering[0]` = `"M-Th-0CN"`
- rule `pr_rule_dipole_trend` / reference `pr_result_trend` / field `$.comparison.dipole_ordering` / result path `$.comparison.dipole_ordering[1]` = `"M-Th-1CN"`
- rule `pr_rule_dipole_trend` / reference `pr_result_trend` / field `$.comparison.dipole_ordering` / result path `$.comparison.dipole_ordering[2]` = `"M-Th-2CN"`
- rule `pr_rule_dipole_trend` / reference `pr_result_trend` / field `$.comparison.esp_ordering` / result path `$.comparison.esp_ordering[0]` = `"M-Th-0CN"`
- rule `pr_rule_dipole_trend` / reference `pr_result_trend` / field `$.comparison.esp_ordering` / result path `$.comparison.esp_ordering[1]` = `"M-Th-1CN"`
- rule `pr_rule_dipole_trend` / reference `pr_result_trend` / field `$.comparison.esp_ordering` / result path `$.comparison.esp_ordering[2]` = `"M-Th-2CN"`
- rule `pr_rule_dipole_trend` / reference `pr_result_trend` / field `$.comparison.trend_statement` / result path `$.comparison.trend_statement` = `"Final optimized-geometry B3LYP/6-31G(d) dipoles are 1.1570, 3.3674, 5.9387 D for corrected 0/1/2 CN identities; corresponding surface ESP ranges are 29.16, 62.65, 66.23 kcal/mol. Both increase across the corrected series. These are local calculations, not the SI Fig. S11 values."`
- rule `pr_rule_pattern` / reference `pr_result_pattern` / field `$.conclusion` / result path `$.conclusion` = `"Gaussian optimizations, harmonic frequencies and Multiwfn molecular-surface ESP extrema completed for all three neutral singlet monomers. Dipole and surface-ESP trends support cyano-driven polarization qualitatively; the independent B3LY..."`
- rule `pr_rule_final` / reference `pr_final_conclusion` / field `$.limitations` / result path `$.limitations` = `"B3LYP/6-31G(d) differs from the paper B3LYP/6-311G** plus CAM-B3LYP/Multiwfn; one conformer per constitutional isomer; no polymer extension. Surface ESP extrema use an electron-density isosurface of 0.001 a.u. with grid spacing 0.15 Bohr and are reported as a range in kcal/mol."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Explicit neutral-singlet monomer series and SMILES.

Public input files and hashes:

- `agent_input/data/inputs/monomer_series.json` — SHA-256 `6e272ab81a021b70c47853fb6ec8012f74d55b9fdb3b4cd12595ad3e69e495e1`; size=561 bytes; explicit_boundary_fields={"$.charge": 0, "$.molecules[0].smiles": "s1c(Br)ccc1Br", "$.molecules[1].smiles": "s1c(Br)c(C#N)cc1Br", "$.molecules[2].smiles": "s1c(Br)c(C#N)c(C#N)c1Br", "$.multiplicity": 1}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_2/paper_0a62b797f51de2c0/verification_report.md` — verification record; SHA-256 `36070f4e1ff43d0ba6cbf5ff207f0b04304920f354869435e56f5270e8523e17`
- `docs/verification/group_2/paper_0a62b797f51de2c0/report/results.json` — verification record; SHA-256 `d54e5aefbd1435aeb30d66a6f119878198b94995b7728fe7ad57ae8f4036e128`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-0CN_b3lyp_optfreq/esp/surfanalysis.pdb` — referenced successful evidence; SHA-256 `ebb632fa6e44ed77cf33889fbbe918b11d36f57a51a37e8f0e1d81d359323a3e`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-1CN_b3lyp_optfreq/esp/surfanalysis.pdb` — referenced successful evidence; SHA-256 `7084a5888a3308ce86830226997ca2b04482e59c1448805e5c58cee18dcbdd79`
- `docs/verification/group_2/paper_0a62b797f51de2c0/artifacts/gaussian_batch/M-Th-2CN_b3lyp_optfreq/esp/surfanalysis.pdb` — referenced successful evidence; SHA-256 `058de45af4f6bd7e4d381f33b2943fd88231e2e130224a440846b49dc8f1ab0c`
- `docs/verification/group_2/paper_0a62b797f51de2c0/provenance/M-Th-0CN_xtbopt.xyz` — referenced successful evidence; SHA-256 `f483a630d782b34052071392648b7302a9e09a2f65d515cd125e1fd1e52701e6`
- `docs/verification/group_2/paper_0a62b797f51de2c0/provenance/M-Th-1CN_xtbopt.xyz` — referenced successful evidence; SHA-256 `03dbe0ecabcb0f3864956d17d8e9a1ad5ba181a5826765d09c17958b400cf723`
- `docs/verification/group_2/paper_0a62b797f51de2c0/provenance/M-Th-2CN_xtbopt.xyz` — referenced successful evidence; SHA-256 `a68776004e63447999fa7987e4920fb57f46b154aba8fd5f88b0d34da39c8f57`
- `docs/verification/group_2/paper_0a62b797f51de2c0/provenance/author_route_evaluation_audit.json` — referenced successful evidence; SHA-256 `16e98247283c431c79ef909b9d2ad8ced9e809e027b4ab664666f715b397429a`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
