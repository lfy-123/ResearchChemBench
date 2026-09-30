# Private paper route

## 1. Scientific objective and author claim

The authors use electronic-structure calculations to connect alkyl-chain length in zwitterionic amino-acid additives to preferred molecular conformation and dipole moment. Their claim is that β-alanine (AL) favors a folded conformation because its terminal ammonium and carboxylate groups approach one another, whereas 4-aminobutyric acid (AB) favors an extended conformation because the longer chain separates those groups; the extended AB dipole is larger and helps explain its interfacial action in aqueous Zn–I2 batteries.

## 2. System and model boundary

The molecular systems are isolated zwitterionic AL ([NH3+]CCC(=O)[O-]) and AB ([NH3+]CCCC(=O)[O-]) in an aqueous environment. The reported conformer energies include an implicit-water optimization followed by a 50-water explicit cluster, semiempirical relaxation, and a single-point calculation; the dipole comparison is made for the surveyed conformers. This computational task does not model the Zn slab, iodine complexes, or electrochemical cell.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate starting conformers | AL and AB zwitterions | Molecular dynamics in Avogadro | MMFF94 force field | Initial conformer geometries | ev_doc_26c71512ab78_000047_b9790b9dc21b |
| 2 | Optimize molecular structures | Initial conformers | ORCA DFT | B3LYP-D4/def2-TZVP, CPCM water, ORCA 6.0.1 | Optimized molecular geometries | ev_doc_26c71512ab78_000047_b9790b9dc21b |
| 3 | Add explicit solvent and relax | Optimized structures | Packmol plus xtb optimization | 50 water molecules; GFN2-xTB | Relaxed solvated clusters | ev_doc_26c71512ab78_000047_b9790b9dc21b |
| 4 | Compare conformers and polarity | Relaxed solvated clusters | ORCA single points and dipole analysis | Solvation energy taken as complex energy minus water-network energy | Relative conformer stability and dipole moments | ev_doc_26c71512ab78_000047_b9790b9dc21b; ev_doc_02148dc7041c_000037_d5e3a2879799; ev_doc_02148dc7041c_000041_cec4130099c7 |

## 4. Validation and analysis protocol

The authors survey multiple conformers for each additive, identify the lowest calculated solvated energy, and compare the corresponding structures and dipoles. The main-text interpretation is checked against the conformational survey (SI Figure S5), dipole survey (SI Figure S7), electrostatic-potential discussion, and FT-IR interpretation. The calculation is interpreted as a molecular-structure explanation, not as a direct prediction of battery lifetime.

## 5. Private reference results

The source-backed reference is qualitative/ordering-based: AL's preferred conformer is folded; AB's preferred conformer is extended; the extended AB conformer has a larger dipole moment than the folded AL conformer. The SI figures contain plotted conformer values, but the normalized evidence does not provide a reliable machine-readable numerical table, so no exact plotted number is used as a scored target.

## 6. Limitations and interpretation boundaries

The paper does not publish unique Cartesian starting coordinates or a complete machine-readable conformer table. Conformer labels are therefore structural (terminal-group contact versus separated/extended backbone), and independent conformer searches may produce different local minima. The result supports the reported molecular trend; it does not establish a unique global conformer under all solvent, temperature, protonation, or sampling models.
