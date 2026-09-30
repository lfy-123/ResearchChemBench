# Private paper route

## 1. Scientific objective and author claim

The paper tests whether a TsCl···THF collision complex can account for the visible-light absorption that enables sulfonyl-radical formation in hydrosulfonylation. The authors claim that the representative complex has a solvent-to-substrate charge-transfer excitation associated with the S–Cl σ* orbital.

## 2. System and model boundary

The modeled system is a neutral singlet 1:1 complex of p-toluenesulfonyl chloride (TsCl) and tetrahydrofuran (THF), in the gas-phase electronic-structure model used for the calculations. The scored observables are vertical excitation wavelength, oscillator strength, and CT assignment; the paper also reports excited-state charge transfer and dipole changes.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Explore complex conformations | TsCl and THF 1:1 structures | B3LYP/6-31G* geometry optimization | Eleven initial conformations; optimized minima | Conformer energies and geometries; Con.1 selected as representative based on arrangement | ev_doc_4e156232f1e0_000025_3696ad59777e; ev_doc_4e156232f1e0_000026_adfa2b24c2d9; ev_doc_4e156232f1e0_000027_cabb00586dd1 |
| 2 | Refine electronic structure | Selected Con.1 geometry | CASSCF geometry refinement in Gaussian 09 | 17-root state-averaged RASSCF; active space 14 electrons/10 orbitals including TsCl/THF lone pairs, π/π*, σ/σ* | Refined geometry and multiconfigurational wavefunction | ev_doc_4e156232f1e0_000087_a1fee0309d29; ev_doc_4e156232f1e0_000096_cda9a218d3d9; ev_doc_4e156232f1e0_000098_12ab3ff5c216 |
| 3 | Compute vertical spectrum | Refined selected-complex wavefunction | CASPT2 single points in Molcas | Standard zeroth-order Hamiltonian; same 14e,10o active space | Excitation energies, oscillator strengths, orbital character | ev_doc_4e156232f1e0_000089_3ecbd52328f5; ev_doc_4e156232f1e0_000098_12ab3ff5c216 |
| 4 | Analyze CT mechanism | Ground and excited-state populations | Mulliken population analysis | Q1/Q2 partition shown in SI | Charge transfer and dipole interpretation | ev_doc_4e156232f1e0_000019_937cad5c0ed1; ev_doc_cf72fd648c7d_000032_4834067fda6c |

## 4. Validation and analysis protocol

The authors compare the calculated absorption with the experimentally observed broad 365–400 nm band for TsCl in THF. They identify the transition by orbital character and population redistribution, and interpret increased excited-state polarity and S–Cl σ* occupation as consistent with charge-transfer-assisted cleavage.

## 5. Private reference results

For the selected Con.1 calculation, the paper reports an absorption character at 380 nm with oscillator strength 0.07. The assigned transition is SCT(1nσ*), with ΔQ = 0.82 e and dipole moments changing from 5.4 D (S0) to 15.8 D (excited state). These values are evaluator-only references.

## 6. Limitations and interpretation boundaries

The result is a vertical, gas-phase multireference calculation on one representative optimized arrangement, not a solvated spectrum or a complete photochemical dynamics simulation. Conformer near-degeneracy and method/active-space sensitivity limit claims about population or kinetic uniqueness. Agreement with the measured band supports consistency with the proposed CT mechanism but does not by itself prove the full reaction mechanism.
