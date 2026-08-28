# Private paper route

## 1. Scientific objective and author claim

The authors used computation to explain why 7,9-bis(4-nitrophenyl)-10-hydroxybenzo[h]quinoline (1NO2) does not follow the usual ESIPT behavior of the HBq series. Their claim is that its lowest singlet excited state has charge transfer from the HBq unit to the 4-nitrophenyl groups, producing a non-ESIPT excited geometry and a shallow proton-transfer barrier.

## 2. System and model boundary

The modeled species is neutral 1NO2 in its enol ground-state form, with an intramolecular O–H···N hydrogen bond, in dichloromethane. The relevant coordinate is the O–H distance; the excited state is the lowest singlet state S1. The paper compares two steric arrangements of the two 4-nitrophenyl groups and carries the lower-Gibbs-energy optimized arrangement forward.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Select a ground-state conformer | Neutral 1NO2 enol structure; two phenyl dihedral arrangements | Gaussian 16W Rev. A.03; DFT | B3LYP/6-311+G(d,p); CPCM dichloromethane; geometry optimization and Gibbs energies | Two optimized S0 structures; lower-Gibbs conformer selected | ev_doc_83714080f5e7_000390_b933e3b2cb5e; ev_doc_83714080f5e7_000391_823063546d85; ev_doc_83714080f5e7_000401_094fbd4e6bda |
| 2 | Characterize singlet states | Selected optimized structure | Gaussian 16W TD-DFT | 30 lowest singlet absorption transitions; B3LYP/6-311+G(d,p) for ground-state-based calculations | Singlet energies, oscillator strengths and orbital assignments | ev_doc_83714080f5e7_000391_823063546d85 |
| 3 | Relax the emissive excited state | Selected S0 geometry | Gaussian 16W TD-DFT | B3LYP/6-31G(d,p); S1 geometry optimization; CPCM dichloromethane | S1 optimized geometry and electronic character | ev_doc_83714080f5e7_000391_823063546d85; ev_doc_83714080f5e7_000614_c166944fbafb |
| 4 | Map proton transfer | S0 and S1 geometries with constrained O–H distances | (TD-)DFT constrained geometry/Gibbs-energy evaluation | O–H distance scan in dichloromethane; relative Gibbs energies plotted | S1 relative-energy profile versus O–H distance | ev_doc_6b75d33bac3b_000011_29abddd92952; ev_doc_83714080f5e7_000614_c166944fbafb |
| 5 | Interpret the profile | Profile and optimized structures | Analysis of geometries, orbitals and relative energies | Identify the non-ESIPT basin, transfer direction and barrier | Mechanistic explanation of 1NO2 behavior | ev_doc_83714080f5e7_000614_c166944fbafb |

## 4. Validation and analysis protocol

The authors checked that optimized ground structures were enol forms with an intramolecular hydrogen bond, examined S1 orbital/transition character, and compared the O–H-dependent S1 Gibbs profile with the corresponding ground-state profile. The S1 profile was interpreted by locating its local basin and the rise toward proton transfer. The SI Fig. S29 is the source for the plotted profile; the main text states the extracted basin location and barrier.

## 5. Private reference results

The S1 profile has a non-ESIPT local minimum at approximately 1.1 Å O–H distance and an approximately 0.05 eV activation energy toward the proton-transfer pathway. The optimized S1 structure has a strongly twisted 4-nitrophenyl group (the 7-position dihedral is reported as 89.76°), and its S1 transition is assigned to HBq-to-nitrophenyl charge transfer. These values and assignments are hidden evaluator references.

## 6. Limitations and interpretation boundaries

The paper does not provide a machine-readable coordinate file or tabulated Fig. S29 values. The benchmark therefore scores the reported profile features and qualitative state assignment, while allowing the Agent to report digitization uncertainty, method dependence, failed optimizations or an alternative validated computational route. The authors' method is private and is not prescribed in the public task.
