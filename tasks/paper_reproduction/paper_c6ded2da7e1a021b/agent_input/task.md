# Scientific objective

Test the authors' qualitative proposal that the helical acridinium framework is configurationally stable by independently locating the helical-inversion transition state of the specified P-1a+ cation and computing the electronic activation barrier ΔE = E(TS) − E(minimum), in kcal mol−1. The candidate mechanism to test is intramolecular helical inversion of the fused-ring skeleton; do not assume the published numerical outcome.

# Public inputs and scientific boundaries

Use `data/inputs/p1a_plus.xyz`, a self-contained 61-atom Cartesian geometry for P-1a+ (C34H26N+, charge +1, singlet), and `data/inputs/system.json`. The system is an isolated gas-phase cation; no BF4−, solvent, crystal packing, or experimental rate is part of the target. You may generate conformers and TS guesses, but the scored state is the inversion TS connected to this helical minimum. Report electronic energies in hartree and the barrier in kcal mol−1. No paper, SI or general-web lookup is allowed.

# Required scientific validation/investigation

Optimize the supplied minimum and verify it is a stationary minimum with zero imaginary frequencies. Generate and investigate at least one chemically plausible inversion TS guess; accept a TS only when optimization converges, it has exactly one imaginary frequency, and the associated displacement is consistent with inversion of the helical fused-ring framework rather than a local peripheral motion. Establish connectivity to the supplied minimum (e.g. displacement along the imaginary mode or an appropriate path/endpoint check). Compute ΔE from the reported stationary-point electronic energies. Completion requires either a validated TS and barrier or a documented bounded failure after reporting all attempted guesses, convergence outcomes, frequency evidence, and the reason the endpoint could not be established. Stop after the validated connected TS is found, while reporting whether additional independent guesses were tried and what coverage they provide.

# Deliverables

Write `report/results.json` following `submission_schema.json`. Include method/software, minimum and TS energies, frequency evidence, TS connectivity evidence, barrier, conclusion about configurational stability, and limitations. If the bounded-failure branch is used, provide the required attempt log and limitation statement and do not fabricate a barrier.
