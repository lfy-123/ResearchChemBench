---
software_id: orca
versions: ["6.1.1"]
topics: [index]
aliases: [ORCA navigation, ORCA tasks]
inputs: ["ORCA input deck", "referenced geometry or basis files"]
outputs: ["stdout.log", "ORCA property and restart files"]
last_smoke_tested: null
---
# ORCA Native Guide

## Topics
- `quickstart`: input structure, blocks, staging, and resources.
- `single-point`: molecular single-point calculations.
- `optimization-frequency`: geometry optimization and vibrational frequency jobs.
- `excited-states`: TDDFT state calculations.
- `troubleshooting`: parser, path, SCF, resource, and termination failures.

## Executable
Use `orca` exactly as returned by `inspect_software`; pass one staged `.inp` target as the argument.
