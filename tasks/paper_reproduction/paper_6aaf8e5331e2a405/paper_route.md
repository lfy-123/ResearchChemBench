# Private paper route

## 1. Scientific objective and author claim

The paper studies how substitutional transition-metal doping activates basal-plane sulfur sites of 2H-MoS2 for the four-electron oxygen reduction reaction (ORR). For the representative Ni-substituted system, the authors claim that structural/electronic rearrangement raises the active sulfur 3p-band center and gives a low ORR thermodynamic overpotential.

## 2. System and model boundary

The model is the exposed (001) basal plane of 2H-MoS2 represented by a 3x3 periodic slab with 15 Å vacuum normal to the sheet. One Mo lattice site is replaced by Ni. All atomic positions are relaxed; the reaction site is a surface sulfur adjacent to the substitution. ORR is treated as the associative four-electron sequence O2 + H+ + e− → OOH*, OOH* + H+ + e− → O* + H2O, O* + H+ + e− → OH*, and OH* + H+ + e− → H2O, using the CHE convention at U=0 V, pH=0, and 298.15 K.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build host slab and doped model | 2H-MoS2, (001), one Mo replaced by Ni | periodic DFT model construction | 3x3 supercell; 15 Å z vacuum | Ni@MoS2 slab | ev_doc_aaa2e4622c79_000049_0a70e8c6c0bd; ev_doc_aaa2e4622c79_000077_aa0d7c284d67; ev_doc_aaa2e4622c79_000078_35fa67f85668 |
| 2 | Optimize geometry | initial slab | spin-polarized VASP DFT | PBE/PAW, 450 eV, D3, 3x3x1 k mesh, forces <0.01 eV Å−1, electronic threshold 10−5 eV; all positions free | relaxed geometry and energy | ev_doc_aaa2e4622c79_000075_bb77e7f28501; ev_doc_aaa2e4622c79_000088_6b4c8573d108; ev_doc_aaa2e4622c79_000089_8e79143bfbe3; ev_doc_aaa2e4622c79_000092_aa7707457288; ev_doc_aaa2e4622c79_000093_799bb513f3bc; ev_doc_aaa2e4622c79_000095_cb693469e62d1 |
| 3 | Evaluate ORR thermodynamics | relaxed slab and OOH*, O*, OH* states | CHE free-energy analysis | U=0 V, pH=0, T=298.15 K; include reaction energy, ZPE and entropy terms | four ΔG values, PDS, η | ev_doc_aaa2e4622c79_000125_28591fb12d5e; ev_doc_aaa2e4622c79_000126_1e9d70a2ed85 |
| 4 | Analyze active-site descriptor | relaxed electronic structure | projected DOS/post-processing | dense 12x12x1 mesh; active sulfur 3p projection and first moment | εp | ev_doc_aaa2e4622c79_000091_0ffa4f1379b1; ev_doc_aaa2e4622c79_000438_6d5bcf5fe4a1 |

## 4. Validation and analysis protocol

The authors checked 3x3 versus 4x4 cells for representative dopants and found only minor η changes, selected the associative four-electron route when O* adsorption is thermodynamically suitable, compared adsorption sites, and used projected electronic structure to relate activity to the sulfur p-band center. They also discuss spin polarization, dispersion, and unconstrained relaxation as method requirements. These checks support a thermodynamic descriptor benchmark but do not establish a kinetic barrier or finite-temperature rate.

## 5. Private reference results

For Ni@MoS2 the reported representative values are η=0.53 V and εp=−1.24 eV. The paper's representative free-energy values at U=0 V are ΔG1=0.85 eV, ΔG2=2.58 eV, ΔG3=0.70 eV, and ΔG4=0.79 eV. The reported active-site interpretation is a surface sulfur site adjacent to Ni; the paper attributes the improvement in the d7–d9 class to Jahn–Teller-associated distortion and charge redistribution. These values and interpretation are private reference content.

## 6. Limitations and interpretation boundaries

The benchmark concerns thermodynamic CHE overpotential and a projected-band descriptor, not an experimentally measured rate, explicit-solvent free energy, or a transition-state barrier. Different legitimate pseudopotential, smearing, magnetic, adsorption-conformer, and post-processing choices can shift values; submissions must report those choices and uncertainty. The public structure is closed through the pinned Materials Project host record and deterministic slab/substitution instructions, while all scored reference values remain hidden.
