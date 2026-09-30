# Private paper route

## 1. Scientific objective and author claim

The paper investigates whether the short Au(I)···Au(I) contacts in the tetranuclear cation derived from Au1·ClO4 are genuine aurophilic/metallophilic interactions and characterizes their electronic bonding. The authors claim that the Au4 core is a bent square stabilized by predominantly closed-shell Au···Au contacts with measurable electron sharing.

## 2. System and model boundary

The modeled system is the tetracationic Au1·X species obtained from the Au1·ClO4 crystal structure after removal of non-coordinating perchlorate anions and solvent. It contains four Au(I) centers, four imidazo[1,5-b]pyridazin-7-ylidene ligands, total charge +4, and a closed-shell singlet state. AIM observables are evaluated at the four edge Au···Au bond critical points; NBO analysis concerns donor–acceptor interactions between adjacent gold centers.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the tetracation geometry | Au1·ClO4 crystal structure, with counterions omitted | Gaussian 16 C.02 DFT | BP86-D3BJ/def2-TZVPP; 60-electron relativistic core potential on Au; charge +4, singlet | Optimized Au4 molecular geometry | ev_doc_39cbb1a4b138_000477_d4118622f683; ev_doc_902355b1b6ea_000137_7aae848bd8fc |
| 2 | Validate the optimized core | Optimized geometry | Geometric inspection | Au···Au contacts and Au4 internal-angle sum compared with crystallographic structure | Four edge contacts and bent-square core | ev_doc_902355b1b6ea_000137_7aae848bd8fc |
| 3 | Locate and characterize Au···Au BCPs | Optimized wavefunction exported for analysis | Multiwfn AIM | BCP search; electron density and density derivatives; high-quality basin grid for DI | ρ, ∇²ρ, ELF, H, V, G and DI for Au1–Au2, Au2–Au3, Au3–Au4, Au4–Au1 | ev_doc_39cbb1a4b138_000477_d4118622f683; ev_doc_39cbb1a4b138_000484_74ef8ec127b5 |
| 4 | Interpret interaction character | AIM results | QTAIM criteria | |V|/G used to distinguish closed-shell/shared-shell character | Predominantly closed-shell metallophilic classification | ev_doc_902355b1b6ea_000137_7aae848bd8fc; ev_doc_902355b1b6ea_000155_671c2a6799f7 |
| 5 | Analyze donor–acceptor bonding | Optimized wavefunction | Gaussian 16 NBO | Second-order perturbation analysis | Au lone-pair→Au acceptor and σ(Au–Ccarbene)→Au acceptor interactions | ev_doc_902355b1b6ea_000137_7aae848bd8fc; ev_doc_39cbb1a4b138_000484_74ef8ec127b5 |

## 4. Validation and analysis protocol

The authors first checked that optimization retained a bent Au4 square and Au···Au contacts comparable to the crystal. They then identified four edge BCPs, extracted the AIM descriptors and DIs, and used |V|/G plus the sign of the Laplacian to classify the contacts. NBO second-order donor–acceptor terms were used as a complementary electronic interpretation. The computed descriptors were compared with the qualitative crystallographic observation that the contacts are shorter than the Au van der Waals diameter.

## 5. Private reference results

The SI Table S2 reports, for Au1–Au2/Au2–Au3/Au3–Au4/Au4–Au1 respectively, ρ = 0.03640169464/0.03642032000/0.03651689197/0.03656342640, ∇²ρ = 0.08581458619/0.08589454713/0.08609670303/0.08624755801, ELF = 0.1657512720/0.1657405478/0.1660910668/0.1661557894, H = −0.004291409923/−0.004294386737/−0.004325103962/−0.004336284078, V = −0.03003614516/−0.03006208816/−0.03017405647/−0.03023412800, G = 0.02574473524/0.02576770143/0.02584895251/0.02589784392, and DI = 0.37416067/0.37419798/0.37543573/0.37521239 (atomic units unless otherwise stated). The paper reports |V|/G = 1.167 and interprets the contacts as predominantly closed-shell with minor shared-shell character. NBO Table S4 reports E(2) values 30.75 and 37.07 kcal mol−1 for the two selected donor–acceptor interactions.

## 6. Limitations and interpretation boundaries

The calculation is a finite-cluster, gas-phase electronic-structure model derived from a crystal structure; it does not establish bulk lattice energetics or solution speciation. AIM descriptors and DIs are method- and partitioning-dependent. Agreement with the private values is a reproduction target, not proof that aurophilicity has a unique operational definition. Counterion and solvent effects are intentionally excluded from the modeled cation.
