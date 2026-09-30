# Verified computation reference — paper_9a58a1fa6ed7d780 (paper_reproduction)

> Evaluator-private archive of successful calculations, not an additional scoring axis. Do not expose to the evaluated agent. Updated 2026-09-18 after user approval to adopt benchmark-computed S2–S4 Sr references.

## Current scope and decision

The original scientific scope is retained: six vertical singlet excitations and four states' hole–electron descriptors for neutral singlet BN-AkFlu. S1 energy/Sr rules and the final weak-S1/stronger-higher-energy absorption conclusion are unchanged. S2–S4 Sr now use actual benchmark verification results, not SI Table S11. This is an explicit reference-source decision, not proof that the SI descriptors have been reproduced.

The prior low-grid archive is superseded for current Sr reference purposes. The group report's newer CONDITIONAL/PENDING statement concerned SI numerical reproduction; no historical report status is changed here. Source equivalence remains unresolved. A version-dependent software effect is a hypothesis, not an established root cause.

- Paper: *Synthesis, Photophysical Properties, and Device Application of Internal BN-Fused Fluoranthenes*, DOI 10.1021/acs.orglett.5c04888.
- Source methods/coordinates/spectrum: SI S39, Table S21 (S49–S50), Table S14 (S42).
- Input: 40 atoms, C22H14B2N2, charge 0, multiplicity 1, isolated gas-phase molecule.
- Both public XYZ files exactly match SI Table S21. The reference properties below were calculated after S0 optimization, not on the unchanged supplied coordinates.
- The optimized geometry differs by aligned RMSD 0.0061867 Å, maximum atomic displacement 0.0089758 Å.
- Identity checks: `docs/claude/artifacts/9a58_root_cause_20260918/source_alignment.json`.

## Successful calculation chain

All paths beginning with `artifacts/` or `provenance/` below are relative to:
`docs/verification/group_1/paper_9a58a1fa6ed7d780`.
Historical source records are read-only and were not rewritten for this task revision.

### 1. S0 preparation and frequency validation

- Input: public/SI BN-AkFlu coordinates, neutral singlet.
- Native input: `artifacts/gaussian_batch/supp_bn_akflu_b3lyp_optfreq/input.com`.
- Actual Gaussian route: `#p B3LYP/6-311G(d,p) Opt Freq`.
- Run: `g16 < input.com`; normal completion, minimum with 114 real frequencies and zero imaginary frequencies.
- Geometry: `artifacts/gaussian_batch/supp_bn_akflu_b3lyp_optfreq/optimized_geometry.xyz`.
- Native output/status: `stdout.log`, `status.json` in that same directory.
- Correction to old prose: the input does NOT specify `Opt=(Tight,MaxCycles=200)`; that phrase in historical result summaries is a documentation error, not the actual route.

### 2. Six vertical singlet excitations on the optimized S0 geometry

- Input: `artifacts/gaussian_batch/supp_bn_akflu_td_b3lyp_optgeom/input.com`.
- Route: `#p TD(NStates=6) B3LYP/6-311G(d,p)`, full TDDFT, gas phase, neutral singlet, Gaussian spherical d functions.
- Run: `g16 < input.com`; normal completion.
- Native output: `stdout.log`, checkpoint and formatted checkpoint in the same directory.
- A separate earlier successful TD run on unchanged SI coordinates exists under `supp_bn_akflu_td_b3lyp`; it is NOT substituted for the optimized-geometry reference used here.

### 3. Recovery of excitation/de-excitation amplitudes

- Directory: `provenance/local_recovery_20260918/BN_AkFlu_TD6_fullcoeff_resume_20260918/`.
- Files: `input.com`, `gaussian.log`, `fullcoeff.chk`, `fullcoeff.fchk`, `status.json`.
- Route: `#p B3LYP/6-311G(d,p) TD=(Read,Singlets,NStates=6) Geom=AllCheck Guess=Read IOp(9/40=4)`.
- Reused the saved optimized-geometry TD checkpoint, printed amplitudes down to 1e-4, completed in 95.2533 s with one SCF cycle, no geometry optimization.
- “Complete coefficients” here means printed down to 1e-4, not mathematically all nonzero coefficients. Normalization residual in subsequent analysis is at most 6e-6.

Recovered spectrum:

| State | E/eV | Wavelength/nm | f |
|---|---:|---:|---:|
| S1 | 2.1401 | 579.34 | 0.0081 |
| S2 | 2.8502 | 435 | 0.0001 |
| S3 | 2.9876 | 414.99 | 0 |
| S4 | 3.401 | 364.55 | 0 |
| S5 | 3.6111 | 343.34 | 1.8535 |
| S6 | 3.7195 | 333.33 | 0 |

The maximum excitation-energy deviation from SI Table S14 is 0.0005 eV. Dominant signed forward amplitudes from this same recovered output (HOMO=MO85):

- S1: MO85 -> MO86: +0.70266; MO83 -> MO88: +0.07407; MO81 -> MO86: -0.02559; MO80 -> MO87: -0.01633.
- S2: MO84 -> MO86: +0.51423; MO85 -> MO87: +0.48072; MO80 -> MO86: +0.03678; MO83 -> MO89: +0.03414.
- S3: MO85 -> MO88: +0.66276; MO83 -> MO86: +0.24143; MO85 -> MO99: -0.02895; MO78 -> MO86: -0.02350.
- S4: MO83 -> MO86: +0.65964; MO85 -> MO88: -0.24190; MO83 -> MO91: -0.03523; MO81 -> MO88: -0.03402.
- S5: MO85 -> MO87: +0.51540; MO84 -> MO86: -0.48592; MO85 -> MO90: -0.05186; MO80 -> MO86: +0.02403.
- S6: MO82 -> MO86: +0.51725; MO85 -> MO89: +0.38984; MO83 -> MO87: +0.20237; MO84 -> MO88: +0.19187.

