# Private paper route

## 1. Scientific objective and author claim

The paper investigates the gas-phase single-collision reaction of ground-state SiN radical with isoprene and claims that hydrogen-loss chemistry produces at least two cyclic methylazasilacyclohexadienylidene isomers whose calculated reaction energies agree with the crossed-beam exoergicity.

## 2. System and model boundary

Reactants are SiN (X2Sigma+) and isoprene (2-methyl-1,3-butadiene, C5H8, X1A'). The product channel is SiNC5H7 + H. The computational boundary is the isolated-molecule electronic potential-energy surface; the paper does not claim a complete statistical product distribution. The experiment supplies a collision energy of 25 +/- 1 kJ mol-1 and an exoergicity of -162 +/- 27 kJ mol-1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Enumerate reaction surface | SiN + isoprene and candidate intermediates/products | Gaussian 16 Rev. C.01 | CBS-QB3; neutral system; reactant doublet and product singlet surfaces | Optimized stationary points | ev_doc_fb5e0df992fe_000112_12a2391d54ba; ev_doc_fb5e0df992fe_000116_51ca74d13d3f |
| 2 | Characterize minima and transition states | Each optimized stationary point | Gaussian 16 | Harmonic frequencies; minima have zero imaginary frequencies; TS have exactly one | Validated minima/TS and IRC connectivity | ev_doc_fb5e0df992fe_000112_12a2391d54ba |
| 3 | Follow favored channels | Terminal-carbon additions, intermediates, ring closures, H shifts, H loss | CBS-QB3 PES calculations | Compare energetics to approximately 24–25 kJ mol-1 collision-energy access | Paths to cyclic products | ev_doc_fb5e0df992fe_000229_135eab69236f |
| 4 | Compare product thermochemistry | 38 product isomers P1–P38 | CBS-QB3, E0 = electronic energy + ZPVE | Reaction energies relative to separated SiN + isoprene | Product ranking and experimental comparison | ev_doc_fb5e0df992fe_000229_135eab69236f |

## 4. Validation and analysis protocol

The paper requires frequency characterization of all stationary points and IRC checks for TS connectivity. It reports 38 product isomers, including six-membered cyclic, five-membered cyclic, and acyclic structures. The experimental mass channel is SiNC5H7 at m/z 109 with atomic-H loss; the translational-energy endpoint gives -162 +/- 27 kJ mol-1. The authors interpret broad/symmetric angular scattering and long-lived intermediates as indirect complex-forming dynamics. Their mechanistic interpretation is nitrogen-centered terminal-carbon addition, isomerization, cyclization, hydrogen migration, and H elimination.

## 5. Private reference results

SI CBS-QB3 (0 K) energies: SiN -343.624031 Eh; isoprene -194.897950 Eh; P1 -538.081719 Eh; P2 -538.079462 Eh. Main-text reaction energies are P1 -156 and P2 -150 kJ mol-1, both inside -162 +/- 27 kJ mol-1. P1 is 4-methyl-1-aza-2-silacyclohexa-3,5-dien-2-ylidene and P2 is 5-methyl-1-aza-2-silacyclohexa-3,5-dien-2-ylidene.

## 6. Limitations and interpretation boundaries

The paper explicitly says the PES mapping is not exhaustive, especially for acyclic channels, and that additional channels may exist. Agreement with the experimental exoergicity supports compatibility, not a uniquely measured product branching ratio. The reported product structures are hidden from Agent-visible inputs in this benchmark.
