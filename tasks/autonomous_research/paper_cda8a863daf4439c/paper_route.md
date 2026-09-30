# Private paper route

## 1. Scientific objective and author claim

The paper builds a multiscale model of hydrogen evolution on Au(111). Its atomistic claim is that GC-DFT energetics for Volmer, Heyrovsky, and Tafel elementary steps vary with proton source, electrode potential, and H* coverage in a way that explains slower alkaline HER and feeds a microkinetic/transport model reproducing polarization behavior. (ev_doc_51c4ed86cc72_000019_ba24fc97dece; ev_doc_51c4ed86cc72_000058_76dc3758fe9d)

## 2. System and model boundary

The authors use a 3-layer p(3×3) Au(111) slab, fixing the bottom two layers, with 15 Å vacuum. Acidic calculations use an Eigen cation H7O3+ (H3O+ plus two H2O molecules, confirmed by the official Au27/O3/H7 coordinates; the main-text phrase "three waters" is a stoichiometric inconsistency); alkaline calculations use an H8O4 four-water cluster with H2O as proton source. VASPsol supplies implicit electrolyte screening. The two coverage environments are clean (0 ML H*) and seven pre-adsorbed H atoms in nine sites (7/9 ML). (ev_doc_51c4ed86cc72_000187_b70ddb2af6e7; ev_doc_51c4ed86cc72_000058_76dc3758fe9d; ev_doc_51c4ed86cc72_000239_fa5ab8a085c2)

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax surface and adsorbate states | Au(111), explicit cluster, reaction-state structures | VASP through ASE; GC/FCP constant-potential DFT | BEEF-vdW, PAW, 400 eV, 2×2×1 Monkhorst–Pack, VASPsol ε=78.4 and λD=3.0 Å; force <0.05 eV Å−1 and ΔE<10−4 eV | Optimized states and electronic energies | ev_doc_51c4ed86cc72_000187_b70ddb2af6e7; ev_doc_51c4ed86cc72_000191_190d76665422; ev_doc_51c4ed86cc72_000197_b8f57f0440b0; ev_doc_51c4ed86cc72_000212_f7baef8dba82; ev_doc_51c4ed86cc72_000213_ee074785be4c; ev_doc_51c4ed86cc72_000214_e633d54d37fd; ev_doc_51c4ed86cc72_000216_560410fae4ce |
| 2 | Locate elementary-step saddle points | Relaxed initial/final states for Volmer, Heyrovsky, Tafel | CI-NEB in VASP | 8 images | TS and barrier for each step | ev_doc_51c4ed86cc72_000217_853d191931c9; ev_doc_51c4ed86cc72_000218_b10112d78f54 |
| 3 | Convert energies to free energies | Optimized states and TSs | Vibrational analysis | Only directly reacting adsorbate 3N modes; 298.15 K; quadratic potential fitting | ΔG(U), activation G_a(U), ZPE/entropy corrections | ev_doc_51c4ed86cc72_000191_190d76665422; ev_doc_51c4ed86cc72_000238_260efcdf7ee |
| 4 | Build reaction profiles and pass to MKM | Stepwise free energies | Reference-state construction and mean-field MKM | Initial Volmer state is zero; interpolate 0 and 7/9 ML in MKM | Profiles, rate constants, coverages, rates | ev_doc_51c4ed86cc72_000239_fa5ab8a085c2; ev_doc_51c4ed86cc72_000240_6a1967601c1e |
| 5 | Couple kinetics to transport | MKM rates, bulk pH/H2 | Continuum Nernst–Planck transport | Local pH from cathode-surface hydronium concentration; iterate to relative pH/H2 change <10−3 | Polarization curves and local environments | ev_doc_51c4ed86cc72_000029_2f014e95dc48; ev_doc_51c4ed86cc72_000182_88e2fb942c05 |

## 4. Validation and analysis protocol

The paper compares acidic (0 V vs SHE, H3O+) and alkaline (−0.826 V vs SHE, H2O) profiles at both coverages, then uses the energetics in MKM and a continuum transport model. It interprets higher alkaline Volmer/Heyrovsky barriers, coverage-induced Volmer-barrier increases and Heyrovsky-barrier decreases in Fig. 2a and SI Tables 6/7, local-pH growth under acid current, and current plateaus. The authors note finite explicit-solvent and static-solvation limitations. (ev_doc_51c4ed86cc72_000058_76dc3758fe9d; ev_doc_51c4ed86cc72_000071_241bc97a4471; ev_doc_51c4ed86cc72_000182_88e2fb942c05; ev_doc_fdf45f3054b8_000228_c377f64927d3)

## 5. Private reference results

Source-backed qualitative references are: alkaline Volmer and Heyrovsky barriers are higher than acidic ones; increasing H* coverage raises Volmer barriers but lowers Heyrovsky barriers at the stated Fig. 2 potentials (Fig. 2a and SI Tables 6/7; the adjacent prose claiming both increase is inconsistent with these numerical results); the overall Volmer–Tafel reaction energy should be coverage invariant when references are consistent; and the multiscale framework produces a local-pH jump/proton-depletion regime and characteristic current plateau. Exact reference numbers and coordinates are not required as public task inputs; the author coordinates are publicly available in Supplementary Data 1 and the official Multiscale_HER repository. (ev_doc_51c4ed86cc72_000071_241bc97a4471; ev_doc_fdf45f3054b8_000205_6a4a4b4f4a5d; ev_doc_51c4ed86cc72_000182_88e2fb942c05)

## 6. Limitations and interpretation boundaries

This benchmark evaluates defensible independent calculations and trend interpretation, not identity with the authors' unpublished starting geometries. Explicit water configuration, functional sensitivity, static solvent treatment, and finite-scan-rate effects must be reported as limitations. Absolute free energies are not treated as transferable beyond the declared model.

## 7. Source consistency correction (2026-09-22)

The recovered SI is retained at `evaluation/source_audit/HER_SI_20260922.pdf`. Fig. 2a shows acid Volmer 0.43→0.89 eV and Heyrovsky 0.80→0.25 eV; alkaline Volmer 0.99→1.57 eV and Heyrovsky 1.03→0.60 eV as coverage rises from 0 to 7/9 ML. SI Tables 6/7 independently reproduce these values at 0 and −0.826 V. These numerical results take precedence over the contradictory adjacent general sentence. Methods specifies a 4.43 V absolute SHE reference, whereas parts of SI Tables 3/4 imply 4.33 V; retain both printed work functions and potentials and explicitly state the reference conversion. The correction does not remove any of the 12 requested step/condition combinations, endpoint/path validation or sensitivity checks. Source-table arithmetic is not an independent DFT verification.
