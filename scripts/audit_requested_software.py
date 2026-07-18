#!/usr/bin/env python3
"""Audit every software/tool requested for the ResearchChemBench build.

The audit deliberately separates an installed dependency runtime from a public
MCP Action.  A package can therefore be configured and documented without
silently introducing a fixed workflow or an implicit backend choice.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "config" / "requested_software.yaml"
AUX_CONFIG = ROOT / "config" / "auxiliary_environments.yaml"
MCP_CONFIG = ROOT / "config" / "mcp_profiles.yaml"
JSON_OUTPUT = ROOT / "config" / "requested_software_status.json"
MARKDOWN_OUTPUT = ROOT / "docs" / "tools" / "CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md"


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError(f"Expected mapping in {path}")
    return value


def root_path(value: str | Path | None) -> Path | None:
    if value is None or str(value).strip() == "":
        return None
    path = Path(str(value)).expanduser()
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def runtime_path(specification: dict[str, Any]) -> Path:
    path = root_path(specification.get("environment"))
    if path is None:
        raise ValueError("Runtime specification has no environment")
    return path


def resolve_runtime_value(value: str, runtime: Path) -> str:
    path = Path(str(value)).expanduser()
    if path.is_absolute():
        return str(path)
    if path.parent != Path("."):
        return str((ROOT / path).resolve())
    return str((runtime / "bin" / path).resolve())


def runtime_environment(specification: dict[str, Any]) -> dict[str, str]:
    runtime = runtime_path(specification)
    path_entries = [runtime / "bin"]
    path_entries.extend(root_path(item) for item in specification.get("path_entries", []))
    library_entries = [runtime / "lib"]
    library_entries.extend(root_path(item) for item in specification.get("library_path_entries", []))
    path_entries = [item for item in path_entries if item is not None]
    library_entries = [item for item in library_entries if item is not None]
    environment = {
        "PATH": os.pathsep.join([*(str(item) for item in path_entries), os.environ.get("PATH", "")]),
        "LD_LIBRARY_PATH": os.pathsep.join(
            [*(str(item) for item in library_entries), os.environ.get("LD_LIBRARY_PATH", "")]
        ),
        "PYTHONPATH": os.pathsep.join([str(ROOT), os.environ.get("PYTHONPATH", "")]),
    }
    for name, value in (specification.get("environment_variables") or {}).items():
        text = str(value)
        if text.startswith(".") or "/" in text:
            candidate = root_path(text)
            environment[str(name)] = str(candidate) if candidate else text
        else:
            environment[str(name)] = text
    for name, value in (specification.get("command_variables") or {}).items():
        candidate = resolve_runtime_value(str(value), runtime)
        if Path(candidate).exists():
            environment[str(name)] = str(Path(candidate).resolve())
    return environment


def runtime_catalog() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    mcp = read_yaml(MCP_CONFIG)
    for group in ("profiles", "support_environments"):
        for name, specification in (mcp.get(group) or {}).items():
            item = dict(specification)
            item["name"] = name
            item["group"] = group
            result[name] = item
    auxiliary = read_yaml(AUX_CONFIG).get("auxiliary_environments") or {}
    for name, specification in auxiliary.items():
        item = dict(specification)
        item["name"] = name
        item["group"] = "auxiliary_environments"
        result[name] = item
    return result


def runtime_python(specification: dict[str, Any]) -> Path:
    configured = str(specification.get("python") or "").strip()
    if configured:
        path = root_path(configured)
        if path is None:
            raise ValueError("Invalid configured runtime Python")
        return path
    return runtime_path(specification) / "bin" / "python"


def probe_modules(python: Path, names: list[str], environment: dict[str, str], timeout: int) -> dict[str, Any]:
    if not names:
        return {}
    if not python.is_file():
        return {name: {"available": False, "error": "runtime Python missing"} for name in names}
    code = r'''
import importlib.metadata
import importlib
import json
import sys

name = sys.argv[1]
try:
    importlib.import_module(name)
except Exception as exc:
    print(json.dumps({"available": False, "error": f"{type(exc).__name__}: {exc}"}))
    raise SystemExit(0)

version = None
for candidate in (name, name.split(".")[0]):
    try:
        version = importlib.metadata.version(candidate)
        break
    except Exception:
        pass
print(json.dumps({"available": True, "version": version}))
'''
    results: dict[str, Any] = {}
    for name in names:
        try:
            completed = subprocess.run(
                [str(python), "-c", code, name],
                cwd=ROOT,
                env={**os.environ, **environment},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
            if completed.returncode == 0 and completed.stdout.strip():
                results[name] = json.loads(completed.stdout.strip().splitlines()[-1])
                continue
            error = (completed.stderr or completed.stdout or "module probe failed")[-500:]
        except subprocess.TimeoutExpired:
            error = f"module import timed out after {timeout}s"
        except (OSError, json.JSONDecodeError) as exc:
            error = f"{type(exc).__name__}: {exc}"
        results[name] = {"available": False, "error": error}
    return results


def command_path(command: str, environment: dict[str, str]) -> str | None:
    value = str(command)
    candidate = Path(value).expanduser()
    if candidate.is_absolute() or "/" in value:
        path = candidate if candidate.is_absolute() else ROOT / candidate
        return str(path.resolve()) if path.is_file() and os.access(path, os.X_OK) else None
    found = shutil.which(value, path=environment.get("PATH"))
    return str(Path(found).resolve()) if found else None


def run_smoke(
    command: list[str],
    environment: dict[str, str],
    timeout: int,
) -> dict[str, Any]:
    if not command:
        return {"success": False, "error": "empty smoke command"}
    executable = command_path(command[0], environment)
    if executable is None:
        return {"success": False, "error": f"command not found: {command[0]}"}
    try:
        completed = subprocess.run(
            [executable, *command[1:]],
            cwd=ROOT,
            env={**os.environ, **environment},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        return {
            "success": completed.returncode == 0,
            "returncode": completed.returncode,
            "output_tail": completed.stdout[-1000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {"success": False, "error": f"timeout after {timeout}s", "output_tail": str(exc.stdout or "")[-1000:]}
    except OSError as exc:
        return {"success": False, "error": f"{type(exc).__name__}: {exc}"}


def md(value: Any) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def relative(path: str | Path | None) -> str:
    if not path:
        return "—"
    value = Path(str(path))
    try:
        return value.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(value.resolve())


def audit(timeout: int) -> dict[str, Any]:
    inventory = read_yaml(INVENTORY).get("requested_software") or []
    runtimes = runtime_catalog()
    by_runtime: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in inventory:
        environment = str(item.get("environment") or "").strip()
        if environment:
            if environment not in runtimes:
                raise ValueError(f"Unknown runtime {environment!r} for {item['name']}")
            by_runtime[environment].append(item)

    runtime_probes: dict[str, dict[str, Any]] = {}
    for name, items in by_runtime.items():
        specification = runtimes[name]
        environment = runtime_environment(specification)
        python = runtime_python(specification)
        modules = sorted({module for item in items for module in item.get("modules", [])})
        module_results = probe_modules(python, modules, environment, timeout)
        command_names = sorted({command for item in items for command in item.get("commands", [])})
        command_results = {command: command_path(command, environment) for command in command_names}
        smoke_results = {}
        for index, command in enumerate(specification.get("smoke_commands") or [], start=1):
            smoke_results[str(index)] = run_smoke([str(value) for value in command], environment, timeout)
        runtime_probes[name] = {
            "name": name,
            "group": specification.get("group"),
            "conda_name": specification.get("conda_name"),
            "environment": str(runtime_path(specification)),
            "python": str(python),
            "python_exists": python.is_file(),
            "python_required": bool(modules),
            "modules": module_results,
            "commands": command_results,
            "smokes": smoke_results,
            "conda_packages": list(specification.get("conda_packages") or []),
            "pip_packages": list(specification.get("pip_packages") or []),
            "cache_paths": [relative(root_path(value)) for value in specification.get("cache_paths", [])],
            "notes": specification.get("notes", ""),
        }

    records: list[dict[str, Any]] = []
    for item in inventory:
        policy = str(item.get("status_policy") or "probe")
        record = dict(item)
        record["official_url"] = item.get("official_url")
        environment_name = str(item.get("environment") or "").strip()
        probe = runtime_probes.get(environment_name, {})
        record["environment_detail"] = {
            "name": environment_name or None,
            "conda_name": probe.get("conda_name"),
            "path": relative(probe.get("environment")),
            "python": relative(probe.get("python")),
            "conda_packages": probe.get("conda_packages", []),
            "pip_packages": probe.get("pip_packages", []),
        }
        if policy == "specification":
            record["status"] = "specification"
            record["verification"] = {"reason": "data/specification contract"}
        elif policy == "manual":
            record["status"] = "manual_required"
            record["verification"] = {"reason": item.get("notes", "operator action required")}
        elif policy == "interface":
            record["status"] = "manual_api_review"
            record["verification"] = {"reason": item.get("notes", "stable API not verified")}
        else:
            module_results = {name: probe.get("modules", {}).get(name, {"available": False}) for name in item.get("modules", [])}
            command_results = {name: probe.get("commands", {}).get(name) for name in item.get("commands", [])}
            cache_results = {}
            for path_value in item.get("cache_paths", []) or []:
                path = root_path(path_value)
                cache_results[str(path_value)] = {
                    "exists": bool(path and path.exists()),
                    "path": relative(path),
                }
            module_ok = all(value.get("available", False) for value in module_results.values())
            command_ok = all(value for value in command_results.values())
            cache_ok = all(value.get("exists", False) for value in cache_results.values())
            checks = [*module_results.values(), *({"available": bool(value)} for value in command_results.values()), *({"available": value.get("exists", False)} for value in cache_results.values())]
            passed = sum(1 for value in checks if value.get("available"))
            runtime_ready = (
                bool(probe.get("python_exists", False))
                if module_results
                else bool(environment_name and runtime_path(runtimes[environment_name]).exists())
            )
            if module_ok and command_ok and cache_ok and runtime_ready:
                status = "configured"
            elif passed:
                status = "partial"
            else:
                status = "not_found"
            record["status"] = status
            record["verification"] = {
                "python_exists": probe.get("python_exists", False),
                "modules": module_results,
                "commands": command_results,
                "cache_paths": cache_results,
                "runtime_smokes": probe.get("smokes", {}),
            }
        records.append(record)

    counts: dict[str, int] = defaultdict(int)
    for item in records:
        counts[str(item["status"])] += 1
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(ROOT),
        "model_cache_root": ".model_cache",
        "software_cache_root": ".software_cache",
        "summary": {
            "total": len(records),
            "counts": dict(sorted(counts.items())),
            "configured": counts.get("configured", 0),
            "manual_or_review": counts.get("manual_required", 0) + counts.get("manual_api_review", 0),
            "complete_for_inventory": counts.get("configured", 0) + counts.get("specification", 0),
        },
        "runtime_probes": runtime_probes,
        "software": records,
    }


def write_markdown(payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    records = payload["software"]
    lines = [
        "# ResearchChemBench 请求软件/工具配置状态",
        "",
        f"> 生成时间：`{payload['generated_at']}`。本报告由 `scripts/audit_requested_software.py` 生成，覆盖用户给出的全部 {summary['total']} 项；它把“依赖已安装”“规范已实现”“需要人工许可/下载”“接口尚未安全接入”分开记录。",
        "",
        "## 总结",
        "",
        "| 状态 | 数量 | 含义 |",
        "|---|---:|---|",
        f"| configured | {summary['counts'].get('configured', 0)} | 声明 runtime 中的模块/命令/缓存路径均通过检查 |",
        f"| partial | {summary['counts'].get('partial', 0)} | 有部分组件可用，但仍有导入、数据库、数据文件或其他检查未通过 |",
        f"| specification | {summary['counts'].get('specification', 0)} | QCSchema 这类规范由其他库实现，不是独立安装包 |",
        f"| manual_required | {summary['counts'].get('manual_required', 0)} | 需要许可证、注册、供应商下载、源码编译或 GUI 主机配置 |",
        f"| manual_api_review | {summary['counts'].get('manual_api_review', 0)} | 官方站点可访问，但尚未确认稳定且条款允许的通用 API |",
        f"| not_found | {summary['counts'].get('not_found', 0)} | 声明为自动探测的软件没有任何模块、命令或缓存检查通过 |",
        f"| 总计 | {summary['total']} | 用户名单逐项覆盖 |",
        "",
        "## 目录约定",
        "",
        "- 软件和大体积二进制只放在 `.software_cache/` 的版本化子目录；运行时定义在 `config/mcp_profiles.yaml` 或 `config/auxiliary_environments.yaml`。",
        "- 模型权重只放在 `.model_cache/`；NequIP 和 DeePMD-kit 本轮只配置运行时，没有擅自下载或选择 checkpoint。",
        "- auxiliary runtime 只用于依赖隔离、健康检查和后续原子适配，不改变公共 MCP 工具目录，也不自动替 Agent 编排流程。",
        "",
        "## 逐项状态表",
        "",
        "| 类别 | 名称 | 状态 | 类型 / 许可 | Runtime / Python 模块 / 命令 | 软件缓存 / 模型缓存 | 公共适配状态 | 功能与处理备注 | 官方入口 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for item in records:
        verification = item.get("verification") or {}
        modules = []
        for name, value in (verification.get("modules") or {}).items():
            version = value.get("version")
            if value.get("available"):
                state = "OK"
            elif "timed out" in str(value.get("error") or ""):
                state = "超时"
            else:
                state = "失败"
            modules.append(f"{name}={state}" + (f" ({version})" if version else ""))
        commands = [f"{name}={'OK' if path else '缺失'}" for name, path in (verification.get("commands") or {}).items()]
        environment = item.get("environment_detail") or {}
        runtime_text = "<br>".join(
            part for part in [
                f"{environment.get('name') or '—'} / `{environment.get('path') or '—'}`",
                "modules: " + (", ".join(modules) or "—"),
                "commands: " + (", ".join(commands) or "—"),
            ] if part
        )
        cache = []
        for value in item.get("cache_paths") or []:
            result = (verification.get("cache_paths") or {}).get(str(value), {})
            cache.append(f"{value}={'存在' if result.get('exists') else '缺失'}")
        if item.get("model_cache"):
            cache.append(f"model: {item['model_cache']}（不自动下载）")
        cache_text = "<br>".join(cache) or "—"
        url = item.get("official_url")
        url_text = f"[官方]({url})" if url else "—"
        lines.append(
            f"| {md(item.get('category'))} | `{md(item.get('name'))}` | **{md(item.get('status'))}** | `{md(item.get('kind'))}`<br>{md(item.get('license'))} | {runtime_text} | {cache_text} | `{md(item.get('public_adapter'))}` | {md(item.get('role'))}<br>{md(item.get('notes'))} | {url_text} |"
        )

    lines.extend([
        "",
        "## Runtime 级检查明细",
        "",
        "| Runtime | Conda 名称 | Python | Conda/Pip 依赖 | Smoke | 说明 |",
        "|---|---|---|---|---|---|",
    ])
    for name, runtime in payload.get("runtime_probes", {}).items():
        smoke = []
        for key, value in (runtime.get("smokes") or {}).items():
            smoke.append(f"{key}={'pass' if value.get('success') else 'fail'}")
        packages = "Conda: " + (", ".join(runtime.get("conda_packages") or []) or "—") + "<br>Pip: " + (", ".join(runtime.get("pip_packages") or []) or "—")
        lines.append(
            f"| `{name}`<br>`{relative(runtime.get('environment'))}` | `{md(runtime.get('conda_name'))}` | `{relative(runtime.get('python'))}`<br>{('存在' if runtime.get('python_exists') else '缺失') if runtime.get('python_required') else '不需要（仅命令型 runtime）'} | {md(packages)} | {', '.join(smoke) or '未执行'} | {md(runtime.get('notes'))} |"
        )
    lines.extend([
        "",
        "## 状态解释与后续手动处理",
        "",
        "- `configured` 仅表示本地依赖/入口已准备好，不代表已经为所有软件编写了公共 Action，也不代表已经替 Agent 选择模型、泛函、基组、赝势或工作流顺序。",
        "- `partial` 项需按备注补充真实输入或数据。当前 Arkane 的入口已安装，但顶层导入在 120 秒内仍未完成，不能用无界等待替代真实案例验证。",
        "- `manual_required` 项需要用户提供许可证、注册下载、源码包或编译工具链；收到后可按本表的官方入口继续接入对应 runtime。",
        "- NIST 两项保持 `manual_api_review`，不通过脆弱网页抓取伪装成稳定工具；在确认官方 API 和使用条款后再增加数据 Action。",
        "",
        "## 重放命令",
        "",
        "```bash",
        ".toolbox_env/bin/python scripts/audit_requested_software.py",
        "```",
        "",
    ])
    MARKDOWN_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    args = parser.parse_args()
    payload = audit(max(5, args.timeout_seconds))
    JSON_OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(payload)
    print(MARKDOWN_OUTPUT)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
