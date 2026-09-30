# Scientific objective

Determine, from independent computation on the supplied neutral and monoanionic ortho-phenyl-phosphonate-borane models, how formation of the anion changes the P–O and intramolecular O(P)···B distances, and whether the resulting structural changes are consistent with the experimentally reported neutral-to-lithium-salt crystallographic boundary. Develop and test any structural explanation yourself.

# Public inputs and scientific boundaries

Use `data/inputs/neutral.xyz` (C10H16BO3P, charge 0, singlet) and `data/inputs/anion.xyz` (C9H13BO3P, charge −1, singlet), with the SI atom order. P is atom 11; O1/O2/O3 are atoms 12/13/14; B is atom 21 in neutral and atom 18 in anion. Measure P–O1, P–O2, P–O3 and O1···B in Å. The models are isolated gas-phase species without Li+, solvent, crystal packing or bulky experimental substituents. The external boundary is only the paper's reported crystallographic neutral/salt distance change, used as an experimental comparison rather than a hidden target structure.

# Required scientific validation/investigation

Independently select a computational approach and, if applicable, generate a finite documented set of starting conformers for each state. Define deduplication and advancement rules, retain state and atom identity, and validate every reported structure by converged optimization plus a no-imaginary-frequency test or a justified equivalent. Report coverage, failed candidates and the basis for selecting the final structure. The investigation is complete when each state has a validated result or a bounded failure report, all requested distances and differences are available for successful states, and a structural interpretation is supported by the computed observables. Stop when the documented conformer-generation rule is exhausted and validation has been performed on every advanced candidate; report a limitation if that stopping condition cannot be reached.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include candidate/coverage information, method provenance, per-state validation, named distances, differences, independently reasoned interpretation, comparison with the experimental boundary, and limitations. Use the failure branch honestly if either state cannot be validated.
