# Private paper route

## 1. Scientific objective and author claim

The authors used electronic-structure calculations to explain why DIBAL-H reduces the imine of the amidine portion of spiro-iminoindoline-pyrazoline 3a selectively, while leaving the hydrazone imine comparatively less reactive. Their claim is that the amidine imine carbon is more positively charged/electron-deficient.

## 2. System and model boundary

The computed object is neutral compound 3a, also named 2',4',5'-triphenyl-2',4'-dihydrospiro[indoline-3,3'-pyrazole] bearing the p-toluenesulfonyl-substituted amidine/hydrazone functionality. The SI gives a 67-atom standard-orientation geometry and reports zero imaginary frequencies. The analysis concerns NPA atomic charges and electrophilicity/reactivity indices for the optimized structure; it does not establish a full DIBAL-H reaction pathway.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Locate a stationary point for the key optimized structure | Compound 3a geometry | Gaussian 16 DFT geometry optimization | M06-2X with Grimme D3BJ dispersion; 6-311++G(d,p) for all atoms; gas-phase as reported | Optimized geometry, thermochemical quantities, vibrational check | ev_doc_3234b698fd08_000706_652565bb0dd3; ev_doc_3234b698fd08_000707_a941d937dc4c |
| 2 | Characterize electronic properties | Optimized 3a | Gaussian 16 natural population analysis and reactivity-index analysis | NPA; electrophilicity and nucleophilicity indices on key optimized structures | Atomic NPA charges and indices | ev_doc_3234b698fd08_000710_9b82f418bc96; ev_doc_3234b698fd08_000711_8b98d1aef611 |
| 3 | Compare the two imine carbons | NPA output for amidine and hydrazone imine carbons | Direct quantitative comparison | Charge sign convention and atom assignments from the optimized structure | Relative electron deficiency used to rationalize reduction selectivity | ev_doc_3234b698fd08_000721_60019e1ccab6 |

## 4. Validation and analysis protocol

The SI reports 0 cm−1 imaginary frequency for the optimized structure. The reported NPA values are +0.518 for the amidine imine carbon and +0.239 for the hydrazone imine carbon. The authors interpret this ordering as greater electron deficiency at the amidine imine, consistent with electrophilicity analysis and with preferential DIBAL-H reduction. The SI attributes enhanced electrophilicity in part to the strongly electron-withdrawing p-toluenesulfonyl group. Experimental follow-up reports 70% isolated yield for reduction with DIBAL-H; NaBH4 and LiBH4 also work (65% and 54%), whereas Pd/C hydrogenation gives no product under the tested pressures.

## 5. Private reference results

The hidden charge targets are +0.518 (amidine imine carbon) and +0.239 (hydrazone imine carbon), in units of |e| under the NPA convention. The amidine value is higher by 0.279 |e|. The hidden qualitative conclusion is that the amidine imine is more electron-deficient/electrophilic and this supports its preferential hydride reduction; this is a mechanistic interpretation, not proof of a complete transition-state pathway.

## 6. Limitations and interpretation boundaries

Partial atomic charges and electrophilicity indices are model- and geometry-dependent descriptors, not observables. The source does not provide a complete explicit DIBAL-H transition-state calculation. Alternative conformers, functionals, population schemes, solvation treatments, and atom-labeling conventions can shift numerical charges, so comparison must identify the atoms and method used. Experimental selectivity supports the interpretation but does not by itself validate the exact charge values.
