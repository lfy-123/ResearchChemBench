# Reference validation plan — V2

Published bda/Py finite structures and TableS21/energy tables support model reconstruction and qualified source-baseline auditing. Existing local-mode work does not validate the old≈110i assignment or all new channels. Ligand constitutions and local inventories are sufficient public molecular inputs; source answer coordinates remain private.

## Source checked

- papers/paper_e2d9397dff2a3f0f/documents/main.pdf PDF pages [8, 9, 10, 11]; SHA256 c24bbaae86761a8d40104b001d415708990565d075c29789011a3c8104993875
- papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf PDF pages [25, 26, 47, 48, 69, 70, 71, 73, 78]; SHA256 1f4f524a63c1856d741bc9b9016079f9fe8ba2eea9117df6a2df9f72bd626975

## Reuse and gaps

- Independent local-state and N–N evidence and defensible numerical uncertainty remain pending.
- Source diffusion-control and global-RDS interpretations need stronger evidence than a monotonic electronic scan or local thermochemistry.
- Semantic calibration and isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.
