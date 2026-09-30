# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to test whether the two functional sites of the bifunctional ionic-liquid catalyst N,N,N-trimethyl-4-(2,2,2-trifluoroacetyl)benzenammonium triflate ([TMTFABA]OTf) electronically influence one another. The authors claim that the trifluoroacetyl site is less electrophilic than the corresponding model TFAP, while the quaternary-ammonium site is more positively charged than the corresponding [PTMA]OTf model; these effects are invoked to explain epoxide selectivity and epoxide activation.

## 2. System and model boundary

The calculated systems are isolated molecular ion pairs [TMTFABA]OTf and [PTMA]OTf, and neutral 2,2,2-trifluoroacetophenone (TFAP), treated in an acetonitrile continuum. The reported observables are Mulliken charges at the carbonyl carbon and quaternary ammonium nitrogen. The SI does not provide Cartesian coordinates; structures therefore require construction from the reported chemical identities and formulas.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize geometries and verify stationary points | [TMTFABA]OTf, [PTMA]OTf, TFAP | Gaussian 16 Rev. A.03 | B3LYP-D3BJ/6-31G**, IEFPCM(acetonitrile), opt+frequency | Optimized structures and frequencies | ev_doc_669ea2418368_000281_0189b62ccbbf; ev_doc_669ea2418368_000282_7276717c858a; ev_doc_669ea2418368_000283_9a95191e3314 |
| 2 | Compute population analysis | Step-1 optimized structures | Gaussian 16 | M06-2X-D3/def2-TZVP, SMD(acetonitrile), single point, full Mulliken population | Atom-by-atom Mulliken charges | ev_doc_669ea2418368_000283_9a95191e3314 |
| 3 | Compare electronic descriptors | Four selected atom charges | Charge differences between paired models | Carbonyl C: [TMTFABA]OTf vs TFAP; NMe3 N: [TMTFABA]OTf vs [PTMA]OTf | Mechanistic interpretation of site cooperation | ev_doc_e86d3aaecd2b_000253_d6d11a3a02fd |

## 4. Validation and analysis protocol

The frequency calculation is used to establish that each optimized structure is a minimum (no imaginary frequencies). The four atom selections must be explicitly identified by element and local chemical environment, and the charge extraction must be traceable to the final single-point output. The paired differences, signs, and an independent comparison of charge trends are required before a mechanistic interpretation is made.

## 5. Private reference results

The paper reports carbonyl-carbon Mulliken charges of 0.204 for TFAP and 0.200 for [TMTFABA]OTf, and quaternary-ammonium-nitrogen Mulliken charges of 0.036 for [PTMA]OTf and 0.040 for [TMTFABA]OTf. The corresponding qualitative interpretation is reduced carbonyl electrophilicity and increased ammonium-site electrophilicity/epoxide activation. These values and interpretations are evaluator-private.

## 6. Limitations and interpretation boundaries

Mulliken populations depend on basis, geometry, charge partitioning and ion-pair/conformer choice; they are not observables independent of a computational protocol. The paper supplies no coordinates or conformer search, so reproduction from constructed geometries is a protocol-faithful test rather than a guaranteed bitwise reproduction. Charge trends should not be promoted to a unique reaction mechanism without the paper's complementary NMR and control-experiment evidence.
