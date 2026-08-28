# Scientific objective

Independently calculate the low-lying states of neutral TD-2T and determine an optimized S0 structure, S1 and T1 energies, ΔE_ST = E(S1)−E(T1), and oscillator strength when available. Test the authors' qualitative hypothesis that donor–acceptor separation in this D–A–D emitter can support CT/HLCT character and TADF/RISC. The hypothesis is qualitative only; no target result or author protocol is supplied.

# Public inputs and scientific boundaries

Use only `data/inputs/td_2t_identity.json`: TD-2T, C72H49N7, charge 0, singlet ground state, with DCTP substituted at positions 3, 6 and 11 by three para-N,N-diphenylamino phenyl groups. Model one isolated gas-phase molecule; exclude solvent, host, aggregate, device, counterions and protonated forms. S0 is the optimized ground state; S1 and T1 are the lowest computed singlet and triplet excited states. Report energies and ΔE_ST in eV and oscillator strength dimensionless, with structure and output provenance.

# Required scientific validation/investigation

Generate and document at least one valid 3-D conformer; deduplicate any alternatives by a stated criterion. Optimize S0 and provide convergence/stationarity evidence, or report a bounded failure with the last valid geometry and reason. Compute and identify S1/T1 on a validated structure, state the open-shell treatment, calculate the gap, and validate units and state assignment. Use NTO/orbital or another defensible diagnostic for state character, separating evidence from interpretation. Completion requires valid geometry (or explained bounded failure), attempted requested states, provenance for every observable, and limitations. If an excited-state calculation or the gap cannot be validly completed, submit the bounded-failure schema branch with attempted-state evidence and an explicit reason; do not invent energies or a gap. Stop after documented conformer coverage and one validated state calculation; explain any additional search and why it stopped.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, including structure provenance, validation evidence, energies, gap calculation, oscillator-strength status, state-character evidence, conclusion and limitations. Bounded failure is allowed only with its reason and partial provenance.
