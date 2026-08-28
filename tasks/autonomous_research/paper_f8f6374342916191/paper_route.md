# Private paper route

## 1. Scientific objective and author claim

The paper tests how glyme chain length and glyme:KTf2N composition control potassium–anion contact and aggregate formation. The authors claim that shorter glymes retain more contact ion pairs/aggregates, and that the fraction of Tf2N− anions coordinated by at least two K+ cations tracks the Raman ν(SN) upshift.

## 2. System and model boundary

The computational systems are bulk periodic cubic mixtures of G1, G2, G3, or G4 with KTf2N at glyme:KTf2N ratios 2:1, 3:1, and 4:1. K+–O(glyme) and K+–O(Tf2N−) distances define first-shell neighbors; an anion coordinated by two or more K+ ions is an AGG anion. The analysis is classical MD at 350 K and does not establish electronic structure, reaction chemistry, or battery performance.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate bulk starting configurations | G1–G4, K+, Tf2N−; 12 compositions | PACKMOL random packing | cubic periodic cells; Table S6 counts and dimensions | initial coordinates | ev_doc_5ce22e485157_000117_aa99295b11a1; ev_doc_7c52b149cdeb_000026_e03d9a7e98c9 |
| 2 | Equilibrate and sample bulk liquid/solid mixtures | packed coordinates and OPLS-AA parameters | LAMMPS classical MD | minimization; 250 ps NVE at 500 K; 14 ns NpT at 350.15 K and 1.01325 bar; 21 ns NVT; 10 ns NVT production; 1 fs step; 1.2 nm LJ/Coulomb cutoff; geometric unlike-atom mixing | production trajectories | ev_doc_5ce22e485157_000127_9cb9779f8393; ev_doc_5ce22e485157_000608_ad0268b2a399 |
| 3 | Establish coordination shells | trajectories | RDF and neighbor analysis | first minima: 394 pm for anion O and 436 pm for glyme O | RDFs and coordination histograms | ev_doc_5ce22e485157_000608_ad0268b2a399; ev_doc_5ce22e485157_000609_32000c055815 |
| 4 | Quantify aggregate anions | anion–cation neighbor histories | trajectory post-processing | AGG = Tf2N− coordinated by ≥2 K+; population tables S7–S14 | AGG fractions for 12 systems | ev_doc_5ce22e485157_000622_8475cc6746f5; ev_doc_7c52b149cdeb_000027_a34a9cd08812; ev_doc_7c52b149cdeb_000029_a1af64e922f8; ev_doc_7c52b149cdeb_000037_6d2d06d49ea1; ev_doc_7c52b149cdeb_000040_21aeaee218bf; ev_doc_7c52b149cdeb_000048_5a60effb852f |
| 5 | Compare simulation with spectroscopy | AGG fractions and Raman peak positions | cross-system qualitative correlation | each glyme/composition is one point | structure–spectroscopy trend | ev_doc_5ce22e485157_000622_8475cc6746f5 |

## 4. Validation and analysis protocol

The authors inspect RDF first-shell structure, cation/anion coordination histograms, and the AGG fraction across all 12 systems. They compare the glyme-length/concentration trend with Raman ν(SN) shifts; the reported interpretation is qualitative correlation, not a causal calibration. The paper also reports DFT cluster binding calculations, but those are supporting calculations and are not needed for the AGG benchmark.

## 5. Private reference results

Hidden reference populations are in SI Tables S7–S14. The paper explicitly reports the 4:1 AGG fractions as 70% (G1), 27% (G2), 7% (G3), and 3% (G4), and reports that increasing salt concentration from 4:1 to 2:1 increases AGG fraction in every glyme series (G4 example: 3% to 26%). Tables S11–S14 provide the complete anion coordination populations from which all twelve AGG fractions are obtained by summing the ≥2 K+ rows. Figure S10 reports a strong qualitative correlation with Raman ν(SN).

## 6. Limitations and interpretation boundaries

The exact Tf2N− parameter file is cited but not printed in the SI, so an independent implementation must document its parameter provenance. Finite-size, sampling, force-field, shell-cutoff, and aggregation-definition sensitivity should be reported. The reference is a population/trend benchmark, not a claim that one trajectory or one force field uniquely represents experiment. The MD results do not by themselves prove a battery mechanism or predict cycling performance.
