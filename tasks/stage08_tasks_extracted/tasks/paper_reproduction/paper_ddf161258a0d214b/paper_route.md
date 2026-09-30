# Private paper route

## 1. Scientific objective and author claim

The paper studies activation and bonding of small molecules by the CAAC-stabilized borylene CAAC-B-N(SiMe3)2 (NCB). For methane, the authors claim C-H activation through a bent NCB(H)-CH3 arrangement with B-H formation and report an endergonic transition-state free-energy barrier.

## 2. System and model boundary

The neutral closed-shell type-B complex 8, NCB(H)-CH3, is the methane activation system. Its complete optimized Cartesian geometry is supplied in SI Figure S2. The modeled process is methane C-H cleavage followed by B-H formation in an isolated molecular calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize complexes 1-9 | Complex geometries | Gaussian 16 | M06-2X/6-311G**, no added dispersion | Optimized structures/frequencies | ev_doc_adade75b464d_000086_00521aea7243; ev_doc_adade75b464d_000098_9d5fb30cd787 |
| 2 | NBO analysis | Optimized complexes | Gaussian 16 NBO | NPA, WBI, orbitals, ESP | Electronic descriptors | ev_doc_adade75b464d_000086_00521aea7243 |
| 3 | Methane activation pathway | NCB(H)-CH3/methane | DFT reaction-path calculation | TS search and frequency/thermal analysis; detailed search not disclosed | TS/free-energy profile | ev_doc_adade75b464d_000406_5a9affb019e0 |
| 4 | EDA | Optimized geometries | ADF 2017 | BP86/TZ2P; NCB and ligand fragments | EDA components | ev_doc_adade75b464d_000086_00521aea7243 |

## 4. Validation and analysis protocol

The authors inspect optimized structures and vibrational descriptors, then interpret the methane profile and bent complex through donor-acceptor interactions. A TS is a stationary point with the reaction-coordinate imaginary mode and a connected post-TS pathway. The paper describes an endergonic TS and favorable subsequent B-H formation.

## 5. Private reference results

The reported methane C-H activation barrier is +21.62 kcal mol-1; subsequent product formation is described as thermodynamically favorable.

## 6. Limitations and interpretation boundaries

The supplied paper does not disclose a complete TS search protocol or all TS/product coordinates. The released task therefore evaluates independently validated calculations and uncertainty reporting, not exact undisclosed geometry reproduction.
