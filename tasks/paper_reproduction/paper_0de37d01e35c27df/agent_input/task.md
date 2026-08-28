# Scientific objective

Test the authors' qualitative hypothesis that one-electron oxidation of conformationally constrained norDTCO can produce a sulfur–sulfur two-center/three-electron interaction. Independently optimize neutral norDTCO and norDTCO+• from the supplied geometry, measure the S16–S17 distance in each, calculate the signed change (radical cation minus neutral), and state whether the structural evidence supports that hypothesis within the stated boundary. Choose and justify your own computational route.

# Public inputs and scientific boundaries

The molecule is norDTCO (C12H18S2; 3,7-dithiatricyclo[6.4.0.0^2,10.0^9,11]dodecane). `data/inputs/norDTCO_neutral.xyz` is a 26-atom starting geometry in Å, with XYZ row order as the 1-based atom index. `data/inputs/system_definition.json` fixes neutral charge 0/multiplicity 1, radical-cation charge +1/multiplicity 2, and sulfur atoms 16 and 17. Treat it as isolated unless a justified extension is reported. Measure straight-line Cartesian S16–S17 distances and their signed difference. Do not score solvent, electrochemical potentials, dication chemistry or a particular software package.

# Required scientific validation/investigation

Generate at least one optimized candidate for each state, retaining exact state and atom identity. Verify atom count, elements, charge and multiplicity. Establish a stationary point or clearly converged minimum using frequencies, gradients/convergence data, or a justified alternative; report imaginary modes and unresolved convergence. If additional conformer or spin candidates are explored, deduplicate equivalents, state generation/advancement criteria and identify the validated selected candidate. Completion requires two validated state results and the comparison. Stop when validated coverage makes the distance-change conclusion stable, and document the limiting reason and coverage.

# Deliverables

Submit `report/results.json` plus referenced files under `report/`. Include state identities, selected structures, distances in Å, signed change, validation diagnostics, provenance (file and atom indices), coverage, limitations and a conclusion about support for the qualitative hypothesis.
