# Verified computation reference — paper_84efbea3ab8e6e20 (paper_reproduction)

> Manually curated evaluator-private archive, updated 2026-09-15. It records existing effective computations and their scientific limits; it is not a scoring standard or an agent input. No group file was changed and no new scientific calculation was run for this update.

## Current scope and correction

The three ground-state calculations, excited-state energies, common near-S1 selection, SOC and real spin-resolved state-character analysis have inspectable successful evidence. **The author's specific CZ2B/T4 HLCT interpretation is not established by the inspected results.** A clearly evidenced alternative is already allowed by the current evaluator; reporting that alternative is different from declaring that the original HLCT claim has been reproduced.

This replaces the prior automatic scheduler snapshot and “Current spin-resolved state-character closure” text. In particular, the earlier sentence claiming that the listed populations show comparatively more Bpin electron character in CZ2B was incorrect: 0.0353 is smaller than 0.0897 and 0.0778 under that same diagnostic. No target, required state-character item, or scoring rule is weakened in this correction.

## Original source and approved benchmark boundary

Dong Ding et al., *Dyes and Pigments* **248** (2026), 113534, “Breaking the lifetime-efficiency trade-off in blue organic room-temperature phosphorescence through site-directed boronate engineering.”

- [Main PDF](../../../../papers/paper_84efbea3ab8e6e20/documents/main.pdf), PDF p.3: T1 charge reorganization and experimental PVA lifetimes; Fig. 1d/f gives CZ1B 3.96 s, CZ4B 4.27 s and CZ2B 5.20 s.
- Main PDF p.4, Fig. 2 and discussion: near-S1 window ±0.30 eV; strongest SOC at CZ1B/T3, CZ2B/T4 and CZ4B/T3; a qualitative core/Bpin-HLCT interpretation. Fig. 2b caption uses T1, whereas the paragraph discusses T3/T4. These are not interchangeable state labels.
- [Publisher SI original DOCX](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/si_candidate.docx), “Calculation method”: B3LYP/6-31G geometry, B3LYP/6-31G(d,p) TDDFT, ORCA SOC and Multiwfn/VMD analysis. SI Figs. S21–S23 explicitly concern T1. Their populations cannot be relabelled as T3/T4 evidence. Retrieval/source identity is recorded in [publisher_si_retrieval.json](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/publisher_si_retrieval.json).
- User-approved D4 keeps lifetimes hidden. The agent submits the molecular comparison and its limits; the evaluator makes the experimental comparison. Absolute PVA lifetime prediction, host-causal reproduction and exact SI partition percentages are not newly imposed requirements.

## Effective successful computation steps

### 1. Molecular identity and ground-state geometry

The named 1-, 2-, and 4-Bpin-substituted carbazoles are C18H20BNO2, neutral singlets. The historical named-graph generation, positional mapping and deduplication inputs are recorded in [public_structure_identity_audit.json](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/public_structure_identity_audit.json). Each retained ground-state run used B3LYP/6-31G Opt/Freq. The 126 printed Cartesian modes include translational/rotational modes; do not call them 126 positive vibrational modes.

- **CZ1B**: [input](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ1B_author_optfreq_retry2/outputs/execution_jobs/job_f5dd524351634b7e80622607a728cb62/input.inp), [Opt/Freq output](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ1B_author_optfreq_retry2/outputs/execution_jobs/job_f5dd524351634b7e80622607a728cb62/stdout.log), [final geometry](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ1B_author_optfreq_retry2/outputs/execution_jobs/job_f5dd524351634b7e80622607a728cb62/input.xyz); 12 optimization cycles, 0 imaginary frequencies; HOMO/LUMO = -5.2213/-0.7462 eV, gap 4.4751 eV.
- **CZ2B**: [input](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ2B_author_optfreq_retry2/outputs/execution_jobs/job_cc983dad0fbb469781ca552e750526e2/input.inp), [Opt/Freq output](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ2B_author_optfreq_retry2/outputs/execution_jobs/job_cc983dad0fbb469781ca552e750526e2/stdout.log), [final geometry](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ2B_author_optfreq_retry2/outputs/execution_jobs/job_cc983dad0fbb469781ca552e750526e2/input.xyz); 14 optimization cycles, 0 imaginary frequencies; HOMO/LUMO = -5.3082/-0.8191 eV, gap 4.4891 eV.
- **CZ4B**: [input](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ4B_author_optfreq_retry2/outputs/execution_jobs/job_f48439d4bc28496dbf545d8a8d4203ba/input.inp), [Opt/Freq output](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ4B_author_optfreq_retry2/outputs/execution_jobs/job_f48439d4bc28496dbf545d8a8d4203ba/stdout.log), [final geometry](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ4B_author_optfreq_retry2/outputs/execution_jobs/job_f48439d4bc28496dbf545d8a8d4203ba/input.xyz); 15 optimization cycles, 0 imaginary frequencies; HOMO/LUMO = -5.1817/-0.7857 eV, gap 4.3960 eV.

