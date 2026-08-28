# Scientific objective

Independently calculate the Gibbs free-energy barrier for the singlet N–O cleavage event in the neutral Ru-bda-Py ammonia-oxidation model. The reactant/reference state is the supplied `reference.xyz` structure (the SI’s singlet bda stationary point) and the target transition-state starting structure is `target.xyz`. Report the barrier in kcal/mol, the stationary-point classifications, the imaginary-frequency count and the vibrational mode assignment. For this reproduction mode, the authors’ qualitative hypothesis is that catalyst-organized N–O cleavage is the kinetically controlling event before NH3 attack; test that hypothesis with your calculations without assuming its numerical outcome.

# Public inputs and scientific boundaries

Inputs are `data/inputs/reference.xyz` and `data/inputs/target.xyz`, each an explicit XYZ geometry with element identities and coordinates. Treat both as neutral singlet molecular systems. The chemical system is Ru-bda-Py, where bda is 2,2′-bipyridine-6,6′-dicarboxylate and Py is pyridine. The medium is acetonitrile; use 298.15 K and report how any electrochemical reference treatment at 0.5 V vs Fc+/0 and pH 15.1 is handled. Do not use the paper, SI, general web, or unpinned structures. The scored endpoint is the free-energy difference between the optimized TS and optimized `reference` reference under the submitted protocol; no product identity or catalyst ranking is requested.

# Required scientific validation/investigation

Choose and document a defensible computational method, optimize both supplied geometries, and perform frequency analyses. Establish that `reference` is a minimum and that `ts3_bda` is a first-order saddle with exactly one imaginary frequency. Identify whether the imaginary displacement is consistent with N–O cleavage by naming the atoms or bonds examined and providing distances/displacement evidence. Refine energies or thermal terms as appropriate for the stated solvent and temperature, define the exact barrier equation, and report convergence information. The calculation is complete when both structures have documented optimization/frequency outcomes and a reproducible barrier or a scientifically justified bounded failure with logs and limitations. Stop after these two fixed structures and the declared validation checks; do not search other pathways or conformers.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the chosen method, charge/multiplicity, structure statuses, frequency evidence, barrier, units, equation, and limitations. If a calculation fails, use the failure branch and provide the attempted inputs, diagnostic evidence and a concrete limitation; do not fabricate a number.
