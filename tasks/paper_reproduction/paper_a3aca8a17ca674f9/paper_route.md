# Private paper route

## 1. Scientific objective and author claim

The authors used computation to explain ligand-controlled methyl versus methylene β-C(sp3)–H activation of 1-methylcyclohexane carboxylic acid. Their claim is that MPAA/MPAThio ligands L7 and L9 diminish the intrinsic methylene preference seen with bidentate pyridone L12, producing methyl-selective chemistry.

## 2. System and model boundary

The model is a Pd-containing CMD activation manifold for the deprotonated cyclic acid under basic conditions. Methyl and methylene β-C–H activation are compared for L7, L9 and L12; the thermochemical comparison is at 373.15 K and 1 atm, with HFIP continuum solvation for electronic single points.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize complexes and CMD transition structures | SI Cartesian structures / conformational starting points | Gaussian 16 | PBE0-D3(BJ)/def2-SVP | Optimized minima and TS geometries | ev_doc_54d7748e04a2_000186_5fdaad027dd8 |
| 2 | Refine electronic energies | optimized structures | Gaussian 16 | PBE0-D3(BJ)/def2-TZVPP, SMD(HFIP), ε=16.7 | single-point energies | ev_doc_54d7748e04a2_000186_5fdaad027dd8; ev_doc_54d7748e04a2_000188_875fb600cd6b |
| 3 | Verify stationary points and obtain thermal terms | optimized structures | Gaussian 16 frequency analysis | 373.15 K, 1 atm | ZPVE/thermal corrections and imaginary-frequency count | ev_doc_54d7748e04a2_000188_875fb600cd6b |
| 4 | Quasi-harmonic thermochemistry | frequency and energy outputs | GoodVibes v3.2 | Grimme entropy correction, 100 cm−1 cutoff, 373.15 K | corrected G values | ev_doc_54d7748e04a2_000190_edf50d18c232 |
| 5 | Connectivity check | each optimized TS | Gaussian 16 IRC | forward/reverse paths | reactant/product-side connectivity | ev_doc_54d7748e04a2_000190_edf50d18c232 |
| 6 | Selectivity comparison | corrected TS free energies | transition-state/Arrhenius analysis | comparable A factors; methyl/methylene symmetry treatment | activation ratios and ligand trend | ev_doc_54d7748e04a2_000180_ceab0bce6845; ev_doc_54d7748e04a2_000181_e26ff1863cfc |

## 4. Validation and analysis protocol

Each claimed TS was frequency-checked as a first-order saddle point and followed by IRC to the appropriate methyl- or methylene-side minima. Barriers were compared on a common reactant reference. Ratios were derived from the Gibbs-energy difference, with the methyl symmetry factor treated as described in SI §2.4.1, and compared with H/D exchange.

## 5. Private reference results

The SI reports ΔG‡ values (kcal mol−1) of 22.87 (L9), 22.32 (L7), and 25.57 (L12) for the methyl channel; methyl–methylene ΔΔG values are 0.33, 0.17 and 0.42, respectively. Reported calculated methyl/methylene ratios are 1.92 (L9), 2.38 (L7), and 1.69 (L12); the L12 experimental ratio is 2.36 and L7/L9 are approximately 6.0. The authors also report methyl-functionalized theoretical maximum yields of 70% (L7) and 66% (L9).

## 6. Limitations and interpretation boundaries

These are model-manifold calculations, not a complete catalytic free-energy surface. Conformer coverage, protonation/aggregation choices and approximate equal pre-exponential factors limit literal kinetic interpretation. The benchmark therefore scores reproducible stationary-point validation, barrier/ratio reporting and consistency with the paper's stated selectivity interpretation, while allowing a bounded failure report when a TS cannot be validated.
