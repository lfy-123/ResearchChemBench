# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to test the 1,4-addition of an IPrCuOMe complex to an ortho-quinol imine (Scheme 5c), supporting its claim that a Cu alkoxide is the nucleophile in the dearomative cascade.

## 2. System and model boundary

The modeled system is the neutral singlet IPrCuOMe + ortho-quinol-imine reactant complex and its neutral singlet 1,4-addition product. The SI labels this calculation “1,4-addition of IPrCuOMe to ortho-quinol imine (Scheme 5c)” and supplies SM, TS and PRD geometries and an energy table.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points and locate the addition TS | SM and TS guesses for the neutral complex | Gaussian 16, DFT | B3LYP-D3(BJ)/def2-SVP | SM, TS and PRD stationary-point geometries and frequencies | ev_doc_f3471bee5ceb_000073_7f40c4427d07; ev_doc_f3471bee5ceb_000089_586bf3d2aeb1 |
| 2 | Confirm TS connectivity | optimized TS | Gaussian 16 IRC | IRC from the optimized TS | connection to reactant and product valleys | ev_doc_f3471bee5ceb_000073_7f40c4427d07 |
| 3 | Assemble the Scheme 5c free-energy difference | validated SM, TS and PRD | Gaussian 16 frequency thermochemistry | B3LYP-D3(BJ)/def2-SVP gas-phase electronic energies plus consistent thermal corrections | relative G for the addition pathway | Main PDF pp3–4; SI §7.1, §7.3/Table S4 |
| 4 | Obtain the activation free energy | frequency thermochemistry and refined energies | Gaussian 16 post-processing | relative free energy in kcal/mol | activation free energy and reaction free energy | ev_doc_806c0608b175_000096_3778c58325ea |

## 4. Validation and analysis protocol

The authors require IRC connectivity for optimized transition states and frequency confirmation of minima. They compare SM, TS and PRD free energies and interpret a moderate barrier for Cu-methoxide addition as mechanistic support for Cu alkoxide nucleophilicity. The reported computational general methods are in SI §7.1; the specific Scheme 5c coordinates and table are in SI §7.3.

## 5. Private reference results

SI Table S4 gives the SM/TS/PRD electronic and free energies. The main paper reports an activation energy of 11.3 kcal/mol for this addition. The product is lower in free energy than the reactant complex in the authors' table.

## 6. Limitations and interpretation boundaries

This is a single modeled complex and a single reported pathway, not a proof that every possible Cu species follows the same route. Barrier values depend on conformer, spin/charge assignment, thermochemical convention and electronic-structure model. The benchmark therefore scores reproducible process validation and the source-reported barrier/conclusion within the declared model boundary.

## Source correction (2026-09-18)

The SMD(DCE)/M06/def2-SVP calculations are the separate alkoxycopper equilibrium in Scheme5d/SI§7.4/TableS5. They are not an energy-refinement step for the Scheme5c addition barrier. Main PDF pp3–4 explicitly distinguishes the branches. SI TableS4 endpoint E/G values are reproduced by the completed gas-phase B3LYP-D3BJ/def2-SVP calculations; do not add M06 solvent corrections to this benchmark observable. No public input, scientific objective, numeric target or tolerance was changed.
