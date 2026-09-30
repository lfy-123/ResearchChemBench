# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to explain regio- and Z-stereoselectivity in photo/copper dual-catalyzed chlorosulfonylation of allenoates. Its computational claim is that two C1-attacked allyl-Cu(III) intermediates, syn,syn-Cu-Int-I-6b and syn,anti-Cu-Int-I-6b, differ in solution-phase Gibbs free energy because the latter is more distorted.

## 2. System and model boundary

The model is neutral singlet Cu/Cl/sulfonyl/allylic complexes for substrate 6b, represented by the SI optimized Cartesian structures. The comparison is between the two explicitly named C1-attacked intermediates; the C3-attacked analogues are reported in the paper but are outside the public task score.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize geometries | SI structures | Gaussian 16 DFT | B3LYP-D3(BJ); LANL2DZ Cu basis/pseudopotential; 6-31G(d,p) other atoms | optimized stationary points | ev_doc_a1b8b2fe7f12_001094_71272630d2bd, ev_doc_a1b8b2fe7f12_001096_3345a070ebb6 |
| 2 | Verify minima and obtain thermal terms | optimized structures | Gaussian 16 harmonic frequencies | same model | no imaginary frequencies; gas Gibbs corrections | ev_doc_a1b8b2fe7f12_001096_3345a070ebb6 |
| 3 | Obtain solution free energies | optimized structures | Gaussian 16 single point | M06; SDD Cu; 6-311+G(d,p) other atoms; SMD acetonitrile, ε=35.7 | Gsol | ev_doc_a1b8b2fe7f12_001099_41ee3818982c, ev_doc_a1b8b2fe7f12_001101_162810a518e1, ev_doc_a1b8b2fe7f12_001103_5846ec28965d, ev_doc_a1b8b2fe7f12_001105_4159d3b2d2cc, ev_doc_a1b8b2fe7f12_001106_11dec88b595b |
| 4 | Compare states and geometry | steps 1–3 | arithmetic and Cartesian measurement | C2-C3-C4 angle and S-C2-C3-C4 dihedral | energy gap and distortion interpretation | ev_doc_974ce0662863_000251_1779f14553f8, ev_doc_974ce0662863_000261_e8f376ba4574, ev_doc_974ce0662863_000262_5dd1b9ad443f, ev_doc_974ce0662863_000263_94a3434b69e6 |

## 4. Validation and analysis protocol

Each optimized structure was frequency-checked as a minimum. The authors compared Gsol values and measured the C2-C3-C4 angle and S-C2-C3-C4 dihedral from the optimized geometries, attributing the energy difference to greater distortion and sulfonyl/n-propyl interaction in syn,anti.

## 5. Private reference results

The paper reports a 2.3 kcal/mol solution-phase free-energy difference, with syn,syn lower than syn,anti. Reported C2-C3-C4 angles are 123.7° (syn,syn) and 129.7° (syn,anti); reported dihedrals are −6.1° and 13.1°. SI Table S1 gives Gsol values for the four intermediates.

## 6. Limitations and interpretation boundaries

This is a two-state model comparison, not a complete reaction free-energy surface. Different legitimate methods, conformer handling, standard states, and thermal treatments may shift numerical values; the task therefore requires method disclosure, minimum validation, and uncertainty/limitation reporting.
