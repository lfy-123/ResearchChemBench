# Verified computation reference — paper_08c040bf4e456891 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Current author-subroute verification — 2026-09-15

The current scoped scientific result is **PASS**, superseding the partial snapshot below. This is an author-route feasibility check, not a replay of an autonomous agent or the LLM evaluator. No public task, scoring rule, reference target, or scientific scope was changed by this update.

- PBE0/def2-TZVP endpoint optimizations/frequencies, the C–Cl scan, the C–F rearrangement NEB, and six canonical CCSD(T)/cc-pVTZ endpoint refinements are complete.
- AIE = **11.818697804709 eV**; Cl-loss appearance energy = **12.128477772882 eV**; F-loss appearance energy = **13.374863779679 eV**. The original and final PR/AR schemas and 12 numeric comparisons pass.
- The 10-image NEB converged at iteration 28. Population single-points on actual images 2 and 9 confirm neutral departing F and the cationic residual fragment; the earlier scan endpoint is not substituted for the NEB geometry.
- Limits: this does not assert a unique global MEP, reproduce every intermediate barrier in the paper, or cover channels outside this task.

Current immutable evidence anchors:

- [Complete route and numeric evidence](../../../../docs/verification/group_5/paper_08c040bf4e456891/artifacts/author_path_closure_20260915.json), SHA-256 `607d2018d112a882257cb53d0d091a2503a46b7062f2be5bff24ffef1384d86f`.
- [Evaluator-scoped qualification](../../../../docs/verification/group_5/paper_08c040bf4e456891/provenance/evaluator_scoped_qualification_20260915.json), SHA-256 `a2ef3996dc2a0e17020b6219db12fba61ca5fea64ca28d84489282b66b263a5f`.
- [Step-by-step continuation and timing](../../../../docs/verification/group_5/paper_08c040bf4e456891/CONTINUATION_20260915.md).

## Historical status — superseded by the closure above

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `bounded_failure` (PARTIAL_OR_BOUNDED)
- Verification-report terminal status: `NOT_RECORDED` (NOT_ESTABLISHED)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

## Source identity

