# Private paper route

## 1. Scientific objective and author claim

The paper uses ab initio spin–orbit calculations to quantify the magnetic anisotropy of the Co(II) sites in heterometallic {Co2Li2} carboxylate complexes. For complex 1, [Co2Li2(2-fur)6(4PhPy)2], the authors claim a positive axial ZFS parameter and therefore easy-plane anisotropy, with appreciable rhombicity and low-lying spin–orbit Kramers doublets relevant to field-induced slow relaxation.

## 2. System and model boundary

The target is one crystallographically characterized molecule of complex 1, containing two Co(II), two Li(I), six 2-furoate ligands and two 4-phenylpyridine ligands. The electronic target is an individual Co(II) center in the experimentally determined molecular geometry, treated as a high-spin d7 ion (S = 3/2) with spin-free excited states, spin–orbit coupling, and an effective spin Hamiltonian. The reported calculations are single-molecule calculations on the X-ray geometry, not periodic or thermodynamic calculations.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate spin-free multiconfigurational states | Experimental X-ray geometry of each complex; Co(II) site | SA-CASSCF in ORCA 5.0.4 | CAS(7,5), seven Co d electrons in five d orbitals; equal-weight average over 10 quartet and 40 doublet states; second-order Douglas–Kroll–Hess; DHK-def2-TZVP for non-H, def2-SVP for H, def2/JK auxiliary basis | Spin-free states and wavefunctions | ev_doc_5e883dc305a4_000315_12f673490a6c; ev_doc_5e883dc305a4_000317_df80a4531334 |
| 2 | Add dynamic correlation | SA-CASSCF states | NEVPT2 in ORCA | N-electron valence second-order perturbation theory | Correlated spin-free state energies | ev_doc_5e883dc305a4_000159_69b6b672e76c; ev_doc_5e883dc305a4_000317_df80a4531334 |
| 3 | Couple states and extract magnetic tensors | Correlated states | QDPT with SOMF/effective-Hamiltonian treatment; SINGLE_ANISO mode | Spin–orbit coupling from excited states; AILFT analysis | D, E/D, principal g values, low-lying Kramers-doublet energies and magnetic-moment matrix elements | ev_doc_5e883dc305a4_000318_556287aef7c0; ev_doc_5e883dc305a4_000320_77af7d7ff9bd; ev_doc_5e883dc305a4_000321_ccbb3be27290 |
| 4 | Interpret anisotropy and relaxation relevance | Magnetic tensors and low-lying states | Spin-Hamiltonian interpretation and comparison with magnetic data | Positive D interpreted as easy-plane; low KDs and QTM matrix elements considered | Physical interpretation of complex 1 | ev_doc_5e883dc305a4_000159_69b6b672e76c; ev_doc_5e883dc305a4_000230_9b1824084fb3 |

## 4. Validation and analysis protocol

The authors compare calculated D, E/D and principal g values in Table 2. They analyze the low-lying spin–orbit states and wavefunction decomposition in SI Tables S6–S7, and use SINGLE_ANISO magnetic-moment matrix elements to discuss QTM and field-induced relaxation. The principal qualitative checks are positive D/easy-plane anisotropy, a first excited KD above the ground KD, and substantial state mixing/QTM consistent with the discussion of field-induced slow relaxation.

## 5. Private reference results

For complex 1, Table 2 reports calculated D = 22.585 cm^-1, E/D = 0.039, and principal g values gx = 2.093, gy = 2.289, gz = 2.310. SI Table S6 reports the first two spin–orbit states at 0 and 45.3 cm^-1. The paper reports a QTM magnetic-moment matrix element of 1.529 μB for complex 1 and states that the positive D corresponds to easy-plane anisotropy.

## 6. Limitations and interpretation boundaries

The reference is a single molecular geometry and a site-local effective Hamiltonian; it is not a claim of periodic-solid magnetic ordering or a direct prediction of a bulk relaxation time. Agreement is method- and geometry-dependent, and axis conventions can permute principal g components. The evaluator therefore scores the reported principal values as an unordered set and accepts a bounded limitation report when the specified high-level calculation cannot be completed, provided the submitted diagnostics and intermediate validation artifacts are present.
