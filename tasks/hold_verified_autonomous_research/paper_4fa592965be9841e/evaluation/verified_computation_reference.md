# Verified computation reference — paper_4fa592965be9841e (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Current evidence status — NOT_RELEASE_READY (2026-09-18)

User decision (2026-09-18): move the ambiguous task to the corresponding hold directory. This package is withheld from release pending source-identity reconciliation and matching calculation evidence; the molecular identity has not been silently changed.

The six stored optimized XYZ branches (corrected, td8, author_6311pp, author_6311gplus_freq, author_6311gplus_td8 and anharmonic_hpc20_v2) all recover the graph with phenyl and thiophene on one alkene carbon, `N#CC=C(c1ccc(N=Cc2cccs2)cc1)c1cccs1`. Main p. 1 naming and p. 2 Fig. 1 instead place nitrile and phenyl on the same carbon: `N#CC(=Cc1cccs1)c1ccc(N=Cc2cccs2)cc1` (stereo omitted here deliberately). Same formula does not make those computations validate the stated object. No correct-connectivity completed branch was found in the inspected archive.

Further source reconciliation is required before the public identity is finalized: the source's E name and its drawn phenyl/thiophene relationship must be reconciled under explicit CIP priorities. Public SMILES still contains the pre-existing invalid N=CH token; it has not been silently replaced with the historically computed wrong graph. Main p. 5 Tables 4/5 give experimental IR 840,1551,1605,1450 cm⁻¹ and UV 262,385 nm, but the C–H 'stretching' label at 1450 cm⁻¹ and the unreported UV solvent need explicit scientific interpretation. These must not be cured by selecting whichever calculated mode is nearest the gold value. Identity/stereochemistry and mode-label decisions are pending; this package is not ready for release.

