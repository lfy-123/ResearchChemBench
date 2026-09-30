# Scientific objective

Test whether La/Tb/Lu conformer preferences are explained by metal replacement, structural relaxation or explicit coordination water within a controlled 4f-core molecular model.

# Author-provided scientific guidance

SI pp21–22 uses Gaussian16 omegaB97XD/def2-SVP on CHNO and Dolg large-core (46+4f^n electrons) ECP/(7s6p5d)/[5s4p3d] Ln basis. Gas geometries and frequencies are combined with SMD-water single points; GoodVibes uses Grimme low-frequency entropy with 100 cm^-1 cutoff, 298 K, 1 M complexes and 55.5 M water. Equations S1/S2/S3 distinguish water binding, anti-minus-syn and gas metal binding. Frozen-backbone and closed hydration-square tests are benchmark additions.

The matched controls and robustness checks below are benchmark-authored extensions. Reproducing an author assertion or old numerical endpoint alone does not complete this investigation.

# Public inputs and scientific boundaries

Use both complete La starting structures and replace only the metal for Tb/Lu. Preserve all 81 original atom IDs and ligand deprotonation (complex charge +1). For the one-water models append O82,H83,H84. Source 4f-core removes 46,54,60 electrons for La,Tb,Lu respectively, leaving 11 explicit neutral-atom electrons; all complex calculations use formal pseudo-singlet in this model. Do not describe Tb as physically spinless. Numerical La ECP46MWB, Tb ECP54MWB and Lu ECP60MWB plus their (7s6p5d)/[5s4p3d] Gaussian-format basis blocks are supplied in data/inputs with hashes and official provenance in ecp_basis_manifest.json. Their availability does not validate a molecular minimum or thermochemistry.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **For each metal and identical hydration n, delta_G=G(anti,n)-G(syn,n) at 298 K, 1 M complexes in aqueous SMD. G=E_solv+(G_gas-E_gas) with consistent source low-frequency treatment, no double-counted ZPE. Water-addition delta_G=G(LnL.H2O)-G(LnL)-G(H2O) with 55.5 M water standard state. Frozen metal replacements compare electronic within-metal conformer gaps, not equilibrium G.**.

This is a paper-reproduction task. Use the authorized author guidance to reproduce the baseline and test it with the same expanded controls. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Same-hydration three-metal conformer free energies** Use and verify the supplied exact ECP/basis files in the selected engine, then validate dry/hydrated syn/anti models for all metals and report matched thermochemistry with collapse evidence where appropriate.

2. **Frozen metal replacement and closed hydration squares** Calculate dry frozen La-skeleton metal replacements and matched water-addition cycles; separate relaxation and hydration contributions to within-metal preferences.

3. **Molecular ECP identity and low-frequency robustness** Audit ECP/basis electron counts and repeat the decisive low-frequency or solvation choice. Explain conformational trends only within the validated model.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Quantitative extraction/metal selectivity is outside scope without an independently closed metal hydration-exchange cycle; no full exchange cycle is mandatory here.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `conformer_hydration_matrix`: Same-hydration three-metal conformer free energies
- `replacement_and_cycles`: Frozen metal replacement and closed hydration squares
- `ecp_and_sensitivity`: Molecular ECP identity and low-frequency robustness
