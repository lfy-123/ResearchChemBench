# Scientific objective

Test, by independent periodic electronic-structure calculations, how Pt, Pd, Au and Ag supports and one- versus two-layer epitaxial CoO films affect the energy and activation barrier for CO + surface lattice oxygen → CO2 + an oxygen vacancy. In reproduction mode, the authors' qualitative hypothesis is that oxide–metal charge transfer and resulting Co–O polarization are relevant; independently test that hypothesis without assuming a result.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`, `data/inputs/co.xyz`, and `data/inputs/co2.xyz`. The system is stoichiometric CoO on fcc(111) noble-metal slabs in a 2×2 cell, six support layers, 3.15 Å in-plane spacing, and the defined vacancy reaction. Select a surface-O site using a reproducible structural criterion and identify it unambiguously in every submitted structure; the public inputs do not prescribe a result-bearing site or geometry. Report total/reaction energies, activation barriers where a validated transition state is found, and Bader transfer for the outermost CoO layer. Do not claim experimental rates or extrapolate beyond these supports/thicknesses.

# Required scientific validation/investigation

Define a reproducible primary model and document all settings, magnetic initialization, constraints, slab/vacuum treatment and gas references. Relax each primary structure to stated SCF/force criteria; verify the reactant and vacancy/product endpoints preserve stoichiometry and the submitted site identity; validate any transition state by an appropriate connectivity/curvature or pathway check. Deduplicate symmetry-equivalent candidates, retain candidate identities and validation status, and state which support/thickness cases were actually completed. A completed case must report converged endpoints, its reaction energy and charge transfer, and either a validated barrier or an explicit no-validated-barrier record. A bounded-failure case must instead record the attempted case, failed stage and evidence, with unavailable observables represented as null. Completion requires every declared primary case to satisfy one of these truthful branches. Stop when that condition is met or when resources prevent further cases; report coverage and limitations rather than silently substituting values.

# Deliverables

Write `report/results.json` following the schema. Include model settings, per-case structures/identities, energies and units, charge-transfer values and sign convention, validation evidence, candidate failures, coverage, conclusion and limitations. A bounded-failure branch is acceptable when accompanied by the attempted case and evidence.
