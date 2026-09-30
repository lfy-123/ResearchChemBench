# Private paper route

## 1. Scientific objective and author claim

The paper uses first-principles calculations to determine sodium-vacancy ordering and the electrochemical reaction path of NASICON Na_xVTi(PO4)3 (1 <= x <= 4). The author claim is that a low-energy sequence of sodium contents gives a multistep voltage profile and that the framework remains low-strain between desodiated and sodiated endpoints.

## 2. System and model boundary

The framework is rhombohedral R-3c Na4VTi(PO4)3, with Na in Na1 (6b) and Na2 (18e) interstitial sites, isolated VO6/TiO6 octahedra corner-sharing with PO4 tetrahedra. The calculated family is Na_xVTi(PO4)3 for x = 1, 1.5, 2, 2.5, 3, 3.5, 4; the end members are NaVTi(PO4)3 and Na4VTi(PO4)3. The paper enumerates Na/vacancy arrangements, removes duplicates, relaxes structures, and compares total energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define the primitive/conventional NASICON model | Na4VTi(PO4)3, R-3c; Na1 6b and Na2 18e | Crystal construction; VESTA for visualization | Conventional cell is three times primitive; SI transformation matrix [1,1,-1; -1,1,1; 1,-1,1] | Starting Na4 structure and Na-site model | ev_doc_7e7dd2caa681_000016_15eda76d0b88; ev_doc_7e7dd2caa681_000018_bf736cb8ee4a; ev_doc_de7907d1d0dc_000174_c83220d83dee |
| 2 | Search sodium/vacancy orderings | Na_xVTi(PO4)3 arrangements at several x | Enumeration followed by duplicate removal | End members Na1 and Na4; x values 1, 1.5, 2, 2.5, 3, 3.5, 4 | Unique candidate configurations | ev_doc_de7907d1d0dc_000195_69611f961e10; ev_doc_de7907d1d0dc_000201_5784dcda7563; ev_doc_de7907d1d0dc_000216_4c28b8d2d388 |
| 3 | Relax structures and obtain energies | Unique candidates | VASP DFT, PBE/GGA + Grimme D3 + GGA+U | V Ueff=3 eV; 550 eV cutoff; Gamma 2x2x1; electronic 1e-5 eV; ionic 0.02 eV/A; 10 A vacuum | Relaxed cells and total energies | ev_doc_de7907d1d0dc_000163_614ba6464700; ev_doc_de7907d1d0dc_000165_a873025b0449; ev_doc_de7907d1d0dc_000166_560410fae4ce; ev_doc_de7907d1d0dc_000167_7faaac5d9fcb; ev_doc_de7907d1d0dc_000168_115898f2dfac; ev_doc_de7907d1d0dc_000169_9960aa7ab6ad; ev_doc_de7907d1d0dc_000170_b1f61ec87c62; ev_doc_de7907d1d0dc_000171_2fce409aca1e |
| 4 | Determine phase stability | Relaxed energies | Formation energy relative to x=1 and x=4; convex hull | Eform = Ex - [(x-1)E4 +(4-x)E1]/3 | Stable/unstable compositions and phase sequence | ev_doc_de7907d1d0dc_000201_5784dcda7563; ev_doc_de7907d1d0dc_000202_1daaa38f33cd; ev_doc_de7907d1d0dc_000216_4c28b8d2d388 |
| 5 | Convert stable-phase energy differences to voltages | Stable phase energies and bulk Na energy | Voltage from adjacent hull phases | V = -[E_x2-E_x1-(x2-x1)E_Na]/[(x2-x1)e] | Voltage plateaus | ev_doc_de7907d1d0dc_000254_1fa151865991; ev_doc_de7907d1d0dc_000255_1daaa38f33cd; ev_doc_de7907d1d0dc_000256_18dda1666800 |
| 6 | Quantify structural strain | Relaxed endpoint volumes | Relative volume comparison | Compare Na1 and Na4 endpoints | Endpoint volume change | ev_doc_de7907d1d0dc_000412_dfc5ef82e52f; ev_doc_de7907d1d0dc_000415_a1a07d2d685b; ev_doc_de7907d1d0dc_000416_141eaf52303c |

## 4. Validation and analysis protocol

The authors check duplicate-free enumeration, identify hull points from formation energies, compare the calculated voltage sequence with electrochemical plateaus, compare optimized Na2 lattice constants with Rietveld values, and report endpoint volume change. The qualitative mechanistic interpretation assigns successive redox activity to V4+/V3+, Ti4+/Ti3+, and V3+/V2+ as sodium is inserted.

## 5. Private reference results

Reference values are retained in the evaluator files and are taken from SI Tables S1, S2 and S5 and the main-text discussion. They include formation energies and configuration labels, optimized lattice parameters/volumes, three voltage plateaus, and endpoint volume change.

## 6. Limitations and interpretation boundaries

The supplied SI does not contain a machine-readable full primitive CIF; the public package therefore uses the explicit SI asymmetric-unit coordinates and symmetry as a reproducible seed. Energies depend on ordering coverage, magnetic initialization, pseudopotentials and numerical settings. Experimental values are comparison context, not substitutes for independently computed values. A candidate that cannot converge all requested states must report the failed states, attempted coverage and a bounded conclusion.
