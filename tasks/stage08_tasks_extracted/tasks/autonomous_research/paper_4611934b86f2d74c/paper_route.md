# Private paper route

## 1. Scientific objective and author claim

The authors computationally test whether photoexcitation of potassium CO2 carbamate 2 can reach a triplet surface and cleave its C–N bond to form persistent radical 4 and potassium CO2 radical anion. They claim the photolysis route is kinetically feasible and supports hydrocarboxylation.

## 2. System and model boundary

The modeled system is potassium benzophenothiazine-CO2 carbamate 2 and its S0, S1, and T1 surfaces, with separated 4(S0) and CO2•−K+ products. Energies are solvent-corrected Gibbs free energies at 298 K, relative to 2A(S0), with DMF represented by SMD.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Explore ground-state carbamate conformers and stationary points | BPTZ anion, CO2, carbamate conformers | Gaussian 16 | ωB97X-D/6-31+G optimization/frequencies; 298 K | S0 minima and TSs | ev_doc_042e2795b9be_001353_3659e8f0baad; ev_doc_042e2795b9be_001358_4ed0b63f08f6 |
| 2 | Relax the lowest singlet excited state | selected S0 carbamate | Gaussian 16 TD-DFT | TD-DFT ωB97X-D/6-31+G | S1 minimum | ev_doc_042e2795b9be_001356_b219d48f8ad2 |
| 3 | Locate S1/T1 crossing | S1/T1 surfaces | KST48 with Gaussian 16 | ωB97X-D/6-31G, mode=stable, SMD(DMF) | MECP | ev_doc_042e2795b9be_001364_edeeb575eacf |
| 4 | Follow triplet cleavage | MECP and T1 carbamate | Gaussian 16 | T1 optimization, frequencies, IRC for TSs; SMD(DMF) single points | cleavage paths and products | ev_doc_12f73a4b6d67_000339_4ef6915955c7; ev_doc_12f73a4b6d67_000345_ec59436ff5bd |
| 5 | Assemble solvent Gibbs profile | all stationary points and fragments | Gaussian 16 energies plus thermal corrections | ΔGsol relative to 2A(S0) | barriers and reaction free energy | ev_doc_12f73a4b6d67_000346_2202cfb99926; ev_doc_12f73a4b6d67_000350_9b645947205a |

## 4. Validation and analysis protocol

Frequencies were used to distinguish minima from transition states and obtain zero-point/thermal corrections. Each transition state was checked by IRC for connection to the intended endpoints. Solvent-corrected single points refined the gas-phase optimized structures. The final profile was interpreted together with experimental evidence for carbamate photolysis and CO2•− formation.

## 5. Private reference results

The paper reports an S1/T1 MECP 9.8 kcal mol−1 above the S1 minimum. The two triplet C–N cleavage barriers are 2.9 and 1.2 kcal mol−1, and the overall reaction free energy is −37.0 kcal mol−1 (all ΔGsol, relative to 2A(S0)).

## 6. Limitations and interpretation boundaries

These are single-level DFT results with implicit DMF and finite conformer sampling; they establish a computationally feasible route, not a complete photochemical dynamics simulation or proof that no competing pathway exists.
