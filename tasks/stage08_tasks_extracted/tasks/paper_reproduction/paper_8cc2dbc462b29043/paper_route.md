# Private paper route

## 1. Scientific objective and author claim

The paper explains why the exo precursor (iso-1) generates an anti-Bredt olefin (ABO) while the endo precursor (iso-2) is kinetically unproductive, and assigns the operative elimination pathway using potential-energy surfaces, stationary-point calculations, NEB, and rate constants. The authors claim that fluoride first gives a pentacoordinate siliconate complex and that iso-1 most plausibly reaches the ABO through near-simultaneous loss of triflate and TMSF; iso-2 has a much larger barrier and an unstable product.

## 2. System and model boundary

The system is the 2-exo- and 2-endo-trimethylsilyl-1-trifluoromethanesulfonyl bicyclo[2.2.1]heptane pair with fluoride. Coordinates are SI Section 11; all structures are gas-phase molecular calculations. Reported observables are stationary-point free energies/barriers, pathway ordering, structural descriptors, and Eyring rate constants. NBO/NAO analysis is interpretive and not essential to the benchmark.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Benchmark and choose model chemistry | ABO structural parameters and trial barriers | DFT in ORCA | BP86/SVP/D3BJ selected | model choice | ev_doc_3882cf5f3295_000025_2748d26a1b76; ev_doc_3882cf5f3295_000026_fd1508fba61d |
| 2 | Optimize minima and transition structures | iso-1, iso-2 and intermediates | ORCA 6.0 optimization/frequencies | BP86/SVP/D3BJ; stationary points classified by Hessian | geometries and frequencies | ev_doc_3882cf5f3295_000026_fd1508fba61d |
| 3 | Explore fluoride approach and leaving-group dissociation | precursor/PCC coordinates | 1D PES scans | Si–F, C1–OTf, and for iso-2 C2–Si coordinates | scan profiles and candidate extrema | ev_doc_3882cf5f3295_000037_a9832df57d84; ev_doc_3882cf5f3295_000063_7ade9b4cc886 |
| 4 | Compare coupled eliminations | iso-1 PCC | 2D PES scan | C1–OTf and C2–Si grid | MEP and alternative paths | ev_doc_3882cf5f3295_000094_f8867ce20935 |
| 5 | Refine paths | reactant/product pairs | NEB followed by optimization/frequency checks | each proposed step | barriers and TS assignments | ev_doc_3882cf5f3295_000123_8f6a2cd6fec8; ev_doc_3882cf5f3295_000131_ba6878e676fa; ev_doc_3882cf5f3295_000133_ea025d39fdd5 |
| 6 | Estimate kinetics | activation free energies | Eyring equation | transmission coefficient 1, standard concentration 1 mol/L, temperature as specified in SI | forward/backward rates | ev_doc_3882cf5f3295_000134_7f9883299a05; ev_doc_3882cf5f3295_000161_7d1403e28527 |

## 4. Validation and analysis protocol

The authors checked minima for no chemically relevant imaginary mode and TSs for one reaction-coordinate imaginary mode, while discounting methyl rotations. They compared iso-1 and iso-2 PESs, checked sequential versus coupled bond loss, and used rate-constant ratios to interpret reversibility and kinetic feasibility.

## 5. Private reference results

The SI reports approximately 12, 30, and 22 kcal/mol for the three iso-1 alternatives (MEP/concerted, E1-like, E1cb-like), NEB barriers of 10.61 kcal/mol for B→C, 36.55 for D→E, and 2.97 for E→F, plus rate constants 3.02×10^8 and 8.07×10^7 for B⇌C, 2.09×10^-12 and 3.64×10^10 for D⇌E, and 1.11×10^11 and 1.37×10^11 for E⇌F. The SI also describes the fluoride approach as nearly barrierless and the iso-2 product as unstable.

## 6. Limitations and interpretation boundaries

The paper uses approximate scans and a modest model chemistry; barriers are not universal observables. The benchmark therefore scores agreement with source-reported quantities and qualitative pathway conclusions, requires method/validation disclosure, and permits an explicit bounded-failure report when a stationary point cannot be located.
