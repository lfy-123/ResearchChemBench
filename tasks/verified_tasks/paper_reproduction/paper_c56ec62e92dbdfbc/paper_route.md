# Private paper route

## 1. Scientific objective and author claim

The paper asks why the CBSCA-catalyzed oxa-Pictet–Spengler reaction of β-aryl ethanol 1a with ketal 2a gives predominantly (R)-3a. The authors claim that C–C bond formation by intramolecular arene addition to a monomeric-catalyst-bound oxocarbenium ion is enantiodetermining. Their lowest-free-energy R- and S-forming C–C transition structures differ by 2.0 kcal mol⁻¹, consistent with the measured 91% ee.

## 2. System and model boundary

The modeled system contains one neutral, singlet molecule each of catalyst 4i, 1a (2-(3-hydroxyphenyl)ethanol), and 2a ((1,1-dimethoxyethyl)benzene), leading to 1-methyl-1-phenylisochroman-6-ol (3a). The computational comparison uses separated starting materials as the free-energy reference and compares the lowest validated pathways leading to R and S product. Explicit molecular sieves, bulk aggregation, counterions, and kinetic mass transport are outside the DFT model. Solvent is represented implicitly for final electronic energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish catalyst conformational space | Catalyst 4i | manual bond rotations, then CREST/xTB | GFN2-xTB; 26 conformers in about 6 kcal mol⁻¹; 8 distinct NCI patterns advanced | lowest and higher catalyst conformers | SI pp. 74–75; ev_doc_817598f88e40_001060_144d11b67b0b, ev_doc_817598f88e40_001062_4206c9d86a1e |
| 2 | Enumerate stereochemical C–C pathways | catalyst-bound oxocarbenium/arene complex | conformational construction and DFT searches | four stereochemical pathways, two ending in each product enantiomer | candidate C–C-forming TSs | Main text computational section; SI p. 75; ev_doc_5f6e819ae4bf_000075_1e4c87f94c82, ev_doc_817598f88e40_001072_5eedd514d14f |
| 3 | Expand TS conformer coverage | provisional lowest R- and S-forming TSs | CREST constrained sampling with NCI utility | C–C constraint force constant 0.50; 60 conformers over 0–5 kcal mol⁻¹; 30 distinct NCI geometries advanced | conformer ensembles for major/minor pathways | SI p. 75; ev_doc_817598f88e40_001060_144d11b67b0b through ev_doc_817598f88e40_001062_4206c9d86a1e |
| 4 | Optimize stationary points and validate | candidate minima and TS geometries | Gaussian 16, B3LYP-D3(BJ)/6-31G* gas phase (SI also describes 6-31+G(d) in the conformer discussion) | harmonic frequencies; QRC from TSs | optimized minima and one-imaginary-frequency TSs | Main text; SI p. 74; ev_doc_5f6e819ae4bf_000075_1e4c87f94c82, ev_doc_5f6e819ae4bf_000076_4c976b416206, ev_doc_817598f88e40_001052_99958ef2cc7b, ev_doc_817598f88e40_001056_bd869ab417d1 |
| 5 | Refine energies in reaction medium | optimized stationary points | ωB97XD/6-311++G** PCM(xylene mixture), Gaussian 16 | single-point electronic energies | refined electronic energies | ev_doc_5f6e819ae4bf_000079_a662ab2eeeff through ev_doc_5f6e819ae4bf_000082_00d2f47c8336 |
| 6 | Obtain comparable free energies | frequencies and refined electronic energies | qRRHO post-processing | 298.15 K; 100 cm⁻¹ cutoff; free-energy correction from optimization added to refined electronic energy | reaction free energies and ΔΔG‡ | SI p. 74; ev_doc_817598f88e40_001056_bd869ab417d1, ev_doc_817598f88e40_001057_ff31caf4b530 |
| 7 | Interpret asymmetric induction | lowest R/S TS pair | energy decomposition and NCI analysis | compare catalyst distortion and stabilizing contacts | mechanistic origin of selectivity | Main text Figure 3 discussion and SI analysis |

## 4. Validation and analysis protocol

All starting geometries and intermediates were required to be minima; every TS was characterized by one imaginary frequency. QRC calculations connected transition structures toward neighboring stationary regions. Candidate coverage included four stereochemical pathways and extensive constrained conformer sampling. The lowest R- and S-forming C–C transition structures were compared on a common separated-reactants reference, and the subsequent rearomatization barriers were also evaluated to establish which step controls selectivity.

## 5. Private reference results

- Lowest C–C-forming R pathway: ΔG‡ = 12.2 kcal mol⁻¹ relative to separated starting materials.
- Lowest C–C-forming S pathway: ΔG‡ = 14.2 kcal mol⁻¹ on the same reference.
- ΔΔG‡(S−R) = +2.0 kcal mol⁻¹; R is favored; predicted ee is about 93% at room temperature versus experimental 91% ee.
- Lowest subsequent rearomatization TSs are 7.9 kcal mol⁻¹ (R route) and 10.2 kcal mol⁻¹ (S route), below their corresponding C–C-forming TSs.
- The authors therefore identify concerted arene C–C bond formation/phenol deprotonation as enantiodetermining. The major TS has stronger favorable noncovalent interactions, including an aromatic CH–π contact, and lower catalyst distortion.

Sources: main text computational discussion, especially ev_doc_5f6e819ae4bf_000110_d48593005e1b, ev_doc_5f6e819ae4bf_000114_a66aaca409b1, and ev_doc_5f6e819ae4bf_000116_8828ddc4cb7e; SI pp. 74–85.

## 6. Limitations and interpretation boundaries

The numerical agreement is method- and conformer-dependent and does not prove that every conceivable pathway was exhausted. The model treats a monomeric catalyst and implicit solvent, whereas experiments show catalyst aggregation can affect selectivity. QRC is weaker than a full IRC for connectivity validation. The reported barriers are relative to separated starting materials and should not be mixed with differently referenced values. The DFT result supports, but does not alone establish, the complete kinetic mechanism under all catalyst loadings.
