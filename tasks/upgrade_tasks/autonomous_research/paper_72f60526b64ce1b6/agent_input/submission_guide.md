# Submission guide

Development status: pending scientific validation; no calibrated expanded reference or publishable upgraded score.

`results.isolated` requires AD, ApiD and AsigmaD numerical vector/magnitude dipoles. `results.devices` requires five named configurations, each with zero and ±0.5-V data and exact source artifacts. `comparisons.bridge/direction/contact` is compulsory; raw T(E,V), current integrations and potential profiles are separate from an isolated dipole. Ratio fields allow null only when documented current-floor bounds make a ratio unresolvable; missing transport is not a bound. `native_chain_manifest` enumerates allowed commands, inputs, dependent lead files and versions.

The top-level `status` is `complete`, `partial` or `bounded_failure`. Complete requires closed prerequisite records backed by actual evidence, methods, all results panels, at least two hypothesis records and a quantitative sensitivity record. This hypothetical complete contract does not certify that the current incomplete package is ready. Failed/partial submissions require `failure_report` and an incomplete conclusion; zero engine launches is truthful when failure precedes computation. Never enter zero for an unknown scientific value.

Each job ID and comparison reference must resolve uniquely. Every referenced artifact must exist, match its hash, and contain the named raw calculation; a schema-valid path or synthetic test fixture is not evidence. Hash the exact input, coordinate, log, wavefunction/density and analysis files used. Keep units, atom labels, charge/spin and geometry reference explicit. The report must explain numerical derivations and why the control can falsify the proposed explanation.

Optional work must be labelled separately. No extra ligand family, Group B junction, SAPT decomposition, docking, graphene or bulk/application inference is required unless explicitly in the core task.
