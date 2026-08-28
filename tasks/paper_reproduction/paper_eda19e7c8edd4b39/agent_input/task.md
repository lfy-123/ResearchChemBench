# Scientific objective

Determine the neutral substitutional Ni-vacancy and Al-vacancy formation energies in ordered bulk β-NiAl (B2), and test the authors' qualitative hypothesis that unequal vacancy energetics can favor Ni defect formation and thereby be consistent with preferential Ni transport toward a surface. The scored objects are the two bulk defect energies, their difference/order, and the defensibility of the computational validation; no surface transition state or precipitate structure is scored.

# Public inputs and scientific boundaries

Use `data/inputs/beta_nial_b2_primitive.poscar` as the ordered B2 conventional cell: cubic lattice parameter 2.890 Å, Ni at fractional (0,0,0), Al at (0.5,0.5,0.5), one formula unit, neutral periodic solid. `system_definition.json` fixes the defect identities and requires a neutral charge state. Build a periodic supercell, remove exactly one Ni for the Ni-vacancy state and exactly one Al for the Al-vacancy state. The measurement is the 0 K electronic formation energy in eV under your stated elemental-reservoir convention; state whether ions and cell are relaxed, the magnetic treatment, and all model choices. Do not use the paper, SI, source-data archive or general web as inputs.

# Required scientific validation/investigation

Plan and execute a reproducible periodic first-principles calculation or an explicitly justified equivalent. Establish a pristine reference and both defect states with identical conventions. Demonstrate numerical convergence or sensitivity for supercell size and the dominant numerical settings, report total energies and the formation-energy equation, and show that atom counts and the removed sublattice are correct. Deduplicate repeated calculations and advance a setting only when the preceding result is internally consistent. Completion is reached when both defect energies, their difference, convergence evidence, and a limitation statement are reported. Stop after a converged comparison or, if resources prevent convergence, report the best bounded result and the exact unresolved sensitivity; do not claim success from a single unvalidated calculation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For a completed investigation, include method provenance, pristine/Ni-vacancy/Al-vacancy energies, formation energies with units and reservoir convention, ordering, validation evidence, and limitations. If convergence cannot be achieved, use the bounded-failure branch and report the validated work, exact missing calculation or unresolved sensitivity, and its consequences without fabricating energies or an ordering. The report must distinguish computed values from interpretation and must not silently substitute a surface or diffusion calculation for the requested bulk observable.
