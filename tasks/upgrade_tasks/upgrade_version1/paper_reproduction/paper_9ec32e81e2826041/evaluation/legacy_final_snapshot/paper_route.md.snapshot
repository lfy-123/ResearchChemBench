# Private paper route

## 1. Scientific objective and author claim

The authors used computation to compare the 300 K Gibbs free energies of coplanar and perpendicular conformers of the mononuclear zincafluorene complex Z-cAAC^Cy. Their qualitative claim is that the cAAC complex has nearly equivalent conformers, in contrast to the NHC analogues, and that dispersion interactions influence the conformational preference.

## 2. System and model boundary

The system is the neutral singlet Z-cAAC^Cy complex containing one Zn center and the C/H/N ligand framework. The two structures are the S0-optimized perpendicular and coplanar conformers tabulated in SI Tables S1 and S2. The reported quantity is ΔG = G_coplanar − G_perpendicular at 300 K. Frequency analysis is part of the local-minimum validation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the perpendicular S0 conformer | SI Table S1 geometry | Gaussian16 Rev. C.02 | PBE0/6-311+G** with Grimme D3BJ | optimized geometry, frequencies, G at 300 K | ev_doc_f5921d5df667_000130_d14eb9249639; ev_doc_f5921d5df667_000211_89949916ff75 |
| 2 | Optimize the coplanar S0 conformer | SI Table S2 geometry | Gaussian16 Rev. C.02 | PBE0/6-311+G** with Grimme D3BJ | optimized geometry, frequencies, G at 300 K | ev_doc_f5921d5df667_000130_d14eb9249639; ev_doc_f5921d5df667_000212_57680c5b2719 |
| 3 | Establish local minima | outputs of Steps 1–2 | vibrational analysis | no imaginary frequencies | minimum validation for each conformer | ev_doc_f5921d5df667_000130_d14eb9249639 |
| 4 | Compare conformers | two Gibbs free energies | arithmetic comparison | ΔG = G_coplanar − G_perpendicular | conformational free-energy difference | ev_doc_f5921d5df667_000131_8862bf418089 |

## 4. Validation and analysis protocol

The authors optimized both starting conformers, checked that neither optimized structure had an imaginary frequency, and evaluated Gibbs free energies at 300 K. They also repeated the comparison without D3BJ to assess the role of dispersion and examined structural overlays and close contacts. Those sensitivity calculations are interpretive context, not required to reproduce the primary ΔG endpoint.

## 5. Private reference results

The SI reports that both optimized conformers are local minima. The main article and SI Table S7 report the primary D3BJ conformational free-energy difference and a separate no-D3BJ sensitivity comparison. These numerical values remain private to the evaluator.

## 6. Limitations and interpretation boundaries

The result is method- and model-dependent, concerns isolated-molecule harmonic thermal corrections at 300 K, and does not establish solution populations or a dynamical barrier. Starting from the supplied geometries tests the conformers represented by those inputs; it is not a global conformer search.
