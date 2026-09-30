# Private paper route

## 1. Scientific objective and author claim

The paper tests how donor–bridge–acceptor architecture controls electronic asymmetry relevant to molecular-junction rectification. For the selected isolated A–D molecule, the authors report a non-zero intrinsic dipole and an asymmetric response of electronic properties to an applied field.

## 2. System and model boundary

The benchmark system is the neutral closed-shell A–D molecule with thiol termini, a pyrimidinyl acceptor and phenyl donor, represented by the SI Cartesian structure without electrodes. The scored endpoint is the isolated zero-field molecule; NEGF electrodes and transport are outside the boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize isolated structures under field | SI Cartesian coordinates | Gaussian 16 Rev. B.01 DFT | B3LYP/6-31+G(d), terminal S fixed, field −2 to +2 V | optimized geometries/electronic structures | ev_doc_f0f63ad02edd_000029_79dc94667663; ev_doc_f0f63ad02edd_000030_e1df05deac30 |
| 2 | Refine properties | optimized geometries | Gaussian 16 Rev. B.01 | B3LYP/6-311++G(d,p) single point | energies, orbitals, dipoles | ev_doc_f0f63ad02edd_000031_2061d57db9a4; ev_doc_f0f63ad02edd_000032_1bfd41c61f0e |
| 3 | Relate descriptors to transport | isolated descriptors and junction results | DFT–NEGF analysis | compare dipole, gaps and energy asymmetry with rectification | bridge/length interpretation | ev_doc_f0f63ad02edd_000084_63a2b87c8025; ev_doc_f0f63ad02edd_000110_763aeba95067 |

## 4. Validation and analysis protocol

The paper compares field-dependent dipoles, relative energies, frontier orbital energies and gaps. It reports a zero-field A–D dipole of 2.67 Debye and a decrease as bias moves from negative to positive. Structural changes under field are described as minor; p-bridged analogues are nearly coplanar while unbridged systems are twisted.

## 5. Private reference results

The selected numerical reference is |dipole(A–D, 0 field)| = 2.67 Debye (Section 3.1.2, Fig. 3 discussion). Exact orbital and energy tables are not scored.

## 6. Limitations and interpretation boundaries

Only the isolated A–D zero-field dipole and defensible computational validation are scored. Dipole sign depends on axis convention, so magnitude is used. The source value is a benchmark, not a claim of method uniqueness.
