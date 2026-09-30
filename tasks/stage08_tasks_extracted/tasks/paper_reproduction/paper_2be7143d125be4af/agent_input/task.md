# Scientific objective

For the two explicitly defined neutral Azo-R molecules in `data/inputs/azo_targets.json`, independently determine how the para substituent changes alpha-nitrogen charge and homolytic azo N=N bond dissociation energy. Form and discriminate plausible electronic explanations from your calculations; generate and test your own explanations without assuming a route or ranking in advance.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the para substituent tunes the electronic character of the azo unit: an electron-withdrawing p-nitrophenyl substituent should make the alpha azo nitrogen more electrophilic and strengthen the azo N=N bond relative to the p-cyanophenyl analogue. This is a qualitative structure-property claim to examine through the two requested observables.

**Candidate route or mechanism.**
For the comparison, treat substituent-driven electron withdrawal and redistribution across the aryl-azo linkage as the candidate explanation, with the alpha-nitrogen charge serving as the local electronic indicator and homolytic N=N cleavage as the bond-strength comparison. The authors connect this electronic modulation to easier reductive azo cleavage, but the scored isolated-molecule task should test the charge and BDE relationship directly.

**Discriminating evidence.**
Use optimized isolated-molecule calculations and auditable charge analysis together with parent and neutral-fragment energies for the mapped azo bond. Compare both molecules under a consistent method, spin treatment, and BDE convention; convergence, conformer or method sensitivity, and agreement or disagreement between charge and BDE trends discriminate the proposed explanation.

# Public inputs and scientific boundaries

The JSON input is the complete molecular specification: canonical SMILES, neutral charge, singlet multiplicity, mapped azo atoms, alpha-nitrogen definition, and homolytic BDE definition. The scored system is the isolated molecule; do not add a host or solvent. Enzyme kinetics, solvent effects, and probe imaging are outside scope. Select and justify computational methods and conformers independently, and use the supplied public inputs as the molecular specification.

# Required scientific validation/investigation

Generate, deduplicate, and optimize at least one conformer for each named molecule. Preserve molecule IDs and atom mapping through all files. Show convergence and stationary-point or equivalent validation, identify the charge-partitioning method, and calculate each BDE from auditable parent and neutral-fragment energies with consistent spin states and units. Propose at least one explanation for the substituent difference and test it against both observables. Completion requires auditable results for both molecules or a bounded failure report naming the missing object and attempted remedies. Stop after both molecules pass validation, or after documenting why further in-scope attempts cannot close a molecule.

# Deliverables

Submit `report/results.json` and referenced supporting files. Keep one record for each input ID (Azo-pNO2 and Azo-pCN), in input order, and identify the mapped alpha atom explicitly; the array order is not a scientific ranking. Report structures, method choices, validation evidence, charge values, parent/fragment energies, BDEs, comparison, the tested explanation, uncertainty, and limitations. Conform the result to the local `submission_schema.json`; the schema permits a documented bounded failure for an identified molecule. Do not fabricate numerical values or structures or claim a conclusion unsupported by completed calculations.
