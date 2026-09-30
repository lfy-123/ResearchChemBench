# Private paper route

## 1. Scientific objective and author claim

Establish the electronic ground state of nanographene complex 4, a formal Ni(IV) species, by comparing closed-shell singlet and triplet states. The authors claim a closed-shell singlet ground state and a substantially higher triplet state.

## 2. System and model boundary

Complex 4 is the octahedral Ni complex with two axial chloride ligands and an adj-CCNN dianionic nanographene-carbaporphyrin framework. The SI coordinate block supplies the optimized molecular geometry; charge is 0 and the compared spin multiplicities are 1 and 3.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize candidate electronic states | Coordinates of complex 4 and singlet/open-shell/triplet guesses | ORCA DFT | B3LYP and BP86; def2-TZVP on Ni, Cl1, Cl2, N1, N2, C1, C2; def2-SVP elsewhere | Optimized structures and energies | ev_doc_392321460733_000107_b8fd18ac154f; ev_doc_392321460733_000120_a9f513183948 |
| 2 | Check stationary points and structure agreement | Optimized structures | Vibrational analysis and comparison to crystallographic metrics | Positive frequencies; compare key Ni bonds | Minimum character and bond-length agreement | ev_doc_392321460733_000107_b8fd18ac154f |
| 3 | Compare spin states | Optimized singlet geometry and triplet calculation | ORCA DFT state calculation | BP86 protocol; multiplicities 1 and 3 | Singlet-triplet energy difference | ev_doc_392321460733_000107_b8fd18ac154f |

## 4. Validation and analysis protocol

The authors tested B3LYP and BP86 with closed-shell singlet, open-shell singlet, and triplet starting guesses. Open-shell singlet guesses converged to the closed-shell singlet solution. Optimized geometries were checked to have only positive frequencies, and calculated bond lengths were compared with crystallographic values. The reported spin-state conclusion was based on the triplet lying well above the closed-shell singlet.

## 5. Private reference results

The SI reports that the BP86 triplet lies 25.1 kcal/mol above the closed-shell singlet. The paper describes the triplet as more than 20 kcal/mol higher and concludes that complex 4 has a closed-shell singlet electronic structure.

## 6. Limitations and interpretation boundaries

The benchmark tests a finite electronic-structure comparison for the supplied molecular geometry. The gap is method-dependent and does not by itself establish all oxidation-state observables; the formal Ni(IV) assignment also relies on the ligand charge/coordination description and experimental characterization.
