# Verified computation reference — paper_b276b18215cba283 (autonomous_research)

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
| 52 | `QUALIFIED` | 因此当前计算状态为 **QUALIFIED（scope-limited）**；`report/results.json` 中的完整结果与本节保持一致。此前失败/重试记录仍保留在 ledger 中，但未被用作成功证据。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Stable ultrabright nanoprobes for two-photon excitation microscopy based on octupolar merocyanine-loaded nanovesicles
- DOI: `10.1039/d5tb02465j`
- Task package: `tasks/final_verified_autonomous_research/paper_b276b18215cba283`
- Verification group: `docs/verification/group_2/paper_b276b18215cba283`
- Paper documents: `papers/paper_b276b18215cba283`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "Within the isolated gas-phase single-arm model, cisoid is lower in S1 excitation energy than transoid, supporting a conformational red shift. This does not prove the full experimental photochemical mechanism, membrane response, kinetics, or experimental wavelength.",
  "input_repair": "Only O symbols mistranscribed as digit 0 were corrected from SI; Cartesian coordinates unchanged. Original public input and hashes retained in provenance/SI_VERTICAL_INPUT_RECOVERY_20260910.json.",
  "provenance": {
    "basis_or_model": "6-31G(d,p)",
    "convergence": "SCF=Tight with XQC fallback, MaxCycle=512; UltraFine integration; NoSymm; both Gaussian application return codes 0 and normal termination",
    "environment": "isolated gas-phase neutral singlet single-arm model",
    "method": "CAM-B3LYP linear-response TD-DFT, lowest ten singlets at SI S0 geometries",
    "software": "Gaussian16 C.01; author Gaussian16 B.01, revision difference disclosed"
  },
  "shift_eV": -0.08050000000000024,
  "status": "complete",
  "structures": [
    {
      "atom_count_verified": true,
      "calculation_status": "converged; Gaussian normal termination; ten singlet TD roots obtained",
      "charge": 0,
      "hpc_job_id": "hpc-job-36dfcb4f-ab4b-43ff-b90d-a932da6047d1",
      "multiplicity": 1,
      "name": "transoid",
      "orbital_character": "Predominantly HOMO (107) -> LUMO (108), printed TD amplitude 0.69409; amplitudes are not asserted to be exact population percentages.",
      "oscillator_strength": 0.9032,
      "raw_output": "provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/stdout.log",
      "s1_energy_eV": 3.2646,
      "validation_notes": "57 atoms C26H27NO3; SI Table S8 matches public XYZ, submitted deck and output geometry. 107 alpha and 107 beta electrons. All ten singlet excitation energies positive and ordered; S1 is the lowest singlet, not a triplet. No reoptimization or conformer search."
    },
    {
      "atom_count_verified": true,
      "calculation_status": "converged; Gaussian normal termination; ten singlet TD roots obtained",
      "charge": 0,
      "hpc_job_id": "hpc-job-609fdb38-8dcd-425a-8069-15dd32a95360",
      "multiplicity": 1,
      "name": "cisoid",
      "orbital_character": "Predominantly HOMO (107) -> LUMO (108), printed TD amplitude 0.67019; amplitudes are not asserted to be exact population percentages.",
      "oscillator_strength": 0.5584,
      "raw_output": "provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/stdout.log",
      "s1_energy_eV": 3.1841,
      "validation_notes": "57 atoms C26H27NO3; SI Table S9 matches public XYZ, submitted deck and output geometry. 107 alpha and 107 beta electrons. All ten singlet excitation energies positive and ordered; S1 is the lowest singlet, not a triplet. No reoptimization or conformer search."
    }
  ],
  "uncertainty_and_method_sensitivity": "Output energies round to 0.0001 eV (difference rounding bound 0.0001 eV). No functional/solvent sensitivity calculation or broader error bound is claimed. Use of the author's model avoids fitting methods to the target. Fixed supplied SI geometry is the requested endpoint; previous optimized geometries are excluded. Software revision and integration controls may cause small numerical differences."
}
```

Paper/SI document hashes:

- `papers/paper_b276b18215cba283/documents/main.pdf` — SHA-256 `389f29d6530237e6642f504587587564347b11765747bb427fc6568960d0b1c4` (declared_match=True)
- `papers/paper_b276b18215cba283/documents/supplementary_001.pdf` — SHA-256 `2c5e532a011fe24841808d9dd1c9f5ef653d924992cc1080a13cbc7e7ee09abf` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **50**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/status.json` — successful status record; SHA-256 `96ba6ea687e934df66ff09c155bb2e4de05b49098f6c6e2d58af7cb52ba3b39c`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/input.com` — successful execution artifact; SHA-256 `2f70a8917b0c5a3b8615f7488fd8eb09f94cc48b2eafc2fed3100713df1c58a1`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/route_manifest.json` — successful execution artifact; SHA-256 `538662850619ee65719adc17d2cdccb13e27036dd2f8187bb73ba8b019672735`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/stdout.log` — successful execution artifact; SHA-256 `f22e325f11bde11d5a71cae162cd3f2ed2fbe5a88402f9659d5eb18e485dc36b`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/status.json` — successful status record; SHA-256 `02fe4a084d1b2cfd5a07b7aca83adaaded2c10feb8195262233b7a66c18e307f`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/input.com` — successful execution artifact; SHA-256 `e0763bea6401adf1cc084370dee632171242febb1ade8a45d2ef1273f8e7ee17`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/route_manifest.json` — successful execution artifact; SHA-256 `e97a224c82b33f571aebd9c2d235fb93ede09e52d1e0d13f5c49f299e48c8c36`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/stdout.log` — successful execution artifact; SHA-256 `58b0ce813462c90f9d981911377ef62a698cf72091563f891256ef0a6bbd0e1f`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/status.json` — successful status record; SHA-256 `b49ed1701c17d266297f4ee75c4674f1930810564136791ad0f9b677d03fc279`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/collection.json` — successful execution artifact; SHA-256 `09de9dad6580fe87b5189a43b777cffb62e2bd122185cc105391a152bb163ec6`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/input.com` — successful execution artifact; SHA-256 `65d5a378074419fa4a1af6f97c977e05d34e081821354aa03f32a15ba88e0ab6`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/stderr.log` — successful execution artifact; SHA-256 `7f9c9e31ac8256ca2f258583df262dbc7d6f68f2a03043d5c99a4ae5a7396ce9`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/stdout.log` — successful execution artifact; SHA-256 `9c45fbc532e3ccc667e44e8a16bc00779062cc68ad44eeb5d7928b54ccd39122`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/status.json` — successful status record; SHA-256 `28455e225404648b546b8b04d1b9d4adcd7a94531c9847328fedea8037c973ad`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/collection.json` — successful execution artifact; SHA-256 `b8d65f9ff1fad4ff629f19477b28ca1568eac1a17650384d956e9f4007ce2aab`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/input.com` — successful execution artifact; SHA-256 `ee3c6bcbc08caf6fa3f97045ae509ecf9903fdae231e7d052efb033dea90b416`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/stderr.log` — successful execution artifact; SHA-256 `7f9c9e31ac8256ca2f258583df262dbc7d6f68f2a03043d5c99a4ae5a7396ce9`
- `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/stdout.log` — successful execution artifact; SHA-256 `14d33285bbfb11f039d8d3cfa2264d66db55ceef91e7c40753b0e38afbe81fe1`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_81aa8ba34e024309b1c32881d866e69a/status.json` — successful status record; SHA-256 `28455e225404648b546b8b04d1b9d4adcd7a94531c9847328fedea8037c973ad`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_81aa8ba34e024309b1c32881d866e69a/collection.json` — successful execution artifact; SHA-256 `b8d65f9ff1fad4ff629f19477b28ca1568eac1a17650384d956e9f4007ce2aab`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_81aa8ba34e024309b1c32881d866e69a/input.com` — successful execution artifact; SHA-256 `ee3c6bcbc08caf6fa3f97045ae509ecf9903fdae231e7d052efb033dea90b416`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_81aa8ba34e024309b1c32881d866e69a/request.json` — successful execution artifact; SHA-256 `4c358b1c720e78b6eedcc89fd1c9af650309b75a459bc025f05438008d029f4a`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_81aa8ba34e024309b1c32881d866e69a/status.pre_recovery.json` — successful execution artifact; SHA-256 `1925e7259880b71ca79a0b5b7ae38b6c24e81630b92fa716d7cdfa7520067a2a`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_f05e81f5d26143338c3a54162462c5aa/status.json` — successful status record; SHA-256 `b49ed1701c17d266297f4ee75c4674f1930810564136791ad0f9b677d03fc279`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_f05e81f5d26143338c3a54162462c5aa/collection.json` — successful execution artifact; SHA-256 `09de9dad6580fe87b5189a43b777cffb62e2bd122185cc105391a152bb163ec6`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_f05e81f5d26143338c3a54162462c5aa/input.com` — successful execution artifact; SHA-256 `65d5a378074419fa4a1af6f97c977e05d34e081821354aa03f32a15ba88e0ab6`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_f05e81f5d26143338c3a54162462c5aa/request.json` — successful execution artifact; SHA-256 `eef5cb44778e8a363a3d0e79f7b2882d6f42c89c0a3aa15fabaf48aee6ffdf68`
- `docs/verification/group_2/paper_b276b18215cba283/native_workspace_batch/outputs/execution_jobs/job_f05e81f5d26143338c3a54162462c5aa/status.pre_recovery.json` — successful execution artifact; SHA-256 `745e8106360e19a713f791ff6f43f528534cd354eafe2444e16ab1e81a9538b5`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/status.json` — successful status record; SHA-256 `17c2d5cf820dbab848b39f7c1b17622f4ce0ca655693a83e23a6bcc8f7b42cbd`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `90dfaab05ac2ac3ae0c30566de70fd7a53d2c889c89855b41cce0f3aa7d4b15e`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/input.com` — successful execution artifact; SHA-256 `5f01d61d6949e66608d37702dcceee5a9eeac232745d84c0ed5f6d516b271ca2`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/route_manifest.json` — successful execution artifact; SHA-256 `425acf14ed986f59b27c8e07ca664a010a019c27d9633f6c21a01c679c543ab5`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/status.json` — successful status record; SHA-256 `96ba6ea687e934df66ff09c155bb2e4de05b49098f6c6e2d58af7cb52ba3b39c`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `346f46a5df4b29cb24f6e4d970a071004bef3d0849ecbd18389b5b878e25222d`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/input.com` — successful execution artifact; SHA-256 `2f70a8917b0c5a3b8615f7488fd8eb09f94cc48b2eafc2fed3100713df1c58a1`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/route_manifest.json` — successful execution artifact; SHA-256 `538662850619ee65719adc17d2cdccb13e27036dd2f8187bb73ba8b019672735`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/status.json` — successful status record; SHA-256 `c4406a3a830e01af060b39b9296c932b3056e6e7209e6b8b402507b158d4bdc5`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `ad57d690add85b13ac0e4efd6ff965bb0f0b38e8480d91012fe626e2aec8f9a1`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/input.com` — successful execution artifact; SHA-256 `28193f6d4e5553d6bd8ca5f6bedea39ac4c3b8f030638fa4f2c47714eb72737a`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/route_manifest.json` — successful execution artifact; SHA-256 `8fc6ccbdb544871985352370ae283bbeed7cefd4b51c16e438b6b34b5f1f49cf`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/status.json` — successful status record; SHA-256 `02fe4a084d1b2cfd5a07b7aca83adaaded2c10feb8195262233b7a66c18e307f`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `0932671bf5f5e00ffa1315174b7d28492ea16f24d8e7d4b5d3deb9cf96e0995d`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/input.com` — successful execution artifact; SHA-256 `e0763bea6401adf1cc084370dee632171242febb1ade8a45d2ef1273f8e7ee17`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/route_manifest.json` — successful execution artifact; SHA-256 `e97a224c82b33f571aebd9c2d235fb93ede09e52d1e0d13f5c49f299e48c8c36`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/transoid_td10/status.json` — label=group_2 paper_b276b18215cba283 transoid_td10; submitted_at=2026-08-29T19:23:51.222088+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-31+G(d,p) TD(NStates=10) NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/collection.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/stderr.log`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/stdout.log`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/transoid_td10/transoid_td10.chk`
2. `artifacts/gaussian_batch/cisoid_td10/status.json` — label=group_2 paper_b276b18215cba283 cisoid_td10; submitted_at=2026-08-29T19:23:51.814385+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-31+G(d,p) TD(NStates=10) NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/cisoid_td10.chk`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/collection.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/stderr.log`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/cisoid_td10/stdout.log`
3. `artifacts/gaussian_batch/author_cisoid_si_vertical_td10/status.json` — label=artifacts/gaussian_batch/author_cisoid_si_vertical_td10/status.json
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/author_cisoid_si_vertical_td10.chk`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/route_manifest.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/stderr.log`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_cisoid_si_vertical_td10/stdout.log`
4. `artifacts/gaussian_batch/author_transoid_si_vertical_td10/status.json` — label=artifacts/gaussian_batch/author_transoid_si_vertical_td10/status.json
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/author_transoid_si_vertical_td10.chk`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/route_manifest.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/stderr.log`
   - output: `docs/verification/group_2/paper_b276b18215cba283/artifacts/gaussian_batch/author_transoid_si_vertical_td10/stdout.log`
5. `provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/status.json` — label=provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/status.json
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/author_cisoid_cam_b3lyp_631gdp_optfreq.chk`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/complete.marker`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/stderr.log`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_cam_b3lyp_631gdp_optfreq_hpc20_20260905T214446Z/stdout.log`
6. `provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/status.json` — label=provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/status.json
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/author_cisoid_si_vertical_td10.chk`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/complete.marker`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/fort.7`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/stderr.log`
7. `provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/status.json` — label=provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/status.json
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/author_transoid_cam_b3lyp_631gdp_optfreq_hpc_migration.chk`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/complete.marker`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/stderr.log`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_cam_b3lyp_631gdp_optfreq_local_migration_20260904T193237Z/stdout.log`
8. `provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/status.json` — label=provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/status.json
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/author_transoid_si_vertical_td10.chk`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/complete.marker`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/fort.7`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/input.com`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/stderr.log`

