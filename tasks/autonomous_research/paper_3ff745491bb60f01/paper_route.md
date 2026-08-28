# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to compare the ground-state frontier-orbital gaps of fluorescent probe CSO-CY and the hydroxylamine-derived oxime product. The authors claim that hydroxylamine conversion changes the electronic structure in a direction consistent with the observed fluorescence blue shift.

## 2. System and model boundary

The systems are neutral singlet ground-state CSO-CY (SI Table S1, 51 atoms) and neutral singlet CSO-CY + NH2OH oxime product (SI Table S2, 38 atoms). The calculation is a molecular DFT treatment with implicit solvation; the reported observable is the HOMO-LUMO energy gap, not a directly simulated emission spectrum.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize probe geometry | CSO-CY S0 Cartesian coordinates | DFT in ORCA | B3LYP-D3, def2-SVP, CPCM solvation | Optimized CSO-CY geometry | ev_doc_b925c5c8752d_000067_834bbacb18f3; ev_doc_b9b2a39868bb_000057_9eccd44ade03 |
| 2 | Optimize oxime-product geometry | CSO-CY + NH2OH S0 Cartesian coordinates | DFT in ORCA | B3LYP-D3, def2-SVP, CPCM solvation | Optimized product geometry | ev_doc_b925c5c8752d_000067_834bbacb18f3; ev_doc_b9b2a39868bb_000066_e96132083ce3 |
| 3 | Obtain frontier orbitals for probe | optimized probe | ORCA DFT single-point analysis | same model chemistry | HOMO, LUMO and gap | ev_doc_b925c5c8752d_000078_808b10de1d9a |
| 4 | Obtain frontier orbitals for product | optimized product | ORCA DFT single-point analysis | same model chemistry | HOMO, LUMO and gap | ev_doc_b925c5c8752d_000078_808b10de1d9a |
| 5 | Compare gaps | both orbital analyses | arithmetic comparison | product minus probe | gap change and blue-shift interpretation | ev_doc_b925c5c8752d_000080_23c1867a2c75 |

## 4. Validation and analysis protocol

The authors compare the same frontier-orbital observable for both structures after geometry optimization and use the computed change as qualitative support for the optical observation. The paper also describes the hydroxylamine reaction as oxime formation at the probe sensing functionality, with an intermediate and elimination step. No direct excited-state or emission calculation is reported.

## 5. Private reference results

The paper reports a 2.59 eV gap for CSO-CY and 2.99 eV for the hydroxylamine-derived product, giving a product-minus-probe increase of 0.40 eV. It states that this larger gap supports a fluorescence blue shift. Source: ev_doc_b925c5c8752d_000080_23c1867a2c75.

## 6. Limitations and interpretation boundaries

A HOMO-LUMO gap is not an optical excitation or emission energy. The reference does not establish uniqueness of conformers, method independence, or a complete photophysical mechanism. The supplied SI coordinates are the source geometries; independent reproduction may differ with optimization, convergence, solvent implementation, or software details.
