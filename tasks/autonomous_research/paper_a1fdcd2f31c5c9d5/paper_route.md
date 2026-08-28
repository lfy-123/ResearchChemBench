# Private paper route

## 1. Scientific objective and author claim

The paper tests whether irregular Cu nanoparticles are unusually active for the competing hydrogen evolution reaction (HER), relative to regular Cu nanoparticles and periodic Cu surfaces, and therefore whether CO2-reduction selectivity is likely to remain. The authors claim that H adsorption and H2 desorption remain thermodynamically/kinetically difficult on the irregular particles. The Cu(111) calculations provide the periodic reference: hollow-site adsorption remains costly until high coverage, whereas occupation of a top site at high coverage makes Tafel recombination essentially barrierless.

## 2. System and model boundary

The periodic reference is a Cu(111) slab, a (2 x 2) surface cell, three Cu layers, 12 Å separation normal to the surface, and lattice constant a = 3.70 Å. The top two layers are relaxed and the lower layer is fixed; relaxed geometries are followed by a fixed-geometry single point with at least six added fcc-bulk Cu layers, and reported energies use that added-layer model. H adsorption is treated through the electrochemical Volmer step and the computational hydrogen electrode (CHE), at 298.15 K and relative to the standard hydrogen electrode. Explicit solvent, grand-canonical potential effects, and Heyrovsky kinetics are outside the model boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and relax clean periodic surfaces | Cu(111), Cu(533), Cu(553) slabs | VASP DFT with BEEF-vdW | a = 3.70 Å; Cu(111) (2x2), 3 layers; 12 Å vacuum; top two layers free; forces <0.03 eV/Å | relaxed clean slab and energy | ev_doc_766b594f950f_000137_fc59f055e33b; ev_doc_766b594f950f_000138_3ed0f14d7db2; ev_doc_766b594f950f_000139_1d7382631ea4; ev_doc_766b594f950f_000140_f690b2c00fc7; ev_doc_766b594f950f_000145_f90613e66eae |
| 2 | Obtain coverage-dependent H structures | clean slab plus sequential H at surface sites | VASP geometry optimizations; previously adsorbed H may migrate during optimization, subject to the region rule for nanoparticles | Cu(111) configurations examined from low coverage through 1.25 ML; fcc hollows first, top sites only after 1 ML; hcp H can migrate to fcc as coverage rises | optimized H/Cu structures and energies | ev_doc_766b594f950f_000193_086ebe343f9c; ev_doc_766b594f950f_000280_2b8e2364537a; ev_doc_766b594f950f_000299_a1c7aaadf3e9 |
| 3 | Convert energies to adsorption free energies | clean/H slab energies and H2 box energy | CHE post-processing | ΔE = E(Cu+H)-E(Cu)-1/2E(H2); ΔG = ΔE + ΔZPE-TΔS; 0.22 eV for hollow/bridge and 0.17 eV for top; ΔG(U)=ΔG(0)-eU; differential adsorption obeys ΔGdiff=-eU at onset | ΔGads and ΔGads,diff versus coverage and potential | ev_doc_766b594f950f_000149_15107aaee39c; ev_doc_766b594f950f_000162_c3d8d7400dbe; ev_doc_766b594f950f_000167_10db9ebcf7c7; ev_doc_766b594f950f_000168_41fc7c84bafd; ev_doc_766b594f950f_000169_e989e5f2bb7b; ev_doc_766b594f950f_000177_fdb1f5a4787c; ev_doc_766b594f950f_000179_ff8542e7c383 |
| 4 | Test H2 formation kinetics | selected Cu(111) coverages | climbing-image NEB/Tafel desorption | 0.50, 1.00, and 1.25 ML considered; barriers reported for 2H, 4H, and 5H states | Tafel activation barriers | ev_doc_766b594f950f_000317_6c19013321aa; ev_doc_766b594f950f_000342_f40d00db24ed |

## 4. Validation and analysis protocol

The authors compare differential adsorption/potential data with Figure 6 and SI Figure S5, and tabulate the top-site onset in Table 2. Tafel barriers are compared across systems and coverages in Table 3 and Figures 7–8. Interpretation is thermodynamic for Volmer adsorption and kinetic for non-electrochemical Tafel recombination; potential enters the latter indirectly through the selected coverage.

## 5. Private reference results

For Cu(111), the top site first becomes occupied at U = -1.65 V (Table 2). Table 3 reports Tafel barriers of 0.96 eV for 2 H at U = -0.24 V, 0.99 eV for 4 H at U = -0.40 V, and 0.00 eV for 5 H at U = -1.65 V. The paper describes hollow/bridge recombination as a barrier just under 1 eV and top-site recombination as barrierless. The single-H Cu(111) free energy is 0.23 eV at an fcc hollow (Table 1).

## 6. Limitations and interpretation boundaries

The model uses constant-charge CHE without explicit solvent or an explicit electrode field. Only Tafel desorption is explicitly modeled; Heyrovsky and Volmer kinetics are not. Coverage exploration is a selected set of configurations rather than an exhaustive global search, and the paper notes that nanoparticle monolayer coverage is approximate. The reference task therefore scores the defined Cu(111) endpoints and requires reporting numerical convergence and model limitations rather than claiming universal HER behavior.
