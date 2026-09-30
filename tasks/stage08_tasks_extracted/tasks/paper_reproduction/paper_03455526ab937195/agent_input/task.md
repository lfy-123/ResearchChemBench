# Scientific objective

For the public 1f + ethynylbenzene system, discover and discriminate plausible photochemical reaction-path explanations and determine whether a validated computational network supports one cycloaddition channel over the other. Quantify channel-specific activation free energies from a clearly identified common reference when possible, using ΔΔG‡ = G‡([2+2]) − G‡([4+2]). The object is an independently investigated mechanism and its uncertainty, not a product-yield simulation.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that direct photoexcitation accesses a triplet reaction manifold and that chemoselectivity is controlled by competing ring-closure free-energy barriers in a stepwise cycloaddition.

**Candidate route or mechanism.**
Consider addition of the sulfonyl-substituted carbon-centered radical of triplet 1f to ethynylbenzene to form a common triplet intermediate. From this intermediate, the proposed alternatives are radical–radical coupling to close the [2+2] ring and radical addition to the substrate's phenyl ring to close the [4+2] ring, each through an open-shell-singlet transition state. The latter route includes subsequent aromatization with methanesulfinic acid loss.

**Discriminating evidence.**
The authors use excitation energies and spin–orbit coupling calculations to examine triplet accessibility, and solution-phase DFT free-energy profiles to compare the two closures from the common intermediate. Frequencies and IRC connectivity test stationary-point assignments; wavefunction stability, spin expectation values, spin densities, and frontier-orbital character probe the proposed open-shell states and reactive sites.

# Public inputs and scientific boundaries

Use the reactant identities and connectivity in `data/inputs/system.json`: neutral 3-(methylsulfonyl)-4-phenyl-1H-pyrrole-2,5-dione (maleimide_1f; explicit SMILES, formula, charge 0, singlet ground state) and neutral ethynylbenzene (ethynylbenzene_2a; explicit SMILES, formula, charge 0, singlet ground state), in acetonitrile at 298.15 K and overall charge 0, under a 400 nm visible-light boundary. The outcome classes to compare are net [4+2] naphthalene-fused-imide formation and net [2+2] four-membered-ring formation. Generate and test your own plausible spin/state and pathway hypotheses. Generate independent 3D conformers and computational models from the supplied connectivity. Report the method, solvation, standard state, temperature, and spin convention actually used.

# Required scientific validation/investigation

Define a finite hypothesis and candidate-generation strategy spanning any spin manifolds, intermediates, conformers, and transition states you consider plausible. Retain stable identities and provenance for every candidate; deduplicate by stated connectivity/geometric/energetic criteria; and report how candidates were advanced or rejected. Validate minima by frequencies, TSs by one intended imaginary mode plus IRC or equivalent endpoint/connectivity evidence, and open-shell states by spin contamination/stability diagnostics. Compare both outcome classes on a common thermochemical reference when possible, and perform an independent starting-geometry or method sensitivity check for each decisive channel when feasible. Completion requires either (a) validated comparable pathways for both outcome classes and a justified discrimination, or (b) a bounded-failure report naming the unresolved state and search/validation limitation. Stop when that condition is met and no unvalidated candidate is decisive; otherwise stop after the stated coverage is exhausted and report the limitation. Do not claim global mechanistic uniqueness.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must contain the candidate ledger, validation evidence, reference-state definition, channel barriers when obtained, signed ΔΔG‡ when both are obtained, the independently reasoned conclusion, method/sensitivity information, and limitations. A bounded-failure branch is allowed only if it identifies attempted coverage and missing validation. Include machine-readable artifact paths for logs, geometries, frequencies, IRCs, and spin diagnostics where available.
