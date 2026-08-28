# Private paper route

## 1. Scientific objective and author claim

The paper studies DQCS, a coumarin/8-hydroxyquinoline Schiff-base fluorescent probe, and its 1:1 divalent-metal complexes. Its computational claim is that coordination changes the electronic structure and that the Ni(II) complex is the most strongly interacting/most electronically softened member of the Cd(II), Co(II), Ni(II) series.

## 2. System and model boundary

The modeled objects are the optimized 1:1 DQCS+Cd2+, DQCS+Co2+, and DQCS+Ni2+ complexes in implicit DMSO. The SI supplies 65-center Cartesian geometries for each complex (Tables S1–S3); each is reported as charge +2, singlet, multiplicity 1. The paper also analyzes free DQCS, but the public benchmark is restricted to the three complete SI complex coordinate sets.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state structures | DQCS and 1:1 Cd, Co, Ni complexes | Gaussian 09 W DFT | B3LYP; 6-311G(d,p) for DQCS and LanL2DZ for metal complexes; DMSO solvent model; complexes +2, singlet | Optimized geometries | ev_doc_f3c1f276c075_000011_aa7b58aaaa7c; ev_doc_f3c1f276c075_000038_05dc405900f0; ev_doc_d0597d980d95_000090_10e60c44cd36 |
| 2 | Obtain orbital and reactivity properties | Optimized structures | Gaussian 09 W DFT | Same functional/basis/solvent assignment | HOMO/LUMO, ESP and global descriptors | ev_doc_f3c1f276c075_000069_6f226cc1ee15; ev_doc_f3c1f276c075_000071_cdb032ea4a26 |
| 3 | Population analysis | Optimized structures | Gaussian 09 W Mulliken analysis | Same DFT settings | Atomic charge distributions | ev_doc_d0597d980d95_000006_d3e829133845; ev_doc_d0597d980d95_000007_bcbab7f470dd |
| 4 | Excited-state analysis | Optimized structures | Gaussian 09 W TD-DFT | First ten singlet states; same system-specific basis assignment and DMSO | Excitation energies, wavelengths, oscillator strengths, transitions | ev_doc_f3c1f276c075_000041_fab44350f40e; ev_doc_d0597d980d95_000003_5e35edb4ae81 |

## 4. Validation and analysis protocol

The authors compare optimized structures and electronic descriptors across the free probe and three complexes. They report a dihedral-angle analysis, ESP redistribution around the imine N, hydroxyl O and quinoline N donor region, Mulliken charges, HOMO/LUMO localization, the HOMO–LUMO gap, and conceptual-DFT descriptors. Experimental fluorescence quenching and binding constants are used as interpretation context, not as computational inputs.

## 5. Private reference results

The reported HOMO–LUMO gaps are 1.997 eV (Cd), 1.511 eV (Co), and 1.243 eV (Ni). Table 1 reports hardness 0.998, 0.755, 0.621 eV and electrophilicity 9.957, 15.112, 19.744 eV, respectively. The ordering is Ni lowest gap/hardness and highest electrophilicity, followed by Co, then Cd. The paper reports donor-region charge redistribution/ICT upon coordination and dihedral angles −22.2°, −29.3°, −36.1° for Cd, Co, Ni.

## 6. Limitations and interpretation boundaries

These are single reported geometries and a single implicit-solvent, charge/spin assignment per complex; they do not establish solution speciation, binding free energies, or a unique mechanistic cause of fluorescence quenching. HOMO–LUMO gaps and Mulliken charges are method-dependent descriptors. Alternative validated methods may differ numerically and must be reported as such.
