# Scientific objective

Determine the singlet–triplet exchange gap J (cm^-1) and the triplet population at 300 K (%) for the three explicitly identified neutral Cu2(AnCOO)4(4-RPy)2 molecular dimers (R = H, CH3, OCH3). Do not assume a paper numerical result.

# Author-provided scientific guidance

In this reproduction mode, the authors' qualitative hypothesis is that changing pyridine electronics changes Cu–Cu exchange; independently plan and perform calculations that test that hypothesis.

# Public inputs and scientific boundaries

Use J=ES−ET (negative for a lower singlet), in cm^-1. The triplet population at 300 K is 100×3 exp[J/(kBT)]/{1+3 exp[J/(kBT)]}; with J in cm^-1 use kB=0.69503476 cm^-1/K. The factor 3 is triplet spin degeneracy. For unambiguous scoring, the complete `systems` array contains exactly R_H, R_CH3, R_OCH3 in that order, once each. Put additional attempts separately. At least one methodological sensitivity check is required, not necessarily a new control for every derivative.

Use `data/inputs/model_systems.json`. It uniquely identifies each system, ligand SMILES, assembly, charge, reference triplet multiplicity, target states, and units. Construct 3-D geometries from the supplied connectivity. The boundary is the isolated dimer, not the periodic MOF or experiment. Report the sign convention used for J and define how the singlet–triplet energy difference maps to it.

# Required scientific validation/investigation

For each of the three named systems, generate and deduplicate at least one chemically valid geometry, optimize or otherwise establish a defensible triplet reference, and calculate the lowest singlet and triplet energies with a method capable of treating the open-shell dimer. Record convergence, spin/state identity, and any imaginary-frequency or stability check performed. Validate at least one methodological sensitivity (basis, functional, geometry, or equivalent justified check). Completion requires all three systems having a traceable gap and population; incomplete work uses a documented failure report with diagnostic evidence.

# Completion and allowed outcomes

Submit a successful result only when all three named systems have the requested gap and
population plus the required validation records. If a system or the sensitivity check cannot
be completed after the attempted scope, submit the bounded-failure branch with the covered
systems, attempted calculations, diagnostics, and the specific missing result; do not invent
numeric values or placeholder structures.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` containing per-system identity, geometry provenance, J, population at 300 K, units, method, validation records (including sign convention and population expression), coverage/status, and a conclusion. A bounded-failure branch is allowed when diagnostics and attempted scope are reported.