- Paper: Electron-impact ionization of CClF3 and CHClF2: absolute cross sections and fragmentation dynamics
- DOI: `10.1039/d5cp04305k`
- Task package: `tasks/final_verified_autonomous_research/paper_08c040bf4e456891`
- Verification group: `docs/verification/group_5/paper_08c040bf4e456891`
- Paper documents: `papers/paper_08c040bf4e456891`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "available_results": {
    "aie_eV": 11.897307686279502,
    "cation_energy_Eh": -697.886685737737,
    "chf2_cation_energy_Eh": -237.869091622887,
    "chfcl_cation_energy_Eh": -598.151341640238,
    "chlorine_atom_energy_Eh": -459.997459007071,
    "chlorine_loss_partial_appearance_eV": 12.445211881160734,
    "chlorine_loss_partial_dissociation_eV": 0.5479041948812313,
    "endpoint_note": "molecular product fragment endpoints and continuous path validation remain incomplete",
    "fluorine_atom_energy_Eh": -99.676203995184,
    "fluorine_loss_partial_appearance_eV": 13.506591853001334,
    "fluorine_loss_partial_dissociation_eV": 1.6092841667218318,
    "neutral_energy_Eh": -698.323903730923
  },
  "computational_approach": {
    "energy_method": "PBE0/def2-TZVP electronic energy",
    "geometry_method": "PBE0/def2-TZVP Opt Freq",
    "justification": "C-Cl is tested as a direct scan; C-F is explicitly provisional because the author route indicates rearrangement.",
    "path_methods": [
      "relaxed one-coordinate C-Cl scan",
      "relaxed one-coordinate C-F scan"
    ]
  },
  "conclusion": "The independently computed AIE is available, but neither named appearance-energy channel is yet validated end-to-end; no paper-level conclusion is assigned.",
  "limitation": "Scans and product-fragment optimizations are not all terminal; the F-loss multidimensional rearrangement/MEP and complete separated endpoint evidence are missing.",
  "method": {
    "route": "PBE0/def2-TZVP independent route",
    "software": "ORCA 6.1.1"
  },
  "status": "bounded_failure"
}
```

Paper/SI document hashes:

- `papers/paper_08c040bf4e456891/documents/supplementary_001.pdf` — SHA-256 `244202bb0e6e7310b3a23ad4c1e44990fde298e1aee9bbedd2ef4eacf8a53a28` (declared_match=True)
- `papers/paper_08c040bf4e456891/documents/main.pdf` — SHA-256 `ecd1daa94317b58da01a92d3edd52693d35e4b9cce4a5515a5f1ef3fd7f52a9f` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **130**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/status.json` — successful status record; SHA-256 `a0cff56174823fcc4fc689a4956aa71096897a2eba952bd26875574c5360756d`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.inp` — successful execution artifact; SHA-256 `6fd732e2ce02fe5ed250c518c2cf968149dda77e6fec4757280af4ed025d3d0c`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.xyz` — successful execution artifact; SHA-256 `706b874c156c6042761b6202e0eb06b57cecd7ae61168e3d194fa8cee47cb084`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry_trj.xyz` — successful execution artifact; SHA-256 `23a5a8cec72382be7add2c36190f54cbec64e0c174796ea181f02af3cbdd35c2`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/collection.json` — successful execution artifact; SHA-256 `bd28db5f5d175296a5f19c3a02caf0e100a3341225c9737163bebf604d09ff4e`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/status.json` — successful status record; SHA-256 `81db9cf1cfa06c656ce68d933dcea834b55756fc0b52a1235968cfdad31f35cd`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/chlorine_atom_product_sp.inp` — successful execution artifact; SHA-256 `9bf374d1d3ef08f85568ab7f0aec3cc59cc988dc9c1eb7069f1846d69d1fd836`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/collection.json` — successful execution artifact; SHA-256 `9ca98be51a83797a01b03df3c5b093e8e5d45e3d300c399bc2c441b90076a2d8`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/request.json` — successful execution artifact; SHA-256 `4506375c0e266f7f93e2d228991596e7da9b80199c43e91126bf0cfbdafd3b10`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/status.json` — successful status record; SHA-256 `f37123574776a592777de36b9d2a47f6d15d7e061fc33729023e4353fa088540`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.001.xyz` — successful execution artifact; SHA-256 `2c00a244e16c6fef224a15a1abc14c6521394293f5cc9d73b4c7d3dad1e4369c`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.002.xyz` — successful execution artifact; SHA-256 `5bc607c86d72c80a82c195544bee55604aa955ada42f2c2e76d2b88953d7627f`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.003.xyz` — successful execution artifact; SHA-256 `24bd5239179b9529c071a5b77daadf7f348b6e850035d14216eb2d5853b115c6`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.004.xyz` — successful execution artifact; SHA-256 `767e542ce6bc8aec2fa59969d982be7b1b359545dacca0c2a478ab7ab90c4677`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/status.json` — successful status record; SHA-256 `51542c64cd45431a4747494494d49528d579a51162f6ea8f6ed38afe43128b7d`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/chclf2_neutral_pbe0_def2svp_sensitivity.inp` — successful execution artifact; SHA-256 `3bd746b370de293a7bb45e016051770c8931cfe2fbf0d6a9ba4db076ab8f23ea`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/collection.json` — successful execution artifact; SHA-256 `3c2819308523c1695b0b362c93798bfadd5ca37a2dda44cdb7e16995ef6ac82f`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/request.json` — successful execution artifact; SHA-256 `743c816726542eb01cd70ddb2d9e3cc989b4aca5351dcd788e9122a2c2ee0da6`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/status.json` — successful status record; SHA-256 `5eb8791d62b23e1e282e750bbeeeecd9f94c5d0e895055c7705d4d48934e9e77`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.inp` — successful execution artifact; SHA-256 `cd941c4269dd08849a3cb0605d549adddc3d1efc7737a44b68050cbf19f19a74`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.xyz` — successful execution artifact; SHA-256 `f07a523cb4f56500c95c0a742eb07b531486b834d985769efabec5007587c758`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry_trj.xyz` — successful execution artifact; SHA-256 `d6212bd5e67b6bb28e7b063775c64816ff215be6f97e0cbf00567ac037f3f694`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/collection.json` — successful execution artifact; SHA-256 `91f98544e18fd6d43fbea41bd661f51367a1cc4ba9f78b41be5d21c1ea2cbb20`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/status.json` — successful status record; SHA-256 `a0dd405842d4576e257164b837b2bc4c50aeb9c01c746bb7d67d5fb032dc3f87`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.001.xyz` — successful execution artifact; SHA-256 `ba16b55fc15a6b54a936ba0844dd383ea812ac90ee106f5475212e54f0008847`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.002.xyz` — successful execution artifact; SHA-256 `c100cf7e6a737c4080a37e7cc9d1d01841642df4eff3451e21308957120a6a34`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.003.xyz` — successful execution artifact; SHA-256 `924d53591e6d3580bfed2effaa082a4a89317e4340fe819f54880962a0fa639a`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.004.xyz` — successful execution artifact; SHA-256 `7d70de32bafe310aeb99c014b093c99cc2076a323e72230d802a674bca4fa55a`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/status.json` — successful status record; SHA-256 `aa8c0766067ed41e9e321e06d1c5cbc6569b1037f6a69e05a6c2918966ba66f4`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.inp` — successful execution artifact; SHA-256 `2c708881f6a20f8b93232aa9238bf7bed174bdac1c538958534200209f5d544c`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.xyz` — successful execution artifact; SHA-256 `be1b7c33a3e822758ac4f1b691575548d639dd3df2dc5deb9cd9ba00de2cd06c`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry_trj.xyz` — successful execution artifact; SHA-256 `c4fbc0603e90dff61c4ee07572dcff5a6eced1203897c7f235493b233b8ed684`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/collection.json` — successful execution artifact; SHA-256 `acfd31b3b79842d9f239d4021a236372161c7f574334e904e6c5ef1b97443812`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/status.json` — successful status record; SHA-256 `44e16115e85d596a1f77c02379da3d2c1c711a84161bd9b836b26bf74aba9096`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.inp` — successful execution artifact; SHA-256 `0d5e847596b074c103527c2f44bd3f4cc82ada57fe1b1008a9af09a86ce69992`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.xyz` — successful execution artifact; SHA-256 `c63492ed46c6e988e3ba377a59bac3690286322e283895e5af1204342cabe08c`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry_trj.xyz` — successful execution artifact; SHA-256 `23a3b98bc4a77244a7f5c6c344d261d4072d80dfbaa8dec19654b0318923c186`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/collection.json` — successful execution artifact; SHA-256 `1ce696b284403fdb0b216275d44da680cc175d17cc0bdc99d0ed77c7c7da6e08`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/status.json` — successful status record; SHA-256 `3be1c57f4a7f6e0824c764e52eb721f6564d02976ee04f6c7676474437b58d6e`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/chclf2_cation_pbe0_def2svp_sensitivity.inp` — successful execution artifact; SHA-256 `160c5713d80570f1459c9e38e344e8990da912a38fff59fe15bee6beee422d0d`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/collection.json` — successful execution artifact; SHA-256 `155427e6ddbc09bf22554d9a371919f5496a36c72b6a80c9800cece385b01a84`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/request.json` — successful execution artifact; SHA-256 `3c584c225be3e048f44d6faff98595e4b0308912ccb42236436018f6730fbcdd`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/status.json` — successful status record; SHA-256 `9d2ff3d1c494dbeaaac73a2186ff3935d9e66a6b33b1acfabfbc5cc56ab173df`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/collection.json` — successful execution artifact; SHA-256 `433ffe821ded2ce44977d186cc11b0fae78c0cc3aaaa9d5cde177d449529e22e`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/fluorine_atom_product_sp.inp` — successful execution artifact; SHA-256 `e37b8d91ec48928b3efd8085b6dc83bd45c35272835dcb22022b507a76ba72c1`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/request.json` — successful execution artifact; SHA-256 `c127633f3ac42073a0964d39f3d235094d024be015a173c2fb8367489894439e`
- `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/status.json` — successful status record; SHA-256 `48669fb304d075e11feaaf425b00de215c736ddbb223b9071e6a4835a86faced`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/case.json` — successful execution artifact; SHA-256 `49d11a1c4e8312d754c3b30980e52db6f534827f5cdc82c66b0e1e0a77e09c6b`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/input.inp` — successful execution artifact; SHA-256 `6972b580e3db7032a1a8fa0ae468a7c98aef7d0931b4b1f74c1cab00ed86ab0f`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/orca_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/orca_stdout.log` — successful execution artifact; SHA-256 `825fd83955dffa11e145ad2a7f163d08c7d585564fc50ffc9ee87ee4b27741bc`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/status.json` — successful status record; SHA-256 `9e3ae20fd8b8cbd576808d88332e3b4e67d418468fabd63497916eaac71641a0`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/case.json` — successful execution artifact; SHA-256 `c07b0250a25aafcddb606456924207bdd067e068c3f756c61fda8fd6828dc237`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/input.inp` — successful execution artifact; SHA-256 `3d3ab12314d4978b91aa35b519edf0cfb043dc1355875d484daad46ffa900fa9`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/orca_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/orca_stdout.log` — successful execution artifact; SHA-256 `41d8d3e9f6f0c4157ae6af46b53ea5dcb30576c2c2ee6dfdc45a8e3163c49e72`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/status.json` — successful status record; SHA-256 `ccb7f9ff5a33d02680355249d1bbce08d2cc31dcc19e091d8a4acf683a8c659a`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/case.json` — successful execution artifact; SHA-256 `9b7cf1f1b487f791ee7bf4488dde7e33ab529fbd8f02dfbf4ae114d04297b73f`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/input.inp` — successful execution artifact; SHA-256 `744f7cfdd6abc24787f70a78a6633c0b5047c461fd4cfed16933e5c8dd0e597a`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/orca_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/orca_stdout.log` — successful execution artifact; SHA-256 `6a335b9d6a344cf2a038eb7d02aa43bd3a7f76eb70ec0ab8dbc192512ac55702`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/status.json` — successful status record; SHA-256 `2a4805dbca5c2045af3a97dcda7a059ef52c154fc67349afd2516d3ce4ad3bb0`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/case.json` — successful execution artifact; SHA-256 `c95a5b0b64d59979cb3586cf489ed8108e309b8ac8510a7639c15b884e114be2`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/input.inp` — successful execution artifact; SHA-256 `31e604c8d616618d96ad3918a5a9ec81a7a81ea9a0862964b5a135b02679c2db`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/orca_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/orca_stdout.log` — successful execution artifact; SHA-256 `7d0bfe31b7780deedb37b3c6f85c237509ab77805a6fa386f2e4d60e2085a047`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/status.json` — successful status record; SHA-256 `b6fae01bd8e12b59681c435813837aa8c0944e430ec25930334387fc81d80bb6`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/case.json` — successful execution artifact; SHA-256 `ca72367e22d5e91a46f453cdff85a856183d476410ec75bcdcdb4574552ab724`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/input.inp` — successful execution artifact; SHA-256 `e6b9b51f6f64f6545af9c37b1663edb9d3416d6da3da45179b5a2b08cae97bce`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/orca_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/orca_stdout.log` — successful execution artifact; SHA-256 `11144f21f5f777ea887f20eb925d90366ae4c3060e473e3258a55428c77e0cac`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/status.json` — successful status record; SHA-256 `0095d3178eb44af610c03fbddfd01646783dd321c816af79e9cb14d0b8e86aa1`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/case.json` — successful execution artifact; SHA-256 `2032f22294852b5a9ba2dfb9b1975561a70bd57cfe4b124e890772427441ee63`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/input.inp` — successful execution artifact; SHA-256 `d618ca02b4765c5e2cddf205dcdeca5c5ba8da62397cc7dd2669ab94928d4b8d`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/orca_stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/orca_stdout.log` — successful execution artifact; SHA-256 `0422b67c1e0dc7427d881d0e6ca4d288b0b343f88b4a8efb4ae01ef38cfda895`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/status.json` — successful status record; SHA-256 `79ff7a4d4384fde38bf1521ded1fa0d3d0d4e2918892df8408686aae13524089`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.001.xyz` — successful execution artifact; SHA-256 `874693c9a7d1044cbbe0ff68997a729e4e97d9cea6b9671cbc1d0b1a9bb18c2c`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.002.xyz` — successful execution artifact; SHA-256 `92e9289fe6f2285286f8c6a28525e1d1fb3c4a981e067a72c69d96bd31f83640`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.003.xyz` — successful execution artifact; SHA-256 `b1ec1f53a669bd9c2cf83666c8e78fce33cb327cb78026cab6bb44cb7127b6fe`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.004.xyz` — successful execution artifact; SHA-256 `3dd1d07f093f39a67fb08648decef76991414f709e0ea4d2a0b9439b3661dca0`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/status.json` — successful status record; SHA-256 `729a5ed1b29d5c544d798672eebc0b6c9643889fa50c8bc4fa9aa06729fcbaa7`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.001.xyz` — successful execution artifact; SHA-256 `b8e64f0df0b7787eafb6461cb827fd1d8eea4d3ad3514bef918eb01fab8e65c0`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.002.xyz` — successful execution artifact; SHA-256 `5c266a8ca35fca35b6aa93347f49f37d6bec7190996e576f99c0a2847557d23e`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.003.xyz` — successful execution artifact; SHA-256 `c30406e2bec1ca48630b1e135e1efdad29aa544eb70dcf3bea71e861926a82db`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.004.xyz` — successful execution artifact; SHA-256 `24042ec1280d684bff2d3e46f4142914e8e8256c3152014bd208a7a52e3bb67b`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/status.json` — successful status record; SHA-256 `f4761e9c9b0e0fa77c809630f24f0dc86838b122ad74e87eb73d92b25276c649`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.inp` — successful execution artifact; SHA-256 `777b43600fc280967e8aafeb14457300fd465432ef7fdcf13e257dea8c55754e`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.xyz` — successful execution artifact; SHA-256 `df1e7ce9e8ce029af26b66136059c664252802ec5551e337c0f7d9e33d06cb94`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input_trj.xyz` — successful execution artifact; SHA-256 `665d84a96d886bbce3609d40860fd095a1f8b850c9380c7c00076e7c4881d025`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/orca_stderr.log` — successful execution artifact; SHA-256 `21181101d409d49dbde6094ec970dbf28f8605e33948699b94b681ded88d1e47`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/status.json` — successful status record; SHA-256 `5661843851ae959f37cf596a87a7866c258ca7af53e93085e23e55e7fd3bd66d`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.inp` — successful execution artifact; SHA-256 `ae56ba80284603faa258dbea1bd88cd2f762af0f1415fb0ea0286b0ef8a3fdd3`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.xyz` — successful execution artifact; SHA-256 `149533d5a6cfbe41f6c09b2bb1b68a7a365eccdeb0945829276d34092d5622cc`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input_trj.xyz` — successful execution artifact; SHA-256 `0e656f22dea0d6db6ecec98b61bf32466ebbdebea3e68981e7a1b516d8644869`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/orca_stderr.log` — successful execution artifact; SHA-256 `427eecbd0cffd613e2ecb1fafbf4039a07ab79b5f9c45f9ac306a8bfa381f224`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/status.json` — successful status record; SHA-256 `ad229ee81aad043d97ca4914373e85e8c12e13226cc0fcbdba0d656782b3f639`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.inp` — successful execution artifact; SHA-256 `74793cd5022f7d78fc4380df601e5a29e414592e7a318eeda648fa2843e56ce8`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.xyz` — successful execution artifact; SHA-256 `cdbe00268baa33d420c8729c27c9d1fed180c35546d6fbf7ec2defa92de565b1`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input_trj.xyz` — successful execution artifact; SHA-256 `bb03676f63341ac54f6a87bb96e81d7bf8125b18c0cf1250b1a3ab987dd06c61`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/orca_stderr.log` — successful execution artifact; SHA-256 `927d03b1487a6112f739dc082bcfa698fc5d1b1416cd6e6cbc767ab6323e477e`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/status.json` — successful status record; SHA-256 `147d410fcdde43e609d4ac453d53bb5e7834b242d4009581aa3c51d355d8fd76`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.inp` — successful execution artifact; SHA-256 `677212a7b1519703c3c6e487b706df5ffca1e5bf470af4058c6c38b91cab8bc3`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.xyz` — successful execution artifact; SHA-256 `5c530cf4560850cc616997767ed3e298bcab725b6ba1c724366eafef1f6d045e`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input_trj.xyz` — successful execution artifact; SHA-256 `6c9d0949ed49ddac15e3f24901b69f1a97c3ce65b28379e9f28c602e927adc7a`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/orca_stderr.log` — successful execution artifact; SHA-256 `96402970b7a40bd2b87f89df1365f2b5889af2c943ee197ffbb3a9cb4dfbc1b1`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/status.json` — successful status record; SHA-256 `40c113f3a30177c1a539fe557b2af01cad144668e3949218df1115b08c44fa1d`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input.inp` — successful execution artifact; SHA-256 `9e69b92c9ce625c0ce260254810d684f2f579cd249f9ab9158d0aba057bf90bb`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/orca_stderr.log` — successful execution artifact; SHA-256 `d7853395aef0185ec4b09147b2ae7593de06b35f2be253cbad4aea7a4ccd9d49`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/orca_stdout.log` — successful execution artifact; SHA-256 `21e08c37c81161b545837a1f27299fbd390778ec95d206c26cb8046efe1dd81d`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/resource_adjustment.json` — successful execution artifact; SHA-256 `cb145311a6c5672ba021b1858862637bb3e9f7f2609cc671d25411609cdc451a`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/status.json` — successful status record; SHA-256 `113d1e992bd3a1474007d01a46cf68d7328658ace3561c4ce9360749a795d8ec`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input.inp` — successful execution artifact; SHA-256 `992f575dc7dbfcb6e574b317aceeafa95e482a9697cb251d168206caee71a4a7`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/orca_stderr.log` — successful execution artifact; SHA-256 `57afe225801866e5d338b1b088bf033a75414202b2cecba5adfe63333c9baa3d`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/orca_stdout.log` — successful execution artifact; SHA-256 `4d0cf5a49b1bb6db075352e2b50c161536bd9563cc46861131c242f7bbff77b8`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/resource_adjustment.json` — successful execution artifact; SHA-256 `48e5e4fb8dbabeb488e5c49f28d279776a3d0a75d319f39222c5899b5d738ce9`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/status.json` — successful status record; SHA-256 `0e0e533d42f0db9fb847ba4213966068564b035ef259f0a676c35eff6deba87d`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input.inp` — successful execution artifact; SHA-256 `1c186ec9cb38122f148b1f9ba2e592374b5f6d1c821636d45263369874189084`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/orca_stderr.log` — successful execution artifact; SHA-256 `50c725ee78602382a266ec8a5fa1943c933e6e5e0542b9d4710ed3e6398f58c9`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/orca_stdout.log` — successful execution artifact; SHA-256 `bfc5e0970caa334bd2a317fa4311160dae0988883aee0fbc5e30dbc4c71bb631`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/resource_adjustment.json` — successful execution artifact; SHA-256 `d14b58aaae22f692a47f3e3e40062fefa97c7f420885791db880aaa25725b85d`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/status.json` — successful status record; SHA-256 `cb01b774c908cf7226a5b91e435fe560e6193e47f387d1eb839bcac1363c9167`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input.inp` — successful execution artifact; SHA-256 `924074ae45ce0fbc411b0683ed77164875fb070664777810ef49485bcc1fc757`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/orca_stderr.log` — successful execution artifact; SHA-256 `aafd75e53d847aa70c3cbb7567cc8340f27fdac22085a0780ad0242cbb9b5daf`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/orca_stdout.log` — successful execution artifact; SHA-256 `854804206e6ea666576e5df9cf5138f42cd66c4b8541fe3fa5d7578a9db65058`
- `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/resource_adjustment.json` — successful execution artifact; SHA-256 `c9b78e4339a4e66c288b04c8f667ca47259d9b0365141bb8a29d0ae4819b6fbf`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/status.json` — label=group_5 paper_08c040bf4e456891 chclf2_neutral_optfreq_retry; submitted_at=2026-09-01T03:16:15.778238+00:00; software=orca; intent=optimization_frequency; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_98679c654e1a4770affb721033a24826/chclf2_neutral_optfreq_retry.opt`
2. `native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/status.json` — label=group_5 paper_08c040bf4e456891 chclf2_cation_optfreq_retry; submitted_at=2026-09-01T03:16:15.797780+00:00; software=orca; intent=optimization_frequency; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_df7c5d8641e645949ef1ebd0e427d244/chclf2_cation_optfreq_retry.opt`
3. `native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/status.json` — label=group_5 paper_08c040bf4e456891 chlorine_atom_product_sp; submitted_at=2026-09-01T11:02:29.797092+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/chlorine_atom_product_sp.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/chlorine_atom_product_sp.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/chlorine_atom_product_sp.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/chlorine_atom_product_sp.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/chlorine_atom_product_sp.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/chlorine_atom_product_sp.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/collection.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_5b39391da9c648aa89aa3704ae4984d7/request.json`
4. `native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/status.json` — label=group_5 paper_08c040bf4e456891 fluorine_atom_product_sp; submitted_at=2026-09-01T11:02:29.840530+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/collection.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/fluorine_atom_product_sp.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/fluorine_atom_product_sp.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/fluorine_atom_product_sp.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/fluorine_atom_product_sp.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/fluorine_atom_product_sp.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/fluorine_atom_product_sp.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_fbd0277a16e5448ab6793dff44c101e9/request.json`
5. `native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/status.json` — label=group_5 paper_08c040bf4e456891 chf2_cation_product_optfreq_spin_retry; submitted_at=2026-09-01T11:04:38.913566+00:00; software=orca; intent=optimization_frequency; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_16c124eb28e1497296adf0d83a551cf0/chf2_cation_product_optfreq_spin_retry.opt`
6. `native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/status.json` — label=group_5 paper_08c040bf4e456891 chfcl_cation_product_optfreq_spin_retry; submitted_at=2026-09-01T11:04:38.938785+00:00; software=orca; intent=optimization_frequency; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_cac64ebe3b5441d099b92a52866517a8/chfcl_cation_product_optfreq_spin_retry.opt`
7. `native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/status.json` — label=group_5 paper_08c040bf4e456891 chclf2_cation_pbe0_def2svp_sensitivity; submitted_at=2026-09-01T11:30:09.642378+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/chclf2_cation_pbe0_def2svp_sensitivity.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/chclf2_cation_pbe0_def2svp_sensitivity.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/chclf2_cation_pbe0_def2svp_sensitivity.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/chclf2_cation_pbe0_def2svp_sensitivity.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/chclf2_cation_pbe0_def2svp_sensitivity.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/chclf2_cation_pbe0_def2svp_sensitivity.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/collection.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_f543de3d5c3b49778ce37f1bb75d8fdf/request.json`
8. `native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/status.json` — label=group_5 paper_08c040bf4e456891 chclf2_neutral_pbe0_def2svp_sensitivity; submitted_at=2026-09-01T11:30:09.665692+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/chclf2_neutral_pbe0_def2svp_sensitivity.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/chclf2_neutral_pbe0_def2svp_sensitivity.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/chclf2_neutral_pbe0_def2svp_sensitivity.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/chclf2_neutral_pbe0_def2svp_sensitivity.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/chclf2_neutral_pbe0_def2svp_sensitivity.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/chclf2_neutral_pbe0_def2svp_sensitivity.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/collection.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_7e4a4b318cf74e48b5723ffa97cd355f/request.json`
9. `native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/status.json` — label=group_5 paper_08c040bf4e456891 chclf2_cation_f_loss_scan_server2_resume; submitted_at=2026-09-01T14:25:26.701682+00:00; software=orca; intent=geometry_optimization; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.001.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.001.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.002.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.002.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.003.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.003.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.004.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_b2bf2a658f1042eba5ed3dadbbc6a7f6/chclf2_cation_f_loss_scan.004.xyz`
10. `native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/status.json` — label=group_5 paper_08c040bf4e456891 chclf2_cation_cl_loss_scan_server2_resume; submitted_at=2026-09-01T14:25:27.216776+00:00; software=orca; intent=geometry_optimization; command=orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.001.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.001.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.002.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.002.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.003.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.003.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.004.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/native_workspace/outputs/execution_jobs/job_72ecfcb756094bca875861711234e2c6/chclf2_cation_cl_loss_scan.004.xyz`
11. `provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/status.json` — label=provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/status.json; command=.software_cache/installations/orca/6.1.1/orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/case.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chfcl_ccsdt_ccpvtz_20260914/20260914T115437_921832_3253075/orca_stderr.log`
12. `provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/status.json` — label=provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/status.json; command=.software_cache/installations/orca/6.1.1/orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/case.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_chf2_ccsdt_ccpvtz_20260914/20260914T115437_951918_3253073/orca_stderr.log`
13. `provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/status.json` — label=provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/status.json; command=.software_cache/installations/orca/6.1.1/orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/case.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_neutral_ccsdt_ccpvtz_20260914/20260914T115437_946668_3253069/orca_stderr.log`
14. `provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/status.json` — label=provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/status.json; command=.software_cache/installations/orca/6.1.1/orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/case.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_cl_ccsdt_ccpvtz_20260914/20260914T115632_374657_3291963/orca_stderr.log`
15. `provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/status.json` — label=provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/status.json; command=.software_cache/installations/orca/6.1.1/orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/case.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/local_tests/recovery_20260914/chclf2_f_ccsdt_ccpvtz_20260914/20260914T115636_329104_3293817/orca_stderr.log`
16. `provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/status.json` — label=provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/status.json; command=.software_cache/installations/orca/6.1.1/orca input.inp
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/case.json`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_ccsdt_ccpvtz_20260914/20260914T121717_686818_343/orca_stderr.log`
17. `provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/status.json` — label=provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.001.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.001.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.002.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.002.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.003.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.003.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_cl_loss_scan_hpc_downstream_20260909/1_20260909T212924213486289_260/input.004.gbw`
18. `provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/status.json` — label=provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.001.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.001.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.002.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.002.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.003.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.003.xyz`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_f_loss_scan_hpc_downstream_20260909/1_20260909T212923097094613_267/input.004.gbw`
19. `provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/status.json` — label=provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chclf2_cation_optfreq_smoke_hpc_missing16_20260909/1_20260909T210251910856126_421/input.inp`
20. `provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/status.json` — label=provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212926580365389_344/input.inp`
21. `provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/status.json` — label=provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chf2_cation_product_optfreq_local_smoke_20260909/hpc_20260909T212142577280864_3033360/input.inp`
22. `provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/status.json` — label=provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.engrad`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.hess`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chfcl_cation_product_optfreq_hpc_downstream_20260909/1_20260909T212923737018780_344/input.inp`
23. `provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/status.json` — label=provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212938349564754_267/input_sha256sums.txt`
24. `provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/status.json` — label=provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/chlorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577648946_3033363/input_sha256sums.txt`
25. `provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/status.json` — label=provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_hpc_downstream_20260909/1_20260909T212939914601321_421/input_sha256sums.txt`
26. `provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/status.json` — label=provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/status.json
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/finished_at`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input.bibtex`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input.densities`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input.densitiesinfo`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input.gbw`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input.inp`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input.property.txt`
   - output: `docs/verification/group_5/paper_08c040bf4e456891/provenance/qzcli_hpc/fluorine_atom_product_sp_local_smoke_20260909/hpc_20260909T212142577421775_3033362/input_sha256sums.txt`

