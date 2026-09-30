# Private paper route

## 1. Scientific objective and author claim

The paper determines the isolated-molecule equilibrium structure of neutral meso-phenyl-BODIPY (4,4-difluoro-8-phenyl-4-bora-3a,4a-diaza-s-indacene) by GED/MS and uses quantum chemistry to assess geometry prediction. The authors report an almost planar dipyrromethene skeleton with a twisted phenyl group and recommend CAM-B3LYP, PBE0 and mPW1PW91 for related molecular geometries. (Main-paper abstract; ev_doc_204b13446b5a_000018_4fab1d13b8ff.)

## 2. System and model boundary

The system is the isolated, neutral, closed-shell 31-atom molecule C15H11BF2N2, treated as a gas-phase equilibrium structure. Hydrogen-containing distances are excluded from the paper's GED comparison; the reported comparison sets contain 190 non-hydrogen internuclear distances and a 23-distance bonded subset. (SI computational details, ev_doc_ef7758f7e469_000016_72f104e8280f and ev_doc_ef7758f7e469_000086_01b606515116.)

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate starting and comparison geometries | Ph-BODIPY connectivity | Gaussian 09 DFT/MP2/semiempirical; ORCA composite methods | Gaussian optimizations tight convergence, ultrafine grid; ORCA tight thresholds | Optimized geometries | ev_doc_ef7758f7e469_000086_01b606515116 |
| 2 | Establish a high-level energetic reference for optimized structures | Optimized geometries | ORCA DLPNO-CCSD(T0) single points | TightPNO, VeryTight SCF, cc-pVTZ and cc-pVQZ, cc-pVnZ/C RI | Relative energies and T1/T2 diagnostics | ev_doc_ef7758f7e469_000086_01b606515116 |
| 3 | Remove basis-set incompleteness in the energy comparison | Two cardinal-basis energies | Two-point CBS extrapolation | n=3,4 expression given as Eq. (4) | CBS relative energies | ev_doc_ef7758f7e469_000097_791fb1086f34 |
| 4 | Obtain the experimental equilibrium reference | GED/MS data and QC force-field information | UNEX GED refinement with VibModule corrections | RM refinement, alpha_reg=60; B3LYP/cc-pVTZ starting parameters; final Rf=5.49% | Refined re structure | ev_doc_ef7758f7e469_000090_2dd44577d51c; ev_doc_ef7758f7e469_000370_deae461117d2 |
| 5 | Quantify geometry agreement | Each QC geometry and GED re structure | Distance post-processing | MUE, MSE, RMSE; all 190 and bonded 23 non-H distances | Geometry-error metrics | ev_doc_ef7758f7e469_000086_01b606515116; ev_doc_204b13446b5a_000233_ca5a30ddbbe4 |

## 4. Validation and analysis protocol

The authors compare non-hydrogen internuclear distances using MUE, MSE and RMSE, separately for all distances and bonded distances. They use the GED RM refinement with alpha_reg=60 as the final experimental result and also assess sensitivity to MOCED/RM choices. Electronic-structure sanity checks include DLPNO T1=0.012, T2=0.047 and FOD NFOD=0.38. A phenyl torsion scan is used to analyze the structural distortion landscape; the reported scan identifies a low-energy twisted arrangement and a high barrier region. (SI pp. 3–6; main paper pp. 4–5.)

## 5. Private reference results

The hidden GED re coordinates are SI Table S32 (RM, alpha_reg=60, Rf=5.49%). The paper reports for the best all-distance comparison a CAM-B3LYP MUE of 0.009 Å, MSE of -0.001 Å and RMSE of 0.012 Å. For bonded distances, the minima are reported for PBE0 and mPW1PW91: MUE 0.003 Å, MSE 0.000 Å and RMSE 0.004 Å. The high-level CBS energy table (SI Table S37) reports B98 and TPSSh as lowest-energy geometries; PBE0 and mPW1PW91 are among the low-relative-energy geometries. These values and identities are evaluator-private. (ev_doc_204b13446b5a_000233_ca5a30ddbbe4; ev_doc_ef7758f7e469_000370_deae461117d2; ev_doc_ef7758f7e469_000086_01b606515116.)

## 6. Limitations and interpretation boundaries

GED has reduced sensitivity to hydrogen coordinates and some out-of-plane distortions. The comparison tests gas-phase equilibrium geometry, not condensed-phase structure, spectra, kinetics or general functional performance. Reproductions using alternative software, grids, conformer protocols or numerical precision must report those choices and should be interpreted as independent computational tests rather than exact software reproduction.
