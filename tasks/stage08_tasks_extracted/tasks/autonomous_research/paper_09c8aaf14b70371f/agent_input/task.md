# Scientific objective

Determine the neutral-singlet E↔Z torsional isomerization of unsubstituted chalcone 3, (2E)/(2Z)-1,3-diphenylprop-2-en-1-one. Find and validate the lowest defensible connecting transition state and quantify, separately in gas phase and implicit acetonitrile, its electronic barrier relative to the optimized E minimum and its specified torsional dihedral. Propose and discriminate plausible connecting explanations using calculations; generate and test your own explanations without assuming a particular mechanism.

# Public inputs and scientific boundaries

Use `data/inputs/chalcone3_system.json` as the complete system definition. It supplies mapped E and Z stereochemical SMILES, formula C15H12O, charge 0, multiplicity 1, and atom roles: carbonyl C=2, alpha C=4, beta C=5, beta-phenyl ipso C=6. The measured coordinate is the signed dihedral (2,4,5,6), in degrees. Treat `gas_phase` as an isolated molecule and `acetonitrile_pcm` as an isolated molecule in an implicit continuum acetonitrile model. Energies must be electronic relative energies in eV, with each environment's E minimum as zero. Alternative defensible model chemistry is allowed if fully documented.

# Required scientific validation/investigation

Define a finite, chemically justified candidate-generation strategy for endpoint conformers and connecting mechanisms, deduplicate candidates by connectivity and geometry, and report coverage. Compare plausible connecting candidates rather than asserting one explanation. For every advanced TS candidate, provide optimization convergence, a Hessian/frequency result, the number and character of imaginary modes, and a connection test (IRC, downhill displacement, or equivalent) to both validated E and Z basins. Select the lowest candidate only after comparing all retained candidates under the same environment/model. Completion requires a validated TS and both validated endpoints in both environments, or a bounded-failure report with all available fields and a concrete reason; stop when the stated candidate coverage and validation criteria are met or when candidate generation is exhausted.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include proposed explanations, candidate identities and per-candidate validation context, coverage/stopping rationale, method/software, per-environment endpoint energies/dihedrals, selected TS energy/dihedral, barrier relative to E, imaginary-frequency count, conclusion and limitations. Preserve atom-role identity in every structure and candidate record. Do not report a success status without the corresponding structures and validation fields.
