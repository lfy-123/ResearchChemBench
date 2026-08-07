# ResearchChem Three-Layer MCP Toolbox

This package is the transport layer for the task-independent three-layer chemistry toolbox.

## Benchmark policy

- The complete versioned Scientific/Data Action catalog is exposed to every task.
- Scientific Actions require an agent-selected `backend_id`; `auto` is invalid.
- The dispatcher executes exactly the submitted backend and never falls back.
- Dependency profiles isolate backend runtimes; they never filter public tools.
- Workflow recipes and old `run_*` software runners are not public tools.
- Predefined Actions are validated conveniences, not the capability boundary.
- Reviewed native commands execute exact Agent-authored argv/input files with no shell.
- Agent-authored `.py` files can run in one explicitly selected chemistry runtime.
- Native/program jobs are asynchronous and persist state, logs, resource use, and output hashes.

## Layout

```text
chemistry_toolbox/src/  core contracts, catalog, dispatcher, artifacts, backends
chemistry_toolbox/mcp/                       FastMCP binding, tracing, workspace integration
chemistry_toolbox/config/mcp_profiles.yaml   dependency-isolated backend runtimes
chemistry_toolbox/config/native_software_guides.yaml reviewed native invocation contracts
```

The pre-refactor repository-root paths (`researchchem_toolbox/`,
`evaluation/mcp_tools/`, and `config/`) have been removed. Use only the
canonical paths shown above.

The generated complete catalog is [TOOL_CATALOG.md](TOOL_CATALOG.md).

## Commands

```bash
.envs/researchchembench/bin/python -m chemistry_toolbox.mcp.tool_manager validate
.envs/researchchembench/bin/python -m chemistry_toolbox.mcp.tool_manager catalog
.envs/researchchembench/bin/python -m chemistry_toolbox.mcp.tool_manager missing
.envs/researchchembench/bin/python chemistry_toolbox/scripts/check_mcp_tools.py --smoke
.envs/researchchembench/bin/python chemistry_toolbox/scripts/verify_toolbox.py --smoke
```

To add a recurring stable capability, define or revise an `ActionSpec`, define a
`BackendSpec`, implement the backend-local handler, assign the backend to exactly
one runtime, and add a conformance test. A paper-specific or uncommon operation
does not require a new Action: use a reviewed native command or an Agent-authored
program. New executable software must have a BackendSpec executable plus a
reviewed invocation guide; do not add a software-named workflow or hidden recipe.
