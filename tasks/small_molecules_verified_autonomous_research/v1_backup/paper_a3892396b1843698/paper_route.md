# Private paper route

## 1. Scientific objective and author claim

The paper computes the free-energy surfaces of the two 10-electron sigmatropic shifts of 1,2-dibutadienecyclopropane (3a). The author claim is that cyclopropyl strain favors a double-boat geometry and substantially lowers both [3,3] and [5,5] barriers.

## 2. System and model boundary

3a is a neutral closed-shell hydrocarbon; the public starting minimum has 25 atoms and the SI supplies labeled optimized structures. The paper considers double-boat [3,3] and [5,5] transition states and also compares double-chair alternatives. Energies are Gibbs free energies at 298.15 K with electronic energies and thermochemical corrections defined in the SI.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize minima and saddle points and obtain frequencies | SI Cartesian structures | Gaussian16 | ωB97X-D/def2SVP; stable-wavefunction checks where relevant | optimized geometries, frequencies | ev_doc_9f2c11e4e641_000028_889bf51d6531; ev_doc_a83f54c6ca47_000034_9a7436bb8a08 |
| 2 | Refine electronic energies | step-1 geometries | Gaussian16 | ωB97X-D/def2TZVPP single points | refined energies | ev_doc_9f2c11e4e641_000028_889bf51d6531 |
| 3 | Convert to free energies and compare pathways | steps 1–2 outputs | Goodvibes | Grimme quasi-RRHO, 298.15 K | ΔG barriers and relative energies | ev_doc_a83f54c6ca47_000034_9a7436bb8a08 |

## 4. Validation and analysis protocol

TS assignments were checked by the reported imaginary frequencies (3-TS[3,3] −364.36 cm⁻¹ and 3-TS[5,5] −320.55 cm⁻¹). The free-energy profiles were compared between [3,3] and [5,5] channels and against chair alternatives.

## 5. Private reference results

The reported double-boat activation barriers are 23.5 kcal/mol for [3,3] and 26.2 kcal/mol for [5,5]. The paper reports chair barriers of 38.2 and 36.9 kcal/mol and reverse barriers of 45.0 and 45.1 kcal/mol. These values are private evaluator references.

## 6. Limitations and interpretation boundaries

The benchmark evaluates reproducibility of the reported stationary-point energetics, not experimental kinetics or a unique global search. Alternative conformers, solvation choices, dispersion treatments and frequency protocols may shift values; submissions must report those choices and distinguish failed, approximate or validated stationary points.
