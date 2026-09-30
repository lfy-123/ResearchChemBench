# Private paper route

## 1. Scientific objective and author claim

The paper uses first-principles energetics to explain thermally driven bulk-to-surface mass exchange in near-stoichiometric β-NiAl. Its central computational claim is that the formation energy of a Ni vacancy is lower than that of an Al vacancy, favoring Ni out-diffusion and contributing to Ni-rich γ′-Ni3Al surface precipitation (main article, DFT modeling and Fig. 6a).

## 2. System and model boundary

The bulk phase is ordered B2 β-NiAl, with Ni and Al on the two interpenetrating simple-cubic sublattices. The reported structural scale is approximately a=2.89 Å; the experimental single crystal is near stoichiometric (about 49% Ni and 51% Al). The vacancy calculations concern one neutral substitutional vacancy in a periodic bulk model, with elemental reservoirs used to define formation energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish bulk reference | Ordered β-NiAl structure | VASP periodic DFT | Relaxed/converged bulk model | pristine total energy | ev_doc_a7bb7508309d_000162_eb3f96b3d721; ev_doc_a7bb7508309d_000225_22cbb9e9c4f9 |
| 2 | Create Ni-defect state | Reference cell with one Ni removed | VASP periodic DFT | neutral vacancy, same bulk boundary | Ni-vacancy total energy | ev_doc_a7bb7508309d_000162_eb3f96b3d721 |
| 3 | Create Al-defect state | Reference cell with one Al removed | VASP periodic DFT | neutral vacancy, same bulk boundary | Al-vacancy total energy | ev_doc_a7bb7508309d_000162_eb3f96b3d721 |
| 4 | Compare defect energetics | Three total energies and elemental chemical potentials | Formation-energy analysis | consistent normalization and reservoir convention | Ni and Al vacancy formation energies | ev_doc_a7bb7508309d_000162_eb3f96b3d721; ev_doc_a7bb7508309d_000172_7ad23d1080d0 |
| 5 | Place result in mechanism | Vacancy energies plus surface calculations | VASP/NEB and interpretation | surface exchange and diffusion considered separately | rationale for preferential Ni surface accumulation | ev_doc_a7bb7508309d_000162_eb3f96b3d721; ev_doc_a7bb7508309d_000172_7ad23d1080d0 |

The methods identify VASP and PBE for the spectroscopy work and VASP/NEB for diffusion barriers, but do not disclose a complete vacancy-calculation input deck. The benchmark therefore treats the computational method as independently chosen by the Agent and scores the observable and defensible validation, not software identity.

## 4. Validation and analysis protocol

The paper compares the two vacancy formation energies and uses their ordering as a mechanistic premise. It also reports independent surface exchange and diffusion calculations, and experimental Ni enrichment, precipitate identification, and near-stoichiometric composition as corroborating context. Interpretation is limited to the stated bulk-defect energetics; vacancy energies alone do not prove the full kinetic pathway.

## 5. Private reference results

The published bulk vacancy formation energies are 0.98 eV for a Ni vacancy and 1.20 eV for an Al vacancy (Fig. 6a and accompanying DFT paragraph). Thus Ni vacancy formation is lower by 0.22 eV. The paper additionally reports a surface exchange barrier of 0.55 eV and net energy change of −0.31 eV, and diffusion barriers including 0.41/0.87 eV for the described <110> Ni processes and 2.13 eV for a <100> Ni process; these are contextual, not primary benchmark targets.

## 6. Limitations and interpretation boundaries

The article does not provide the full source-data archive or every vacancy-calculation convergence setting in the supplied evidence. Cell-size, k-point, pseudopotential, magnetic, chemical-potential, and relaxation choices can affect absolute values. A fair benchmark must require those choices to be disclosed and validated, while treating the published numbers as hidden references and avoiding claims that the vacancy ordering alone establishes all surface kinetics.
