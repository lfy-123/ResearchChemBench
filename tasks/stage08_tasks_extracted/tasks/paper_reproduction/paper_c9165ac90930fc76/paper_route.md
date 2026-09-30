# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT reaction enthalpies to test whether hydrazinium dichloride (HDC) interacts more strongly with Sn(II) iodide than with Pb(II) iodide, and whether this selectivity can retard Sn-rich nucleation and balance Pb–Sn crystallization.

## 2. System and model boundary

The calculated species are BX2 (B = Sn or Pb; X = I) associated with formamidinium iodide (FAI), HDC, or an HDC–DMSO intermediate. The comparison is molecular-complex binding/reaction energy, not a bulk perovskite free energy, solution speciation calculation, or device simulation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build molecular complexes and isolated fragments | SnI2, PbI2, FAI, HDC and HDC-induced intermediate structures | Molecular model construction | Complexes shown in Fig. S12 | Initial geometries | ev_doc_c0aa66d33c65_000158_0b1a46bf5d17; ev_doc_3f28433c0365_000211_0e13849134be |
| 2 | Relax and evaluate energies | Complex and fragment geometries | VASP DFT | PAW; PBE-GGA; DFT-D3; 450 eV cutoff; electronic convergence 1.0e-5 eV; forces below 0.01 eV/A | Optimized structures and total energies | ev_doc_3f28433c0365_000211_0e13849134be; ev_doc_3f28433c0365_000212_5d7465ada835; ev_doc_3f28433c0365_000213_7a64c89fd9ad; ev_doc_3f28433c0365_000214_f6451a2e0f81 |
| 3 | Derive binding energies | Complex and isolated-fragment energies | Energy difference | Reaction-enthalpy/binding-energy convention used in Fig. 2f | Six BX2–ligand values | ev_doc_c0aa66d33c65_000163_c56915fe51c6; ev_doc_c0aa66d33c65_000165_3bc23b91ae3a |
| 4 | Interpret selectivity | Six values | Cross-metal and ligand comparison | Compare Sn versus Pb for each ligand and HDC-induced intermediate | Selective Sn coordination claim | ev_doc_c0aa66d33c65_000165_3bc23b91ae3a; ev_doc_c0aa66d33c65_000176_6cd1411aa5c6 |

## 4. Validation and analysis protocol

The source reports SCF/geometry convergence criteria and compares six complexes: PbI2–HDC–DMSO, PbI2–HDC, PbI2–FAI, SnI2–HDC–DMSO, SnI2–HDC and SnI2–FAI. Interpretation is based on stronger (more negative) association for Sn with HDC-containing species and the resulting proposed suppression of Sn nucleation. The source does not provide reproducible Cartesian coordinates or a full conformer protocol; the benchmark therefore requires explicit geometry-search coverage and convergence evidence from the evaluated Agent.

## 5. Private reference results

Published values (eV): SnI2–HDC–DMSO -1.599; SnI2–HDC -1.352; SnI2–FAI -1.075; PbI2–HDC–DMSO -1.286; PbI2–HDC -1.207; PbI2–FAI -1.158. For each metal, HDC–DMSO is most negative, followed by HDC, then FAI. HDC-containing association is substantially more selective for Sn than Pb, especially for HDC–DMSO.

## 6. Limitations and interpretation boundaries

The source omits Cartesian structures, k-point/pseudopotential variants and a complete conformer/charge protocol. The values should be treated as model-dependent molecular binding energies. They support a coordination/selectivity interpretation but do not alone establish a unique solution mechanism or bulk nucleation free-energy barrier.
