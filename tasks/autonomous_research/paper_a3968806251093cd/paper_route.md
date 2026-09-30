# Private paper route

## 1. Scientific objective and author claim

The paper studies 4-(((5-(p-chlorophenoxy)-3-methyl-1-phenyl-1H-pyrazol-4-yl)methylene)amino)-5-methyl-4H-1,2,4-triazole-3-thione (7a). Its computational claim is that gas-phase DFT reproduces the SCXRD geometry and that CAM-B3LYP gives the closer geometrical and vibrational agreement.

## 2. System and model boundary

The isolated neutral thione tautomer, formula C20H17ClN6OS, is treated as a singlet molecule. Experimental comparison is to the molecular geometry reported by SCXRD; crystal packing is not optimized in the DFT calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize isolated molecular geometry and calculate frequencies | compound 7a structure | Gaussian 09 / GaussView 6.0.16 | B3LYP/6-311+G(d,p), gas phase | optimized coordinates, vibrational frequencies, electronic properties | ev_doc_6fa279192fe2_000064_6865e8763f76; ev_doc_6fa279192fe2_000065_c2f990fc8770 |
| 2 | Independent optimization and property calculation | same 7a structure | Gaussian 09 / GaussView 6.0.16 | CAM-B3LYP/6-311+G(d,p), gas phase | optimized coordinates, vibrational frequencies, electronic properties | ev_doc_6fa279192fe2_000064_6865e8763f76; ev_doc_6fa279192fe2_000065_c2f990fc8770 |
| 3 | Compare geometry with crystallography | optimized structures and SCXRD geometry | PLATON-derived geometric parameters and tabulation | bond lengths, inter-bond angles, torsions | Tables S1-S3 comparison | ev_doc_6fa279192fe2_000153_20c82d2580d2; ev_doc_2d756ad0ed72_000066_d7f5216731d0; ev_doc_2d756ad0ed72_000072_8698fc6e9da7; ev_doc_2d756ad0ed72_000076_096ec81ee6fc |

## 4. Validation and analysis protocol

The authors correlate calculated bond lengths, bond angles, torsion angles and FT-IR frequencies with experiment. The structural conclusion is based on the three geometry tables; the paper reports that CAM-B3LYP is more accurate for geometrical parameters and vibrational analysis. The molecule is described as non-planar, with tautomerism and hydrogen-bonding contacts discussed from SCXRD, Hirshfeld, RDG and IRI analyses.

## 5. Private reference results

The public comparison data contain only the SCXRD observations in Supplementary Tables S1-S3; the theoretical columns, source model ranking and derived reference errors remain evaluator-only. Table S1 contains 13 bonds, Table S2 24 printed angles (23 unique; C6-N1-C7 is repeated), and Table S3 11 torsions. The source tables report near-identical theoretical values for most rows, with notable S1 differences at N5-C18 and N6-C19. These table features must be checked against independently computed, identity-validated results; they are not themselves proof of successful reproduction.

## 6. Limitations and interpretation boundaries

Gas-phase isolated-molecule calculations are compared with a crystal molecular geometry. Agreement does not establish crystal-packing energetics, biological activity, or causal mechanistic claims. Torsion errors must be treated with a circular-angle convention, and any alternative conformer or tautomer must be explicitly identified rather than silently substituted.

## 2026-09-18 molecular identity repair and historical PASS withdrawal

Main PDF p4/Fig.3 specifies pyrazole N1-N2-C9-C8-C7, with N1-C6 phenyl, C7-O1-C11 chlorophenoxy, C8-C17 imine and C9-C10 methyl. The old task SMILES encoded a positional isomer. The public graph and source-label mapping are now corrected, with Cl1/Cl2 as aliases for one chlorine. The original public files and manifest are preserved under docs/verification/group_2/paper_a3968806251093cd/provenance/correct_7a_20260918/original_task_archive/.

Both historical author-level Opt/Freq outputs use the wrong graph and cannot certify this repaired task. New independent correct-object B3LYP/CAM-B3LYP /6-311+G(d,p) calculations are required. The source conclusion and evaluator target are not changed to fit new results; a mixed or unsupported method ranking must remain unqualified. Public SCXRD observations make the requested error analysis possible; no crystal coordinates or author-computed numbers are published. This is an input/contract repair, not a reduced scientific objective or a final-package release.

Fig.3 also places C8 and N4 trans across C17=N3. The repaired public SMILES now specifies this E imine; the independently generated quantum starter already used the same E identity. This corrects an additional missing identity constraint, not a fit to theoretical geometry or an optimization result. Held copies are not automatically released or certified by this repair.
