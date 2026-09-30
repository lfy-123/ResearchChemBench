# Private paper route

## 1. Scientific objective and author claim

The paper uses compound 5 (hexa-peri-hexabenzo[7]helicene) as a structural calibration case. Its claim is that the calculated mean inner-rim torsion angle agrees closely with experiment, supporting the geometry method used for the derivative series.

## 2. System and model boundary

Compound 5 is a neutral, closed-shell carbon/hydrogen helicene. The authors treat the isolated molecule without symmetry constraints; the supplied starting geometry is the reported Cartesian structure. The structural observable is the mean of the five symmetry-related inner-rim torsions (with equivalent positions counted once as described in the paper).

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain equilibrium geometry | Compound-5 Cartesian coordinates | Gaussian 09 DFT optimization | B3LYP/6-31G(d), neutral singlet, no symmetry constraint | Optimized S0 geometry | ev_doc_6cee37660cb1_000046_5ec4566e0531; ev_doc_6cee37660cb1_000185_3b7e9592867a |
| 2 | Verify stationary point | Optimized geometry | Gaussian 09 frequency calculation | Same electronic state/model | Frequencies; no imaginary modes | ev_doc_6cee37660cb1_000046_5ec4566e0531; ev_doc_6cee37660cb1_000185_3b7e9592867a |
| 3 | Extract structural metric | Validated optimized geometry | Multiwfn 3.8 (dev) / equivalent dihedral analysis | Inner-rim torsion convention and symmetry averaging | Mean torsion angle | ev_doc_6cee37660cb1_000161_7b23280f2256; ev_doc_6cee37660cb1_000203_541d85e0e0cf |

## 4. Validation and analysis protocol

The optimized structure is accepted as a minimum only if the frequency calculation has no imaginary frequencies. Torsions are measured on the inner rim using a documented atom-index definition, with sign handled consistently (absolute magnitudes may be used because the paper reports the mean distortion angle). The result is compared with the experimental structural value reported in the main text.

## 5. Private reference results

The paper reports a calculated mean torsion angle of 27.1 degrees for compound 5 and an experimental value of 27.0 degrees (ev_doc_6cee37660cb1_000203_541d85e0e0cf). The supplementary material reports the optimized coordinates and a selected geometric comparison (ev_doc_5e1275b9a308_000143_e50193d6cd32; ev_doc_5e1275b9a308_000144_3bb93c300503; ev_doc_5e1275b9a308_000145_dda04376541d).

## 6. Limitations and interpretation boundaries

This is a gas-phase, single-molecule structural calibration, not a claim that one level of theory is universally accurate. Different conformer searches, torsion conventions, optimization thresholds, dispersion treatments, or thermal/solvent models can shift the value. The evaluator therefore scores a documented, validated mean inner-rim torsion and its comparison, while retaining method and uncertainty disclosures.
