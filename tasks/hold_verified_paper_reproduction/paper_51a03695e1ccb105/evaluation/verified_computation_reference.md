# Verified computation reference — paper_51a03695e1ccb105 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Current evidence status — NOT_RELEASE_READY (2026-09-18)

Existing four endpoint minima, the one-imaginary-mode TS (−1650.1799 cm⁻¹), ΔG‡≈13.2521 and ΔG_rxn≈−29.5339 kcal/mol remain useful real results. The gap is the specified connection to separated iminotriazole-anion/nitrosotriazole and azo/OH− basins, not the historical use of an SI TS.

In `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/stdout.log`, the two 100-point endpoints give (forward/reverse, Å): N8–N9 1.460321/1.415034; N9–O18 1.374330/1.480448; N8–H17 1.023161/2.006356; O18–H17 2.125623/0.982053. This is evidence of the proton-transfer portion, not a demonstrated complete coupling/separation connection. Normal termination or a point limit alone does not decide chemical connectivity. Independent optimized products do not demonstrate that this TS reaches them.

No matching completed endpoint-connection continuation was found in the inspected stored branches. Existing evidence must be supplemented by mapped downstream relaxation/connection evidence before this full target can be certified. No new calculation or target narrowing was performed. Historical PASS/connection claims below are superseded only in that respect; energies are not discarded or invented.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `validated` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **NOT_VERIFIED_FOR_FULL_CURRENT_TARGET**
- Applicability note: See the current evidence correction above; historical execution success is not full target validation.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 81 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 `report/results.json`、`artifacts/gaussian/` 和 `provenance/`。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Photocatalytic synthesis of 3,3′-azo-1,2,4-triazole compounds
- DOI: `10.1016/j.molstruc.2025.144415`
- Task package: `tasks/final_verified_paper_reproduction/paper_51a03695e1ccb105`
- Verification group: `docs/verification/group_3/paper_51a03695e1ccb105`
- Paper documents: `papers/paper_51a03695e1ccb105`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "activation_free_energy_kcal_mol": 13.252133500398472,
  "conclusion": "Atom-balanced base-assisted coupling is computationally supported within the stated model: the SI TS-2 branch has one relevant imaginary mode and an IRC connection, with ΔG‡=13.252 kcal/mol and ΔG_rxn=-29.534 kcal/mol for azo + OH− formation.",
  "hypotheses": [
    {
      "candidate_tests": [
        "The retained TS-2 candidate has one coupled N-N bond-forming/O-H-transfer imaginary mode.",
        "A normally terminated IRC connects the TS to the validated reactant and atom-balanced product basins."
      ],
      "description": "The supplied iminotriazole anion and nitrosotriazole undergo an elementary N-N/O-H coupled coupling to the atom-balanced azo-plus-hydroxide endpoint.",
      "evidence": [
        "states.candidates[0].imaginary_frequency_details",
        "states.candidates[0].connection_evidence",
        "activation_free_energy_kcal_mol",
        "reaction_free_energy_kcal_mol"
      ],
      "hypothesis_id": "base_assisted_coupling",
      "outcome": "supported",
      "selection_reason": "Selected because it is the atom-balanced coupling hypothesis directly tested by the retained TS-2 frequency and IRC evidence."
    },
    {
      "candidate_tests": [
        "Unassisted and alternative base-TS attempts were retained in the provenance job inventory and did not yield a validated connection; the retained TS-2 branch was selected only after frequency/IRC validation."
      ],
      "description": "An unassisted or chemically distinct transition-state family provides the validated coupling connection instead of the base-assisted branch.",
      "evidence": [
        "provenance/job_inventory.json",
        "states.candidates",
        "limitation"
      ],
      "hypothesis_id": "unassisted_or_alternative_ts",
      "outcome": "not_supported_by_retained_evidence",
      "selection_reason": "Retained as a competing candidate family because unassisted and alternative base-TS attempts were actually recorded in the provenance inventory."
    }
  ],
  "limitation": "One SI TS-2 starting candidate and one conformer per endpoint; the composite thermal/electronic free-energy convention and continuum solvation are model dependent. Historical unbalanced TS attempts remain archived and are not used.",
  "method": {
    "energy_method": "M062X/def2-TZVP single points with SMD methanol; thermal corrections from matched B3LYP-D3/CPCM calculations",
    "free_energy_convention": "Separated species, 298.15 K, 1 atm harmonic thermal G; composite G = B3LYP-D3/CPCM thermal G + M062X/SMD electronic correction; 1 Eh=627.509474 kcal/mol",
    "geometry_method": "Gaussian 16 C.01 B3LYP-D3BJ/6-31G(d), Opt/Freq, CPCM methanol",
    "solvent": "CPCM methanol for geometry/thermal terms; SMD methanol for M062X electronic correction"
  },
  "reaction_free_energy_kcal_mol": -29.5339200778861,
  "states": {
    "candidates": [
      {
        "candidate_id": "azo_TS2_si_cpcm_ts",
        "connection_evidence": "normally terminated IRC: azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g; endpoint inspection archived in artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/",
        "geometry_provenance": "SI Table S17 / Fig. S8 TS-2 Cartesian candidate (azotriazole_ts2_si.xyz), independently reoptimized",
        "imaginary_frequency_details": {
          "count": 1,
          "required_mode": "N-N bond formation coupled to O-H transfer",
          "values_cm_minus_1": "<nested value omitted>"
        },
        "imaginary_frequency_diagnostic": "count=1; values_cm^-1=[-1650.1799]; required mode=N-N bond formation coupled to O-H transfer",
        "validation_status": "validated"
      }
    ],
    "coproduct": {
      "charge": -1,
      "frequency_diagnostic": "validated minimum; zero imaginary frequencies; hydroxide_cpcm_opt_freq",
      "identity": "hydroxide anion (OH−; atom/charge-balanced coproduct)",
      "multiplicity": 1
    },
    "product": {
      "charge": 0,
      "frequency_diagnostic": "validated minimum; zero imaginary frequencies; azo_si_s12_cpcm_opt_freq",
      "identity": "neutral 3,3′-azo-1,2,4-triazole (SI Tables S12-S13)",
      "multiplicity": 1
    },
    "reactants": [
      {
        "charge": -1,
        "frequency_diagnostic": "validated minimum; zero imaginary frequencies; imino_anion_si_cpcm_opt_freq",
        "identity": "iminotriazole anion (SI Table S8/public XYZ; atom-balanced reactant)",
        "multiplicity": 1
      },
      {
        "charge": 0,
        "frequency_diagnostic": "validated minimum; zero imaginary frequencies; nitroso_si_cpcm_opt_freq",
        "identity": "nitrosotriazole (SI Tables S12-S13/public XYZ)",
        "multiplicity": 1
      }
    ]
  },
  "status": "validated"
}
```

## Re-audit source-evidence drift

- Classification: **SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW**
- Previous `results.json` SHA-256: `efe8e8361a97852163b0adcff7998418037305c49220090129d7601aef8fd10a`
- Current `results.json` SHA-256: `e295ac1f3e4133458d4a972d358b53c53097858255453d51dfb9f30227b96175`
- Changed top-level result fields: `hypotheses`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["hypotheses"], "classification": "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW", "current_sha256": "e295ac1f3e4133458d4a972d358b53c53097858255453d51dfb9f30227b96175", "detected": true, "previous_sha256": "efe8e8361a97852163b0adcff7998418037305c49220090129d7601aef8fd10a"} -->

Paper/SI document hashes:

- `papers/paper_51a03695e1ccb105/documents/main.pdf` — SHA-256 `ff0c3a07a7654fe58c89fda8609843dad3e47e187f11d23c9e7f3d40033f23ae` (declared_match=True)
- `papers/paper_51a03695e1ccb105/documents/supplementary_001.pdf` — SHA-256 `d64cd6ed75e24bee3ac926642e80296c78df2f9a59bf15b28bc1b93108383919` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **150**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/status.json` — successful status record; SHA-256 `a8dd4a29adeb78f3114cd3bf1a1bd693aa0fd25f428e25bcfc40f8e8e2150119`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/azo_TS2_si_cpcm_ts_optimized.xyz` — successful execution artifact; SHA-256 `377dcb570ae3b1b03021046ba929f06fba82ac20a5c9f675f4705505fc7de307`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/collection.json` — successful execution artifact; SHA-256 `14451a75a6bc21724c37485813aeaabd8b0868923c0190dd02eebe6f39315f76`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/formchk.log` — successful execution artifact; SHA-256 `149786eed662d8d1c4b1f864b53703d733b27c0c9f9b4690c6001577b51a4426`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/input.com` — successful execution artifact; SHA-256 `82896bceb7f9a3d59ec60a02eba6e035a8ab2829552cf9a30d2e2b6e31ec7228`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/status.json` — successful status record; SHA-256 `f142a152f72006fe3cb8086670ea183690eacd5ebc2a9395a2d9a68148742318`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g_optimized.xyz` — successful execution artifact; SHA-256 `da5ecac109def21595b853219a9d64a226440baa07ab5787a38970b9425c5766`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/collection.json` — successful execution artifact; SHA-256 `3eb5fc997366cc7f221af11cb45e9885cd070360ad16f6b5505017fcd8a326ad`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/formchk.log` — successful execution artifact; SHA-256 `fd30bef3ee1ef5f135cdc33b4cdeb61205f13a5a6b933196593e4f5438e647c9`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/input.com` — successful execution artifact; SHA-256 `bbcefced3e2b079947fbed13d463e03dd70464b3743387afabda6bd3b15c657d`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/status.json` — successful status record; SHA-256 `9175225cb56c8f333e4123c800de87bae1b5f32c330ef2cbc27ee09bfdd75ff2`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/azo_TS2_si_cpcm_ts_m062x_smd_sp_optimized.xyz` — successful execution artifact; SHA-256 `48ab2cfabe1045729b54d7b32a7965eb323a9612ad37e3b717f5f3fff58b8435`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/collection.json` — successful execution artifact; SHA-256 `a537e794e2a7fb27db49da958bfb041f4da91a09dc0f4c0ca639f97e9b2eef79`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/formchk.log` — successful execution artifact; SHA-256 `e61b8fe918f1366595eca36ad2289623907f56357a2f1c9e98006ed753898c03`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/input.com` — successful execution artifact; SHA-256 `1434d76d4f78cf11cf2711a6f89f6a2b974bee2589103ba5c3f36e41125ec5aa`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/status.json` — successful status record; SHA-256 `269cacd0e8511df4305c2d37b94ee98986a002632e172539c4f0f94723077876`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/azo_product_b3lyp_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `f39381a224825e981adf47ac575fbda7558de8433ba0f8170f650c43f7bb9188`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/collection.json` — successful execution artifact; SHA-256 `0837b0a55969f5010b084faab2596ef9779ff786f25990eb3a60a066b8bdca6e`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/formchk.log` — successful execution artifact; SHA-256 `bd2256a075c08eabd003a2dfb7639045a3720a8d1107a8ec70392c7b402fdcb6`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/input.com` — successful execution artifact; SHA-256 `cfc650c60e0bb6bed1da5b767c5dedc9f45805eee0f5b651b032ce3f3fdc6806`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/status.json` — successful status record; SHA-256 `f1f8ca3254177133c601c3a0d91ac03db7a1e0f6ab607b803e27187a9a61087d`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/azo_product_rb3lyp_retry_optimized.xyz` — successful execution artifact; SHA-256 `6bd142ed4a2bfe1c57acac181aeb173f06f1aaa8d8e07b6f2c294a84047a1352`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/collection.json` — successful execution artifact; SHA-256 `743a63d8f814364eef4ebb56ce90d946abb54016d162f10fec4a8d83b33c526c`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/formchk.log` — successful execution artifact; SHA-256 `846bbcaf876cee2773fe8d37f2cf6a86634f7d36b9690a327e0d59ee020d7e08`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/input.com` — successful execution artifact; SHA-256 `b93479babcc1c05417084dc852e35b4e95219a92862b0791d69f6180bdc40701`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/status.json` — successful status record; SHA-256 `27d1110fb821218724dd5bdcd07918c7d41a77aeacac52cdd6f6f23c530b3e08`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/azo_si_s12_cpcm_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `325af2cb5c71caffdfda2c1aa794a71baa38dda76c3d88b007db3d2298abb012`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/collection.json` — successful execution artifact; SHA-256 `71c0889a01569deea68683294d60d7f3be36a97cdfef21aec1d0a14fa3bb31a4`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/formchk.log` — successful execution artifact; SHA-256 `6393dbda437d2c45eab54c6b62bdfada9c0fc1fd0ac12ebfff2c8cd5a3c272f3`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/input.com` — successful execution artifact; SHA-256 `5d204a91a499fa98723be449f6b69d679fafc4eddbf93f893dce6b0a0e0643e8`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/status.json` — successful status record; SHA-256 `e03f8c419b105b2dad3449afddd89f080ace2089a9e06f9ea6f928e3efe8da9d`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/azo_si_s12_cpcm_opt_freq_m062x_smd_sp_optimized.xyz` — successful execution artifact; SHA-256 `92838b5015a883aa6c86bb0288ef0a530c7261504a870f0e08148f68aaca05a0`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/collection.json` — successful execution artifact; SHA-256 `af2904a699f85d0490df93bf0c59ed08de64de31b42d541b7bceeaa77ae656a3`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/formchk.log` — successful execution artifact; SHA-256 `01224745dcd2ff26e2daa4de8df513a40bca59fdfcca3746abc8c6d096d6d4cb`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/input.com` — successful execution artifact; SHA-256 `6845911a77ecb7f5232166a41fb867ab9a81c870c9b1b3d48b94999cc2f909b6`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/status.json` — successful status record; SHA-256 `e78f18d6f7ccba2f2b96a85b523b5fc633ea3650089beb1b387716a978f0e380`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/collection.json` — successful execution artifact; SHA-256 `2274b3e14f4e504d951fb61e11e934bb2dad62c13b824ca9cc959d1e4883b781`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/formchk.log` — successful execution artifact; SHA-256 `88d6c5957301bc0c81af554f5e71a001d8f8233e7f73339f4b657116477c8524`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/hydroxide_cpcm_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `ff5ee3ae9ee47e69706d778349533c16f596e4842e31dfaaf0e790ee0f9eaad6`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/input.com` — successful execution artifact; SHA-256 `63082cad51091f75567d7a8c73f04afff79aa72d46618c9c35aac74c17d71947`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/status.json` — successful status record; SHA-256 `b51e90db7c27a377cd74ad34d71e45e48bef05ae62902564303fbdffcaf2771f`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/collection.json` — successful execution artifact; SHA-256 `26b81835080434b90edd104a75f5d9353c9c7d674953ae2b9dd81b1d00ef614e`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/formchk.log` — successful execution artifact; SHA-256 `20fbd445fda3e7a6063dec873b04e0ea866989b07812e09b55c9ccfb995df2a9`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/hydroxide_cpcm_opt_freq_m062x_smd_sp_optimized.xyz` — successful execution artifact; SHA-256 `b4977dd26c63abf397a98135e1957078006104730a7d932818bd81ea0ad6a830`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/input.com` — successful execution artifact; SHA-256 `d0531ec6800ab97b2a76a8e57cd734a8b9878c9217e9716eef90e785c4cdcf44`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/status.json` — successful status record; SHA-256 `32e07c7d8dfb5be6ecc33eb97dd0d406be43c9f3652705818f18eca651e015bb`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/collection.json` — successful execution artifact; SHA-256 `08345e56b9e5eba90e0024e529022d3acf333f73261c82e634d3e7469d656b4b`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/formchk.log` — successful execution artifact; SHA-256 `13566361eaf65ebbb2ba0ce023dfb3297844adbc15366f44d6d019e6826b3bce`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/imino_anion_si_cpcm_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `7f61464973d8d0340852f2fb2b327ae74523f90a6f8de83b7cb9d371d060e37d`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/input.com` — successful execution artifact; SHA-256 `99d230e12ff441235e4ba09ccbbb8ea88f7b8c5a07442b4fa5aed92f202242e6`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/status.json` — successful status record; SHA-256 `8dde167da3e8109a137d5cbf2af61c9cb3afc110cd649b269ed6fdcdf0a9e9b5`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/collection.json` — successful execution artifact; SHA-256 `659fd5a8227584a716a528012793c3cb7a07e26b85935a6c60cfceb996291e00`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/formchk.log` — successful execution artifact; SHA-256 `d8e48fa1645f2e2d052b7c8ccdc2fd72f8c72451640bcaca3a1a2fe21b3a3ef5`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/imino_anion_si_cpcm_opt_freq_m062x_smd_sp_optimized.xyz` — successful execution artifact; SHA-256 `f51e85ecfef88139c20c7cce574bf82e4eb742e2a12efe53cb9fb8187c3cc21a`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/input.com` — successful execution artifact; SHA-256 `e6a6be1ef1678bcd6fa30a7a3894609a0d6d101446e5ef0c19dee03b17bd4c1b`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/status.json` — successful status record; SHA-256 `0eb8aaa3ac4d0823e6853afde728cfe8bf3bd1f911dc2c3c14891a58e5bda495`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/collection.json` — successful execution artifact; SHA-256 `e9e34d2ad1414a8ebebea1d8c9aafaa95077f47e72184cc5c061161e96ccf2d0`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/formchk.log` — successful execution artifact; SHA-256 `4f7984358f07512ff55c3692b44eea5eee47053ef22fc3bc5777368f9b924a5d`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/iminotriazole_optimized.xyz` — successful execution artifact; SHA-256 `519cd998a5712a87128226c016cb4bd394abf3057a482051243cc53f5c4feee7`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/input.com` — successful execution artifact; SHA-256 `c9c4947c8b84cb666aa696e54b0b51c805f5df5007a571e5da22a9ee4ec2a47c`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/status.json` — successful status record; SHA-256 `64c3801d2596d8e08c187061aa6635dca9f89f394aac996e24e59e5f02e75b3e`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/collection.json` — successful execution artifact; SHA-256 `db92bfc5aa943b24e49c03526ca521db1697a1f131edc0a6ef708d132c1747a1`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/formchk.log` — successful execution artifact; SHA-256 `7c47d6fb39fab0551a366e2483b1bfdbc3f2b3bc25ee06de86a2c3bec2723750`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/input.com` — successful execution artifact; SHA-256 `5667ed163417e470d3645e34165179ab8d4ea186d0a79e3aae57629cd39139f8`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/nitroso_si_cpcm_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `df7e6a57b2f33431a5d10f67471a675c93a77a825201a33c186f5a9f55fe8f45`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/status.json` — successful status record; SHA-256 `06dd6ecba99d387a490558d4c734bf0e274401e410119ca5670ddf63586915b0`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/collection.json` — successful execution artifact; SHA-256 `c3c1712f7a247a4c3495028e898092c66e34f622dcf8b137cfa84d93aa6d37b6`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/formchk.log` — successful execution artifact; SHA-256 `d641b6560dcef2090a5000afea49395936b78f2a2856b1b7b6f95c494f0ca504`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/input.com` — successful execution artifact; SHA-256 `a55d8a096ae26d3d13961f09e8e77cb402c22de5a4adeadb2a315ed1b9eefc8e`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/nitroso_si_cpcm_opt_freq_m062x_smd_sp_optimized.xyz` — successful execution artifact; SHA-256 `61e4de4c51931294f0121953d916624701b3b7fba33a9cea70c5785f671384a3`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/status.json` — successful status record; SHA-256 `f151f3e80bf6e95ddd7b9bdff0d6b6ec568d83780d798618ab8035f54d676f1c`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/collection.json` — successful execution artifact; SHA-256 `1a5c3be321806292750251ce09678e34feb146421fc6f820ef8f6342989dc1d8`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/formchk.log` — successful execution artifact; SHA-256 `9e8b5ca2f1b848a0a8445b6b4c89c81a7692fb867f6dec0362c3244dfd7060b1`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/input.com` — successful execution artifact; SHA-256 `6f4f62ee034f1f24e73dca363ebc60b9bf074ab9d5e1b9b254efb9815c179f85`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/nitrosotriazole_optimized.xyz` — successful execution artifact; SHA-256 `fc20ed9e5d9b2489cea09df4807360c6aadd869d341056b16da66f5e59f20654`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts/outputs/execution_jobs/job_1f52574277fa4a3ab3b5800cc06eef1b/status.json` — successful status record; SHA-256 `a8dd4a29adeb78f3114cd3bf1a1bd693aa0fd25f428e25bcfc40f8e8e2150119`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts/outputs/execution_jobs/job_1f52574277fa4a3ab3b5800cc06eef1b/collection.json` — successful execution artifact; SHA-256 `14451a75a6bc21724c37485813aeaabd8b0868923c0190dd02eebe6f39315f76`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts/outputs/execution_jobs/job_1f52574277fa4a3ab3b5800cc06eef1b/input.com` — successful execution artifact; SHA-256 `82896bceb7f9a3d59ec60a02eba6e035a8ab2829552cf9a30d2e2b6e31ec7228`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts/outputs/execution_jobs/job_1f52574277fa4a3ab3b5800cc06eef1b/request.json` — successful execution artifact; SHA-256 `11e4b7f188bf81d0800b813ba99f9b54ae8e9db02af65438bcf1a3c82a25d8a2`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts/outputs/execution_jobs/job_1f52574277fa4a3ab3b5800cc06eef1b/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/outputs/execution_jobs/job_c0ccb579d5e94e1a9f1242f2eda09491/status.json` — successful status record; SHA-256 `f142a152f72006fe3cb8086670ea183690eacd5ebc2a9395a2d9a68148742318`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/outputs/execution_jobs/job_c0ccb579d5e94e1a9f1242f2eda09491/collection.json` — successful execution artifact; SHA-256 `3eb5fc997366cc7f221af11cb45e9885cd070360ad16f6b5505017fcd8a326ad`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/outputs/execution_jobs/job_c0ccb579d5e94e1a9f1242f2eda09491/input.com` — successful execution artifact; SHA-256 `bbcefced3e2b079947fbed13d463e03dd70464b3743387afabda6bd3b15c657d`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/outputs/execution_jobs/job_c0ccb579d5e94e1a9f1242f2eda09491/request.json` — successful execution artifact; SHA-256 `c221b455155b49a0d3ef125e1c0c0d8316c9af7850bc7975b31834980c54167a`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/outputs/execution_jobs/job_c0ccb579d5e94e1a9f1242f2eda09491/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_m062x_smd_sp/outputs/execution_jobs/job_84dc946135214e08ac16e88ed5ee7ce8/status.json` — successful status record; SHA-256 `9175225cb56c8f333e4123c800de87bae1b5f32c330ef2cbc27ee09bfdd75ff2`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_m062x_smd_sp/outputs/execution_jobs/job_84dc946135214e08ac16e88ed5ee7ce8/collection.json` — successful execution artifact; SHA-256 `a537e794e2a7fb27db49da958bfb041f4da91a09dc0f4c0ca639f97e9b2eef79`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_m062x_smd_sp/outputs/execution_jobs/job_84dc946135214e08ac16e88ed5ee7ce8/input.com` — successful execution artifact; SHA-256 `1434d76d4f78cf11cf2711a6f89f6a2b974bee2589103ba5c3f36e41125ec5aa`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_m062x_smd_sp/outputs/execution_jobs/job_84dc946135214e08ac16e88ed5ee7ce8/request.json` — successful execution artifact; SHA-256 `97a8281247b67df154ea9864a88c42b330009eea9b256d62e8aeab5ea8ded031`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_TS2_si_cpcm_ts_m062x_smd_sp/outputs/execution_jobs/job_84dc946135214e08ac16e88ed5ee7ce8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_b3lyp_opt_freq/outputs/execution_jobs/job_6f04b86b750346efa0df81f86255d6b5/status.json` — successful status record; SHA-256 `269cacd0e8511df4305c2d37b94ee98986a002632e172539c4f0f94723077876`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_b3lyp_opt_freq/outputs/execution_jobs/job_6f04b86b750346efa0df81f86255d6b5/collection.json` — successful execution artifact; SHA-256 `0837b0a55969f5010b084faab2596ef9779ff786f25990eb3a60a066b8bdca6e`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_b3lyp_opt_freq/outputs/execution_jobs/job_6f04b86b750346efa0df81f86255d6b5/input.com` — successful execution artifact; SHA-256 `cfc650c60e0bb6bed1da5b767c5dedc9f45805eee0f5b651b032ce3f3fdc6806`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_b3lyp_opt_freq/outputs/execution_jobs/job_6f04b86b750346efa0df81f86255d6b5/request.json` — successful execution artifact; SHA-256 `df1ffcfeffed4536b1cf665e952d33a096dc23651d5b00e1c636faac62eeaa77`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_b3lyp_opt_freq/outputs/execution_jobs/job_6f04b86b750346efa0df81f86255d6b5/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_rb3lyp_retry/outputs/execution_jobs/job_530fd94f40ad4bb987b91e04e1c5c2ed/status.json` — successful status record; SHA-256 `f1f8ca3254177133c601c3a0d91ac03db7a1e0f6ab607b803e27187a9a61087d`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_rb3lyp_retry/outputs/execution_jobs/job_530fd94f40ad4bb987b91e04e1c5c2ed/collection.json` — successful execution artifact; SHA-256 `743a63d8f814364eef4ebb56ce90d946abb54016d162f10fec4a8d83b33c526c`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_rb3lyp_retry/outputs/execution_jobs/job_530fd94f40ad4bb987b91e04e1c5c2ed/input.com` — successful execution artifact; SHA-256 `b93479babcc1c05417084dc852e35b4e95219a92862b0791d69f6180bdc40701`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_rb3lyp_retry/outputs/execution_jobs/job_530fd94f40ad4bb987b91e04e1c5c2ed/request.json` — successful execution artifact; SHA-256 `4edff2ae82d77230016ba54bfafa92dfa6ff437579b64331662b78e3fd810794`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_product_rb3lyp_retry/outputs/execution_jobs/job_530fd94f40ad4bb987b91e04e1c5c2ed/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq/outputs/execution_jobs/job_43eec333f46242e6acc3129f0d0c8c49/status.json` — successful status record; SHA-256 `27d1110fb821218724dd5bdcd07918c7d41a77aeacac52cdd6f6f23c530b3e08`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq/outputs/execution_jobs/job_43eec333f46242e6acc3129f0d0c8c49/collection.json` — successful execution artifact; SHA-256 `71c0889a01569deea68683294d60d7f3be36a97cdfef21aec1d0a14fa3bb31a4`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq/outputs/execution_jobs/job_43eec333f46242e6acc3129f0d0c8c49/input.com` — successful execution artifact; SHA-256 `5d204a91a499fa98723be449f6b69d679fafc4eddbf93f893dce6b0a0e0643e8`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq/outputs/execution_jobs/job_43eec333f46242e6acc3129f0d0c8c49/request.json` — successful execution artifact; SHA-256 `e1d639238342542ea4cd7109fa97d024ee2250fdc697231c70185401c204f00c`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq/outputs/execution_jobs/job_43eec333f46242e6acc3129f0d0c8c49/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_45db9b312f5c462a9989dddcd81b1b0f/status.json` — successful status record; SHA-256 `e03f8c419b105b2dad3449afddd89f080ace2089a9e06f9ea6f928e3efe8da9d`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_45db9b312f5c462a9989dddcd81b1b0f/collection.json` — successful execution artifact; SHA-256 `af2904a699f85d0490df93bf0c59ed08de64de31b42d541b7bceeaa77ae656a3`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_45db9b312f5c462a9989dddcd81b1b0f/input.com` — successful execution artifact; SHA-256 `6845911a77ecb7f5232166a41fb867ab9a81c870c9b1b3d48b94999cc2f909b6`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_45db9b312f5c462a9989dddcd81b1b0f/request.json` — successful execution artifact; SHA-256 `fa20055cd79adda48822e3df0d4d4e2bafe42e440e1c05fec4b33cafd5ee031b`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_45db9b312f5c462a9989dddcd81b1b0f/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq/outputs/execution_jobs/job_ee04b93717894d4a8b4372467f028422/status.json` — successful status record; SHA-256 `e78f18d6f7ccba2f2b96a85b523b5fc633ea3650089beb1b387716a978f0e380`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq/outputs/execution_jobs/job_ee04b93717894d4a8b4372467f028422/collection.json` — successful execution artifact; SHA-256 `2274b3e14f4e504d951fb61e11e934bb2dad62c13b824ca9cc959d1e4883b781`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq/outputs/execution_jobs/job_ee04b93717894d4a8b4372467f028422/input.com` — successful execution artifact; SHA-256 `63082cad51091f75567d7a8c73f04afff79aa72d46618c9c35aac74c17d71947`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq/outputs/execution_jobs/job_ee04b93717894d4a8b4372467f028422/request.json` — successful execution artifact; SHA-256 `c7e09bda79e1ce4eed675b401fff10abd097449a038af3505c2bfa33e68aeeae`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq/outputs/execution_jobs/job_ee04b93717894d4a8b4372467f028422/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_3fecbed8bd3042a6ac722163510dea23/status.json` — successful status record; SHA-256 `b51e90db7c27a377cd74ad34d71e45e48bef05ae62902564303fbdffcaf2771f`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_3fecbed8bd3042a6ac722163510dea23/collection.json` — successful execution artifact; SHA-256 `26b81835080434b90edd104a75f5d9353c9c7d674953ae2b9dd81b1d00ef614e`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_3fecbed8bd3042a6ac722163510dea23/input.com` — successful execution artifact; SHA-256 `d0531ec6800ab97b2a76a8e57cd734a8b9878c9217e9716eef90e785c4cdcf44`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_3fecbed8bd3042a6ac722163510dea23/request.json` — successful execution artifact; SHA-256 `6859feeadbc9449835994beb37c1ccece7877a89b10226adfe93b72d2ae55d02`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/hydroxide_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_3fecbed8bd3042a6ac722163510dea23/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq/outputs/execution_jobs/job_894b4951738f4464ad38a0c13a7ba9b7/status.json` — successful status record; SHA-256 `32e07c7d8dfb5be6ecc33eb97dd0d406be43c9f3652705818f18eca651e015bb`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq/outputs/execution_jobs/job_894b4951738f4464ad38a0c13a7ba9b7/collection.json` — successful execution artifact; SHA-256 `08345e56b9e5eba90e0024e529022d3acf333f73261c82e634d3e7469d656b4b`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq/outputs/execution_jobs/job_894b4951738f4464ad38a0c13a7ba9b7/input.com` — successful execution artifact; SHA-256 `99d230e12ff441235e4ba09ccbbb8ea88f7b8c5a07442b4fa5aed92f202242e6`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq/outputs/execution_jobs/job_894b4951738f4464ad38a0c13a7ba9b7/request.json` — successful execution artifact; SHA-256 `c582a257d91d27566c929ea5b2d1d9b16f177070a2bc68d6768e97d90259ace3`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq/outputs/execution_jobs/job_894b4951738f4464ad38a0c13a7ba9b7/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_0f1a7a128f0d44d3bbcac2d7104d0f1c/status.json` — successful status record; SHA-256 `8dde167da3e8109a137d5cbf2af61c9cb3afc110cd649b269ed6fdcdf0a9e9b5`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_0f1a7a128f0d44d3bbcac2d7104d0f1c/collection.json` — successful execution artifact; SHA-256 `659fd5a8227584a716a528012793c3cb7a07e26b85935a6c60cfceb996291e00`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_0f1a7a128f0d44d3bbcac2d7104d0f1c/input.com` — successful execution artifact; SHA-256 `e6a6be1ef1678bcd6fa30a7a3894609a0d6d101446e5ef0c19dee03b17bd4c1b`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_0f1a7a128f0d44d3bbcac2d7104d0f1c/request.json` — successful execution artifact; SHA-256 `8282b442519938a1a4509618c3caa8d968cb8e8c44aa96e2c3bfae0a354ce0de`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_0f1a7a128f0d44d3bbcac2d7104d0f1c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/iminotriazole/outputs/execution_jobs/job_ce306f83f01c46d2bf61c18ff199c095/status.json` — successful status record; SHA-256 `0eb8aaa3ac4d0823e6853afde728cfe8bf3bd1f911dc2c3c14891a58e5bda495`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/iminotriazole/outputs/execution_jobs/job_ce306f83f01c46d2bf61c18ff199c095/collection.json` — successful execution artifact; SHA-256 `e9e34d2ad1414a8ebebea1d8c9aafaa95077f47e72184cc5c061161e96ccf2d0`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/iminotriazole/outputs/execution_jobs/job_ce306f83f01c46d2bf61c18ff199c095/input.com` — successful execution artifact; SHA-256 `c9c4947c8b84cb666aa696e54b0b51c805f5df5007a571e5da22a9ee4ec2a47c`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/iminotriazole/outputs/execution_jobs/job_ce306f83f01c46d2bf61c18ff199c095/request.json` — successful execution artifact; SHA-256 `2d2cc976ef8aa6cb3b008217719df9fb2dc66d669380adf13917ae04aa29a620`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/iminotriazole/outputs/execution_jobs/job_ce306f83f01c46d2bf61c18ff199c095/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq/outputs/execution_jobs/job_c5c6f75056654e348063e36900c821a4/status.json` — successful status record; SHA-256 `64c3801d2596d8e08c187061aa6635dca9f89f394aac996e24e59e5f02e75b3e`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq/outputs/execution_jobs/job_c5c6f75056654e348063e36900c821a4/collection.json` — successful execution artifact; SHA-256 `db92bfc5aa943b24e49c03526ca521db1697a1f131edc0a6ef708d132c1747a1`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq/outputs/execution_jobs/job_c5c6f75056654e348063e36900c821a4/input.com` — successful execution artifact; SHA-256 `5667ed163417e470d3645e34165179ab8d4ea186d0a79e3aae57629cd39139f8`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq/outputs/execution_jobs/job_c5c6f75056654e348063e36900c821a4/request.json` — successful execution artifact; SHA-256 `4ba7d2bedbe9b10fb6d5158c45499b34bbd030621a2a0d91cc59551f0c30a356`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq/outputs/execution_jobs/job_c5c6f75056654e348063e36900c821a4/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_8c42e3c176d24d19ada006d7ff77f7cd/status.json` — successful status record; SHA-256 `06dd6ecba99d387a490558d4c734bf0e274401e410119ca5670ddf63586915b0`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_8c42e3c176d24d19ada006d7ff77f7cd/collection.json` — successful execution artifact; SHA-256 `c3c1712f7a247a4c3495028e898092c66e34f622dcf8b137cfa84d93aa6d37b6`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_8c42e3c176d24d19ada006d7ff77f7cd/input.com` — successful execution artifact; SHA-256 `a55d8a096ae26d3d13961f09e8e77cb402c22de5a4adeadb2a315ed1b9eefc8e`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_8c42e3c176d24d19ada006d7ff77f7cd/request.json` — successful execution artifact; SHA-256 `fc1e5e2ffbee47c2f220d1a57b44bb7d131a81ae96c22839d56d2254cd64a552`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitroso_si_cpcm_opt_freq_m062x_smd_sp/outputs/execution_jobs/job_8c42e3c176d24d19ada006d7ff77f7cd/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitrosotriazole/outputs/execution_jobs/job_538556a0956f42ec9b404dc0e3779766/status.json` — successful status record; SHA-256 `f151f3e80bf6e95ddd7b9bdff0d6b6ec568d83780d798618ab8035f54d676f1c`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitrosotriazole/outputs/execution_jobs/job_538556a0956f42ec9b404dc0e3779766/collection.json` — successful execution artifact; SHA-256 `1a5c3be321806292750251ce09678e34feb146421fc6f820ef8f6342989dc1d8`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitrosotriazole/outputs/execution_jobs/job_538556a0956f42ec9b404dc0e3779766/input.com` — successful execution artifact; SHA-256 `6f4f62ee034f1f24e73dca363ebc60b9bf074ab9d5e1b9b254efb9815c179f85`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitrosotriazole/outputs/execution_jobs/job_538556a0956f42ec9b404dc0e3779766/request.json` — successful execution artifact; SHA-256 `5ed3e3464382c599560600193cddf315072d9756e7842c8072b3f7d25f1a70ee`
- `docs/verification/group_3/paper_51a03695e1ccb105/native_workspace/nitrosotriazole/outputs/execution_jobs/job_538556a0956f42ec9b404dc0e3779766/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/iminotriazole/status.json` — label=group_3 paper_51a03695e1ccb105 iminotriazole; submitted_at=2026-08-29T07:50:21.205132+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/iminotriazole.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/iminotriazole.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/iminotriazole_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/iminotriazole/stderr.log`
2. `artifacts/gaussian/nitrosotriazole/status.json` — label=group_3 paper_51a03695e1ccb105 nitrosotriazole; submitted_at=2026-08-29T07:50:21.926794+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/nitrosotriazole.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/nitrosotriazole.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/nitrosotriazole_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitrosotriazole/stderr.log`
3. `artifacts/gaussian/azo_product_b3lyp_opt_freq/status.json` — label=group_3 paper_51a03695e1ccb105 azo_product_b3lyp_opt_freq; submitted_at=2026-08-29T16:54:00.128485+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/azo_product_b3lyp_opt_freq.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/azo_product_b3lyp_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/azo_product_b3lyp_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_b3lyp_opt_freq/stderr.log`
4. `artifacts/gaussian/azo_product_rb3lyp_retry/status.json` — label=group_3 paper_51a03695e1ccb105 azo_product_rb3lyp_retry; submitted_at=2026-08-29T17:06:09.250499+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycle=512) Freq Int=UltraFine NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/azo_product_rb3lyp_retry.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/azo_product_rb3lyp_retry.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/azo_product_rb3lyp_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_product_rb3lyp_retry/stderr.log`
5. `artifacts/gaussian/imino_anion_si_cpcm_opt_freq/status.json` — label=group_3 paper_51a03695e1ccb105 imino_anion_si_cpcm_opt_freq; submitted_at=2026-08-30T12:36:00.866198+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycles=300) Freq Int=UltraFine NoSymm SCF=XQC SCRF=(CPCM,Solvent=Methanol); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/imino_anion_si_cpcm_opt_freq.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/imino_anion_si_cpcm_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/imino_anion_si_cpcm_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq/stderr.log`
6. `artifacts/gaussian/nitroso_si_cpcm_opt_freq/status.json` — label=group_3 paper_51a03695e1ccb105 nitroso_si_cpcm_opt_freq; submitted_at=2026-08-30T12:36:07.866015+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycles=300) Freq Int=UltraFine NoSymm SCF=XQC SCRF=(CPCM,Solvent=Methanol); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/nitroso_si_cpcm_opt_freq.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/nitroso_si_cpcm_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/nitroso_si_cpcm_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq/stderr.log`
7. `artifacts/gaussian/azo_si_s12_cpcm_opt_freq/status.json` — label=group_3 paper_51a03695e1ccb105 azo_si_s12_cpcm_opt_freq; submitted_at=2026-08-30T12:36:12.978575+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycles=300) Freq Int=UltraFine NoSymm SCF=XQC SCRF=(CPCM,Solvent=Methanol); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/azo_si_s12_cpcm_opt_freq.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/azo_si_s12_cpcm_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/azo_si_s12_cpcm_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq/stderr.log`
8. `artifacts/gaussian/hydroxide_cpcm_opt_freq/status.json` — label=group_3 paper_51a03695e1ccb105 hydroxide_cpcm_opt_freq; submitted_at=2026-08-30T12:36:19.166471+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycles=300) Freq Int=UltraFine NoSymm SCF=XQC SCRF=(CPCM,Solvent=Methanol); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/hydroxide_cpcm_opt_freq.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/hydroxide_cpcm_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/hydroxide_cpcm_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq/stderr.log`
9. `artifacts/gaussian/azo_TS2_si_cpcm_ts/status.json` — label=group_3 paper_51a03695e1ccb105 azo_TS2_si_cpcm_ts; submitted_at=2026-08-30T12:36:25.259437+00:00; software=gaussian; intent=transition_state; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(TS,CalcFC,NoEigenTest,MaxStep=3,MaxCycles=300) Freq Int=UltraFine NoSymm SCF=XQC SCRF=(CPCM,Solvent=Methanol); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/azo_TS2_si_cpcm_ts.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/azo_TS2_si_cpcm_ts.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/azo_TS2_si_cpcm_ts_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts/stderr.log`
10. `artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/status.json` — label=group_3 paper_51a03695e1ccb105 nitroso_si_cpcm_opt_freq_m062x_smd_sp; submitted_at=2026-08-30T12:57:52.730700+00:00; software=gaussian; intent=single_point; route=#p M062X/def2TZVP SCRF=(SMD,Solvent=Methanol) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/nitroso_si_cpcm_opt_freq_m062x_smd_sp.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/nitroso_si_cpcm_opt_freq_m062x_smd_sp.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/nitroso_si_cpcm_opt_freq_m062x_smd_sp_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/nitroso_si_cpcm_opt_freq_m062x_smd_sp/stderr.log`
11. `artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/status.json` — label=group_3 paper_51a03695e1ccb105 hydroxide_cpcm_opt_freq_m062x_smd_sp; submitted_at=2026-08-30T12:58:00.566756+00:00; software=gaussian; intent=single_point; route=#p M062X/def2TZVP SCRF=(SMD,Solvent=Methanol) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/hydroxide_cpcm_opt_freq_m062x_smd_sp.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/hydroxide_cpcm_opt_freq_m062x_smd_sp.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/hydroxide_cpcm_opt_freq_m062x_smd_sp_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/hydroxide_cpcm_opt_freq_m062x_smd_sp/stderr.log`
12. `artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/status.json` — label=group_3 paper_51a03695e1ccb105 imino_anion_si_cpcm_opt_freq_m062x_smd_sp; submitted_at=2026-08-30T13:05:55.100661+00:00; software=gaussian; intent=single_point; route=#p M062X/def2TZVP SCRF=(SMD,Solvent=Methanol) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/imino_anion_si_cpcm_opt_freq_m062x_smd_sp.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/imino_anion_si_cpcm_opt_freq_m062x_smd_sp.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/imino_anion_si_cpcm_opt_freq_m062x_smd_sp_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/imino_anion_si_cpcm_opt_freq_m062x_smd_sp/stderr.log`
13. `artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/status.json` — label=group_3 paper_51a03695e1ccb105 azo_si_s12_cpcm_opt_freq_m062x_smd_sp; submitted_at=2026-08-30T14:01:35.666292+00:00; software=gaussian; intent=single_point; route=#p M062X/def2TZVP SCRF=(SMD,Solvent=Methanol) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/azo_si_s12_cpcm_opt_freq_m062x_smd_sp.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/azo_si_s12_cpcm_opt_freq_m062x_smd_sp.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/azo_si_s12_cpcm_opt_freq_m062x_smd_sp_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_si_s12_cpcm_opt_freq_m062x_smd_sp/stderr.log`
14. `artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/status.json` — label=group_3 paper_51a03695e1ccb105 azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g; submitted_at=2026-09-01T02:06:11.526782+00:00; software=gaussian; intent=reaction_path; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Int=UltraFine NoSymm SCF=(XQC,MaxCycle=2048) SCRF=(CPCM,Solvent=Methanol) IRC=(CalcFC,MaxPoints=100,StepSize=2,MaxCycles=100); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/stderr.log`
15. `artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/status.json` — label=group_3 paper_51a03695e1ccb105 azo_TS2_si_cpcm_ts_m062x_smd_sp; submitted_at=2026-09-02T02:27:58.207440+00:00; software=gaussian; intent=single_point; route=#p M062X/def2TZVP SCRF=(SMD,Solvent=Methanol) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/azo_TS2_si_cpcm_ts_m062x_smd_sp.chk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/azo_TS2_si_cpcm_ts_m062x_smd_sp.fchk`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/azo_TS2_si_cpcm_ts_m062x_smd_sp_optimized.xyz`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/collection.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/formchk.log`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/input.com`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_m062x_smd_sp/stderr.log`

