# Private paper route

## 1. Scientific objective and author claim

The authors used density-functional calculations to provide atomistic models for the interaction of the coumarin–squaramide receptor L1 with ibuprofen anion (IBU−) and to test whether calculated structure and optical response are consistent with the experimental host–guest observations. Their claim is that low-energy L1–IBU− structures in solution are organized by hydrogen bonding between the squaramide NH donors and the guest carboxylate, supplemented by aromatic stacking, and that the calculated complex spectrum exhibits a red shift relative to free L1. They conclude that the calculated structures and spectra are reliable models for species present in solution and support the experimental interpretation.

## 2. System and model boundary

The computed host is neutral singlet L1, 3-(benzylamino)-4-((2-oxo-4-(trifluoromethyl)-2H-chromen-7-yl)amino)cyclobut-3-ene-1,2-dione. The guest is singlet ibuprofen carboxylate, and the modeled host–guest object is the 1:1 anionic L1–IBU− complex. Calculations treated DMSO and ACN as implicit solvents. The paper does not report selection of an ibuprofen enantiomer and does not establish enantioselectivity. Counterions and explicit solvent molecules are absent from the reported computational complex. Standard Gibbs energies derive from harmonic vibrational thermochemistry on optimized stationary points; the reported binding energy uses the most stable computed conformers of L1, IBU−, and their complex.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish solution conformers of free receptor | L1 molecular structure, including comparison to the L1·DMSO crystal conformation | Full DFT geometry optimization in Gaussian 16 | ωB97X-D/6-311+G(d,p); SMD DMSO and SMD ACN | Optimized L1 conformers | Main paper computational details: ev_doc_066b6a58a933_000306_5895c303183b through ev_doc_066b6a58a933_000309_47b089fba6b3; conformer discussion: ev_doc_066b6a58a933_000222_339c09689014 and ev_doc_066b6a58a933_000234_631a3b6642b6 |
| 2 | Verify stationary points and compare conformer thermochemistry | Optimized L1 conformers | Harmonic vibrational frequency analysis | Same electronic-structure and solvent model; relative standard Gibbs energies | Confirmed minima and relative Gibbs-energy ordering | ev_doc_066b6a58a933_000309_47b089fba6b3; Fig. 10 caption ev_doc_066b6a58a933_000238_1dc5cc5012b9 |
| 3 | Assess conformer-dependent optical response | All found L1 conformers | TD-DFT in Gaussian 16 | ωB97X-D/6-311+G(d,p), SMD solvent | Calculated UV-visible spectra | ev_doc_066b6a58a933_000309_47b089fba6b3; SI Fig. S19 ev_doc_043bb42454dd_000108_85eac858d274 |
| 4 | Model host–guest structural alternatives | 1:1 L1 and IBU− encounter structures | Full DFT optimization in Gaussian 16 | ωB97X-D/6-311+G(d,p); SMD DMSO and ACN | Seven optimized complex isomers in each solvent | ev_doc_066b6a58a933_000239_4c461d29046b; Fig. 12 ev_doc_066b6a58a933_000249_ba425baf45bd; SI Fig. S20 ev_doc_043bb42454dd_000109_0c3a75342e9b |
| 5 | Verify and rank complex isomers | Optimized complex structures | Harmonic frequencies and standard Gibbs thermochemistry | Same level and solvent model | Confirmed minima and relative standard Gibbs-energy ordering | ev_doc_066b6a58a933_000309_47b089fba6b3 and ev_doc_066b6a58a933_000249_ba425baf45bd |
| 6 | Quantify association | Most stable computed L1, IBU−, and complex conformers | Energy difference at the reported DFT/SMD level | Binding energy from the three most stable reference structures | DMSO and ACN binding energies | ev_doc_066b6a58a933_000241_b5f5c4e72ba0; PDF page 8 layout block 9 confirms the printed negative signs |
| 7 | Test the optical consequence of complexation | Free L1 and most stable L1–IBU− complex | TD-DFT in Gaussian 16 | Same functional, basis, and implicit solvent family | Comparative UV-visible spectra | ev_doc_066b6a58a933_000250_98997b3b5cb3; Fig. 13 ev_doc_066b6a58a933_000255_d3519ba2395c |

## 4. Validation and analysis protocol

The authors performed full optimization and harmonic frequency calculations to confirm that reported geometries are minima and to obtain relative standard Gibbs energies. They compared multiple free-L1 conformers and seven complex isomers. For free L1 in DMSO, the four lowest conformers lie within 1 kJ mol−1 and their calculated spectra are almost superimposable. The complex analysis identifies intermolecular contacts in the most stable structure and compares calculated spectra of free and bound L1. The author protocol includes both DMSO and ACN as a solvent sensitivity comparison, although the benchmark public objective is bounded to DMSO.

## 5. Private reference results

- In DMSO the four lowest L1 conformations differ by less than 1 kJ mol−1; their calculated absorption spectra are almost superimposable.
- Seven different L1–IBU− complex isomers were reported in DMSO and in ACN.
- The most stable DMSO isomer has both carboxylate oxygen atoms involved in hydrogen bonds with the two squaramide NH hydrogens.
- Aromatic stacking occurs between the ibuprofen aromatic ring and one of the aromatic groups attached to the L1 squaramide, particularly in more stable species.
- The reported binding energy is −42.5 kJ mol−1 in DMSO and −38.9 kJ mol−1 in ACN. The negative signs are visible in the source PDF layout; normalized evidence text dropped the glyphs.
- The calculated lowest-energy absorption band is red-shifted on complex formation relative to L1, without net deprotonation of the NH groups.
- The authors conclude that the calculated structures and spectra provide reliable models for solution species and support their interpretation of experiment.

## 6. Limitations and interpretation boundaries

The paper does not provide a complete machine-readable coordinate archive for all optimized conformers and isomers, nor a fully enumerated candidate-generation procedure. Consequently, exact isomer labels and exhaustive reproduction of every Fig. 10/12 relative energy are not fair public targets. The reported binding energy is model- and convention-dependent; explicit-solvent, counterion, BSSE, deformation, entropy, concentration/standard-state, and anharmonic effects may change its magnitude. The source supports a 1:1 computational model but experimental mass spectra also contain other stoichiometries for L1, so the computational result must not be overgeneralized to unique experimental speciation. The unspecified ibuprofen stereocenter precludes enantioselective claims. A calculated red shift supports consistency with optical response but does not alone prove a unique microscopic solution structure.
