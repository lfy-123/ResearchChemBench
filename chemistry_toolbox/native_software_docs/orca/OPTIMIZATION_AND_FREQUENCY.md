---
software_id: orca
versions: ["6.1.1"]
topics: [optimization-frequency, optimization, frequency, surface-scans, constraints, hessian]
aliases: [ORCA Opt Freq, geometry optimization, frequency calculation, geom Scan, atom indices, InHess]
inputs: ["ORCA input deck", "referenced geometry or basis files"]
outputs: ["stdout.log", "ORCA property and restart files"]
last_smoke_tested: null
example_path: chemistry_toolbox/examples/native/orca/optimization_frequency/input.inp
---
# ORCA Optimization and Frequency

## Setup
Use `Opt` for geometry optimization and `Freq` only when a Hessian and vibrational analysis are required. A combined `Opt Freq` job evaluates frequencies at the final geometry.

## Coordinate formats
An inline `* xyz charge multiplicity` section contains atom coordinate rows and ends with `*`; omit the XYZ file's atom-count and comment lines. An external `* xyzfile charge multiplicity geometry.xyz` reference is one line ending in a newline, with **no closing `*`**. Stage the referenced XYZ file with its atom-count line, comment line (which may be blank), and the declared number of atom rows. Multiple XYZ frames may follow consecutively, optionally separated by `>`.

Source: ORCA 6.1 official manual, Essential Elements / Coordinates and Multiple XYZ File Scans.

## Scan and Constraints: zero-based atom indices
ORCA `%geom Scan` and `%geom Constraints` use **zero-based** atom indices: XYZ row 1 is index 0. For N atoms, valid indices are 0 through N−1. A chemical atom-map label is not an ORCA index. Check the mapping to the actual submitted coordinate rows.

This H2 example scans the distance between atoms 0 and 1; distances are in angstroms. `Opt` requests a relaxed scan. A single-point calculation without `Opt` does not establish a relaxed scan, even if it exits normally.

```text
! HF STO-3G Opt
%geom
  Scan
    B 0 1 = 0.74, 1.00, 3
  end
end
*xyz 0 1
H 0 0 0
H 0 0 0.74
*
```

For a fixed bond constraint, use `Constraints` with `{ B 0 1 C }` inside the `%geom` block instead of the Scan block. Confirm scan steps or constrained optimization in the native output; a normal footer alone does not establish that the requested operation ran.

Source: ORCA 6.1 official PDF manual, PDF page 52 (indexing) and Geometry Optimizations / Relaxed Surface Scans. The versioned PDF and derived page-numbered text are in the local documentation cache.

## InHess: supported initial Hessian models
The `%geom InHess` options include `unit`, `Almloef`, `Lindh`, `Schlegel`, `Swart`, `XTB0`, `XTB1`, `XTB2`, `GFNFF`, and `Read` with `InHessName`. `GXTB` is not an `InHess` option. Changing the Hessian does not repair an out-of-range Scan or Constraints atom index. See the installed version's manual for method and coordinate-system restrictions.

Source: ORCA 6.1 official PDF manual, PDF pages 621 and 639.

## SMD solvent specification
For SMD, use `%cpcm` with `smd true` and `SMDsolvent "1,4-dioxane"`, followed by `end`. A `Solvent name not provided` message is an input failure even if the executable returns zero. The predefined ORCA Action accepts this through `method_spec.solvation_model="smd"` and `method_spec.solvent`.

## Validation
Require normal termination, optimization convergence, and the expected number of vibrational modes. A minimum should have no meaningful imaginary frequencies; a transition state should have one intended imaginary mode and must be checked separately.

## Restart
Do not claim convergence from the last geometry of an interrupted job. Restart from a collected geometry or ORCA restart artifact using syntax compatible with the installed version.
