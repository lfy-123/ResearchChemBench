#!/usr/bin/env python3
"""Run real bounded toolbox probes and write JSON/Markdown status reports."""

from __future__ import annotations

import importlib
import json
import os
import shutil
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from evaluation.mcp_tools.adapters.runtime import backend_status, module_version
from evaluation.mcp_tools.adapters.toolbox_registry import software_entries
from evaluation.mcp_tools.registry import discover_tools


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "TOOLBOX_STATUS.md"
JSON_PATH = ROOT / "docs" / "TOOLBOX_STATUS.json"


def _prepare_path() -> None:
    environment_bin = Path(sys.executable).resolve().parent
    os.environ["PATH"] = str(environment_bin) + os.pathsep + os.environ.get("PATH", "")


def _xyz(workspace: Path) -> str:
    path = workspace / "data" / "water.xyz"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "3\nwater\nO 0.000000 0.000000 0.000000\nH 0.758602 0.000000 0.504284\nH -0.758602 0.000000 0.504284\n",
        encoding="utf-8",
    )
    return "data/water.xyz"


def _pdb(workspace: Path) -> str:
    path = workspace / "data" / "water.pdb"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "HETATM    1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O  \n"
        "HETATM    2  H1  HOH A   1       0.758   0.000   0.504  1.00  0.00           H  \n"
        "HETATM    3  H2  HOH A   1      -0.758   0.000   0.504  1.00  0.00           H  \n"
        "TER\nEND\n",
        encoding="utf-8",
    )
    return "data/water.pdb"


def _periodic_structure(workspace: Path) -> str:
    path = workspace / "data" / "silicon.vasp"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "Si\n1.0\n5.43 0 0\n0 5.43 0\n0 0 5.43\nSi\n1\nDirect\n0 0 0\n",
        encoding="utf-8",
    )
    return "data/silicon.vasp"


def _result_status(result: Any) -> tuple[str, str]:
    if not isinstance(result, dict):
        return "failed", f"Tool returned {type(result).__name__}, not a structured object"
    status = str(result.get("status", "success"))
    if status in {"success", "available"}:
        return "working", "Minimal functional smoke test succeeded"
    if status in {"unavailable", "unknown"}:
        return "not_configured", str(result.get("reason") or result.get("manual_action") or status)
    return "failed", str(result.get("reason") or result.get("stderr_preview") or status)


def _json_safe(value: Any) -> Any:
    """Normalize backend metadata such as timedelta, Path, and NumPy values."""

    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "tolist"):
        return _json_safe(value.tolist())
    if hasattr(value, "model_dump"):
        return _json_safe(value.model_dump(mode="json"))
    return str(value)


def _call_core(name: str, workspace: Path) -> Any:
    module = importlib.import_module(f"evaluation.mcp_tools.tools.{name}")
    core = getattr(module, f"{name}_core")
    xyz = _xyz(workspace)
    pdb = _pdb(workspace)
    periodic = _periodic_structure(workspace)
    dummy = workspace / "data" / "input.inp"
    dummy.write_text("test input\n", encoding="utf-8")

    cases: dict[str, Callable[[], Any]] = {
        "list_toolbox_capabilities": lambda: core(),
        "check_backend_availability": lambda: core("RDKit"),
        "standardize_molecule": lambda: core("CCO"),
        "convert_structure": lambda: core(xyz, "outputs/water_copy.xyz"),
        "generate_3d_structure": lambda: core("O", "outputs/water.sdf", 2025),
        "generate_conformers_rdkit": lambda: core("CCO", "outputs/conformers.sdf", 3, 2025),
        "query_pubchem": lambda: core("water", "name", 1),
        "query_rcsb_pdb": lambda: core("1CRN"),
        "query_catalysis_hub": lambda: core("CO", "CO2", 1),
        "query_materials_project": lambda: core(material_id="mp-149", max_records=1),
        "run_reaction_kinetics": lambda: core(["A", "B"], [1.0, 0.0], [[1, 0]], [[0, 1]], [1.0], 1.0, 5),
        "run_pyscf": lambda: core("H 0 0 0; H 0 0 0.74", output_file="outputs/pyscf.json"),
        "run_psi4": lambda: core("0 1\nH 0 0 0\nH 0 0 0.74\nunits angstrom", output_file="outputs/psi4.json"),
        "prepare_md_system": lambda: core(pdb, "outputs/prepared.pdb"),
        "run_openmm": lambda: core(pdb, force_fields=["tip3p.xml"], steps=0),
        "analyze_md_trajectory": lambda: core(pdb, max_frames=1),
        "run_cantera": lambda: core("H2:2,O2:1,N2:3.76", temperature_kelvin=1000.0),
        "run_mlip": lambda: core(periodic, "chgnet", device="cpu", allow_model_download=True),
        "run_xtb": lambda: core(xyz, output_directory="outputs/xtb", timeout_seconds=180),
        "generate_conformers_crest": lambda: core(xyz, output_directory="outputs/crest", timeout_seconds=180),
        "run_phonopy": lambda: core(periodic, output_directory="outputs/phonopy", timeout_seconds=120),
    }
    if name == "analyze_wavefunction":
        from evaluation.mcp_tools.tools.run_xtb import run_xtb_core

        xtb_result = run_xtb_core(
            xyz,
            output_directory="outputs/analyze_wavefunction_xtb",
            timeout_seconds=180,
        )
        if xtb_result.get("status") != "success":
            return xtb_result
        return core("outputs/analyze_wavefunction_xtb/stdout.log")
    if name == "validate_computation":
        result_file = workspace / "outputs" / "validation_input.json"
        result_file.write_text(json.dumps({"status": "success", "energy": -1.0}), encoding="utf-8")
        return core("outputs/validation_input.json", ["energy"], [])
    if name in cases:
        return cases[name]()
    return {
        "status": "unavailable",
        "reason": "Adapter is registered, but no safe automated real smoke input is defined",
        "manual_action": "Run a representative licensed/configured backend input manually.",
    }


