# Private paper route

## 1. Scientific objective and author claim

The paper studies nitrogen-centred 6–7–6–6 fused-ring helical acridinium cations. Its computational claim is that helicity is configurationally stable; for 1a+ the computed racemisation barrier is 44.0 kcal mol−1.

## 2. System and model boundary

The benchmark system is the isolated P-1a+ cation (C34H26N+, charge +1, singlet), without the BF4− counterion or crystal/solvent environment. The measured endpoint is the electronic-energy barrier from the optimized helical minimum to the helical-inversion transition state.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize P-1a+ minimum | SI Cartesian geometry | Gaussian 16W, (U)CAM-B3LYP/6-31+G(d,p) | closed-shell singlet, charge +1; frequency check | minimum and energy | ev_doc_52d435de715f_000363_5624c37130af; ev_doc_52d435de715f_000049_9ab6a743f062 |
| 2 | Locate inversion TS | optimized minimum and TS guess | Gaussian 16W TS optimization | Opt=(TS, CalcFC, NoEigenTest, MaxStep=5); unrestricted formalism | TS and one imaginary mode | ev_doc_52d435de715f_000363_5624c37130af |
| 3 | Evaluate barrier | minimum and TS energies | energy difference | ΔE = ETS − Emin, reported in kcal mol−1 | racemisation barrier | ev_doc_71b4826ed11e_000180_907d3af285a8 |

## 4. Validation and analysis protocol

The minimum was checked to have no imaginary frequencies. The TS was checked to have exactly one imaginary frequency and that its displacement corresponds to helical inversion. The barrier was obtained from the TS/minimum energy difference and interpreted as evidence for configurational stability, with the usual dependence on electronic structure model and isolated-molecule boundary.

## 5. Private reference results

The SI reports the P-1a+ minimum as having no imaginary frequency and gives its optimized energy as −1365.14086737 Eh. It reports a 1a+ TS with one imaginary frequency and energy −1365.07137556 Eh. The main paper reports a 1a+ racemisation barrier of 44.0 kcal mol−1.

## 6. Limitations and interpretation boundaries

This is an electronic barrier for an isolated cation at the stated computational level, not an experimentally measured rate or a solution free-energy barrier. Different conformers, solvation, thermal corrections, and model chemistries may shift the value. A failed TS search is a scientifically reportable bounded outcome, but it cannot establish the barrier.
