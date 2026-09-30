# Verified computation reference — paper_1b285cf9f763f2cf (paper_reproduction)

> Evaluator-private provenance, not agent input and not an alternative scoring rule. This archive records existing successful calculations and read-only postprocessing. No new quantum calculation or public-starter replay was performed. `docs/verification` is read-only; historical records are not edited.

## Approved boundary repair — release reconciliation (2026-09-15)

The complete fixed-cell shell extraction replaces the historical representative/nearest-target angle selection. Composition labels are reconstructed from POSCAR/CONTCAR, without altering any atomic coordinate, electron number or evaluator target.

## Paper basis and benchmark scope

- [Main paper](../../../../papers/paper_1b285cf9f763f2cf/documents/main.pdf), PDF p. 3 (methods) and p. 8 (UC models/local distortion): VASP, 500 eV, Γ-centered 4×4×4, electronic 10⁻⁵ eV and force 0.03 eV/Å criteria; substitution-driven geometry trends.
- [SI](../../../../papers/paper_1b285cf9f763f2cf/documents/supplementary_001.pdf), PDF p. 10 Fig. S17 and p. 20 Table S7: model depiction and selected bond/angle observables. Selected table angles are not means over a whole octahedron.
- Approved benchmark adaptation: a complete constructed 56-atom host at fixed 8.08 Å; one Fe; UC-3 neutral electronic compensation. This is not an exact dilute experimental loading, an ICSD export, or the full experimental ionic-compensation mechanism. Nominal +2 ionic bookkeeping for UC-3 is not the actual total electronic cell charge.

## Successful calculation chain

1. Start from the constructed u=0.3600 host; replace one Al by Fe in all states, then Zn→Li/O→F for UC-2, a further Zn→Si for UC-3. This archived chain has one candidate per state; it is not an exhaustive site search.
2. Relax atom positions only (ISIF=2) using the archived spin-polarized VASP inputs; 500 eV, 4×4×4 Γ mesh, EDIFF=10⁻⁵, EDIFFG=−0.03 eV/Å. Fe initial moment is 5 μB; there is no NELECT override. Do not impose this initial moment as a final oxidation/spin result.
3. Check final composition, atom order and fixed cell against initial POSCAR. Map initial fractional positions uniquely onto all 56 public host labels modulo lattice translations, then retain that map through CONTCAR. All labels are present exactly once.
4. Enumerate periodic O/F neighbors in adjacent cell images for every cation. Take the nominal four for parent Zn/Li/Si and six for Al/Fe. Retain image vectors, every bond, all unordered neighbor-pair angles and the next-neighbor distance. No target angle enters selection. Actual shell separations are well clear of ties.
5. Compare full same-definition distributions, including split shells and near-180° octahedral angles. Li–O/Si–O shortening and Al–F lengthening are supported; do not infer emission performance or an exact ionic compensation mechanism.

## Application validation

| State | Actual composition | Atoms | Maximum final force / eV Å⁻¹ | Integrated final moment / μB | Smallest shell-to-next-neighbor gap / Å |
|---|---|---:|---:|---:|---:|
| UC-1 | Zn8FeAl15O32 | 56 | 0.029583428 | 1.0000000 | 1.362260528 |
| UC-2 | LiZn7FeAl15FO31 | 56 | 0.027920659 | 1.0000001 | 1.168996707 |
| UC-3 | LiSiZn6FeAl15FO31 | 56 | 0.021361383 | -0.3744090 | 1.119126062 |

All three OUTCAR files contain the required-accuracy stopping statement and normal timing footer. Each state has 24 cation centers, 128 nominal-shell bonds and 288 unordered pair angles. The integrated moment is not a site-resolved Fe valence assignment.

| Complete-set mean / Å | UC-1 | UC-2 | UC-3 |
|---|---:|---:|---:|
| Zn-O | 1.945657 | 1.947965 | 1.971200 |
| Li-O | not present | 1.888110 | 1.880858 |
| Si-O | not present | not present | 1.676866 |
| Al-O | 1.911441 | 1.908120 | 1.914339 |
| Al-F | not present | 2.065858 | 2.108241 |

## Raw output anchors and full data

- UC-1: [Initial model](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc1_spinel_relax_u036_retry/1/POSCAR), [Final geometry](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc1_spinel_relax_u036_retry/1/CONTCAR), [OUTCAR](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc1_spinel_relax_u036_retry/1/OUTCAR), [INCAR](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc1_spinel_relax_u036_retry/1/INCAR), [KPOINTS](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc1_spinel_relax_u036_retry/1/KPOINTS).
- UC-2: [Initial model](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc2_spinel_relax_u036_retry/1/POSCAR), [Final geometry](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc2_spinel_relax_u036_retry/1/CONTCAR), [OUTCAR](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc2_spinel_relax_u036_retry/1/OUTCAR), [INCAR](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc2_spinel_relax_u036_retry/1/INCAR), [KPOINTS](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc2_spinel_relax_u036_retry/1/KPOINTS).
- UC-3: [Initial model](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc3_spinel_relax_u036_retry/1/POSCAR), [Final geometry](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc3_spinel_relax_u036_retry/1/CONTCAR), [OUTCAR](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc3_spinel_relax_u036_retry/1/OUTCAR), [INCAR](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc3_spinel_relax_u036_retry/1/INCAR), [KPOINTS](../../../../docs/verification/group_5/paper_1b285cf9f763f2cf/provenance/qzcli_hpc/uc3_spinel_relax_u036_retry/1/KPOINTS).

[boundary_repair_evidence.json](task_provenance/boundary_repair_evidence.json), `release_reconciliation.states`, retains all 56-atom maps, all 384 bonds and 864 angles across the three states, images, complete-set summaries, force and magnetization evidence. Re-extract with `scripts/replay_three_boundary_observables.py paper_1b285cf9f763f2cf --release-details`.

Historical status: original group composition prose omitted a Zn; the actual input/output counts above are correct. The historical nearest-target representative-angle selection is not used for current validation. Group records remain untouched. The successful evidence supports the approved local-geometry scope and minimum one-candidate coverage; it does not establish exhaustive dopant-site optimization, exact dilute chemistry, a unique Fe oxidation state or optical performance. Numerical-setting sensitivity beyond the archived primary settings is not newly claimed here.

## Archive independence (2026-09-18)

The scientific route, model definition, extraction algorithm, computed summary and primary raw-output links above are part of this reference itself. The maintenance-only JSON under `task_provenance/` is supplementary and can be removed at release without removing those explanations. Historical commentary is not a scored submission requirement.

## Evidence scope review (2026-09-19)

The accepted boundary remains the explicitly constructed fixed-cell 56-atom model. Existing release reconciliation is usable only for fields supported by actual candidate/site/spin records; a format conversion is not evidence of unperformed hypotheses or sensitivity. For the current submission format, map `release_reconciliation.states[].element_counts/atom_count/nominal_ionic_charge_sum` to the same state fields; use the retained CONTCAR for `cell_vectors_A` and `geometry_artifact`, `retained_atom_mapping` for the candidate atom map, `geometry[].neighbors` for all `bond_lengths` (retain periodic images), and `geometry[].angles` for all `bond_angles`. Keep validation and integrated magnetization attached to that same state. This yields one evidenced candidate per state; missing AR hypothesis/discrimination or sensitivity records are not synthesized by the mapping.
