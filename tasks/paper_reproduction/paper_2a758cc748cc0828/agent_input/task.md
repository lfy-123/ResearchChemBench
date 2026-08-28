# Scientific objective

Independently test the authors' proposed radical carbonylation/aminocarbonylation route for the explicitly supplied cyclohexyl system. Calculate relative Gibbs free energies (kcal/mol) for CO capture, iodine transfer, amine attack, and product formation, and compare activation barriers and tetrahedral-intermediate stability for aniline, N-ethylaniline, N-methylaniline, and morpholine. The author hypothesis to test is a radical chain in which an alkyl radical adds CO, iodine-atom transfer regenerates the radical, and catalyst-organized intramolecular nucleophilic attack on acyl iodide leads to amide.

# Public inputs and scientific boundaries

`data/inputs/molecular_system.json` gives unique SMILES, charge, multiplicity, and role for cyclohexyl radical, CO, iodocyclohexane, morpholine, aniline, N-methylaniline, and N-ethylaniline. Generate all geometries independently, including the cyclohexanecarbonyl-iodide intermediate derived from the proposed sequence; its result-bearing structure is not supplied. The radical pathway is evaluated on a neutral doublet surface; amine attack is evaluated on a neutral singlet surface. Use an acetonitrile continuum or justify another solvent treatment, and state temperature and standard-state conventions. Do not use the paper, SI, general web, or hidden reference values.

# Required scientific validation/investigation

Build and deduplicate at least one chemically connected conformer/approach for each requested state. Optimize every reported minimum and transition structure, perform frequencies, and retain atom connectivity. A minimum must have zero imaginary frequencies; a transition structure must have exactly one and its mode must correspond to the bond-making/bond-breaking event. For each pathway report the reactant reference, ΔG‡ and ΔG, with identity retained per candidate/state. Validate the radical sequence and all four amine channels independently, report failed or ambiguous searches honestly, and explain conformer coverage. The direct calculation is complete when every requested state has either a validated stationary point and free energy or a bounded, evidence-based failure explanation; stop after the stated candidate set has been searched and additional starting geometries no longer produce a distinct validated stationary point.

# Deliverables

Submit `report/results.json` conforming to the schema. Include methods, state identities, frequency counts, connectivity/imaginary-mode validation, numerical energies in kcal/mol, uncertainty/limitations, and a conclusion testing the author hypothesis. A bounded failure branch is allowed only when the corresponding validation evidence and attempted search coverage are reported.
