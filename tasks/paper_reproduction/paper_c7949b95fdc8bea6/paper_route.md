# Private paper route

## 1. Scientific objective and author claim

The paper asks whether an excess electron, used as a minimal model of n-type/Sb-doped silicon, changes Li diffusion in crystalline silicon. The authors claim that an electron-trapping state develops near the bulk Li migration transition state and lowers the migration barrier.

## 2. System and model boundary

The bulk model is periodic crystalline diamond Si with Li initially at a tetrahedral interstitial site and migrating to an adjacent tetrahedral site. The authors also considered clean (100)/(110) slabs and amorphous–crystalline interfaces, but those are outside this task. Neutral, one-electron-added, and one-electron-removed periodic charge states are distinct calculations; the scored state is the one-electron-added bulk cell.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish bulk c-Si diffusion model | Conventional Si8 cell; Li at adjacent empty Td interstitials | VASP, PBE/PAW | 480 eV cutoff; odd-electron N_up-N_down=1; use the disclosed MP 12x12x12 Si8 lattice optimization, then 2x2x2 expansion to Si64 as required by main p.3. The Si64 diffusion k mesh is not explicitly disclosed and needs a recorded convergence test; SI's Si216/MP 2x2x2 applies to absorption energy, not diffusion. | Relaxed Li@Si64 endpoints | ev_doc_42d5442bda71_000067_2fc7fd89c941; SI S1-S2 distinguish the lattice/absorption calculation from main p.3 diffusion |
| 2 | Locate Li migration path | Relaxed Td endpoint and adjacent Td endpoint, linearly interpolated images | NEB in VASP | Nimage=7; residual forces <0.3 eV/A; HSE screening parameter 0.2 and sampled k points in Fock operator | Energy profile and barrier for neutral/charged states | ev_doc_42d5442bda71_000067_2fc7fd89c941, ev_doc_474f0d99b606_000009_4f212f15751e, ev_doc_474f0d99b606_000011_7651d6b86012, ev_doc_474f0d99b606_000012_b9ef799a6038 |
| 3 | Test excess-electron effect | Same bulk path with NELECT increased by one | HSE single-point/NEB comparison | Electronic convergence ΔE <3×10^-8 eV; spin up/down difference one for odd electron count only; even-electron treatment explicitly recorded | Charged-state barrier and comparison to neutral HSE | ev_doc_42d5442bda71_000104_a1ac4b4885f2, ev_doc_42d5442bda71_000105_0d3e43774792, ev_doc_42d5442bda71_000108_dfcafb1d8e03 |
| 4 | Interpret electronic mechanism | Charge density/wavefunction near barrier | HSE electronic-structure analysis | Compare state localization and energy relative to CBM | Electron-trapping interpretation | ev_doc_42d5442bda71_000012_1799fb255a6d, ev_doc_42d5442bda71_000108_dfcafb1d8e03 |

## 4. Validation and analysis protocol

The authors checked the neutral bulk barrier against prior values and compared PBE and HSE. They inspected the HSE band gap and the wavefunction at the hexagonal-center barrier configuration; the excess-electron state was reported below the CBM and localized around Li at the barrier. The paper cautions that clean-surface barriers are idealized and should not be directly mapped to electrolyte experiments.

## 5. Private reference results

Table 1 reports bulk Li migration barriers of 0.57 eV (PBE), 0.50 eV (HSE), and 0.41 eV (HSE + one excess electron); the one-electron-removed value is 0.64 eV. The HSE c-Si gap is 1.27 eV. At the bulk barrier, the excess-electron trapping state is 0.28 eV below the CBM. These values are evaluator-only.

## 6. Limitations and interpretation boundaries

The model is a dilute, idealized bulk interstitial calculation and does not include explicit Sb, electrolyte solvation, surfaces, SEI, finite temperature, or a full dopant concentration. Barrier agreement is method- and cell-dependent; a submitted alternative method must report convergence and sensitivity rather than being treated as an exact reproduction of VASP.
