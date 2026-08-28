## Scientific objective

Determine, for the specified Pd/CMD model of 1-methylcyclohexane-1-carboxylic acid, how L7, L9 and L12 affect methyl versus methylene β-C(sp3)–H activation. Independently plan and perform calculations testing the authors' qualitative hypothesis that ligand coordination can alter the site preference. Report ΔG‡ for both sites, methyl/methylene activation ratios, and the ligand trend. Use the source labels only to identify the three ligand structures; no source transition structure or answer is provided.

## Public inputs and scientific boundaries

`data/inputs/model_system.json` defines the acid, sites, temperature and reaction medium. `ligand_definitions.json` gives source-supported, answer-neutral connectivity descriptions for the three ligand identities. Reconstruct each ligand and every Pd complex with explicit atom mapping, charge and multiplicity; do not use paper optimized complexes or TS geometries. The measured objects are methyl and β-methylene CMD stationary points for each ligand. Do not claim a complete catalytic-cycle barrier or experimental yield from this task.

## Required scientific validation/investigation

For each ligand/site pair, generate and deduplicate a finite set of plausible complexes and TS guesses, optimize them, and advance only structures with a chemically coherent Pd–ligand–acid arrangement. Verify minima and TSs by frequencies; a claimed TS must have exactly one relevant imaginary mode and the mode must involve C–H cleavage/C–Pd formation. Validate connectivity by IRC in both directions, or report a reproducible alternative path test with its limitation. Select the lowest validated conformer under your stated model, report coverage and discarded candidates, and stop when additional independent guesses no longer produce a new validated lower stationary point or when resources force a bounded-failure report.

## Deliverables

Submit `report/results.json` conforming to the schema. Use one uniquely named object for each ligand/site pair (`object_id`, ligand and site), and include methods, atom mapping, charge/multiplicity, a per-object candidate ledger, frequency/IRC evidence, barriers in kcal/mol relative to the corresponding reactant complex, ratios and uncertainty. A bounded failure branch is allowed only if every attempted object has its candidate ledger, validation state and failure reason; do not fabricate missing numbers or structures.
