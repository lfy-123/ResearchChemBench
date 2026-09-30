# Private paper route

## 1. Scientific objective and author claim

The paper uses first-principles calculations to quantify how an isolated O2 molecule interacts with Ag(111).  The authors claim that electron transfer from Ag into O2 reduces the molecular magnetic moment by about 10%, weakening exchange interactions and thereby helping explain the distorted O2-monolayer lattice.

## 2. System and model boundary

The computed system is one spin-polarized O2 molecule adsorbed upright at a high-symmetry site of a six-layer, 2×2 Ag(111) slab, with a vacuum region.  Adsorption energy is referenced to the separately calculated isolated O2 molecule and clean Ag(111) slab.  Charge transfer is obtained from Bader analysis and the molecular magnetic moment from the spin-polarized density.  The SI also reports other adsorption sites and a commensurate monolayer model, but those are outside this benchmark's scored object.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and relax isolated adsorption models | O2 plus Ag(111) slab | Spin-polarized DFT in VASP 5.4.4 with PAW | rev-vdW-DF2; 900 eV plane-wave cutoff; 12×12×1 Monkhorst–Pack mesh; Gaussian smearing σ=0.05 eV; dipole correction; six Ag layers in a 2×2 cell and 15 Å vacuum | Relaxed structures and total energies | ev_doc_e29be8a82f59_000013_5367c3b799d2; ev_doc_e29be8a82f59_000037_3b2876255e82 |
| 2 | Define adsorption energy | Relaxed combined system, clean slab, isolated O2 in a 25 Å cube | Total-energy difference | Reference is the sum of isolated O2 and Ag(111) energies | E_ad for each site/orientation | ev_doc_e29be8a82f59_000013_5367c3b799d2 |
| 3 | Quantify substrate electron transfer | Relaxed combined-system charge density | Bader charge analysis | Charge received by O2 reported in e | q on O2 | ev_doc_e29be8a82f59_000037_3b2876255e82; ev_doc_e29be8a82f59_000069_dce062a7cfc8 |
| 4 | Extract magnetic response | Relaxed spin density | Spin-density/magnetic-moment analysis | Molecular moment reported in μB | μ(O2) | ev_doc_0f2a167df996_000263_f983eb25a33a; ev_doc_0f2a167df996_000265_ef65bc192365 |

## 4. Validation and analysis protocol

The authors compared adsorption sites and orientations, checked adsorption-energy convergence to 1 meV, and used the resulting charge transfer and moment reduction as the electronic input to a Monte Carlo spin-lattice model.  The comparison to the O2 monolayer lattice and its domain-boundary distortions is interpretive support, not part of the fixed single-molecule calculation.

## 5. Private reference results

For the upright fcc row of SI Table 1a, the reported values are E_ad = -0.137 eV, z = 2.99 Å, q = -0.20 e, and μ = 1.74 μB.  The neighboring upright rows are top (-0.110 eV, 3.53 Å, -0.11 e, 1.89 μB), bridge (-0.132 eV, 3.04 Å, -0.19 e, 1.76 μB), and hcp (-0.135 eV, 3.01 Å, -0.20 e, 1.75 μB).

## 6. Limitations and interpretation boundaries

The isolated adsorption model does not reproduce the full incommensurate O2 monolayer or its collective magnetic ordering.  The reference is model- and method-dependent, and charge partitioning is Bader-analysis dependent.  A calculated moment reduction supports, but by itself does not prove, the paper's full causal explanation of the observed phase transition.
