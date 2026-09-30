# Reference validation plan — V2

The source provides all four molecular identities, ground-state/TD methods and a comparable1a screen; existing photophysical jobs can inform their exact state/geometry windows. This supports a bounded electronic investigation but does not validate full mechanism or an expanded oxygen-state cycle. Actual source mechanistic experiments apply to9a/24; this distinction corrects V1 overtransfer. No new scientific run.

## Source checked

- papers/paper_d3b4575397179146/documents/main.pdf PDF pages [3, 4, 5, 8, 9]; SHA256 da7d8a332e3db06579fabefe3cebeeebac3f61e58a0cb964b9e91a70eb54a22b
- papers/paper_d3b4575397179146/documents/supplementary_001.pdf PDF pages [19, 47, 48, 49, 50, 51, 52, 53, 54, 55, 101, 105, 106, 107]; SHA256 1b9598869e850445e58e1ae41e64fee1f5cd1b6ae49ab9f63bf06143c9e7aee5

## Reuse and gaps

- Claim-specific excited/redox-state calibration and kinetic inference remain pending.
- No direct1a quenching/trapping dataset is supplied;9a/24 cannot fill that gap.
- Numerical tolerances, semantic judge and runtime isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.
