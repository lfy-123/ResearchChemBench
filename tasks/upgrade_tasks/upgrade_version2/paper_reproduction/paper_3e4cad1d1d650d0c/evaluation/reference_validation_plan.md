# V2 reference validation plan

Existing Gaussian anion/radical logs and reproducible analysis demonstrate a feasible solution-phase molecular route. The toolbox Gaussian/ORCA and Python analysis interfaces may support alternative routes after inspecting actual installed capability. No new calculation is needed for this content upgrade; future reference review can first reparse the named artifacts and Figure 3 and then assess any method-specific gaps.

## Existing evidence and limits

Read-only existing real artifacts: docs/upgrade_tasks_verification/group_2/papers/paper_3e4cad1d1d650d0c/report/results.json (SHA256 84bf365fd1e7d49e9837eb500d20900948bbb04702c74bb35a1771f4af22fd75), report/report.md, analysis/recompute.py, analysis/resource_accounting.json, outputs/legacy_reused/1a_anion/stdout.log, outputs/legacy_reused/1e_anion/stdout.log, outputs/1a_radical_source_optfreq/attempt_002/stdout.log and outputs/1e_radical_source_optfreq/attempt_001/stdout.log. These support an author-informed CAM-B3LYP/CPCM route and its limited sensitivities plus a graphical quenching analysis. They are not blind AR evidence or an exhaustive model reference, and their additional operations are not V2 requirements.

## Outstanding scientific calibration

Electrochemical total error and microscopic association alternatives are not calibrated; raw individual lifetime measurements are missing. Existing reference computations were author-informed and used a limited state/conformer model. A quantitative kinetic or yield conclusion is unsupported. V2 semantic judge calibration and sandbox isolation are pending.

This authoring run performed no new chemistry calculations, HPC submissions or remote judge calls. Offline package/contract/runtime checks do not establish chemical accuracy. A future reference review should verify source/structure/state correspondence, reproduce the claim-relevant quantities from raw existing artifacts, and assess the agent-chosen method limitations; additional science is separately authorized. No fixed V1 matrix, winner or uncalibrated tolerance is an acceptance rule. Actual alternative-route judging and private-file isolation must be checked independently.
