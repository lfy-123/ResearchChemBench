# case_02 Input preparation checklist

This directory provides the scientific question, exact molecular connectivity, stereochemical constraints, conditions/observations, budget and submission format. No further human transcription of molecules from paper screenshots is needed; figures and multimodal functionality are not required.

|File|Prepared content|Provide to ARCHE?|
|---|---|---|
|task.md|Complete text-only scientific question, scope and required results|Yes|
|molecules.json|SMILES, atom/bond tables and necessary stereochemical/coordination definitions|Yes|
|facts_and_conditions.json|Chemical conditions and explicitly permitted experimental facts|Yes|
|run_settings.json|Proposed common budget and number of runs|Yes|
|submission_schema.json|Format for results, native evidence and physical references|Yes|
|initial_geometry.xyz and initial_geometry.mapping.json|Independently generated initial guess without quantum-chemical optimization, with complete mapping|Yes|

For cases without an initial XYZ, the connectivity graphs and constraints already suffice to define the problem. ARCHE must construct three-dimensional conformations, coordination models and TSs. This is part of the capability being tested; humans need not prepare correct intermediates or transition states in advance.

The operator only needs to provide available computational software/scheduling interfaces, fix the configuration and storage location for this run, and copy this directory separately to ARCHE. Papers and private answers must not be mounted in the execution environment. If supplied inputs conflict, record the conflict and refer it for reference adjudication; humans must not repair molecules or suggest pathways during the primary run.
