# Scientific objective

For the public two-atom diamond-Ge cell, independently determine whether a defensible electronic-structure model can jointly describe the zero-pressure equilibrium lattice constant a, Γ–Γ and Γ–L fundamental gaps, and cubic elastic constants B0, C11, C12 and C44. The research object is bulk ground-state Ge. Propose and discriminate plausible model explanations for any disagreement among structural, electronic and elastic observables, without importing a paper-specific route or result.

# Public inputs and scientific boundaries

Use `data/inputs/germanium_diamond.json`. It uniquely fixes elemental Ge, diamond Fd-3m symmetry, two fractional coordinates, neutral charge, singlet/nonmagnetic state and three-dimensional periodicity. Use a nonrelativistic PAW Ge pseudopotential including 3d electrons and identify its exact file/provenance. Equivalent cell representations are allowed if composition and connectivity are preserved. No author route, winning model, target value or result is supplied. Report a in Å, gaps in eV and elastic constants in GPa; define Γ and L and the experimental temperature convention used for comparison. No defects, surfaces, finite-temperature free energies or phonons are required.

# Required scientific validation/investigation

Select and justify a computational model, then execute an independent calculation. Show relaxation/energy-volume or equation-of-state convergence for the zero-pressure minimum; test numerical sensitivity that could affect the reported observables; identify valence and conduction band edges and direct versus indirect gaps; and derive all four cubic elastic constants from documented independent strains/stresses or energy response with fit diagnostics. If multiple plausible models are investigated, retain model identity and validation context for each and explain the discrimination rule. Completion requires every observable to have a value or a scientifically justified bounded-failure status, uncertainty and provenance, plus a conclusion about model adequacy. Stop when the chosen model is converged to its stated uncertainty and alternatives have been reasonably discriminated, or document the specific implementation/resource limitation and report partial coverage without fabricated values.

# Deliverables

Submit `report/results.json` and supporting files listed in the schema. Include candidate/model identities, method and pseudopotential provenance, convergence and validation evidence, all observables or bounded-failure branches, comparison to experimental boundary data, independent conclusion, and limitations. Do not claim discovery beyond the computed scope.
