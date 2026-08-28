# Scientific objective

Test the authors' qualitative proposal that anion-dependent AI association is governed by hydrogen-bond/electrostatic organization of an AI–anion cluster. Independently construct the AI2 dimer and one AI–anion complex for each of [NF2]−, [NTf2]−, [NNf2]−, [OTf]−, [BF4]−, [DCA]− and Br−, and calculate counterpoise-corrected interaction energies. The measured quantity is ΔE_int = E_complex − E_AI − E_anion with Boys–Bernardi fragment bookkeeping, reported in kcal mol−1. This is an isolated gas-phase cluster problem, not an ionic-liquid free-energy calculation.

# Public inputs and scientific boundaries

`data/inputs/system.json` gives unique identities, SMILES, charge and singlet multiplicity for 7-azaindole and all seven anions, plus a starting AI geometry and the eight required complex IDs. `data/inputs/*.xyz` gives source-supported isolated starting geometries for AI and each anion; the manifest identifies each file and SI table. No optimized complex, selected complex conformer, reference energy or ranking is public. You may generate 3-D conformers and choose computational methods, but must state them. The physical boundary is isolated gas-phase AI2/AI–anion clusters; do not use a bulk-solvent model as the reported observable. The authors' hypothesis is only a qualitative route suggestion; it does not specify a winning geometry or energy.

# Required scientific validation/investigation

For each required complex ID, generate a finite, explicitly described set of chemically distinct starting arrangements/conformers, deduplicate by connectivity and a stated geometry criterion, optimize or otherwise relax candidates, and retain the candidates advanced for energy evaluation. Validate component identity, atom mapping, total charge and multiplicity; validate each retained structure as a stationary minimum or clearly label an alternative validated state and limitation; and show fragment energies and counterpoise treatment. Report candidate counts, deduplication, failed jobs, retained structures, and coverage. Completion requires either one validated retained state with an interaction energy for every required ID or a truthful bounded-failure entry for each unresolved ID. Stop when all eight IDs meet that condition and no unreported candidate class remains within the stated generation rules; if compute or method limits prevent this, stop and report the limitation and unresolved IDs rather than inventing values.

# Deliverables

Submit `report/results.json` and any supporting files listed there. The JSON must include per-complex identity, selected structure reference, validation context, interaction energy and units when available, plus a coverage/stopping statement, method description, comparison of anion complexes with AI2, and limitations. A bounded-failure branch is allowed and must identify the missing observable and attempted coverage. Do not copy source documents or evaluator files into the report.
