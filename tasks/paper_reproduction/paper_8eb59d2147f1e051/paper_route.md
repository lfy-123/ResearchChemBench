# Private paper route

## 1. Scientific objective and author claim

The authors use spin-polarized DFT to explain why Ni-containing Fe2NiSe4 is a more effective Li–S sulfur host than Fe3Se4. Their computational claim is that Ni doping strengthens Li polysulfide interaction and lowers the kinetic barrier for Li2S decomposition, thereby supporting faster sulfur conversion and better rate performance.

## 2. System and model boundary

The calculated systems are Fe3Se4 and monoclinic Fe2NiSe4 slab models, with Li2Sx (x = 8, 6, 4, 2, 1) adsorbates. Binding energy is defined as E_sub + E_Li2Sx − E_Li2Sx@sub. The SI describes periodic slabs with at least 15 Å vacuum and treats the Li2S decomposition barrier with CI-NEB between specified initial and final positions.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Prepare the two host surfaces | Fe3Se4 and Fe2NiSe4 crystal structures | Spin-polarized PAW DFT in VASP | RPBE; 450 eV plane-wave cutoff; 3×3×1 Monkhorst–Pack mesh; ≥15 Å slab vacuum; D3 dispersion; energy convergence 10^-5 eV; force threshold 0.02 eV Å^-1 | Optimized slabs | ev_doc_0480dffe8eba_000043_8189b95929bc; ev_doc_0480dffe8eba_000046_d472efb6e4de; ev_doc_0480dffe8eba_000049_696040a7261b; ev_doc_0480dffe8eba_000012_af69288e83d3 |
| 2 | Compare electronic structure and adsorption | Optimized slabs plus Li2S/Li2S6 configurations | Same DFT model; DOS and charge-density-difference analysis | Same periodic settings | DOS, d-band-center comparison, charge redistribution, LiPS binding energies | ev_doc_84a44e8bb792_000336_307027bc59ea; ev_doc_84a44e8bb792_000338_a934603fea49 |
| 3 | Follow sulfur reduction thermodynamics | Adsorbed LiPS intermediates | DFT reaction-energy/Gibbs analysis | ΔG = ΔE + ΔZPE − TΔS; SI sets ΔS to zero at low temperature | S8-to-Li2S energy profile and rate-limiting step | ev_doc_0480dffe8eba_000049_696040a7261b; ev_doc_0480dffe8eba_000051_c85bf75a536d |
| 4 | Quantify Li2S decomposition kinetics | Initial and final Li2S surface states | CI-NEB in VASP | Minimum-energy path between supplied endpoint geometries | Decomposition barriers on both hosts | ev_doc_84a44e8bb792_000028_adafe257ce00 |

## 4. Validation and analysis protocol

The authors compare the two hosts using the same definitions and periodic settings, inspect metallic electronic structure and charge redistribution, compare LiPS binding, identify the rate-limiting *Li2S2 → *Li2S transformation, and compare Li2S decomposition barriers. The paper reports barriers of 2.33 eV for Fe3Se4 and 1.86 eV for Fe2NiSe4; it states that Fe2NiSe4 binds LiPSs more strongly. These computational observations are interpreted alongside experimental rate capability and cycling data, not as a standalone proof of every macroscopic mechanism.

## 5. Private reference results

The reported Li2S decomposition barriers are 2.33 eV (Fe3Se4) and 1.86 eV (Fe2NiSe4). The *Li2S2 → *Li2S step is identified as rate-limiting. The paper states that Fe2NiSe4 has stronger LiPS binding than Fe3Se4 and attributes this to Ni-modified electronic structure and Fe/Se/Ni sites.

## 6. Limitations and interpretation boundaries

The source does not expose a complete machine-readable slab termination, thickness, adsorption geometry, or NEB endpoint coordinates. An independent reproduction must therefore report its chosen surface and endpoint construction and test their stability/coverage. Agreement is meaningful as a trend and model-dependent barrier comparison; it is not a claim that one unconverged surface geometry uniquely represents the porous rGO composite.
