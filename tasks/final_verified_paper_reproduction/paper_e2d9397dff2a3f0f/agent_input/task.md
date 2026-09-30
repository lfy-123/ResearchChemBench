# Scientific objective

Independently calculate the Gibbs free-energy barrier for the singlet N–O cleavage event in the cationic Ru-bda-Py ammonia-oxidation model. The reactant/reference state is the supplied `reference.xyz` structure (the SI’s 1(5bda) cationic stationary point) and the transition-state candidate must be generated and validated independently; no TS coordinate is public. `data/inputs/state_definition.json` is authoritative for charge +1 and singlet multiplicity for the reference and the independently generated TS candidate. Report the barrier in kcal/mol, the stationary-point classifications, the imaginary-frequency count and the vibrational mode assignment. For this reproduction mode, the authors’ qualitative hypothesis is that catalyst-organized N–O cleavage is the kinetically controlling event before NH3 attack; compute the specified local event without assuming its numerical outcome; comparison with the entire catalytic cycle is not a required result.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret catalyst-organized N–O cleavage in the bda model as the kinetically controlling event before ammonia attack.

**Candidate route or mechanism.**
The proposed event is cleavage of the N–O interaction in the singlet bda intermediate, proceeding through the independently generated singlet candidate saddle, before a subsequent NH3 attack step. Treat this as the candidate explanation to test with the reference and independently generated candidate.

**Discriminating evidence.**
Use stationary-point optimization and harmonic frequencies to distinguish a minimum from a first-order saddle, and inspect the imaginary-mode displacements and N–O bond metrics for cleavage character. Assemble the Gibbs barrier from the optimized structures, thermal terms, solvent treatment, and any stated electrochemical reference convention.

# Public inputs and scientific boundaries

The public input is `data/inputs/reference.xyz`, an explicit 48-atom XYZ reference geometry with element identities and coordinates. Generate the TS candidate independently; no TS coordinate is public. Treat both structures as the charge +1 singlet cation specified in `state_definition.json`. The chemical system is Ru-bda-Py, where bda is 2,2′-bipyridine-6,6′-dicarboxylate and Py is pyridine. The medium is acetonitrile; use 298.15 K and report how any electrochemical reference treatment at 0.5 V vs Fc+/0 and pH 15.1 is handled. Do not use the paper, SI, general web, or unpinned structures. The scored endpoint is the free-energy difference between the optimized independently generated TS and optimized reference under the submitted protocol; no product identity or catalyst ranking is requested.

# Required scientific validation/investigation

Choose and document a defensible computational method, optimize the supplied reference and the independently generated TS candidate, and perform frequency analyses. Establish that `reference` is a minimum and that the candidate is a first-order saddle with exactly one imaginary frequency. Identify whether the imaginary displacement is consistent with N–O cleavage by naming the atoms or bonds examined and providing distances/displacement evidence. Refine energies or thermal terms as appropriate for the stated solvent and temperature, define the exact barrier equation, and report convergence information. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result. The reference XYZ is a supplied reactant-side starter, not the author's optimized endpoint; do not copy an author/SI TS coordinate.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the chosen method, charge/multiplicity, structure statuses, frequency evidence, barrier, units, equation. If a calculation fails, use the failure branch and provide the attempted inputs, diagnostic evidence and the observed failure; do not fabricate a number.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
