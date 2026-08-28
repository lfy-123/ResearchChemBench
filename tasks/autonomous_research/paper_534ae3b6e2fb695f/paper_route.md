# Private paper route

## 1. Scientific objective and author claim

The paper uses molecular electronic-structure calculations to rationalize why the aromatic diamines ODA, 6FODA and PFMB can undergo interfacial polycondensation with TMC, and claims the nucleophilicity order ODA > 6FODA > PFMB. The reported nucleophilicity indices are 4.26, 3.68 and 3.56 eV, respectively.

## 2. System and model boundary

The molecular systems are 4,4'-diaminodiphenyl ether (ODA), 4,4'-oxybis[3-(trifluoromethyl)aniline] (6FODA), 2,2'-bis(trifluoromethyl)benzidine (PFMB), and trimesoyl chloride (TMC). The monomer calculations are gas-phase, neutral, singlet calculations. The paper's mechanistic boundary is electronic reactivity of the diamine amine sites toward TMC; it is not a prediction of polymer performance by itself.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate and deduplicate monomer conformers | ODA, 6FODA, PFMB | xtb gfn2-xTB conformational search | 100 initial conformations per monomer; retain within 1 kcal mol−1 and geometrical deviation ≤1 Å as described | Representative conformers | ev_doc_1c73d8151157_000192_dd59907735bd |
| 2 | Optimize representative geometries | Representative diamine conformers | ORCA 5.0.4, B3LYP-D3BJ/def2-SVP | Gas phase; neutral singlets | Optimized structures | ev_doc_1c73d8151157_000192_dd59907735bd |
| 3 | Refine energies and analyze structure | Optimized structures | ORCA single point and Multiwfn | def2-TZVP; inter-ring dihedral C1–C2–X–C3 | Refined energies and dihedral angles | ev_doc_1c73d8151157_000192_dd59907735bd |
| 4 | Evaluate reactivity descriptors | Optimized diamines and amine sites | DFT descriptor analysis | ESP, ALIE, Fukui function, LEAE, HOMO/LUMO and nucleophilicity index | Descriptor maps and values | ev_doc_1c73d8151157_000201_84be483c9063; ev_doc_1ec204d1c673_000043_baebf4f34a87 |
| 5 | Interpret relative reactivity toward TMC | Descriptor results | Multidescriptor interpretation | ALIE and nucleophilicity index primary; ESP complementary | ODA > 6FODA > PFMB | ev_doc_1c73d8151157_000201_84be483c9063; ev_doc_1ec204d1c673_000043_baebf4f34a87 |

## 4. Validation and analysis protocol

The authors re-optimized 6FODA to remove slight terminal-site asymmetry, then used multiple descriptors to corroborate the reactivity order. The optimized inter-benzene dihedrals reported for ODA, 6FODA and PFMB are 75.2°, 81.6° and 77.1°. Descriptor calculations are interpreted as intrinsic gas-phase monomer properties and are not treated as direct kinetic constants. The paper also reports a separate polymer-fragment torsion workflow, but its exact fragment coordinates and numerical barriers are not supplied and are outside this benchmark.

## 5. Private reference results

Reported nucleophilicity indices: ODA 4.26 eV, 6FODA 3.68 eV, PFMB 3.56 eV. Reported ordering: ODA > 6FODA > PFMB. Reported optimized inter-benzene dihedrals: ODA 75.2°, 6FODA 81.6°, PFMB 77.1°. The paper states that all three diamines have sufficient reactivity for polycondensation with TMC.

## 6. Limitations and interpretation boundaries

The descriptor values depend on conformer selection, electronic-structure settings and the definition of the descriptor. They support a comparative hypothesis, not an experimental rate constant. The source contains a reviewer-identified ESP/ALIE discrepancy in an earlier analysis and a revised multidescriptor interpretation; the benchmark scores the revised reported claim and requires agents to disclose their computational choices and uncertainty.
