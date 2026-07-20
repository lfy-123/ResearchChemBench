# ResearchChem Atomic MCP Toolbox

This package is the transport layer for the task-independent atomic chemistry toolbox.

## Benchmark policy

- All 40 Scientific Actions and 5 Data Actions are exposed to every task.
- Scientific Actions require an agent-selected `backend_id`; `auto` is invalid.
- The dispatcher executes exactly the submitted backend and never falls back.
- Dependency profiles isolate backend runtimes; they never filter public tools.
- Workflow recipes and old `run_*` software runners are not public tools.

## Layout

```text
researchchem_toolbox/       core contracts, catalog, dispatcher, artifacts, backends
evaluation/mcp_tools/       FastMCP binding, tracing, workspace integration
config/mcp_profiles.yaml    dependency-isolated backend runtimes
```

The generated complete catalog is [TOOL_CATALOG.md](TOOL_CATALOG.md).

## Commands

```bash
.toolbox_env/bin/python -m evaluation.mcp_tools.tool_manager validate
.toolbox_env/bin/python -m evaluation.mcp_tools.tool_manager catalog
.toolbox_env/bin/python -m evaluation.mcp_tools.tool_manager missing
.toolbox_env/bin/python scripts/check_mcp_tools.py --smoke
.toolbox_env/bin/python scripts/verify_toolbox.py --smoke
```

To add a capability, define or revise an `ActionSpec`, define a `BackendSpec`, implement the backend-local handler, assign the backend to exactly one runtime, and add a conformance test. Do not add a software-named runner or a hidden multi-step workflow.
