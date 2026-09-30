# Private paper route

## 1. Scientific objective and author claim

The authors use quantum-chemical ^77Se NMR calculations to corroborate assignment of weak signals near 422 and 816 ppm in the spectrum of diselenide 3s to a minor Ar^F-substituted triselenide impurity. They propose rapid exchange between cis and trans triselenide conformers whose calculated energies are similar.

## 2. System and model boundary

The computational system is the neutral, closed-shell Ar^F-substituted triselenide represented by the Cartesian structures in SI Tables S6 (trans) and S7 (cis): Se3 flanked by two identical C6F5 groups (formula C12F10Se3, therefore 25 atoms). An earlier task note said “27-atom”; the supplied complete XYZ files and the formula both give 12 C + 10 F + 3 Se = 25, so the atom-count typo is corrected here without changing the molecular identity or evaluation objective. The comparison concerns optimized molecular minima, relative conformer energy, and three ^77Se shieldings converted to shifts relative to isolated Me2Se. Experimental NMR is in CDCl3 at ambient temperature; the calculations are primarily gas phase.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize diselenide and triselenide conformers | Molecular structures and starting geometries | Gaussian 16 DFT | Geometry survey used B3LYP or PW6B95 with 6-311G(d,p), cc-pVDZ, def2-TZVP or def2-QZVP; reported geometries are PW6B95/def2-QZVP, vacuum | Optimized cis/trans geometries | ev_doc_0dce5914050f_001520_31e08834342b; ev_doc_0dce5914050f_001525_524c30661bee; ev_doc_0dce5914050f_001529_3e798145948d |
| 2 | Compute selenium shieldings and convert to shifts | Optimized geometries and isolated Me2Se standard | Gaussian 16 GIAO | Best-match NMR level B97-2/pcSseg-2, vacuum; Me2Se calculated at same NMR level | ^77Se chemical shifts | ev_doc_0dce5914050f_001520_31e08834342b; ev_doc_0dce5914050f_001513_5a84e8b91568 |
| 3 | Compare with experiment and interpret impurity | Calculated spectra and measured ^77Se spectrum of 3s | Spectral comparison | Minor signals at 422 and 816 ppm in ca. 2:1 integral ratio; conformers within 1 kcal/mol | Assignment of signals to exchanging triselenide | ev_doc_0dce5914050f_001520_31e08834342b; ev_doc_4b7078df2b5a_000155_7200ff8fb055 |

## 4. Validation and analysis protocol

Stationarity of optimized structures is checked by vibrational analysis. The three selenium sites are retained and identified consistently between input and output. Calculated shifts are compared site-by-site or as an explicitly described spectrum-to-spectrum assignment against the observed weak signals; conformer energies are compared after a common zero. Interpretation is limited to semiquantitative corroboration, not proof of a unique dynamic mechanism.

## 5. Private reference results

The SI Figure S251 contains the calculated cis/trans triselenide spectrum and the exact calculated shift locations. The text reports observed minor signals at 422 and 816 ppm in approximately 2:1 intensity and states that cis and trans conformers are within 1 kcal/mol. Exact plotted calculated peak values remain evaluator-private.

## 6. Limitations and interpretation boundaries

The paper does not establish a unique exchange rate or population model. Gas-phase and PCM calculations were compared by the authors, with solvent effects described as minor. Agreement is semiquantitative and depends on conformer labeling, shielding referencing, and the chosen electronic-structure model.
