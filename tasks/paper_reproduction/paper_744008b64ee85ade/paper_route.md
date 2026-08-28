# Private paper route

## 1. Scientific objective and author claim

The paper investigates whether reactions of carbonyl peroxy radicals with HO2 provide a missing cool-flame source of organic acids. For the acetyl-peroxy system, the authors claim that the singlet surface includes an acid-forming channel and that adding the resulting kinetics improves acid predictions.

## 2. System and model boundary

The central system is CH3C(O)O2 + HO2 at atmospheric pressure. Both reactants are doublets; the authors include singlet and triplet surfaces and neglect intersystem crossing because the atoms are light. The reported rate constants cover 250–1000 K; cool-flame interpretation emphasizes 500–800 K. The measured validation point is acetaldehyde chemistry at 520 K and 760 Torr.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Find conformers and stationary points | CH3C(O)O2 + HO2 complexes and paths a–c | MSTor and Gaussian 16 | Lowest-energy conformers; broken-symmetry open-shell singlets | Initial structures | ev_doc_37892eba5f2b_000282_d052cfe57309 |
| 2 | Optimize minima/TSs and obtain ZPE | Stationary-point guesses | B3LYP-D3(BJ)/def2-TZVP, Gaussian 16 | Frequency scale 0.999; broken-symmetry singlets | Optimized structures, frequencies, ZPE | ev_doc_37892eba5f2b_000282_d052cfe57309 |
| 3 | Refine energetics | Optimized structures | CCSD(T)/CBS from cc-pVTZ and cc-pVQZ | T1 diagnostics; 0 K enthalpy = energy + ZPE | Stationary-point enthalpies | ev_doc_37892eba5f2b_000417_5856138a6202 |
| 4 | Compute thermal kinetics | Energies, frequencies, structures | MESS one-dimensional time-dependent master equation | TST/RRHO for barriers; 1-D Eckart tunnelling; phase-space theory for barrierless steps; Ar bath; LJ parameters; exponential-down transfer | Channel and total rate constants, branching fractions | ev_doc_37892eba5f2b_000420_0a24b2c528de; ev_doc_37892eba5f2b_000421_635345a1ad64; ev_doc_37892eba5f2b_000422_efd07be09ea3 |
| 5 | Apply empirical energy adjustment | Electronic-structure surface | Relative stationary-point energies shifted | Singlet −1.4 kcal/mol; triplet −0.5 kcal/mol | Adjusted rate constants/branching | ev_doc_37892eba5f2b_000243_8782fee8d917 |
| 6 | Test kinetic relevance | Adjusted reaction rates plus NUIG model | PSR transient-to-steady simulation in Chemkin-Pro | 80 s end time; experimental conditions | Formic/acetic acid mole fractions | ev_doc_37892eba5f2b_000434_79b04f6a0028; ev_doc_37892eba5f2b_000443_96e728316679 |

## 4. Validation and analysis protocol

The authors compare singlet (paths b+c) and triplet (path a) rates with Hui et al. measurements, report agreement after empirical energy adjustment, and inspect temperature-dependent branching. They also compare kinetic-model acid mole fractions with SVUV-PIMS measurements. The paper reports 6.0 × 10^-5 acetic-acid mole fraction at 520 K and 760 Torr versus 5.3 ± 1.6 × 10^-5 measured. It reports that the acid-forming singlet branch decreases with temperature and remains 4–11% in the 500–800 K cool-flame range. The authors also considered an in-complex H shift from PC4 to PC3 and found it uncompetitive because its barrier is approximately 10–12 kcal/mol higher than direct dissociation.

## 5. Private reference results

The source reference is the adjusted MESS calculation and its comparison to experiment: negative temperature dependence, good agreement of singlet/triplet rates after adjustment, increasing triplet and decreasing singlet branching with temperature, 4–11% acid-forming path-b fraction at 500–800 K, and the 520 K model/measurement pair above. Exact rate-fit coefficients and stationary-point enthalpies are retained in the paper/SI evidence and are not public task inputs.

## 6. Limitations and interpretation boundaries

The work is a gas-phase atmospheric-pressure/cool-flame model, not a full engine simulation. Peracid products from path a were not detected by SVUV-PIMS because hydroperoxides photodissociate. The relative importance of HO2 and OH pathways outside the reported temperature/pressure scope remains unresolved.
