# Scientific objective

Use the public tetraethylammonium tetrachloroferrate ion pair in its sextet state and determine the charge-transfer composition of a clearly identified representative excited state. The requested measured quantities are the state index/selection rationale, excitation energy and oscillator strength, LMCT and MLCT percentages, the other IFCT channels if available, and a conclusion about whether the state is predominantly LMCT.

# Author-provided scientific guidance

Independently test the authors' proposal that photoexcitation of the Fe(III) chloride catalyst is dominated by ligand-to-metal charge transfer (LMCT). The authors' qualitative route is a hypothesis to test; do not assume their geometry, state ordering, or numerical result; the primary reproduction protocol below defines the quantitative comparison.

# Public inputs and scientific boundaries

The sole scientific input is `data/inputs/catalyst_system.json`: tetraethylammonium cation `CC[N+](CC)(CC)CC` (charge +1) paired with an FeCl4 anion (Fe bonded to four Cl atoms, charge −1; Fe(III) notation), total charge 0 and spin multiplicity 6. The object is the isolated ion pair, not solvent molecules or the reaction substrates. Generate a reproducible starting geometry and any conformers yourself. The scored endpoint is an excited-state IFCT decomposition; a transition-state or reaction free-energy search is outside scope.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure workflow. Optimize or otherwise justify the ground-state geometry, verify charge and multiplicity, and report convergence and stationary-point/frequency evidence where applicable. Compute enough low-lying excited states to justify the state selected for charge-transfer analysis; retain a per-state record for the examined range, including state identity, excitation energy, wavelength, and oscillator strength. Perform hole/electron and fragment-resolved charge-transfer analysis with explicit fragment definitions and settings. Report LMCT, MLCT, and any remaining channels, with units and normalization. Repeat a material sensitivity check (for example a second conformer, functional/basis choice, or fragment partition) or explain why it is not feasible. A completed outcome requires a traceable calculation record, justified representative state, and quantitative IFCT result. If that endpoint cannot be reached, submit the bounded-failure outcome with attempted-state and validation context and a technically specific failure reason; do not invent successful-state values.

Use an implicit acetonitrile environment; excluding solvent molecules means no explicit solvent, not gas phase. Examine the low-lying sextet excited-state manifold, report at least the three largest oscillator strengths, and select the largest-f physical state in that manifold for the primary analysis. Resolve near degeneracy/state mixing with reported physical character and coverage, never by closeness to a charge-transfer target or by a fixed software state number. The common primary IFCT convention is a Mulliken-like transition-density decomposition into three disjoint fragments: all four Cl ligands, Fe, and the complete TEA+ cation. LMCT means Cl -> Fe and MLCT Fe -> Cl. Normalize over all fragment-to-fragment channels (including local channels); report the full matrix/normalization in supporting analysis. Other partitions/population schemes are sensitivity only.

Primary author-route protocol: B3LYP-D3(BJ), SDD basis/ECP for Fe and 6-31G(d) for other atoms, SMD(MeCN) optimization/frequencies; M06-D3, Fe SDD and other-atom 6-311+G(d,p), implicit MeCN for 30 sextet TD states. Use the highest-f selection rule above, not an author state index. Disclose the solvent-response implementation and equivalent software settings.

Retain and explain signed fragment contributions and any numerical normalization residuals produced by the declared population scheme; do not normalize LMCT and MLCT alone to 100%.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus any supporting files referenced by it (input decks, coordinates, logs, and analysis tables). The JSON must preserve candidate/state identity and validation evidence. State explicitly whether the calculation completed, give the selected state and results when available, and include a concise scientific conclusion. Do not quote or seek the private paper/SI during the investigation.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
