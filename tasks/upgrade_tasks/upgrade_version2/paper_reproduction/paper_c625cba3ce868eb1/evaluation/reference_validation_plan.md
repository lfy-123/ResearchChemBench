# Reference validation plan — V2

Source graphs and substrate MEP calculations support a bounded molecular study. Previous NBS-related local structures can only support their exact state/inventory and require actual stationary-point/path inspection before reuse. Expanded kinetic explanation is not already validated by source charges. No new calculations were run.

## Source checked

- papers/paper_c625cba3ce868eb1/documents/main.pdf PDF pages [3, 5, 6, 7]; SHA256 44b374957665d941b519f781fe9341f1632c84a6c7b975c4cd231874281e0ef8
- papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf PDF pages [30, 31, 32]; SHA256 19d3e128aae61e6d8f4904d7f5f3cc8cd31230ccb210eb81ba15402de096e4db

## Reuse and gaps

- NBS chemical-path and selectivity calibration remains pending.
- The source concentration typo and aqueous-computation/DCM-experiment mismatch must remain explicit.
- Expanded uncertainty, semantic judge and runtime isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.
