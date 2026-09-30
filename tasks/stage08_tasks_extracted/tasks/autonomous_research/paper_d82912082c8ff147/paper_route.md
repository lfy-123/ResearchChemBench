# Private paper route

## 1. Scientific objective and author claim

The paper studies conformer preferences of neutral gas-phase Ala-Ala-Ala (Ala3), especially why the species observed after laser desorption and Ar-jet expansion are not described by a simple equilibrium population of the lowest-electronic-energy conformer. The authors claim that bent structures containing terminal 5-membered and 7-membered intramolecular hydrogen-bonded rings are important, and that the observed Ala3 population reflects both a high conformational temperature (about 450 K) and inter-conformer relaxation in the jet.

## 2. System and model boundary

The system is neutral, isolated L-Ala3 in the gas phase, with free amino and carboxylic-acid termini; the paper treats the molecule as a singlet. Candidate structures are conformers of one covalent connectivity. The conformer analysis uses harmonic thermochemistry and normalized Boltzmann factors; the jet analysis treats barriers below about 800 cm^-1 as potentially traversable.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Explore conformational space | Ala3 molecular structure | Tinker `scan`, MM3 | breadth-first scan, approximately 10^4 trial conformers | trial conformer pool | ev_doc_587a3c47e777_000102_06942bb59f9f, ev_doc_587a3c47e777_000108_bd697fe694ed |
| 2 | Remove duplicates and pre-optimize | trial pool | MOPAC PM7, then Gaussian B3LYP/6-31+G(d)+GD3BJ | duplicate RMSD cutoff <0.2 Å; retain unique structures within approximately 1600 cm^-1 | candidate minima | ev_doc_587a3c47e777_000108_bd697fe694ed |
| 3 | Refine minima | candidate minima | Gaussian, ωB97XD/6-311++G(d,p) | neutral singlet; full optimization | optimized conformers | ev_doc_587a3c47e777_000111_a708b9cdda89, ev_doc_587a3c47e777_000112_d9468f5a36da |
| 4 | Obtain higher-level energies | optimized conformers | Gaussian CBS-4M | single-point energies including ZPE | electronic energies including ZPE | ev_doc_1353336e731f_000004_a1c96647023e, ev_doc_587a3c47e777_000112_d9468f5a36da |
| 5 | Obtain vibrational thermochemistry and IR bands | optimized conformers | Gaussian harmonic analysis, B3LYP-GD3BJ/N07D | harmonic approximation | frequencies, thermochemical corrections and predicted IR bands | ev_doc_587a3c47e777_000112_d9468f5a36da |
| 6 | Estimate thermal populations | CBS-4M energies plus thermochemistry | normalized Boltzmann factors | 10–1000 K; conformational temperature approximately 450 K; sum ψ1 counterpairs where appropriate | relative abundances | ev_doc_587a3c47e777_000293_e303066c51b3, ev_doc_587a3c47e777_000297_6282df262a04, ev_doc_587a3c47e777_000323_d9bbe28c984c, ev_doc_587a3c47e777_000324_c401e2013490 |
| 7 | Model jet relaxation | pairs of optimized conformers | Gaussian QST2/QST3 transition-state searches at ωB97XD/6-311++G(d,p) | compare TS electronic barriers with approximately 800 cm^-1 critical barrier | relaxable graph and post-relaxation populations | ev_doc_587a3c47e777_000112_d9468f5a36da, ev_doc_587a3c47e777_000432_697334ef0c83, ev_doc_587a3c47e777_000438_1bd5e6026ae3 |

## 4. Validation and analysis protocol

The paper identifies minima by converged optimizations and harmonic spectra, labels structures by terminal/backbone hydrogen-bond and dihedral motifs, and compares computed IR bands with IRMPD-VUV features. It analyzes normalized Boltzmann populations without relaxation and then builds a connectivity/relaxation picture from pairwise transition states. The hydrogen-bond definition is XH···Y with X=N/O/F, H···Y from 1.2–2.5 Å, and an angle criterion increasing with distance (source ev_doc_587a3c47e777_000152_4e610daffa52). The authors interpret the remaining experimentally compatible Ala3 structures together with low-barrier relaxation pathways rather than treating the lowest electronic energy alone as decisive.

## 5. Private reference results

The SI Figure 2 presents Ala3 candidates and CBS-4M electronic energies including ZPE: 5N−/7eq/g+(t) 0 cm^-1, 5N−/7eq/7eqC 61, 5N+/7eq/7eqC 209, 5N−/7eq/g−(t) 283, 5N−/7eq/t(t) 322, 5N+/7ax/g−(t) 456, 5N+/7eq/g−(t) 482, 5N+/7eq/t(t) 505, 5N−/7ax/g−(t) 515, 5N−/7eq/g−(c) 520, 5N−/7eq/7axC 523, 5N−/7ax/7eqC 561, 5N−/7eq/g+(c) 562, 5N+/7eq/g+(t) 664, 5N−/5N,5/t(t) 670, 5N+/7eq/g−(c) 701, 5N+/7eq/g+(c) 715, 5N+/7ax/7eqC 739, 5N+/7eq/7axC 782, 5N+/5N,5/t(t) 795, 5N−/7eq/a−(c) 805, 5N+/7eq/a−(c) 974, 5N−/7ax/7axC 1385, and 5/5/t(t) 1147 cm^-1 (layout evidence on SI page 2). The paper reports that the post-relaxation Ala3 non-relaxing set includes 5N−/7eq/t(t), 5N−/7eq/7eqC and 5N−/7eq/g+(t); 5N−/7eq/t(t) is most abundant, while 5N−/7eq/g−(t) cannot be excluded spectroscopically. Reported Ala3 barriers below 800 cm^-1 are 381, 114, 267 and 538 cm^-1 for the four listed Ala3 conversions in Table 1.

## 6. Limitations and interpretation boundaries

The paper's population model assumes a conformational temperature and harmonic thermochemistry; jet relaxation is represented by a barrier cutoff, not a time-resolved master equation. Experimental IRMPD is not a direct population measurement, and two Ala3 conformers remain spectroscopically difficult to distinguish. The SI supplies depictions and labels, not a public Cartesian coordinate set, so exact reproduction of every starting geometry is not an appropriate public-input contract.
