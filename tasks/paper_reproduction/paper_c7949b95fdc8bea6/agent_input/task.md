# Scientific objective

Determine, for the supplied periodic bulk crystalline-Si/Li interstitial system, the Li migration barrier in the neutral and one-excess-electron charge states and whether the charge-state change supports the authors' qualitative hypothesis that an electron-trapping state near the migration saddle facilitates Li motion. Independently choose and justify the computational method and path-search implementation; do not assume the paper's numerical result.

# Public inputs and scientific boundaries

Use `data/inputs/bulk_si_li_system.json`. It defines the 3x3x3 conventional diamond-Si supercell, lattice, all eight Si fractional positions in the conventional cell, Li identity and the initial/final fractional coordinates, endpoint atom mapping, periodic boundary condition, and charge states 0 and -1. The object is dilute bulk interstitial migration only: no surfaces, explicit Sb, electrolyte, SEI, amorphous phase, or finite-temperature free energy. The measured barrier is the maximum relaxed-path energy minus the lower relaxed endpoint energy, in eV, for each charge state. Electronic-state interpretation is optional only if supported by the chosen method.

# Required scientific validation/investigation

Relax both named endpoints while preserving composition and mapping. Generate a finite, documented set of continuous images between the two endpoints, deduplicate equivalent paths, and optimize/locate a saddle or defensible maximum-energy path for both charge states. Demonstrate endpoint convergence, path continuity, saddle character or a clearly reported bounded failure, and numerical convergence/sensitivity to at least one relevant setting. Report the number and identity of attempted paths/images and why the search stopped. Completion requires either converged barriers for both states with validation evidence, or a truthful bounded-failure report containing completed calculations, failure cause, and limitations; do not claim a charge-state effect from one state alone.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include method, software, charge/multiplicity, endpoint and path files or hashes, convergence evidence, per-state barriers when obtained, an explicit charge-state comparison object with difference and direction (or unresolved status), an electronic-assessment object naming the computed observable or why it was unavailable, and a conclusion tied to the supplied bulk model. Cite reproducibility artifacts and state all limitations. If either state cannot be validated, use the failed state branch with a null barrier and report the completed work and cause; do not fabricate energies.
