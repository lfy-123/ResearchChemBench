# ResearchChem chemistry toolbox

This directory is the canonical home of the composable chemistry toolbox.

```text
chemistry_toolbox/
├── src/researchchem_toolbox/   protocol-independent Action and Backend core
├── mcp/                        FastMCP transport and Agent integration
├── config/                     runtime, software, and scientific-resource manifests
├── scripts/                    setup, audit, smoke, and report commands
├── tests/                      chemistry-toolbox tests
└── docs/                       architecture, capability, and audit documentation
```

The repository-root `researchchem_toolbox`, `evaluation/mcp_tools`, and `config`
paths are compatibility links. New code and documentation should use the
canonical paths under this directory.

Large runtime assets remain outside the source tree:

- `../.software_cache`: installed scientific programs and local documentation
- `../.model_cache`: model weights
- `../.tool_envs`: isolated backend runtimes
- `../.toolbox_env`: development and audit environment

The completed migration and verification record is available in
[`docs/CHEMISTRY_TOOLBOX_LAYOUT_REFACTOR_20260721.md`](docs/CHEMISTRY_TOOLBOX_LAYOUT_REFACTOR_20260721.md).
