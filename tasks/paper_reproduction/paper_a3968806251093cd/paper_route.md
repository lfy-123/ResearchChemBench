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

The hidden reference consists of the SCXRD values in Supplementary Tables S1-S3 and the paper's qualitative conclusion that CAM-B3LYP is the closer geometry model overall. Table S1 contains 13 bond-length rows, Table S2 24 angle rows, and Table S3 11 torsion rows. The source tables report near-identical optimized values for most rows, with notable S1 differences at N5-C18 and N6-C19. These values and derived comparison metrics are evaluator-only.

## 6. Limitations and interpretation boundaries

Gas-phase isolated-molecule calculations are compared with a crystal molecular geometry. Agreement does not establish crystal-packing energetics, biological activity, or causal mechanistic claims. Torsion errors must be treated with a circular-angle convention, and any alternative conformer or tautomer must be explicitly identified rather than silently substituted.
