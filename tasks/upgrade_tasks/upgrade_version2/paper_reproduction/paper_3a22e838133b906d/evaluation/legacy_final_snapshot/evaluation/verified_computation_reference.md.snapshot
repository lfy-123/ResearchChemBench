# Verified computation reference — paper_3a22e838133b906d (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Public-input maintenance note (2026-09-14)

The SI neutral and anion optimized endpoints are retained only under `evaluation/author_results/`. The public XYZ files are RDKit ETKDGv3 topology-only starters (seeds 2337/3337), with composition, charge, multiplicity and P/O/B atom mapping preserved. No new quantum calculation was run; the historical author-route result supports the evaluator target but does not certify reachability from these changed public starters.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **AUTHOR_ROUTE_ONLY_PUBLIC_STARTER_NOT_REPLAYED**
- Applicability note: Public neutral/anion endpoint coordinates from the SI DFT section were replaced by independent topology-only starters; the historical group verification used the author endpoints. Under the accepted author-route verification policy this starter difference is not itself a task/evaluator mismatch; no independent discovery or public-starter replay is claimed.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 8 | `CONDITIONAL` | - 最终状态：**CONDITIONAL** |
| 108 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 117 | `PASS` | - 论文复现结论：`PASS` |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Dealkylation as a Strategy to Synthesize Unconventional Lithium Salts from ortho-Phenyl-phosphonate-boranes
- DOI: `10.1021/acs.inorgchem.5c05101`
- Task package: `tasks/final_verified_paper_reproduction/paper_3a22e838133b906d`
- Verification group: `docs/verification/group_1/paper_3a22e838133b906d`
- Paper documents: `papers/paper_3a22e838133b906d`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": "Anion minus neutral differences (Å): P-O1=+0.041255, P-O2=+0.064125, P-O3=-0.109385, O1-B=-0.116464. The stated comparison is qualitative and scoped to the isolated models.",
  "coverage": {
    "advanced_candidates": "Both named states were advanced through optimization and frequency validation.",
    "candidate_generation": "Neutral and anion structures supplied in the public task input.",
    "deduplication": "Not applicable to the two explicitly defined charge states.",
    "stopping_statement": "Stopped after both states had normal termination and zero imaginary frequencies."
  },
  "differences_A": {
    "O1-B": -0.11646424616004936,
    "P-O1": 0.04125538412468743,
    "P-O2": 0.06412469125061127,
    "P-O3": -0.10938505565517564
  },
  "interpretation": "The anion lengthens P-O1/P-O2, shortens P-O3 and shortens O1-B relative to the neutral model. This direction is consistent with strengthened intramolecular O(P)...B interaction in the isolated-model comparison.",
  "limitations": "The calculation omits Li+, solvent and crystal packing. The experimental boundary is labeled O2-B whereas the computational extraction uses O1-B; atom-label mapping must be kept explicit.",
  "method": {
    "charges_and_multiplicities": "neutral singlet (0,1); monoanion singlet (-1,1)",
    "method_description": "B3LYP-D3(BJ)/6-311++G(2d,p) Opt+Freq",
    "software_or_code": "Gaussian 16"
  },
  "provenance": "artifacts/author_gaussian_parsed.json",
  "states": [
    {
      "atom_mapping": "P=11; O1=12; O2=13; O3=14; B=21",
      "distances_A": {
        "O1-B": 1.6955959118082942,
        "P-O1": 1.516778733237317,
        "P-O2": 1.5793438823698276,
        "P-O3": 1.5945705807536397
      },
      "imaginary_frequency_count": 0,
      "state": "neutral",
      "validated": true,
      "validation_evidence": "docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log; normal termination, Opt+Freq, 87 frequencies"
    },
    {
      "atom_mapping": "P=11; O1=12; O2=13; O3=14; B=18",
      "distances_A": {
        "O1-B": 1.5791316656482448,
        "P-O1": 1.5580341173620045,
        "P-O2": 1.6434685736204389,
        "P-O3": 1.485185525098464
      },
      "imaginary_frequency_count": 0,
      "state": "anion",
      "validated": true,
      "validation_evidence": "docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log; normal termination, Opt+Freq, 75 frequencies"
    }
  ],
  "status": "complete"
}
```

Paper/SI document hashes:

- `papers/paper_3a22e838133b906d/documents/main.pdf` — SHA-256 `0b3a6429a4f8d324616b78c736daedf397971e63fdeff848f1b28058a39a1238` (declared_match=True)
- `papers/paper_3a22e838133b906d/documents/supplementary_001.pdf` — SHA-256 `0179f85740483c73a9996ca3c5ef36fd4f0044eca862b18eadc90e03463a7235` (declared_match=True)

Report evidence lines retained:

- Each optimized structure was accepted only after a frequency calculation showed zero imaginary frequencies. The authors extracted the P–O distances and the intramolecular B···O(P) contact and compared neutral/anion changes with crystallographic 2a/[Li(MeCN)2][3] data. The comparison is qualitative in the prose; the SI supplies the model coordinates and calculation summaries.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **10**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/status.json` — successful status record; SHA-256 `8f2dcccd848c141766a27885aa0ce313413514f863acf031b9486a9de40fc2c3`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/collection.json` — successful execution artifact; SHA-256 `335a7a103ef5365bd97b83f381565ca169c6a2f3b53fcc697f4eb7543e3f77d1`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/input.com` — successful execution artifact; SHA-256 `e1281cbfb7429fd467a035345e393f3d5bab437b6b412adc644f75b3886f4ce5`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/request.json` — successful execution artifact; SHA-256 `ec14d44d60880f6b030808639162caa7438443c0e44243ec9f013b78b124ed20`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/status.json` — successful status record; SHA-256 `d3d1ca0a3021237466f17578f7338d9524d3386fe04a83c354eca8245110d2cd`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/collection.json` — successful execution artifact; SHA-256 `afee7033ea262597db3054207223e280bcdc0ac55d9e50f369e9dce103ef6862`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/input.com` — successful execution artifact; SHA-256 `6fea0b2418e36c3bde92813eefe14c9b803c3e9568533c13d2473160f82d4b33`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/request.json` — successful execution artifact; SHA-256 `6483ace0514882447f45e2fc5d5332d20130d43a76fe321c467adfea573fab4c`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/status.json` — label=paper3a neutral DFT; submitted_at=2026-08-28T22:35:42.623437+00:00; software=gaussian; intent=optimization_frequency; route=#P B3LYP/6-311++G(2d,p) EmpiricalDispersion=GD3BJ Opt=(Tight,CalcFC,MaxCycles=120) Freq NoSymm Int=UltraFine SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/collection.json`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/fort.7`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/input.com`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/neutral_b3lyp.chk`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/request.json`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stderr.log`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/supervisor_spec.json`
2. `native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/status.json` — label=paper3a anion DFT; submitted_at=2026-08-28T22:35:42.639273+00:00; software=gaussian; intent=optimization_frequency; route=#P B3LYP/6-311++G(2d,p) EmpiricalDispersion=GD3BJ Opt=(Tight,CalcFC,MaxCycles=120) Freq NoSymm Int=UltraFine SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/anion_b3lyp.chk`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/collection.json`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/fort.7`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/input.com`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/request.json`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stderr.log`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log`
   - output: `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/supervisor_spec.json`

