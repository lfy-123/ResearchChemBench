# Scientific objective

Establish, by an independent periodic computational investigation, the relaxed structure and chemical bonding of high-pressure Cd3(C3N6), and determine whether the evidence supports a chemically meaningful Cd-N contribution associated with non-planar/distorted melaminate geometry. Formulate and discriminate plausible explanations for any distortion from calculations and validation evidence.

# Public inputs and scientific boundaries

Use only `data/inputs/cd3c3n6_experimental_47p7GPa.cif` and `data/inputs/structure_manifest.json`. They define neutral periodic Cd3(C3N6), R3c (No. 161), hexagonal cell a=b=11.5351 Å, c=5.188 Å, angles 90°,90°,120°, Z=6, pressure 47.7 GPa, and labelled Cd1, C1, N1 and N2 18b asymmetric-unit sites. Reconstruct the full cell with standard R3c symmetry and preserve composition, charge and site labels. Measure C-N distances and a distortion descriptor for the anion, characterize Cd-N bonding with a stated bond-order or equivalent electronic descriptor, and compare at least two plausible explanations using discriminating calculations or sensitivity evidence. The result is an independently supported conclusion.

# Required scientific validation/investigation

Choose and document model chemistry, numerical settings, pressure/cell treatment, charge and spin treatment, and protocol. Relax the structure and verify convergence, composition and crystallographic identity. Define finite candidate explanations before testing them, deduplicate equivalent explanations, and advance only those for which the proposed observable and discriminating test are explicit. Report C-N classes by explicit labels or a reproducible selector, validate Cd-N contacts individually, and define the distortion metric in coordinates. The investigation is complete when one converged primary calculation, at least one discriminating sensitivity/validation check, explicit object mappings, and an uncertainty/limitation assessment support or fail to support a conclusion. Stop when those conditions are met; if a required stage fails, submit a bounded failure report with attempted remedies and the evidence needed to resume.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For a complete outcome include hypotheses considered, route and settings, convergence and identity checks, explicit structure/bond mappings, measured observables, discriminating validation, limitations, and a final conclusion. If a required stage cannot be completed, use the bounded-failure branch and report the failed stage, attempted remedies, and evidence needed to resume; do not fabricate success-only observables. Do not use the paper, SI or general web as an execution substitute.
