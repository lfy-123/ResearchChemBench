# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical structures and charge/electrostatic analysis to explain how the phosphonium-containing zwitterion formed from tris(diethylamino)phosphine and phthalic anhydride interacts with propylene oxide and an alkoxide chain end. The author claim is that the onium site activates the epoxide and stabilizes the growing chain end through complementary noncovalent contacts, supporting the high-activity CO2/PO copolymerization mechanism.

## 2. System and model boundary

The computed species are neutral singlet `(Et2N)3P`, its propylene-oxide adduct `(Et2N)3P-PO`, and its phthalic-anhydride zwitterion `(Et2N)3P-PA`. The SI supplies Cartesian tables, but the PA S39-S40 table omits C6H4 relative to Figure 6a. The public task supplies the full source-defined graph and explicitly labels the generated missing-fragment coordinates; they are not attributed to the author. The analysis concerns isolated ground-state molecules, not the full polymerization environment, solvent, or explicit triethylborane.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize all three ground-state structures | SI Cartesian coordinates | Gaussian 16 DFT | B3LYP/6-31G(d), D3(BJ) | optimized geometries | ev_doc_8a1aa1009e1c_000089_0d189ebf08e1; ev_doc_8a1aa1009e1c_000091_46143619f057 |
| 2 | Verify stationary points and generate wavefunctions | optimized geometries | Gaussian 16 frequency calculation | same model chemistry | harmonic frequencies and wavefunction files | ev_doc_8a1aa1009e1c_000091_46143619f057 |
| 3 | Analyze electrostatics and atomic charges | frequency wavefunctions | Multiwfn | ADCH population analysis; MEP mapping | ADCH charges and MEP maps | ev_doc_8a1aa1009e1c_000091_46143619f057 |
| 4 | Compare mechanistically relevant contacts and charge redistribution | optimized structures and ADCH charges | geometric measurement and tabulation | O···P, O···αH, O···βH; P/αH/βH charge comparisons | interaction distances, charge differences, mechanistic interpretation | ev_doc_1e6fd476cea2_000575_f419bbd900ed; ev_doc_1e6fd476cea2_000586_09162b3b4845; ev_doc_1e6fd476cea2_000593_e48b8864ac77; ev_doc_1e6fd476cea2_000595_f3f1c106ba01; ev_doc_1e6fd476cea2_000604_fcd38ffd08b9 |

## 4. Validation and analysis protocol

Each optimized structure is checked as a true minimum by the absence of imaginary harmonic frequencies. Atom identities are retained from the supplied coordinate order. For `(Et2N)3P-PO`, the epoxide oxygen contacts P and nearby α/β hydrogens; for `(Et2N)3P-PA`, the carboxylate oxygen contacts α/β hydrogens and more weakly P. Distances are measured directly from the optimized Cartesian coordinates. ADCH values are extracted for P and the relevant α/β hydrogens, and MEP maps are inspected for the cationic/electrophilic and carboxylate/nucleophilic regions.

## 5. Private reference results

The paper reports for `(Et2N)3P-PO`: O···P = 1.828 Å, O···αH = 2.124 Å, O···βH = 2.437 Å. For `(Et2N)3P-PA`: O···αH = 2.312 Å, O···βH = 2.363 Å, O···P = 2.651 Å. Figure 6b-d gives absolute P charges -0.018, +0.447 and +0.455 e for free/PO/PA. The +0.074 e label belongs to free-base alpha-H, not P or a P-charge difference; the paper also reports αH and βH charge values for all three species and describes increased electron density around the PA phosphonium region in the MEP. These values are hidden evaluator references.

## 6. Limitations and interpretation boundaries

The calculations are isolated-molecule ground-state DFT models and do not establish a full catalytic free-energy profile, solvent effects, dynamic populations, or the complete role of Et3B. Contact distances and ADCH/MEP patterns support the proposed interaction picture but are not, alone, a quantitative causal proof of polymerization rate or selectivity.

## Source-binding clarification (2026-09-15)

Figure 6 contacts are defined on N-ethyl CH2/CH3 H sites (P–N–C), despite the generic alpha/beta wording in the main-text paragraph. PO indices: O49/P46/H5(CH2)/H45(CH3). PA indices: carboxylate O49/P46/H27(CH2)/H29(CH3). Source Figure 6 uses a signed ESP color bar (-0.05 red to +0.05 blue au); its wording about increased electron density in a blue region must not be substituted for a charge-density measurement. Verify signed ESP and state this wording limitation. No new scientific goal is added or removed.
