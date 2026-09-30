# Reference validation plan — V2

Source catalyst graphs and charge-calculation protocol support a small molecular baseline. Existing charge/cluster calculations, where exact geometry and inventory match, can inform feasibility but do not certify local reaction barriers or full catalytic synergy. No new engine run is needed for content authoring.

## Source checked

- papers/paper_6f9a36fff6964313/documents/main.pdf PDF pages [1, 3, 4]; SHA256 52d820c30c17046603a1f36d40eaa3ee538c8b16a60d329a00ed678a09d61c4c
- papers/paper_6f9a36fff6964313/documents/supplementary_001.pdf PDF pages [7, 8, 12, 16]; SHA256 e6f2422063d54b825e1ee8290d0671b06674dc7633081ca057c2388d636bf419

## Reuse and gaps

- New local reaction evidence and its numerical uncertainty remain pending; source population analysis is not a reaction reference.
- Mixture speciation and standard-state/pressure effects require claim-specific treatment.
- Actual judge calibration and filesystem isolation pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.
