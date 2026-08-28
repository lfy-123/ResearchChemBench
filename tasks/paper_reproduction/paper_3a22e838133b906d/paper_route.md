# Private paper route

## 1. Scientific objective and author claim

The paper tests whether optimized small models of the neutral ortho-phenyl-phosphonate-borane 2a and its mono-dealkylated anion [3] reproduce the experimentally observed P–O and B···O(P) structural changes. The authors claim that the calculated E–O distances (E = P or B) largely parallel the crystallographic changes, with the largest P–O change at the oxygen that loses ethyl substitution.

## 2. System and model boundary

The neutral model is C10H16BO3P, singlet, charge 0; the anion model is C9H13BO3P, singlet, charge −1. Both are isolated gas-phase molecular models with methyl substituents replacing the experimental ethyl/cyclohexyl groups as shown by the SI Cartesian coordinates. Lithium and solvent are absent from the model calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define model neutral and anion | SI Cartesian structures | Gaussian 16 Rev. C.01 | neutral 0/ singlet; anion −1/ singlet; no solvent | molecular input geometries | ev_doc_1ee3111cb1db_000388_0872cb12d625; ev_doc_1ee3111cb1db_000400_1c6ac69f1e5d; ev_doc_1ee3111cb1db_000401_350692fdcb12 |
| 2 | Optimize geometry and energy | model geometries | DFT in Gaussian 16 | B3LYP-D3(BJ)/6-311++G(2d,p) | minimized geometries | ev_doc_1ee3111cb1db_000391_ffd13ad510a7 |
| 3 | Verify stationary points | optimized structures | harmonic frequency calculation | no imaginary frequencies | minimum confirmation | ev_doc_1ee3111cb1db_000391_ffd13ad510a7 |
| 4 | Measure E–O distances | validated geometries | distance extraction | P–O bonds and O(P)···B contact | computed structural observables | ev_doc_18788bc22c6f_000138_6f70f93cdd8d; ev_doc_18788bc22c6f_000140_a9f33a4b3d0a |
| 5 | Compare trends | computed and X-ray distances | paired comparison | neutral versus anion and corresponding experimental structures | trend/fit interpretation | ev_doc_18788bc22c6f_000140_a9f33a4b3d0a; ev_doc_18788bc22c6f_000142_36cf21712871 |

## 4. Validation and analysis protocol

Each optimized structure was accepted only after a frequency calculation showed zero imaginary frequencies. The authors extracted the P–O distances and the intramolecular B···O(P) contact and compared neutral/anion changes with crystallographic 2a/[Li(MeCN)2][3] data. The comparison is qualitative in the prose; the SI supplies the model coordinates and calculation summaries.

## 5. Private reference results

The SI reports neutral and anion frequency jobs as RB3LYP, 6-311++G(2d,p), gas phase, singlet, with zero imaginary frequencies. The neutral and anion optimized Cartesian coordinates are the source reference structures. The paper reports the crystallographic B···O(P) contact changing from 1.666(2) Å (2a) to 1.624(2) Å ([Li(MeCN)2][3]) and a corresponding P–O change from 1.513(1) to 1.525(1) Å; it states that model calculations largely parallel these changes and that the neutral fit is better.

## 6. Limitations and interpretation boundaries

The models omit lithium coordination, solvent, crystal packing, and the experimental bulky substituents. Therefore agreement is a bond-length trend test, not a claim of quantitative crystal-structure prediction or a reaction-energy calculation. Different valid conformer searches and computational methods may give modestly different numbers; conclusions must report the actual search and validation performed.
