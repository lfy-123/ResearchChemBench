# ResearchChem three-layer chemistry toolbox

This directory is the canonical home of the composable chemistry toolbox.

The MCP surface has three peer execution layers:

1. all 101 predefined Scientific/Data Actions for validated common operations;
2. reviewed software-native commands for Agent-authored input decks when no Action fits;
3. Agent-authored Python programs in explicitly selected chemistry runtimes.

No layer selects a workflow, software, method, or scientific parameter for the
Agent, and there is no automatic fallback. See
[`docs/CHEMISTRY_TOOLBOX_THREE_LAYER_ARCHITECTURE.md`](docs/CHEMISTRY_TOOLBOX_THREE_LAYER_ARCHITECTURE.md)
for the complete execution and benchmark contract.

```text
chemistry_toolbox/
├── src/   protocol-independent Action and Backend core
├── mcp/                        FastMCP transport and Agent integration
├── config/                     versioned runtime, software, and resource manifests
├── environment/                reproducible environment specifications and locks
├── software_management/        managed software-cache installation and migration
├── native_software_docs/       generated, Agent-searchable native software manuals
├── evidence/                   versioned smoke and failure-replay evidence
├── scripts/                    setup, audit, smoke, and report commands
├── tests/                      chemistry-toolbox tests
├── examples/                   small analysis and native-integration examples
├── patches/                    reviewed upstream compatibility patches
└── docs/                       architecture, capability, and audit documentation
```

Run the focused toolbox regression suite with:

```bash
bash chemistry_toolbox/scripts/run_toolbox_tests.sh
```

`config/native_software_guides.yaml` is the versioned, machine-readable source
for exact native command syntax, input mode, required files, output behavior,
and examples. It is validated against BackendSpec executables and explicitly
configured runtime-only commands.

The pre-refactor repository-root implementations and compatibility links were
removed. Source code, configuration, scripts, tests, and documentation now have
one canonical location under this directory.

Large runtime assets remain outside the source tree:

- `../.software_cache`: installed scientific programs and local documentation
- `../.model_cache`: model weights
- `../.envs/researchchembench`: framework, development, and audit environment
- `../.envs/*`: seven consolidated backend runtime environments

The completed migration and verification record is available in
[`docs/CHEMISTRY_TOOLBOX_LAYOUT_REFACTOR_20260721.md`](docs/CHEMISTRY_TOOLBOX_LAYOUT_REFACTOR_20260721.md).
The complete 233-pair Action/Backend audit is available in
[`docs/ACTION_BACKEND_COMPLETE_AUDIT_20260721.md`](docs/ACTION_BACKEND_COMPLETE_AUDIT_20260721.md).
The follow-up repair and PubChem connectivity report is available in
[`docs/ACTION_BACKEND_REPAIR_REPORT_20260721.md`](docs/ACTION_BACKEND_REPAIR_REPORT_20260721.md).

Exact `linux-64` environment locks and the automatic migration/bootstrap
workflow are documented in
[`docs/CHEMISTRY_TOOLBOX_PORTABLE_BOOTSTRAP.md`](docs/CHEMISTRY_TOOLBOX_PORTABLE_BOOTSTRAP.md).