## Evaluator alignment

- Key-point IDs: `ar_process_states, ar_process_paths, ar_aie, ar_r1, ar_r2`
- Conclusion IDs: `ar_final_energies, ar_final_interpretation`
- Scoring-rule IDs: `autonomous_research_ar_process_states, autonomous_research_ar_process_paths, autonomous_research_aie, autonomous_research_r1, autonomous_research_r2, autonomous_research_ar_final_energies, autonomous_research_ar_final_interpretation`
- Bound result-field status: **BRANCH_INAPPLICABLE_FIELDS_ONLY**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `$.channels, $.channels.chlorine_loss.appearance_energy, $.channels.fluorine_loss.appearance_energy, $.states, $.states.aie`
- Submission-schema branch selected for the archived result: `1`
- Verification-report status: `NOT_RECORDED` (NOT_ESTABLISHED); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `autonomous_research_ar_process_states` → reference `ar_process_states`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert condition check; evaluator_target_present=False
- rule `autonomous_research_ar_process_paths` → reference `ar_process_paths`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert condition check; evaluator_target_present=False
- rule `autonomous_research_aie` → reference `ar_aie`; type=numeric; unit=eV; tolerance=0.5; comparison=absolute difference; evaluator_target_present=True
- rule `autonomous_research_r1` → reference `ar_r1`; type=numeric; unit=eV; tolerance=0.5; comparison=absolute difference; evaluator_target_present=True
- rule `autonomous_research_r2` → reference `ar_r2`; type=numeric; unit=eV; tolerance=0.5; comparison=absolute difference; evaluator_target_present=True
- rule `autonomous_research_ar_final_energies` → reference `ar_final_energies`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `autonomous_research_ar_final_interpretation` → reference `ar_final_interpretation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `autonomous_research_aie` / reference `ar_aie`: target=11.9 eV; tolerance=0.5; numeric result leaves=[]; within_tolerance=None; applicability=not applicable to result branch
- rule `autonomous_research_r1` / reference `ar_r1`: target=12.4 eV; tolerance=0.5; numeric result leaves=[]; within_tolerance=None; applicability=not applicable to result branch
- rule `autonomous_research_r2` / reference `ar_r2`: target=13.5 eV; tolerance=0.5; numeric result leaves=[]; within_tolerance=None; applicability=not applicable to result branch

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `autonomous_research_ar_final_energies` / reference `ar_final_energies` / field `$.conclusion` / result path `$.conclusion` = `"The independently computed AIE is available, but neither named appearance-energy channel is yet validated end-to-end; no paper-level conclusion is assigned."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Explicit CHClF2 connectivity, atom order, state charges/multiplicities, channel endpoint identities, and 5-atom XYZ starter geometries.

