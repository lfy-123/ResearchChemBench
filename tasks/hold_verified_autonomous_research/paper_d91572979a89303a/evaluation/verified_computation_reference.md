# Verified computation reference — paper_d91572979a89303a (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Current evidence status — NOT_RELEASE_READY (2026-09-18)

The `provenance/strict_v2_observables.json` archive in `docs/verification/group_3/paper_d91572979a89303a` contains nine successful states and four local activation barriers (29.9877296, 44.0737680, 20.0681947 and 32.7377591 kcal/mol). These are valid local results, not proof of a connected complete reaction profile. The author's main Scheme 4 / SI p. 51 includes the INT1A → TS2A → INT2A [2,3]-Wittig segment; no successful TS2A/connection branch was located in the inspected record. `provenance/restored_inputs/TS2A.xyz` is an input structure, not a completed calculation.

The public task now states the half-entropy definition `G = E_solution_SP + Hcorr - 0.5*(Hcorr-Gcorr)`; this clarifies the quantity without filling the missing network evidence. Actual stored inputs use wB97XD and must not be relabeled as a separately computed GD3BJ branch. Before full-target release, locate a successful mapped TS2A/path record and connect the common-reference network. Four local barriers must not silently replace that requirement. No new calculation, target reduction or directory move was performed. Historical PASS/full-profile claims below are superseded to this extent only.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **NOT_VERIFIED_FOR_FULL_CURRENT_TARGET**
- Applicability note: See the current evidence correction above; historical execution success is not full target validation.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 4 | `PASS` | 最终判定：**PASS（严格作者路线，评估任务范围内）** |
| 49 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 report/results.json、artifacts/gaussian/ 和 provenance/。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: d5gc05901a 3226..3231 ++
- DOI: `10.1039/d5gc05901a`
- Task package: `tasks/final_verified_autonomous_research/paper_d91572979a89303a`
- Verification group: `docs/verification/group_3/paper_d91572979a89303a`
- Paper documents: `papers/paper_d91572979a89303a`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "candidates": [
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "minimum frequency check",
      "frequency_validation": "normal termination; imaginary_frequency_count=0",
      "geometry_provenance": "artifacts/gaussian/1a/1a_optimized.xyz",
      "id": "1a",
      "state_type": "minimum",
      "status": "validated"
    },
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "minimum frequency check",
      "frequency_validation": "normal termination; imaginary_frequency_count=0",
      "geometry_provenance": "artifacts/gaussian/txt/txt_optimized.xyz",
      "id": "txt",
      "state_type": "minimum",
      "status": "validated"
    },
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "minimum frequency check",
      "frequency_validation": "normal termination; imaginary_frequency_count=0",
      "geometry_provenance": "artifacts/gaussian/propellane/propellane_optimized.xyz",
      "id": "propellane",
      "state_type": "minimum",
      "status": "validated"
    },
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "minimum frequency check",
      "frequency_validation": "normal termination; imaginary_frequency_count=0",
      "geometry_provenance": "artifacts/gaussian/INT1A_rerun_retry/INT1A_rerun_retry_optimized.xyz",
      "id": "INT1A_rerun_retry",
      "state_type": "minimum",
      "status": "validated"
    },
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "minimum frequency check",
      "frequency_validation": "normal termination; imaginary_frequency_count=0",
      "geometry_provenance": "artifacts/gaussian/INT2A_rerun_retry/INT2A_rerun_retry_optimized.xyz",
      "id": "INT2A_rerun_retry",
      "state_type": "minimum",
      "status": "validated"
    },
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "artifacts/gaussian/TS1A_rerun_retry_irc/parsed_observables.json",
      "frequency_validation": "normal termination; imaginary_frequency_count=1",
      "geometry_provenance": "artifacts/gaussian/TS1A_rerun_retry/TS1A_rerun_retry_optimized.xyz",
      "id": "TS1A_rerun_retry",
      "state_type": "transition_state",
      "status": "validated"
    },
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc/parsed_observables.json",
      "frequency_validation": "normal termination; imaginary_frequency_count=1",
      "geometry_provenance": "artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/TS3A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz",
      "id": "TS3A_TXT_rerun_retry_unbounded_recovery96g",
      "state_type": "transition_state",
      "status": "validated"
    },
    {
      "charge_multiplicity": "as supplied SI model",
      "connected_state_ids": [],
      "connectivity": "TXT-catalysed thioaromatization model state",
      "connectivity_validation": "artifacts/gaussian/TS3B_rerun_retry_irc/parsed_observables.json",
      "frequency_validation": "normal termination; imaginary_frequency_count=1",
      "geometry_provenance": "artifacts/gaussian/TS3B_rerun_retry/TS3B_rerun_retry_optimized.xyz",
      "id": "TS3B_rerun_retry",
      "state_type": "transition_state",
      "status": "validated"
    },
    "<success-only excerpt: 8 of 9 entries>"
  ],
  "conclusion": "Under the matched wB97XD/def2-TZVP IEFPCM(toluene) route and SI half-entropy convention, TXT lowers aromatization from 44.0738 to 20.0682 kcal/mol. Within the TXT-assisted cycle, deamination is the largest barrier (32.7378 kcal/mol) and the model rate-limiting step.",
  "coverage": "All supplied/restored minima and four labelled TS candidates with IRC checks.",
  "limitations": "One conformer per labelled state; the profile is limited to the validated SI-derived candidate network and does not establish a global conformational search or experimental kinetics. Barrier references are state-specific and use the SI half-entropy convention.",
  "method": {
    "model": "wB97XD/def2SVP with D3BJ-style dispersion",
    "software_or_code": "Gaussian 16 C.01",
    "thermochemistry": "Gaussian 298.15 K harmonic thermal free energies"
  },
  "profiles": [
    {
      "barriers": [
        {
          "comparison_label": "initial_attack",
          "reference_state": "1a+2a",
          "transition_state_id": "TS1A_rerun_retry",
          "unit": "kcal/mol",
          "validation_evidence": "provenance/strict_v2_observables.json#barriers.initial_attack",
          "value": 29.987729598463076
        },
        {
          "comparison_label": "TXT-assisted_aromatization",
          "reference_state": "INT2A+TXT",
          "transition_state_id": "TS3A_TXT_rerun_retry_unbounded_recovery96g",
          "unit": "kcal/mol",
          "validation_evidence": "provenance/strict_v2_observables.json#barriers.TXT-assisted_aromatization",
          "value": 20.06819474694376
        },
        {
          "comparison_label": "uncatalyzed_aromatization",
          "reference_state": "INT2A",
          "transition_state_id": "TS3B_rerun_retry",
          "unit": "kcal/mol",
          "validation_evidence": "provenance/strict_v2_observables.json#barriers.uncatalyzed_aromatization",
          "value": 44.07376797036684
        },
        {
          "comparison_label": "deamination",
          "reference_state": "INT3A_TXT",
          "transition_state_id": "TS4A_TXT_rerun_retry_unbounded_recovery96g",
          "unit": "kcal/mol",
          "validation_evidence": "provenance/strict_v2_observables.json#barriers.deamination",
          "value": 32.737759120775245
        }
      ],
      "catalyst_context": "TXT explicit model",
      "pathway_id": "TXT-assisted sequence",
      "states": [
        "1a",
        "txt",
        "propellane",
        "INT1A_rerun_retry",
        "INT2A_rerun_retry",
        "TS1A_rerun_retry",
        "TS3A_TXT_rerun_retry_unbounded_recovery96g",
        "TS3B_rerun_retry",
        "<success-only excerpt: 8 of 9 entries>"
      ]
    }
  ],
  "provenance": {
    "barrier_recalculation": "provenance/strict_v2_observables.json",
    "conversion": "Hartree differences converted once with 627.509474 kcal mol^-1.",
    "method_consistency": "All nine required states have normal Gaussian Link1 completion and frequency signatures; each barrier uses its stated preceding state(s)."
  },
  "status": "complete"
}
```

## Re-audit source-evidence drift

- Classification: **SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW**
- Previous `results.json` SHA-256: `db5440a524de747cafb7f786613c19397a350e2d7eb44da29fab5db350de42b0`
- Current `results.json` SHA-256: `610b0576a9be0ca79746232331c2eaa6a65d91c27aac6c9d9945ecef770dca04`
- Changed top-level result fields: `conclusion, limitations, profiles, provenance`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["conclusion", "limitations", "profiles", "provenance"], "classification": "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW", "current_sha256": "610b0576a9be0ca79746232331c2eaa6a65d91c27aac6c9d9945ecef770dca04", "detected": true, "previous_sha256": "db5440a524de747cafb7f786613c19397a350e2d7eb44da29fab5db350de42b0"} -->

Paper/SI document hashes:

- `papers/paper_d91572979a89303a/documents/main.pdf` — SHA-256 `2eba8cd5bc4372e9dad5edbe6c15a48c55ad80012b9a27d435870bb1f6c4d664` (declared_match=True)
- `papers/paper_d91572979a89303a/documents/supplementary_001.pdf` — SHA-256 `4ed906d3929bc6efd125b7ea86eff304aff73dab67d89d7149c0395d0d9ebd1e` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **200**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/status.json` — successful status record; SHA-256 `69b0c2f5f15a99d876a17e93d2f13fec1d71ca179cd4f5d7e8166073ce6a38c5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/1a_optimized.xyz` — successful execution artifact; SHA-256 `974348d8e408a54a8fb71a1daf0cd5d1f7952a6f5ee422f717c27aae5d8087ea`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/collection.json` — successful execution artifact; SHA-256 `f5fdeca44818c122c8dcf65f0540e58d3dd1f090c4e434c5226a5c35c246a5bf`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/formchk.log` — successful execution artifact; SHA-256 `07800cdb85ac4a74c05c26d5f8a8ca4b28b0f09ae27b50f8c108a890da10ef00`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/input.com` — successful execution artifact; SHA-256 `a40614d2eda1d47e8a132d8f5e48e1fe513f6a4c7153b920c6f35c7cc34e7483`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/status.json` — successful status record; SHA-256 `dc118ad199dad7ca1951e74800fbe7ef2bcb585c73e3894ace1e6e33bde4238e`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/1a_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `a44337cd5033b6e1dcf924732933e3f86c54aedf90ad3767746b1e23d14831b1`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `ad91fe0bb2a4695efe0718d7a4664877a56fa01509d07f7b13b1859ab756b26c`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `cb1b9e8b5a96d2aed007dbb10c81916e9b877df2a8065e816961d64a2d4e8ff8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `faee93885e2a893ba0b612468b448b5c677e4a2e8cd79526dcf1ec2586daed7a`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/2a_author_route_strict_v2/status.json` — successful status record; SHA-256 `e38f7c42a1500d1ab86ebc521f73a35f158c8b92924fa69a77cdcb28ebb62bd8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/2a_author_route_strict_v2/2a_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `81761aa6535f9b391715d359e1c9d171a9ab0521bd450286da1696975b2b7cd8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/2a_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `ce54086c968db0a4e615fb5823d0fc5ce60fc1c1c9558ef560e3032497ae430f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/2a_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `0e9b22d5222872a99c85ef8019e35c1a1166ab4b78cd6529903c03da59d2cafa`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/2a_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `3a8e8838959332caa67cdf26b85aee4a599b0128f80a62dc77acc958daa1e70f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/status.json` — successful status record; SHA-256 `f0be6886899e14f87b180bd3d3553b800804f1e77eb4243b26b92fbac1ebc0a3`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/3a_rerun_retry_optimized.xyz` — successful execution artifact; SHA-256 `baf7566594cba4a28862881f55425f3cd9eb1a672cd55fad7a12b9fe025f7bf0`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/collection.json` — successful execution artifact; SHA-256 `e9ad91ad2db35ea81f11e173689812fb95754ca4912ce389dcd52344299068af`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/formchk.log` — successful execution artifact; SHA-256 `260564df4a69148165b085161ab0a6f6f39d7f8af925b76140bba602d6c8cf14`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/input.com` — successful execution artifact; SHA-256 `825222cb2a0943886e5abe98d8a9e719911876dffe6ad3bcfedccfc7208eccc5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/status.json` — successful status record; SHA-256 `92caade074a470e9986a1922ee2135f2ccfd4c94dd9be4c6d92aad6301977d8d`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/INT1A_rerun_retry_optimized.xyz` — successful execution artifact; SHA-256 `d32fd0cd99674f0f6ddef2cb75737c08d0c4c26b6561e3fd8af86adc0baa4fe5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/collection.json` — successful execution artifact; SHA-256 `7fd529bd0a272658d620f3fa5eb4d31dc7bd68c3b70c9cdc7fb9c21be47a4482`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/formchk.log` — successful execution artifact; SHA-256 `26122d2bf7326663695600e1418bd2a4ff2593d33bfbd8509cef792635de876f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/input.com` — successful execution artifact; SHA-256 `b7262b099d03ae22eefd31d56aea5a7df857db414e71fcaa0ad0bce50a1e91ed`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_author_route_strict_v2/status.json` — successful status record; SHA-256 `ce84b49dbfd186d8dfd0c4ff2a277ba8ed05206b95d83e4f4b067612d6ebc2ed`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_author_route_strict_v2/INT2A_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `44e208e809b6f7b096be3947018c9fb07ec8617288c4b6ef4ee79c2334af0014`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `3fb6b93b4da7da76fb7ea29ef1ec2a7d6ef10161a91b3aa5fc0f437772f23bf8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `57b720a7886610ac5a5802ad58851509ca8816027267787f41c1e910b1e06113`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `3f495f727f842840c8aa411d39531e884dc69750f3b9f853ed358e8cb07b8319`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/status.json` — successful status record; SHA-256 `625bea50b768de3036fb8fb6decb8d9abb95ace505e9103524db784ba9b0ce76`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/INT2A_rerun_retry_optimized.xyz` — successful execution artifact; SHA-256 `8698280b31409f75ed6074fd1d8ec5b1746f10aff0431473a0120bb264befae0`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/collection.json` — successful execution artifact; SHA-256 `9c50c8c45e81fd2a9e7e087e8d0ed38407aa20a90da5e828660349a67b4a669a`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/formchk.log` — successful execution artifact; SHA-256 `8e003cb535bf611d508aa6c0fbc9541fce144ffda8ef4de9ecf91138f53a1cbb`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/input.com` — successful execution artifact; SHA-256 `d2d3169c63e8725a044512d45fee19a9086ba0cde834f87a61716c2cdfb15bff`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT3A_TXT_author_route_strict_v2/status.json` — successful status record; SHA-256 `31020baa8f56b1c8dde97c248d8db236f7b4c6d1cc98f4e082b36e26cb859b44`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT3A_TXT_author_route_strict_v2/INT3A_TXT_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `62757e8b2ef21ea66315109245d7b0fc1de9b400b451af8ea97bea5da32cfdac`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT3A_TXT_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `40c39b80ed55226a49c7f6c9875c20f3d1248db433ff3ddfe726e725fe7f9496`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT3A_TXT_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `de8d3b8ae088a2f6aa976b516dddbdb1db4d006ab52428c7123dcd2f1eda45f6`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT3A_TXT_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `d6cbcdf5315b0d873457f5306f179f238884e25e67c24ad66a8bfaa237f62485`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_author_route_strict_v2/status.json` — successful status record; SHA-256 `dd81991f04a773cd20fda770138a9e3e806dd6a3b0536b1620c0f1fa98ff46c9`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_author_route_strict_v2/TS1A_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `b0fdc5529d4d386735bcf899917716a5a6a5f615f18d0ac38a86f6ebe44f24b6`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `580330875dc9931e59c982ef7fbdb35bc5be1ea29f8054bb07009814d1cbe2f6`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `c766f1875efcdec534e515c1b0bd70749ede3b6987b5946c0fc3e1814cbb5b58`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `574f4372efb3049521d4d9da8b9fa711c25b49a95282bac0beb4cfda83b56ea0`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/status.json` — successful status record; SHA-256 `c757f0d721e186229f7c089906eab504062cf68cbfc8b83c5494750e6249c076`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/TS1A_rerun_retry_optimized.xyz` — successful execution artifact; SHA-256 `16cdf2e05fd5750cf868eb3405ce7cfb78ac588e6f9b258a4f658c0a493480b8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/collection.json` — successful execution artifact; SHA-256 `fc5b1dd59fae776424975d48bc61c2a8c0499db641a449d1267a975ca05d0478`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/formchk.log` — successful execution artifact; SHA-256 `1fd7cd67cf793cf2d9b1f8eee435ecb0f7998ba8dc0ef3692a4931e7fb628a06`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/input.com` — successful execution artifact; SHA-256 `245cd6383015dbf02d044787e9de7a416b8304be6fe2f6fd052b9c931522508b`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/status.json` — successful status record; SHA-256 `b1d2598fd55aefbafe51780e9c58e1be5a7e19e5a3ee18d5c1bfad7f1815f7ca`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/TS1A_rerun_retry_irc2_unbounded16g_optimized.xyz` — successful execution artifact; SHA-256 `ddbe4209554941ffd716457377f0a3d024213f9e413bccbff6890bd2988dbcac`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/collection.json` — successful execution artifact; SHA-256 `bdb138a63a17d257d521bff0e5b10def068073a65712f1c7094c8fac5d2c3922`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/formchk.log` — successful execution artifact; SHA-256 `01897ae95f040219a9cdc72c1de2c6db32d95603bc7ca3a093e4cab148ca7256`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/input.com` — successful execution artifact; SHA-256 `fb4cde7f680c701a3dfd0dce1ee9c28a8c6b627d9b9cc003e50f88734e31a68c`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/status.json` — successful status record; SHA-256 `7f687be30dac39f782140ef44310dbeb953f966d342657195c4883965429464f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/TS1A_rerun_retry_irc3_unbounded16g_optimized.xyz` — successful execution artifact; SHA-256 `81d4573f345206cbc8ecba2da2696541f88c33d35f6d731bad4e48678a61c123`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/collection.json` — successful execution artifact; SHA-256 `77de9281e100068ef4fde580037074bfc18a4a8e320cabcd86f721368105f9d0`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/formchk.log` — successful execution artifact; SHA-256 `40f6c292594cf8e1f941f6d9a9c5f00c8798ac7336e06315c538045ce00d8327`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/input.com` — successful execution artifact; SHA-256 `6e656f17ef678104bf0ac3720e5cf537068a28e8aa9e4aff8d6aad40d0a049d6`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_author_route_strict_v2/status.json` — successful status record; SHA-256 `758bcf2ac9e6d96ed6776474a635a7674e43c10d5a019bff0f479f8a7ec54edb`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_author_route_strict_v2/TS3A_TXT_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `1a488802a44dabf407eee568295e4c934d89f013b1184d932038c1ceaf86cd2d`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `cd9085c9ffc2f9560fabbd516be22fe74ee00462eb5dd14784fd45798b02baf5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `e77c300a2d0a6bc71d363d788c6c59b918b0a7eda3d69871d4ae78c9034b17d8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `d2ac7ccaaee0d700b611de26f8d900ac2c80b620bc31ab471dd004bc1e77ebc0`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/status.json` — successful status record; SHA-256 `4b68889e209710c585bafeff35311d690745c8d767f277b27a31e956a44539e7`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/TS3A_TXT_rerun_retry_optimized.xyz` — successful execution artifact; SHA-256 `29d0154abbd22724533cf38f1d387682b704fe05172c41c21d61e21bbd8d19fa`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/collection.json` — successful execution artifact; SHA-256 `36736448aa723193ec9db8cc84bad0da7956822fe0c6e7b78748c943b8ea0420`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/formchk.log` — successful execution artifact; SHA-256 `b585332932698600978b8347f79100be81684a5a5c0912d33b8ee5a2901bbe7f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/input.com` — successful execution artifact; SHA-256 `686d43bb46d4d27c993445f32060c86f57e0f3b163880eb1a649e415a2f2437e`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/status.json` — successful status record; SHA-256 `90003452795272bc6b52575313ba348f887b6ce83699c8210b04db1e93d5a62b`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/TS3A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz` — successful execution artifact; SHA-256 `ff67d56cd4eb04074a5d4e2668b92d15bddd32bb9a255f49e1c3f3cd84cede75`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/collection.json` — successful execution artifact; SHA-256 `56ffc6984f99f70bb1a7f48a207892261500fce5acc18bbd302961d264620281`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/formchk.log` — successful execution artifact; SHA-256 `32d395319c3ac8ff80913b686c539a4e99d7768a5bb6cbe5cbea242285d3524b`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/input.com` — successful execution artifact; SHA-256 `932b5b0d19d32abd67a020bf476d8dfcb5c75ec25bcadb4b3164a579ee8ed5a3`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/status.json` — successful status record; SHA-256 `ce749b9b1c345ef4fd32fff499e9650b5b72cf7db12638f574a1a30ae2150b95`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_optimized.xyz` — successful execution artifact; SHA-256 `75869d21c0ceba4ba4249b0f8c2e329498bf69e84806b90bf1094351a7e41e4f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/formchk.log` — successful execution artifact; SHA-256 `5be710bf315763458c4b977f69a2d891a16f4b80e8990e92ce9e68d76b14349b`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/input.com` — successful execution artifact; SHA-256 `b4ce543bf2d32d943da1914949c7a093c8d8d23813ea1bc34557fd947810f277`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/parsed_observables.json` — successful execution artifact; SHA-256 `7b18334a93985114f333ddbd3ec813cdab2fdc3492b45876d5621a5c43ef1e8d`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_author_route_strict_v2/status.json` — successful status record; SHA-256 `ccd8d85fd2d45ca658c4b6c57082a2467b9e9daa9fb50c29305207a7d971b77c`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_author_route_strict_v2/TS3B_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `6617f08acffce61716e9dcd9016248c80c75934966179c36310a06907c6d064e`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `6aca231d138372e667424859cbda1a16b2227c25fa717ea2dd2983ee7ed234ce`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `4daaff48efbbe67bd56f49cd0b55888fb1c0f133ce08ab36f77c4fdca2c0bddd`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `7885004da3d2066f162c0e828d1368a2597ed45f74b6e76ec68dfc4e038f9182`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/status.json` — successful status record; SHA-256 `126bd4cc09bae6c8b79dfd4467d9e0044f51bd1306a3e86932edad92a9ef5bf5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/TS3B_rerun_retry_optimized.xyz` — successful execution artifact; SHA-256 `a4721482a34b8400fa4e91b637affba761c0a88dc16fbb56099f654942e30ac9`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/collection.json` — successful execution artifact; SHA-256 `89adfd28af3c2e110003298af61544c02b421c1705d8f3d4f349f99d562a8583`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/formchk.log` — successful execution artifact; SHA-256 `2fcf077b763810bf30b1bf14b5a81ae5fae0b5099557396ce7e669b9f1b0a05d`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/input.com` — successful execution artifact; SHA-256 `de69246ee6c5e80a57b8af27438f121ab973139314be807c4acf3462027b2ffd`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/status.json` — successful status record; SHA-256 `f376f0e44d5f91d897e24a4a1ebcdb807dc98605c1668e5288538386e07ef8dd`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/TS3B_rerun_retry_irc_optimized.xyz` — successful execution artifact; SHA-256 `6750a62445078599de925c5997dc5c53a04ca621d10096531f1ce0b02a131fe8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/collection.json` — successful execution artifact; SHA-256 `74e5e6eb7dda7fbd78bd761317e9b152f8e6d195ae4bcb0e354d8a972b2c3d21`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/formchk.log` — successful execution artifact; SHA-256 `f72e27b495ddba580a4bf4f023a15b6d585382d8b5338027e2b31e7e7d578ab4`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/input.com` — successful execution artifact; SHA-256 `ca991be51e0286d55edd72927850c229112593aee1253356d457efa13ecca745`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_author_route_strict_v2/status.json` — successful status record; SHA-256 `e5b8aa25487306143186c148896d7c71acb9149c9a4f11d741637561f57e055f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_author_route_strict_v2/TS4A_TXT_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `4a0baf6e5ecc93e0e6ac33d1d66eb0b6eb745efd00550ce2312f4786069106ec`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `ce6fb0ad096c9c453ec1b5d19d392e861c51c22605170a83a55d7419ab907a77`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `b3b24a2254953fcb2d90a7912bd8f5581466443778f028177a44234e4109fae5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `ea4830ea80b06272ff60d49159d78d25aaa31d85e4f2269b52d2290fc2b636b5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/status.json` — successful status record; SHA-256 `91821b184009284ca4f720ed585c4787f8988b5957de67518beb50ed0533b534`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/TS4A_TXT_rerun_retry_optimized.xyz` — successful execution artifact; SHA-256 `6164889fcc83e35f4ffbc96deab46c713999ae64942a25f2a4f512a635da3425`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/collection.json` — successful execution artifact; SHA-256 `e481bf622521ec3352f780a2e08bab4da3ddc0435dc6353f857e4bf781a6f37b`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/formchk.log` — successful execution artifact; SHA-256 `bef2496dbae4ec9e7c6144d56b1fda91e79e9f1b5eebfc284a39c62879066a0e`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/input.com` — successful execution artifact; SHA-256 `618446560c32f707a85967e94738be3cb5aed7768791fa2afff174753e32083f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/status.json` — successful status record; SHA-256 `023b4e6676d82bf0ba63c25b60ce871b47c79373b052d0b0f9fa2e9bf941c233`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/TS4A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz` — successful execution artifact; SHA-256 `2ee33a6ceee077298897fc82d4de0fa1281a19f2a68241b09e9276607ed7a30c`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/collection.json` — successful execution artifact; SHA-256 `71ecd26fd85261ec2caf6cba2dfd136df598f8b8e1a7c8b640f348a586fc497a`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/formchk.log` — successful execution artifact; SHA-256 `cae7ca323e02ed6fdb01972f98aaf1cd87fb9c21bbb3a6a2d238a34d294712cd`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/input.com` — successful execution artifact; SHA-256 `cfe52cc9320201c1e4af7dd035bf123a3a041274beb33f41ef306aae62d7ad4d`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/status.json` — successful status record; SHA-256 `60059359add7997048e8c130cf8cdeceeeff0565e8ba35a18373291fdb887a53`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_optimized.xyz` — successful execution artifact; SHA-256 `c5518ac58a8e5e9e2122cc93818077380b9d35d26d4ef549963ebc51313b89d8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/formchk.log` — successful execution artifact; SHA-256 `ef62bfb8b38b2965b3bd1349486b2998fbffe386c6ae40b884a3a0234e0d7988`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/input.com` — successful execution artifact; SHA-256 `b4f652111e561ad70b1e60e9aa447104feb9922eb4c6e0a033b437ddd68a2cab`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/parsed_observables.json` — successful execution artifact; SHA-256 `3a54a40a758f713b2c0d0dc322396e5c5a134f59a07d38c393f1600904cdff1b`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TXT_author_route_strict_v2/status.json` — successful status record; SHA-256 `e703d36f03bfc41ea5f2217865ee3bfbface57917416ce41fca95c9257cd2f86`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TXT_author_route_strict_v2/TXT_author_route_strict_v2_optimized.xyz` — successful execution artifact; SHA-256 `193be44d0174bc52c0b991893f3410e86f126ea7de9d005d606b2c0b9c377466`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TXT_author_route_strict_v2/formchk.log` — successful execution artifact; SHA-256 `b3fb145499d09155c706aac06e07bd564eb7ad4e719460c813deb075e462a2ec`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TXT_author_route_strict_v2/input.com` — successful execution artifact; SHA-256 `5297b90fa701f89b9b41c9af1adc0e403c15412ea15692ccb3f701f82007dab6`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TXT_author_route_strict_v2/parsed_observables.json` — successful execution artifact; SHA-256 `072ce03e618df4ffaa8c7628171e47dc35cfaa9a9d85def756795d46e23b31dd`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/status.json` — successful status record; SHA-256 `7a81c2d0281578a5b51f62d93b23b4b37457467b394bde849d4dbd7c968748f3`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/collection.json` — successful execution artifact; SHA-256 `8a6f6f21a8461b928a03aaf362c68f64f915d6300c6c1321ac63c08d8904f01b`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/formchk.log` — successful execution artifact; SHA-256 `af186da31a16c8bab756f629b371d58cd3e4ea11b1d713f7b9c748c72912d527`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/input.com` — successful execution artifact; SHA-256 `deb6db2c3e44dbccaf90bf32f14ee08820882e7fc4b563ab70526d65d63de6e7`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/parsed_observables.json` — successful execution artifact; SHA-256 `1f366f314bec71991e87c948ccbd5ae5cd9bd830f70be03f77b3d78837567280`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/status.json` — successful status record; SHA-256 `87770d5f89b754c667a66d10f3b594411a9b73f68c6f21c14b145e5cf6bd841f`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/collection.json` — successful execution artifact; SHA-256 `9274d78ec656a95b6cdd91b213f78e2d8288c2caa59718def86d5967606f2407`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/formchk.log` — successful execution artifact; SHA-256 `b92ef4fc86914a602fc2b6a399ed9b47a496e36b8d898d444391f01afc0bb765`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/input.com` — successful execution artifact; SHA-256 `4248162f1ea047a159dfeb52cb422706386ffc2ec7d2e095e6d9a9eb5d4f3edb`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/parsed_observables.json` — successful execution artifact; SHA-256 `93d8cef2a82ae80319a237560997cb2c95593c29dcef695436bfddca32dd779d`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/1a/outputs/execution_jobs/job_5a68cb4098674b369d57c1f89919b83c/status.json` — successful status record; SHA-256 `69b0c2f5f15a99d876a17e93d2f13fec1d71ca179cd4f5d7e8166073ce6a38c5`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/1a/outputs/execution_jobs/job_5a68cb4098674b369d57c1f89919b83c/collection.json` — successful execution artifact; SHA-256 `f5fdeca44818c122c8dcf65f0540e58d3dd1f090c4e434c5226a5c35c246a5bf`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/1a/outputs/execution_jobs/job_5a68cb4098674b369d57c1f89919b83c/input.com` — successful execution artifact; SHA-256 `a40614d2eda1d47e8a132d8f5e48e1fe513f6a4c7153b920c6f35c7cc34e7483`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/1a/outputs/execution_jobs/job_5a68cb4098674b369d57c1f89919b83c/request.json` — successful execution artifact; SHA-256 `4f09631b642b1b8751eb486d5bbe8afad89e7848f881cc636af16b0d07c75604`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/1a/outputs/execution_jobs/job_5a68cb4098674b369d57c1f89919b83c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/3a_rerun_retry/outputs/execution_jobs/job_fb09b321011a40d99951414c5e149215/status.json` — successful status record; SHA-256 `f0be6886899e14f87b180bd3d3553b800804f1e77eb4243b26b92fbac1ebc0a3`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/3a_rerun_retry/outputs/execution_jobs/job_fb09b321011a40d99951414c5e149215/collection.json` — successful execution artifact; SHA-256 `e9ad91ad2db35ea81f11e173689812fb95754ca4912ce389dcd52344299068af`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/3a_rerun_retry/outputs/execution_jobs/job_fb09b321011a40d99951414c5e149215/input.com` — successful execution artifact; SHA-256 `825222cb2a0943886e5abe98d8a9e719911876dffe6ad3bcfedccfc7208eccc5`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/3a_rerun_retry/outputs/execution_jobs/job_fb09b321011a40d99951414c5e149215/request.json` — successful execution artifact; SHA-256 `a27e2704d5121b0df3e2cefe9014bb6400b089921c4bbc6eff8cd03741d78e9a`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/3a_rerun_retry/outputs/execution_jobs/job_fb09b321011a40d99951414c5e149215/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT1A_rerun_retry/outputs/execution_jobs/job_1fb8a11167b24f399fca0b23646208e2/status.json` — successful status record; SHA-256 `92caade074a470e9986a1922ee2135f2ccfd4c94dd9be4c6d92aad6301977d8d`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT1A_rerun_retry/outputs/execution_jobs/job_1fb8a11167b24f399fca0b23646208e2/collection.json` — successful execution artifact; SHA-256 `7fd529bd0a272658d620f3fa5eb4d31dc7bd68c3b70c9cdc7fb9c21be47a4482`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT1A_rerun_retry/outputs/execution_jobs/job_1fb8a11167b24f399fca0b23646208e2/input.com` — successful execution artifact; SHA-256 `b7262b099d03ae22eefd31d56aea5a7df857db414e71fcaa0ad0bce50a1e91ed`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT1A_rerun_retry/outputs/execution_jobs/job_1fb8a11167b24f399fca0b23646208e2/request.json` — successful execution artifact; SHA-256 `11a169be0cda26d7b3dfa87432715e176a4ea9e5c6e1a04a96b58da76123a8e8`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT1A_rerun_retry/outputs/execution_jobs/job_1fb8a11167b24f399fca0b23646208e2/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT2A_rerun_retry/outputs/execution_jobs/job_af59560ffe3d4c2f86777218006f8202/status.json` — successful status record; SHA-256 `625bea50b768de3036fb8fb6decb8d9abb95ace505e9103524db784ba9b0ce76`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT2A_rerun_retry/outputs/execution_jobs/job_af59560ffe3d4c2f86777218006f8202/collection.json` — successful execution artifact; SHA-256 `9c50c8c45e81fd2a9e7e087e8d0ed38407aa20a90da5e828660349a67b4a669a`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT2A_rerun_retry/outputs/execution_jobs/job_af59560ffe3d4c2f86777218006f8202/input.com` — successful execution artifact; SHA-256 `d2d3169c63e8725a044512d45fee19a9086ba0cde834f87a61716c2cdfb15bff`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT2A_rerun_retry/outputs/execution_jobs/job_af59560ffe3d4c2f86777218006f8202/request.json` — successful execution artifact; SHA-256 `5af0f7b6e8ceb7d51d39c94bbe4885f67312f846d22d2010af9385ff34902142`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/INT2A_rerun_retry/outputs/execution_jobs/job_af59560ffe3d4c2f86777218006f8202/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry/outputs/execution_jobs/job_fc91d7c278ca498a9d958756938067af/status.json` — successful status record; SHA-256 `c757f0d721e186229f7c089906eab504062cf68cbfc8b83c5494750e6249c076`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry/outputs/execution_jobs/job_fc91d7c278ca498a9d958756938067af/collection.json` — successful execution artifact; SHA-256 `fc5b1dd59fae776424975d48bc61c2a8c0499db641a449d1267a975ca05d0478`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry/outputs/execution_jobs/job_fc91d7c278ca498a9d958756938067af/input.com` — successful execution artifact; SHA-256 `245cd6383015dbf02d044787e9de7a416b8304be6fe2f6fd052b9c931522508b`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry/outputs/execution_jobs/job_fc91d7c278ca498a9d958756938067af/request.json` — successful execution artifact; SHA-256 `399ecfd23cc3b893be32290aa20118e5d7063491555f3946ec8788c31cf130e5`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry/outputs/execution_jobs/job_fc91d7c278ca498a9d958756938067af/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc2_unbounded16g/outputs/execution_jobs/job_6e27d6634e374c07b7c852b048d24015/status.json` — successful status record; SHA-256 `b1d2598fd55aefbafe51780e9c58e1be5a7e19e5a3ee18d5c1bfad7f1815f7ca`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc2_unbounded16g/outputs/execution_jobs/job_6e27d6634e374c07b7c852b048d24015/collection.json` — successful execution artifact; SHA-256 `bdb138a63a17d257d521bff0e5b10def068073a65712f1c7094c8fac5d2c3922`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc2_unbounded16g/outputs/execution_jobs/job_6e27d6634e374c07b7c852b048d24015/input.com` — successful execution artifact; SHA-256 `fb4cde7f680c701a3dfd0dce1ee9c28a8c6b627d9b9cc003e50f88734e31a68c`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc2_unbounded16g/outputs/execution_jobs/job_6e27d6634e374c07b7c852b048d24015/request.json` — successful execution artifact; SHA-256 `9672b17201418665182dc4fe0d01d275dacfb3d3ba952d7e64133b48c17ebb4e`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc2_unbounded16g/outputs/execution_jobs/job_6e27d6634e374c07b7c852b048d24015/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc3_unbounded16g/outputs/execution_jobs/job_ce00df3ec3c7479a82afa1b28b927cdc/status.json` — successful status record; SHA-256 `7f687be30dac39f782140ef44310dbeb953f966d342657195c4883965429464f`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc3_unbounded16g/outputs/execution_jobs/job_ce00df3ec3c7479a82afa1b28b927cdc/collection.json` — successful execution artifact; SHA-256 `77de9281e100068ef4fde580037074bfc18a4a8e320cabcd86f721368105f9d0`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc3_unbounded16g/outputs/execution_jobs/job_ce00df3ec3c7479a82afa1b28b927cdc/input.com` — successful execution artifact; SHA-256 `6e656f17ef678104bf0ac3720e5cf537068a28e8aa9e4aff8d6aad40d0a049d6`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc3_unbounded16g/outputs/execution_jobs/job_ce00df3ec3c7479a82afa1b28b927cdc/request.json` — successful execution artifact; SHA-256 `0ebfc0cd56695a318a3c932d1a5aadd1e72a8238c3594c64c8c4ee7dacd1154a`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS1A_rerun_retry_irc3_unbounded16g/outputs/execution_jobs/job_ce00df3ec3c7479a82afa1b28b927cdc/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry/outputs/execution_jobs/job_ff806e2dd8fb452088e28914819bd25c/status.json` — successful status record; SHA-256 `4b68889e209710c585bafeff35311d690745c8d767f277b27a31e956a44539e7`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry/outputs/execution_jobs/job_ff806e2dd8fb452088e28914819bd25c/collection.json` — successful execution artifact; SHA-256 `36736448aa723193ec9db8cc84bad0da7956822fe0c6e7b78748c943b8ea0420`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry/outputs/execution_jobs/job_ff806e2dd8fb452088e28914819bd25c/input.com` — successful execution artifact; SHA-256 `686d43bb46d4d27c993445f32060c86f57e0f3b163880eb1a649e415a2f2437e`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry/outputs/execution_jobs/job_ff806e2dd8fb452088e28914819bd25c/request.json` — successful execution artifact; SHA-256 `b3c3adc3a3d7c6f7d8c03a6e5c0bcfff6a9221fa89718174b0e8871b6b670af7`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry/outputs/execution_jobs/job_ff806e2dd8fb452088e28914819bd25c/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_28e481ab54cc4e368100fb710f3ba84c/status.json` — successful status record; SHA-256 `90003452795272bc6b52575313ba348f887b6ce83699c8210b04db1e93d5a62b`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_28e481ab54cc4e368100fb710f3ba84c/collection.json` — successful execution artifact; SHA-256 `56ffc6984f99f70bb1a7f48a207892261500fce5acc18bbd302961d264620281`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_28e481ab54cc4e368100fb710f3ba84c/input.com` — successful execution artifact; SHA-256 `932b5b0d19d32abd67a020bf476d8dfcb5c75ec25bcadb4b3164a579ee8ed5a3`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_28e481ab54cc4e368100fb710f3ba84c/request.json` — successful execution artifact; SHA-256 `50dfa49165f3213accedaf9fdd761f0afd91859b7fa27189bbffec85fbe70e94`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_28e481ab54cc4e368100fb710f3ba84c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry/outputs/execution_jobs/job_7a6b117525e242bc869831b42539c824/status.json` — successful status record; SHA-256 `126bd4cc09bae6c8b79dfd4467d9e0044f51bd1306a3e86932edad92a9ef5bf5`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry/outputs/execution_jobs/job_7a6b117525e242bc869831b42539c824/collection.json` — successful execution artifact; SHA-256 `89adfd28af3c2e110003298af61544c02b421c1705d8f3d4f349f99d562a8583`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry/outputs/execution_jobs/job_7a6b117525e242bc869831b42539c824/input.com` — successful execution artifact; SHA-256 `de69246ee6c5e80a57b8af27438f121ab973139314be807c4acf3462027b2ffd`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry/outputs/execution_jobs/job_7a6b117525e242bc869831b42539c824/request.json` — successful execution artifact; SHA-256 `696f3aa56e946d0cf12930ea339a8384ea0927c7960df0da490dfb5e615f8843`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry/outputs/execution_jobs/job_7a6b117525e242bc869831b42539c824/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry_irc/outputs/execution_jobs/job_a42a690ef1274c0fbf98e73895408b38/status.json` — successful status record; SHA-256 `f376f0e44d5f91d897e24a4a1ebcdb807dc98605c1668e5288538386e07ef8dd`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry_irc/outputs/execution_jobs/job_a42a690ef1274c0fbf98e73895408b38/collection.json` — successful execution artifact; SHA-256 `74e5e6eb7dda7fbd78bd761317e9b152f8e6d195ae4bcb0e354d8a972b2c3d21`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry_irc/outputs/execution_jobs/job_a42a690ef1274c0fbf98e73895408b38/input.com` — successful execution artifact; SHA-256 `ca991be51e0286d55edd72927850c229112593aee1253356d457efa13ecca745`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry_irc/outputs/execution_jobs/job_a42a690ef1274c0fbf98e73895408b38/request.json` — successful execution artifact; SHA-256 `22ce38bb35f33db150a57de0b2472eed92d2fe0566290089174e7ae47e5466b2`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS3B_rerun_retry_irc/outputs/execution_jobs/job_a42a690ef1274c0fbf98e73895408b38/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry/outputs/execution_jobs/job_a3d9658f0d1c453295185bb6a88ce69a/status.json` — successful status record; SHA-256 `91821b184009284ca4f720ed585c4787f8988b5957de67518beb50ed0533b534`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry/outputs/execution_jobs/job_a3d9658f0d1c453295185bb6a88ce69a/collection.json` — successful execution artifact; SHA-256 `e481bf622521ec3352f780a2e08bab4da3ddc0435dc6353f857e4bf781a6f37b`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry/outputs/execution_jobs/job_a3d9658f0d1c453295185bb6a88ce69a/input.com` — successful execution artifact; SHA-256 `618446560c32f707a85967e94738be3cb5aed7768791fa2afff174753e32083f`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry/outputs/execution_jobs/job_a3d9658f0d1c453295185bb6a88ce69a/request.json` — successful execution artifact; SHA-256 `f2698acf2e5d7fcf50e59d1cb22a09f51cd64116a544b0cf25cb914567f4609f`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry/outputs/execution_jobs/job_a3d9658f0d1c453295185bb6a88ce69a/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_156221af2771401bac08dcf3010df41a/status.json` — successful status record; SHA-256 `023b4e6676d82bf0ba63c25b60ce871b47c79373b052d0b0f9fa2e9bf941c233`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_156221af2771401bac08dcf3010df41a/collection.json` — successful execution artifact; SHA-256 `71ecd26fd85261ec2caf6cba2dfd136df598f8b8e1a7c8b640f348a586fc497a`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_156221af2771401bac08dcf3010df41a/input.com` — successful execution artifact; SHA-256 `cfe52cc9320201c1e4af7dd035bf123a3a041274beb33f41ef306aae62d7ad4d`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_156221af2771401bac08dcf3010df41a/request.json` — successful execution artifact; SHA-256 `a79bdbe794ff78cb5ed5ca9a427cb1882a926f5b4049e12a1159046945412ca9`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/TS4A_TXT_rerun_retry_unbounded_recovery96g/outputs/execution_jobs/job_156221af2771401bac08dcf3010df41a/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/propellane/outputs/execution_jobs/job_f20c4261abf24f09b8d850c0268c4809/status.json` — successful status record; SHA-256 `7a81c2d0281578a5b51f62d93b23b4b37457467b394bde849d4dbd7c968748f3`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/propellane/outputs/execution_jobs/job_f20c4261abf24f09b8d850c0268c4809/collection.json` — successful execution artifact; SHA-256 `8a6f6f21a8461b928a03aaf362c68f64f915d6300c6c1321ac63c08d8904f01b`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/propellane/outputs/execution_jobs/job_f20c4261abf24f09b8d850c0268c4809/input.com` — successful execution artifact; SHA-256 `deb6db2c3e44dbccaf90bf32f14ee08820882e7fc4b563ab70526d65d63de6e7`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/propellane/outputs/execution_jobs/job_f20c4261abf24f09b8d850c0268c4809/request.json` — successful execution artifact; SHA-256 `2a4b0a91a0c662f0e302d2812b44d00caa0e68781f593254c413338c87ef5329`
- `docs/verification/group_3/paper_d91572979a89303a/native_workspace/propellane/outputs/execution_jobs/job_f20c4261abf24f09b8d850c0268c4809/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/1a/status.json` — label=group_3 paper_d91572979a89303a 1a; submitted_at=2026-08-29T07:51:06.841290+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/1a_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/stdout.log`
2. `artifacts/gaussian/propellane/status.json` — label=group_3 paper_d91572979a89303a propellane; submitted_at=2026-08-29T07:51:07.624248+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/propellane_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/stdout.log`
3. `artifacts/gaussian/txt/status.json` — label=group_3 paper_d91572979a89303a txt; submitted_at=2026-08-29T07:51:08.396665+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/txt_optimized.xyz`
4. `artifacts/gaussian/3a_rerun_retry/status.json` — label=group_3 paper_d91572979a89303a 3a_rerun_retry; submitted_at=2026-08-29T16:47:31.076555+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/def2SVP Opt Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/3a_rerun_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/3a_rerun_retry/stdout.log`
5. `artifacts/gaussian/INT1A_rerun_retry/status.json` — label=group_3 paper_d91572979a89303a INT1A_rerun_retry; submitted_at=2026-08-29T16:47:32.377257+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/def2SVP Opt Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/INT1A_rerun_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/stdout.log`
6. `artifacts/gaussian/INT2A_rerun_retry/status.json` — label=group_3 paper_d91572979a89303a INT2A_rerun_retry; submitted_at=2026-08-29T16:47:33.265740+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/def2SVP Opt Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/INT2A_rerun_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/stdout.log`
7. `artifacts/gaussian/TS1A_rerun_retry/status.json` — label=group_3 paper_d91572979a89303a TS1A_rerun_retry; submitted_at=2026-08-29T16:47:34.205759+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/def2SVP Opt=(TS,CalcFC,NoEigenTest,MaxStep=5) Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/TS1A_rerun_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/stdout.log`
8. `artifacts/gaussian/TS3A_TXT_rerun_retry/status.json` — label=group_3 paper_d91572979a89303a TS3A_TXT_rerun_retry; submitted_at=2026-08-29T16:47:35.076943+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/def2SVP Opt=(TS,CalcFC,NoEigenTest,MaxStep=5) Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/TS3A_TXT_rerun_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry/stdout.log`
9. `artifacts/gaussian/TS3B_rerun_retry/status.json` — label=group_3 paper_d91572979a89303a TS3B_rerun_retry; submitted_at=2026-08-29T16:47:35.927588+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/def2SVP Opt=(TS,CalcFC,NoEigenTest,MaxStep=5) Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/TS3B_rerun_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/stdout.log`
10. `artifacts/gaussian/TS4A_TXT_rerun_retry/status.json` — label=group_3 paper_d91572979a89303a TS4A_TXT_rerun_retry; submitted_at=2026-08-29T16:47:36.749484+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/def2SVP Opt=(TS,CalcFC,NoEigenTest,MaxStep=5) Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/TS4A_TXT_rerun_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry/stdout.log`
11. `artifacts/gaussian/TS3B_rerun_retry_irc/status.json` — label=group_3 paper_d91572979a89303a TS3B_rerun_retry_irc; submitted_at=2026-08-30T06:10:53.550444+00:00; software=gaussian; intent=single_point; route=#p p wB97XD/def2SVP  Int=UltraFine NoSymm SCF=XQC IRC=(CalcFC,MaxPoints=50,StepSize=10) NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/TS3B_rerun_retry_irc_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry_irc/stdout.log`
12. `artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/status.json` — label=group_3 paper_d91572979a89303a TS3A_TXT_rerun_retry_unbounded_recovery96g; submitted_at=2026-08-31T09:51:25.066065+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/def2SVP Opt=(TS,CalcFC,NoEigenTest,MaxStep=5) Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/TS3A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/stdout.log`
13. `artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/status.json` — label=group_3 paper_d91572979a89303a TS4A_TXT_rerun_retry_unbounded_recovery96g; submitted_at=2026-08-31T10:19:17.579505+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/def2SVP Opt=(TS,CalcFC,NoEigenTest,MaxStep=5) Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/TS4A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/stdout.log`
14. `artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/status.json` — label=group_3 paper_d91572979a89303a TS1A_rerun_retry_irc3_unbounded16g; submitted_at=2026-09-01T01:38:12.452271+00:00; software=gaussian; intent=reaction_path; route=#p wB97XD/def2SVP Int=UltraFine NoSymm SCF=(XQC,MaxCycle=2048) IRC=(CalcFC,MaxPoints=100,StepSize=2,MaxCycles=100); command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/TS1A_rerun_retry_irc3_unbounded16g_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc3_unbounded16g/stdout.log`
15. `artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/status.json` — label=group_3 paper_d91572979a89303a TS1A_rerun_retry_irc2_unbounded16g; submitted_at=2026-09-03T03:09:19.711816+00:00; software=gaussian; intent=reaction_path; route=#p wB97XD/def2SVP  Int=UltraFine NoSymm SCF=XQC IRC=(CalcFC,MaxPoints=100,StepSize=5,MaxCycles=50) NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/TS1A_rerun_retry_irc2_unbounded16g_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/collection.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/stderr.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/stdout.log`
16. `artifacts/gaussian/1a_author_route_strict_v2/status.json` — label=None
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/1a_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/1a_author_route_strict_v2.fchk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/1a_author_route_strict_v2_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a_author_route_strict_v2/stdout.log`
17. `artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/status.json` — label=hpc-job-430adc5a-bbdf-48cf-8cea-d986e240de1f
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc.fchk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/stdout.log`
18. `artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/status.json` — label=hpc-job-bddd8148-d707-4f48-b454-5c06ea3a6952
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc.fchk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_optimized.xyz`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/formchk.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/parsed_observables.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/stdout.log`
19. `provenance/qzcli_hpc/1a_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/1a_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/1a_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/1a_author_route_strict_v2/1/sha256sums.txt`
20. `provenance/qzcli_hpc/2a_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/2a_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/2a_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/2a_author_route_strict_v2/1/sha256sums.txt`
21. `provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/INT2A_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT2A_author_route_strict_v2/1/sha256sums.txt`
22. `provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/INT3A_TXT_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/INT3A_TXT_author_route_strict_v2/1/sha256sums.txt`
23. `provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/TS1A_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS1A_author_route_strict_v2/1/sha256sums.txt`
24. `provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/TS3A_TXT_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_author_route_strict_v2/1/sha256sums.txt`
25. `provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/status.json` — label=provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/sha256sums.txt`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/source_input.com`
26. `provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/TS3B_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS3B_author_route_strict_v2/1/sha256sums.txt`
27. `provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/TS4A_TXT_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_author_route_strict_v2/1/sha256sums.txt`
28. `provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/status.json` — label=provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/sha256sums.txt`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc_hpc20_migrated/1/source_input.com`
29. `provenance/qzcli_hpc/TXT_author_route_strict_v2/1/status.json` — label=provenance/qzcli_hpc/TXT_author_route_strict_v2/1/status.json
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/TXT_author_route_strict_v2.chk`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/input.com`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_d91572979a89303a/provenance/qzcli_hpc/TXT_author_route_strict_v2/1/sha256sums.txt`

## Evaluator alignment

- Key-point IDs: `kp-ar-1, kp-ar-2, kp-ar-3, kp-ar-4`
- Conclusion IDs: `c-ar-1, c-ar-2`
- Scoring-rule IDs: `r-ar-1, r-ar-2, r-ar-3, r-ar-4, r-ar-final, r-ar-conclusion`
- Bound result-field status: **BRANCH_INAPPLICABLE_FIELDS_ONLY**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `$.hypotheses`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r-ar-1` → reference `kp-ar-1`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r-ar-2` → reference `kp-ar-2`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r-ar-3` → reference `kp-ar-3`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r-ar-4` → reference `c-ar-2`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r-ar-final` → reference `kp-ar-4`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r-ar-conclusion` → reference `c-ar-1`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].id` = `"1a"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].state_type` = `"minimum"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].geometry_provenance` = `"artifacts/gaussian/1a/1a_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].frequency_validation` = `"normal termination; imaginary_frequency_count=0"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].connectivity_validation` = `"minimum frequency check"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[0].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].id` = `"txt"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].state_type` = `"minimum"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].geometry_provenance` = `"artifacts/gaussian/txt/txt_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].frequency_validation` = `"normal termination; imaginary_frequency_count=0"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].connectivity_validation` = `"minimum frequency check"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[1].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].id` = `"propellane"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].state_type` = `"minimum"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].geometry_provenance` = `"artifacts/gaussian/propellane/propellane_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].frequency_validation` = `"normal termination; imaginary_frequency_count=0"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].connectivity_validation` = `"minimum frequency check"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[2].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].id` = `"INT1A_rerun_retry"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].state_type` = `"minimum"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].geometry_provenance` = `"artifacts/gaussian/INT1A_rerun_retry/INT1A_rerun_retry_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].frequency_validation` = `"normal termination; imaginary_frequency_count=0"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].connectivity_validation` = `"minimum frequency check"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[3].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].id` = `"INT2A_rerun_retry"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].state_type` = `"minimum"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].geometry_provenance` = `"artifacts/gaussian/INT2A_rerun_retry/INT2A_rerun_retry_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].frequency_validation` = `"normal termination; imaginary_frequency_count=0"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].connectivity_validation` = `"minimum frequency check"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[4].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].id` = `"TS1A_rerun_retry"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].state_type` = `"transition_state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].geometry_provenance` = `"artifacts/gaussian/TS1A_rerun_retry/TS1A_rerun_retry_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].frequency_validation` = `"normal termination; imaginary_frequency_count=1"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].connectivity_validation` = `"artifacts/gaussian/TS1A_rerun_retry_irc/parsed_observables.json"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[5].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].id` = `"TS3A_TXT_rerun_retry_unbounded_recovery96g"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].state_type` = `"transition_state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].geometry_provenance` = `"artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/TS3A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].frequency_validation` = `"normal termination; imaginary_frequency_count=1"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].connectivity_validation` = `"artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g_irc/parsed_observables.json"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[6].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].id` = `"TS3B_rerun_retry"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].state_type` = `"transition_state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].geometry_provenance` = `"artifacts/gaussian/TS3B_rerun_retry/TS3B_rerun_retry_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].frequency_validation` = `"normal termination; imaginary_frequency_count=1"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].connectivity_validation` = `"artifacts/gaussian/TS3B_rerun_retry_irc/parsed_observables.json"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[7].status` = `"validated"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].id` = `"TS4A_TXT_rerun_retry_unbounded_recovery96g"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].state_type` = `"transition_state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].connectivity` = `"TXT-catalysed thioaromatization model state"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].charge_multiplicity` = `"as supplied SI model"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].geometry_provenance` = `"artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/TS4A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].frequency_validation` = `"normal termination; imaginary_frequency_count=1"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].connectivity_validation` = `"artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g_irc/parsed_observables.json"`
- rule `r-ar-1` / reference `kp-ar-1` / field `$.candidates` / result path `$.candidates[8].status` = `"validated"`
- rule `r-ar-2` / reference `kp-ar-2` / field `$.coverage` / result path `$.coverage` = `"All supplied/restored minima and four labelled TS candidates with IRC checks."`
- rule `r-ar-3` / reference `kp-ar-3` / field `$.conclusion` / result path `$.conclusion` = `"Under the matched wB97XD/def2-TZVP IEFPCM(toluene) route and SI half-entropy convention, TXT lowers aromatization from 44.0738 to 20.0682 kcal/mol. Within the TXT-assisted cycle, deamination is the largest barrier (32.7378 kcal/mol) and ..."`
- rule `r-ar-4` / reference `c-ar-2` / field `$.limitations` / result path `$.limitations` = `"One conformer per labelled state; the profile is limited to the validated SI-derived candidate network and does not establish a global conformational search or experimental kinetics. Barrier references are state-specific and use the SI h..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: paper route changed
- Files changed in that review: `agent_input/task.md, package_manifest.json, paper_route.md`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained identities and environmental boundary for 1a, propellane and TXT.

Public input files and hashes:

- `agent_input/data/inputs/README.md` — SHA-256 `7a1eca7cd0b796c039e94719a571a6bc14a8b6596a8313a7bb70b37b00a23144`; size=247 bytes; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/reactants.json` — SHA-256 `729eea37dd32e8fc09348e987f76e21c3acac40bb3d273c631c7869ed62b281d`; size=533 bytes; explicit_boundary_fields={"$.environment.solvent": "toluene", "$.environment.temperature_K": 298.15, "$.molecules[0].charge": 0, "$.molecules[0].multiplicity": 1, "$.molecules[0].smiles": "Brc1ccc(NSc2ccccc2)cc1", "$.molecules[1].charge": 0, "$.molecules[1].multiplicity": 1, "$.molecules[1].smiles": "C1C2C3C1C23", "$.molecules[2].charge": 0, "$.molecules[2].multiplicity": 1, "$.molecules[2].smiles": "O=C1c2ccccc2Sc2ccccc21"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_d91572979a89303a/verification_report.md` — verification record; SHA-256 `2a71e4fc7b99e57e9aa8e7d033e8d22d982509e951f3ecfbac8d874cd7711842`
- `docs/verification/group_3/paper_d91572979a89303a/report/results.json` — verification record; SHA-256 `610b0576a9be0ca79746232331c2eaa6a65d91c27aac6c9d9945ecef770dca04`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/1a/1a_optimized.xyz` — referenced successful evidence; SHA-256 `974348d8e408a54a8fb71a1daf0cd5d1f7952a6f5ee422f717c27aae5d8087ea`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT1A_rerun_retry/INT1A_rerun_retry_optimized.xyz` — referenced successful evidence; SHA-256 `d32fd0cd99674f0f6ddef2cb75737c08d0c4c26b6561e3fd8af86adc0baa4fe5`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/INT2A_rerun_retry/INT2A_rerun_retry_optimized.xyz` — referenced successful evidence; SHA-256 `8698280b31409f75ed6074fd1d8ec5b1746f10aff0431473a0120bb264befae0`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry/TS1A_rerun_retry_optimized.xyz` — referenced successful evidence; SHA-256 `16cdf2e05fd5750cf868eb3405ce7cfb78ac588e6f9b258a4f658c0a493480b8`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3A_TXT_rerun_retry_unbounded_recovery96g/TS3A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz` — referenced successful evidence; SHA-256 `ff67d56cd4eb04074a5d4e2668b92d15bddd32bb9a255f49e1c3f3cd84cede75`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS3B_rerun_retry/TS3B_rerun_retry_optimized.xyz` — referenced successful evidence; SHA-256 `a4721482a34b8400fa4e91b637affba761c0a88dc16fbb56099f654942e30ac9`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS4A_TXT_rerun_retry_unbounded_recovery96g/TS4A_TXT_rerun_retry_unbounded_recovery96g_optimized.xyz` — referenced successful evidence; SHA-256 `2ee33a6ceee077298897fc82d4de0fa1281a19f2a68241b09e9276607ed7a30c`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/propellane/propellane_optimized.xyz` — referenced successful evidence; SHA-256 `7c524347f31e2cc2f311e1f7fdcc25b3905482248865afbf6189402dd3b95fcc`
- `docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/txt/txt_optimized.xyz` — referenced successful evidence; SHA-256 `8cc9fa4761218d90ba1dc35ec9fb864f87c2f03e6094bc91978817c0f0d53681`
- `docs/verification/group_3/paper_d91572979a89303a/provenance/strict_v2_observables.json` — referenced successful evidence; SHA-256 `2b0299e87a9179e889b66503e42b5dac5b9934bcc4ec8c5e1fa8439e03e1688a`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
