# Scientific objective

Compute the work functions of two named, clean TiO2 surfaces: anatase TiO2(101) and rutile TiO2(110). Test the reproduction hypothesis that the phase with the lower work function can donate electrons toward the phase with the higher work function, as a component of the proposed hetero-phase charge-transfer picture. The measured quantity is each surface work function, defined as the vacuum electrostatic-potential plateau minus the slab Fermi energy, in eV, plus their signed difference and ordering.

# Public inputs and scientific boundaries

Use `data/inputs/anatase_bulk.POSCAR` (anatase TiO2, Materials Project identity cross-check mp-390) and `data/inputs/rutile_bulk.POSCAR` (rutile TiO2, mp-2657), and `data/inputs/slab_protocol.json`. Construct neutral, stoichiometric, nonmagnetic symmetric slabs exposing Miller facets (101) and (110), respectively, using six atomic layers, the stated in-plane repetition, identical terminations on both faces, and 18 Å vacuum unless a justified converged equivalent is reported. No adsorbates, dopants, solvent, external field, or interface is included. You may choose software and model chemistry, but report all choices and do not use the paper or general web to fill missing inputs.

# Required scientific validation/investigation

Independently plan and execute slab relaxation followed by a work-function calculation for both named surfaces. Demonstrate force convergence (or report a bounded failure), identify a genuine vacuum plateau and Fermi reference, and retain per-surface identity with input structure and calculation settings. Check at least one relevant numerical sensitivity (vacuum, slab thickness, k-point sampling, or equivalent) when computationally feasible; if not, state why and quantify the limitation. The calculation is complete when both surfaces have either a reproducible converged work function with extraction evidence or an explicitly documented failure, and the comparison and limitations are reported. Stop after both endpoints and the required validation are covered; do not expand to other facets or materials.

# Deliverables

Submit `report/results.json` conforming to the schema. Include both named surfaces, work functions in eV when obtained, signed difference/order when both are available, convergence and plateau evidence, methods, sensitivity, and a conclusion that independently assesses the qualitative author hypothesis. A bounded failure branch is allowed only with concrete diagnostics and attempted-surface records.
