# Verified computation reference — paper_8b7bf002cc6a4ba9 (paper_reproduction)

> Evaluator-private, manually curated provenance; not an agent input or scoring standard. Updated 2026-09-15 by read-only examination of existing outputs. Original group files were not changed.

## Current finding

**The full conformer-stability/dipole conclusion is not established by the inspected author-route chain.** Four implicit-water ORCA Opt/Freq calculations are valid. The subsequent four explicit-water xTB optimizations are not converged; later successful single points do not repair those geometries. This is a concrete scientific-chain defect, not a public-starter replay requirement.

This record supersedes the earlier “Current successful author-route closure” paragraph. That paragraph incorrectly treated xTB termination as optimization convergence, called CPCM(water) dipoles gas-phase values, and labelled atomic-unit dipoles as Debye. It also inferred conformer identities from initial filenames. No evaluator target or scientific scope has been changed to conceal these discrepancies.

## Paper/SI basis and task boundary

Dong Wook Kim et al., *ACS Nano* **2026**, 20, 6081–6093, DOI 10.1021/acsnano.5c19783.

- [Main PDF](../../../../papers/paper_8b7bf002cc6a4ba9/documents/main.pdf), PDF p.3 / journal p.6083: the reported qualitative outcome is folded AL, extended AB, and a larger dipole for the latter. These are hidden targets, not public inputs.
- Main PDF p.10 / journal p.6090, “Theoretical Calculation”: initial MMFF94/Avogadro candidates → B3LYP-D4/def2-TZVP/CPCM(water) optimization → 50 waters with Packmol → GFN2-xTB optimization → ORCA single points. The conformer comparison uses **E(complex) − E(corresponding water network)**, not the whole-water-cluster total energy alone. The final single-point level is not separately repeated in the paragraph; reusing the earlier level is a disclosed implementation assumption.
- [SI](../../../../papers/paper_8b7bf002cc6a4ba9/documents/supplementary_001.pdf), PDF p.7 Fig. S5 and p.9 Fig. S7, inspected as figures: the paper displays three AL and four AB conformers and molecular dipoles in Debye. The four local candidates are not automatically those seven author-labelled conformers; no extra seven-member requirement is added to the current task.
- Public molecular identities are zwitterionic AL `[NH3+]CCC(=O)[O-]` and AB `[NH3+]CCCC(=O)[O-]`, neutral overall singlets. PR may receive the author hypothesis/route, but not optimized endpoints, calculated rankings or dipoles. Both modes require validated molecular identities, an aqueous model, within-molecule energies, and explicitly defined dipoles.

## Effective successful computation steps

### 1. Candidate construction and implicit-water Opt/Freq

The historical candidate IDs encode attempted folded/extended starts; an endpoint must be described from its geometry, not its filename. The actual input and output files below establish the implemented ORCA B3LYP-D4/def2-TZVP/CPCM(Water) protocol (not gas phase), optimization convergence, completed frequencies and zero imaginary frequencies.

- **AL_folded**: [input](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_edd329f28d9a47ec9fc286ff5c5ca242/al_folded_optfreq_serial_retry.inp), [Opt/Freq output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_edd329f28d9a47ec9fc286ff5c5ca242/stdout.log), [optimized solute](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_edd329f28d9a47ec9fc286ff5c5ca242/al_folded_optfreq_serial_retry.xyz).
- **AL_extended**: [input](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_74865d5774c948c58bd3f210e7e8f1e8/al_extended_optfreq.inp), [Opt/Freq output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_74865d5774c948c58bd3f210e7e8f1e8/stdout.log), [optimized solute](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_74865d5774c948c58bd3f210e7e8f1e8/al_extended_optfreq.xyz).
- **AB_folded**: [input](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_eca228023eb5475b84e90d0b9e80945b/ab_folded_optfreq_serial_retry.inp), [Opt/Freq output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_eca228023eb5475b84e90d0b9e80945b/stdout.log), [optimized solute](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_eca228023eb5475b84e90d0b9e80945b/ab_folded_optfreq_serial_retry.xyz).
- **AB_extended**: [input](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_1c9990ab759443f9be9463e769f6d103/ab_extended_optfreq_serial_retry.inp), [Opt/Freq output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_1c9990ab759443f9be9463e769f6d103/stdout.log), [optimized solute](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_1c9990ab759443f9be9463e769f6d103/ab_extended_optfreq_serial_retry.xyz).

