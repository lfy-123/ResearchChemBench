# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to test whether catalyst F binds differently to phenolic and alcoholic acceptors and their glycosylation products, as an explanation for product inhibition and incomplete conversion. The authors claim preferential catalyst binding to phenolic substrate 2g, while alcohol product 3w competes effectively with alcohol substrate 2w.

## 2. System and model boundary

Neutral, singlet monomers 2g, 2w, 3g, 3w and pyridinium bromide catalyst F in toluene. Complexation is noncovalent; interaction energy is defined as E(X-F)-E(X)-E(F). The reported structures are optimized stationary-point geometries and selected low-Gibbs-energy complex conformations.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Locate and validate complex minima | monomer structures and several complex starting arrangements | Gaussian 16, B3LYP-D3(BJ)/6-311G(d,p), IEFPCM | toluene, 1 M standard state; neutral singlets | optimized geometries, frequencies and Gibbs corrections at 383.15 K | ev_doc_d0edfe375cd3_000964_850425ce3f4b |
| 2 | Refine electronic energies | optimized complexes and isolated monomers | ORCA 6.0.0 RI-revDSD-PBEP86-D4/Def2-QZVPP | Def2/JK and Def2-QZVPP/C; SMD toluene, 1 M | electronic energies | ev_doc_d0edfe375cd3_000964_850425ce3f4b |
| 3 | Compute binding energies | energies from step 2 | arithmetic | ΔE=E(X-F)-E(X)-E(F) | four interaction energies | ev_doc_d0edfe375cd3_001003_ddb087d29a58 |
| 4 | Interpret contacts | selected complexes and wavefunctions | Multiwfn IGMH and electrostatic-potential analysis | IGMH Hirshfeld density; isovalue 0.003 a.u. | interaction maps and qualitative contact assignments | ev_doc_d0edfe375cd3_000964_850425ce3f4b |

## 4. Validation and analysis protocol

Several arrangements were optimized for each complex; the lowest reported relative Gibbs-energy arrangement was used for the comparative binding analysis. The authors interpret green IGMH surfaces as weak van der Waals/stacking or hydrogen-bond contacts. The comparison is between phenol substrate/product and alcohol substrate/product, not an absolute kinetic model.

## 5. Private reference results

Table S24 reports interaction energies (kcal mol−1): 2g-F −13.82354459, 3g-F −7.818101589, 2w-F −7.553865435, and 3w-F −7.669501881. The associated ordering is 2g strongest; 3g weaker; 3w marginally stronger than 2w. Tables S20–S23 report the selected conformations as Int 1-a, Int 3-a, Int 1′-a and Int 3′-a.

## 6. Limitations and interpretation boundaries

The calculation samples reported low-energy conformations rather than proving global minima, and interaction energies are not free energies of catalysis. Product inhibition is a mechanistic interpretation supported by binding comparisons and experiments, not established by binding energy alone.
