# Scientific objective

Determine the buffer-node insertion free energies ΔG_Buf (kcal mol−1) for H3BO3 and Tris binding to the defined Ce6-MOF-808 truncated node in its oxidized and singly reduced states, and calculate ΔΔG_Buf = ΔG_Buf,reduced − ΔG_Buf,oxidized for each buffer. The reproduction tests the authors' qualitative hypothesis that buffer coordination differs across oxidation states and can contribute to direction-dependent PCET kinetics; independently plan calculations that test this hypothesis.

# Public inputs and scientific boundaries

Use `data/inputs/bare_node.xyz`, `boric_acid.smi`, `tris.smi`, and `problem_definition.json`. The node identity is Ce6(H2O)6(OH)6(μ3-OH)4(μ3-O)4(HCO2)6; the oxidized state is the supplied neutral singlet model and the reduced state adds one proton and one electron, with doublet spin and protonation at a terminal OH. For each buffer, define insertion as replacement of one terminal aqua ligand, explicitly identify the site, preserve atom identity and charge/multiplicity, and state the thermochemical cycle and standard-state convention. Do not use paper/SI values as inputs.

# Required scientific validation/investigation

Generate exactly one reproducible calculation record for each of four systems (H3BO3/oxidized, H3BO3/reduced, Tris/oxidized, Tris/reduced), with any additional site or conformer trials listed and deduplicated by connectivity plus geometry. Optimize each bound system and the separated species using a defensible electronic-structure method; compute the requested free-energy cycle. Validate every accepted bound minimum with a frequency result (zero imaginary modes or clearly documented alternative), and validate each reduced state by reporting spin population/localization and the assigned protonation. Advance only systems with converged optimization and consistent atom/charge bookkeeping. Completion requires all four systems or a scientifically bounded failure report; stop when this condition is met or when repeated documented attempts fail, and report coverage and limitations.

# Deliverables

Write `report/results.json` containing `status`, `method_summary`, `systems` (one object per named system with `system_id`, `buffer`, `oxidation_state`, `site`, `charge`, `multiplicity`, `delta_g_buf_kcal_mol`, `frequency_validation`, `spin_validation`, and `artifacts`), `delta_delta_g_kcal_mol` (boric_acid and tris when available), `coverage`, `limitations`, and `conclusion`. Include enough paths and numerical details to reproduce every reported value. If bounded failure is reported, retain the same system identities and provide truthful null values plus diagnostics.