The historical PASS, spectra and rule matches below document completed executions of the other isomer, not current-object validation. Original group records remain unchanged.

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
| 75 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 report/results.json、artifacts/gaussian/ 和 provenance/。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Synthesis, crystal structure, DFT analysis, and molecular docking studies of a novel thiophene- containing acrylonitrile Schiff base as a potential tyrosine kinase inhibitor
- DOI: `10.1016/j.molstruc.2025.144652`
- Task package: `tasks/hold_verified_autonomous_research/paper_4fa592965be9841e`
- Verification group: `docs/verification/group_3/paper_4fa592965be9841e`
- Paper documents: `papers/paper_4fa592965be9841e`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "candidate_coverage": {
    "candidates_considered": 1,
    "deduplication_rule": "The fixed stereochemical SMILES defines one neutral E/E compound-I identity; repeated author-route and corrected runs were retained as validation records for that identity rather than counted as distinct molecular candidates.",
    "stopping_reason": "The fixed molecule was optimized and frequency-validated, all four requested IR assignments and two requested UV-visible bands were obtained, and the stated isolated-molecule diagnostic scope was complete; no additional candidate identity was required by the task boundary."
  },
  "conclusion": "The exact public B3LYP/6-311+G(d,p) follow-up is complete. All four IR assignments are numerically close to Table 4 (<=11 cm-1); the two visible/UV bands are within 15 nm of the experimental bands. Dominant configurations/NTO output provide qualitative, not quantitative, support for the reported intramolecular charge-transfer interpretation.",
  "frequency_validation": {
    "assignments": [
      {
        "absolute_error_cm1": 0.6081000000000358,
        "assignment": "C-S stretching",
        "computed_wavenumber_cm1": 840.6081,
        "experimental_cm1": 840.0
      },
      {
        "absolute_error_cm1": 3.6679999999998927,
        "assignment": "C=C stretching",
        "computed_wavenumber_cm1": 1554.668,
        "experimental_cm1": 1551.0
      },
      {
        "absolute_error_cm1": 8.03189999999995,
        "assignment": "C=N stretching",
        "computed_wavenumber_cm1": 1613.0319,
        "experimental_cm1": 1605.0
      },
      {
        "absolute_error_cm1": 10.757100000000037,
        "assignment": "C-H stretching",
        "computed_wavenumber_cm1": 1460.7571,
        "experimental_cm1": 1450.0
      }
    ],
    "imaginary_frequency_count": 0,
    "normal_termination": true
  },
  "ir_results": [
    {
      "assignment": "C-S stretching",
      "computed_wavenumber_cm1": 840.6081,
      "experimental_comparison": "computed=840.6081 cm-1; experimental=840.0 cm-1; absolute_error=0.6081000000000358 cm-1",
      "validation_evidence": "Gaussian normal termination and frequency output archived under source_evidence.raw_hpc_dirs"
    },
    {
      "assignment": "C=C stretching",
      "computed_wavenumber_cm1": 1554.668,
      "experimental_comparison": "computed=1554.668 cm-1; experimental=1551.0 cm-1; absolute_error=3.6679999999998927 cm-1",
      "validation_evidence": "Gaussian normal termination and frequency output archived under source_evidence.raw_hpc_dirs"
    },
    {
      "assignment": "C=N stretching",
      "computed_wavenumber_cm1": 1613.0319,
      "experimental_comparison": "computed=1613.0319 cm-1; experimental=1605.0 cm-1; absolute_error=8.03189999999995 cm-1",
      "validation_evidence": "Gaussian normal termination and frequency output archived under source_evidence.raw_hpc_dirs"
    },
    {
      "assignment": "C-H stretching",
      "computed_wavenumber_cm1": 1460.7571,
      "experimental_comparison": "computed=1460.7571 cm-1; experimental=1450.0 cm-1; absolute_error=10.757100000000037 cm-1",
      "validation_evidence": "Gaussian normal termination and frequency output archived under source_evidence.raw_hpc_dirs"
    }
  ],
  "limitations": "The article does not publish the original Cartesian/checkpoint or a numerical CT metric; Gaussian/NTO evidence therefore cannot claim an exact reproduction of the authors' orbital plots.",
  "method": {
    "excited_state_method": "B3LYP/6-311+G(d,p) Freq and TD=(NStates=8), gas phase",
    "followup": "B3LYP/6-311+G(d,p) Freq and TD=(NStates=8), gas phase",
    "frequency_method": "B3LYP/6-311+G(d,p) Freq and TD=(NStates=8), gas phase",
    "geometry": "B3LYP/6-311++G(d,p) Opt/Freq (Gaussian 09/16-compatible)",
    "geometry_method": "B3LYP/6-311++G(d,p) Opt/Freq (Gaussian 09/16-compatible)",
    "software": "Gaussian 16 C.01",
    "temperature": 298.15
  },
  "source_evidence": {
    "paper": "main.pdf Table 4 and Table 5; computational details section",
    "raw_hpc_dirs": [
      "docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1",
      "docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1"
    ]
  },
  "stationary_point": {
    "evidence": "Gaussian normal termination and frequency-validation records in source_evidence.raw_hpc_dirs",
    "imaginary_frequency_count": 0,
    "optimized": true
  },
  "status": "complete",
  "strict_acceptance": "PASS",
  "strict_author_route": true,
  "structure_validation": {
    "atom_count": 34,
    "charge": 0,
    "formula": "C18H12N2S2",
    "multiplicity": 1,
    "stereochemistry_verified": true
  },
  "uv_results": [
    {
      "band_id": "Band I",
      "comparison": "computed=276.78 nm; experimental=262.0 nm; absolute_error=14.779999999999973 nm",
      "oscillator_strength": 0.0422,
      "transition_character": "higher-energy pi-to-pi-star manifold; the Gaussian dominant configurations and archived NTO calculation are the evidence, while no numerical CT index is claimed",
      "wavelength_nm": 276.78
    },
    {
      "band_id": "Band II",
      "comparison": "computed=373.7 nm; experimental=385.0 nm; absolute_error=11.300000000000011 nm",
      "oscillator_strength": 0.5546,
      "transition_character": "lowest bright transition; Gaussian dominant configurations and NTO output support the paper's delocalized/charge-transfer interpretation only qualitatively",
      "wavelength_nm": 373.7
    }
  ],
  "uv_validation": {
    "all_eight_roots": [
      {
        "energy_eV": 3.3178,
        "oscillator_strength": 0.5546,
        "state": 1,
        "wavelength_nm": 373.7
      },
      {
        "energy_eV": 3.6065,
        "oscillator_strength": 0.0112,
        "state": 2,
        "wavelength_nm": 343.78
      },
      {
        "energy_eV": 3.7799,
        "oscillator_strength": 0.2671,
        "state": 3,
        "wavelength_nm": 328.01
      },
      {
        "energy_eV": 4.0699,
        "oscillator_strength": 0.2292,
        "state": 4,
        "wavelength_nm": 304.64
      },
      {
        "energy_eV": 4.1793,
        "oscillator_strength": 0.0427,
        "state": 5,
        "wavelength_nm": 296.67
      },
      {
        "energy_eV": 4.2146,
        "oscillator_strength": 0.0847,
        "state": 6,
        "wavelength_nm": 294.18
      },
      {
        "energy_eV": 4.4478,
        "oscillator_strength": 0.0492,
        "state": 7,
        "wavelength_nm": 278.75
      },
      {
        "energy_eV": 4.4795,
        "oscillator_strength": 0.0422,
        "state": 8,
        "wavelength_nm": 276.78
      }
    ],
    "normal_termination": true,
    "reported_bands": [
      {
        "absolute_error_nm": 14.779999999999973,
        "band_id": "Band I",
        "computed_state": 8,
        "experimental_wavelength_nm": 262.0,
        "oscillator_strength": 0.0422,
        "paper_calculated_wavelength_nm": 261.0,
        "transition_character": "higher-energy pi-to-pi-star manifold; the Gaussian dominant configurations and archived NTO calculation are the evidence, while no numerical CT index is claimed",
        "wavelength_nm": 276.78
      },
      {
        "absolute_error_nm": 11.300000000000011,
        "band_id": "Band II",
        "computed_state": 1,
        "experimental_wavelength_nm": 385.0,
        "oscillator_strength": 0.5546,
        "paper_calculated_wavelength_nm": 409.0,
        "transition_character": "lowest bright transition; Gaussian dominant configurations and NTO output support the paper's delocalized/charge-transfer interpretation only qualitatively",
        "wavelength_nm": 373.7
      }
    ]
  }
}
```

## Re-audit source-evidence drift

- Classification: **SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW**
- Previous `results.json` SHA-256: `52f29445e7f73d48f649463cbebd4b9ffdd19900f2b8bc44dba2cd777d04b793`
- Current `results.json` SHA-256: `a9de1987b8c4dc776310a668e764e17638fe8dd627ecdcd76b7cd5d30500fbdd`
- Changed top-level result fields: `candidate_coverage`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["candidate_coverage"], "classification": "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW", "current_sha256": "a9de1987b8c4dc776310a668e764e17638fe8dd627ecdcd76b7cd5d30500fbdd", "detected": true, "previous_sha256": "52f29445e7f73d48f649463cbebd4b9ffdd19900f2b8bc44dba2cd777d04b793"} -->

Paper/SI document hashes:

- `papers/paper_4fa592965be9841e/documents/supplementary_001.pdf` — SHA-256 `f6f8cecafea8ab20ee437c693a57bb733219302e656d7f00b50870adef80bf20` (declared_match=True)
- `papers/paper_4fa592965be9841e/documents/main.pdf` — SHA-256 `3d133a394a7f608bbe2300ef6431ef052053de81d804bb94a165d0f957b4b8d1` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |
- older 6-31G diagnostic artifacts: B3LYP/6-311++G(d,p) Opt/Freq for the public
- normally; the frequency calculation has zero imaginary modes and the TD job

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **60**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/status.json` — successful status record; SHA-256 `2d526b603dcbb9744ed7e16b249ae6ae8accc56876a92042a428f7ea72eee0b6`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/compoundI_author_6311gplus_freq_optimized.xyz` — successful execution artifact; SHA-256 `31a318fcac6e7297bfb6f71d760b20b3382e8f5b409dc06a83f44960f901beaa`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/formchk.log` — successful execution artifact; SHA-256 `850746a6ba04f464e688ed8b21429273d64137f98110c51e32c73dab75515220`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/gaussian.log` — successful execution artifact; SHA-256 `cd308c36bafae8f9a451681b0d82d48a2eb640230fc4b32d8114d1a2bf55e3a5`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/input.com` — successful execution artifact; SHA-256 `38c6215613a9acadc74fa8483745766942001218d64f2fdcd9cd9dd4c76c231b`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/status.json` — successful status record; SHA-256 `fdd6c650c37af514bd76ab620eb4c37a5f657d8e963282ec57baaa9cb5b4b48c`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/compoundI_author_6311gplus_td8_optimized.xyz` — successful execution artifact; SHA-256 `d630d8182616081af2456a9e7d48f4b739c3b0afc4d3a8449fcc0908082bfc11`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/formchk.log` — successful execution artifact; SHA-256 `86012e3f6aca75db67f7d7c5524788ea65ea9bf838edf5dfaaac657306c395f7`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/gaussian.log` — successful execution artifact; SHA-256 `f1b3c4cd5adf3493d1753c12ff532f4f7cf0acdd2cdc509a3de0455a648fbbaf`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/input.com` — successful execution artifact; SHA-256 `c6af2f0c35acf8ce04093280d79cd49e3ec1d2dbfad079563acd10c0e532f121`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/status.json` — successful status record; SHA-256 `be2e8bd5784320e1510afe0cdc35eec84b350e674b146a4dc5e1e21fd097c5ec`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/collection.json` — successful execution artifact; SHA-256 `5f6b98864dd647fab497f25f372088df1fde732974882f6d7286bfd0d47d2520`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/compoundI_author_6311pp_opt_freq_unbounded32g_optimized.xyz` — successful execution artifact; SHA-256 `bf067421bbec7b896ce3074402eb212ca5d1b56058ede9e34b4cc2d34057964a`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/formchk.log` — successful execution artifact; SHA-256 `578ed4420ebda49055578686bab3fc23ca5a59a42dadebad7b8b6a7503198776`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/input.com` — successful execution artifact; SHA-256 `cba1a7f340995a7c2ad71942c92dd74796014dcaa96f4528b396db717f538c83`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/status.json` — successful status record; SHA-256 `c9c0e2422e43ca249492cf8f4414defa64ac7eb6edf64795fbfec1ff1fb2b5cc`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/collection.json` — successful execution artifact; SHA-256 `055bdfc0b312f854328451e5e1b6ef1a28fd3d8f4a26c6b7a84c9e934982f93a`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/compoundI_corrected_optimized.xyz` — successful execution artifact; SHA-256 `53ea76235163ea45cece2b298205e2dd7488a1dc01cea7dc3f4e5829d4e7843f`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/formchk.log` — successful execution artifact; SHA-256 `75b4515e362ee450c003a04a2493995adcd6f682246df0baa0f3529b128d05bf`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/input.com` — successful execution artifact; SHA-256 `4af4619d267f3f3eb23fe60fd821a3c1ced319bbeac2e2f201c0abf265dd1eab`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/status.json` — successful status record; SHA-256 `ad735893fb93eda78048f638c5b0253bb5ef7e99038c0b900da01df0cce3adda`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/compoundI_ir_anharmonic_optimized.xyz` — successful execution artifact; SHA-256 `6c3309646f61fecadada02a6989556531c672e5e4daf1f703c3ffe61f9b64bfe`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/formchk.log` — successful execution artifact; SHA-256 `b16f6bd64d0601a3094a6c5ecf8120350cda19b0096e49dc0284e3f6c0db1384`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/input.com` — successful execution artifact; SHA-256 `868254eb2776eea93e4fe0793677648a5f7749160c39f4580300c35695a72e4b`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/parsed_observables.json` — successful execution artifact; SHA-256 `954c7bce91f45b0d900ea300884825dc6c16d8869a2446152f6b4e676b38c6f9`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/status.json` — successful status record; SHA-256 `a3d624327bf92a55991c4e099eb8ba998dcd3f9646d3be0029c2be99a2c62df5`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/collection.json` — successful execution artifact; SHA-256 `b20d2a6a7fce0ff74c69675ff33b686a483cd87a05f0e5b6cb01bbf5856ed9ea`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/compoundI_td8_optimized.xyz` — successful execution artifact; SHA-256 `257584b2f1d8afe17d1d622a3592b3fc4fd764febb1b60b36e9a7225c222acf6`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/formchk.log` — successful execution artifact; SHA-256 `6b6dd530b0b5d8fb88bfb17ba3e7a867ff9bba792ad6f12959a810608390fbdb`
- `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/input.com` — successful execution artifact; SHA-256 `0cf4518659b954295f0d4cd97004fad6e26758a83112074d7793a978261f03c7`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_author_6311pp_opt_freq_unbounded32g/outputs/execution_jobs/job_7ef0efcbd44e442ebbb6181745eebf4d/status.json` — successful status record; SHA-256 `be2e8bd5784320e1510afe0cdc35eec84b350e674b146a4dc5e1e21fd097c5ec`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_author_6311pp_opt_freq_unbounded32g/outputs/execution_jobs/job_7ef0efcbd44e442ebbb6181745eebf4d/collection.json` — successful execution artifact; SHA-256 `5f6b98864dd647fab497f25f372088df1fde732974882f6d7286bfd0d47d2520`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_author_6311pp_opt_freq_unbounded32g/outputs/execution_jobs/job_7ef0efcbd44e442ebbb6181745eebf4d/input.com` — successful execution artifact; SHA-256 `cba1a7f340995a7c2ad71942c92dd74796014dcaa96f4528b396db717f538c83`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_author_6311pp_opt_freq_unbounded32g/outputs/execution_jobs/job_7ef0efcbd44e442ebbb6181745eebf4d/request.json` — successful execution artifact; SHA-256 `77dd9be5f957ce55defe0c9d6ec88b976f590b55e19a535079bc605b5835b454`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_author_6311pp_opt_freq_unbounded32g/outputs/execution_jobs/job_7ef0efcbd44e442ebbb6181745eebf4d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_corrected/outputs/execution_jobs/job_78130b539da34814833eaf171235073c/status.json` — successful status record; SHA-256 `c9c0e2422e43ca249492cf8f4414defa64ac7eb6edf64795fbfec1ff1fb2b5cc`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_corrected/outputs/execution_jobs/job_78130b539da34814833eaf171235073c/collection.json` — successful execution artifact; SHA-256 `055bdfc0b312f854328451e5e1b6ef1a28fd3d8f4a26c6b7a84c9e934982f93a`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_corrected/outputs/execution_jobs/job_78130b539da34814833eaf171235073c/input.com` — successful execution artifact; SHA-256 `4af4619d267f3f3eb23fe60fd821a3c1ced319bbeac2e2f201c0abf265dd1eab`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_corrected/outputs/execution_jobs/job_78130b539da34814833eaf171235073c/request.json` — successful execution artifact; SHA-256 `d2e2edb91167d04115912d75068d5552204983f311e0e155acaa39bc799c694a`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_corrected/outputs/execution_jobs/job_78130b539da34814833eaf171235073c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_td8/outputs/execution_jobs/job_dd222526ec4144bb80cd8aa9150ab860/status.json` — successful status record; SHA-256 `a3d624327bf92a55991c4e099eb8ba998dcd3f9646d3be0029c2be99a2c62df5`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_td8/outputs/execution_jobs/job_dd222526ec4144bb80cd8aa9150ab860/collection.json` — successful execution artifact; SHA-256 `b20d2a6a7fce0ff74c69675ff33b686a483cd87a05f0e5b6cb01bbf5856ed9ea`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_td8/outputs/execution_jobs/job_dd222526ec4144bb80cd8aa9150ab860/input.com` — successful execution artifact; SHA-256 `0cf4518659b954295f0d4cd97004fad6e26758a83112074d7793a978261f03c7`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_td8/outputs/execution_jobs/job_dd222526ec4144bb80cd8aa9150ab860/request.json` — successful execution artifact; SHA-256 `7199ce45a48d96734aa1bb9e2d7ae20d46d8297307da0e5e8a0f94c350c2c778`
- `docs/verification/group_3/paper_4fa592965be9841e/native_workspace/compoundI_td8/outputs/execution_jobs/job_dd222526ec4144bb80cd8aa9150ab860/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/status.json` — successful status record; SHA-256 `a3d9ea103ca3ad37ec91229b8a1897719f4cf7acf8da6dbfc2eca0f951197f10`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/gaussian.log` — successful execution artifact; SHA-256 `cd308c36bafae8f9a451681b0d82d48a2eb640230fc4b32d8114d1a2bf55e3a5`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/hpc_stdout.log` — successful execution artifact; SHA-256 `501fa8d29005388c986cdf0642bd90b9d966c7c77dbc093226c3366f56f4b5e5`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/input.com` — successful execution artifact; SHA-256 `38c6215613a9acadc74fa8483745766942001218d64f2fdcd9cd9dd4c76c231b`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/resource_adjustment.json` — successful execution artifact; SHA-256 `9146c075cda6bb1d1ea0ade4dd8b5eaa2367ca5e9c24a2184589fd83488bf137`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/status.json` — successful status record; SHA-256 `0b46c408e3f1020e0a719672c928fdd20dc193f7ed35e96f533c2826b54b4d1e`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/gaussian.log` — successful execution artifact; SHA-256 `f1b3c4cd5adf3493d1753c12ff532f4f7cf0acdd2cdc509a3de0455a648fbbaf`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/hpc_stdout.log` — successful execution artifact; SHA-256 `21e27bf4eb7c52a79a47fa553b829174d4a1cbe09294ed8377003bde905ce094`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/input.com` — successful execution artifact; SHA-256 `c6af2f0c35acf8ce04093280d79cd49e3ec1d2dbfad079563acd10c0e532f121`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/resource_adjustment.json` — successful execution artifact; SHA-256 `22eb1742961261dc94afa64031f555910a768da3b6158667de67c9ee57dbf109`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/status.json` — successful status record; SHA-256 `cc1f6d11e15dc382e70d0fb33e6766260c3565ac52e475f4736914a1e2ccf45d`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/gaussian.log` — successful execution artifact; SHA-256 `f34d71398ae313bd35eace8f32997a9e43ccf2ae21e5c8b68aade7857541cd34`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/hpc_stdout.log` — successful execution artifact; SHA-256 `8579cb7db95bf2ed30438713dac978c9238e1a758e68add50127420b210d95a4`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/input.com` — successful execution artifact; SHA-256 `868254eb2776eea93e4fe0793677648a5f7749160c39f4580300c35695a72e4b`
- `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/resource_adjustment.json` — successful execution artifact; SHA-256 `7fbe5f44759099ce2a4dabccec6a88cd479e816229b999b4fde92fb1d8120d55`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/compoundI_corrected/status.json` — label=group_3 paper_4fa592965be9841e compoundI_corrected; submitted_at=2026-08-29T07:56:07.677198+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/collection.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/compoundI_corrected.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/compoundI_corrected.fchk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/compoundI_corrected_optimized.xyz`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/formchk.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/parsed_observables.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_corrected/stderr.log`
2. `artifacts/gaussian/compoundI_td8/status.json` — label=group_3 paper_4fa592965be9841e compoundI_td8; submitted_at=2026-08-30T18:21:26.082475+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ TD(NStates=8) Pop=(NTO,Full) NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/collection.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/compoundI_td8.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/compoundI_td8.fchk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/compoundI_td8_optimized.xyz`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/formchk.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/parsed_observables.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_td8/stderr.log`
3. `artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/status.json` — label=group_3 paper_4fa592965be9841e compoundI_author_6311pp_opt_freq_unbounded32g; submitted_at=2026-09-03T04:02:32.675269+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-311++G(d,p) Opt Freq Int=UltraFine NoSymm SCF=(XQC,MaxCycle=2048); command=g16 < input.com
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/collection.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/compoundI_author_6311pp_opt_freq_unbounded32g.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/compoundI_author_6311pp_opt_freq_unbounded32g.fchk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/compoundI_author_6311pp_opt_freq_unbounded32g_optimized.xyz`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/formchk.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311pp_opt_freq_unbounded32g/stderr.log`
4. `artifacts/gaussian/compoundI_author_6311gplus_freq/status.json` — label=hpc-job-c3bd47ed-ea77-483b-82ec-9c7b3b184bc0
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/compoundI_author_6311gplus_freq.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/compoundI_author_6311gplus_freq.fchk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/compoundI_author_6311gplus_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/formchk.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/gaussian.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/resource_adjustment.json`
5. `artifacts/gaussian/compoundI_author_6311gplus_td8/status.json` — label=hpc-job-bb26a965-d0a6-44a9-8cd4-8cb0be8fefcd
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/compoundI_author_6311gplus_td8.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/compoundI_author_6311gplus_td8.fchk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/compoundI_author_6311gplus_td8_optimized.xyz`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/formchk.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/gaussian.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/parsed_observables.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_td8/resource_adjustment.json`
6. `artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/status.json` — label=None
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/compoundI_ir_anharmonic.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/compoundI_ir_anharmonic.fchk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/compoundI_ir_anharmonic_optimized.xyz`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/formchk.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/parsed_observables.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_ir_anharmonic_hpc20_v2/stdout.log`
7. `provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/status.json` — label=provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/status.json
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/compoundI_author_6311gplus_freq.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/exit_code`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/gaussian.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/hpc_failure.txt`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_freq/1/sha256sums.txt`
8. `provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/status.json` — label=provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/status.json
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/compoundI_author_6311gplus_td8.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/exit_code`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/gaussian.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/hpc_failure.txt`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_author_6311gplus_td8/1/sha256sums.txt`
9. `provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/status.json` — label=provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/status.json
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/compoundI_ir_anharmonic.chk`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/exit_code`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/fort.7`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/gaussian.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/hpc_stdout.log`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/input.com`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/resource_adjustment.json`
   - output: `docs/verification/group_3/paper_4fa592965be9841e/provenance/qzcli_hpc/compoundI_ir_anharmonic_hpc20_v2/1/sha256sums.txt`

## Evaluator alignment

- Key-point IDs: `kp_ar_structure, kp_ar_validation, kp_ar_ir, kp_ar_uv`
- Conclusion IDs: `con_ar_agreement, con_ar_interpretation`
- Scoring-rule IDs: `r_ar_structure, r_ar_validation, r_ar_ir, r_ar_uv, r_ar_con1, r_ar_con2`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_structure` → reference `kp_ar_structure`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_validation` → reference `kp_ar_validation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_ir` → reference `kp_ar_ir`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_uv` → reference `kp_ar_uv`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_con1` → reference `con_ar_agreement`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_con2` → reference `con_ar_interpretation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_structure` / reference `kp_ar_structure` / field `$.structure_validation.formula` / result path `$.structure_validation.formula` = `"C18H12N2S2"`
- rule `r_ar_structure` / reference `kp_ar_structure` / field `$.structure_validation.stereochemistry_verified` / result path `$.structure_validation.stereochemistry_verified` = `true`
- rule `r_ar_validation` / reference `kp_ar_validation` / field `$.candidate_coverage.stopping_reason` / result path `$.candidate_coverage.stopping_reason` = `"The fixed molecule was optimized and frequency-validated, all four requested IR assignments and two requested UV-visible bands were obtained, and the stated isolated-molecule diagnostic scope was complete; no additional candidate identit..."`
- rule `r_ar_validation` / reference `kp_ar_validation` / field `$.stationary_point.evidence` / result path `$.stationary_point.evidence` = `"Gaussian normal termination and frequency-validation records in source_evidence.raw_hpc_dirs"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].assignment` / result path `$.ir_results[*].assignment` = `"C-S stretching"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].assignment` / result path `$.ir_results[*].assignment` = `"C=C stretching"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].assignment` / result path `$.ir_results[*].assignment` = `"C=N stretching"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].assignment` / result path `$.ir_results[*].assignment` = `"C-H stretching"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].experimental_comparison` / result path `$.ir_results[*].experimental_comparison` = `"computed=840.6081 cm-1; experimental=840.0 cm-1; absolute_error=0.6081000000000358 cm-1"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].experimental_comparison` / result path `$.ir_results[*].experimental_comparison` = `"computed=1554.668 cm-1; experimental=1551.0 cm-1; absolute_error=3.6679999999998927 cm-1"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].experimental_comparison` / result path `$.ir_results[*].experimental_comparison` = `"computed=1613.0319 cm-1; experimental=1605.0 cm-1; absolute_error=8.03189999999995 cm-1"`
- rule `r_ar_ir` / reference `kp_ar_ir` / field `$.ir_results[*].experimental_comparison` / result path `$.ir_results[*].experimental_comparison` = `"computed=1460.7571 cm-1; experimental=1450.0 cm-1; absolute_error=10.757100000000037 cm-1"`
- rule `r_ar_uv` / reference `kp_ar_uv` / field `$.uv_results[*].wavelength_nm` / result path `$.uv_results[*].wavelength_nm` = `276.78`
- rule `r_ar_uv` / reference `kp_ar_uv` / field `$.uv_results[*].wavelength_nm` / result path `$.uv_results[*].wavelength_nm` = `373.7`
- rule `r_ar_uv` / reference `kp_ar_uv` / field `$.uv_results[*].transition_character` / result path `$.uv_results[*].transition_character` = `"higher-energy pi-to-pi-star manifold; the Gaussian dominant configurations and archived NTO calculation are the evidence, while no numerical CT index is claimed"`
- rule `r_ar_uv` / reference `kp_ar_uv` / field `$.uv_results[*].transition_character` / result path `$.uv_results[*].transition_character` = `"lowest bright transition; Gaussian dominant configurations and NTO output support the paper's delocalized/charge-transfer interpretation only qualitatively"`
- rule `r_ar_con1` / reference `con_ar_agreement` / field `$.conclusion` / result path `$.conclusion` = `"The exact public B3LYP/6-311+G(d,p) follow-up is complete. All four IR assignments are numerically close to Table 4 (<=11 cm-1); the two visible/UV bands are within 15 nm of the experimental bands. Dominant configurations/NTO output prov..."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Exact neutral singlet Compound I identity, stereochemistry, formula and requested diagnostic observable classes.

Public input files and hashes:

- `agent_input/data/inputs/compound_I.json` — SHA-256 `9fe92387dd5a71950732a0b7b9b56e8ae56024dbfb91ddc4d17c32496aea631e`; size=502 bytes; explicit_boundary_fields={"$.charge": 0, "$.formula": "C18H12N2S2", "$.multiplicity": 1, "$.smiles": "N#C/C(=C(\\c1ccc(N=CH/c2cccs2)cc1)c3cccs3)"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_4fa592965be9841e/verification_report.md` — verification record; SHA-256 `9030368e0ba6c6794626a10878662298bed13d8a92c7d517910ca76df006b473`
- `docs/verification/group_3/paper_4fa592965be9841e/report/results.json` — verification record; SHA-256 `a9de1987b8c4dc776310a668e764e17638fe8dd627ecdcd76b7cd5d30500fbdd`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
