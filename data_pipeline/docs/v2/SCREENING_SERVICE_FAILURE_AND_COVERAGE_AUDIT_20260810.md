# Screening Service Failure and Coverage Audit (2026-08-10)

## Incident conclusion

The 2,000-paper run is not a valid end-to-end screening result. Stage 02 recorded 725
`processing_failed` decisions after the local Qwen endpoint at `127.0.0.1:18083`
became unreachable. These records are infrastructure failures, not screening
rejections.

The run had 1,776 Stage 01 package passes, hence 178 ten-paper microbatches. Phase 1
did finish all 178 microbatches before the Qwen-to-MinerU switch. The phase barrier
did not return early. The failure began around 13:53, approximately nine minutes
before Phase 1 aggregation and the intentional service switch at 14:02-14:03.

At inspection time there was no local SSH forward listening on port 18083. The same
remote worker was reachable and subsequently hosted MinerU on port 18084. The most
likely failure is therefore loss of the long-lived SSH tunnel, although the remote
runtime logs were ephemeral and had already been removed with the worker, so a
simultaneous gateway failure cannot be excluded. The previous implementation had no
runtime tunnel recovery and converted exhausted connection retries into isolated
paper errors, allowing the queue to continue.

## General fix

- `manage_rlaunch_worker.sh recover-screening` checks the remote gateway first. It
  recreates only the SSH tunnel when Qwen is healthy and restarts Qwen only when the
  remote health check also fails.
- `ManagedScreeningServiceGuard` performs rate-limited local health checks and
  serializes recovery, preventing concurrent model calls from starting duplicate
  recovery operations.
- `RoleModelClient` retries one complete request after managed-service recovery.
- Stage 02 and Stage 03 now raise `ManagedScreeningServiceError` after an unrecovered
  connection failure. Phase 1 stops and cannot switch the worker to MinerU.
- `ordered_pipeline_map` now cancels queued work after the first stage exception.
  Microbatch outputs containing errors remain non-reusable, so a resumed run can
  recompute them after service restoration.

The current two-phase pipeline already enforces that all Stage 01-03 work finishes
before MinerU starts. That scheduling change was committed while the failed run was
already executing and was not loaded by its Python process.

## Manual audit of the 15 old `software_covered` decisions

The audit used each paper's main text and all locally available supplementary text,
not only the model summary. "Core covered" means every explicitly named program
needed for the main computational workflow exists in the current toolbox native
catalog. Auxiliary visualization names do not reject a paper, but are recorded as
inventory caveats.

| # | DOI | Manually observed software | Core covered | Audit note |
|---|---|---|---|---|
| 1 | 10.1021/jacs.4c00529 | Gaussian 16, ORCA 5.0, CP2K | yes | Complete named workflow. |
| 2 | 10.1021/jacs.3c12780 | VASP, VASPKIT | yes | Old result omitted VASP and passed for the wrong evidence reason. Current aliases recover the full VASP name. |
| 3 | 10.1021/jacs.3c12400 | Gaussian 16 | yes | Diradical/HOMA post-processing is not attributed to another named executable. |
| 4 | 10.1021/acscatal.5c02037 | CREST, xTB, Gaussian 09 | yes | CYLview and SambVca are auxiliary analysis/visualization omissions in the old inventory. |
| 5 | 10.1039/d3sc06107h | LAMMPS, pymatgen | yes | OVITO is mentioned only for trajectory visualization and is absent from the current catalog. |
| 6 | 10.1021/acscatal.4c03226 | VASP, Materials Project data | yes | Materials Project is also catalogued; it is a structure source rather than the DFT engine. |
| 7 | 10.1021/acscatal.4c04049 | Quantum ESPRESSO, ASE, VASP | yes | Both primary and validation DFT engines are present. |
| 8 | 10.1002/anie.202406095 | Gaussian 16, ORCA, CREST, xTB, Multiwfn, VMD | yes | Complete named workflow; VMD is visualization-only and also catalogued. |
| 9 | 10.1039/d4sc07811j | VASP, LOBSTER, VASPKIT, VESTA | yes | Bader analysis is named as a method without a separate executable name. |
| 10 | 10.1021/jacs.4c06067 | Gaussian 09, CREST, GoodVibes | yes | CYLview/PyMol are auxiliary visualization omissions. |
| 11 | 10.1002/anie.202405405 | VASP, LOBSTER, Materials Project data | yes | The old model incorrectly described Materials Project as computing RDF; it is only a structure source. |
| 12 | 10.1021/jacs.5c08979 | VASP | yes | Microkinetic post-processing is described but no separate program is named. |
| 13 | 10.1021/acscatal.4c06557 | Gaussian 16, GoodVibes, CREST, Multiwfn | yes | Complete named workflow. |
| 14 | 10.1021/jacs.4c01354 | VASP | yes | VASP supplies DFT, constrained AIMD and thermodynamic integration. |
| 15 | 10.1039/d4sc03378g | VASP | yes | The MLFF and delta-ML workflow uses VASP's on-the-fly MLFF implementation. |

All 15 papers use a toolbox-covered core computational engine. However, the old
model inventory should not be called fully reliable: papers 2, 4, 5, 10 and 12 have
an omitted, misclassified or unnamed auxiliary step. The current code is stricter:
an essential step without named software or an explicit `task_specific_python`
execution layer returns `software_inventory_unconfirmed`, and the current alias set
detects "Vienna ab initio simulation package" as VASP.

## Verification

- Shell and Python syntax checks passed.
- Targeted recovery, retry, phase-barrier and cancellation tests passed.
- Full data-pipeline suite: 341 tests and 8 subtests passed.
