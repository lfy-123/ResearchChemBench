# Scientific objective

Determine the free-energy barrier for reductive elimination of H2 from the uniquely specified neutral singlet palladium dihydride complex INT-G in `data/inputs/int_g.xyz`, and assess whether the computed terminal step is compatible with catalytic turnover. Do not use or seek the paper authors' route. Independently investigate the fixed terminal H2-release step from the supplied structure.

# Public inputs and scientific boundaries

The only molecular input is `data/inputs/int_g.xyz`: 73 atoms, Cartesian coordinates in Angstrom, neutral charge (0), singlet multiplicity (1), and the identity INT-G as the Pd complex containing two terminal hydrides. The measured quantity is the activation free energy ΔG‡ for the channel INT-G → H2 + the corresponding Pd(0) complex, in kcal/mol. You may generate endpoint structures and conformers, but do not treat an unconnected or chemically different channel as the requested endpoint. Do not use the paper, SI or general web.

# Required scientific validation/investigation

Plan and execute an independent computational investigation. Optimize or otherwise validate the INT-G minimum and report charge, multiplicity, method, dispersion, solvent model, thermal/free-energy convention and software. Locate a transition state for loss of H2; establish its stationary-point character and provide an IRC, mode-following, relaxed scan, or a chemically justified equivalent showing connection to the INT-G-side and H2/Pd(0)-side endpoints. Report all distinct starting conformers or TS attempts that materially affect the conclusion and deduplicate them by connectivity and geometry. The calculation is complete when at least one defensible connected TS is characterized, or when a bounded, documented search has failed; in the latter case submit the failure branch with attempted structures and evidence. Stop after the connected TS is validated and additional independent searches no longer change the preferred barrier by more than the uncertainty you report, or after a documented resource/search boundary is reached.

# Deliverables

Submit `report/results.json` containing the required schema fields. Set `status` to `success` only when the connected TS and barrier are defensible; otherwise set it to `bounded_failure` and populate the dedicated failure report without fabricating success-only values. In either branch, enumerate material conformer/TS attempts, state the completion basis and stopping criterion. Include a concise narrative conclusion, numerical barrier if obtained, stationary-point diagnostics, endpoint/connection evidence, method details, uncertainty and limitations. A bounded failure is valid only when the failure reason, attempted search and available diagnostics are populated.
