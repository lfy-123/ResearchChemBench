# Stage03 Targeted Fix and Retest (2026-08-10)

## Scope

This change keeps the current Stage03 workflow, one model call per paper, and the existing
microbatch scheduler. It addresses general extraction and validation defects without adding
paper-specific rules or changing later stages.

## Changes

1. Separated external-software recognition from toolbox availability.
   `external_software_aliases.json` supplies detection-only names. Final coverage still uses
   `software_aliases.json` and `toolbox_capabilities.json`, so recognizing Q-Chem or Molpro
   cannot make it available in the toolbox.
2. Recovered method evidence when GROBID emits section headings as ordinary paragraphs with an
   empty `section_path`. Relevant blocks from the main paper and SI now receive evidence space.
3. Preserved compact rule and Softcite candidates before generic evidence when bounding the
   prompt. The original 18 KB prompt and 9 KB evidence budgets were retained after a larger
   budget caused excessive output truncation.
4. Deterministic entity recovery no longer assigns `core_compute` by default. An entity omitted
   by the model is retained with `role=unknown`, which cannot silently pass coverage.
5. A named program can be attached to a workflow step only when that step cites local evidence
   for the program. A program named elsewhere in the paper cannot be transferred to an unnamed
   analysis step.
6. Training, simulation, molecular dynamics, microkinetic modeling, electronic-structure work,
   and similar core runtimes cannot be waived as unnamed task-specific Python post-processing.
7. `inventory_complete=false` now prevents `software_covered`, even when the named subset of the
   workflow is covered.
8. Removed the generic executable alias `pes` from KinBot recognition because it collides with
   the scientific term “potential energy surface”.

## Retest Input

- Upstream run: `data_pipeline/runs/v2_screening_2000_fresh_20260810`
- Reused Stage02 decisions and Stage01 GROBID documents; Stage00-02 were not rerun.
- Stage02 passed papers supplied to Stage03: 38
- Model: `Qwen3-30B-A3B-Instruct-2507`
- Final retest: `data_pipeline/runs/v2_stage03_retest_r20_20260810`
- Prompt/evidence limits: 18 KB / 9 KB

## Final Results

| Decision | Papers |
|---|---:|
| `software_covered` | 6 |
| `core_software_uncovered` | 22 |
| `software_inventory_unconfirmed` | 10 |
| `processing_failed` | 0 |

Seven papers required the existing compact truncation retry. No paper failed processing.

## Manual Audit of All Passed Papers

| Paper | Required software confirmed in evidence | Audit conclusion |
|---|---|---|
| Molecular Mechanism for Converting Carbon Dioxide Surrounding Water Microdroplets... | Gaussian 16, ORCA 5.0, CP2K | Correctly covered |
| Replica exchange molecular dynamics for Li-intercalation in graphite... | LAMMPS, Pymatgen | Correctly covered |
| Allyl-Allyl Coupling Promoted by Catalyst Systems with two Palladium Atoms... | Gaussian 16, ORCA, Multiwfn, CREST; VMD is visualization | Correctly covered |
| Finding Natural, Dense, and Stable Frustrated Lewis Pairs... | VASP, LOBSTER; Materials Project supplies structures | Correctly covered |
| Unraveling Alcohol Additive Effects on Hypervalent Iodine(III)-Catalyzed... | Gaussian 16, CREST, GoodVibes, Multiwfn | Correctly covered |
| Synthesis Landscapes for Ammonia Borane Chemical Vapor Deposition... | VASP | Correctly covered |

All six passed papers use only software present in the frozen toolbox snapshot for their named
required computation. No passed paper contains a confirmed toolbox-external required runtime.

## Conservative Holds and Known Residuals

The strict local-attribution check holds some papers that are probably executable with the
toolbox when the paper scopes one program over several later steps without repeating its name.
Examples include Gaussian calculations with explicit-solvent variants and CP2K AIMD analysis.
This is an accepted false-negative tradeoff for the current screening objective.

Some rejected model inventories still classify scientific methods as software, such as GPW or
PME. These cases currently produce conservative rejection rather than false coverage. They do
not justify more special-case rules at this stage. The final passed-set precision is adequate to
continue to Stage04 high-quality normalization.

## Verification

```text
345 passed, 8 subtests passed
```
