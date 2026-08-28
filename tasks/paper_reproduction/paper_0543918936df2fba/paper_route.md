# Private paper route

## 1. Scientific objective and author claim

The paper tests how Pt incorporation into Ni changes hydrogen binding and the ability of adsorbed 5-hydroxymethylfurfural (HMF) to change from a thermodynamically preferred parallel geometry to a tilted geometry associated with selective carbonyl hydrogenation. The authors claim that Pt weakens H2/H* adsorption and lowers the parallel-to-tilted HMF configurational barrier, while MFI confinement weakens BHMF binding and suppresses further hydrogenolysis.

## 2. System and model boundary

The periodic models reported by the authors are three-layer 4×4 Ni(111), three-layer 4×4 NiPt(111), and 3×4 SiO2(101), separated by 15 Å vacuum with the bottom layer fixed. Supported catalysts were represented by a Ni10Pt1 cluster on SiO2(101). Adsorbates include H2, two adsorbed H atoms, HMF in parallel and tilted geometries, and BHMF. The benchmark public core is restricted to ideal Ni(111) and one top-layer Pt-substituted 4×4 Ni(111), because the paper does not disclose coordinates sufficient to uniquely reconstruct the SiO2-supported Ni10Pt1 models.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Construct periodic catalyst models | Ni(111), NiPt(111), SiO2(101), Ni10Pt1 cluster | VASP periodic DFT | 4×4 three-layer metal slabs; 3×4 SiO2(101); Ni10Pt1/SiO2; 15 Å vacuum; bottom layer fixed | Relaxable clean catalyst slabs | Main paper §2.5, page 5, ev_doc_935ab153accc_000193_5d99d8f6f25f and surrounding layout block |
| 2 | Optimize clean and adsorbate-covered structures | Slabs plus H2, 2H*, HMF, or BHMF | GGA-PBE with Grimme DFT-D in VASP | 450 eV cutoff; 3×3×1 Monkhorst-Pack mesh; forces below 0.05 eV/Å | Optimized adsorption structures | Main paper §2.5, page 5; Fig. 9 caption, page 9 |
| 3 | Calculate adsorption energies | Optimized adsorbate/slab, isolated adsorbate, clean slab energies | Total-energy differences | Eads = E(gas/slab) − E(gas) − E(slab) | H2, H*, HMF and BHMF adsorption energies | Main paper Eq. 6 and explanatory text, page 5 |
| 4 | Compare HMF configurations | Parallel and tilted HMF structures on Ni(111) and NiPt(111) | DFT energy profile (specific path algorithm not reported) | Same electronic-structure model; endpoints shown in Fig. 9 | Parallel-to-tilted energy barriers | Main paper Fig. 9 and §3.3, pages 9–10 |
| 5 | Interpret selectivity | Computed adsorption/barrier trends plus DRIFTS and catalytic measurements | Cross-comparison | H2 environment, catalyst identity, adsorption orientation | Mechanistic explanation of BHMF selectivity | Main paper §3.3 and Fig. 10, pages 8–10 |

## 4. Validation and analysis protocol

The authors report optimized adsorption structures for H2, 2H*, and both HMF orientations, use a common adsorption-energy definition, and compare like-for-like Ni and NiPt models. Experimental H2-TPD is used as qualitative support for weaker hydrogen binding after Pt addition, while time-resolved DRIFTS is used to support hydrogen-induced tilted HMF adsorption on Pt-containing catalysts. The paper does not report transition-path algorithm, image count, vibrational analysis, spin settings, smearing, pseudopotential release, electronic convergence, or dipole correction; these omissions limit exact numerical reproduction and require independent numerical validation in the benchmark.

## 5. Private reference results

- Molecular H2 adsorption energy: Ni(111) −0.38 eV; NiPt(111) −0.23 eV.
- Reported H* adsorption energy: Ni(111) −1.22 eV; NiPt(111) −1.01 eV (Fig. 9 depicts 2H*, but the textual normalization is not fully specified, so this quantity is not scored in the public benchmark).
- Parallel HMF is more stable than tilted HMF on both surfaces.
- Parallel-to-tilted HMF barrier: Ni(111) 0.55 eV; NiPt(111) 0.34 eV.
- BHMF adsorption: NiPt/MFI −1.56 eV; NiPt@MFI −1.23 eV (not benchmarked because the supported structures are not reconstructible from disclosed inputs).

## 6. Limitations and interpretation boundaries

The model is an idealized periodic surface and cannot establish the full structure of experimental nanoparticles or zeolite-confined interfaces. The paper does not provide complete atomistic coordinates or all numerical settings. Adsorption and configurational energetics are electronic-energy model results, not finite-temperature free energies or catalytic rates. The association between lower HMF configurational barrier and selectivity is mechanistic support, not a standalone kinetic proof. Exact reproduction may be sensitive to lattice constant, magnetic initialization, dispersion implementation, adsorption-site coverage, and transition-path treatment.
