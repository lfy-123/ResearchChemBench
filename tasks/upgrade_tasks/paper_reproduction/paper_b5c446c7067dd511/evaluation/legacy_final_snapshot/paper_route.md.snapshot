# Private paper route

## 1. Scientific objective and author claim

The paper studies four donor–acceptor phenanthroimidazole emitters (Ph-mP, Na-mP, An-mP and Py-mP) and uses quantum-chemical excited-state calculations to support an HLCT/high-RISC interpretation. The authors claim that the molecules have mixed local-excitation and intramolecular-charge-transfer character and that triplet excitons can be harvested through higher triplet states rather than only the lowest-triplet-to-lowest-singlet channel.

## 2. System and model boundary

The systems are neutral, closed-shell organic molecules containing a 1-(p-tolyl)-1H-phenanthro[9,10-d]imidazole core, a para-phenylene bridge, and, respectively, phenyl, naphthalen-1-yl, anthracen-9-yl, or pyren-1-yl terminal groups. The authors' quantum calculations are gas-phase molecular calculations: ground-state geometry/HOMO/LUMO analysis, vertical singlet and triplet excitations, and NTO/IFCT analysis. Crystal packing, solvent response and measured photoluminescence are outside the electronic-structure calculation itself.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain ground-state structures and frontier orbitals | Four neutral molecular structures | Gaussian 09W DFT | B3LYP/6-31G(d,p), vacuum gas phase | Optimized ground-state geometries, HOMO/LUMO distributions | ev_doc_394c9393163d_000070_354c43ff43f0; ev_doc_394c9393163d_000307_94c6a66e427d |
| 2 | Compute vertical excited states | Optimized ground-state geometries | Gaussian 09W TD-DFT | TD-B3LYP/6-31G(d,p), vacuum gas phase; singlet and triplet states through at least T10/S10 | Vertical S1–S10 and T1–T10 energies | ev_doc_394c9393163d_000078_b007aab8ef13; ev_doc_586e5801e993_000019_e02e18f03cbc |
| 3 | Analyze excited-state character | Excited-state wavefunctions | Multiwfn, with VMD rendering | NTO and three-fragment IFCT analysis | Hole/electron distributions and CT/LE percentages | ev_doc_394c9393163d_000101_c690d6ee3cc7; ev_doc_394c9393163d_000108_ebb6f32d4c36 |
| 4 | Compare singlet/triplet gaps and interpret mechanism | State energies and character analysis | Author post-processing | ΔE(S1−T1), adjacent higher-triplet relationship, mixed CT/LE interpretation | Mechanistic support for HLCT/high-RISC | ev_doc_394c9393163d_000080_76472f8b1ebd; ev_doc_394c9393163d_000090_cb61d9ef1fa6 |

## 4. Validation and analysis protocol

The authors compare the computed state energies across all four compounds, inspect NTOs for simultaneous hole/electron overlap and separation, and partition each molecule into phenanthrimidazole, methylphenyl, and terminal aromatic fragments for IFCT. The gas-phase calculation is interpreted together with the experimental oxygen-quenching and temperature-dependence observations, but those experiments are not computational inputs. A defensible reproduction should verify optimization convergence, state calculation completion, state ordering, and that all reported CT/LE percentages are defined on the same fragments and state labels.

## 5. Private reference results

The SI Table S1 reports S1/T1 energies (eV): Ph-mP 3.518/2.635, Na-mP 3.463/2.572, An-mP 3.104/1.761, and Py-mP 3.146/2.041; it reports S2–S10/T2–T10 values for all four molecules. The main paper reports ΔE(S1−T1) values of 0.88, 0.89, 1.34 and 1.11 eV for Ph-mP, Na-mP, An-mP and Py-mP. SI Table S2 reports S1 CT/LE percentages of 59.10/40.90, 66.49/33.51, 37.73/62.27 and 54.23/45.77%, respectively. The paper discusses the adjacent higher triplet as HLCT-like and reports a notably large anthracene/bridge torsion.

## 6. Limitations and interpretation boundaries

The paper does not provide author input coordinates or machine-readable wavefunctions, and the reported values are method-dependent. Geometry/conformer choices, state character assignment, and numerical deviations must therefore be reported transparently. A successful computational match does not by itself prove the full photophysical mechanism; it tests the stated electronic-structure evidence within the gas-phase model boundary.
