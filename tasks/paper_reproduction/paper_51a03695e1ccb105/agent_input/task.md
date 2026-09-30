# Scientific objective

Test the proposed base-assisted elementary coupling between the supplied iminotriazole anion and nitrosotriazole, with neutral 3,3′-azo-1,2,4-triazole as the target organic product. Independently plan and perform a defensible molecular electronic-structure investigation of the stationary points and report the coupling activation free energy and atom-balanced reaction free energy. The authors qualitatively proposed that base-assisted deprotonation enables this coupling; test that hypothesis without assuming a published numerical result.

# Public inputs and scientific boundaries

The public files are `data/inputs/iminotriazole_anion.xyz` (9 atoms, charge −1, multiplicity 1), `data/inputs/nitrosotriazole.xyz` (9 atoms, charge 0, multiplicity 1), and `data/inputs/azotriazole_ts2_si.xyz` (18 atoms, total charge −1, multiplicity 1). The last file is the Cartesian candidate reported as azotriazole transition state 2 in SI Table S17 (SI p. S26); it is an initial candidate, not a validated transition state or an answer-bearing energy, and must be independently optimized and characterized.

The target organic product is neutral 3,3′-azo-1,2,4-triazole: two 1,2,4-triazol-3-yl units joined by an N=N bond at their 3 positions. Atom and charge conservation fix the base-assisted endpoint as

`iminotriazole anion + nitrosotriazole -> neutral azotriazole + hydroxide anion`.

Thus the 18-atom reactant side and the product side (`C4H4N8 + OH−`) both have total charge −1. Hydroxide is a required coproduct/reference fragment, not an alternate target product. Do not compare energies of the 18-atom reactants with a 16-atom azo molecule alone, and do not silently change atom identity, total charge, multiplicity, or azo connectivity. The calculation boundary is this isolated, atom-balanced molecular reaction in a methanol-like solution model. The photocatalyst, oxygen, and the rest of the catalytic cycle are outside the scored endpoint. Choose and disclose your own electronic-structure method, solvent treatment, thermal convention, conformer handling, and energy reference.

# Required scientific validation/investigation

Optimize and characterize the supplied reactants, neutral azo product, and hydroxide coproduct; then optimize and characterize the supplied SI transition-state candidate and any additional chemically plausible candidate you generate. Retain candidate identity, geometry provenance, total charge/multiplicity, atom count, and computational settings. A minimum must have no imaginary frequency; a transition state must have one relevant N−N bond-forming/O−H-transfer imaginary mode and an intrinsic-reaction-coordinate calculation or an explicitly justified equivalent connection test to the stated reactant and atom-balanced product basins. Compute the activation free energy relative to the separated supplied reactants and the reaction free energy relative to separated neutral azo plus hydroxide, using one explicitly stated standard-state/solvation convention and reporting units. If no validated TS is found, submit a bounded-failure report listing attempted candidates, diagnostics, coverage, and the next limitation. Completion requires either a `validated` report with one validated TS and both energies or a `bounded_failure` report; do not fabricate energies when no TS is validated. Stop when the validated endpoint is converged under your stated geometry/TS search protocol or when additional searches no longer produce a new validated connection; report search coverage and limitations.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include method/settings, reactant/product/coproduct identities, stationary-point frequency diagnostics, TS connection evidence, activation and atom-balanced reaction free energies when available, and a concise mechanistic conclusion. You may attach supporting files under `report/`, but the JSON is the scored primary result.
