# Private paper route

## 1. Scientific objective and author claim

The authors use spin-polarized DFT to explain Br-controlled spin-state changes of nickelocene (NiCp2) on Br-decorated Au(111). Their central claim is that charge transfer and hybridization with a sufficiently populated Br island remove one of the two frontier Ni 3d-derived unpaired-electron components, changing NiCp2 from an intrinsic S=1 state toward S=1/2. They also study a Br-terminated tip, but the present benchmark focuses on the surface-adsorbed molecule and the four Br-island adsorption geometries.

## 2. System and model boundary

The calculated surface is a periodic Au(111) slab with a=b=14.98 Å and gamma=60°, vacuum greater than 10 Å, and the bottom two Au layers fixed. A (sqrt(3) x sqrt(3))R30° Br island containing nine Br atoms is placed on the surface. One neutral NiCp2 molecule is adsorbed above the island. The reported conf3 geometry is the bridge site between two Br atoms. Br and Au are treated as nonmagnetic in the interpretation; molecular, Ni-atom and Ni-3d magnetic moments are distinguished. In the main text's Theoretical Calculations section (physical page 8, printed page 3363), the additional 4x4 Au unit cell holds the Br-tip in a separate junction calculation; it is not the specified adsorption substrate. The total adsorption-slab layer count is not stated in that paragraph.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build surface adsorption models | Au(111) slab, nine-Br island, NiCp2 and four local adsorption environments | Periodic atomistic model | Adsorption cell a=b=14.98 Å, gamma=60°; vacuum >10 Å; bottom two Au layers fixed; molecule tilted about 5–15° from the surface plane. Do not substitute the separate 4x4 Br-tip cell. | Initial geometries for conf1–conf4 | ev_doc_714d91a42012_000035_e2afc2d03340; ev_doc_f07fda1c5a07_000507_b8b7553a1605; ev_doc_f07fda1c5a07_000234_d5e8ace74f24; main physical p8, printed p3363 |
| 2 | Relax adsorption structures | Each initial geometry | Spin-polarized VASP DFT | optB86 exchange-correlation; PAW; 500 eV cutoff; Gamma-only sampling; relax until all forces <0.02 eV/Å | Optimized geometry and energy | ev_doc_f07fda1c5a07_000507_b8b7553a1605; ev_doc_f07fda1c5a07_000508_3566c50c7170; ev_doc_f07fda1c5a07_000509_d12711c34000 |
| 3 | Extract spin observables | Relaxed geometry and converged spin density | VASP OUTCAR/charge and magnetization analysis | Molecular total moment, Ni local moment, and Ni 3d contribution reported separately | Magnetic moments | ev_doc_714d91a42012_000229_3c560bc59c98; ev_doc_714d91a42012_000262_db343bb52491 |
| 4 | Interpret spin transition | Moments, charge transfer, PDOS | Bader/planar charge analysis and spin-resolved PDOS | Compare gas phase with Br/Au; identify splitting of Ni 3d xz/yz-derived frontier states | S=1 to S=1/2 interpretation | ev_doc_f07fda1c5a07_000260_1f5a67e826c7; ev_doc_f07fda1c5a07_000261_43a66aabe536; ev_doc_714d91a42012_000262_db343bb52491 |

## 4. Validation and analysis protocol

The authors compare several adsorption environments and report that their molecular moments are close in magnitude (0.87–0.95 μB) despite opposite spin orientation signs. They use force convergence below 0.02 eV/Å, compare the gas-phase and adsorbed spin densities, and support the moment reduction with approximately 0.4 e charge transfer, Bader analysis, and spin-resolved PDOS showing splitting of the Ni 3d-derived frontier states. Table S3 reports conf1–conf4 molecular, Ni, and Ni-3d moments.

## 5. Private reference results

For conf3 (bridge between two Br atoms), Table S3 reports NiCp2 = -0.87 μB, Ni = -0.56 μB, and Ni 3d = -0.57 μB. The paper's main text describes the nine-Br-island molecular moment as approximately 0.87 μB and interprets it as an effective S=1/2 state. The four molecular moments are conf1 0.87, conf2 -0.95, conf3 -0.87, and conf4 -0.90 μB.

## 6. Limitations and interpretation boundaries

The source does not provide a machine-readable starting coordinate file or a unique azimuth/height for every initial adsorption structure. The benchmark therefore scores the converged, explicitly identified bridge-site state and requires the investigator to disclose the deterministic construction and sensitivity/alternative-start checks. A signed magnetic moment depends on the chosen global spin axis; comparison should retain sign when available and also report magnitude and convention. DFT magnetic moments are model observables, not direct experimental spin quantum numbers.
