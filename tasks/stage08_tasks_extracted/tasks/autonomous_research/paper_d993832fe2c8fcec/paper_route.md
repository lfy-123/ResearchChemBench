# Private paper route

## 1. Scientific objective and author claim

The paper studies how arene substitution controls the conformation of diaryl-substituted α-iminonitriles. For compound 2d, the authors claim that the lowest-energy gas-phase structure is type II, that the ortho-hydroxy group supports an intramolecular hydrogen bond to the iminyl nitrogen, and that the DFT geometry agrees closely with the single-crystal structure.

## 2. System and model boundary

Compound 2d is (E)-2-((2-hydroxybenzylidene)amino)-2-(naphthalen-1-yl)acetonitrile, neutral and singlet. The computational boundary is an isolated gas-phase molecule. The solid-state comparison is an external validation boundary, not a periodic crystal calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Explore the bridge torsion and locate the lowest conformer | Molecular structure of each α-iminonitrile | Gaussian 16 | Relaxed scan about C=N–Cα–CAr; Cα is carbon α to CN and CAr is the adjacent arene ipso carbon | Candidate conformers and starting geometries | ev_doc_d8d216122569_000120 (main-paper §3.3); ev_doc_d8d216122569_000042_cadd2963e73f (computational modeling) |
| 2 | Optimize the selected gas-phase structure | Lowest-scan conformer | Gaussian 16 | M06-2X/def2SVP; neutral singlet | Optimized minimum geometry and electronic properties | ev_doc_d8d216122569_000042_cadd2963e73f; ev_doc_9b3537121f4e_000182_22e9670298b4 |
| 3 | Verify a true local minimum | Optimized structure | Gaussian 16 harmonic analysis | No imaginary frequencies | Frequency-validated minimum | ev_doc_d8d216122569_000042_cadd2963e73f |
| 4 | Compare calculated and experimental conformation | DFT structure and SCXRD structure of 2d | Geometric comparison | Bridge torsions φ1−2−3−4 and φ2−3−4−5 | Agreement assessment | ev_doc_d8d216122569_000197_f3c36e4aff01; ev_doc_d8d216122569_000199_ec9ba494b1c2 |

## 4. Validation and analysis protocol

The authors use the absence of imaginary frequencies as the local-minimum check. They classify the bridge using the relative orientation of the bridge bonds in the numbered inset of Fig. 1, and compare the DFT and X-ray torsions in Table 1. They interpret the 2d endo arrangement and near-coplanarity in terms of an intramolecular O–H···N interaction.

## 5. Private reference results

For 2d, Table 1 reports conformer type II, DFT φ1−2−3−4 = 177.9° and φ2−3−4−5 = 59.7°; the corresponding X-ray values are 179.0° and 57.3°. The SI reports E(RM062X) = −916.122625 hartree and dipole moment 1.835001 D for the optimized gas-phase structure. The paper describes the DFT and X-ray structures as nearly superimposable and attributes the conformation to an ortho-hydroxy/iminyl-nitrogen hydrogen bond.

## 6. Limitations and interpretation boundaries

The reported calculation is a gas-phase molecular calculation at one model-chemistry level; it is not a crystal-packing or solution free-energy calculation. A reproduced energy is meaningful only with the same charge, multiplicity, molecular identity and stated method convention. Agreement with an X-ray geometry does not establish a complete conformational free-energy surface or biological activity.
