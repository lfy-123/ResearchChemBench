# Scientific objective

Independently test the authors' qualitative hypothesis that hydrazinium dichloride (HDC) coordinates selectively with Sn(II)-iodide precursor species more strongly than with Pb(II)-iodide species, using binding energies for SnI2/PbI2 complexes with FAI, HDC, and HDC+DMSO. The author hypothesis is a proposed coordination explanation to test, not a supplied answer.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It gives formulas, charge, multiplicity, component SMILES, six named complex systems, the binding-energy convention, and the finite-molecular scope. Construct and document geometries yourself; no transition state, selected conformer, energy, ranking, or paper computational protocol is supplied. Keep the same component stoichiometry in complex and fragments. Report whether each optimized structure is a genuine local minimum under your method and state limitations. Literature/paper/SI access is not allowed during the investigation.

# Required scientific validation/investigation

Choose and justify an electronic-structure method suitable for charged heavy-element molecular complexes, including relativistic treatment, dispersion, basis/cutoff, charge and spin. Generate a finite, chemically justified set of distinct starting arrangements for every named complex, deduplicate converged structures by connectivity and geometry, and advance only candidates with converged SCF and geometry. Recheck the reported best candidate for each system with at least one independent starting geometry or stated sensitivity test. Compute isolated-component energies consistently and calculate all six binding energies. Completion requires either validated values for all six systems or a bounded-failure report identifying the exact systems and causes. Stop when the stated candidate-generation rules have been exhausted or when additional starts no longer yield a distinct minimum; report counts, deduplication and coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, system identities and atom mappings, candidate/search and convergence evidence, per-system energies and binding energies with units, cross-system comparisons, the conclusion about the HDC selectivity hypothesis, and limitations. Numeric precision must reflect method uncertainty; do not claim agreement solely from a single unvalidated geometry.
