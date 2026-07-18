# ResearchChem Managed MCP Tools

This directory is organized for frequent tool addition, deletion, and modification.

## Management model

- One public MCP tool equals one file under `tools/`.
- Every file owns its metadata through `TOOL_SPEC`.
- `registry.py` automatically discovers `tools/*.py`; there is no central tool list to update.
- `tool_config.json` only controls enable/disable policy and server text.
- `tool_manager.py` provides list, validate, scaffold, enable, disable, archive, restore, and catalog commands.
- `server.py` contains no chemistry tool implementation.
- `config/mcp_profiles.yaml` groups tools into dependency-compatible MCP runtimes without
  changing the one-tool-one-file source layout.

## Dependency-isolated profiles

```bash
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py --continue-on-error
.toolbox_env/bin/python scripts/check_mcp_profile_envs.py --live-materials-project
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_003 \
  --mcp-profiles core,services --no-score
```

Adding a tool file also requires assigning it to exactly one profile in
`config/mcp_profiles.yaml`; profile validation rejects unknown, missing, or duplicate tool
assignments.

## Layout

```text
mcp_tools/
├── models.py                 ToolSpec metadata contract
├── tool_config.json          enable/disable policy only
├── registry.py               automatic discovery and validation
├── tool_manager.py           lifecycle management CLI
├── TOOL_CATALOG.md           generated catalog
├── server.py                 FastMCP server assembly/transport
├── settings.py               ChemGraph discovery
├── workspace.py              path confinement
├── tracing.py                results/traces/artifacts
├── adapters/                 runtime, HTTP, and software-registry helpers
├── archived_tools/           safely removed source files
└── tools/
    ├── calculator.py
    ├── run_ase.py
    ├── run_xtb.py
    ├── run_openmm.py
    ├── query_pubchem.py
    └── ...                   41 public tools total
```

## Common commands

From ResearchChemBench:

```bash
bash scripts/manage_mcp_tools.sh list
bash scripts/manage_mcp_tools.sh validate
bash scripts/manage_mcp_tools.sh catalog
```

Create a disabled scaffold:

```bash
bash scripts/manage_mcp_tools.sh scaffold my_tool \
  --description "Describe exactly what the tool does" \
  --category simulation \
  --backend "MySoftware" \
  --dependency my-software-python-package \
  --executable my-software-cli \
  --side-effect "writes calculation files"
```

After implementing and testing it:

```bash
bash scripts/manage_mcp_tools.sh enable my_tool
```

Temporarily take a tool offline:

```bash
bash scripts/manage_mcp_tools.sh disable my_tool
```

Safely remove and restore its file:

```bash
bash scripts/manage_mcp_tools.sh archive my_tool --yes
bash scripts/manage_mcp_tools.sh restore my_tool
```

Restored and newly scaffolded tools are disabled until explicitly enabled.

## Required tool-file contract

The filename must equal `TOOL_SPEC.name`:

```python
"""MCP tool: my_property."""

from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="my_property",
    description="Compute one documented molecular property.",
    category="property_prediction",
    version="1.0.0",
    backend="MySoftware",
    dependencies=("my-software-python-package",),
    tags=("molecule", "property"),
)


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def my_property(value: str) -> dict:
        def call() -> dict:
            # Validate input and call the real software/core function here.
            return {"value": value}

        return execute_traced(TOOL_SPEC.name, {"value": value}, call)
```

Validation enforces:

- lower-snake-case file/tool name;
- filename equals `TOOL_SPEC.name`;
- non-empty description, category, and version;
- exactly one unique public name;
- callable `register(mcp)`;
- exactly one registered MCP tool whose name matches `TOOL_SPEC.name`;
- successful metadata import for every discovered tool during `validate`;
- rejection of the generated `NotImplementedError` placeholder during `enable`.

## Enable/disable policy

The repository configuration explicitly allows only reviewed tools. Therefore,
a new manually added file is discovered but remains disabled until it is enabled:

The current file explicitly lists all 41 reviewed tools. A newly scaffolded or manually added tool remains disabled until it is added with `tool_manager enable`.

`"enabled_tools": ["*"]` is supported, but it also auto-enables future files
and is not recommended for routine development.

Environment overrides are useful for one run:

```bash
export RESEARCHCHEM_MCP_ENABLED_TOOLS=calculator,molecule_name_to_smiles
export RESEARCHCHEM_MCP_DISABLED_TOOLS=run_ase
```

## Adding many future software tools

For each software capability, create a separate file even when several tools use the same external package. Put reusable software-client/process helpers in a non-tool support package whose filename starts with `_` or outside `tools/`; automatic discovery ignores underscore-prefixed files.

Recommended separation:

```text
software adapter/client layer
        ↓
one MCP tool wrapper file
        ↓
ToolSpec + argument schema + workspace safety + tracing
```

Do not place multiple public `@mcp.tool` functions in one file.
Keep optional and heavy backend imports inside `register(mcp)` or the tool call,
so metadata discovery remains usable without every chemistry package installed.

## Verification

```bash
bash scripts/manage_mcp_tools.sh validate
python scripts/check_mcp_tools.py
python scripts/check_mcp_tools.py --smoke
python scripts/verify_toolbox.py
bash evaluation/mcp_tools/test_tools/run_tests.sh --live-network --status-report
pytest -q
```

## Packaging appendix

The directory remains independently installable, but packaging is secondary to tool management:

```bash
pip install .
python -m researchchem_mcp_tools.server
```

Agent configuration helpers remain available in `installer.py` and `install.sh`.
