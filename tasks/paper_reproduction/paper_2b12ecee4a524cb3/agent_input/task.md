# Scientific objective

Independently test the authors' qualitative proposal that oxygen insertion into the Fe–C bond occurs by migration from a high-valent iron–oxo intermediate, using the supplied neutral quintet stationary-point geometries. Determine the Gibbs free-energy barrier from minimum 7 to TS 7–8 and state whether the validated calculation supports the proposed oxo-insertion step within this model boundary. The measured quantity is ΔG‡ = G(TS) − G(7), in kcal/mol, at 298.15 K and 1 atm.

# Public inputs and scientific boundaries

`data/inputs/intermediate_7.xyz` and `data/inputs/ts_7_8.xyz` are the complete 85-atom Cartesian geometries of the neutral quintet reactant minimum and candidate transition structure, respectively; the first line is the atom count and the second is a comment. `data/inputs/system.json` fixes charge 0, multiplicity 5, temperature, pressure, atom identity and endpoint definition. You may generate conformers or restart geometries, but the scored endpoint calculation must identify which supplied geometry was used and preserve element identities. Do not use the paper, SI, general web or hidden reference values.

# Required scientific validation/investigation

Choose and disclose a defensible electronic-structure and thermochemistry protocol, including treatment of spin, solvent, dispersion and thermal corrections. Optimize or otherwise verify both supplied structures. Demonstrate that the minimum has zero imaginary frequencies and the transition structure has exactly one chemically relevant imaginary frequency; report the frequency values and units. Attempt IRC or an equivalently explicit connectivity test from the transition structure toward minimum 7 and product-side minimum 8, and report either successful connectivity or a bounded failure with evidence. Compute ΔG‡ with a clearly defined consistent energy assembly. Completion requires a converged calculation, the stated stationary-point checks, an explicit connectivity result or limitation, and an uncertainty/sensitivity discussion. Stop after these checks and at least one documented reasonable method-sensitivity test. If any required calculation or validation cannot be completed, submit the bounded-failure branch with the attempted method, convergence/provenance evidence, observations actually obtained, uncertainty and limitations, and a conclusion limited to what was established; do not invent a barrier or placeholder number.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method settings, convergence evidence, frequencies, connectivity evidence, energy components, the barrier if computable, uncertainty, limitations, and a concise mechanistic conclusion. Include enough provenance to reproduce every reported number.
