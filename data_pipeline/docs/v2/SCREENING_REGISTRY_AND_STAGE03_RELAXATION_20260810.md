# Unified screening registry and Stage03 relaxation

Date: 2026-08-10

## Scope

This change has two goals:

1. retain the complete screening history of every copied paper even after its local PDF/SI bundle is deleted;
2. make Stage03 a recall-oriented preliminary toolbox gate while retaining deployed-model review.

The scientific stage order and the Stage02 computational-content rule are unchanged.

## Unified screening registry

The implementation is in `data_pipeline/src/registry`. The authoritative store is SQLite and the human-readable export is JSONL.

Default locations, resolved relative to the v2 configuration file, are:

- `registry/paper_screening_registry.sqlite`
- `registry/exports/paper_screening_registry.jsonl`

The SQLite database contains:

- `runs`: run identity, configuration hash, workspace and status;
- `papers`: canonical paper metadata;
- `paper_sources`: remote main/SI paths, local Stage00 directory and asset state;
- `stage_results`: the complete result JSON for every paper and stage;
- `software_mentions`: Stage03 software entities, normalized identifiers, roles and catalog presence;
- `artifact_events`: deletion result, reason, local path and bytes released.

The JSONL export contains one record per run and paper, including all source paths and all stage results. SQLite remains durable during a run; JSONL is refreshed when the run finishes.

### Deletion boundary

Only a failed result from Stage00, Stage01, Stage02 or Stage03 can prune a paper bundle. Stage04 through Stage07 are always recorded with pruning disabled.

Deletion uses this order:

1. write the complete stage result and software inventory;
2. commit the record and mark the source bundle `delete_pending`;
3. validate that the target is exactly `stage_00_remote_corpus/corpus/<source_paper_id>`;
4. delete the complete paper directory, including main PDF and all SI;
5. record `deleted` or `delete_failed` in `artifact_events`.

The implementation refuses symlink targets or paths outside the Stage00 corpus. If the process stops after step 2, the screening result is still durable and the file is not silently lost.

Configuration:

```json
{
  "registry": {
    "enabled": true,
    "database": "registry/paper_screening_registry.sqlite",
    "export_jsonl": "registry/exports/paper_screening_registry.jsonl",
    "prune_rejected_stage00_assets": true
  }
}
```

## Relaxed Stage03 policy

Stage03 still calls the deployed screening model and still builds a structured workflow/software inventory. Deterministic code then maps actual software mentions to the frozen toolbox catalog.

Stage03 now forwards four decisions:

- `software_covered`: complete inventory and covered required software;
- `software_coverage_probable`: a covered named engine exists but the inventory is incomplete;
- `mixed_workflow_candidate`: at least one independent workflow is covered and another is not;
- `software_inventory_unconfirmed`: software implementation is unnamed or evidence is incomplete.

It rejects only:

- `core_software_uncovered`: no independent covered workflow and a required named program is absent;
- `cost_exceeds_budget`: explicit resource evidence exceeds the configured budget;
- `processing_failed`: the paper could not be reviewed safely.

This stage no longer claims that every forwarded paper is toolbox-covered. Unconfirmed and mixed papers are retained for the stronger Stage05 suitability review, which is the intended precision gate.

The normalizer also handles general model-output defects without paper-specific rules:

- role values accidentally placed in `entity_type`;
- modules explicitly described as bundled inside a named host program;
- scientific methods and generic computation phrases such as `MD simulations` reported as programs;
- malformed boolean/null fields.

## 38-paper regression

Input: the 38 Stage02 passes from `v2_screening_2000_fresh_20260810`.

Model: `Qwen3-30B-A3B-Instruct-2507`, using the completed deployed-model cache. The server stopped after the original calls completed, so the final validation replay required no worker restart and no new model calls.

Final result:

| Decision | Papers | Forwarded |
|---|---:|---:|
| `software_covered` | 4 | 4 |
| `software_coverage_probable` | 1 | 1 |
| `mixed_workflow_candidate` | 3 | 3 |
| `software_inventory_unconfirmed` | 14 | 14 |
| `core_software_uncovered` | 16 | 0 |
| `processing_failed` | 0 | 0 |
| **Total** | **38** | **22** |

### Manual paper-by-paper audit

