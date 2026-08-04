# MiniChem Three-Layer MCP Interface

This directory exposes the focused MiniChem catalog over MCP. The public surface has three peer
layers:

1. typed predefined Actions;
2. allowlisted native software execution;
3. isolated Agent-authored Python programs.

Scientific Actions require an explicit backend. Native and Python jobs are asynchronous and retain
their requests, status, logs, resource use, hashes, and collected artifacts in the task workspace.
The dispatcher does not silently choose a scientific method or switch software after failure.

The generated focused catalog is [TOOL_CATALOG.md](TOOL_CATALOG.md). From the toolbox root:

```bash
.envs/minichem/bin/python -m minichem_mcp_tools.tool_manager validate
.envs/minichem/bin/python -m minichem_mcp_tools.tool_manager catalog
.envs/minichem/bin/python -m minichem_mcp_tools.tool_manager missing
bash scripts/start_mcp.sh --transport stdio --discovery-mode progressive
```

Recurring, typed capabilities belong in an `ActionSpec` and backend implementation. Less common
paper-specific operations should use a reviewed native command or an auditable Python program.
