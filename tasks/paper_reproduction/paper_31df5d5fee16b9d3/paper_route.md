# Private paper route

## 1. Scientific objective and author claim

The paper studies hydrated vanadium pentoxide, especially whether the bilayer V₂O₅·H₂O structure is adequately represented by C2/m or is better represented by an unconstrained P1 cell, and assigns its Raman-active vibrations. The author claim is that water disrupts the nominal monoclinic symmetry and that the intense band near 890 cm⁻¹ is water-related rather than a V–O–V stretch.

## 2. System and model boundary

The principal system is bilayer V₂O₅·H₂O. The SI P1 unit cell contains 8 V, 24 framework O, 1 water O (O*), and 8 H, with all water confined between V₂O₅ bilayers. The calculations concern Γ-point vibrations and Raman activity; low-frequency modes and finite-temperature disorder are interpretation limits.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax competing structural models | PDF-derived V₂O₅·H₂O cell | VASP PAW, PBE+D2, Dudarev DFT+U | Ueff(V 3d)=4 eV; ENCUT 500 eV; Gaussian 0.05 eV; 2×6×2 k mesh; energy 10⁻⁷ eV and force 10⁻³ eV Å⁻¹ convergence | optimized C2/m and P1 cells | ev_doc_9ea2cfb4970a_000101_b51f6e19e355; ev_doc_9ea2cfb4970a_000109_26385f3647b4; ev_doc_9ea2cfb4970a_000116_e3ffbd3902aa; ev_doc_9ea2cfb4970a_000123_f2e0831b3bf8; ev_doc_ca6ede7d6af2_000006_ca6ce7454223 |
| 2 | Obtain lattice dynamics | optimized cells | finite displacement, Phonopy | Γ point; 2×2×1 displaced supercell; no frequency scaling | frequencies/eigenvectors | ev_doc_9ea2cfb4970a_000125_060cf35f5006; ev_doc_9ea2cfb4970a_000624_c76d830aea58 |
| 3 | Compute Raman spectrum | phonons and dielectric response | numerical dielectric-tensor differentiation in VASP | 300 K; 633 nm; Lorentzian FWHM 2 cm⁻¹ | Raman activities and spectrum | ev_doc_9ea2cfb4970a_000126_1f5c36c43cfc; ev_doc_9ea2cfb4970a_000152_6261d79ec188; ev_doc_9ea2cfb4970a_000153_eddfbd617872 |
| 4 | Compare with experiment and assign modes | calculated peaks and PDF lattice data | peak assignment and structural comparison | water modes and 500–1100 cm⁻¹ framework region | symmetry interpretation and assignments | ev_doc_9ea2cfb4970a_000207_95162728a54e; ev_doc_9ea2cfb4970a_000209_7e775f101f84; ev_doc_9ea2cfb4970a_000247_be0372e815f0; ev_doc_9ea2cfb4970a_000349_04207e5b292b |

## 4. Validation and analysis protocol

The authors compare relaxed lattice parameters with PDF values, compare water Raman modes with measured peaks, inspect framework-mode ranges and eigenvectors, and use PVDOS/ML-force-field calculations as supplementary validation across hydration levels.

## 5. Private reference results

The reported P1 lattice is a=11.69 Å, b=3.63 Å, c=10.93 Å, β=88.481° (α=γ=90° in the SI table); the experimental PDF values are a=11.72 Å, b=3.57 Å, c=11.52 Å, β=88.651°. P1 water-mode frequencies are 3580, 3764 and 1575 cm⁻¹ versus experimental 3562, 3756 and 1595 cm⁻¹. Main P1 peaks include 510, 539, 704, 760, 893, 1041 and 1076 cm⁻¹. The paper concludes P1 is more consistent than C2/m and assigns the ~890 cm⁻¹ band to confined-water modes.

## 6. Limitations and interpretation boundaries

Hydrated V₂O₅ is locally disordered and water positions are humidity- and temperature-sensitive. Harmonic Γ-point spectra do not establish finite-temperature disorder. Reported ML calculations have larger lattice uncertainty and are corroborative, not the primary reference.
