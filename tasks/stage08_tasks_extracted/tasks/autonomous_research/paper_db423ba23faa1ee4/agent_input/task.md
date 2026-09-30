# Scientific objective

For the supplied neutral singlet IPrCuOMe/ortho-quinol-imine reactant complex and supplied 1,4-addition product endpoint, independently determine whether a validated computational pathway exists and quantify its activation free energy. Draw a mechanistic conclusion only from the calculations performed within this fixed system boundary.

# Public inputs and scientific boundaries

`data/inputs/reactant.xyz` and `product.xyz` are 107-atom Cartesian structures in Å, with XYZ row order defining atom identity within each file. `system_definition.json` fixes charge 0 and multiplicity 1 and identifies the IPr-ligated Cu–OCH3 fragment, ortho-quinol-imine substrate, and 1,4-addition endpoint. You may generate conformers and TS guesses. Report all software, model chemistry, solvent treatment, thermochemical convention, and any alternative conformers actually used; these are not prescribed. The measured quantities are validated stationary-point free energies and the activation free energy from the reactant complex to a validated addition TS, in kcal/mol. Do not use the paper, SI, or general web.

# Required scientific validation/investigation

Generate and deduplicate a finite set of chemically distinct TS hypotheses for bond formation at the 1,4-addition site, retaining for every candidate its geometry, starting guess, and identity. Optimize candidates and advance only those with a chemically sensible reaction mode, one imaginary frequency associated with the addition coordinate, and a reproducible connection to the supplied reactant and product endpoints by IRC or an explicitly justified equivalent path test. Validate both endpoint minima with frequency analysis (no imaginary frequencies) and use the same stated free-energy convention for all compared states. Completion requires at least one validated TS or a documented bounded failure after all attempted candidate classes and computational limitations are reported. Stop when additional candidate classes are not producing new connectivity hypotheses or when resources prevent further validation; state coverage and the stopping reason.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include the selected candidate identity, all attempted candidates and validation context, the activation free energy and reaction free energy when successful, or a truthful bounded-failure branch, plus a final conclusion about what the computation establishes and its limitations. Include paths to logs/geometries and enough method details to reproduce the reported values.
