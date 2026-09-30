# Scientific objective

Independently determine the neutral substitutional Ni-vacancy and Al-vacancy formation energies in ordered bulk β-NiAl (B2), compare the two defect classes, and state what conclusion about relative defect propensity is justified by the calculation. The benchmark is route-neutral: discover and justify your own computational model and validation strategy.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that unequal formation energies for neutral substitutional vacancies in ordered β-NiAl can favor formation of Ni vacancies. They interpret that energetic asymmetry as consistent with preferential Ni transport toward a surface and associated Ni enrichment, while the bulk vacancy comparison alone does not establish the complete surface or diffusion mechanism.

**Candidate route or mechanism.**
The candidate explanation is a bulk defect-mediated route in which Ni-vacancy formation is energetically preferred to Al-vacancy formation, enabling Ni-related mass exchange toward a surface. Treat this as a proposed interpretation to test through the requested bulk calculations; surface exchange and diffusion processes are contextual comparisons rather than replacement observables.

**Discriminating evidence.**
Distinguish the claim by calculating pristine, neutral Ni-vacancy, and neutral Al-vacancy total energies under one consistent periodic model, then evaluating the formation-energy difference with an explicit elemental-reservoir convention. Test whether the ordering is numerically stable through supercell and dominant-setting sensitivity or convergence checks, and use atom-count, sublattice, charge, and relaxation validation to support the comparison.

# Public inputs and scientific boundaries

Use `data/inputs/beta_nial_b2_primitive.poscar` as the ordered B2 conventional cell: cubic lattice parameter 2.890 Å, Ni at fractional (0,0,0), Al at (0.5,0.5,0.5), one formula unit, neutral periodic solid. `system_definition.json` fixes the defect identities and requires a neutral charge state. Build a periodic supercell, remove exactly one Ni for the Ni-vacancy state and exactly one Al for the Al-vacancy state. The measurement is the 0 K electronic formation energy in eV under your stated elemental-reservoir convention. The public problem contains no author mechanism or candidate route; do not use the paper, SI, source-data archive or general web as inputs.

# Required scientific validation/investigation

Propose and execute a reproducible periodic first-principles calculation or a justified equivalent. Generate and compare the pristine, Ni-vacancy and Al-vacancy states under one coherent convention. Validate the atom identities, charge, relaxation and numerical convergence or sensitivity, and report coverage of the settings explored. Completion is reached when both formation energies, their difference/order, validation evidence, and an independently reasoned interpretation are available. Stop after convergence and a stable comparison, or report bounded failure with the exact missing calculation and limitation; a single unvalidated number is incomplete.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For a completed investigation, include the discovered method, all reference and defect energies, formation energies with units and reservoir convention, ordering, validation evidence, conclusion, and limitations. If the investigation remains bounded by a missing calculation or unresolved sensitivity, use the bounded-failure branch and report that exact limitation without fabricating energies or an ordering. Do not invent an experimental result or claim that bulk vacancy energetics alone proves a complete surface mechanism.
