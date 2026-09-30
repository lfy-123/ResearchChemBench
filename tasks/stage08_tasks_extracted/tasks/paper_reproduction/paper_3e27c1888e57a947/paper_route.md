# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to explain why the allylic radical derived from 1,3-butadiene undergoes selective SO2 capture at the terminal (1,4) site rather than the alternative internal (1,2) site. The authors claim that the 1,4-addition transition state is kinetically preferred for Int2-a, consistent with the absence of a 1,2-addition byproduct.

## 2. System and model boundary

The computational system is the neutral doublet allylic radical Int2-a derived from 1,3-butadiene plus SO2. The reported stationary-point structures are isolated molecular models; reaction free energies are evaluated at 298.15 K with solution-phase single-point energies in DMSO. The subsequent defluorination/product-forming chemistry is outside the barrier comparison.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | Reported structures for Int2-a and SO2-addition TSs | Gaussian 16 | PBE1PBE with GD3BJ, 6-31G(d), gas phase | Optimized minima/TS geometries | ev_doc_dae8dc0cd8db_000382_de8c4212446d; ev_doc_dae8dc0cd8db_000388_c6419d5407eb |
| 2 | Classify stationary points and obtain thermal terms | Optimized geometries | Gaussian 16 frequency analysis | 298.15 K | Gibbs thermal corrections; minima/TS classification | ev_doc_dae8dc0cd8db_000382_de8c4212446d |
| 3 | Add solvent electronic energy | Optimized geometries | Gaussian 16 single point | PBE1PBE/6-311+G(d,p), SMD(DMSO) | Solution-phase SCF energies | ev_doc_dae8dc0cd8db_000383_c50fcb641a51; ev_doc_dae8dc0cd8db_000384_4e46baac2dcb |
| 4 | Compare barriers | Thermal terms and solution energies | Composite free-energy calculation | Relative to Int2-a | 1,4 and 1,2 SO2-addition ΔG‡ values | ev_doc_e2120ae96275_000205_29d3c7ff1e4b; ev_doc_e2120ae96275_000209_d71f39d2a050; ev_doc_e2120ae96275_000211_e92407999616 |
| 5 | Verify connectivity | Candidate TSs | IRC | Forward/reverse paths | TS-to-intermediate/product connectivity | ev_doc_dae8dc0cd8db_000382_de8c4212446d |

## 4. Validation and analysis protocol

Each proposed TS was frequency-checked and IRC-checked. Int2-a was treated as the common reference. The authors also computed spin populations for Int2-a and Int2-b with Multiwfn and used them qualitatively to discuss terminal-site preference.

## 5. Private reference results

The paper reports ΔG‡ = 3.2 kcal/mol for TS2-a (1,4 addition) and 7.6 kcal/mol for TS2-c (1,2 addition), a 4.4 kcal/mol difference. It reports that TS2-a is connected to the 1,4 pathway and TS2-c to the 1,2 pathway; no 1,2-addition byproduct was observed. The Int2-a spin populations are 0.75 at C4 and 0.71 at C2.

## 6. Limitations and interpretation boundaries

These are single-level molecular-model calculations and do not establish a complete catalytic free-energy surface. Conformer, entropy, solvation, and model-chemistry sensitivity may affect absolute barriers. The evaluator therefore scores the reported observables and stationary-point/connectivity validation, while accepting a transparent bounded-failure report when a validated TS cannot be located.