def _probe_original(name: str, workspace: Path) -> Any:
    module = importlib.import_module(f"evaluation.mcp_tools.tools.{name}")

    class Capture:
        def __init__(self):
            self.function = None

        def tool(self, *args, **kwargs):
            def decorator(function):
                self.function = function
                return function
            if args and callable(args[0]):
                return decorator(args[0])
            return decorator

    capture = Capture()
    module.register(capture)
    function = capture.function
    if function is None:
        raise RuntimeError("register(mcp) did not expose one function")
    if name == "calculator":
        return {"status": "success", "value": function("(2 + 3) * 4")}
    if name == "molecule_name_to_smiles":
        return {"status": "success", "smiles": function("sulfur dioxide")}
    if name == "smiles_to_coordinate_file":
        return function("O", "outputs/original_water.xyz", 2025, "xyz")
    if name == "extract_output_json":
        path = workspace / "outputs" / "sample_result.json"
        path.write_text('{"energy": -1.0}\n', encoding="utf-8")
        value = function("outputs/sample_result.json")
        return {"status": "success", "value": value}
    if name == "run_ase":
        _xyz(workspace)
        params = module.ASEInputSchema.model_validate(
            {
                "input_structure_file": "data/water.xyz",
                "output_results_file": "outputs/ase_energy.json",
                "driver": "energy",
                "calculator": {"calculator_type": "emt"},
            }
        )
        return function(params)
    raise KeyError(name)


def probe_tools(workspace: Path) -> list[dict[str, Any]]:
    original = {"calculator", "extract_output_json", "molecule_name_to_smiles", "run_ase", "smiles_to_coordinate_file"}
    rows = []
    for record in discover_tools(include_disabled=True, strict=False):
        name = record.spec.name if record.spec else record.module_stem
        row = {
            "name": name,
            "enabled": record.enabled,
            "category": record.spec.category if record.spec else "",
            "backend": record.spec.backend if record.spec else "",
            "status": "failed" if record.error else "registered",
            "detail": record.error or "",
        }
        if record.error:
            rows.append(row)
            continue
        try:
            result = _probe_original(name, workspace) if name in original else _call_core(name, workspace)
            row["status"], row["detail"] = _result_status(result)
            row["result"] = _json_safe(result)
        except Exception as exc:
            row["status"] = "failed"
            row["detail"] = f"{type(exc).__name__}: {exc}"
            row["traceback"] = traceback.format_exc(limit=8)
        rows.append(row)
    return rows


