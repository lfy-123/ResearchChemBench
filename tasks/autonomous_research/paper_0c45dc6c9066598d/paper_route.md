# Private paper route

## 1. Scientific objective and author claim

The paper uses molecular dipole moments to test whether incorporating 4-cyanopyridine (CNPy) through an O–H⋯N hydrogen bond increases the polarity of 4-alkyloxy-2-fluorobenzoic acids, thereby rationalizing the enhanced positive dielectric anisotropy of the complexes. The authors claim that the cyano-bearing acceptor contributes a strong longitudinal dipole to the supramolecular complex.

## 2. System and model boundary

The computational comparison is between isolated 8OBAF and 14OBAF acids and their 1:1 complexes with 4-cyanopyridine. The acid is 4-alkyloxy-2-fluorobenzoic acid; the alkoxy-chain carbon count is eight or fourteen. The complex is modeled as a hydrogen-bonded acid/4-cyanopyridine pair, with the acid hydroxyl proton directed toward pyridine N. The reported observable is the molecular dipole moment in Debye.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build acid and hydrogen-bonded complex models | Structures shown for nOBAF and nOBAF:CNPy | Molecular model construction | 1:1 acid:CNPy pair; O–H⋯N contact | Initial geometries | ev_doc_67e381560d53_000051_f581a7626ed4; ev_doc_67e381560d53_000052_4c39c093c447 |
| 2 | Optimize geometries | Initial molecular models | DFT, Gaussian 09 | B3LYP/6-311+G(d,p) | Optimized structures/wavefunctions | ev_doc_67e381560d53_000209_2a61acf58651; ev_doc_67e381560d53_000210_5cd9a3d853b0 |
| 3 | Extract polarity | Optimized wavefunctions | Gaussian 09 dipole analysis | Same B3LYP/6-311+G(d,p) level | Dipole moments in Debye | ev_doc_67e381560d53_000230_e01cec56b8fe |

## 4. Validation and analysis protocol

The paper compares the acid and complex dipoles and interprets a larger complex dipole as computational support for the cyano-group structure–property explanation. The surrounding experimental boundary is that 8OBAF:CNPy has positive dielectric anisotropy, including Δε = +4.0 at 102 °C, compared with approximately 0.6 for pure 8OBAF; these measurements are context rather than computational targets (ev_doc_67e381560d53_000213_5c7f385ad0fc).

## 5. Private reference results

Table 4 reports: 8OBAF 2.8 D; 14OBAF 2.9 D; 8OBAF/CNPy 4.5 D; 14OBAF/CNPy 4.53 D (ev_doc_67e381560d53_000227_e5950cdf4e6d; ev_doc_67e381560d53_000230_e01cec56b8fe). Thus both complexes have larger reported dipoles than their corresponding acids.

## 6. Limitations and interpretation boundaries

The article does not publish Cartesian starting coordinates, optimization convergence details, conformer enumeration, or an uncertainty analysis. Dipole moments are geometry- and method-dependent. A successful reproduction should therefore report the exact structures, charge/multiplicity, conformer/geometry-search choices, convergence and frequency or other stationary-point validation, and should distinguish a computed result from the paper's reference values. The dipole comparison supports polarity enhancement but does not alone prove bulk dielectric anisotropy or molecular alignment.
