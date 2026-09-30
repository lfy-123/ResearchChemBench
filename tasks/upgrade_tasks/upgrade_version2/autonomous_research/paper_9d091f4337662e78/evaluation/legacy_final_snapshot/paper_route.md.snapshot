# Private paper route

## 1. Scientific objective and author claim

The paper uses conformer thermochemistry as the population-weighting foundation for calculated ECD spectra used to assign absolute configuration of pyrazine derivative 1. The authors claim that compound 1 has a defined absolute configuration supported by agreement between experimental and Boltzmann-averaged calculated ECD.

## 2. System and model boundary

The system is neutral, singlet compound 1 (C24H24N2O4) in the gas phase for conformer thermochemistry at 298.15 K. The SI reports a 16-conformer analysis (Table S1), but supplies Cartesian coordinates publicly only for 1-1, 1-2 and 1-3 (Tables S2-S4); this construction therefore evaluates that reproducible three-conformer subset.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate initial conformers | Compounds 1-5 | Spartan’14 MMFF94 | 10 kcal/mol energy window | Initial conformer ensemble | ev_doc_3181296dbe92_000136_e0b596b31315 |
| 2 | Optimize and characterize minima | Initial conformers | Gaussian 09 DFT | M06-2X-GD3/6-311G(d,p), opt+freq | Optimized minima and frequencies | ev_doc_3181296dbe92_000369_0453109bcdea |
| 3 | Refine energies | Optimized geometries and frequencies | Gaussian 09 | M06-2X-GD3/6-311+G(2d,p), gas phase | Gibbs free energies with thermal corrections | ev_doc_3181296dbe92_000369_0453109bcdea |
| 4 | Population weighting | Gibbs free energies | Boltzmann analysis | 298.15 K; retain populations >1% for later ECD | Conformer populations | ev_doc_3181296dbe92_000370_80cb88d47d45 |
| 5 | Absolute-configuration test | Selected conformers | TD-DFT and SpecDis 1.70.1 | CAM-B3LYP/6-31+G(2d,p), MeOH IEFPCM; Boltzmann average | Calculated ECD compared with experiment | ev_doc_3181296dbe92_000370_80cb88d47d45; ev_doc_3181296dbe92_000136_e0b596b31315 |

## 4. Validation and analysis protocol

Frequency calculations were used to verify true local minima (no imaginary frequencies). Relative Gibbs energies and Boltzmann populations were calculated at 298.15 K. The paper then selected conformers above 1% population for ECD calculations and compared the Boltzmann-averaged spectrum to experiment.

## 5. Private reference results

For the evaluated public subset, SI Table S1 reports populations for the corresponding three entries labelled 1-1, 1-2 and 1-3 as 32.77%, 10.39% and 8.90%, respectively, with relative Gibbs energies 0, 0.680486100 and 0.771969325 kcal/mol. The full table contains 16 entries; the other 13 coordinate sets are not released here.

## 6. Limitations and interpretation boundaries

This benchmark tests reproducibility of reported conformer thermochemistry for a closed three-structure subset, not recovery of the full 16-conformer ensemble or the ECD spectrum. Differences caused by software, numerical settings, frequency scaling, conformer reoptimization, or treatment of low-frequency modes must be reported as limitations rather than silently equated with an exact reproduction.