## Evaluator alignment

- Key-point IDs: `ar_process_identity, ar_process_state, ar_result_shift`
- Conclusion IDs: `ar_final_claim`
- Scoring-rule IDs: `ar_rule_identity, ar_rule_state, ar_rule_shift, ar_rule_conclusion`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `ar_rule_identity` → reference `ar_process_identity`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_rule_state` → reference `ar_process_state`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_rule_shift` → reference `ar_result_shift`; type=numeric; unit=eV; tolerance=0.03; comparison=absolute difference; evaluator_target_present=True
- rule `ar_rule_conclusion` → reference `ar_final_claim`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `ar_rule_shift` / reference `ar_result_shift`: target=-0.08 eV; tolerance=0.03; numeric result leaves=[-0.08050000000000024]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].name` = `"transoid"`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].atom_count_verified` = `true`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].charge` = `0`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].multiplicity` = `1`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].calculation_status` = `"converged; Gaussian normal termination; ten singlet TD roots obtained"`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].validation_notes` = `"57 atoms C26H27NO3; SI Table S8 matches public XYZ, submitted deck and output geometry. 107 alpha and 107 beta electrons. All ten singlet excitation energies positive and ordered; S1 is the lowest singlet, not a triplet. No reoptimizatio..."`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].s1_energy_eV` = `3.2646`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].oscillator_strength` = `0.9032`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].orbital_character` = `"Predominantly HOMO (107) -> LUMO (108), printed TD amplitude 0.69409; amplitudes are not asserted to be exact population percentages."`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].raw_output` = `"provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/stdout.log"`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[0].hpc_job_id` = `"hpc-job-36dfcb4f-ab4b-43ff-b90d-a932da6047d1"`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].name` = `"cisoid"`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].atom_count_verified` = `true`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].charge` = `0`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].multiplicity` = `1`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].calculation_status` = `"converged; Gaussian normal termination; ten singlet TD roots obtained"`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].validation_notes` = `"57 atoms C26H27NO3; SI Table S9 matches public XYZ, submitted deck and output geometry. 107 alpha and 107 beta electrons. All ten singlet excitation energies positive and ordered; S1 is the lowest singlet, not a triplet. No reoptimizatio..."`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].s1_energy_eV` = `3.1841`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].oscillator_strength` = `0.5584`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].orbital_character` = `"Predominantly HOMO (107) -> LUMO (108), printed TD amplitude 0.67019; amplitudes are not asserted to be exact population percentages."`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].raw_output` = `"provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/stdout.log"`
- rule `ar_rule_identity` / reference `ar_process_identity` / field `$.structures` / result path `$.structures[1].hpc_job_id` = `"hpc-job-609fdb38-8dcd-425a-8069-15dd32a95360"`
- rule `ar_rule_shift` / reference `ar_result_shift` / field `$.shift_eV` / result path `$.shift_eV` = `-0.08050000000000024`
- rule `ar_rule_conclusion` / reference `ar_final_claim` / field `$.conclusion` / result path `$.conclusion` = `"Within the isolated gas-phase single-arm model, cisoid is lower in S1 excitation energy than transoid, supporting a conformational red shift. This does not prove the full experimental photochemical mechanism, membrane response, kinetics,..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized/final structure is exposed as agent input for a scored comparison; redesign with neutral or independently generated starting geometry
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Neutral-singlet 57-atom XYZ structures for the named transoid and cisoid conformers.

