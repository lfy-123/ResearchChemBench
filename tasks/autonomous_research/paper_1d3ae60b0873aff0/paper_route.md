# Private paper route

## 1. Scientific objective and author claim

The paper tests whether correlated ab initio EPR parameters can predict ligand-nucleus paramagnetic NMR shifts well enough to identify the Fe coordination state and local geometry in Fe@PCN-224. The implemented benchmark system is a neutral, sextet Fe(III)Cl@TCPP cluster. The author claim is that the chloride axial model agrees closely with the observed Fe@PCN-224 shifts and local Fe--N/Fe--Cl distances, whereas hydroxide and Fe(II) alternatives do not.

## 2. System and model boundary

The model is the TCPP linker with one Fe and one axial Cl, using the 86-atom Cartesian structure in SI Table S14. Charge is 0 and multiplicity is 6. Observables are site-averaged isotropic 1H and 13C shifts for the three aromatic proton sites and eight carbon environments, plus EPR/NMR tensors and optimized Fe--N/Fe--Cl distances. Experimental comparison uses the Fe@PCN-224 solid-state MAS NMR data at 320 K.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize model geometry and verify a minimum | SI Table S14 Fe(III)Cl@TCPP coordinates | ORCA 5.0.1, PBE0-D4/def2-TZVP | neutral sextet; TightSCF; TightOpt; numerical Hessian | optimized geometry, frequencies, Fe--N/Fe--Cl distances | ev_doc_e13525bf6fae_000096_647e7f72e349; ev_doc_e13525bf6fae_000462_de625fe42df5 |
| 2 | Compute ligand hyperfine tensors | step-1 geometry | all-electron DLPNO-CCSD | cc-pwCVTZ(Fe,Cl)/EPR-II(O,N,C,H); NoFrozenCore; unrelaxed CCSD density; NormalPNO; T1 diagnostics <=0.016 | A tensors and A_iso | ev_doc_e13525bf6fae_000122_33bf1b34a755; ev_doc_e13525bf6fae_000421_eadfb5acbb53 |
| 3 | Compute orbital shielding | step-1 geometry | GIAO PBE0 | pcSseg-1; RIJCOSX; TightSCF | sigma_orb tensors | ev_doc_e13525bf6fae_000106_ab35e5fab708; ev_doc_e13525bf6fae_000426_df78b2fc1dac |
| 4 | Compute electronic-spin parameters | step-1 geometry | DKH2 state-averaged CASSCF/NEVPT2 | Fe(III) CAS(5,5); 1 sextet, 20 quartet, 30 doublet roots; cc-pwCVTZ-DK(Fe)/cc-pVDZ-DK(other atoms); SOC | g and D tensors | ev_doc_e13525bf6fae_000130_f3f7dcac403c |
| 5 | Assemble shifts | steps 2--4 and T=320 K | published pNMR equations (S2--S3) | average equivalent positions; CH4 reference for orbital shifts | isotropic 1H/13C shifts | ev_doc_e13525bf6fae_000130_f3f7dcac403c |
| 6 | Compare to experiment and structural data | step-5 shifts; X-ray comparison | linear regression and distance comparison | report R2 for 1H and 13C; compare Fe--N and axial distance | assignment and coordination conclusion | ev_doc_7e3fa721f7a7_000172_7b766ef189d6; ev_doc_7e3fa721f7a7_000175_6ef27da77e2f |

## 4. Validation and analysis protocol

The authors require a Hessian-confirmed minimum, coupled-cluster convergence diagnostics, and quantitative comparison of calculated and observed site shifts. Equivalent nuclei are averaged. The model is assessed against the observed 1H positions (beta, meta, ortho) and eight 13C environments, and its Fe--N and Fe--Cl distances are compared to diffraction-derived coordination distances. Alternative axial/oxidation-state models were evaluated in the paper as a sensitivity analysis.

## 5. Private reference results

The paper reports calculated Fe(III)Cl@TCPP shifts, experimental site shifts, R2 values, and Fe--N/Fe--Cl distance comparisons. These values are stored only in evaluator reference files. The central reported correlations are approximately 0.998 for 1H and 0.975 for 13C; the paper reports Fe--N distances of 2.071, 2.071, 2.073, 2.074 A and Fe--Cl 2.224 A for this optimized model.

## 6. Limitations and interpretation boundaries

This is a cluster-model benchmark, not a periodic MOF calculation. Site averaging, finite-temperature treatment, conformational disorder, and model chemistry sensitivity limit direct transfer to every material environment. A failed or incomplete high-level calculation must be reported as such rather than replaced with paper values.
