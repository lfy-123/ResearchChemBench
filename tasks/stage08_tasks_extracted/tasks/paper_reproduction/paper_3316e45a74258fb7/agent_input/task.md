# Scientific objective

Independently determine and interpret the low-lying electronic states of neutral TD-2T: a validated S0 structure, S1 and T1 energies, ΔE_ST = E(S1)−E(T1), and oscillator strength when available. Infer state character and mechanistic implications from your own calculations and diagnostics without assuming any paper-specific route or mechanism.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that donor–acceptor separation in this D–A–D emitter can support charge-transfer or hybridized local-and-charge-transfer (CT/HLCT) character, with a small singlet–triplet separation relevant to thermally activated delayed fluorescence and reverse intersystem crossing (TADF/RISC).

**Candidate route or mechanism.**
Examine whether the lowest singlet and triplet excitations involve different degrees of donor–acceptor charge transfer and local excitation, including possible mixing between these characters, as a candidate explanation for the relevant state ordering and transition behavior.

**Discriminating evidence.**
Use excited-state energies and the singlet–triplet gap together with oscillator strength and NTO, orbital, or related density-based diagnostics that distinguish local excitation from donor–acceptor charge transfer and assess state character. Compare the evidence across the identified S1 and T1 states when the chosen method supports such a comparison.

# Public inputs and scientific boundaries

Use only `data/inputs/td_2t_identity.json`: TD-2T, C72H49N7, charge 0, singlet ground state, with DCTP substituted at positions 3, 6 and 11 by three para-N,N-diphenylamino phenyl groups. Model one isolated gas-phase molecule; exclude solvent, host, aggregate, device, counterions and protonated forms. S0 is the optimized ground state; S1 and T1 are the lowest computed singlet and triplet excited states. Report energies and ΔE_ST in eV and oscillator strength dimensionless, with structure and output provenance.

# Required scientific validation/investigation

Choose and justify a reproducible route. Generate and document at least one valid 3-D conformer; deduplicate any alternatives by a stated criterion. Optimize S0 and provide convergence/stationarity evidence, or report a bounded failure with the last valid geometry and reason. Compute and identify S1/T1 on a validated structure, state the open-shell treatment, calculate the gap, and validate units and state assignment. Use NTO/orbital or another defensible diagnostic for state character, formulate interpretation from evidence, and state limitations. Completion requires valid geometry (or explained bounded failure), attempted requested states, provenance for every observable, and limitations. If an excited-state calculation or the gap cannot be validly completed, submit the bounded-failure schema branch with attempted-state evidence and an explicit reason; do not invent energies or a gap. Stop after documented conformer coverage and one validated state calculation; explain any additional search and why it stopped.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, including structure provenance, validation evidence, energies, gap calculation, oscillator-strength status, state-character evidence, conclusion and limitations. Bounded failure is allowed only with its reason and partial provenance.
