# case_10 Input preparation checklist

This directory supplies the scientific question, exact molecular connectivity, stereochemical constraints, conditions/observations, budget and submission format. No further human transcription of molecules from paper screenshots is needed, and neither figures nor multimodal capabilities are required.

|File|Prepared contents|Provide to ARCHE|
|---|---|---|
|task.md|Complete plain-text scientific question, scope and required results|Yes|
|molecules.json|SMILES, atom/bond tables and necessary stereochemical/coordination definitions|Yes|
|facts_and_conditions.json|Chemical conditions and explicitly permitted experimental facts|Yes|
|run_settings.json|Recommended uniform budget and number of runs|Yes|
|submission_schema.json|Format for results, native evidence and physical references|Yes|

For cases without initial XYZ files, the connectivity graphs and constraints already suffice to define the problem. ARCHE constructs three-dimensional conformers, coordination models and TSs. This is the capability being tested; humans need not prepare correct intermediates or transition states in advance.

Operators only need to provide available computational software/scheduling interfaces, freeze the configuration and storage location for this run, and copy this directory separately to ARCHE. Papers and private answers should not be mounted in the runtime environment. If supplied inputs conflict, record the conflict and submit it for reference adjudication; humans must not repair molecules or suggest pathways during the main run.
