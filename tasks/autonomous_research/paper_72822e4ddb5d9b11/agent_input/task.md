# Scientific objective

Determine whether neutral nanographene complex 4 supports a closed-shell singlet ground state relative to its triplet state. Report the singlet-triplet electronic energy difference in kcal/mol, identify the lower state, and assess whether each optimized state is a true minimum.

# Public inputs and scientific boundaries

`data/inputs/complex_4.xyz` is the complete 165-atom Cartesian geometry from SI Section 13, “Coordinates of 4”. Atom order and element identities are fixed. Use neutral charge (0), comparing multiplicity 1 (singlet) with multiplicity 3 (triplet). The primary target is the electronic energy difference on a defensible common footing; thermal corrections are outside the primary target.

# Required scientific validation/investigation

Plan and execute an independent electronic-structure comparison. Choose and justify the computational model, document basis, convergence, and software. Verify state identity from multiplicity and diagnostics; report convergence; and perform a vibrational or equivalent stationarity check for every optimized state. Ensure the gap uses same-unit energies and consistent geometries, and discuss sensitivity or limitations. Completion requires both states converged and a validated gap/state assignment, or a bounded-failure report naming the failed calculation, attempted alternatives, and limitation. Stop when the comparison is converged and validated, or after documented failure prevents a defensible comparison despite reasonable alternatives.

# Deliverables

Submit `report/results.json` and supporting files referenced by it. Preserve object identity with `singlet_state` and `triplet_state`, methods, and validation. State either `completed` or `bounded_failure`; include `gap_kcal_mol` and `lower_state` only when completed, and a specific limitation when bounded_failure.
