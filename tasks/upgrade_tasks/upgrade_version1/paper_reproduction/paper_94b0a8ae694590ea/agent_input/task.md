# Scientific objective

Determine whether isolated-molecule donor arguments survive explicit adsorption, charge-rearrangement and vacuum-referenced work-function comparisons on a common periodic SWCNT model.

# Author-provided scientific guidance

The source reports molecular DFT and thermoelectric composites, and invokes donor energetics to explain SWCNT doping. Main experimental section identifies XFS22 tubes (diameter 1–2 nm; length 5–30 micrometers) without a single chirality. SI molecular coordinate sections define the three molecules. Explicit periodic interfaces and vacuum/density controls are benchmark additions; the source does not provide an adsorption or transport reference.

The matched controls and robustness checks below are benchmark-authored extensions. Reproducing an author assertion or old numerical endpoint alone does not complete this investigation.

# Public inputs and scientific boundaries

Use complete source molecules including both octyl chains. The public ideal (10,10) armchair tube has 12 primitive repeats, 480 C atoms, periodic z and 18 angstrom transverse vacuum on each side. Source experimental tubes have unspecified chirality; this benchmark model is conditional and is not claimed to reconstruct the exact experimental distribution. Use one molecule per baseline cell, total neutral charge, with the same electronic/spin treatment and dispersion protocol across all interfaces.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **E_int=E(tube+molecule)-E(tube at interface geometry)-E(molecule at interface geometry); E_def=E(tube frozen)-E(tube relaxed)+E(molecule frozen)-E(molecule relaxed); E_ads=E_int+E_def. All in eV per molecule at identical numerical conditions. Work function W=V_vac-E_F; electron gain on the molecule is positive in the declared density partition.**.

This is a paper-reproduction task. Use the authorized author guidance to reproduce the baseline and test it with the same expanded controls. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Three full interfaces with frozen and relaxed references** Optimize the pristine tube, isolated molecules and two adsorption starts per molecule, then calculate same-geometry fragments, density differences and vacuum-referenced work functions.

2. **Length, coverage, vacuum and reciprocal-sampling controls** Compute the fixed-coverage size control for 2BF-TTA and paired k-grid/vacuum sensitivities before trusting the three-member ranking.

3. **Donation versus interfacial dipole and adsorption geometry** Compare molecular electron gain and work-function changes against adsorption/deformation, distinguish donation and dipole explanations, and state the model-conditional conclusion.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Absolute carrier transport, NEGF, thermoelectric PF, tube diameter series and dilution dependence are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `interface_matrix`: Three full interfaces with frozen and relaxed references
- `boundary_controls`: Length, coverage, vacuum and reciprocal-sampling controls
- `charge_mechanism`: Donation versus interfacial dipole and adsorption geometry
