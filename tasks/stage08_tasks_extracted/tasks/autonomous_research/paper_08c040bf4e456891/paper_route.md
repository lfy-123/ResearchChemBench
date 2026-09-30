# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical ionization and dissociation calculations to explain the measured appearance of the dominant neutral-halogen-loss channels of chlorodifluoromethane, CHClF2. The central computational claim is that an adiabatic first ionization followed by channel-specific cation dissociation yields appearance energies consistent with experiment: simple C–Cl cleavage gives CHF2+ + Cl, whereas formation of CHFCl+ + F follows a more complex rearranging minimum-energy path.

## 2. System and model boundary

The parent is isolated gas-phase CHClF2 (connectivity FC(F)Cl), treated as a closed-shell neutral singlet and its lowest doublet monocation. The scored channels are CHClF2+ -> CHF2+ + Cl and CHClF2+ -> CHFCl+ + F, with neutral ground-state halogen atoms at separated-fragment endpoints. Appearance energies are referenced to the optimized neutral parent and combine the adiabatic ionization energy with the cation dissociation requirement. The paper's values are electronic-energy results; no explicit thermal or zero-point correction is described. Other fragmentation channels, electron-impact cross sections, and the dication are outside the selected core.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish relaxed parent states | CHClF2 neutral and monocation | DFT in ORCA 6.0 | PBE0/def2-TZVP geometry optimization | Optimized neutral and cation geometries | Main paper, Computational details, p. 4; `ev_doc_fb21b47b4bb6_000101_acf0b2d3b4fa` |
| 2 | Refine state energies | Optimized structures | CCSD(T) single points | cc-pVTZ basis | Final neutral/cation electronic energies and adiabatic ionization energy | Main paper, Computational details, p. 4; `ev_doc_fb21b47b4bb6_000101_acf0b2d3b4fa` |
| 3 | Map Cl-loss channel R1 | Optimized CHClF2+ | Relaxed DFT scan | PBE0/def2-TZVP; C–Cl separation with relaxation of remaining coordinates | Dissociation profile and separated CHF2+ + Cl endpoint | SI S3, p. S10; `ev_doc_1807c2e8e205_000170_92f3216c3560` and main paper Fig. 15 discussion, pp. 11–12 |
| 4 | Map F-loss channel R2 | CHClF2+ and product endpoint | Scan-assisted NEB at DFT level | PBE0/def2-TZVP; full-coordinate image optimization | Rearranging minimum-energy path to CHFCl+ + F | SI S3, p. S10; `ev_doc_1807c2e8e205_000171_c48109368f90`, `ev_doc_1807c2e8e205_000173_0dccba584531`; main paper Fig. 15 discussion |
| 5 | Form appearance energies | AIE plus channel dissociation energies | Energy bookkeeping | Neutral-parent zero; separated products or maximum required state as described in Fig. 15 | APEs for R1 and R2 | Main paper pp. 10–11, Table 5 and Fig. 15; `ev_doc_fb21b47b4bb6_000441_f8aaa36ade59`, `ev_doc_fb21b47b4bb6_000442_d5b3f43350dc`, `ev_doc_fb21b47b4bb6_000462_deabccd4bd9e` |

## 4. Validation and analysis protocol

The authors compare computed appearance energies with electron- and photon-impact literature values in Table 5. R1 is checked as a monotonic/simple bond dissociation with relaxation. R2 is treated as a multidimensional path because bond weakening and structural motion make a one-coordinate scan insufficient; scan structures assist the NEB path. The reported cation equilibrium C–Cl distance and large-separation behavior provide structural checks, and the resulting appearance energies are compared with experimental ranges/averages.

## 5. Private reference results

- Adiabatic ionization energy of CHClF2: 11.9 eV.
- R1, CHF2+ + Cl: cation C–Cl equilibrium distance about 2.3 Å; dissociation contribution 0.5 eV at about 6.25 Å; total appearance energy 12.4 eV. The text notes an experimental appearance near 12.2 eV.
- R2, CHFCl+ + F: total dissociation contribution 1.6 eV, described as 1.1 eV at an intermediate step plus 0.5 eV later in the path; total appearance energy 13.5 eV. The path involves motion of chlorine while C–F weakens and neutral F separates.
- The authors state that these estimates agree well with available experimental appearance-energy data.

## 6. Limitations and interpretation boundaries

The source does not document exhaustive conformer, electronic-state, basis-set, or multireference sensitivity analyses, and it does not state a zero-point/thermal correction convention. The selected benchmark therefore evaluates defensible independent electronic-energy calculations and path validation, with method sensitivity reported by the submitter. Agreement with the reference numbers alone is insufficient if charge/spin conservation, fragment identity, endpoint separation, or path validation is absent.
