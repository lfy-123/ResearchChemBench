# Scientific objective

Using the supplied geometries of exo precursor iso-1 and endo precursor iso-2 plus fluoride, determine whether fluoride-promoted conversion can form an anti-Bredt bridgehead alkene and explain the difference between the isomers. The authors proposed fluoride capture at silicon followed by elimination involving C1–OTf and C2–Si; independently test this qualitative proposal. Determine defensible pathways, stationary points, activation free energies and Eyring rates where feasible. In the author SI atom order, C1 is carbon index 2 (1-based; bonded to the OTf oxygen) and C2 is carbon index 12 (1-based; bonded to the TMS silicon) for both isomers. OTf is the O–S(=O)2–CF3 group attached to C1; TMS is Si(CH3)3 attached to C2.

# Public inputs and scientific boundaries

`data/inputs/iso-1.xyz` and `iso-2.xyz` are 38-atom Cartesian geometries in Å transcribed from the authors' SI Section 11; file atom order is authoritative. `fluoride.xyz` is a one-atom F− reagent (charge −1, multiplicity 1); combine it with each precursor without changing precursor connectivity. The scope is gas-phase fluoride-promoted elimination; solvent, counterions, trapping agents and alternative substrates are out of scope. You may generate conformers, complexes, interpolated structures and TS guesses. Choose and report software and model chemistry. Report energies/barriers in kcal mol−1 with a stated reference, and rates with units and temperature. This task input is the public structure definition; all source-based identity changes are recorded in the verification report.

# Required scientific validation/investigation

Generate and deduplicate a finite set of fluoride-approach, siliconate-complex, sequential-elimination and coupled-elimination candidates for each isomer. Advance a candidate only when connectivity and charge are interpretable. Optimize advanced minima and TS candidates; verify minima/TS character by Hessian or a justified equivalent, and verify endpoint connectivity by IRC, NEB, constrained scans plus endpoint checks, or an explicit alternative. Compare coupled and sequential orderings when formable. Report failed searches and candidate identities. Completion requires either a connected validated path for each isomer with barriers/rates for feasible steps, or a bounded-failure report naming missing stationary points, attempts and evidence for stopping. Stop after all proposed candidate families have been tested with no unvalidated lower candidate in the stated scope, or when resources prevent this; report coverage and limitation.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include conclusion, path identities, energies/barriers, rates or explicit nulls with reasons, validation evidence, method/units and search coverage. A bounded-failure branch is acceptable only with attempted-search evidence.
