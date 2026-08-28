# Private paper route

## 1. Scientific objective and author claim

The paper tests whether metavanadate activates the hydroxyl group of model propargyl alcohol 1a in the AgVO3/Sphos carboxylative cyclization with CO2. The authors claim that coordination of VO3− to the alcohol oxygen makes O–H cleavage exceptionally facile, whereas a pathway in which CO2 is pre-bound to metavanadate is much less favorable.

## 2. System and model boundary

The mechanistic DFT boundary is the model alcohol 1a, monomeric or dimeric metavanadate models, CO2 where needed, and (for later ring formation) silver/Sphos-containing complexes. The central scored comparison is the O–H cleavage portion of the pathway; it is not a complete heterogeneous AgVO3 surface model. The paper describes an O-bound IM1(VO), an alternative C≡C-interacting IM1(VC), an O–H-cleavage TS1(VO), IM(VO), and a CO2-prebound alternative ending in TS1′.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize intermediates and transition states | Model structures for the alcohol/vanadate and subsequent Ag/Sphos species | Gaussian 16 C.01, TPSSh-D3BJ | V and Ag def2-TZVP; O and N ma-def2-SVP; C and H def2-SVP; gas-phase geometry optimization | Stationary-point geometries and frequencies | ev_doc_10e1659ed090_000010_fd0d1b345b4b; ev_doc_12d810a84dd6_000290_f3dac329a324 |
| 2 | Add implicit-solvent electronic energy | Optimized gas-phase geometries | Gaussian SMD single points at M05-2X/6-31G* | 1-hexanol continuum | Solvent electronic-energy correction | ev_doc_10e1659ed090_000010_fd0d1b345b4b; ev_doc_10e1659ed090_000012_1e0d7940b1bb |
| 3 | Refine electronic energies | Optimized geometries | ORCA 5.0.4, ωB97X-2-D3BJ/ma-def2-TZVPP | RI; def2-TZVPP/C auxiliary basis | Refined gas-phase electronic energies | ev_doc_10e1659ed090_000012_1e0d7940b1bb |
| 4 | Assemble free energies and barriers | Frequencies, thermal terms, solvent and refined energies | Authors' quasi-harmonic thermochemistry | Grimme quasi-harmonic correction; −1.89 kcal mol−1 molar correction per solvated species | ΔG profile and activation barriers | ev_doc_10e1659ed090_000010_fd0d1b345b4b; ev_doc_10e1659ed090_000012_1e0d7940b1bb |

## 4. Validation and analysis protocol

Minima were required to be genuine minima and transition states to have the appropriate first-order saddle-point character. The paper compares the direct TS1(VO)→IM(VO) barrier with the CO2-prebound alternative, then analyzes CO2 insertion and later Ag-catalyzed ring closure. In situ FTIR was used as an independent qualitative check: substrate bands at 958 and 887 cm−1 decrease, product bands including 1823 cm−1 increase, and hydroxyl-activated intermediate features at 834, 1048, and 1242 cm−1 grow during the CO2-free preactivation period.

## 5. Private reference results

The reported direct metavanadate-mediated O–H cleavage barrier is ΔG‡ = 2.4 kcal mol−1. The CO2-prebound alternative barrier is ΔG‡ = 26.8 kcal mol−1. The paper additionally reports 19.7 kcal mol−1 for CO2 insertion and a −12.1 kcal mol−1 overall reaction Gibbs energy after protonation, but these are contextual and not the primary benchmark targets.

## 6. Limitations and interpretation boundaries

The article does not provide machine-readable Cartesian coordinates for every mechanistic stationary point; structures must therefore be independently generated from the stated molecular identities and mechanistic endpoint definitions. The benchmark evaluates computationally supported barrier and stationary-point claims, not exact reproduction of a unique conformer or a heterogeneous surface. Differences in conformer coverage, solvation implementation, standard-state convention, and electronic-structure method must be reported and interpreted as limitations.
