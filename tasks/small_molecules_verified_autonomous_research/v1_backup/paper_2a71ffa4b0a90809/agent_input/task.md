# Scientific question

Which molecular differences account for the principal contrasts in the product-yield profiles of catalysts A–E in the isoquinoline Mukaiyama–Mannich reaction? Provide a calculation-supported explanation covering the catalyst series and the uncatalyzed reaction.

# Inputs and scope

`data/inputs/system.json` contains molecular identities, amounts and mixing order. A and B are separately prepared axial isomers; their relative iodine arrangements are specified in addition to constitution-only SMILES. The reaction uses isoquinoline, 2,2,2-trichloroethyl chloroformate and the specified ketene silyl acetal in dry THF at 193.15 K with 0.5 mol% catalyst.

`data/inputs/observations.json` contains product yields at seven times, including the uncatalyzed reaction. Replicate uncertainties are not supplied. The required scope is the principal differences within this catalyst series.

# Required results

Provide quantitative molecular evidence, the supported explanation and unresolved findings. Calculated objects require defined identity, composition, charge and spin. Quantities require units, references, conditions and supporting validity evidence. For solution free energies, report the raw thermal and standard-state conventions and any conversion to the common 1 M convention separately.

# Submission

Submit `report/results.json` and `report/report.md` under `submission_schema.json` and `submission_guide.md`, with native calculation artifacts and reproducible analysis.
