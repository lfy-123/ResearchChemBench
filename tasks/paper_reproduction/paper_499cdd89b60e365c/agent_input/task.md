## Scientific objective

Test the authors' qualitative hypothesis that reduction of gallium oxide can produce a thermodynamically stable Ga-substituted Cu(111) surface alloy at methanol-synthesis conditions, while bulk Cu–Ga alloying is less favored there. Independently plan and perform calculations for Cu, β-Ga2O3, H2/H2O, Cu bulk, and Ga-substituted Cu(111). Report the stable Ga surface coverage at 230 °C and H2O/H2 = 0.003, together with the corresponding bulk comparison. Do not assume a particular winning coverage or numerical energy.

## Public inputs and scientific boundaries

Use `data/inputs/cu111_base.cif` as a 2×2 Cu(111) four-layer slab, `cu_bulk.cif` as the Cu reference, `h2.xyz` and `h2o.xyz` as neutral singlet molecules, and `system_spec.json` for the reaction point, allowed top-layer substitutions, and β-Ga2O3 Materials Project record mp-1008844. Preserve atom identity and charge/multiplicity; only replace top-layer Cu by Ga. The physical boundary is Cu/Cu(111), Ga2O3, H2 and H2O. The observable is thermodynamic stability/free-energy difference and stable Ga coverage, not catalytic rate or kinetic mechanism. You may choose software, functional, convergence settings, and candidate coverage sampling, but disclose them.

## Required scientific validation/investigation

Generate a finite, explicitly listed set of symmetry-distinct top-layer substitutions spanning the supplied coverages; deduplicate equivalent structures and retain a unique candidate ID, composition, coordinates, and relaxation status for every candidate. Optimize all candidates and references, report force/energy convergence, audit atom counts and fixed layers, and construct a consistent oxide/H2/H2O-referenced chemical-potential balance. Compare both surface and bulk alloy families at 503.15 K and H2O/H2=0.003. Completion requires either a converged stable-coverage assignment plus bulk/surface comparison, or a bounded-failure report identifying the missing calculation and the best-supported interval. In bounded failure, do not invent energies or stable coverage for unevaluated or non-converged candidates. Stop when all requested coverages have been evaluated or when a documented numerical/resource limit prevents further evaluation; report coverage and validation limitations.

## Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include methods, candidate records, energies/free-energy differences with units, reaction-point stable coverage or interval, bulk comparison, validation evidence, conclusion, and limitations. Include enough coordinates or file references to reproduce every advanced candidate.
