# Private paper route

## 1. Scientific objective and author claim

The paper builds a multiscale model of hydrogen evolution on Au(111). Its atomistic claim is that GC-DFT energetics for Volmer, Heyrovsky, and Tafel elementary steps vary with proton source, electrode potential, and H* coverage in a way that explains slower alkaline HER and feeds a microkinetic/transport model reproducing polarization behavior. (ev_doc_51c4ed86cc72_000019_ba24fc97dece; ev_doc_51c4ed86cc72_000058_76dc3758fe9d)

## 2. System and model boundary

The authors use a 3-layer p(3×3) Au(111) slab, fixing the bottom two layers, with 15 Å vacuum. Acidic calculations use an Eigen cation H7O3+ (H3O+ plus three waters); alkaline calculations use an H8O4 four-water cluster with H2O as proton source. VASPsol supplies implicit electrolyte screening. The two coverage environments are clean (0 ML H*) and seven pre-adsorbed H atoms in nine sites (7/9 ML). (ev_doc_51c4ed86cc72_000187_b70ddb2af6e7; ev_doc_51c4ed86cc72_000058_76dc3758fe9d; ev_doc_51c4ed86cc72_000239_fa5ab8a085c2)

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax surface and adsorbate states | Au(111), explicit cluster, reaction-state structures | VASP through ASE; GC/FCP constant-potential DFT | BEEF-vdW, PAW, 400 eV, 2×2×1 Monkhorst–Pack, VASPsol ε=78.4 and λD=3.0 Å; force <0.05 eV Å−1 and ΔE<10−4 eV | Optimized states and electronic energies | ev_doc_51c4ed86cc72_000187_b70ddb2af6e7; ev_doc_51c4ed86cc72_000191_190d76665422; ev_doc_51c4ed86cc72_000197_b8f57f0440b0; ev_doc_51c4ed86cc72_000212_f7baef8dba82; ev_doc_51c4ed86cc72_000213_ee074785be4c; ev_doc_51c4ed86cc72_000214_e633d54d37fd; ev_doc_51c4ed86cc72_000216_560410fae4ce |
| 2 | Locate elementary-step saddle points | Relaxed initial/final states for Volmer, Heyrovsky, Tafel | CI-NEB in VASP | 8 images | TS and barrier for each step | ev_doc_51c4ed86cc72_000217_853d191931c9; ev_doc_51c4ed86cc72_000218_b10112d78f54 |
| 3 | Convert energies to free energies | Optimized states and TSs | Vibrational analysis | Only directly reacting adsorbate 3N modes; 298.15 K; quadratic potential fitting | ΔG(U), activation G_a(U), ZPE/entropy corrections | ev_doc_51c4ed86cc72_000191_190d76665422; ev_doc_51c4ed86cc72_000238_260efcdf7ee |
| 4 | Build reaction profiles and pass to MKM | Stepwise free energies | Reference-state construction and mean-field MKM | Initial Volmer state is zero; interpolate 0 and 7/9 ML in MKM | Profiles, rate constants, coverages, rates | ev_doc_51c4ed86cc72_000239_fa5ab8a085c2; ev_doc_51c4ed86cc72_000240_6a1967601c1e |
| 5 | Couple kinetics to transport | MKM rates, bulk pH/H2 | Continuum Nernst–Planck transport | Local pH from cathode-surface hydronium concentration; iterate to relative pH/H2 change <10−3 | Polarization curves and local environments | ev_doc_51c4ed86cc72_000029_2f014e95dc48; ev_doc_51c4ed86cc72_000182_88e2fb942c05 |

## 4. Validation and analysis protocol

The paper compares acidic (0 V vs SHE, H3O+) and alkaline (−0.826 V vs SHE, H2O) profiles at both coverages, then uses the energetics in MKM and a continuum transport model. It interprets higher alkaline Volmer/Heyrovsky barriers, coverage-induced barrier increases, local-pH growth under acid current, and current plateaus. The authors note finite explicit-solvent and static-solvation limitations. (ev_doc_51c4ed86cc72_000058_76dc3758fe9d; ev_doc_51c4ed86cc72_000071_241bc97a4471; ev_doc_51c4ed86cc72_000182_88e2fb942c05; ev_doc_fdf45f3054b8_000228_c377f64927d3)

## 5. Private reference results

Source-backed qualitative references are: alkaline Volmer and Heyrovsky barriers are higher than acidic ones; increasing H* coverage increases both barriers; the overall Volmer–Tafel reaction energy should be coverage invariant when references are consistent; and the multiscale framework produces a local-pH jump/proton-depletion regime and characteristic current plateau. Exact Supplementary Data 1 numbers and author coordinates remain private and are not required as public inputs. (ev_doc_51c4ed86cc72_000071_241bc97a4471; ev_doc_fdf45f3054b8_000205_6a4a4b4f4a5d; ev_doc_51c4ed86cc72_000182_88e2fb942c05)

## 6. Limitations and interpretation boundaries

This benchmark evaluates defensible independent calculations and trend interpretation, not identity with the authors' unpublished starting geometries. Explicit water configuration, functional sensitivity, static solvent treatment, and finite-scan-rate effects must be reported as limitations. Absolute free energies are not treated as transferable beyond the declared model.