### 2. Extract properties of those same implicit-water minima

Read the final electronic energy and thermochemistry from each Opt/Freq output. For dipoles use the explicitly printed **Magnitude (Debye)**, not the preceding vector or **Magnitude (a.u.)**. The old `validation.json` Debye field names are erroneous; they remain unchanged in the source archive.

| Candidate | Electronic energy / Eh | Gibbs energy / Eh | Molecular dipole / Debye | Shortest terminal N···O / Å |
|---|---:|---:|---:|---:|
| AL_folded | -323.747205378808 | -323.66735872 | 14.620695228 | 2.584651 |
| AL_extended | -323.737901422754 | -323.65847391 | 21.369550129 | 4.234205 |
| AB_folded | -363.052590913947 | -362.94677402 | 14.886720073 | 2.564431 |
| AB_extended | -363.039991769228 | -362.93432832 | 26.981347392 | 5.177330 |

Within each molecule, compute relative energy as `(E(candidate) − min E(validated candidates)) × 627.509474` kcal/mol. These implicit-water electronic energies prefer folded AL by about 5.8383 kcal/mol and **folded AB by about 7.9061 kcal/mol** over the respective extended candidates. Gibbs energies give the same two preferences. A valid alternative-model result is not evidence that the explicit-water author ranking has been reproduced.

The molecular dipoles for a preselected extended AB and folded AL do have AB > AL, but this does not prove that those two are the lowest conformers under one coherent validated model. This stage supplies valid candidate/minimum/property evidence, not the full final claim.

## Downstream diagnostics excluded from the successful scientific chain

### Unconverged explicit-water precursors

Packmol generated 50-water starts, but each subsequent xTB output explicitly reports failed geometry convergence. The existence of `xtbopt.xyz`, a total energy, or a successful wrapper status is insufficient.

| Initial candidate label | Application failure marker | Endpoint identity diagnostic | Evidence |
|---|---|---|---|
| AL_folded | FAILED TO CONVERGE GEOMETRY OPTIMIZATION IN 498 ITERATIONS | compact; N–H=2, O–H=1 | [raw output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_1ade6d286c4e44c19e7ccec838ca9cd0/stdout.log) |
| AL_extended | FAILED TO CONVERGE GEOMETRY OPTIMIZATION IN 498 ITERATIONS | fragmented; N–H=3, O–H=0 | [raw output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_e99d76c1b78f4b48a10b6644324490be/stdout.log) |
| AB_folded | FAILED TO CONVERGE GEOMETRY OPTIMIZATION IN 498 ITERATIONS | compact; N–H=2, O–H=1 | [raw output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_858d7c43af674fd3a1873aa51265d486/stdout.log) |
| AB_extended | FAILED TO CONVERGE GEOMETRY OPTIMIZATION IN 527 ITERATIONS | compact; N–H=2, O–H=1 | [raw output](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/native_workspace/outputs/execution_jobs/job_678f2668ca3c4cf49f34682ec997e628/stdout.log) |

AL_extended also has broken heavy-atom connectivity. The other three endpoints have NH2/COOH contacts rather than the requested NH3+/COO− form. In particular the file labelled AB_extended is compact at its final geometry. These structures cannot be counted as four validated zwitterionic conformers. See the paired geometry/atom-index diagnostics in [the existing audit](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/artifacts/alab_author_sp_audit_20260915.json); the distance diagnostic is not a new scoring threshold.

