# Private paper route

## 1. Scientific objective and author claim

The paper computes buffer insertion free energies at the Ce6 node to explain apparent direction-dependent PCET kinetics. It compares H3BO3 and Tris on pristine and singly reduced nodes.

## 2. System and model boundary

The truncated node is Ce6(H2O)6(OH)6(μ3-OH)4(μ3-O)4(HCO2)6. Buffer insertion replaces terminal −OH2. The oxidized state is singlet; the 1H+/1e− reduced state is doublet with terminal-OH protonation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Construct truncated node and buffer-bound models | SI coordinates and substituted structures | ORCA 6.0 | no constraints | starting structures | ev_doc_393f62b3c7e3_000440_d0437d60d366 |
| 2 | Optimize structures | four bound states | ωB97X-D4/def2-SVPD/SMD(water) | singlet oxidized, doublet reduced | minima | ev_doc_393f62b3c7e3_000573_3a9a88f84648 |
| 3 | Composite free energies | optimized structures | ωB97M-V/def2-TZVPPD/SMD(water) | consistent thermochemical cycle | ΔG_Buf | ev_doc_393f62b3c7e3_000573_3a9a88f84648 |
| 4 | Oxidation-state comparison | ΔG values | ΔΔG = reduced − oxidized | kcal mol−1 | state shift | ev_doc_ce507d894743_000462_e188a5baaee6 |

## 4. Validation and analysis protocol

All optimized structures were frequency checked for no imaginary modes. Reduced clusters were checked for spin density localized predominantly on one Ce adjacent to the protonation site.

## 5. Private reference results

Table 4: H3BO3 oxidized −0.29, Tris oxidized −2.11, H3BO3 reduced 3.21, Tris reduced 1.97 kcal mol−1; reduced-minus-oxidized shifts are 3.50 and 4.08 kcal mol−1.

## 6. Limitations and interpretation boundaries

This is a truncated cluster with implicit water, not a full solvated MOF ensemble. Energies are model thermochemistry and do not directly equal kinetic constants.
