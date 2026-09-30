# Scientific objective

For the supplied periodic bulk crystalline-Si/Li interstitial system, independently determine how adding one electron changes the Li migration barrier and assess whether the computed electronic structure provides a physically supported explanation. Formulate and discriminate plausible explanations using your calculations; do not rely on any external paper-specific route.

# Public inputs and scientific boundaries

Use `data/inputs/bulk_si_li_system.json`. It uniquely defines the 3x3x3 conventional diamond-Si supercell, lattice, Si fractional positions, Li identity, two adjacent tetrahedral endpoint coordinates, atom mapping, periodic boundary condition, and charge states 0 and -1. The object is dilute bulk interstitial migration only: no surfaces, explicit dopant, electrolyte, SEI, amorphous phase, or finite-temperature free energy. The measured barrier is the maximum relaxed-path energy minus the lower relaxed endpoint energy for each state, in eV. Electronic-state claims require an explicit computed observable.

# Required scientific validation/investigation

Choose and justify a computational route. Generate a finite documented set of continuous candidate paths/images, deduplicate them by endpoint mapping and path geometry, and advance candidates to validated saddles or maxima. Demonstrate endpoint relaxation, path continuity, saddle character or bounded failure, convergence and at least one sensitivity/check. Report candidate coverage and a stopping rule based on stabilization of the selected path/barrier or an explicit resource/technical limitation. Completion requires validated barriers for both charge states and an evidence-based conclusion, or a truthful bounded-failure report with completed work and limitations; do not infer a charge-state effect from an incomplete comparison.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include the independent hypothesis/explanation, method and software, charge/multiplicity, candidate-path identities and validation, per-state barriers when obtained, an explicit charge-state comparison object with difference and direction (or unresolved status), an electronic-assessment object naming the computed observable or why it was unavailable, stopping rationale, artifact references, and limitations. If either state cannot be validated, use the failed state branch with a null barrier and report completed work and cause; do not fabricate energies.
