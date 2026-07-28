---
software_id: lobster
versions: ["5"]
topics: [projection-setup, cohp, coop, cobi]
aliases: [lobsterin, COHP projection, bonding projection]
inputs: ["lobsterin", "compatible VASP output set"]
outputs: ["lobsterout", "COHP, COOP, COBI, DOS, and charge files"]
last_smoke_tested: 2026-07-28
example_path: chemistry_toolbox/examples/native/lobster/cohp/lobsterin
---
# LOBSTER Projection Setup

## Input
Use one `lobsterin` with basis settings compatible with the upstream PAW datasets and explicitly request the COHP, COOP, COBI, DOS, or charge outputs needed by the task.

## Validation
Require normal LOBSTER termination, parseable requested outputs, and acceptable charge and total spilling under thresholds declared before interpretation.
