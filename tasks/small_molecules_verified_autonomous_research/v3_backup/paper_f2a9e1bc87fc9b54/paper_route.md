# Private reference index for case_14

`agent_input/task.md` defines the public question. `evaluation/scoring_rules.json` is the authoritative `human_review_conclusion_evidence_20261102` / `paper_science_v3` scoring contract: 3 semantic conclusions, 100 points, no numeric target/tolerance gates.
Computed numerical evidence remains mandatory for each conclusion; absence of required values or genuine native support fails the associated item.

Readable criteria: `evaluation/scoring_guide.md`. Protocol: `evaluation/SCORING_INTERFACE.md`. Coverage: `evaluation/conclusion_coverage.json`.
Paper/SI and existing native verification references are in `evaluation/evidence_map.json`; limitations are in `evaluation/reference_qualification.json`.
`evaluation/verified_computation_reference.md` and `evaluation/historical_reference/` remain historical evidence, not extra scoring requirements. No new quantum verification or retrospective score change is claimed.
