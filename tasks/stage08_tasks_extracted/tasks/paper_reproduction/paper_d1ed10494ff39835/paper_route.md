# Private paper route

## 1. Scientific objective and author claim

The paper studies the late-lanthanide monohydrate LuFe(SO4)3(H2O) (compound 14). The authors optimized crystal structures with periodic DFT and then used self-consistent calculations to inspect DOS and ELF/real-space electron density. Their interpretation is that O-centered localization and Fe–O/S–O hybridization indicate covalent bonding components, while weak Lu localization and an asymmetric electron distribution are consistent with the noncentrosymmetric R3c structure.

## 2. System and model boundary

The computational object is the periodic compound-14 crystal: one Lu, one Fe, one S and five O atoms in the asymmetric unit, with trigonal R3c symmetry. The experimental cell is a≈b=8.7636 Å, c=21.9397 Å, α=β=90°, γ=120°. The composition is LuFeS3O13 (equivalent to LuFe(SO4)3(H2O)); Lu and Fe are treated as trivalent and sulfate S as hexavalent in the chemical interpretation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax the crystal | Experimental compound-14 structure | VASP periodic DFT | PBE-GGA; 520 eV plane-wave cutoff; force convergence 1×10^-2 eV Å^-1; energy convergence 1×10^-4 eV | Optimized lattice and positions | ev_doc_62e010b0c664_000208_d797eb4f7b09; ev_doc_62e010b0c664_000209_9d457f9f46a4; ev_doc_62e010b0c664_000215_599cab63d7d5; ev_doc_62e010b0c664_000216_2f774598c4f1 |
| 2 | Obtain converged density | Optimized compound-14 structure | VASP SCF | 520 eV cutoff; energy convergence 1×10^-4 eV | Self-consistent charge density | ev_doc_62e010b0c664_000217_34a5c54fab12 |
| 3 | Map localization | SCF density | VASP ELF calculation | Same SCF cutoff/convergence; ELF volumetric output | ELF/real-space localization map | ev_doc_62e010b0c664_000217_34a5c54fab12; ev_doc_62e010b0c664_000567_5dfa2a4b3c39 |
| 4 | Resolve orbital contributions | SCF calculation | VASP DOS/PDOS | Same SCF calculation; total and projected DOS | DOS with O, S, Fe and Lu projections | ev_doc_62e010b0c664_000217_34a5c54fab12; ev_doc_62e010b0c664_000559_cd3075a8f939 |
| 5 | Interpret bonding and polarity | Optimized structure, DOS and ELF | Compare profiles and real-space features | Fermi level referenced to 0 eV; qualitative feature comparison | Bonding/noncentrosymmetry interpretation | ev_doc_62e010b0c664_000566_1feef1823056; ev_doc_62e010b0c664_000567_5dfa2a4b3c39; ev_doc_62e010b0c664_000571_8e189b6ad2f5; ev_doc_62e010b0c664_000573_c120f42cf210 |

## 4. Validation and analysis protocol

The paper's analysis checks the relaxed crystal against the experimental structure, then checks the DOS in three energy windows: O-2s-dominated deep valence states around −20 eV; S-3s/3p and O-2p contributions from about −12 to −6 eV; and overlapping Fe-3d/O-2p weight from about −5 to 0 eV. Lu-4f states are described as sharp and localized slightly below the Fermi level. The ELF map is inspected for strong O-centered localization in Fe–O and S–O environments, weak Lu localization, asymmetric O lobes, and aligned Lu–O(water) character along c.

## 5. Private reference results

The hidden reference is the source-supported qualitative profile above, together with the experimental compound-14 cell and coordinates in SI Table S15. The paper reports the compound-14 space group as R3c and the measured cell as a=b=8.7636(2) Å, c=21.9397(5) Å, γ=120°. No numerical DOS peak or ELF-asymmetry score is asserted because the paper does not tabulate one; evaluation therefore uses feature-wise semantic/condition rules.

## 6. Limitations and interpretation boundaries

The paper omits several ordinary numerical settings (k mesh, smearing, PAW dataset, spin setup and exact DOS/ELF tags), so the public task permits a justified reproducible choice and requires reporting it. DOS peak positions and ELF asymmetry are assessed qualitatively because Figure 6 is graphical and no tabulated numerical target exists. Agreement with an author interpretation does not establish a unique causal bonding decomposition; the result is limited to the stated periodic ground-state model and chosen numerical settings.
