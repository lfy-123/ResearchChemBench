# Scientific objective

Using the supplied periodic crystal model, independently determine the electronic structure and spatial electron-localization characteristics of LuFe(SO4)3(H2O), and decide what bonding character and symmetry of the electron distribution are supported by the calculations. Generate and discriminate plausible interpretations from the computed evidence; no author route, candidate mechanism or expected result is provided.

# Public inputs and scientific boundaries

`data/inputs/compound14.cif` is the complete periodic starting model: LuFe(SO4)3(H2O), formula LuFeS3O13, R3c (No. 161), a=b=8.7636 Å, c=21.9397 Å, α=β=90°, γ=120°, Z=6, with unique sites Lu1, Fe1, S1 and O1–O5. Fractional coordinates and symmetry operations are in the CIF. Use neutral-crystal stoichiometry and state charge, spin treatment, pseudopotentials, k-point sampling, smearing and all other choices. The target is the periodic electronic ground state within the chosen reproducible model; the starting cell is a structural reference only.

# Required scientific validation/investigation

Design and document a reproducible periodic calculation, relax the structure or justify a fixed-structure calculation, and show numerical convergence. Report cell metrics, composition, symmetry handling and a coordinate comparison or displacement summary against the supplied model. Compute total and element/orbital-resolved DOS with an explicit energy reference, range and resolution. Compute ELF or a defined equivalent localization field and provide a rendered map or quantitative descriptors tied to named atoms/regions. Form at least two plausible interpretations of the bonding/electron distribution from the computed observables, identify what evidence discriminates them, and state residual ambiguity. Completion requires all artifacts, reproducibility metadata, convergence evidence and an evidence-backed final decision; partial work must enumerate unsupported observables and a scientifically justified stopping reason. Stop when convergence is stable and DOS/localization analysis has discriminated the proposed interpretations, or when a documented resource/software limitation prevents completion.

# Deliverables

Submit `report/results.json` plus referenced files under `report/`. The JSON must contain `status`, `method`, `structure`, `dos`, `elf`, `hypotheses`, `validation`, and `conclusion`. `status` is `complete` or `partial`; partial work must include a limitation. DOS and ELF entries must include named feature/region assessments and artifact paths. `hypotheses` must record at least two proposed interpretations and the discriminating evidence, unless the status is partial with an explicit reason. The conclusion must identify the supported bonding character and electron-distribution symmetry, scope and uncertainty. Include coordinate/cell output, DOS data/plot, ELF data/plot, and logs or convergence evidence.
