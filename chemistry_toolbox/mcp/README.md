# ResearchChem Atomic MCP Toolbox

This package is the transport layer for the task-independent atomic chemistry toolbox.

## Benchmark policy

- The complete versioned Scientific/Data Action catalog is exposed to every task.
- Scientific Actions require an agent-selected `backend_id`; `auto` is invalid.
- The dispatcher executes exactly the submitted backend and never falls back.
- Dependency profiles isolate backend runtimes; they never filter public tools.
- Workflow recipes and old `run_*` software runners are not public tools.

## Layout

```text
chemistry_toolbox/src/researchchem_toolbox/  core contracts, catalog, dispatcher, artifacts, backends
chemistry_toolbox/mcp/                       FastMCP binding, tracing, workspace integration
chemistry_toolbox/config/mcp_profiles.yaml   dependency-isolated backend runtimes
```

The pre-refactor repository-root paths (`researchchem_toolbox/`,
`evaluation/mcp_tools/`, and `config/`) have been removed. Use only the
canonical paths shown above.

The generated complete catalog is [TOOL_CATALOG.md](TOOL_CATALOG.md).

## Commands

```bash
.toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager validate
.toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager catalog
.toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager missing
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_tools.py --smoke
.toolbox_env/bin/python chemistry_toolbox/scripts/verify_toolbox.py --smoke
```

To add a capability, define or revise an `ActionSpec`, define a `BackendSpec`, implement the backend-local handler, assign the backend to exactly one runtime, and add a conformance test. Do not add a software-named runner or a hidden multi-step workflow.
