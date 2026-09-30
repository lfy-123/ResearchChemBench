# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical orbital analysis of the deprotonated merocyanine form NI(O)-Qu to support assignment of the long-wavelength absorption to intramolecular charge transfer (ICT) from the hydroxynaphthalimide donor region toward the N-methylquinolinium acceptor region. The broader claim is that the dye is a viscosity-sensitive mitochondrial fluorophore.

## 2. System and model boundary

NI(O)-Qu is the zwitterionic/deprotonated form of NI-Qu: an (E)-styryl-linked 4-hydroxynaphthalimide bearing an N-carboxymethyl imide substituent and an N-methylquinolinium terminus. The modeled species is the isolated neutral zwitterionic molecule, closed-shell singlet. The reported orbital analysis concerns the chromophore, not explicit solvent, counterion, DNA, protein, or cellular environment.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build NI(O)-Qu model | NI-Qu constitution and deprotonated hydroxyl form | MOPAC2016 model construction | Closed-shell singlet; zwitterionic charge balance | 3D starting structure | ev_doc_8021be9f12b5_000004_daafa5bc3e53; ev_doc_d2a003238519_000070_21659543046e |
| 2 | Relax geometry and calculate orbitals | Starting structure | PM6 in MOPAC2016 with COSMO | epsilon=5; n^2=2; optimization until gradient variation <0.01 kcal/mol; CI over 8 occupied and 8 unoccupied MOs | Optimized geometry and molecular orbitals | ev_doc_8021be9f12b5_000004_daafa5bc3e53; ev_doc_8021be9f12b5_000024_daafa5bc3e53 |
| 3 | Interpret frontier orbitals | Optimized orbital calculation | Orbital-energy extraction and plotted isosurfaces | Identify HOMO and LUMO and inspect fragment localization | Frontier energies and localization assignment | ev_doc_d2a003238519_000072_87b754941997; ev_doc_d2a003238519_000077_cb8a2ebe2d04 |

## 4. Validation and analysis protocol

The authors compare the HOMO/LUMO topology with the structural fragments and use it to associate the long-wavelength band with donor-to-acceptor ICT. The paper also reports that the long-wavelength band is associated with NI(O)-Qu and that its fluorescence responds strongly to viscosity; those optical observations are contextual validation, not additional inputs to the orbital calculation.

## 5. Private reference results

The paper reports HOMO = -8.51 eV and LUMO = -2.07 eV for NI(O)-Qu. The HOMO is localized over the naphthalimide unit and the LUMO is predominantly localized over the quinoline heterocycle. These values and assignments are hidden evaluator references.

## 6. Limitations and interpretation boundaries

The reported values are method- and model-dependent frontier-orbital energies, not experimentally measured ionization potentials or excitation energies. Initial conformer choice, protonation/tautomer treatment, solvent representation, orbital plotting threshold, and software conventions can shift numerical values or visual localization. Evaluation therefore requires the submitted method and state definition, a reproducible optimization/convergence record, and fragment-resolved evidence; it does not treat the numbers as method-independent constants.