## Evaluator alignment

- Key-point IDs: `kp_pr_process_minima, kp_pr_process_identity, kp_pr_result_trend`
- Conclusion IDs: `con_pr_final`
- Scoring-rule IDs: `r1, r2, r3, r4`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r1` → reference `kp_pr_process_minima`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert comparison; evaluator_target_present=False
- rule `r2` → reference `kp_pr_process_identity`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert comparison; evaluator_target_present=False
- rule `r3` → reference `kp_pr_result_trend`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert comparison; evaluator_target_present=False
- rule `r4` → reference `con_pr_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].state` = `"neutral"`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].validated` = `true`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].imaginary_frequency_count` = `0`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].atom_mapping` = `"P=11; O1=12; O2=13; O3=14; B=21"`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].distances_A.P-O1` = `1.516778733237317`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].distances_A.P-O2` = `1.5793438823698276`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].distances_A.P-O3` = `1.5945705807536397`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].distances_A.O1-B` = `1.6955959118082942`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[0].validation_evidence` = `"docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log; normal termination, Opt+Freq, 87 frequencies"`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].state` = `"anion"`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].validated` = `true`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].imaginary_frequency_count` = `0`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].atom_mapping` = `"P=11; O1=12; O2=13; O3=14; B=18"`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].distances_A.P-O1` = `1.5580341173620045`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].distances_A.P-O2` = `1.6434685736204389`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].distances_A.P-O3` = `1.485185525098464`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].distances_A.O1-B` = `1.5791316656482448`
- rule `r1` / reference `kp_pr_process_minima` / field `$.states` / result path `$.states[1].validation_evidence` = `"docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log; normal termination, Opt+Freq, 75 frequencies"`
- rule `r1` / reference `kp_pr_process_minima` / field `$.status` / result path `$.status` = `"complete"`
- rule `r3` / reference `kp_pr_result_trend` / field `$.comparison` / result path `$.comparison` = `"Anion minus neutral differences (Å): P-O1=+0.041255, P-O2=+0.064125, P-O3=-0.109385, O1-B=-0.116464. The stated comparison is qualitative and scoped to the isolated models."`
- rule `r4` / reference `con_pr_final` / field `$.limitations` / result path `$.limitations` = `"The calculation omits Li+, solvent and crystal packing. The experimental boundary is labeled O2-B whereas the computational extraction uses O1-B; atom-label mapping must be kept explicit."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: experimental boundary input removed
- Files changed in that review: `agent_input/task.md, package_manifest.json, task_info.json`
- Files deleted in that review: `agent_input/data/inputs/experimental_crystal_boundary.json`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Independent topology-generated, unoptimized neutral and anion XYZ starters with charge, multiplicity and atom mapping; author endpoints are evaluator-private.
- `data/inputs/experimental_crystal_boundary.json` — crystal distances

