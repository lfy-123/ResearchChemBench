# Submission conventions

The JSON Schema is the exact field contract. This guide explains the scientific meaning.

- `methods.primary` states software/version, functional, basis/ECP, solvent and numerical settings. `methods.sensitivity` identifies actual alternative protocols. Use `method_key` to associate every record with the correct named protocol; explain additional names in the report.
- A `calculation_record` identifies an actual engine result with a unique ID, job ID, log path, molecular identity, state and environment. `energies.electronic_Eh` is the electronic energy. `thermal_G_correction_Eh`, if given, is **G minus electronic E**, including ZPE: therefore G = E + thermal_G_correction, not E + ZPE + thermal_G_correction. Record ZPE separately for audit. Cross points have no invented equilibrium G.
- A single engine job can support several quantities; reference the same record. Separately launched jobs have distinct IDs even if they converge to the same geometry. Deduplicate physical minima, not the history of attempted jobs. If no tool job ID exists, record the actual execution identifier and log location.
- Arrays of `evidence_files` point to actual workspace files in `outputs/`, `data/` or `code/`. They are provenance, not declarations of correctness. Every cited record, geometry, normal-mode or NTO file must exist and correspond to the reported method. JSON validity alone does not verify this.
- All angles are degrees, geometry distances angstrom, electronic energies hartree; panel names specify other units. State comparisons use **right minus left** for energy and oscillator-strength deltas; report the state-matching metric and its definition. Character metrics must give normalization and fragment definitions. Quantitative character is needed for every state used in an inference; the full root window still includes energy/f for dark and unused roots.
- `hypotheses` records distinguishable propositions, an observation that tests each, actual supporting/contradicting records and the resulting assessment. A hypothesis statement without a calculation is not evidence.
- `sensitivity` compares actual baseline and alternative quantities: `change = alternative_value - baseline_value`. Reusing primary results without a changed, justified factor is not a sensitivity test.
- A `bounded_failure` may omit uncomputed panels, hypotheses and sensitivity results; provide actual attempt records, available partial results, failure evidence and missing endpoints. Failed records may omit energy and geometry rather than fabricate them. No numerical minimum or endpoint is implied by format acceptance.

# Required result panels

## `conformers`

Two starting families × dispersion on/off, validated basins and 300 K harmonic G.

## `energy_decomposition`

Diagonal and reciprocal cross-geometry electronic-energy matrix.

## `transitions`

Root windows and matched NTO/fragment states at representative geometries.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
