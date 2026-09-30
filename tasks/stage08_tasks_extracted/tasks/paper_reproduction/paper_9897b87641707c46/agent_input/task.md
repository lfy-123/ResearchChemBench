# Scientific objective

Determine whether a computational free-energy profile for styrene hydroboration by HBpin on the public truncated bipyridyl–Fe(II) dihydride model supports the proposed regioselective mechanism. Quantify the relative Gibbs free energies (kcal/mol) of styrene coordination, both possible alkene-insertion branches, and the subsequent HBpin sigma-bond-metathesis transition states. Identify which branch leads to the linear versus branched boronate connectivity and which elementary step has the largest turnover-relevant activation free energy. The authors propose a catalyst-organized intramolecular insertion/metathesis cycle; independently test that qualitative route.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the reaction as a catalyst-organized cycle in which the truncated bipyridyl–Fe(II) dihydride undergoes ligand dissociation, styrene coordination, alkene insertion into an Fe–H bond, and reaction with HBpin. They associate the 1,2 insertion connectivity with the linear, anti-Markovnikov boronate and the 2,1 connectivity with the branched, Markovnikov boronate.

**Candidate route or mechanism.**
Search a dissociative resting-state-to-reactive-catalyst route followed by styrene coordination and the two regioisomeric Fe–H insertion branches. Continue each insertion product through its corresponding HBpin sigma-bond-metathesis event, retaining object identity so the linear and branched pathways can be compared on the same model.

**Discriminating evidence.**
Use a consistent 333.15 K free-energy profile to compare coordination, both insertion transition states and products, and both metathesis transition states. Validate minima by frequencies and transition states by one reaction-coordinate imaginary mode plus a connection check, then use the resulting barriers and branch-resolved connectivity to assess the proposed regioselectivity and rate-controlling event.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It defines styrene (C8H8, `C=Cc1ccccc1`), HBpin (C6H13BO2, `CC1(C)OB(O1)`), and a neutral truncated molecular catalyst consisting of unsubstituted 2,2'-bipyridine bound through both nitrogens to Fe(II), two hydrides, and two axial THF ligands in the resting state. Use a quintet electronic state for Fe-containing species unless a documented state comparison motivates a different state; report all deviations. The framework is omitted. Use implicit toluene at 333.15 K and state the standard-state convention used for relative Gibbs energies. No paper/SI coordinates, result structures, reference values, or literature search are required or permitted.

# Required scientific validation/investigation

Generate and document independent 3D conformers for the resting catalyst, dissociated reactive catalyst, styrene-bound complex, both insertion products, both insertion transition states, and both HBpin metathesis transition states. Define each candidate by retained atom mapping/connectivity and a stable label. Deduplicate conformers or explain why apparently duplicate candidates remain distinct. Optimize every advanced minimum and transition-state candidate with a defensible electronic-structure method; calculate frequencies and thermochemical corrections consistently at 333.15 K; and report the reaction-coordinate interpretation of every imaginary mode. A minimum is validated only with no imaginary frequencies and chemically continuous connectivity; a TS is validated only with one imaginary frequency whose eigenvector and an IRC, relaxed scan, or equivalent connection check support the claimed elementary event. Report method, basis, dispersion, solvation, spin, convergence status and failed attempts.

Completion requires either (a) a connected, frequency-validated profile containing both insertion branches and both metathesis branches, or (b) a bounded-failure report identifying the missing species/connection, all attempted candidates, and why further work under the stated model is not justified. Stop when both branches have been searched with at least one validated candidate at each required event and additional independent starting conformers no longer produce a distinct validated pathway, or when the computational/model limitation prevents that condition; in the latter case report coverage and the limitation explicitly. Do not claim selectivity from a single unvalidated TS.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include a profile array with object identity, branch, state, relative free energy, activation free energy where applicable, validation evidence and method; a candidate-search/coverage record; and a conclusion that distinguishes computed model evidence from experimental selectivity. Include enough provenance to reproduce every reported number. If completion is bounded-failure, use the schema's failure branch and provide the attempted candidates, missing required event, and limitation instead of fabricated numerical values.
