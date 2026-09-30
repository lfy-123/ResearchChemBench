# Expanded-reference validation plan

Status: implemented_pending_expanded_reference. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_9132719dbf91c978/documents/main.pdf`, PDF pages 1, 4; SHA256 3d08d907aafb9175e71858913e8f6671891645f0479d189eab246a24d442faeb
- `papers/paper_9132719dbf91c978/documents/supplementary_001.pdf`, PDF pages 10, 11, 12; SHA256 ae27addc290464f1b17ef3fbd0dd6cac8eb0830aa03cc0aaa686fd57321d2817

The authors propose HAT formation of Pd dihydride INT-G followed by H2 reductive elimination, with a small local barrier (main p4, SI pp10–12/FigS4). The new release/recoordination and pressure controls are benchmark extensions. Historical −1.76058 kcal/mol at 1 atm and +0.133748 with all solutes 1 M refer to different conventions, not conflicting measurements on one scale.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- HH_formation: Connected H–H formation saddle and bound-H2 endpoint.
- release_and_recoordination: Real separated and re-ligated states, not relabelled eta2-H2.
- standard_state_control: Explicit H2 pressure and gas/solute standard-state conversions.

The existing terminal-H2 verification includes INT-G/TS6, bidirectional endpoints, dissociation scans and separated Pd/H2 calculations. Check exact state, level and standard state before reusing those artifacts. DMAc recoordination, mixed gas/solute standard-state comparison and pressure sensitivity remain new gaps.

Historical structured reports directly inspected in this development pass:

- `docs/verification/group_4/paper_9132719dbf91c978/provenance/terminal_h2_closure_20260923/result.json`; SHA256 71ae33985e006817eb1fe4c8ef9e39f590d75c2bab9498c329685e0cd88d1be4
- `docs/verification/group_4/paper_9132719dbf91c978/report/results.json`; SHA256 4cd2a9c8752df8c9eb112007c63dc0f5ec62ec5ee07cf657b3907f371d2e8b4e

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Audit one old connected H-H path and the actual bound-versus-separated H2 identities; then independently optimize Pd(XantPhos)(DMAc). Assemble a mixed H2 gas1atm/solute1M ledger, compare all1M and pressure dependence, and locate the limiting local regeneration cost without extrapolating to full turnover.

### Scientific adversarial calibration (not executed here)

Rename eta2-H2 as free gas, delete XantPhos or mix 1atm and 1M terms to make regeneration favourable: reject.

Unfavourable release or recoordination under the declared pressure is a valid result even if the H-H saddle is small.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

Bound H2 called free gas; mixing 1atm/1M terms; deleting XantPhos; small H–H barrier used as proof of spontaneous release or full catalyst turnover.