Public input files and hashes:

- `agent_input/data/inputs/chclf2_cation.xyz` — SHA-256 `beb2d4b6fa22ed445a756673f11cf947164354eaceb2e83205345417e898ac7f`; size=208 bytes; xyz_atom_count=5; xyz_comment=CHClF2 cation starter geometry; atom order C H Cl F F; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/chclf2_dication.xyz` — SHA-256 `d0d6708bc009c3c5b1ec94709e335cb20e6dacdb9e1690cf4f77d554126074b4`; size=210 bytes; xyz_atom_count=5; xyz_comment=CHClF2 dication starter geometry; atom order C H Cl F F; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/chclf2_neutral.xyz` — SHA-256 `be0e97719cb38aa6513c50a636e7e9a2fab6ea454b4bd16ff465304c88697b4c`; size=209 bytes; xyz_atom_count=5; xyz_comment=CHClF2 neutral starter geometry; atom order C H Cl F F; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/system.json` — SHA-256 `4504c5e708236027a2b63f301233982ff23d296287886efe937909325f991fa0`; size=714 bytes; explicit_boundary_fields={"$.atom_order": ["C", "H", "Cl", "F1", "F2"], "$.connectivity": "FC(F)Cl with one H on C", "$.energy_unit": "eV", "$.states[0].charge": 0, "$.states[0].multiplicity": 1, "$.states[1].charge": 1, "$.states[1].multiplicity": 2}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_5/paper_08c040bf4e456891/verification_report.md` — verification record; SHA-256 `50a57e91a7bfefa4a42a7f25e21155d10e7c9d4cf0b88a388ad0e0975f8d963e`
- `docs/verification/group_5/paper_08c040bf4e456891/report/results.json` — verification record; SHA-256 `9802386d58d60dcb615e45fe84c793471dbec9bc3d6512e3f5e67248e4695a98`
- `docs/verification/group_5/paper_08c040bf4e456891/artifacts/independent_results.json` — referenced successful evidence; SHA-256 `f24b8a353a6321870880f0d51ac2ce82c8fa4002d6ae6aa1f46bf46b162d955f`
- `provenance/chclf2_dissociation_queue_manifest.json` — **not found at audit time** (reported evidence path; not found at audit time)

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
