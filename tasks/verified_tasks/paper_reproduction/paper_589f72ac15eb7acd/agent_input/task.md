# Scientific objective

Independently plan and perform calculations testing the authors' qualitative hypothesis that changing the two cis pseudohalide co-ligands in neutral octahedral Fe(II) complexes `[Fe(LPh-TDA)(NCE)2]` changes isolated-molecule spin-state energetics in a ligand-field series. Determine the electronic isolated-molecule spin-transition energy for the three named complexes C1 (E=S), C2 (E=Se), and C3 (E=BH3), using the paper-defined convention `E_el^iso = E_HS − E_LS` and reporting kJ mol−1. The measured object is the optimized isolated complex, not a crystal, solvate, free energy, or transition temperature.

# Author-provided scientific guidance

The authors propose that a stronger-field auxiliary ligand should favor LS relative to HS across this series; independently test that qualitative hypothesis and do not assume its numerical outcome.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json` as the complete identity specification. It defines LPh-TDA connectivity, Fe(II), neutral charge, octahedral cis coordination, the N-bound NCS−/NCSe−/NCBH3− ligands, and HS multiplicity 5 versus LS multiplicity 1. You may generate 3-D conformers and computational inputs, but may not use the paper, SI, their coordinate files, or general web searches. Your calculations may use any defensible electronic-structure method and software available to you; state all choices. Compare only like-for-like states within each method.

# Required scientific validation/investigation

For each of C1–C3, generate and retain at least one chemically valid HS and LS structure with named donor/atom mapping. Use a finite, explicitly reported set of starting conformers and state-initialization strategies; deduplicate converged structures by a stated structural criterion. Advance only structures that converge with the intended multiplicity and chemically intact connectivity. For every system and spin state, report the attempted candidate identities, dispositions and rejection reasons. Validate every selected state separately by optimization diagnostics, a stationary-point/frequency check when feasible (or a state-specific bounded-failure explanation), spin contamination or spin-density diagnostics, intact-connectivity evidence, and an energy-unit/sign audit. The investigation is complete when every complex has a selected HS and LS state and a gap, or when the declared search budget is exhausted and every unresolved state is represented truthfully in the bounded-failure branch. Retain per-system/per-state coverage and do not substitute an unvalidated structure. Additional scientifically motivated searches are allowed. For a complete result, include a quantitative comparison among C1–C3 and explain whether the qualitative author hypothesis is supported within your method and computed evidence. For bounded failure, state which comparisons remain possible and do not assert an ordering unsupported by the validated subset.

Generic limitations or uncertainty prose is optional and unscored. Keep the required scientific identities, computed evidence, coverage and actual failure diagnostics. Additional scientifically motivated calculations are allowed and should be separated from the primary results; optional work not performed needs no disclaimer.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must contain the system/state identities, selected structures or structure references, energies and gaps where available, validation evidence, coverage/stopping record, method details, and a conclusion. Numeric values must be your calculated values, never copied reference values.
