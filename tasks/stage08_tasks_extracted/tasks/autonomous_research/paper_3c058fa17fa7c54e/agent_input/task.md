# Scientific objective

Calculate the lowest singlet (S1) and triplet (T1) excitation energies of An-σ-Ph and An-σ-DA and test 2T1>S1 and S1−T1>0.5 eV. Generate and test your own explanations from the calculations, then formulate the interpretation.

# Public inputs and scientific boundaries

Use `data/inputs/molecule_manifest.json`, which uniquely defines both neutral, charge-0, singlet-ground-state molecules. Generate 3D geometries while preserving connectivity and protonation. The scored system is the isolated molecule; do not add a host, solvent, aggregate, device or experiment. Define your energy convention and state extraction.

# Required scientific validation/investigation

For each named system optimize a geometry and identify S1 and T1. Record method, basis, software, roots, spin treatment, convergence and provenance. Validate unchanged identity, geometry convergence and stationary-point evidence (or document a bounded failure), and verify state assignments. For a successful system report both derived gaps and an explicit assessment of both inequalities; for a bounded failure, identify every missing observable and do not fabricate numbers. Investigate at least one sensitivity/uncertainty source and report coverage. Completion requires auditable evidence for both systems and all observables, or an exact bounded-failure diagnosis. Stop at that completion condition or after documenting the failed route and remaining limitation.

# Deliverables

Write `report/results.json` per `submission_schema.json`, with one entry per manifest system, geometry and validation provenance, S1/T1 energies and gaps, conclusion and limitations. Include auditable logs/calculation files if available. Bounded failure must remain truthful and identify missing observables.
