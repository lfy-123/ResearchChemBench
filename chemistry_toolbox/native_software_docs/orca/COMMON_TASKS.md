---
software_id: orca
versions: ["6.1.1"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["ORCA", "orca"]
inputs: ["input.inp", "optional external XYZ", "basis", "point charges", "or restart files", "export: input.gbw and optional input.json.conf; input.densities for requested densities"]
outputs: ["stdout.log", ".gbw", ".xyz", ".hess", ".densities", "property files", "export: input.json"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# ORCA Common Tasks

## Appropriate calculation families
- **Single Point**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Frequency**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Transition State**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Irc**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Excited States**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Correlated Density**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Existing Gbw To Ascii Json**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `calculate_energy`: validated structured route through backend `orca`.
- `calculate_forces`: validated structured route through backend `orca`.
- `calculate_hessian`: validated structured route through backend `orca`.
- `optimize_geometry`: validated structured route through backend `orca`.
- `calculate_dipole_moment`: validated structured route through backend `orca`.
- `calculate_atomic_charges`: validated structured route through backend `orca`.
- `calculate_orbitals`: validated structured route through backend `orca`.
- `calculate_bond_orders`: validated structured route through backend `orca`.
- `calculate_excited_states`: validated structured route through backend `orca`.
- `calculate_correlated_electron_density`: validated structured route through backend `orca`.
- `export_electron_density_grid`: validated structured route through backend `orca`.

## Minimum input responsibilities
- `input.inp`
- `optional external XYZ`
- `basis`
- `point charges`
- `or restart files`
- `export: input.gbw and optional input.json.conf; input.densities for requested densities`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `stdout.log`
- `.gbw`
- `.xyz`
- `.hess`
- `.densities`
- `property files`
- `export: input.json`

Only collect outputs produced by the same job or by explicitly linked parent jobs. Do not combine checkpoints, force constants, trajectories, pseudopotentials, wavefunctions, or databases from unrelated calculations.

## State-specific validation
| State | Required evidence | Not sufficient |
|---|---|---|
| Process completed | Exit code zero and Supervisor did not cancel or time out | A submitted job ID |
| Software normal | Program-specific normal marker and absence of fatal diagnostics | Exit code zero alone |
| Electronic convergence | Requested SCF or electronic tolerance reached | A printed energy from an unconverged cycle |
| Geometry convergence | Optimization stopping criteria reached for the requested degrees of freedom | SCF convergence at the last geometry |
| Frequency completion | Hessian/frequencies finished and modes were parsed | Optimization completion alone |
| Transition-state candidate | Optimization converged and exactly the intended imaginary mode was verified | One negative number without mode inspection |
| Dynamics completion | Requested steps completed with acceptable stability diagnostics | Creation of a partial trajectory |
| Artifact validity | Required files exist, are non-empty, and can be parsed | Files with expected names only |

## Software-specific end markers
- `ORCA TERMINATED NORMALLY`

## Scientific convergence notes
SCF CONVERGED, geometry convergence, frequency completion, imaginary-mode count, and IRC completion are separate checks. orca_2json is postprocessing with no SCF convergence criterion; inspect native return code, the JSON writing marker and collected JSON identity/fields, not an ORCA TERMINATED NORMALLY footer.

## Version-specific caution
These mechanics target the installed `6.1.1` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `orca`
- Synopsis: `orca input.inp`.
- Input mode: `arguments`.
- Declared example inputs: `input.inp`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes the primary output to stdout and ORCA property/restart files in the job directory.
- Caution: Method, basis, charge, multiplicity, calculation keywords, parallelism, memory, and convergence must be explicit in input.inp.
- Caution: ORCA should be launched by its resolved absolute path; the execution layer does this without changing the input.
- Caution: Count negative modes in the final VIBRATIONAL FREQUENCIES block or matching .hess file; Total number of imaginary perturbations is not a vibrational imaginary-frequency count. A single negative mode still needs reaction-mode and connection evidence for a claimed pathway.
- Caution: Use this asynchronous native-job contract when the Agent must author an ORCA input deck directly; it uses the same evaluator-controlled compute timeout as managed compute Actions and requires stable bulk supervision with wait_execution_jobs.

## Command: `orca_2json`
- Synopsis: `orca_2json input.gbw -json`.
- Input mode: `arguments`.
- Declared example inputs: `input.gbw`, `input.json.conf`.
- Declared example outputs: `input.json`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Writes input.json and stdout.log in the job directory; collect_execution_job returns file paths and hashes. Export completion does not validate SCF, TD states or any scientific interpretation.
- Caution: Reviewed interface is existing GBW to ASCII JSON only, with optional -json. Property conversion, GBW import and binary JSON formats are not exposed by this contract.
- Caution: Stage the GBW and same-basename input.json.conf explicitly. A staged orca.json.conf is the directory-wide alternative; do not stage both configuration files. No configuration means native defaults, not requested densities or integrals.
- Caution: For MO coefficients, basis data and overlap use {"MOCoefficients": true, "Basisset": true, "1elIntegrals": ["S"], "JSONFormats": ["json"]}. ORCA may compute auxiliary integrals during export; no SCF or TD recalculation is requested.
- Caution: JSON contains Molecule.Atoms, Charge, Multiplicity and CoordinateUnits; the example additionally requests per-atom Basis, MolecularOrbitals.MOs[].MOCoefficients and S-Matrix. Check actual keys/dimensions and molecular identity after collecting the output.
- Caution: Densities requires the matching .densities file and explicitly selected names. GBW/MO export alone does not export full-RPA X/Y amplitudes; those require the original .cis and separate validated state mapping/analysis.
- Caution: Use software_id=orca, executable=orca_2json, calculation_intent=other. The installed 6.1.1 executable is separately allowlisted; no arbitrary command or shell fallback is enabled.