Orbital amplitudes are not probabilities; do not copy them as percentage contributions without the appropriate convention.

### 4. Full-printed-coefficient high-grid hole–electron analysis

- Directory: `artifacts/hole_electron_fullcoeff_20260918/`.
- Native evidence: `commands.txt`, `settings.ini`, `multiwfn.log`, `results.json`, `status.json`.
- Wavefunction and TD log: matched `fullcoeff.fchk` / `gaussian.log` from step 3.
- Software: Multiwfn 2026.7.15; menu 18 → 1, read TD log, analyze roots 1–4 individually, high grid (1782000 points), 2 threads.
- Actual cross-term threshold: `cfgcrossthres=0.01` (not 0.001 in this four-state high-grid run).
- Normal completion in 284.4321 s. Hole/electron integrals 0.999948–0.999991.

| State | D/Å | Sr | H/Å | t/Å | HDI | EDI |
|---|---:|---:|---:|---:|---:|---:|
| S1 | 0.001 | 0.78432 | 3.988 | -3.575 | 5.14 | 4.99 |
| S2 | 0 | 0.91366 | 3.907 | -3.442 | 4.6 | 4.54 |
| S3 | 0 | 0.74133 | 4.104 | -3.677 | 5.1 | 5.02 |
| S4 | 0.001 | 0.74956 | 4.207 | -3.771 | 4.54 | 4.95 |

These are computed data from the native analysis, not a table populated from evaluator targets. In particular S1 HDI/EDI are 5.14/4.99 for THIS high-grid branch; 5.13/4.98 belong to the subsequent medium-grid control.

### 5. Successful cutoff/grid controls (no new SCF/optimization/TD solve)

Evidence root: `docs/claude/artifacts/9a58_root_cause_20260918/`.

- `cross_0.001_grid2_states1-2-3-4-5-6/`: same fchk/log, cutoff 0.001, medium grid (532532 points), 2 threads, 162.4193 s. S2/S3/S4 Sr = 0.91388/0.74158/0.74978.
- `cross_0.001_grid3_states2-3/`: same fchk/log, cutoff 0.001, high grid, 2 threads, 158.7749 s. S2/S3 Sr = 0.91366/0.74133.
- Each directory preserves settings, input menu, raw Multiwfn log, results and exit status.
- The largest medium/high difference for S2–S4 in these checks is 0.00025; the S4 comparison changes both grid and cutoff. No S4 high-grid cutoff=0.001 run is claimed.
- D is almost zero, so the direction used by t can be sensitive even when Sr is stable. No new t hard threshold is added.
- SI Table S11 lists S2/S3/S4 Sr = 0.795/0.919/0.913. The discrepancy remains; simple grid/cutoff explanations have not resolved it. Neither root relabeling nor claims of author error are justified.

## Current evaluator alignment

- Existing S1 energy reference: 2.1406 eV, tolerance 0.08 eV; verification 2.1401 eV.
- Existing S1 Sr reference: 0.797, tolerance 0.08; verification 0.78432.
- New result key point: `pr_high_state_sr`, connected to the unchanged final conclusion as supporting evidence so the scoring runtime actually receives the new rules.
- Rule `pr_r6`: S2 Sr = 0.91366, binds `$.hole_electron[1].Sr`.
- Rule `pr_r7`: S3 Sr = 0.74133, binds `$.hole_electron[2].Sr`.
- Rule `pr_r8`: S4 Sr = 0.74956, binds `$.hole_electron[3].Sr`.
- Rule `pr_r5` remains the original final-conclusion rule.
- Each new Sr rule uses absolute tolerance 0.08, consistent with the existing S1 Sr scoring allowance. This is an authored benchmark criterion, not a calibrated cross-method error bar; observed grid-control differences (at most 0.00025) demonstrate stability of the reference route only. Five decimal digits identify the archived result, not a requirement to reproduce five decimal places.
- Task and schema require ordered arrays with explicit state IDs. Schema position constraints prevent duplicated/reordered IDs from silently satisfying a wrong state's scalar rule. Physical root identity and computational evidence still require scientific review.
- The Sr density definition and state serialization order are public; the autonomous mode retains method choice, and reproduction mode offers author-level route guidance. Sr answers, SI numbers and verification outputs remain evaluator-private. No universal cross-method invariance is claimed.
- Other S2–S4 descriptors remain required outputs with scientific consistency review, not newly added SI numeric targets.
- No extra final-conclusion count, global scoring-policy change or scientific limitation checklist was introduced.

## What this record does and does not establish

It documents a successful calculation route for the requested observables and the adopted benchmark Sr answers. It does not establish exact numerical reproduction of SI Table S11, universal method-independence of Sr, or causal BN-versus-carbon effects from a calculation of BN-AkFlu alone. The core scored conclusion remains weak S1 absorption, stronger higher-energy absorption and substantial S1 overlap; experimental emission/device performance is not inferred from these isolated-molecule calculations.

The original source files and low-grid records remain in the group directory. No new quantum-chemistry jobs were run to perform this evaluator-reference revision.
