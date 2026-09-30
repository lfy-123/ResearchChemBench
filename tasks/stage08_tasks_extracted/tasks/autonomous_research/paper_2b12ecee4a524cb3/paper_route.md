# Private paper route

## 1. Scientific objective and author claim

The paper tests whether oxygen insertion into the Fe–C bond of aryl complex 3 proceeds through an Fe(IV)-oxo intermediate rather than a concerted organometallic Baeyer–Villiger (OMBV) attack. The authors claim that oxo migration through TS 7–8 is the operative C–O bond-forming event.

## 2. System and model boundary

The calculated system is the neutral high-spin (quintet) iron complex represented by intermediate 7 and its TS 7–8 geometry, for oxygen insertion into the Fe–C bond. The reported thermochemistry is at 298.15 K and 1 atm, with gas-phase geometry/thermal calculations and THF SMD single-point solvation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize minimum 7 | SI Cartesian geometry | Gaussian 09; M06L/def2-SVP | unconstrained gas phase, quintet, neutral | optimized 7 | ev_doc_d39b5524d55f_000698_cd652557d054; ev_doc_d39b5524d55f_000702_2dab71980229 |
| 2 | Validate 7 and obtain thermal terms | optimized 7 | harmonic frequencies | 298.15 K, 1 atm; zero imaginary modes | Gibbs correction and minimum validation | ev_doc_d39b5524d55f_000698_cd652557d054 |
| 3 | Optimize TS 7–8 | SI TS geometry | Gaussian 09; M06L/def2-SVP | unconstrained gas phase, quintet, neutral | optimized TS | ev_doc_d39b5524d55f_000698_cd652557d054; ev_doc_d39b5524d55f_000702_2dab71980229 |
| 4 | Validate TS and obtain thermal terms | optimized TS | harmonic frequencies and IRC | one imaginary mode; IRC to 7 and 8 | TS validation and Gibbs correction | ev_doc_d39b5524d55f_000698_cd652557d054 |
| 5 | Refine energies | optimized geometries | M06L/def2-TZVPP single points with GD3 and SMD(THF) | gas-phase thermal correction combined with refined electronic energies | solution-phase free energies | ev_doc_d39b5524d55f_000700_8f42bbb8ee1d; ev_doc_d39b5524d55f_000701_338096266cc3; ev_doc_d39b5524d55f_000702_2dab71980229 |

## 4. Validation and analysis protocol

Stationary points were classified by harmonic frequencies; IRC calculations were used to confirm that transition states connect relevant minima. The barrier is the Gibbs free-energy difference G(TS 7–8) − G(7), using the stated composite protocol. The OMBV alternative was separately assessed in the paper by an analogous TS search.

## 5. Private reference results

The paper reports an activation free energy of 5.1 kcal/mol for TS 7–8 and a highly exergonic insertion (ΔG = −47.3 kcal/mol). The OMBV TS 6–9 has a reported barrier of 85.6 kcal/mol. These values and the paper's mechanistic conclusion are evaluator-only references.

## 6. Limitations and interpretation boundaries

The benchmark evaluates reproduction of the reported composite free-energy quantity and validation of the supplied stationary-point identities; it does not establish experimental kinetics, global conformer completeness, or universal superiority of one density functional. Differences caused by legitimate software and numerical implementations must be reported with method details.