Public input files and hashes:

- `agent_input/data/inputs/README.md` — SHA-256 `2c1acc1d9243e709b678d2b97c4935e785b9e46706e20f31b531ae97bce22ad4`; size=549 bytes; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/anion.xyz` — SHA-256 `c56774a24954b80385e06f50fe3313b5777844c3b31d2bfb326479a3e2ecf9a9`; size=1081 bytes; xyz_atom_count=27; xyz_comment=anion C9H13BO3P independent topology-only ETKDG starter; unoptimized; atom indices retained; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/experimental_crystal_boundary.json` — SHA-256 `12276ce67af6858c07be00f88db8948a6464c46beea5328cbec7176a229286a5`; size=2007 bytes; explicit_boundary_fields={"$.units": {"distance": "angstrom"}}
- `agent_input/data/inputs/neutral.xyz` — SHA-256 `e182b99d5199275920a7d0a50c661c1326e84e521a870560234f1375f682696a`; size=1238 bytes; xyz_atom_count=31; xyz_comment=neutral C10H16BO3P independent topology-only ETKDG starter; unoptimized; atom indices retained; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/starting_geometry_definition.json` — SHA-256 `c186b912cea9f594ca2d3b93264690ac6f2cd95dd7af1f0c53f9ff660d0750d5`; size=1081 bytes; explicit_boundary_fields={"$.states.anion.xyz.atom_count": 27, "$.states.anion.xyz.atom_map_ids": {"B": 18, "O1": 12, "O2": 13, "O3": 14, "P": 11}, "$.states.anion.xyz.charge": -1, "$.states.anion.xyz.formula": "C9H13BO3P", "$.states.anion.xyz.mapped_smiles": "[c:1]12[c:3]([c:6]([H:9])[c:2]([H:10])[c:5]([H:8])[c:4]1[H:7])[B-:18]([C:20]([H:21])([H:22])[H:23])([C:24]([H:25])([H:26])[H:27])[O:12][P+:11]2([O:13][C:15]([H:16])([H:17])[H:19])[O-:14]", "$.states.anion.xyz.multiplicity": 1, "$.states.neutral.xyz.atom_count": 31, "$.states.neutral.xyz.atom_map_ids": {"B": 21, "O1": 12, "O2": 13, "O3": 14, "P": 11}, "$.states.neutral.xyz.charge": 0, "$.states.neutral.xyz.formula": "C10H16BO3P", "$.states.neutral.xyz.mapped_smiles": "[c:1]12[c:3]([c:6]([H:9])[c:2]([H:10])[c:5]([H:8])[c:4]1[H:7])[B-:21]([C:24]([H:25])([H:26])[H:27])([C:28]([H:29])([H:30])[H:31])[O:12][P+:11]2([O:13][C:18]([H:19])([H:20])[H:23])[O:14][C:15]([H:16])([H:17])[H:22]", "$.states.neutral.xyz.multiplicity": 1}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_1/paper_3a22e838133b906d/verification_report.md` — verification record; SHA-256 `66169da4ea14dec31894aa211e5fb3253308caa8e2b77bfc79c0362026908333`
- `docs/verification/group_1/paper_3a22e838133b906d/report/results.json` — verification record; SHA-256 `05209a96cef5d430f4268f3b1833b9070188b264dbd261edd158497166b127d3`
- `docs/verification/group_1/paper_3a22e838133b906d/artifacts/author_gaussian_parsed.json` — referenced successful evidence; SHA-256 `86c84706621036eb96bb13e13c9d0d6f1c8bae64d9649758c8aef456f9e94a43`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_0882136fdd7743e3976a38e3b067f214/stdout.log` — referenced successful evidence; SHA-256 `6eef17edbe3a9c5c180a9fb7bb5d4895391e2b2551a2ff8e1892ea87ab506f41`
- `docs/verification/group_1/paper_3a22e838133b906d/native_workspace/outputs/execution_jobs/job_f187b8d5db8540c78d880295569b749a/stdout.log` — referenced successful evidence; SHA-256 `97dc91d677012d30d4465ac8701bc60578c001b2f52748db35e2830b0b822c09`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
