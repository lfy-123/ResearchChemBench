# Reference validation plan — V2

Source monomer graphs and formal molecular descriptor methods permit a bounded molecular investigation. Existing descriptor/conformer outputs, if reused privately after state/method checks, support only those quantities; previous attempted first-acylation calculations do not establish a validated reaction path. No scientific execution was performed for this upgrade.

## Source checked

- papers/paper_534ae3b6e2fb695f/documents/main.pdf PDF pages [2, 3]; SHA256 285a5ec0e199ceec20676911267bae9407b30b2576f345aa5884611d83955e11
- tasks/upgrade_tasks/coordination_20260927/batch4/source_review/paper_534ae3b6e2fb695f/publisher_formal_SI.pdf PDF pages [10, 11, 12, 13, 14, 20, 21, 22, 32]; SHA256 b1244e83d3294b7f9628231d1c173995c3158077fcf8663266632602c2306c89

## Reuse and gaps

- Reaction-path or kinetic interpretations beyond electronic descriptors remain uncalibrated.
- The source optimization-basis wording is inconsistent; a reproduction must state its interpretation.
- Semantic judge, new numerical error bounds and runtime filesystem isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.
