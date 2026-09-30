# Scientific objective

Using the supplied neutral singlet substrate 1a and one equivalent of the supplied phosphoric-acid catalyst, investigate the first intramolecular Friedel–Crafts cyclization that can lead to the two regioisomeric benzofuran channels. Here “ortho/4-hydroxybenzofuran” means C–C bond formation at the aromatic carbon adjacent to the substrate’s phenoxy oxygen (the channel whose cyclized product retains the phenolic OH at benzofuran C4); “para/6-hydroxybenzofuran” means bond formation at the para aromatic carbon (the channel whose product retains that OH at C6). The authors qualitatively propose that catalyst organization can favor the ortho channel by activating both the ketone and phenolic OH; independently test this proposal. Determine the validated relative Gibbs barriers for the two channels, their difference in kcal/mol, and whether the computed ordering supports the observed regioselective reaction boundary.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that organization by the phosphoric-acid catalyst, with simultaneous activation of the ketone and phenolic OH, favors the ortho/4-hydroxybenzofuran cyclization channel over the para/6-hydroxybenzofuran channel.

**Candidate route or mechanism.**
Compare the two first intramolecular Friedel–Crafts cyclization transition-state pathways from a common catalyst-bound precursor: one forms the aromatic C–C bond adjacent to the phenoxy oxygen and retains the phenolic OH at benzofuran C4, while the competing pathway forms that bond at the para aromatic carbon and retains the OH at C6. In the proposed favored arrangement, the catalyst can organize and hydrogen-bond to both the ketone and phenolic OH; the competing arrangement may activate the ketone without the same dual interaction.

**Discriminating evidence.**
Use optimized stationary points, harmonic-frequency classification, and IRC connectivity to validate the two transition structures and their common precursor. Compare their Gibbs free-energy barriers under a common thermochemical convention, including the catalyst–substrate organization and hydrogen-bonding geometry, and use the signed barrier difference to test the proposed regioselective ordering.

# Public inputs and scientific boundaries

`data/inputs/system.json` is the complete chemical identity input: it gives explicit SMILES, charge, multiplicity and 1:1 association for 1a and bis(4-nitrophenyl) phosphate. Build 3-D structures and any catalyst-bound conformers yourself. The physical boundary is the neutral singlet 1:1 complex in a toluene-like continuum at 298.15 K and the first C–C-forming cyclization event; later dehydration, product isolation and bulk concentration effects are outside the scored endpoint. The measured quantities are stationary-point classification, IRC connectivity, relative Gibbs barriers from a common catalyst-bound precursor, and the barrier difference between the two regiochannels. Do not use the paper, SI or general web as an input source.

# Required scientific validation/investigation

Generate and deduplicate a defensible set of catalyst-bound conformers and transition-state guesses for both regiochannels, retaining the atom mapping and structural identity of every candidate. Advance candidates only when optimization produces a stationary point for the specified cyclization event. Validate each reported minimum by a frequency calculation and each reported transition structure by exactly one relevant imaginary mode plus an IRC (or a scientifically equivalent path-following validation) connecting it to the intended precursor and post-cyclization minimum. Compare both channels to the same reference state and report the thermochemical convention, solvent treatment, temperature and model chemistry actually used. Completion requires either (a) at least one validated candidate for each channel and a barrier comparison, or (b) a bounded-failure report stating which channel could not be validated, what candidate/conformer coverage was attempted, and why the conclusion is limited. Stop when additional searches no longer produce a distinct validated candidate under the stated generation/deduplication rule, or when computational resources are exhausted; report the stopping basis and unresolved alternatives.

# Deliverables

Submit `report/results.json` and any referenced coordinate, frequency, IRC and energy files. The JSON must identify each candidate and channel, give structure identity, validation status, separate frequency and IRC evidence, state the common reference, report the two barriers when available, report the signed barrier difference when both are available, and include a conclusion about support for the qualitative hypothesis plus limitations. If either channel cannot be validated, use the bounded-failure branch: document every attempted candidate ID, the failed channel(s), coverage and validation failures, set barrier availability to not_available with a reason, and do not fabricate a numerical barrier or ordering.
