# Private paper route

## 1. Scientific objective and author claim

The authors computationally test why direct photoexcitation of 3-(methylsulfonyl)-4-phenyl-1H-pyrrole-2,5-dione (1f) followed by reaction with ethynylbenzene (2a) favors the dehydro-Diels–Alder [4+2] channel over the competing [2+2] channel. They claim a triplet-manifold stepwise cycloaddition in which the [4+2]-forming open-shell-singlet transition state is lower than the [2+2]-forming alternative, placing chemoselectivity under kinetic control; the sulfonyl group also assists later aromatization.

## 2. System and model boundary

The modeled system is the neutral 1:1 combination of 1f and ethynylbenzene in acetonitrile. The mechanistic boundary begins with photoexcited triplet 1f and alkyne addition, includes the common triplet intermediate and competing open-shell-singlet ring-closing transition states, and ends with the [2+2] adduct or the [4+2] intermediate and its aromatization. The paper treats solvent with a continuum model and does not include explicit solvent, the lamp, or nonadiabatic dynamics in the reaction-path calculations.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish ground-state and photophysical reference | 1f | Gaussian 16; B3LYP/6-311+G(d,p), TD-DFT; Multiwfn; ORCA for SOC | SMD acetonitrile; S0 frequency minimum; low singlet/triplet states and SOC | Excitation spectrum, T1/S0 gap, ISC channels | SI §§9.2–9.3; ev_doc_2abfd66a6977_000895_4ee590a5a664 |
| 2 | Generate reaction-path guesses | 1f, ethynylbenzene, product connectivity | Potential-energy-surface scans | Product crystal structure used to guide scans | Initial TS guesses | SI §9.3.1; ev_doc_2abfd66a6977_000895_4ee590a5a664 |
| 3 | Locate common addition path | Triplet reactant complex | Gaussian 16, M06-2X/6-311+G(d,p) | SMD acetonitrile | TS1 and triplet IM1 | SI §§9.3.1–9.3.2; ev_doc_2abfd66a6977_000895_4ee590a5a664 |
| 4 | Locate competing closures | IM1 | Unrestricted/open-shell-singlet DFT in Gaussian 16 | M06-2X/6-311+G(d,p), SMD acetonitrile; guess=mix and stable=opt | OSS-TS2 ([4+2]) and OSS-TS2′ ([2+2]) | SI §9.3.1; ev_doc_2abfd66a6977_000895_4ee590a5a664 |
| 5 | Validate stationary points | All minima and transition states | Harmonic frequencies and IRC | Minima: no imaginary modes; TS: one reaction-coordinate imaginary mode and/or IRC connectivity; OSS wavefunction stability and suitable ⟨S²⟩ | Validated path network | SI §9.3.1; ev_doc_2abfd66a6977_000895_4ee590a5a664 |
| 6 | Compare free-energy barriers | Validated IM1 and closure TSs | M06-2X/6-311+G(d,p), Gaussian 16 | SMD acetonitrile; reported solution free energies | ΔΔG‡ and preferred channel | Main text Figure 5G; ev_doc_b41a30f85df5_000075_86cf70037817 |
| 7 | Analyze downstream aromatization | [4+2] intermediate IM2 | Same reaction-path level; interaction/orbital analysis | Hydrogen-bond-like O···H interaction; IRI/spin-density analysis | Aromatization barrier and qualitative sulfonyl role | Main text Figure 5G; SI §§9.3.3–9.3.4 |

## 4. Validation and analysis protocol

The authors optimized reactants/products and checked them as minima. Transition states were required to have one imaginary mode corresponding to the intended coordinate and/or an IRC connecting the designated endpoints. Open-shell-singlet closures were treated with spin-mixed guesses and stability optimization, and their open-shell character was checked using ⟨S²⟩. Selectivity was analyzed from free-energy barriers referenced to the common intermediate, supplemented by spin-density, frontier-orbital, and weak-interaction analyses.

## 5. Private reference results

The triplet excitation uphill is reported as 52.77 kcal/mol. Addition through TS1 has an approximate 6.63 kcal/mol barrier and forms triplet IM1. From IM1, the [4+2] open-shell-singlet transition state OSS-TS2 is 6.35 kcal/mol lower in free-energy barrier than [2+2] OSS-TS2′, predicting kinetic preference for [4+2]. The subsequent aromatization barrier is 18.24 kcal/mol. Experimentally, 1f gives 84% [4+2] product and 11% [2+2] product under the reported model conditions. These values are from ev_doc_b41a30f85df5_000075_86cf70037817 and the Figure 2 table.

## 6. Limitations and interpretation boundaries

The calculation supports relative kinetic accessibility within the investigated stepwise triplet/open-shell-singlet network; it does not establish excited-state population dynamics, absolute quantum yields, or exclude every possible photochemical route. Continuum solvation, harmonic thermochemistry, functional dependence, conformational coverage, and broken-symmetry treatment introduce uncertainty. The reported barrier difference should therefore be interpreted as mechanism-supporting evidence consistent with observed chemoselectivity, not as a direct quantitative prediction of product ratio.
