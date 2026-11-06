# Submission guide

Submit `report/results.json` and `report/report.md` using `submission_schema.json`. Set `case_id` to `case_08`; this is the submission identifier. Record unresolved findings in `unresolved`.

- `models`: identify molecular models, conditions and approximations.
- `states`: identify composition, charge, multiplicity, geometry files and supporting evidence.
- `metrics`: report the required computed values with units, physical definitions, subtraction order where applicable, reference states, conditions and evidence IDs.
- `claims`: state the scientific conclusions, link them to metric/evidence IDs and describe their limitations.
- `evidence`: retain native input/output paths, relevant geometry files, calculation type, settings and validation results. All referenced IDs and files must resolve.

Describe methods, numerical derivations and the scientific meaning of the results in `report/report.md`. Integrated or symmetry-based inferences may reuse explicitly identified computed values. Supplied observations and newly computed results need distinct provenance. Retain actual failed attempts and available evidence without inventing missing quantities. Field names and allowed types are defined by the schema.

## Resource protocol

Use the supplied inputs, computational tools and general chemical-method/software documentation. The source paper, its mechanism or energy answers, author-computed structures, private evaluation files, historical runs and other systems' results are excluded; general web literature searches are not permitted.
