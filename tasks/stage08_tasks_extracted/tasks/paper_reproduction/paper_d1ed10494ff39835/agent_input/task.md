# Scientific objective

Using the supplied periodic crystal model, independently determine the electronic structure and spatial electron-localization characteristics of LuFe(SO4)3(H2O), and decide what bonding character and symmetry of the electron distribution are supported by the calculations. Generate and test your own plausible interpretations and discriminate them using the computed evidence.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the bonding as including covalent Fe–O and S–O contributions and propose that the electron distribution reflects the crystal's lack of inversion symmetry.

**Candidate route or mechanism.**
Test this interpretation through Fe–O and sulfate S–O orbital hybridization and the spatial distribution of oxygen lone-pair and bonding localization. Compare these environments with the Lu coordination environment, including the orientation of Lu–O(water) bonds relative to the c axis.

**Discriminating evidence.**
Use periodic DFT projected DOS to examine O s/p, S s/p, Fe d and Lu f contributions and orbital overlap across the valence states. Combine this with real-space localization analysis around O and Lu, checking the shapes of oxygen-centered lobes and their behavior under inversion across the unit cell. These complementary analyses test the bonding interpretation and its connection to electron-distribution symmetry.

# Public inputs and scientific boundaries

`data/inputs/compound14.cif` is the complete periodic starting model: LuFe(SO4)3(H2O), formula LuFeS3O13, R3c (No. 161), a=b=8.7636 Å, c=21.9397 Å, α=β=90°, γ=120°, Z=6, with unique sites Lu1, Fe1, S1 and O1–O5. Fractional coordinates and symmetry operations are in the CIF. Use neutral-crystal stoichiometry and state charge, spin treatment, pseudopotentials, k-point sampling, smearing and all other choices. The target is the periodic electronic ground state within the chosen reproducible model; the starting cell is a structural reference only.

# Required scientific validation/investigation

Design and document a reproducible periodic calculation, relax the structure or justify a fixed-structure calculation, and show numerical convergence. Report cell metrics, composition, symmetry handling and a coordinate comparison or displacement summary against the supplied model. Compute total and element/orbital-resolved DOS with an explicit energy reference, range and resolution. Compute ELF or a defined equivalent localization field and provide a rendered map or quantitative descriptors tied to named atoms/regions. Form at least two plausible interpretations of the bonding/electron distribution from the computed observables, identify what evidence discriminates them, and state residual ambiguity. Completion requires all artifacts, reproducibility metadata, convergence evidence and an evidence-backed final decision; partial work must enumerate unsupported observables and a scientifically justified stopping reason. Stop when convergence is stable and DOS/localization analysis has discriminated the proposed interpretations, or when a documented resource/software limitation prevents completion.

# Deliverables

Submit `report/results.json` plus referenced files under `report/`. Conform to the local `submission_schema.json`, including its required files and the applicable complete or partial result schema. `status` is `complete` or `partial`; partial work must include a limitation. DOS and ELF entries must include named feature/region assessments and artifact paths. Record at least two proposed interpretations and the discriminating evidence in the schema-conforming report, unless the status is partial with an explicit reason. The conclusion must identify the supported bonding character and electron-distribution symmetry, scope and uncertainty. Include coordinate/cell output, DOS data/plot, ELF data/plot, and logs or convergence evidence.
