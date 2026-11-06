# case_13 Input preparation checklist

This directory provides the scientific question, exact molecular connectivity, stereochemical constraints, conditions/observations, budget and submission format. No human transcription of molecules from paper screenshots is needed, and no accompanying images or multimodal capabilities are required.

|File|Prepared content|Provide to ARCHE?|
|---|---|---|
|task.md|Complete plain-text scientific question, scope and required results|Yes|
|molecules.json|SMILES, atom/bond tables, and necessary stereochemical/coordination definitions|Yes|
|facts_and_conditions.json|Chemical conditions and explicitly permitted experimental facts|Yes|
|run_settings.json|Recommended common budget and number of runs|Yes|
|submission_schema.json|Format for results, native evidence and physical references|Yes|

For tasks without initial XYZ files, the connectivity graphs and constraints are sufficient to define the problem. ARCHE constructs three-dimensional conformations, coordination models and TSs. This is part of the capability being assessed; humans do not need to prepare correct intermediates or transition states in advance.

The operator only needs to provide available computational software/scheduler interfaces, freeze the configuration and storage location for this run, and copy this directory separately to ARCHE. Papers and private answers should not be mounted in the execution environment. If contradictions arise in the supplied inputs, record them and refer them for reference adjudication; humans should not correct molecules or suggest pathways during the main run.
