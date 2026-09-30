# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT projected densities of states to locate occupied Au–thiol hybrid states on Au(111), linking their onset to the photon-energy threshold for direct charge-transfer chemical interface damping (CID). The authors claim that the hybrid occupied state begins about 1 eV below the Fermi energy and therefore explains the observed CID increase above roughly 1 eV.

## 2. System and model boundary

The experimental system is decanethiol on Au(111), while the computational models simplify the adsorbate to S, SH, or SCH3 on ideal Au(111) slabs. The relevant model here is SCH3 at 1/4 monolayer coverage on a 2x2 Au(111) cell, with adsorbates on both slab faces. The SI notes that the exact atomistic interface is not known experimentally and that smaller adsorbates are used for cost control.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build periodic model | Au(111) and SCH3 | VASP periodic slab | 2x2 cell; 12 Au layers; at least 13 Å vacuum; 1/4 ML; symmetric two-sided adsorption; initially tilted SCH3 | initial slab | ev_doc_860a7f763c22_000096_bec232bfe118; ev_doc_860a7f763c22_000097_d107fb6c8fd8 |
| 2 | Relax structure | initial slab | spin-polarized PBE/PAW DFT in VASP | 550 eV cutoff; 15x15x1 k mesh for 2x2; forces below 5 meV/Å | relaxed geometry and energy | ev_doc_860a7f763c22_000095_3f8a9d8ccb85 |
| 3 | Compute electronic structure | relaxed slab | VASP DOS | tetrahedron method with Blöchl corrections; projections on S and Au atoms bonded to S | projected DOS | ev_doc_860a7f763c22_000095_3f8a9d8ccb85; ev_doc_4baced4bbc50_000141_9bfa360b7c5a |
| 4 | Interpret pDOS | projected DOS | energy-aligned analysis | identify the occupied Au–S hybrid feature relative to EF | onset near -1 eV | ev_doc_4baced4bbc50_000141_9bfa360b7c5a; ev_doc_860a7f763c22_000113_205957e3f3ea |

## 4. Validation and analysis protocol

The relaxed tilted SCH3 model moved from fcc toward a bridge-like site, approximately 0.2 Å toward hcp, and produced surface corrugation of about 0.3 Å. The authors compare alternative adsorbates and surface models; most retain a hybrid Au–S state near -1 eV. They caution that DOS alone does not determine transition probabilities and that longer chains and unknown interface structures can shift levels.

## 5. Private reference results

The main paper identifies an increase in DOS around -1 eV for Au atoms bonded to sulfur and describes this as the onset of hybrid HOMO states. The SI reports the same qualitative feature for bridge-like SCH3 and related models. The paper interprets the approximately 1.0–1.5 eV optical region as the onset/growth region of direct charge transfer, alongside an energy-independent roughness contribution.

## 6. Limitations and interpretation boundaries

The model is not a full decanethiol SAM, does not simulate solution or the experimental preparation, and uses a simplified interface. A pDOS feature is an energetic indicator, not a transition probability. Comparisons should therefore be made to the occupied-state location and qualitative CID interpretation, not to an exact experimental rate.
