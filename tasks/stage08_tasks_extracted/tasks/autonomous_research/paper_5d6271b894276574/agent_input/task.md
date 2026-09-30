# Scientific objective

Determine, by independent computation, how the seven named anions alter the isolated association strength of 7-azaindole relative to the AI2 dimer. Construct and validate AI2 and one AI–anion complex for each of [NF2]−, [NTf2]−, [NNf2]−, [OTf]−, [BF4]−, [DCA]− and Br−, and report counterpoise-corrected interaction energies ΔE_int = E_complex − E_AI − E_anion in kcal mol−1. Identify and discriminate plausible structural explanations from the computed evidence.

# Public inputs and scientific boundaries

`data/inputs/system.json` gives unique identities, SMILES, charge and singlet multiplicity for 7-azaindole and all seven anions, plus a starting AI geometry and the eight required complex IDs. `data/inputs/*.xyz` gives isolated starting geometries; `component_manifest.json` maps files to identities and SI tables. The physical boundary is isolated gas-phase clusters, and the observable is the counterpoise-corrected electronic interaction energy, not a solution free energy or experimental dimerization constant. The scored system is the isolated molecule or isolated cluster; do not add a host or solvent.

# Required scientific validation/investigation

Propose plausible interaction motifs before calculation, generate a finite and explicitly described candidate set for each required ID, deduplicate by connectivity and a stated geometry criterion, relax candidates, and retain all candidates advanced for energy evaluation. Validate identity, atom mapping, total charge and multiplicity; validate each retained structure as a stationary minimum or label an alternative validated state and limitation; and show fragment energies and counterpoise bookkeeping. Report candidate counts, coverage, failed jobs and the evidence used to discriminate explanations. Completion requires either one validated retained state and energy for every required ID or a truthful bounded-failure entry for each unresolved ID. Stop when all eight IDs meet that condition and the stated candidate-generation rules have been exhausted, or stop earlier only with an explicit compute/method limitation and unresolved IDs. Do not fabricate missing values.

# Deliverables

Submit `report/results.json` and any supporting files listed there. Include per-complex identity, selected structure reference, validation context, interaction energy and units when available, the proposed/discriminated explanation, coverage/stopping statement, method description and limitations. A bounded-failure branch is valid only when it records attempted coverage and the unresolved observable. Conform to the local `submission_schema.json`. Do not include paper text or evaluator files.
