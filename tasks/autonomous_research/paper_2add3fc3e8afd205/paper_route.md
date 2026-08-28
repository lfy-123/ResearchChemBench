# Private paper route

## 1. Scientific objective and author claim

The authors investigate whether the high-pressure Cd3(C3N6) structure and its unusual
melaminate distortion are explained by appreciable Cd-N covalency. Their claim is that
geometry optimization reproduces the experimentally refined R3c structure and that bonding
analysis supports a covalent Cd-N contribution that constrains the anion geometry.

## 2. System and model boundary

The system is the periodic 47.7(10) GPa Cd3(C3N6) phase, trigonal R3c (No. 161), with
one crystallographically independent Cd, C and two N sites on 18b positions. The public
starting model is the experimental asymmetric unit and hexagonal cell; symmetry generates
the full periodic crystal. The quantities of interest are relaxed C-N distances, the
non-planar/distorted melaminate geometry, Cd-N bond indices, and C-N integrated crystal
orbital bond indices.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the crystal structure | Experimental R3c Cd3(C3N6) model | Plane-wave DFT in CASTEP for structural work | PBE; norm-conserving on-the-fly pseudopotentials; 1000 eV cutoff; Monkhorst-Pack spacing <0.023 Å^-1; energy <5e-6 eV atom^-1; force <0.008 eV Å^-1; stress <0.02 GPa | Relaxed cell and positions | ev_doc_760096ebe5d2_000130_e79d05a4f88c; ev_doc_760096ebe5d2_000134_52dcbfa85de0 |
| 2 | Obtain accurate wavefunctions and bonding indices | Optimized periodic structure | VASP followed by LOBSTER | PBE/PAW; 800 eV; Gamma-centered mesh at 2pi x 0.02 Å^-1; geometry optimization before accurate SCF; Gaussian smearing 0.02 eV for optimization and tetrahedron/Blöchl for accurate energies; LOBSTER 5.1.1 | Wavefunction-derived bond indices | ev_doc_760096ebe5d2_000185_90993b4ba6e7; ev_doc_760096ebe5d2_000186_5070fff8e12c; ev_doc_760096ebe5d2_000188_6cc034a6cb80; ev_doc_760096ebe5d2_000190_b8c26963f852; ev_doc_760096ebe5d2_000191_a302edf57c4e |
| 3 | Compare structure and bonding with reported values | Relaxed geometry and LOBSTER output | Bond-length statistics and ICOBI/COBI analysis | C-N labels x, y, z follow the paper's melaminate labeling; compare Cd-N Wiberg-Mayer range and C-N ICOBI pattern | Validation report | ev_doc_3edd95c8090c_000236_23b1c53d651c; ev_doc_3edd95c8090c_000238_f5d6be8ba34b; ev_doc_3edd95c8090c_000241_be08173b7336; ev_doc_3edd95c8090c_000243_5d007ceb55bd |

## 4. Validation and analysis protocol

The authors compare optimized and experimental C-N distances, inspect the out-of-plane
distortion of the melaminate unit, and use Wiberg-Mayer Cd-N bond orders and LOBSTER ICOBI
values to interpret covalency. Their C-N bond labels x, y and z are those in Figure 3e and
Table 2. The ICOBI analysis distinguishes terminal C-N bonds from in-ring C-N bonds and
weights values by multiplicity when forming an anion total.

## 5. Private reference results

Table 2 reports calculated Cd3(C3N6) C-N distances of 1.388, 1.338 and 1.380 Å for x, y
and z at 0.0001 GPa. The paper reports Cd-N Wiberg-Mayer bond orders of 0.30-0.35. For
the related Ca3(C3N6) analysis at 35 GPa, terminal and in-ring C-N ICOBI contributions are
4.236 and 6.786, respectively, with total 11.022; these are retained as context for the
bonding interpretation and are not public task targets.

## 6. Limitations and interpretation boundaries

The experimental Cd coordinates are measured at high pressure whereas the tabulated DFT
Cd distances are listed at near-zero pressure, so pressure/model differences limit direct
numerical equivalence. Bond indices depend on basis reconstruction and population-analysis
conventions. A successful reproduction supports, but does not uniquely prove, the proposed
covalency mechanism; failure of one observable must be interpreted with convergence,
symmetry, pressure and bonding-analysis diagnostics.