### Completed paired single points: arithmetic only, not a repaired conformer chain

All eight ORCA single points exist and terminate normally. At each fixed, unvalidated precursor geometry, the calculation `E(complex) − E(water network)` can be reconstructed. Values below are local computed diagnostics, **not paper targets or validated conformer rankings**.

| Initial label | E(complex) / Eh | E(water) / Eh | Difference / Eh | Within-molecule relative difference / kcal mol−1 | Raw outputs |
|---|---:|---:|---:|---:|---|
| AL_folded | -4145.879465775113 | -3822.133727900158 | -323.745737874955 | 0.000000 | [complex](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/al_folded_complex_author_sp_20260914/20260915T080601_820524_2343170/orca_stdout.log), [water network](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/al_folded_water_network_author_sp_20260914/20260915T081130_831587_2504742/orca_stdout.log) |
| AL_extended | -4145.865412334043 | -3822.141166864354 | -323.724245469689 | 13.486688 | [complex](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/al_extended_complex_author_sp_20260914/20260915T081246_758379_2544361/orca_stdout.log), [water network](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/al_extended_water_network_author_sp_20260914/20260915T081547_582574_2628185/orca_stdout.log) |
| AB_folded | -4185.203354610122 | -3822.153674759046 | -363.049679851076 | 4.358680 | [complex](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/ab_folded_complex_author_sp_20260914/20260915T081741_592550_2679145/orca_stdout.log), [water network](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/ab_folded_water_network_author_sp_20260914/20260915T081932_241969_2732171/orca_stdout.log) |
| AB_extended | -4185.207209411223 | -3822.15058356071 | -363.056625850513 | 0.000000 | [complex](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/ab_extended_complex_author_sp_20260914/20260915T082210_339198_2805230/orca_stdout.log), [water network](../../../../docs/verification/group_5/paper_8b7bf002cc6a4ba9/provenance/local_tests/recovery_20260914/ab_extended_water_network_author_sp_20260914/20260915T082314_727482_2836127/orca_stdout.log) |

A single point cannot establish a minimum or restore lost protonation/connectivity. The printed cluster dipoles include the 50 waters and cannot be substituted for the solute-only dipoles in Fig. S7. Nor may these differences be combined with implicit-water precursor dipoles and then described as properties of the same final conformer/model.

## Evaluator alignment and remaining decision (D5)

- Molecular identity, candidate-generation and implicit-water minimum/property evidence exist.
- The inspected chain does **not** support the current folded-AL/extended-AB lowest-conformer conclusion in a consistent validated aqueous model. This remains a release hold for both modes when claiming successful author-conclusion verification.
- The public task permits an aqueous-model choice while the evaluator expects a specific conformer trend. The authoritative primary energy/model and solute-dipole convention still need a declared, scientifically justified boundary. Preserve the goal and hidden answers; do not replace the author formula with whole-cluster totals or silently switch the target to folded AB.
- Recommended next maintenance action: decide the primary comparison definition from the paper, inspect any separately existing converged, identity-preserving paired evidence against that definition, and only then assess closure. No new calculations are requested or initiated by this record. If such evidence is absent, preserve this explicit gap.
- Source `report/results.json` is a placeholder and `report/validation.json` (2026-09-11) has the convergence/unit errors above. Neither a newer timestamp nor a PASS label would supersede raw application and identity checks.

## Input isolation and archive policy

Only `agent_input` may be exported. This file, author figures, private results and group outputs must remain evaluator-private. The molecule-only public input contains no final coordinates; that package boundary alone is not proof of actual runtime filesystem/network isolation.

Failed optimization/scheduler records are retained in their original group locations and in Git history, not presented as successful scientific steps. A successful retry may be part of the chain when the application output establishes its validity. Author endpoints are legitimate private verification inputs; replay from current public starters is not required.
