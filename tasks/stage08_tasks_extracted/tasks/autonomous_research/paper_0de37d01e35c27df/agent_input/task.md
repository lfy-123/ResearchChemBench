# Scientific objective

Determine computationally how one-electron oxidation changes the transannular sulfur–sulfur separation in conformationally constrained norDTCO, and what that structural change does and does not establish about an odd-electron S–S interaction. Obtain and validate neutral norDTCO and norDTCO+• structures without relying on a supplied paper route or target answer.

# Public inputs and scientific boundaries

The research object is norDTCO (C12H18S2; 3,7-dithiatricyclo[6.4.0.0^2,10.0^9,11]dodecane). `data/inputs/norDTCO_neutral.xyz` is a 26-atom Cartesian starting geometry in Å; XYZ row order is the immutable 1-based atom index. `data/inputs/system_definition.json` fixes neutral charge/multiplicity (0/1), radical-cation charge/multiplicity (+1/2), and sulfur atoms 16 and 17. Use an isolated-molecule boundary unless a justified extension is reported. Measure straight-line Cartesian S16–S17 distances and the signed radical-cation-minus-neutral change. Solvent, potentials, dication states and external literature are outside the required measurement boundary.

# Required scientific validation/investigation

Design and execute a reproducible calculation for both states. Verify atom count, elements, charge, multiplicity and sulfur identity. Generate and, if useful, compare additional conformer or spin candidates; deduplicate equivalents, report candidate-generation scope and coverage, and select a validated converged minimum. Validate each selected structure with stationary-point/convergence diagnostics and report imaginary modes, spin diagnostics and material caveats. Completion requires both validated structures and a reproducible comparison. Stop after validated coverage is sufficient to make the conclusion stable, and state why the coverage supports stability or what limitation remains.

# Deliverables

Submit `report/results.json` and referenced files under `report/`. Provide state and structure identities, distances in Å, signed change, validation evidence, candidate coverage, limitations and a route-neutral conclusion about structural evidence for an odd-electron S–S interaction.
