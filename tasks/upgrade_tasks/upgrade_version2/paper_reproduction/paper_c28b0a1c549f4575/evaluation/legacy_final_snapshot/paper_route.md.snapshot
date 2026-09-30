# Private paper route

## 1. Scientific objective and author claim

The paper uses molecular calculations to explain why the divalent DEDABCO cation can reorganize solvation in TEA-BF4/propylene carbonate (PC) electrolyte.  Its claim is that DED2+ has stronger PC binding than TEA+, allowing competitive sequestration of PC and thinning the TEA+ solvation shell (main paper, Fig. 2d and Section 2.2).

## 2. System and model boundary

The molecular systems are TEA+ (tetraethylammonium), DED2+ (the 1,4-diethyl-substituted DABCO dication called DEDABCO in the paper), BF4−, and propylene carbonate.  The DFT binding comparison concerns isolated ion–PC pairs.  The authors also discuss PC, BF4−–PC, TEA+–PC and DED2+–PC frontier orbitals, graphene adsorption, and condensed-electrolyte MD; those are interpretation/validation context rather than the primary binding-energy target.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize isolated ions and solvent and verify minima | TEA+, DED2+, BF4−, PC and pair structures | Gaussian 16, DFT B3LYP with D3BJ | def2-SVP; harmonic frequencies for all atoms | optimized structures and frequencies | ev_doc_66c8a05332da_000002_dff27fbd0a37 |
| 2 | Compute ion–solvent energies | optimized monomers and complexes | Gaussian 16 single points | B3LYP/6-311+G(2d,p) | electronic energies used for binding energies | ev_doc_66c8a05332da_000002_dff27fbd0a37 |
| 3 | Compare solvation binding | energies from Step 2 | ΔE_bind = E(pair) − E(ion) − E(PC) | sign convention interpreted as more negative = stronger binding | TEA+–PC, BF4−–PC and DED2+–PC comparison | ev_doc_1ba231dc5b49_000145_6075a0711e0f; ev_doc_1ba231dc5b49_000179_03dbcb08b4ca |
| 4 | Contextual electronic-structure analysis | optimized pair structures | B3LYP/6-311G** frontier orbitals | HOMO/LUMO of PC and ion–PC pairs | orbital-level interpretation | ev_doc_1ba231dc5b49_000189_012e0e76a101 |
| 5 | Contextual condensed-phase analysis | electrolyte boxes | GROMACS/Packmol, GAFF and RESP | NPT at 298.15 K and 1 bar; 30 ns equilibration plus 10 ns production; RDF/MSD | coordination and PC mobility trends | ev_doc_66c8a05332da_000002_dff27fbd0a37; ev_doc_1ba231dc5b49_000214_915c2bab7b9e |

## 4. Validation and analysis protocol

The paper identifies harmonic-frequency minima, compares the signed binding energies, and uses the DFT result together with NMR/Raman and MD observations.  The reported qualitative checks are stronger DED2+–PC binding, more cooperative PC interaction around DED2+, and a reduced/optimized TEA+ solvation shell at the 1+0.2 formulation.  The paper also reports graphene adsorption energies of −45.68, −24.83 and −10.69 kcal mol−1 for DED2+, TEA+ and PC, respectively, but these are not the primary pair-binding target.

## 5. Private reference results

The source gives a qualitative, not machine-readable, primary reference: DED2+–PC binds more strongly than TEA+–PC.  The main-paper Fig. 2d is a plotted binding-energy comparison without a recoverable numerical table in the supplied evidence.  Source-backed contextual values are graphene adsorption energies DED2+ −45.68, TEA+ −24.83 and PC −10.69 kcal mol−1 (ev_doc_1ba231dc5b49_000179_03dbcb08b4ca / surrounding Fig. 2f text), and the DED2+–PC RDF has a characteristic peak at 0.37 nm while TEA+–PC has a peak at 0.43 nm (ev_doc_1ba231dc5b49_000246_05784b3fcbbb).

## 6. Limitations and interpretation boundaries

No numerical Fig. 2d values or author Cartesian coordinates are available in the indexed paper/SI evidence.  Initial geometries and conformer choices are therefore not reproducible as an exact author trajectory; the benchmark evaluates independently generated structures and the source-supported ordering.  Binding energies are electronic pair energies, not free energies or bulk solvation free energies, and the qualitative ordering must not be interpreted as a complete desolvation proof by itself.
