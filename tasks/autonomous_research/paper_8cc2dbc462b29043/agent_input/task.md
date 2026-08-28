# Scientific objective

Using the supplied geometries of exo precursor iso-1 and endo precursor iso-2 plus fluoride, determine whether fluoride-promoted conversion can form an anti-Bredt bridgehead alkene and explain the difference between the isomers. Independently discover and discriminate plausible mechanisms, stationary points, activation free energies and Eyring rates where feasible. C1 and C2 are the first and second carbon atoms in each XYZ file. OTf is the O–S(=O)2–CF3 group attached to C1; TMS is Si(CH3)3 attached to C2.

# Public inputs and scientific boundaries

`data/inputs/iso-1.xyz` and `iso-2.xyz` are 35-atom Cartesian geometries in Å for neutral precursors; file atom order is authoritative. `fluoride.xyz` is a one-atom F− reagent (charge −1, multiplicity 1); combine it with each precursor without changing precursor connectivity. The scope is gas-phase fluoride-promoted elimination; solvent, counterions, trapping agents and alternative substrates are out of scope. You may generate conformers, complexes, interpolated structures and TS guesses. Choose and report software and model chemistry. Report energies/barriers in kcal mol−1 with a stated reference, and rates with units and temperature. Do not use the paper, SI, general web or hidden references.

# Required scientific validation/investigation

Formulate plausible mechanistic hypotheses before calculation and discriminate them through a finite, explicitly described search over fluoride approach, silicon coordination, bond-cleavage order and coupled cleavage. Deduplicate by connectivity and structural similarity. Advance candidates only when connectivity and charge are interpretable. Optimize advanced minima and TS candidates; verify stationary-point character by Hessian or justified equivalent, and endpoint connectivity by IRC, NEB, constrained scans plus endpoint checks, or an explicit alternative. Report rejected candidates, failed searches, identities, coverage and stopping rationale. Completion requires either a connected validated explanation for each isomer with barriers/rates for feasible steps, or a bounded-failure report naming missing stationary points, attempts and evidence for stopping. Stop after all proposed candidate families have been tested with no unvalidated lower candidate in the stated scope, or when resources prevent this; report coverage and limitation.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include hypotheses, selected/rejected paths, energies/barriers, rates or explicit nulls with reasons, validation evidence, method/units and search coverage. A bounded-failure branch is acceptable only with attempted-search evidence.