### 2. Excitation energies, S1 character and SOC

The optimized geometries feed B3LYP/6-31G(d,p) TDDFT, with DoSOC and NTO output. Preserve the actual state energies and spin labels; an `input.s3.nto` filename is not proof of a T3 state. The original S1 NTO files below are singlet evidence.

- **CZ1B**: [input](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ1B_author_tddft_soc_nto/outputs/execution_jobs/job_d28532a8cb9e42e186a68915b92705c0/input.inp), [TD/SOC output](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ1B_author_tddft_soc_nto/outputs/execution_jobs/job_d28532a8cb9e42e186a68915b92705c0/stdout.log), [S1 NTO](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ1B_author_tddft_soc_nto/outputs/execution_jobs/job_d28532a8cb9e42e186a68915b92705c0/input.s1.nto); S1=3.819 eV; 20 singlet and 20 triplet roots.
- **CZ2B**: [input](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ2B_author_tddft_soc_nto/outputs/execution_jobs/job_f1b51a9441fc47acb2b6c1a688599fd6/input.inp), [TD/SOC output](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ2B_author_tddft_soc_nto/outputs/execution_jobs/job_f1b51a9441fc47acb2b6c1a688599fd6/stdout.log), [S1 NTO](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ2B_author_tddft_soc_nto/outputs/execution_jobs/job_f1b51a9441fc47acb2b6c1a688599fd6/input.s1.nto); S1=3.854 eV; 20 singlet and 20 triplet roots.
- **CZ4B**: [input](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ4B_author_tddft_soc_nto/outputs/execution_jobs/job_70cc591851724a0a810d9a8bac72ef44/input.inp), [TD/SOC output](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ4B_author_tddft_soc_nto/outputs/execution_jobs/job_70cc591851724a0a810d9a8bac72ef44/stdout.log), [S1 NTO](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/native_workspace/CZ4B_author_tddft_soc_nto/outputs/execution_jobs/job_70cc591851724a0a810d9a8bac72ef44/input.s1.nto); S1=3.777 eV; 20 singlet and 20 triplet roots.

For each molecule select **all** triplets with `abs(E(T) − E(S1)) <= 0.30 eV`, not only the largest-SOC pair. Compute the norm as `sqrt(sum(|Hx|², |Hy|², |Hz|²))` from the complex printed SOC components, in cm−1.

| Molecule | Triplet | S1 / eV | T / eV | T−S1 / eV | SOC vector norm / cm−1 |
|---|---|---:|---:|---:|---:|
| CZ1B | T3 | 3.819 | 3.747 | -0.072 | 0.045825757 |
| CZ1B | T4 | 3.819 | 4.103 | 0.284 | 0.041231056 |
| CZ2B | T3 | 3.854 | 3.927 | 0.073 | 0.031622777 |
| CZ2B | T4 | 3.854 | 4.038 | 0.184 | 0.044721360 |
| CZ4B | T3 | 3.777 | 3.760 | -0.017 | 0.050000000 |

These norms are derived from the printed component precision, not newly calculated high-precision SOC values. The largest-SOC roots within the selected window are T3/T4/T3.

### 3. Recover genuine triplet state character from existing wavefunctions

The later existing [full-RPA reconstruction](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/analysis.json) reads binary X/Y amplitudes and exported AO overlap. State identity uses multiplicity metadata, paired amplitudes, stdout energies and RPA normalization; neither the stored root field nor the singlet filename is used alone. The hole and particle matrices are `XXᵀ+YYᵀ` and `XᵀX+YᵀY`. AO orthonormality and known singlet-weight reconstruction are checked. Bpin is defined by the connected component after cutting the unique B–carbazole C bond, not by matching a desired percentage.

- **CZ1B**: [original spin-resolved run](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/qzcli_hpc/CZ1B_triplet_nto_target/1_20260912T120659Z_344); full source hashes, binary spin/energy checks, AO overlap, partition indices and singlet-weight regression are retained in `analysis.json`.
- **CZ2B**: [original spin-resolved run](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/qzcli_hpc/CZ2B_triplet_nto_target/1_20260912T120800Z_266); full source hashes, binary spin/energy checks, AO overlap, partition indices and singlet-weight regression are retained in `analysis.json`.
- **CZ4B**: [original spin-resolved run](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/qzcli_hpc/CZ4B_triplet_nto_target/1_20260912T121344Z_499); full source hashes, binary spin/energy checks, AO overlap, partition indices and singlet-weight regression are retained in `analysis.json`.

