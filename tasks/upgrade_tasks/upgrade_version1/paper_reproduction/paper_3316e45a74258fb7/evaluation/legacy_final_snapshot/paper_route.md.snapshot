# Private paper route

## 1. Scientific objective and author claim

The authors use quantum-chemical calculations to relate the electronic structure of the red TADF emitter TD-2T to its photophysical behavior. Their claim is that donor–acceptor orbital separation and the resulting small singlet–triplet gap support reverse intersystem crossing (RISC) and TADF.

## 2. System and model boundary

TD-2T is the neutral, closed-shell molecule 4,4',4''-(dibenzo[f,h]pyrazino[2,3-b]quinoxaline-3,6,11-triyl)tris(N,N-diphenylaniline), with a DCTP fused-ring acceptor and three triphenylamine donors (main paper Fig. 1 and SI synthesis). The calculations concern the isolated molecule and its low-lying S0, S1 and T1 electronic states.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain the ground-state structure | TD-2T molecular structure | DFT, Gaussian 09 | B3LYP/6-31G(d,p); neutral singlet; full S0 optimization | optimized S0 geometry | ev_doc_6975943bb119_000068_5b32f2868dd3 |
| 2 | Obtain low-lying excited states | optimized S0 geometry | TD-DFT, Gaussian 09 | same B3LYP/6-31G(d,p) level; S1 and T1 | S1/T1 energies and oscillator strength | ev_doc_6975943bb119_000068_5b32f2868dd3, ev_doc_6975943bb119_000076_e603cd6c1353 |
| 3 | Interpret the electronic structure | excited-state output | Multiwfn 3.8 | NTO analysis | hole/electron distributions and CT/HLCT interpretation | ev_doc_6975943bb119_000082_3d4fae2d7f3f |

## 4. Validation and analysis protocol

The authors compare the calculated S1/T1 separation with the reported TD-2T singlet–triplet gap and use orbital/NTO separation, donor–acceptor dihedral geometry and oscillator strength to interpret TADF. The main text explicitly reports a calculated TD-2T ΔE_ST of 0.34 eV (ev_doc_6975943bb119_000107_7247d55a5967). The paper reports that donor–acceptor separation gives CT character and that the TD-2T T1 state has HLCT-like partial overlap (ev_doc_6975943bb119_000082_3d4fae2d7f3f, ev_doc_6975943bb119_000113_c4e14f4f0073).

## 5. Private reference results

The source-backed computational reference is ΔE_ST(TD-2T) = 0.34 eV (ev_doc_6975943bb119_000107_7247d55a5967). The source also supports the qualitative conclusion that TD-2T has separated donor/core orbitals, CT-like S1 character and HLCT-like T1 character. The SI identifies Table S1 as the simulation-data table but the normalized supplied SI does not expose its cell values; no unsupported table value is promoted here.

## 6. Limitations and interpretation boundaries

The paper does not provide machine-readable coordinates, and the normalized SI does not expose all Table S1 numerical cells. Geometry, conformer choice and method dependence therefore limit exact reproduction. ΔE_ST is an electronic-structure diagnostic, not by itself a measurement of a device RISC rate or OLED efficiency. The reported value should be interpreted within the isolated-molecule computational model.
