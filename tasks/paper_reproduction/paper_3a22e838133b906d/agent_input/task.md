## Scientific objective

Test the authors' qualitative hypothesis that a neutral and a monoanionic ortho-phenyl-phosphonate-borane model retain an intramolecular O(P)···B interaction and that dealkylation/anion formation changes the P–O and O(P)···B distances in the same qualitative direction as the corresponding crystallographic structures. Independently choose and document calculations; do not assume the authors' numerical results.

## Public inputs and scientific boundaries

Use `data/inputs/neutral.xyz` (C10H16BO3P, charge 0, singlet) and `data/inputs/anion.xyz` (C9H13BO3P, charge −1, singlet), with the SI atom order. In each file, P is atom 11, O1/O2/O3 are atoms 12/13/14, and B is atom 21 (neutral) or 18 (anion). Measure P–O1, P–O2, P–O3 and O1···B in Å. These are isolated gas-phase models: omit Li+, solvent, crystal packing and experimental bulky substituents. The experimental comparison observations are provided in `data/inputs/experimental_crystal_boundary.json` for 2a and [Li(MeCN)2][3]. Use them as an external structural boundary, state any atom-label mapping, and do not treat them as a quantitative crystal prediction or computed target.

## Required scientific validation/investigation

Generate at least one optimized structure for each supplied state using a documented electronic-structure method, charge and multiplicity. If multiple starting conformers are tested, deduplicate by connectivity and report the selection rule. A result is validated only when the optimization is converged and a frequency (or an explicitly justified equivalent stationary-point test) shows no imaginary frequencies; report failures rather than silently substituting unvalidated structures. Extract distances by the named atom identities, preserving state identity. The investigation is complete when both states have a validated or explicitly bounded-failure result, all four distances per successful state and state-to-state differences are reported, and the qualitative comparison and limitations are stated. Stop after validation of the documented conformer set and no additional distinct low-energy structure is found under the stated generation rule; if resources prevent this, report coverage and limitation.

## Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, containing method provenance, per-state validation, distances, differences, comparison, and limitations. Include enough provenance to reproduce the actual calculations and identify atom mapping. A bounded failure branch is allowed when a state cannot be validated, but it must identify the failed state and evidence.
