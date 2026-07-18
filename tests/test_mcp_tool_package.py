import importlib.util
import ast
import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from evaluation.mcp_tools import installer
from evaluation.mcp_tools import registry, tool_manager
from evaluation.mcp_tools.installer import configure_opencode
from evaluation.mcp_tools.models import ToolSpec
from evaluation.mcp_tools.registry import (
    ToolRecord,
    ToolRegistryError,
    discovered_module_stems,
    tool_is_enabled,
)
from evaluation.mcp_tools.tools.run_ase import _sanitize_calculator
from evaluation.mcp_tools.workspace import workspace_root


def test_auto_discovery_has_one_self_describing_file_per_tool():
    package_root = Path(__file__).resolve().parents[1] / "evaluation" / "mcp_tools"
    names = discovered_module_stems()
    expected_current_tools = {
        "calculator",
        "extract_output_json",
        "molecule_name_to_smiles",
        "run_ase",
        "smiles_to_coordinate_file",
    }
    assert expected_current_tools.issubset(names)
    assert len(names) == len(set(names))
    for name in names:
        module_file = package_root / "tools" / f"{name}.py"
        tree = ast.parse(module_file.read_text(encoding="utf-8"))
        assigned = {
            target.id
            for node in tree.body
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        functions = {
            node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert "TOOL_SPEC" in assigned
        assert "register" in functions
        assert importlib.util.spec_from_file_location(name, module_file) is not None


def test_environment_can_disable_one_tool(monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_DISABLED_TOOLS", "calculator")
    assert not tool_is_enabled("calculator")
    assert tool_is_enabled("run_ase")


def test_environment_can_disable_all_tools_with_wildcard(monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_DISABLED_TOOLS", "*")
    assert not tool_is_enabled("calculator")
    assert not tool_is_enabled("run_ase")


def test_unknown_new_file_name_is_disabled_by_default():
    assert not tool_is_enabled("future_unreviewed_tool")


def test_all_tool_metadata_is_discoverable_without_loading_runtime_backends():
    records = registry.discover_tools(include_disabled=True, strict=False)
    assert records
    assert not [record.error for record in records if record.error]
    assert all(record.spec is not None for record in records)


def test_tool_spec_rejects_inconsistent_sequence_metadata():
    spec = ToolSpec(
        name="invalid_metadata",
        description="Invalid metadata example",
        category="test",
        dependencies=["not-a-tuple"],  # type: ignore[arg-type]
    )
    with pytest.raises(ValueError, match="must be a tuple"):
        spec.validate()


def test_run_ase_module_import_is_lazy(monkeypatch):
    monkeypatch.delenv("CHEMGRAPH_ROOT", raising=False)
    module = importlib.import_module("evaluation.mcp_tools.tools.run_ase")
    assert module.TOOL_SPEC.name == "run_ase"


def test_run_ase_confines_calculator_commands_directories_and_models(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "tool_logs").mkdir()
    (tmp_path / "data").mkdir()
    model = tmp_path / "data" / "model.pt"
    model.write_bytes(b"model")

    with pytest.raises(ValueError, match="NWChem commands"):
        _sanitize_calculator(
            {"calculator_type": "nwchem", "command": "sh untrusted.sh"}
        )
    with pytest.raises(ValueError, match="escapes"):
        _sanitize_calculator(
            {"calculator_type": "orca", "directory": "../outside"}
        )
    with pytest.raises(ValueError, match="workspace"):
        _sanitize_calculator(
            {"calculator_type": "mace_mp", "model": "/tmp/untrusted.pt"}
        )

    safe_nwchem = _sanitize_calculator(
        {"calculator_type": "nwchem", "directory": ".", "command": None}
    )
    assert Path(safe_nwchem["directory"]).is_relative_to(tmp_path)
    safe_mace = _sanitize_calculator(
        {"calculator_type": "mace_mp", "model": "data/model.pt"}
    )
    assert safe_mace["model"] == str(model)


def test_workspace_defaults_to_server_cwd(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("RESEARCHCHEM_MCP_WORKSPACE", raising=False)
    monkeypatch.delenv("RESEARCHCHEMBENCH_WORKSPACE", raising=False)
    monkeypatch.chdir(tmp_path)
    assert workspace_root() == tmp_path.resolve()


def test_opencode_project_installer_preserves_existing_config(tmp_path: Path):
    config_path = tmp_path / "opencode.json"
    config_path.write_text(json.dumps({"model": "provider/model"}), encoding="utf-8")
    configure_opencode(
        name="researchchem-tools",
        command=["/venv/bin/python", "-m", "researchchem_mcp_tools.server"],
        environment={"CHEMGRAPH_ROOT": "/opt/ChemGraph"},
        scope="project",
        project_dir=tmp_path,
        uninstall=False,
        dry_run=False,
    )
    config = json.loads(config_path.read_text())
    assert config["model"] == "provider/model"
    server = config["mcp"]["researchchem-tools"]
    assert server["type"] == "local"
    assert server["command"][-1] == "researchchem_mcp_tools.server"
    assert server["environment"]["CHEMGRAPH_ROOT"] == "/opt/ChemGraph"
    assert config_path.with_suffix(".json.researchchem.bak").is_file()


def test_claude_installer_puts_name_before_variadic_env(monkeypatch):
    commands = []

    def capture(command, *, dry_run, ignore_error=False):
        commands.append(command)

    monkeypatch.setattr(installer, "_run", capture)
    installer.configure_claude(
        name="researchchem-tools",
        command=["python", "-m", "researchchem_mcp_tools.server"],
        environment={"CHEMGRAPH_ROOT": "/opt/ChemGraph", "PYTHONUNBUFFERED": "1"},
        scope="project",
        uninstall=False,
        dry_run=False,
    )
    add = commands[1]
    assert add[:7] == [
        "claude",
        "mcp",
        "add",
        "--scope",
        "project",
        "researchchem-tools",
        "--env",
    ]
    assert add.index("researchchem-tools") < add.index("CHEMGRAPH_ROOT=/opt/ChemGraph")


def test_manager_scaffold_enable_disable_archive_restore(tmp_path: Path, monkeypatch):
    tools_dir = tmp_path / "tools"
    archived_dir = tmp_path / "archived_tools"
    tools_dir.mkdir()
    config_path = tmp_path / "tool_config.json"
    config_path.write_text(
        json.dumps(
            {
                "server_name": "test",
                "server_instructions": "test",
                "enabled_tools": [],
                "disabled_tools": [],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(registry, "TOOLS_DIR", tools_dir)
    monkeypatch.setattr(registry, "TOOL_CONFIG_PATH", config_path)
    monkeypatch.setattr(tool_manager, "TOOLS_DIR", tools_dir)
    monkeypatch.setattr(tool_manager, "TOOL_CONFIG_PATH", config_path)
    monkeypatch.setattr(tool_manager, "ARCHIVED_TOOLS_DIR", archived_dir)

    created = tool_manager.scaffold_tool(
        "future_tool",
        description="Future software adapter",
        category="simulation",
        backend="FutureSoftware",
        dependencies=("future-python",),
        tags=("simulation",),
        requires_network=True,
        executables=("future-cli",),
        side_effects=("writes output file",),
    )
    assert created.is_file()
    source = created.read_text(encoding="utf-8")
    assert "dependencies=('future-python',)" in source
    assert "requires_network=True" in source
    assert "executables=('future-cli',)" in source
    config = json.loads(config_path.read_text())
    assert "future_tool" not in config["enabled_tools"]
    assert "future_tool" in config["disabled_tools"]

    archived = tool_manager.archive_tool("future_tool", confirmed=True)
    assert archived.is_file() and not created.exists()
    config = json.loads(config_path.read_text())
    assert "future_tool" not in config["enabled_tools"]
    assert "future_tool" not in config["disabled_tools"]

    restored = tool_manager.restore_tool("future_tool")
    assert restored.is_file() and not archived.exists()
    config = json.loads(config_path.read_text())
    assert "future_tool" not in config["enabled_tools"]
    assert "future_tool" in config["disabled_tools"]

    with pytest.raises(ValueError, match="NotImplementedError"):
        tool_manager.set_enabled("future_tool", enabled=True)
    created.write_text(
        source.replace(
            'raise NotImplementedError("Implement future_tool before enabling it")',
            'return {"value": value}',
        ),
        encoding="utf-8",
    )

    tool_manager.set_enabled("future_tool", enabled=True)
    config = json.loads(config_path.read_text())
    assert "future_tool" in config["enabled_tools"]
    assert "future_tool" not in config["disabled_tools"]

    tool_manager.set_enabled("future_tool", enabled=False)
    config = json.loads(config_path.read_text())
    assert "future_tool" not in config["enabled_tools"]
    assert "future_tool" in config["disabled_tools"]


def test_manager_rolls_back_file_moves_when_config_write_fails(
    tmp_path: Path, monkeypatch
):
    tools_dir = tmp_path / "tools"
    archived_dir = tmp_path / "archived_tools"
    tools_dir.mkdir()
    archived_dir.mkdir()
    config_path = tmp_path / "tool_config.json"
    config_path.write_text(
        json.dumps(
            {
                "enabled_tools": ["rollback_tool"],
                "disabled_tools": [],
            }
        ),
        encoding="utf-8",
    )
    active = tools_dir / "rollback_tool.py"
    archived = archived_dir / active.name
    active.write_text("# active\n", encoding="utf-8")
    monkeypatch.setattr(registry, "TOOLS_DIR", tools_dir)
    monkeypatch.setattr(registry, "TOOL_CONFIG_PATH", config_path)
    monkeypatch.setattr(tool_manager, "TOOLS_DIR", tools_dir)
    monkeypatch.setattr(tool_manager, "TOOL_CONFIG_PATH", config_path)
    monkeypatch.setattr(tool_manager, "ARCHIVED_TOOLS_DIR", archived_dir)

    def fail_save(_config):
        raise OSError("simulated config write failure")

    monkeypatch.setattr(tool_manager, "_save_config", fail_save)
    with pytest.raises(OSError, match="simulated"):
        tool_manager.archive_tool("rollback_tool", confirmed=True)
    assert active.is_file() and not archived.exists()

    active.replace(archived)
    with pytest.raises(OSError, match="simulated"):
        tool_manager.restore_tool("rollback_tool")
    assert archived.is_file() and not active.exists()


def test_registry_rejects_multiple_public_tools_from_one_file(monkeypatch, tmp_path: Path):
    spec = ToolSpec(
        name="single_tool",
        description="Must be the only public tool in its file.",
        category="test",
    )

    def register(mcp):
        @mcp.tool(name="single_tool")
        def first():
            return 1

        @mcp.tool(name="single_tool")
        def second():
            return 2

    record = ToolRecord(
        module_stem="single_tool",
        module_name="fake.single_tool",
        path=tmp_path / "single_tool.py",
        enabled=True,
        spec=spec,
        module=SimpleNamespace(register=register),
    )
    monkeypatch.setattr(registry, "discover_tools", lambda **_: [record])

    class FakeMCP:
        def tool(self, *args, **kwargs):
            if args and callable(args[0]):
                return args[0]
            return lambda function: function

    with pytest.raises(ToolRegistryError, match="more than one"):
        registry.register_all_tools(FakeMCP())