All selected triplets are retained below. Fractions use **state-weighted Löwdin populations**; leading-pair populations and Mulliken partitions are separate quantities.

| Molecule | Triplet | Energy / eV | Bpin hole fraction | Bpin particle fraction | Full arrays |
|---|---|---:|---:|---:|---|
| CZ1B | T3 | 3.747 | 0.009059513 | 0.089721184 | [natural hole/particle arrays](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/CZ1B/T3_natural_hole_particle.npz) |
| CZ1B | T4 | 4.103 | 0.016025377 | 0.043073511 | [natural hole/particle arrays](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/CZ1B/T4_natural_hole_particle.npz) |
| CZ2B | T3 | 3.927 | 0.010843035 | 0.053638270 | [natural hole/particle arrays](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/CZ2B/T3_natural_hole_particle.npz) |
| CZ2B | T4 | 4.038 | 0.006590135 | 0.035307522 | [natural hole/particle arrays](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/CZ2B/T4_natural_hole_particle.npz) |
| CZ4B | T3 | 3.760 | 0.005239193 | 0.077837085 | [natural hole/particle arrays](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/CZ4B/T3_natural_hole_particle.npz) |

For the largest-SOC roots, all three have mainly carbazole-localized hole/particle populations in this partition. CZ2B does not have the largest Bpin particle fraction. The nonzero Bpin contribution is evidence of mixing, but does not by itself prove the author's distinct CZ2B HLCT explanation; an arbitrary percentage threshold is not introduced.

### 4. Independent postprocessor-definition check and separate T1 comparison

Existing successful [documented Multiwfn full-amplitude import](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/documented_multiwfn_fullrpa.json) and [native NTO composition](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/spin_resolved_nto_reconstruction_20260915/multiwfn_nto_composition_runs.json) retain multiplicity-3 T3/T4/T3, explicit MO indexing, normalization and all-atom composition. Native leading-NTO Mulliken Bpin hole/electron percentages are CZ1B 1.08522/6.82537, CZ2B 0.37487/2.72158, CZ4B 0.66518/2.94046. This also does not establish uniquely stronger Bpin character for CZ2B. Multiwfn's leading-NTO construction is not identical to the full-RPA natural-hole/particle definition; the two are not silently merged.

The [separate T1 reconstruction](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/provenance/si_caption_t1_reconstruction_20260915/comparison.json) gives T1=2.999/3.009/2.980 eV. Its same-definition Mulliken charge-reorganization diagnostic is smallest for CZ2B, qualitatively consistent with main PDF p.3. This supports that **T1** statement, not the separate T4-HLCT assertion. Exact SI partition agreement remains unestablished.

### 5. Cross-isomer interpretation and evaluator use

The valid molecular chain supports comparison of geometries, frontier gaps, S1/triplet energies, selected SOC pairs and computed state character with explicit limitations. In the current evaluator, `*_result_state_character` allows a **clearly evidenced alternative**. The data above can support such an alternative—mainly core-localized states with partition-dependent Bpin mixing—without falsely asserting reproduction of the original HLCT interpretation.

Thus distinguish:
- **Computability and the allowed evidence-based alternative:** supported by existing molecular calculations and postprocessing.
- **Exact reproduction of the paper's CZ2B/T4-HLCT explanation:** not established.
- **PVA-host causation or absolute film lifetimes:** outside the approved isolated-molecule verification scope.

The source [results.json](../../../../docs/verification/group_6/paper_84efbea3ab8e6e20/report/results.json) still uses `bounded_failure` under its stricter author-claim closure. That label is not by itself proof that the present alternative-allowing task is a computational dead end. Conversely, a broad PASS would not establish the unreproduced author explanation. Release descriptions must state which claim is supported. Keep the existing evaluator's evidence-based alternative; do not silently turn all negative or unsupported statements into success.

## Information boundary and exclusions

PR may supply the qualitative author route/hypothesis but not numerical answers or final state/geometry data. In both modes the lifetime data, source outputs, NTOs and this reference remain private. CCDC entries are provenance only, not hidden required downloads. Public-only input staging must still be enforced at runtime.

Cancelled originals, scheduler recovery records, failed software-interface attempts and incorrectly labelled singlet NTO evidence are not successful steps. Their original records remain in the group archive and prior Git versions. Only the effective successful derivatives above are archived here. No public-start replay or new DFT/TDDFT/SOC calculation is implied.
