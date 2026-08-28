# Private paper route

## 1. Scientific objective and author claim

The paper tests whether a CoO–NiO(1:3) heterostructure strengthens HMF adsorption relative to NiO and attributes the effect to interfacial electron redistribution. The reported DFT observables are adsorption energies and a Bader charge-transfer value.

## 2. System and model boundary

The authors use periodic NiO and CoO–NiO(1:3) slab models and neutral HMF. SI Tables S8–S11 give the cell parameters and fractional coordinates for the clean and adsorbed models. The DFT calculation is bounded to these named oxide systems and one HMF molecule.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize clean oxide models | NiO and CoO–NiO(1:3) cells | VASP periodic DFT | PBE/PAW, DFT+U, D3; 450 eV; 2×2×1; 1e-5 eV and 0.05 eV Å⁻¹ convergence | Clean surfaces | SI DFT section, ev_doc_b1b32ac616c8_000077_bce2eaeac7dd; Tables S8–S9 |
| 2 | Optimize HMF adsorption | Clean surfaces and HMF | VASP periodic DFT | Same stated settings; adsorbed models in Tables S10–S11 | HMF/surface structures | SI Tables S10–S11, ev_doc_b1b32ac616c8_000195_7f9cb8fd7166, ev_doc_b1b32ac616c8_000199_a469f0f4403d |
| 3 | Compute adsorption energies | Optimized complex, isolated HMF, clean substrate | Energy difference | E_ads = E*HMF − E_HMF − E_sub | Adsorption energies | SI Eq. 6 and Table S6, ev_doc_b1b32ac616c8_000174_490dd02f7d15 |
| 4 | Analyze interface charge | CoO–NiO charge density and Bader partition | Bader analysis | Domain charge comparison | Net CoO→NiO transfer | Main-paper Fig. 3 discussion, ev_doc_5c256f1dfb33_000095_8fd63d4dc750 |

## 4. Validation and analysis protocol

The authors compare the two adsorption energies and use differential charge density plus Bader analysis to interpret interfacial polarization. The paper reports stronger binding on CoO–NiO and electron transfer from CoO to NiO. The SI states the functional, PAW, DFT+U, cutoff, k points, D3 correction and convergence criteria; numerical U values are not supplied in the normalized evidence.

## 5. Private reference results

SI Table S6 reports E_ads = -0.85 eV for NiO and -1.01 eV for CoO–NiO. The main paper reports net transfer of 0.415 e− from CoO to NiO and identifies electron-rich Ni sites as adsorption/activation centers.

## 6. Limitations and interpretation boundaries

The source does not fully specify U/J values or a complete independent conformer/site search. The evaluator therefore scores object identity, validation, comparison and source-backed qualitative conclusions, while accepting a truthful bounded-failure report when computations cannot be completed.
