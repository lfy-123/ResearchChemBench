# Private paper route

## 1. Scientific objective and author claim

The authors used ground-state DFT and TD-DFT to relate molecular conformation and substitution to the optical properties of four benzimidazole–acrylonitrile donor–π–acceptor luminogens. For compound 1, the computational claim is that the lowest vertical singlet absorption is a strong, predominantly HOMO→LUMO π–π* charge-transfer excitation and that the simulated absorption is close to the THF experiment.

## 2. System and model boundary

The benchmark system is neutral, closed-shell, singlet (E)-4-(2-(1H-benzo[d]imidazol-2-yl)-2-cyanovinyl)-2-methoxyphenyl acetate (compound 1; C19H15N3O3). The paper treats an isolated molecule for ground-state optimization and an implicit tetrahydrofuran environment for vertical singlet excitations. The hidden comparison covers S1–S5 excitation energies, wavelengths, oscillator strengths, and leading orbital configurations, plus the reported ground-state HOMO–LUMO gap.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain a stable ground-state molecular structure | Compound 1 molecular structure | Gaussian 09W; DFT | B3LYP/6-31+G(d), gas phase, full optimization, no symmetry restrictions | Optimized Cartesian geometry reported in SI Table S3 | Main paper §2.5, ev_doc_7713b8cbf741_000144_b574cef9e06a; SI pp. S21–S22, ev_doc_479922d781bd_000112_1f2de3903526 |
| 2 | Characterize frontier orbitals | Optimized ground-state geometry | Gaussian 09W; Kohn–Sham orbital analysis | B3LYP/6-31+G(d) | HOMO/LUMO distributions and HOMO–LUMO gap | Main paper §2.5 and Fig. 5, ev_doc_7713b8cbf741_000144_b574cef9e06a and ev_doc_7713b8cbf741_000145_55eea3b719d5 |
| 3 | Predict solution absorption | Optimized ground-state geometry | Gaussian 09W; TD-DFT | CAM-B3LYP/6-31+G(d), PCM tetrahydrofuran, singlet vertical excitations | Simulated spectrum; S1–S5 energies, wavelengths, oscillator strengths, and configurations | Main paper §2.5, ev_doc_7713b8cbf741_000145_55eea3b719d5; SI Fig. S30 and Table S7, ev_doc_479922d781bd_000122_4b355e95b4a1 and ev_doc_479922d781bd_000123_67f4ffe096a0 |
| 4 | Compare theory with experiment | Simulated lowest absorption and THF spectrum | Numerical/qualitative comparison | Calculated maximum versus experimental THF maximum | Claimed close agreement and ICT assignment | Main paper §2.5, ev_doc_7713b8cbf741_000145_55eea3b719d5 |

## 4. Validation and analysis protocol

The paper states that geometries were fully optimized without symmetry restrictions to represent the most stable conformers. It compares the simulated absorption maxima with measured THF maxima and interprets the orbital distributions and leading TD-DFT configurations. Table S7 reports only configuration contributions above 10%.

## 5. Private reference results

- Ground-state HOMO–LUMO gap for compound 1: 3.33 eV.
- S1: 3.4888 eV, 355.37 nm, oscillator strength 1.1496, HOMO→LUMO 47.1%.
- S2: 4.3681 eV, 283.84 nm, oscillator strength 0.0679, HOMO−1→LUMO 45.5%.
- S3: 4.4800 eV, 276.75 nm, oscillator strength 0.0173; HOMO−3→LUMO 21.0% and HOMO−2→LUMO 19.9%.
- S4: 4.7571 eV, 260.63 nm, oscillator strength 0.0870; HOMO−3→LUMO 17.3% and HOMO−2→LUMO 23.6%.
- S5: 5.2615 eV, 235.64 nm, oscillator strength 0.0047, HOMO−4→LUMO 40.6%.
- The paper describes S1 as the primary HOMO→LUMO π–π* charge-transfer transition localized on the cyanostilbene fragment. The reported calculated absorption maximum is 355 nm versus 365 nm experimentally in THF.

## 6. Limitations and interpretation boundaries

The paper does not document a systematic conformer ensemble, vibrational frequency calculation, functional sensitivity study, explicit-solvent treatment, or excited-state geometry optimization. Its charge-transfer interpretation is based on frontier-orbital distributions and TD-DFT configurations. The benchmark therefore evaluates reproducibility of vertical absorption and the qualitative state assignment for a neutral monomer in implicit THF, not aggregation, fluorescence, non-radiative rates, solid-state packing, or excited-state dynamics.
