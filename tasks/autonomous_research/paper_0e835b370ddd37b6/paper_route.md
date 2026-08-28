# Private paper route

## 1. Scientific objective and author claim

The paper computationally tests whether six-membered cyclic (alkyl)(amino)silylene 1 activates H2 more readily than the experimentally known NacNacSi analogue V′. The authors claim lower H–H activation barriers and exergonic products for the designed CAASis.

## 2. System and model boundary

Neutral singlet silylenes 1 and V′ plus neutral H2; molecular structures are treated with benzene continuum solvent and thermal free energies at 298 K and 1 atm.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize reactants | 1, V′, H2 | Gaussian 09 DFT | PBE0-D3BJ/Def2-TZVP, SMD benzene, no symmetry constraints | stationary-point geometries | ev_doc_471aa5635a97_000080_efbca894c4b1; ev_doc_0505660cda6b_000271_82b939af9c6d |
| 2 | Characterize minima | optimized reactants | Gaussian 09 frequency | same model | no imaginary frequencies, thermochemistry | ev_doc_471aa5635a97_000080_efbca894c4b1 |
| 3 | Locate H2-activation TSs | each silylene + H2 | Gaussian 09 TS search | same model | 1_TSH-H and V′_TSH-H | ev_doc_0505660cda6b_000004_e27d0fb6c41c; ev_doc_0505660cda6b_000076_4b069bc96ba0 |
| 4 | Validate TSs | TS geometries | frequency/IRC characterization | same model | exactly one imaginary mode and connected endpoints | ev_doc_471aa5635a97_000080_efbca894c4b1 |
| 5 | Compare energetics | validated stationary points | thermochemical free-energy analysis | 298 K, 1 atm | ΔG°‡(H–H) and reaction ΔG° | ev_doc_471aa5635a97_000082_e93620212ebd; ev_doc_471aa5635a97_000173_f6c5ba5bd173 |

## 4. Validation and analysis protocol

Reactant geometries are minima; each H2 transition structure has one imaginary frequency associated with H–H cleavage and connects reactant and H–H splitting product. Barriers are measured from the corresponding separated singlet reactant plus H2 reference. Compare the two catalyst systems and interpret only within the stated model.

## 5. Private reference results

Table 2 reports ΔG°‡(H–H) = 32.9 kcal mol−1 for 1 and 47.4 kcal mol−1 for V′; corresponding total reaction free energies are −29.4 and −21.3 kcal mol−1. The paper concludes that 1–6 have lower barriers than V′/VIII′ and that this supports metal-free H2 activation.

## 6. Limitations and interpretation boundaries

These are model-chemistry predictions, not kinetic measurements. Transition-state searches can miss alternative conformers; comparison is meaningful only for consistently defined singlet reactants, H2, solvent, temperature and pressure.