def probe_software() -> list[dict[str, Any]]:
    rows = []
    for entry in software_entries():
        module = entry.get("python_module") or ""
        executable = entry.get("executable") or ""
        configured = entry.get("status", "planned")
        if configured in {"blocked_license", "blocked_credentials", "manual_required", "unsupported_platform"}:
            runtime_status = configured
            detail = entry.get("failure_reason") or entry.get("manual_action") or configured
        elif entry.get("install_method", "").startswith("remote"):
            runtime_status = "integrated"
            detail = "Remote API adapter is present; live status is reported by the corresponding MCP tool."
        elif not module and not executable:
            # A registry-only/manual entry with no detectable runtime must not
            # be reported as installed merely because there was nothing to
            # probe.  Preserve its declared lifecycle status instead.
            runtime_status = configured
            detail = entry.get("failure_reason") or entry.get("manual_action") or configured
        else:
            probe = backend_status(
                entry["name"],
                python_modules=(module,),
                executables=(executable,),
                manual_action=entry.get("manual_action") or "Install the backend in .toolbox_env.",
            )
            runtime_status = "installed" if probe["available"] else "planned"
            detail = "Runtime dependency detected" if probe["available"] else probe["manual_action"]
        rows.append(
            {
                "name": entry["name"],
                "category": entry.get("category"),
                "status": runtime_status,
                "detail": detail,
                "python_module": module or None,
                "python_version": module_version(module.split(".")[0]) if module else None,
                "executable": executable or None,
                "executable_path": shutil.which(executable) if executable else None,
                "official_url": entry.get("official_url"),
                "manual_action": entry.get("manual_action"),
            }
        )
    return rows


def _markdown(tool_rows: list[dict[str, Any]], software_rows: list[dict[str, Any]], workspace: Path) -> str:
    labels = {
        "working": "正常工作",
        "not_configured": "未配置/未完成真实 smoke",
        "failed": "未正常工作",
        "registered": "已注册",
    }
    tool_counts = Counter(row["status"] for row in tool_rows)
    software_counts = Counter(row["status"] for row in software_rows)
    lines = [
        "# ResearchChemBench 工具箱状态报告",
        "",
        f"- 生成时间：{datetime.now(timezone.utc).isoformat()}",
        f"- Python：`{sys.executable}`",
        f"- 验证 workspace：`{workspace}`",
        f"- MCP 工具数：{len(tool_rows)}",
        f"- 正常工作：{tool_counts['working']}",
        f"- 未配置/未完成真实 smoke：{tool_counts['not_configured']}",
        f"- 未正常工作：{tool_counts['failed']}",
        "",
        "## MCP 工具状态",
        "",
        "| Tool | Category | Backend | Status | Detail |",
        "|---|---|---|---|---|",
    ]
    for row in tool_rows:
        detail = str(row.get("detail", "")).replace("|", "\\|").replace("\n", " ")[:500]
        lines.append(
            f"| {row['name']} | {row['category']} | {row['backend']} | "
            f"{labels.get(row['status'], row['status'])} | {detail} |"
        )
    lines.extend(
        [
            "",
            "## 软件/服务状态",
            "",
            "状态统计：" + ", ".join(f"`{key}`={value}" for key, value in sorted(software_counts.items())),
            "",
            "| Software | Category | Status | Module/Executable | Detail | Manual action |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in software_rows:
        runtime = row.get("python_module") or row.get("executable") or "remote/manual"
        detail = str(row.get("detail", "")).replace("|", "\\|").replace("\n", " ")[:400]
        manual = str(row.get("manual_action") or "").replace("|", "\\|").replace("\n", " ")[:400]
        lines.append(f"| {row['name']} | {row['category']} | {row['status']} | {runtime} | {detail} | {manual} |")
    lines.extend(
        [
            "",
            "## 判定说明",
            "",
            "- `正常工作`：实际执行了最小功能输入并得到结构化成功结果。",
            "- `未配置/未完成真实 smoke`：wrapper 已注册，但缺少程序、凭据、模型、许可证，或尚无安全的自动 smoke 输入。",
            "- `未正常工作`：后端存在或工具被调用，但最小测试抛出异常或返回错误。",
            "- 软件表中的 `installed` 只表示检测到模块/可执行文件；是否完成计算以 MCP 工具表的真实 smoke 为准。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    _prepare_path()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    workspace = ROOT / "workspaces" / "toolbox_verification" / timestamp
    (workspace / "outputs").mkdir(parents=True, exist_ok=False)
    os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
    os.environ["RESEARCHCHEMBENCH_RUN_ID"] = f"toolbox-verification-{timestamp}"
    os.environ.setdefault("CHEMGRAPH_ROOT", str(ROOT.parent / "ChemGraph"))
    tool_rows = probe_tools(workspace)
    software_rows = probe_software()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.executable,
        "workspace": str(workspace),
        "tools": tool_rows,
        "software": software_rows,
    }
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(_markdown(tool_rows, software_rows, workspace), encoding="utf-8")
    print(REPORT_PATH)
    print(JSON_PATH)
    counts = Counter(row["status"] for row in tool_rows)
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
