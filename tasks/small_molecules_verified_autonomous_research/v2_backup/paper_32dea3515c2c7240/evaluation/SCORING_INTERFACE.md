# Scoring interface

`expert_scoring_rules.json` contains the English expert criteria with the user-authorized 2026-10-26 amendment: only r_inversion_p now uses 33.99±3.0 kcal/mol instead of 33.99±2.0. The immutable source expert package retains the original tolerance. `scoring_rules.json` contains exactly the same scientific item identities, weights, criteria, numerical targets and tolerances, using the repository-supported `paper_science_v2` transport policy and bindings. The transport projection does not change any scientific criterion.

The expert whole-case decision requires all required items to pass after evidence qualification. A weighted score, an empty review template, or a completed job does not establish whole-case success. Use the provided blinded adjudication template and the unchanged expert aggregation tool:

```bash
python evaluation/score_case.py \
  --rules evaluation/expert_scoring_rules.json \
  --results /run/report/results.json \
  --adjudication /review/adjudication.json \
  --submission-root /run \
  --output /review/score.json
```

The source-file paths inside the untranslated package layout are resolved by `expert_source_map.json`. Historical files retain their original language and are not active scoring rules. The submission file contains the expert JSON Schema unchanged plus the repository transport fields `required_files`, `primary_result_file` and an identical `result_schema` view.
