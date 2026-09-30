# Reference validation plan — scientific validation pending

Personally read main PDF pp2–4 and transport sections; visually inspected Fig.1 and computational page. A–D labels mean donor/acceptor endpoints, not four candidates A through D. The bounded first-version family is three Group A members: A–D, A–pi–D, A–sigma–D; Group B remains optional.

Parsed SI coordinate blocks, personally inspected pp1–2 and pp5–10. Isolated counts are 22/26/28 atoms (C10H8N2S2, C12H10N2S2, C12H12N2S2); device counts are 92/96/98, each 72 Au plus a molecule missing its two thiol H atoms. Main text and Cartesian lists supply substantial geometry information, but not a checked allowed electrode/TranSIESTA/TBtrans workflow.

## Reusable evidence and limits

Old fixed isolated-AD dipole and force check are molecular calibration only. They contain no current, electrode self-energy, transmission or finite-bias convergence. The prior scalar target is removed. Source optimized coordinates remain private and cannot prove independent device construction.

## Explicit missing prerequisites

- Native siesta and tbtrans 5.4.2 invocation contracts are now declared, including stdin_file and dependencies; integrated TranSIESTA is selected through SolutionMethod transiesta. Scientific lead/device and finite-bias validation remains incomplete.
- No complete mapped allowed electrode/device input chain (pseudopotentials, principal layers, self-energy artifacts and finite-bias restart conventions) has been validated.
- No actual same-junction zero/±V pilot, transport convergence or expanded control reference is available.

## Minimum pilot and release sequence

1. Command declaration was resolved by the tool owner on 2026-09-28. Use the declared siesta/tbtrans routes and preserve exact dependencies and raw-output capture.
2. Translate the mapped identities into explicitly recorded Au(111) lead/central-region cells, anchoring and atom ordering. Use source SI privately for atom-count/geometry auditing; independently build public starts. Validate pseudopotential/basis compatibility and electrostatic lead matching.
3. Execute one AD_base zero/−0.5/+0.5-V pilot with actual self-consistent outputs, transmission integration and k/energy/screening convergence. Installed binaries or zero-bias molecular jobs do not close the gate.
4. Only then run all three bridges, AD reversal and unilateral contact perturbation; measure noise and sensitivity, calibrate common AR/PR evaluation and review release readiness.

## Full expanded reference

Three isolated dipoles and five device configurations at three biases (15 device/bias conditions, not claimed engine launch count), plus decisive lead/k/energy convergence. Include raw electrode and central inputs, finite-bias logs, T(E,V), I(V), profiles, integration scripts and floor-aware ratios. No 2A series is required.

## Software and quantitative calibration

Gaussian/ORCA can support isolated molecular baselines. Native siesta and tbtrans 5.4.2 are declared and executable, with integrated TranSIESTA; a scientifically validated matched electrode/device chain is still required. QuantumATK source settings are contextual. Do not claim an unsupported NEGF substitute or run unapproved subprograms. Numerical uncertainty must be measured from converged raw calculations, model variation and geometry sensitivity. Paper numbers remain historical anchors only; there is no newly calibrated absolute tolerance, ranking or winner. Do not impose optional extensions as gates.

## Actual work in this upgrade

At the original package construction no new quantum, periodic or transport engine was launched. The V1 verification continuation has prepared source-matched lead/device models and submitted the electrode pilot; a submitted job is not an observed engine launch or accepted reference. Local source reading, graph/stoichiometry checks and schema tests are development work. Preserve inputs, failed/restarted jobs, actual engine launches, CPU allocation and engine times when a future pilot is authorized and budgeted. Current scope is a development package, not a released benchmark or validated scientific reference.