| Paper (short title) | Result | Manual Stage03 assessment |
|---|---|---|
| MCR methane bioconversion | unconfirmed | Correct: MD is described but its engine is unnamed; `MD simulations` is no longer treated as a program. |
| Alloy catalyst surface-atom knockout | unconfirmed | Correct: theoretical calculation is present but no implementation is named. |
| Mo2C nitrogen reduction | uncovered | Correct: VASP is covered but required VASPsol is absent. |
| TMD nanoribbon/nanowire | uncovered | Correct: CALYPSO and QSTEM are absent. |
| Interfacial-water rotation | mixed | Correct: CP2K/GROMACS workflow is covered; n2p2 workflow is not. |
| CO2 microdroplet mechanism | covered | Correct: Gaussian, ORCA and CP2K are present. |
| Doped BCN photocatalysis | unconfirmed | Conservative forward: VASP/VASPKIT are present; one implementation remains unresolved. |
| Lithium nanochains | uncovered | Correct: required TRAVIS/fftool are absent. |
| CatTSunami | uncovered | Conclusion is appropriate because its specialized ML workflow is absent; the model-versus-code entity boundary remains an audit caveat. |
| Glycine receptor activation | uncovered | Correct: core Molaris-XG and required HOLE are absent. |
| DHP diradicals | unconfirmed | Conservative forward: Gaussian is present but workflow binding is incomplete. |
| IMPRESSION generation 2 | uncovered | Correct: required IMPRESSION implementation is absent. |
| Chlorination of EO catalysts | uncovered | Correct: DMol3/Materials Studio is absent. |
| Electron-density fidelity witness | mixed | Correct: PySCF/Critic2 workflow is covered; Qiskit workflow is not. |
| Ethylene tetramerization | mixed | Correct: CREST/Gaussian workflow is covered; Q-Chem EDA is not. |
| Li intercalation REMD | covered | Correct: LAMMPS and Pymatgen are present. |
| Glucose oxidation catalyst | unconfirmed | Conservative forward: VASP is present; one workflow step is unresolved. |
| Supported-gold descriptor design | probable | Correct: Quantum ESPRESSO/ASE/VASP are present; post-processing inventory is incomplete. |
| Molecular qubits | unconfirmed | Correct forward: Gaussian/OpenMolcas are present and SINGLE_ANISO is a bundled OpenMolcas module. |
| Charged water channels | uncovered | Correct: CHARMM-GUI/Discovery Studio preprocessing is absent. |
| GABAB receptor activation | uncovered | Correct: required CHARMM-GUI is absent. |
| Au/Co3O4 glucose sensor | unconfirmed | Correct forward: CP2K is present; generic GPW method is no longer a program. |
| Pd allyl coupling | covered | Correct: Gaussian, ORCA, Multiwfn, CREST and xTB are present. |
| Vanadium-oxide vacancies | unconfirmed | Conservative forward: VASP/LOBSTER/VASPKIT/VESTA are present; one step is unresolved. |
| Haloacetate electron density | uncovered | Correct: required NBO/refnx/DDEC6 components are absent. |
| Tetrazine reactions | unconfirmed | Conservative forward: Gaussian/CREST/GoodVibes are present; one step is unresolved. |
| Pd/In2O3 coupling catalyst | uncovered | Correct: Materials Studio is absent. |
| Surface frustrated Lewis pairs | covered | Core VASP/LOBSTER workflow is covered; a Materials Project role error is non-blocking and should be rechecked downstream. |
| Methylamine electrosynthesis | unconfirmed | Conservative forward: VASP is present; microkinetic implementation is unresolved. |
| Hypervalent iodine catalysis | unconfirmed | Conservative forward: Gaussian/GoodVibes/CREST/Multiwfn are present; one step is unresolved. |
| Air/ice interface | uncovered | Correct: i-PI, MBX/MB-pol and GenIce are absent. |
| Ammonia-borane CVD | unconfirmed | Conservative forward: VASP is present; workflow binding is incomplete. |
| PtSn4 surface states | uncovered | Correct: required GOCIA/custom STM code is absent. |
| Standard hydrogen electrode | unconfirmed | Conservative forward: VASP is present; MLFF/free-energy implementation is incomplete. |
| ML molecular mechanics force fields | uncovered | Correct: core Espaloma and additional preparation stack are absent. |
| Ti/SiO2 epoxidation kinetics | uncovered | Correct: Q-Chem and MATLAB are absent. |
| Spin-state relaxation | unconfirmed | Correct: simulations/in-house implementation are unnamed. |
| Xylene separation membranes | uncovered | Correct: COMSOL workflow is absent even though GROMACS is present. |

The hard-reject set has high precision in this sample: every rejected paper has a defensible missing required implementation. The forward set intentionally contains 14 unresolved cases; these are retained to reduce false negatives and must not be reported as confirmed toolbox coverage.

## Validation

- Data-pipeline v2 and registry tests: 188 passed.
- Full repository collection in the unified data-pipeline environment is blocked by optional dependencies not installed in that environment (`flask` and `fastmcp`).
- Ruff and whitespace validation passed for all changed Python/configuration files.

## Output paths

- Regression decisions: `data_pipeline/runs/v2_stage03_relaxed_regression_20260810/stage_03_toolbox_resource_gate/decisions.jsonl`
- Regression summary: `data_pipeline/runs/v2_stage03_relaxed_regression_20260810/stage_03_toolbox_resource_gate/stage_summary.json`
- Processing errors: `data_pipeline/runs/v2_stage03_relaxed_regression_20260810/stage_03_toolbox_resource_gate/processing_errors.jsonl`
