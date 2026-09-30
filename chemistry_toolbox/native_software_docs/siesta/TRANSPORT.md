---
software_id: siesta
versions: ["5.4.2"]
topics: ["transport", "TranSIESTA", "TBtrans", "provenance", "validation"]
aliases: ["SIESTA", "TranSIESTA", "TBtrans"]
inputs: ["input.fdf", "pseudopotentials", "converged electrode and device Hamiltonians"]
outputs: ["native logs", "Hamiltonians", "transmission", "configured current-analysis outputs"]
last_smoke_tested: null
---
# Integrated TranSIESTA and TBtrans

## Installed command routes

The installed SIESTA and TBtrans binaries both report 5.4.2. This is an executable
availability observation, not a completed transport scientific smoke.

TranSIESTA is integrated into `siesta` in current SIESTA releases. Select
`SolutionMethod transiesta` in the full FDF input; a separate `transiesta` executable
is neither required nor declared. Native TBtrans requests use software ID `siesta`,
executable `tbtrans`, an explicit FDF file staged as `input.fdf`, and
`stdin_target: input.fdf`. As usual, arguments are individual tokens, never a shell
redirection string.

## Scientific dependencies

An installed binary or a successful version query is insufficient. The agent must:

- Supply actual lattice vectors, the electrode repeat units, the scattering region,
  composition, atom order, contact geometry, pseudopotentials and localized basis.
- Generate converged electrode Hamiltonians with the intended k sampling, spin,
  XC, temperature and numerical conventions.
- Link each scattering-region run to those exact electrode artifacts and its
  explicit chemical potentials and voltage convention. Finite-bias SCF convergence
  must be checked at each required sign and value of the bias.
- Stage the matched device/electrode HSX, TSHS or supported NetCDF artifacts in the
  paths named by the TBtrans FDF. Preserve original hashes and job identities.
- Check transmission-energy integration, k mesh, screening length and current
  conservation. State the energy zero and the relation between bias and electrode
  chemical potentials. Reintegrate currents using the declared temperature.

TBtrans evaluates transport from Hamiltonians; it does not establish that the
upstream finite-bias density is self-consistent. Do not substitute an isolated
dipole, orbital gap, field energy or equilibrium Hamiltonian for that evidence.
Matching a different code's electrode/basis/pseudopotential setup requires a
documented scientific correspondence and a converged pilot.

## Verification boundary

Native catalog declaration and staging checks establish interface availability.
They do not certify a particular junction or validate the benchmark's reference.
Version-query evidence and the exact official pages retrieved on 2026-09-28 are
recorded in `docs/upgrade_tasks_v2_review_20260928/coordinator_review/`.

Official references:

- https://docs.siesta-project.org/projects/siesta/en/stable/reference/siesta.html
- https://docs.siesta-project.org/projects/siesta/en/stable/reference/tbtrans.html
