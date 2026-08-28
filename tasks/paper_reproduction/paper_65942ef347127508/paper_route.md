# Private paper route

## 1. Scientific objective and author claim

Determine the free-energy barrier for axial racemization of product 3a at 323.15 K (50 °C) in toluene. The authors claim that the calculated barrier agrees with the measured barrier and explains weak configurational stability.

## 2. System and model boundary

Neutral 3a and its enantiomeric minimum ent-3a are treated as isolated molecules with implicit SMD(toluene). The SI supplies 57-atom Cartesian geometries for both minima and the racemization saddle.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize structures and calculate frequencies | 3a, ent-3a, saddle geometries | Gaussian 16 DFT | M06/6-31G(d,p), SMD(toluene) | stationary points and frequencies | ev_doc_4e0cb55e9fc4_000086_01006f96bfbd; ev_doc_4e0cb55e9fc4_000090_01aae6cd9401 |
| 2 | Verify transition-state connectivity | optimized saddle | IRC at stated level | SMD(toluene) | path to both minima | ev_doc_4e0cb55e9fc4_000090_01aae6cd9401 |
| 3 | Refine energies and construct free energies | optimized structures | M06-2X/def2-TZVPP-SMD(toluene) single points plus thermal corrections | source labels thermal correction as 353.15 K although narrative and claim use 323.15 K | corrected free energies | ev_doc_4e0cb55e9fc4_000615_5dd548b0b0b7; ev_doc_4e0cb55e9fc4_000620_01d0244b3d5f; ev_doc_4e0cb55e9fc4_000626_acdff7cfce91 |
| 4 | Compute barrier | saddle and connected minimum | ΔG‡ = G(TS) − G(minimum), hartree-to-kcal/mol conversion | use lower connected minimum and disclose temperature convention | ΔG‡ | ev_doc_57094099459d_000051_ef7127cc758c |

## 4. Validation and analysis protocol

Minima must have no imaginary frequencies; the saddle must have exactly one. IRC must connect the saddle to both opposite axial minima. The SI reports −42.45 cm−1 for the saddle and corrected free energies −2369.209662, −2369.207107 and −2369.159528 hartree for ent-3a, 3a and the saddle.

## 5. Private reference results

The article reports ΔG‡ = 29.86 kcal/mol at 50 °C and an experimental barrier of 29.0 kcal/mol.

## 6. Limitations and interpretation boundaries

The SI has a 323.15/353.15 K labeling inconsistency. The benchmark uses the article's 50 °C claim and requires disclosure of the inconsistency. One modeled pathway does not establish a global kinetic mechanism.
