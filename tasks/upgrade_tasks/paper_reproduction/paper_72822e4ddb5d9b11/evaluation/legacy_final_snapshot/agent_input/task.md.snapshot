# Scientific objective

Compare the relaxed closed-shell singlet and triplet states of neutral nanographene complex 4. Calculate their adiabatic electronic energy difference and determine which of these two states is lower.

# Author-provided scientific guidance

The author route tests a closed-shell singlet assignment by separate optimization and comparison with a triplet calculation. Evaluate the two states without assuming their energetic ordering.

# Public inputs and scientific boundaries

`data/inputs/complex_4.xyz` defines the complete 165-atom C87H72Cl2N2NiO complex. Use charge 0 and multiplicities 1 and 3, preserving chemical identity. The primary quantity is [E_triplet(relaxed) − E_singlet(relaxed)] in kcal/mol: optimize each state independently under the same declared model. A positive value means the singlet is lower; this definition supplies no expected sign. It is not a vertical same-geometry gap and contains no thermal/free-energy correction. Such controls may be reported separately. No paper, SI, evaluator, historical verification archive or general-web lookup is an agent input.

# Required scientific validation/investigation

Choose and document the method, basis, software and numerical settings. Check each state's multiplicity, electronic convergence and vibrational/equivalent stationary-point evidence. Retain both electronic energies in Hartree, the conversion, numerical gap and lower-state assignment, so they can be independently checked. The comparison concerns these specified states, not all possible electronic states or geometrical discovery.

# Deliverables

Submit `report/results.json` and cited supporting files. `completed` requires both optimized validated states, their electronic energies, `gap_kcal_mol` and `lower_state`. Otherwise use `bounded_failure` with `failure_reason` and whatever diagnostics/results actually exist; unavailable energies are not mandatory. Optional extra attempts must not overwrite the two primary state records.
