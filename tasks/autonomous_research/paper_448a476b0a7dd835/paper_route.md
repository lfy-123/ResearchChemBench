# Private paper route

## 1. Scientific objective and author claim

The authors sought an artificial DNA base pair whose intrinsic base--base interaction is directional and strong enough to support a strand-compatible, approximately planar pairing geometry. Their computational screen identified the iodine-containing IIPO--oIPP model as the most promising motif, and the subsequent biochemical work tested incorporation of dIIPO opposite doIPP.

## 2. System and model boundary

The computational model truncates each nucleoside to its nucleobase plus a methyl group at the C1' sugar-attachment position. The isolated pair is treated in the gas phase; phosphodiester backbone, glycosidic-torsion preferences, vertical stacking, and duplex/solvent effects are omitted. The principal observable is the interaction reaction enthalpy of the dimer relative to the two isolated monomers. A methyl--methyl (C1'--C1') distance of 10.5--10.7 Å is used as a proxy for strand compatibility, and at least one coplanar optimized conformation is required for a candidate to remain in the screen.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Explore low-energy conformations | Methyl-capped monomer/dimer models | CREST/GFN2-xTB | 6 kcal/mol energy window; 0.125 Å RMSD, 0.05 kcal/mol energy and 0.01 Boltzmann pruning; cregen; up to ten distinct conformers; approximately planar interface constraints for dimers | Representative conformer ensemble | ev_doc_be078d0660ba_000597_b411c47da935 |
| 2 | Optimize structures and verify minima | Representative conformers | Gaussian 16, ωB97X-D | Gas phase; 6-311+G(d,p) for H--Ar; aug-cc-pVTZ-PP for Br/I; opt/freq | Optimized geometry and frequencies; minima have no imaginary frequencies | ev_doc_be078d0660ba_000600_bce450bb0a10, ev_doc_be078d0660ba_000610_5677346d43f7 |
| 3 | Refine electronic energies | Optimized monomer and dimer geometries | ORCA 5.0.3, RI-DSD-BLYP-D3(BJ) | def2-TZVPPD; RIJCOSX; def2/J and def2-TZVPPD/C | Refined electronic energies | ev_doc_be078d0660ba_000611_dd8b4083b322, ev_doc_be078d0660ba_000613_eccc5c9fa710 |
| 4 | Obtain thermochemical interaction quantity | Electronic energies plus harmonic frequencies | ORCA quasi-harmonic thermochemistry | Grimme quasi-harmonic treatment; reaction enthalpy rather than entropy-free screening | ΔH(pair) = H(dimer) − H(monomer A) − H(monomer B) | ev_doc_be078d0660ba_000615_65c96475d08f |
| 5 | Interpret interaction origin | Optimized electron densities/geometries | Gaussian/NBO6, NCIPLOT 3.0, PyMOL; Psi4 1.3.2 SAPT0 | SAPT0/def2-TZVPP with density fitting | NBO charge transfer, NCI/ESP maps, SAPT components | ev_doc_be078d0660ba_000597_b411c47da935 |

## 4. Validation and analysis protocol

The authors screened a broad candidate set, then systematically varied iodine to bromine and carbonyl oxygen to sulfur. They compared interaction enthalpy, C1'--C1' distance, planarity, NBO n→σ* charge transfer, and SAPT0 components. They report that the IIPO--oIPP motif is especially favorable, iodine analogues generally interact more strongly than bromine analogues, and sulfur-containing variants commonly distort from planarity. The computational interpretation is limited to intrinsic gas-phase model interactions and is not a direct prediction of duplex thermodynamics.

## 5. Private reference results

For Basepair 1 (I-I-O-O), the SI gives dimer SCF energy −1926.252174 hartree and enthalpy correction +0.349903 hartree. The corresponding BaseA1 and BaseB1 monomer records give −1002.271093/+0.196029 and −923.961977/+0.151782 hartree. Combining these source values gives ΔH = −0.017012 hartree = −10.675 kcal/mol (−44.66 kJ/mol). The source SAPT0 total for the same pair is −56.2922 kJ/mol. The authors' source-backed qualitative conclusion is that IIPO--oIPP is a promising, halogen-bond-supported, approximately planar, strand-compatible motif.

## 6. Limitations and interpretation boundaries

The methyl cap is only a sugar-attachment proxy. The gas-phase model omits solvent, backbone, stacking, and glycosidic conformational costs; the screen therefore compares intrinsic pair interactions rather than predicting full duplex behavior. Numerical agreement should be interpreted with method and conformer sensitivity reported by the researcher, not as experimental accuracy.