## Evaluator alignment

- Key-point IDs: `pr_process_minima, pr_process_ts, pr_result_barrier, pr_result_thermo`
- Conclusion IDs: `pr_final`
- Scoring-rule IDs: `pr_r1, pr_r2, pr_r3, pr_r4, pr_r5`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `pr_r1` → reference `pr_process_minima`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r2` → reference `pr_process_ts`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r3` → reference `pr_result_barrier`; type=numeric; unit=kcal/mol; tolerance=3; comparison=absolute difference; evaluator_target_present=True
- rule `pr_r4` → reference `pr_result_thermo`; type=numeric; unit=kcal/mol; tolerance=5; comparison=absolute difference; evaluator_target_present=True
- rule `pr_r5` → reference `pr_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `pr_r3` / reference `pr_result_barrier`: target=13.35 kcal/mol; tolerance=3; numeric result leaves=[13.252133500398472]; within_tolerance=True; applicability=applicable
- rule `pr_r4` / reference `pr_result_thermo`: target=-29.58 kcal/mol; tolerance=5; numeric result leaves=[-29.5339200778861]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[0].identity` = `"iminotriazole anion (SI Table S8/public XYZ; atom-balanced reactant)"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[0].charge` = `-1`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[0].multiplicity` = `1`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[0].frequency_diagnostic` = `"validated minimum; zero imaginary frequencies; imino_anion_si_cpcm_opt_freq"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[1].identity` = `"nitrosotriazole (SI Tables S12-S13/public XYZ)"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[1].charge` = `0`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[1].multiplicity` = `1`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.reactants` / result path `$.states.reactants[1].frequency_diagnostic` = `"validated minimum; zero imaginary frequencies; nitroso_si_cpcm_opt_freq"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.product` / result path `$.states.product.identity` = `"neutral 3,3′-azo-1,2,4-triazole (SI Tables S12-S13)"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.product` / result path `$.states.product.charge` = `0`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.product` / result path `$.states.product.multiplicity` = `1`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.product` / result path `$.states.product.frequency_diagnostic` = `"validated minimum; zero imaginary frequencies; azo_si_s12_cpcm_opt_freq"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.coproduct` / result path `$.states.coproduct.identity` = `"hydroxide anion (OH−; atom/charge-balanced coproduct)"`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.coproduct` / result path `$.states.coproduct.charge` = `-1`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.coproduct` / result path `$.states.coproduct.multiplicity` = `1`
- rule `pr_r1` / reference `pr_process_minima` / field `$.states.coproduct` / result path `$.states.coproduct.frequency_diagnostic` = `"validated minimum; zero imaginary frequencies; hydroxide_cpcm_opt_freq"`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].candidate_id` = `"azo_TS2_si_cpcm_ts"`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].geometry_provenance` = `"SI Table S17 / Fig. S8 TS-2 Cartesian candidate (azotriazole_ts2_si.xyz), independently reoptimized"`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].validation_status` = `"validated"`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].imaginary_frequency_diagnostic` = `"count=1; values_cm^-1=[-1650.1799]; required mode=N-N bond formation coupled to O-H transfer"`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].imaginary_frequency_details.count` = `1`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].imaginary_frequency_details.values_cm_minus_1[0]` = `-1650.1799`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].imaginary_frequency_details.required_mode` = `"N-N bond formation coupled to O-H transfer"`
- rule `pr_r2` / reference `pr_process_ts` / field `$.states.candidates` / result path `$.states.candidates[0].connection_evidence` = `"normally terminated IRC: azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g; endpoint inspection archived in artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/"`
- rule `pr_r3` / reference `pr_result_barrier` / field `$.activation_free_energy_kcal_mol` / result path `$.activation_free_energy_kcal_mol` = `13.252133500398472`
- rule `pr_r4` / reference `pr_result_thermo` / field `$.reaction_free_energy_kcal_mol` / result path `$.reaction_free_energy_kcal_mol` = `-29.5339200778861`
- rule `pr_r5` / reference `pr_final` / field `$.conclusion` / result path `$.conclusion` = `"Atom-balanced base-assisted coupling is computationally supported within the stated model: the SI TS-2 branch has one relevant imaginary mode and an IRC connection, with ΔG‡=13.252 kcal/mol and ΔG_rxn=-29.534 kcal/mol for azo + OH− forma..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI TS input removed; leakage fix needs redesign
- Files changed in that review: `agent_input/submission_schema.json, agent_input/task.md, package_manifest.json, task_info.json`
- Files deleted in that review: `agent_input/data/inputs/azotriazole_ts2_si.xyz`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs/iminotriazole_anion.xyz` — Public XYZ reactant structure with explicit charge and multiplicity metadata.
- `data/inputs/nitrosotriazole.xyz` — Public XYZ reactant structure with explicit charge and multiplicity metadata.

Public input files and hashes:

- `agent_input/data/inputs/iminotriazole_anion.xyz` — SHA-256 `24e57554253085d61b2d7392ad1bdffb7caad6ccb7e20cd691117f047b5d3af2`; size=348 bytes; xyz_atom_count=9; xyz_comment=Supplied iminotriazole anion reactant geometry; charge -1, multiplicity 1; explicit_boundary_fields={"charge": "-1", "multiplicity": "1"}
- `agent_input/data/inputs/nitrosotriazole.xyz` — SHA-256 `84c4d382e625c6be9d7fdc8d9cb3ad3fd00dc97b8f61592783704ff69516732c`; size=343 bytes; xyz_atom_count=9; xyz_comment=Supplied nitrosotriazole reactant geometry; charge 0, multiplicity 1; explicit_boundary_fields={"charge": "0", "multiplicity": "1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_51a03695e1ccb105/verification_report.md` — verification record; SHA-256 `d2442af4c166677076a855154c3e065ca58caa9b6da82142b967cca8bb738d50`
- `docs/verification/group_3/paper_51a03695e1ccb105/report/results.json` — verification record; SHA-256 `e295ac1f3e4133458d4a972d358b53c53097858255453d51dfb9f30227b96175`
- `docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/status.json` — referenced successful evidence; SHA-256 `f142a152f72006fe3cb8086670ea183690eacd5ebc2a9395a2d9a68148742318`
- `docs/verification/group_3/paper_51a03695e1ccb105/provenance/job_inventory.json` — referenced successful evidence; SHA-256 `fbefc9bcd324303165828a9cf25e888c562ed23763af080c052f699807a2e850`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
