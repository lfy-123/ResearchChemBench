# Scientific objective

For isolated gas-phase CHClF2, independently determine the adiabatic first ionization energy and the appearance energies and chemically valid minimum-energy dissociation paths for CHF2+ + neutral Cl and CHFCl+ + neutral F. Use the computed results to explain, within the defined scope, what structural/path features control the difference between the two channels. Do not rely on or report any presumed author mechanism.

# Public inputs and scientific boundaries

The system is CHClF2 with connectivity FC(F)Cl and one H on C, atom order C,H,Cl,F1,F2, supplied in `data/inputs/system.json` and XYZ starter files. Use neutral charge 0/multiplicity 1 and monocation charge +1/multiplicity 2. The fixed endpoints are CHF2+ + Cl(2P) and CHFCl+ + F(2P), separated until interaction is negligible; total charge and electron count must be conserved. The energy zero is optimized neutral CHClF2 electronic energy. Select and disclose methods independently; paper software/model chemistry and route are not public assumptions. Dication chemistry is outside scope.

# Required scientific validation/investigation

Optimize both parent charge states and validate stationary points. Compute AIE. Before selecting a path treatment, formulate at least two plausible path representations across the two fixed channels (for example, alternative reaction coordinates or a one-coordinate versus multidimensional treatment), state what evidence would discriminate them, and compare them using calculated continuity, endpoint and energy evidence. Generate and retain enough distinct path images or relaxed-coordinate points to determine whether a simple cleavage coordinate is adequate or coupled motion is needed; deduplicate equivalent endpoints and report the actual path coverage. Validate fragment identities, charge/spin assignments, electron-count conservation, endpoint separation, continuity and energy convergence separately for each channel. Perform one method/basis sensitivity check. Completion requires validated endpoints and paths plus all three requested energies, methods, uncertainties and a defensible mechanistic conclusion. Stop when those conditions are satisfied; if a channel remains unresolved after two documented alternative path constructions, use the bounded-failure branch and report the attempted coverage and limitation rather than inventing a result.

# Deliverables

Submit `report/results.json` with completion status, methods, state energies, AIE, per-channel path candidates and validation context, dissociation and appearance energies, sensitivity analysis, and a final scoped conclusion. Include geometry/path artifacts cited by the JSON. A bounded failure must identify the unresolved channel, all attempted candidates and evidence; a status string without these fields is incomplete.
