# MiniChem Toolbox

MiniChem is a portable, Gaussian-centered subset of the ResearchChem chemistry toolbox for
ARCHE Case1-style molecular reaction-mechanism tasks. It keeps structure preparation, conformer
search, transition-state/path calculations, thermochemistry, selectivity analysis, and electronic
analysis while omitting materials, molecular dynamics, docking, and remote chemistry databases.

## Scientific Scope

The intended workflow is:

1. standardize a molecular structure and enumerate stereochemistry, tautomers, protonation states,
   or coordination isomers when required;
2. generate and cluster conformers with RDKit, Open Babel, CREST, and xTB;
3. optimize minima and transition states and run frequency/IRC calculations, primarily with Gaussian;
4. parse outputs and calculate thermochemistry, populations, selectivity, and reaction profiles;
5. inspect charges, bond orders, density surfaces, and wavefunction-derived quantities with Multiwfn.

This toolbox supports computational inputs that can be reconstructed from a paper and its supporting
information. It does not decide the scientifically correct functional, basis set, solvent model,
conformer set, transition-state guess, or standard-state correction for the Agent.

## Three Invocation Layers

MiniChem preserves the comprehensive toolbox's invocation model:

1. **Predefined Actions** provide typed, validated operations such as conformer generation, xTB or
   Gaussian energy/optimization, transition-state/path calculations, and thermochemistry.
2. **Native software calls** let an Agent author complete Gaussian, CREST, xTB, pysisyphus,
   GoodVibes, Open Babel, or Multiwfn inputs and submit an allowlisted command without a shell.
3. **Python program interface** lets an Agent write an auditable program using the installed RDKit,
   ASE, cclib, QCElemental, NumPy, SciPy, Sella, or other retained libraries in an isolated job.

The layers are peers. An Agent may combine them, and no layer silently chooses software or falls back
to a different scientific method.

## Included Software

| Software | Role |
|---|---|
| Gaussian 16 | Core DFT/HF calculation, optimization, Hessian/frequency, TS and IRC through native inputs; typed common Actions are also available |
| xTB | Low-cost energy, force, Hessian, optimization, charge, bond-order, and prescreening calculations |
| CREST | Conformer and rotamer exploration driven by xTB |
| RDKit | Standardization, 3D embedding, stereoisomer/tautomer enumeration, clustering, alignment, and graph operations |
| Open Babel | Molecular format conversion and alternative 3D preparation |
| pysisyphus | NEB/path, scan, TS, and IRC workflows, restricted to the retained xTB calculator in predefined Actions |
| Sella | Geometry and transition-state optimization with retained calculator backends |
| GoodVibes | Thermochemistry, quasi-harmonic corrections, ensembles, selectivity, and free-energy profiles |
| cclib / QCElemental | Quantum-output parsing and structured chemistry records |
| Multiwfn | Charges, bond orders, electron-density surfaces, and Agent-authored wavefunction analysis |

Gaussian is licensed software. Its cache may only be copied and used according to the applicable
license. MiniChem does not download or redistribute Gaussian.

## Portable Layout

All checked-in configuration paths are relative to this directory:

```text
minichem_toolbox/
├── .mini_software_cache/
│   ├── gaussian/
│   ├── multiwfn/
│   ├── runtimes/minichem/
│   └── runtime_packs/
├── .mini_model_cache/
│   └── all-MiniLM-L6-v2/
├── config/
├── mcp/
├── native_software_docs/
├── scripts/
├── src/minichem_toolbox/
└── tests/harnesses/
```

The default root is discovered from the copied toolbox itself. Optional relocation variables are:

- `MINICHEM_HOME`: override the toolbox root;
- `MINICHEM_ENV_ROOT`: override the directory containing the `minichem` runtime prefix;
- `MINICHEM_MODEL_CACHE`: override the local model cache;
- `MINICHEM_MCP_WORKSPACE`: set the current Agent task workspace.

## Models

Core calculations require no learned model. The optional semantic-search model is
`sentence-transformers/all-MiniLM-L6-v2`, downloaded from Hugging Face and placed at:

```text
.mini_model_cache/all-MiniLM-L6-v2/
```

Action and software-document embedding files are stored directly under `.mini_model_cache/`.
Remote Agent models such as `deepseek-v4-flash` are API models and are not stored locally.

## Installation and Migration

After copying the whole `minichem_toolbox` directory to another compatible Linux x86-64 host, run:

```bash
bash scripts/bootstrap.sh
```

The script uses an existing `.mini_software_cache/runtimes/minichem` prefix, an optional
`.mini_software_cache/runtime_packs/minichem.tar.gz`, or creates the environment from
`.mini_software_cache/environment.yml`. It then runs a catalog and backend health verification.

Cache provenance is recorded in `.mini_software_cache/manifest.json` and
`.mini_model_cache/manifest.json`. Regenerate both after changing a cache payload:

```bash
.mini_software_cache/runtimes/minichem/bin/python scripts/generate_cache_manifests.py
```

To prepare the optional relocatable runtime archive before moving the directory:

```bash
bash scripts/package_runtime.sh
```

Start the MCP server directly with:

```bash
bash scripts/start_mcp.sh --transport stdio --discovery-mode progressive
```

## Agent Harnesses

Each harness creates an isolated workspace under `tests/results/<cli>/`, including the prompt,
chat/event stream, stderr, MCP traces, tool outputs, generated chemistry files, and session state.

```bash
bash tests/harnesses/run_codex.sh
bash tests/harnesses/run_claude.sh
bash tests/harnesses/run_opencode.sh
```

The OpenCode harness defaults to `deepseek/deepseek-v4-flash`. Configure it without storing secrets:

```bash
export OPENAI_API_KEY=...
export MINICHEM_AGENT_BASE_URL=https://api.deepseek.com/v1
export MINICHEM_AGENT_MODEL=deepseek/deepseek-v4-flash
```

The harness may also read these variables from `config.local.env` in this directory or its parent.
That local file is ignored by Git.

## Verification

Fast verification:

```bash
.mini_software_cache/runtimes/minichem/bin/python scripts/verify_minichem.py
```

Focused tests:

```bash
.mini_software_cache/runtimes/minichem/bin/python -m pytest tests
```
