## Scientific objective

Determine, by independent computational investigation, the temperature-dependent kinetics and channel selectivity of the gas-phase reaction between acetyl-peroxy radical CH3C(O)O2 and HO2 at 1 atm. Test the author hypothesis that carbonyl-peroxy/HO2 chemistry provides an acid-forming cool-flame channel: independently plan calculations for the singlet and triplet surfaces, identify and validate stationary points and product channels, and assess the 520 K acetic-acid kinetic-model observable.

## Public inputs and scientific boundaries

Use `data/inputs/reactants.json` as the authoritative identity, mapping, charge, multiplicity, pressure and temperature input. The research object is the CH3C(O)O2 + HO2 reaction, not the whole combustion model. Track the three explicitly named product-channel identities in that file and report atom balance, spin assignment and whether each channel is barriered or barrierless. You may generate conformers and computational models, but do not use the paper, SI or general web for answer recovery.

## Required scientific validation/investigation

Generate a finite, identity-preserving set of conformers/complexes and stationary-point candidates for both surfaces; deduplicate by connectivity and symmetry/geometry criteria that you state. Advance only candidates with documented optimization and frequency evidence; validate minima by zero imaginary frequencies and transition states by one imaginary frequency plus an intended reaction-mode check, or report a justified alternative. Compute/estimate channel rates and branching at the listed temperatures and state the method, pressure treatment and uncertainty. Completion requires either a converged validated pathway/rate model covering every named channel and temperature or a bounded-failure report naming the unresolved candidates and coverage. Stop when all generated candidates are classified and additional searches no longer produce a distinct low-energy channel under your stated generation rule; report the stopping rule and limitations.

## Deliverables

Submit `report/results.json` conforming to the schema. Include per-candidate identity and validation context, rate/branching tables with units, the 520 K acetic-acid mole-fraction test, evidence paths, conclusion, coverage and limitations. A bounded failure is acceptable only if all required fields in the failure branch are populated.
