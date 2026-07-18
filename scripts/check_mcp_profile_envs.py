#!/usr/bin/env python3
"""Verify all isolated MCP environments and generate Markdown/JSON reports."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from dotenv import dotenv_values


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "mcp_profiles.yaml"
INSTALL_STATUS_PATH = ROOT / "config" / "mcp_profile_status.json"
LOCAL_CONFIG_PATH = ROOT / "config.local.env"
JSON_REPORT = ROOT / "docs" / "MCP_PROFILE_STATUS.json"
MARKDOWN_REPORT = ROOT / "docs" / "MCP_PROFILE_STATUS.md"
MARKER = "PROFILE_PROBE_JSON="
MODEL_CACHE_ENV = "RESEARCHCHEMBENCH_MODEL_CACHE"


def run_profile_probe(
    name: str,
    profile: dict[str, Any],
    *,
    timeout_seconds: int,
    live_materials_project: bool,
    check_models: bool,
    secrets: dict[str, str],
) -> dict[str, Any]:
    python = (ROOT / profile["environment"] / "bin" / "python").resolve()
    if not python.is_file():
        return {
            "profile": name,
            "required_ok": False,
            "error": f"Python environment is missing: {python}",
        }
    command = [str(python), str(ROOT / "scripts" / "probe_mcp_profile.py"), "--profile", name]
    if live_materials_project and name == "services":
        command.append("--live-materials-project")
    if check_models and (profile.get("health_checks") or {}).get("models"):
        command.append("--check-models")
    environment = os.environ.copy()
    environment.update(secrets)
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(ROOT), str(ROOT.parent / "ChemGraph" / "src"), environment.get("PYTHONPATH", "")]
    )
    # Profile probes only inspect imports, commands, and MCP metadata.  Give the
    # server a disposable workspace so repeated health checks do not accumulate
    # benchmark artifacts under workspaces/.
    with tempfile.TemporaryDirectory(prefix=f"researchchem_{name}_probe_") as workspace:
        environment["RESEARCHCHEMBENCH_WORKSPACE"] = workspace
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
            check=False,
        )
    marker_lines = [line for line in completed.stdout.splitlines() if line.startswith(MARKER)]
    if not marker_lines:
        return {
            "profile": name,
            "required_ok": False,
            "returncode": completed.returncode,
            "error": "Profile probe did not emit structured output",
            "output_tail": completed.stdout[-4000:],
        }
    result = json.loads(marker_lines[-1][len(MARKER) :])
    result["returncode"] = completed.returncode
    if completed.returncode and result.get("required_ok"):
        result["required_ok"] = False
    return result


def support_probe(name: str, specification: dict[str, Any]) -> dict[str, Any]:
    environment = (ROOT / specification["environment"]).resolve()
    commands = {}
    for command in (specification.get("health_checks") or {}).get("commands", []):
        candidate = environment / "bin" / str(command)
        commands[str(command)] = str(candidate.resolve()) if candidate.is_file() else None
    python = environment / "bin" / "python"
    dependency_check = {
        "success": False,
        "returncode": None,
        "output": "Python environment is missing",
    }
    if python.is_file():
        dependency_environment = os.environ.copy()
        dependency_environment.pop("PYTHONPATH", None)
        completed = subprocess.run(
            [str(python), "-m", "pip", "check"],
            cwd=environment,
            env=dependency_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        dependency_check = {
            "success": completed.returncode == 0,
            "returncode": completed.returncode,
            "output": completed.stdout.strip(),
        }
    return {
        "name": name,
        "conda_name": specification.get("conda_name"),
        "environment": str(environment),
        "commands": commands,
        "dependency_check": dependency_check,
        "required_ok": python.is_file()
        and all(commands.values())
        and dependency_check["success"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = []
    for name, result in payload["profiles"].items():
        manual_missing = [key for key, value in result.get("manual_commands", {}).items() if not value]
        detail = "ready"
        if manual_missing:
            detail += "; manual: " + ", ".join(manual_missing)
        if not result.get("required_ok"):
            detail = result.get("error") or "required module/command/tool-list check failed"
        rows.append(
            f"| `{name}` | `{result.get('conda_name', '-')}` | "
            f"`{result.get('server_name', '-')}` | "
            f"{len(result.get('listed_tools', []))} | "
            f"{'通过' if result.get('required_ok') else '失败'} | {detail} |"
        )
    support_rows = [
        f"| `{name}` | `{result.get('conda_name', '-')}` | "
        f"{'通过' if result.get('required_ok') else '失败'} | "
        f"{', '.join(result.get('commands', {})) or '-'} |"
        for name, result in payload["support_environments"].items()
    ]
    return "\n".join(
        [
            "# MCP 分环境安装与检查状态",
            "",
            f"- 生成时间：{payload['generated_at']}",
            f"- MCP profiles：{payload['summary']['profile_count']}",
            f"- 必需检查通过：{payload['summary']['ready_profiles']}",
            f"- 工具总数：{payload['summary']['tool_count']}",
            f"- Materials Project key：{'已配置' if payload['credentials']['MP_API_KEY'] else '未配置'}",
            f"- Materials Project live smoke：{payload['summary']['materials_project_live']}",
            f"- 模型功能检查：{payload['summary']['model_checks']}",
            f"- 项目模型缓存：`{payload['summary']['model_cache']}`",
            "",
            "## MCP profiles",
            "",
            "| Profile | Conda environment | MCP server | Tools | Required checks | Detail |",
            "|---|---|---|---:|---|---|",
            *rows,
            "",
            "## 仅可执行程序环境",
            "",
            "| Environment | Conda environment | Check | Commands |",
            "|---|---|---|---|",
            *support_rows,
            "",
            "## 说明",
            "",
            "- `manual: orca` 与 `manual: gnina` 不影响对应 profile 的基础可用性；它们需要人工接受许可/下载二进制。",
            "- 周期计算拆成 QE、CP2K、DFTB+/SIESTA 调度、ABINIT 支撑环境和 Phonopy 环境，避免求解器互相降级。",
            "- NequIP、DeepMD、FAIRChem、AIMNet2 尚无完成的模型加载 adapter，因此没有作为 `run_mlip` 的必需依赖安装。",
            "- 每个 profile 和支撑环境都执行独立的 `pip check`；依赖冲突会使必需检查失败。",
            "- 该报告不会记录或输出 API key 的具体值。",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", default="", help="Optional comma-separated profile subset.")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--live-materials-project", action="store_true")
    parser.add_argument(
        "--check-models",
        action="store_true",
        help="Load configured model weights and run a minimal energy calculation.",
    )
    args = parser.parse_args()

    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    profiles = config["profiles"]
    selected = [item.strip() for item in args.profiles.split(",") if item.strip()] or list(profiles)
    unknown = sorted(set(selected) - set(profiles))
    if unknown:
        raise SystemExit(f"Unknown profiles: {unknown}")
    raw_secrets = dotenv_values(LOCAL_CONFIG_PATH) if LOCAL_CONFIG_PATH.exists() else {}
    secrets = {key: str(value) for key, value in raw_secrets.items() if value is not None}
    configured_cache = secrets.get(MODEL_CACHE_ENV, "").strip()
    model_cache = Path(
        configured_cache or str(config.get("model_cache_root") or ".model_cache")
    ).expanduser()
    if not model_cache.is_absolute():
        model_cache = ROOT / model_cache

    results = {
        name: run_profile_probe(
            name,
            profiles[name],
            timeout_seconds=args.timeout_seconds,
            live_materials_project=args.live_materials_project,
            check_models=args.check_models,
            secrets=secrets,
        )
        for name in selected
    }
    support = {
        name: support_probe(name, specification)
        for name, specification in (config.get("support_environments") or {}).items()
    }
    tool_count = sum(len(profiles[name]["tools"]) for name in selected)
    materials = results.get("services", {}).get("live_checks", {}).get("materials_project")
    model_checks = [
        check
        for result in results.values()
        for check in result.get("model_checks", {}).values()
    ]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "install_status_path": str(INSTALL_STATUS_PATH),
        "credentials": {"MP_API_KEY": bool(secrets.get("MP_API_KEY"))},
        "summary": {
            "profile_count": len(results),
            "ready_profiles": sum(bool(item.get("required_ok")) for item in results.values()),
            "tool_count": tool_count,
            "materials_project_live": (
                "passed" if materials and materials.get("success") else
                "failed" if materials else "not_requested"
            ),
            "model_checks": (
                f"{sum(bool(item.get('success')) for item in model_checks)}/"
                f"{len(model_checks)} passed"
                if model_checks else "not_requested"
            ),
            "model_cache": str(model_cache.resolve()),
        },
        "profiles": results,
        "support_environments": support,
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MARKDOWN_REPORT.write_text(render_markdown(payload), encoding="utf-8")
    print(MARKDOWN_REPORT)
    failed = any(not item.get("required_ok") for item in results.values()) or any(
        not item.get("required_ok") for item in support.values()
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