Public input files and hashes:

- `agent_input/data/inputs/cisoid.xyz` — SHA-256 `ca652a2c08151ae0f6a0d182bb21679121445a71c370ebb8cee060214ab4ef2d`; size=1979 bytes; xyz_atom_count=57; xyz_comment=cisoid simplified single-arm chromophore; charge 0 multiplicity 1; explicit_boundary_fields={"charge": "0", "multiplicity": "1"}
- `agent_input/data/inputs/transoid.xyz` — SHA-256 `c398cb809c2b9e320d6a76ee3e8e6352eadb55c64224a5885bb1971c597fd6b4`; size=1982 bytes; xyz_atom_count=57; xyz_comment=transoid simplified single-arm chromophore; charge 0 multiplicity 1; explicit_boundary_fields={"charge": "0", "multiplicity": "1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_2/paper_b276b18215cba283/verification_report.md` — verification record; SHA-256 `58e9e545bb886bdac1d57e64c5c89bed6bb8da53e6500c837b73c029a200f3d3`
- `docs/verification/group_2/paper_b276b18215cba283/report/results.json` — verification record; SHA-256 `bda85f5d6f01661cf61e203a0072836e3661fd387039a266c9ab7d3b84edfdeb`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/SI_VERTICAL_INPUT_RECOVERY_20260910.json` — referenced successful evidence; SHA-256 `75951690e389cd818d19f1ac073dc2cd7ffcfaaf09056c90bc24281e145d2da7`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_cisoid_si_vertical_td10_hpc20_20260910T174604Z/stdout.log` — referenced successful evidence; SHA-256 `f22e325f11bde11d5a71cae162cd3f2ed2fbe5a88402f9659d5eb18e485dc36b`
- `docs/verification/group_2/paper_b276b18215cba283/provenance/qzcli_hpc/author_transoid_si_vertical_td10_hpc20_20260910T174609Z/stdout.log` — referenced successful evidence; SHA-256 `58b0ce813462c90f9d981911377ef62a698cf72091563f891256ef0a6bbd0e1f`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
