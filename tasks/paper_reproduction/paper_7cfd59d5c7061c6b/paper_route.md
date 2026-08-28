# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to test N-demethylation of N,N-dimethylaniline (DMA) by the side-on Fe(III)-peroxo 12-TMC complex (complex 1). The authors compare direct H-atom abstraction by the peroxo complex with a route initiated by homolytic O–O cleavage to an Fe(IV)(oxo)(oxyl) species, followed by HAT. Their claim is that O–O cleavage is the kinetically relevant first event and that the subsequent HAT is accessible.

## 2. System and model boundary

The modeled reactant is the sextet, cationic [Fe(III)(O2)(12-TMC)]+ complex with one DMA molecule, using the SI TPSSH/Def2-SVP coordinate block labeled 61RC. Energies are electronic relative energies in a TFE continuum model; the paper also reports higher-basis single-point refinement and dispersion contributions. The paper discusses two pathways and several n-TMC ring sizes, but the central detailed comparison is complex 1 with DMA.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish the relevant spin state and optimize structures | Fe(III)-peroxo n-TMC models and DMA complex | Gaussian 16 DFT | uB3LYP, TPSSH and M06L; Def2-SVP; CPCM(TFE); sextet selected as lowest state | Optimized reactant/intermediate/TS structures | ev_doc_e55105431bad_000617_fc7222aad49a, ev_doc_e55105431bad_000756_f375fe8d5483 |
| 2 | Test direct HAT | 1RC + DMA | TPSSH PES/TS search | Def2-SVP geometry and frequency calculations | Direct-HAT TS/intermediate | ev_doc_e55105431bad_000617_fc7222aad49a, ev_doc_61c34947163c_000079_755fe6cd81d5 |
| 3 | Test O–O cleavage then HAT | 1RC + DMA | TPSSH TS searches and IRC | Def2-SVP; sextet; CPCM(TFE) | 1TS1b, 1IM1b, 1TS2b, 1IM2b/1IM3b | ev_doc_e55105431bad_000629_50b16d8b4c43, ev_doc_e55105431bad_000639_35c0f2e66a1c |
| 4 | Refine relative energies | optimized structures | TPSSH single points | Def2-TZVPP; CPCM(TFE); D3-BJ contribution | electronic relative energies/barriers | ev_doc_e55105431bad_000756_f375fe8d5483, ev_doc_61c34947163c_000288_9585fe786909 |
| 5 | Validate stationary points and interpret mechanism | candidate TSs and intermediates | frequency and IRC calculations; spin-density analysis | one imaginary mode for TSs; endpoint connectivity | validated pathway and barrier comparison | ev_doc_e55105431bad_000617_fc7222aad49a, ev_doc_61c34947163c_000288_9585fe786909 |

## 4. Validation and analysis protocol

The authors determine spin-state ordering, optimize structures, locate transition states, verify TS frequencies, and use IRC calculations to establish connectivity. They compare direct HAT against the O–O-cleavage-first pathway using electronic energies at TPSSH/Def2-TZVPP//Def2-SVP with CPCM(TFE) and D3-BJ. The SI reports Mulliken spin densities and full coordinate sets for the structures.

## 5. Private reference results

For complex 1 with DMA, the O–O cleavage transition state 1TS1b is reported at 13.1 kcal mol−1 relative to 1RC, and the subsequent HAT transition state 1TS2b at 9.2 kcal mol−1 relative to 1RC. The paper describes the O–O-cleavage-first pathway as favored over direct HAT; the SI TPSSH table gives direct-HAT 61TS1a at 27.64 kcal mol−1 and the O–O-cleavage-first electronic barriers as 13.09 and 9.18 kcal mol−1.

## 6. Limitations and interpretation boundaries

The model is a finite molecular cluster with continuum solvent and electronic, rather than Gibbs, energies emphasized by the authors. Transition-metal DFT and conformational selection introduce method sensitivity; the authors note that flexible TMC ligands can produce structural isomers. A reproduced barrier is evidence within this model and protocol, not a general experimental rate prediction.
