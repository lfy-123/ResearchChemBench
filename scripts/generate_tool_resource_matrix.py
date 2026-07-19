#!/usr/bin/env python3
"""Generate the detailed action/backend/runtime/resource audit requested for the toolbox."""

from __future__ import annotations

import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from researchchem_toolbox.catalog import CATEGORY_LABELS, catalog_snapshot


OUTPUT = ROOT / "docs" / "tools" / "CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md"
PROFILE_STATUS = ROOT / "docs" / "MCP_PROFILE_STATUS.json"
RESOURCE_STATUS = ROOT / "config" / "toolbox_resource_status.json"
RESOURCE_SMOKE_STATUS = ROOT / "config" / "scientific_resource_smoke_status.json"
DATA_SMOKE_STATUS = ROOT / "config" / "data_source_smoke_status.json"
REQUESTED_SOFTWARE_STATUS = ROOT / "config" / "requested_software_status.json"
PYTEST_STATUS = ROOT / "config" / "pytest_status.xml"


def read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def md(value: Any) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def code_list(values: Any) -> str:
    values = list(values or [])
    return ", ".join(f"`{md(value)}`" for value in values) if values else "—"


def relative(path_value: str | Path | None) -> str:
    if not path_value:
        return "—"
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        return path.as_posix()
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def requirements_for_action(backend: dict[str, Any], action_id: str) -> str:
    method = (backend.get("required_method_fields") or {}).get(action_id, [])
    settings = (backend.get("required_setting_fields") or {}).get(action_id, [])
    parts = []
    if method:
        parts.append("method: " + ", ".join(method))
    if settings:
        parts.append("settings: " + ", ".join(settings))
    return "; ".join(parts) or "no mandatory backend-specific fields"


def map_text(mapping: dict[str, Any]) -> str:
    if not mapping:
        return "—"
    return "<br>".join(f"`{md(key)}`: {md(value)}" for key, value in mapping.items())


def required_by_action(mapping: dict[str, list[str]]) -> str:
    if not mapping:
        return "—"
    return "<br>".join(
        f"`{action}`: {', '.join(fields) if fields else '—'}"
        for action, fields in mapping.items()
    )


def pytest_summary() -> dict[str, Any]:
    if not PYTEST_STATUS.is_file():
        return {}
    root = ET.parse(PYTEST_STATUS).getroot()
    if root.tag == "testsuites":
        suites = list(root.findall("testsuite"))
        return {
            key: (
                root.attrib.get(key)
                if root.attrib.get(key) is not None
                else str(
                    sum(
                        float(suite.attrib.get(key, 0))
                        for suite in suites
                    )
                )
            )
            for key in ("tests", "failures", "errors", "skipped", "time")
        }
    return {
        key: root.attrib.get(key)
        for key in ("tests", "failures", "errors", "skipped", "time")
    }


def main() -> int:
    load_dotenv(ROOT / "config.local.env", override=False)
    generated_at = datetime.now(timezone.utc).isoformat()
    catalog = catalog_snapshot(include_health=True)
    profiles_config = yaml.safe_load(
        (ROOT / "config" / "mcp_profiles.yaml").read_text(encoding="utf-8")
    )
    profile_status = read_json(PROFILE_STATUS, {"summary": {}, "profiles": {}})
    resource_status = read_json(RESOURCE_STATUS, {"summary": {}, "resources": []})
    resource_smokes = read_json(
        RESOURCE_SMOKE_STATUS, {"summary": {}, "cases": []}
    )
    data_smokes = read_json(DATA_SMOKE_STATUS, {"summary": {}, "cases": []})
    requested_software = read_json(
        REQUESTED_SOFTWARE_STATUS, {"summary": {}, "software": []}
    )
    tests = pytest_summary()

    actions = catalog["actions"]
    backends = catalog["backends"]
    resources = catalog["resources"]
    backend_by_id = {item["id"]: item for item in backends}
    health_by_id = {item["id"]: item.get("health") or {} for item in backends}
    resources_by_backend: dict[str, list[dict[str, Any]]] = {}
    for resource in resources:
        for backend_id in resource.get("compatible_backends") or []:
            resources_by_backend.setdefault(backend_id, []).append(resource)
    allowed_unavailable = set(
        (profiles_config.get("audit") or {}).get("allowed_unavailable_backends", [])
    )
    unavailable = sorted(
        backend_id for backend_id, health in health_by_id.items() if not health.get("available")
    )
    unexpected_unavailable = sorted(set(unavailable) - allowed_unavailable)
    resource_smoke_by_backend: dict[str, list[dict[str, Any]]] = {}
    for item in resource_smokes.get("cases", []):
        resource_smoke_by_backend.setdefault(item["backend"], []).append(item)
    data_smoke_by_action = {
        item["action"]: item for item in data_smokes.get("cases", [])
    }
    resource_status_by_id = {
        item["id"]: item for item in resource_status.get("resources", [])
    }
    profile_results = profile_status.get("profiles", {})
    expected_runtimes = {
        name
        for group in ("profiles", "support_environments")
        for name in (profiles_config.get(group) or {})
    }
    missing_profile_results = sorted(expected_runtimes - set(profile_results))
    profile_failures = sorted(
        name for name, item in profile_results.items() if not item.get("required_ok")
    )
    all_configured = (
        not unavailable
        and bool(resource_status.get("summary", {}).get("all_ok"))
        and bool(resource_smokes.get("summary", {}).get("all_ok"))
        and bool(data_smokes.get("summary", {}).get("all_ok"))
        and not profile_failures
        and not missing_profile_results
    )
    gpu_device_present = any(Path("/dev").glob("nvidia[0-9]*"))

    lines = [
        "# ResearchChemBench 化学工具箱：工具、后端与环境资源矩阵",
        "",
        f"> 生成时间：`{generated_at}`。本文件由 `scripts/generate_tool_resource_matrix.py` 从当前代码、运行环境、资源注册表和验证结果生成。",
        "",
        "## 1. 审计结论",
        "",
        "| 审计项 | 当前结果 | 判定口径 |",
        "|---|---|---|",
        f"| 公共工具 | {len(actions)} 个：{sum(not item['data_action'] for item in actions)} 个 Scientific Actions + {sum(item['data_action'] for item in actions)} 个 Data Actions | 所有任务暴露同一份完整原子工具目录 |",
        f"| Agent 可选后端 | {len(backends)} 个；可用 {sum(bool(item.get('health', {}).get('available')) for item in backends)} 个；不可用 {len(unavailable)} 个 | BackendSpec、运行环境、模块/命令/凭据联合探测 |",
        f"| 允许缺失后端 | {code_list(sorted(allowed_unavailable))} | 完整 benchmark 构建应为空；任何缺失都不会触发自动替代 |",
        f"| 非预期缺失后端 | {code_list(unexpected_unavailable)} | 应为空 |",
        f"| 隔离运行环境 | {profile_status.get('summary', {}).get('ready_profiles', 0)}/{profile_status.get('summary', {}).get('profile_count', 0)} 通过 | 模块、命令、外部命令、`pip check`、模型加载及 Backend health |",
        f"| 注册资源 | {resource_status.get('summary', {}).get('passed', 0)}/{resource_status.get('summary', {}).get('resource_count', 0)} 通过 | 文件存在、归档/模型校验、元素/参数覆盖；SSSP 深度逐文件 MD5 |",
        f"| 下载资源真实计算 | {resource_smokes.get('summary', {}).get('passed', 0)}/{resource_smokes.get('summary', {}).get('case_count', 0)} 通过 | 实际启动量化/周期/对接后端并加载显式模型，不是仅检查命令 |",
        f"| 在线数据源 | {data_smokes.get('summary', {}).get('passed', 0)}/{data_smokes.get('summary', {}).get('case_count', 0)} 通过 | 有界超时的实时 PubChem/RCSB/Materials Project/Catalysis-Hub 请求 |",
        f"| 用户扩展软件清单 | configured={requested_software.get('summary', {}).get('counts', {}).get('configured', 0)}，partial={requested_software.get('summary', {}).get('counts', {}).get('partial', 0)}，manual/API review={requested_software.get('summary', {}).get('manual_or_review', 0)}，specification={requested_software.get('summary', {}).get('counts', {}).get('specification', 0)}；总计 {requested_software.get('summary', {}).get('total', 0)} | 独立 runtime 的真实导入/命令/缓存检查；许可软件和无稳定 API 项不伪报完成 |",
        f"| Pytest | tests={tests.get('tests', '未记录')}，failures={tests.get('failures', '未记录')}，errors={tests.get('errors', '未记录')}，skipped={tests.get('skipped', '未记录')} | `config/pytest_status.xml` |",
        f"| 总结 | **{'核心原子工具箱全部配置；扩展清单仍有人工项' if all_configured and requested_software.get('summary', {}).get('manual_or_review', 0) else ('全部配置完成' if all_configured else '仍有未完成项，见下表')}** | 核心 Backend 健康与用户扩展软件状态分开判定，不把许可/API 阻塞隐藏为“已配置” |",
        "",
        f"Catalog hash：`{catalog['catalog_hash']}`。GPU 设备节点当前{'存在' if gpu_device_present else '未发现'}；GNINA 已通过 CPU/CNN 模式验证，GPU 模式仍由 Agent 通过 `use_gpu` 与 `gpu_device` 显式选择。",
        "",
        "### 配置完成的含义",
        "",
        "- 工具已注册，输入/输出与可选后端双向一致；没有 `run_ase`、`run_periodic_calculation` 一类固定流程工具。",
        "- Scientific Action 必须由 Agent 显式给出 `backend_id`；系统不会选择后端，也不会 fallback。",
        "- 赝势、Slater–Koster 参数集和 MLIP checkpoint 必须由 Agent 显式给出 `ResourceRef`；系统只校验和解析，不会按元素、精度、模型规模或任务领域自动选择。",
        "- `resource_limits` 只表达机械执行约束，不承载科学选择；当前本地执行器实际强制 walltime，并用 `cpu_cores` 约束 OMP/MKL/OpenBLAS/NumExpr 线程。ORCA 映射为 `%pal nprocs`，Gaussian 映射为 `%NProcShared`，GAMESS 映射为 `rungms` 进程数，NAMD 映射为 `+pN`，Amber 在 `cpu_cores>1` 时启动同规模 PMEMD MPI；Gaussian/GAMESS 还分别把 `memory_mb` 映射为 `%Mem`/`MWORDS`。`gpu_count` 只进入请求与溯源，当前新增的 NAMD CUDA 包和 Amber CUDA 构建均不会被自动选择。没有外部调度器时不宣称 CPU/内存已做硬隔离。",
        "- “环境健康”与“真实科学计算”分开记录；核心下载资源后端和在线数据源的证据见第 9、10 节，新增 MESS、MESMER、AutoMeKin、Multiwfn、VESTA 等 runtime 的代表性真实 smoke 见第 12 节及独立配置状态报告。",
        "",
        "## 2. 目录与资源管理约定",
        "",
        "| 目录 | 用途 | 是否提交 Git | 管理规则 |",
        "|---|---|---|---|",
        "| `.toolbox_env/` | 公共 MCP 服务与测试 Python 环境 | 否 | 只承载统一服务，不决定 Agent 可见工具子集 |",
        "| `.tool_envs/<runtime>/` | 后端依赖隔离环境 | 否 | Conda/Pip 软件包与命令按 runtime 隔离 |",
        "| `.software_cache/` | 手工下载、源码构建、数据文件和独立大体积二进制 | 否 | ORCA/OpenMPI、VASP、RMG 数据库、EasySpin、GPAW 数据及其他源码/二进制均使用独立版本化子目录 |",
        "| `.model_cache/` | MACE、NequIP、Allegro、DeePMD 等模型权重缓存 | 否 | 已下载模型按精确文件 ID 和校验值登记；每次计算仍由 Agent 显式选 checkpoint、branch、device 等参数，调用时不联网下载 |",
        "| `download/` | 赝势、参数集及其原始归档 | 否 | 作为只读科学数据源；不把任意路径直接暴露给 Agent |",
        "| `config/toolbox_resources.json` | 受控资源注册表 | 是 | 声明 ID、路径、格式、版本、覆盖、校验值、许可与适用后端 |",
        "| `workspaces/` | 每次任务输出、trace 与 Artifact | 否（保留目录骨架） | 所有普通文件输入/输出继续受 workspace 边界约束 |",
        "",
        "## 3. Agent 显式资源选择接口",
        "",
        "```json",
        "{",
        '  "backend_id": "quantum_espresso",',
        '  "method_spec": {',
        '    "pseudopotentials": {',
        '      "Si": "resource://qe_sssp_1_3_pbe_efficiency/Si"',
        "    },",
        '    "input_dft": "PBE",',
        '    "ecutwfc_ry": 30.0,',
        '    "ecutrho_ry": 240.0',
        "  }",
        "}",
        "```",
        "",
        "等价对象形式为 `{" + '"resource_id":"qe_sssp_1_3_pbe_efficiency","element":"Si"' + "}`。参数集目录使用 `resource://dftb_3ob_3_1`；模型使用独立 ID，例如 `resource://nequip_oam_s_0_1` 或 `resource://deepmd_dpa_3_3_1m`，DeePMD branch 另由 `method_spec.model_branch` 明确给出。未知 ID、缺失元素、路径穿越、运行时管理二进制被当作请求资源等情况都会被拒绝。",
        "",
        "## 4. 公共工具逐项矩阵（44 个）",
        "",
        "| # | Tool / 类型 | 类别 | 功能与主输出 | 输入契约 | Agent 可选后端 / runtime / 健康 | 后端要求的显式字段 | 相关科学资源与联网情况 |",
        "|---:|---|---|---|---|---|---|---|",
    ]

    for index, action in enumerate(actions, start=1):
        backend_cells = []
        requirements = []
        related_resources = []
        for backend_id in action["backend_ids"]:
            backend = backend_by_id[backend_id]
            health = health_by_id[backend_id]
            backend_cells.append(
                f"`{backend_id}` / `{backend['runtime']}` / "
                + ("available" if health.get("available") else "unavailable")
            )
            requirements.append(
                f"`{backend_id}` — {requirements_for_action(backend, action['id'])}"
            )
            for resource in resources_by_backend.get(backend_id, []):
                related_resources.append(f"`{resource['id']}`")
        live = data_smoke_by_action.get(action["id"])
        network_text = "需联网"
        if live:
            network_text += f"；本轮 live={live['status']} ({live.get('elapsed_seconds')} s)"
        elif not action.get("requires_network"):
            network_text = "不要求联网"
        input_text = (
            f"{action.get('input_description') or 'structured ActionRequest'}; "
            f"required={', '.join(action['required_inputs']) or 'none'}; "
            f"optional={', '.join(action['optional_inputs']) or 'none'}"
        )
        kind = "Data" if action["data_action"] else "Scientific"
        resource_text = ", ".join(dict.fromkeys(related_resources)) or "无注册外部科学数据"
        resource_text += "; " + network_text
        lines.append(
            f"| {index} | `{action['id']}`<br>{kind} | {md(CATEGORY_LABELS.get(action['category'], action['category']))} | {md(action['description'])}<br>Primary: `{md(action['primary_output'])}` | {md(input_text)} | {'<br>'.join(backend_cells)} | {'<br>'.join(requirements)} | {resource_text} |"
        )

    lines.extend(
        [
            "",
            f"## 5. Backend 安装与环境矩阵（{len(backends)} 个）",
            "",
            "| Backend | 软件 / runtime 环境 | Python 模块 | 可执行文件与命令变量 | Conda / Pip | 注册科学资源 | License / 健康 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for backend in backends:
        health = backend.get("health") or {}
        runtime_path = relative(health.get("runtime_python"))
        modules = []
        for name, value in (health.get("python_modules") or {}).items():
            modules.append(
                f"`{name}`={'OK' if value.get('available') else 'missing'}"
                + (f" ({value.get('version')})" if value.get("version") else "")
            )
        executable_parts = [
            f"`{name}`={'`' + relative(path) + '`' if path else 'missing'}"
            for name, path in (health.get("executables") or {}).items()
        ]
        executable_parts.extend(
            f"`{name}`={'set' if (health.get('environment') or {}).get(name) else 'missing'}"
            for name in backend.get("environment_variables") or []
        )
        package_text = (
            "Conda: " + (", ".join(backend.get("conda_packages") or []) or "—")
            + "<br>Pip: "
            + (", ".join(backend.get("pip_packages") or []) or "—")
        )
        resource_text = "<br>".join(
            f"`{item['id']}` ({'available' if item.get('available') else 'missing'})"
            for item in resources_by_backend.get(backend["id"], [])
        ) or "—"
        status_text = "available" if health.get("available") else "unavailable"
        if backend["id"] in allowed_unavailable:
            status_text += "（允许缺失）"
        lines.append(
            f"| `{backend['id']}`<br>{md(backend['display_name'])} | runtime=`{backend['runtime']}`<br>python=`{md(runtime_path)}` | {'<br>'.join(modules) or '—'} | {'<br>'.join(executable_parts) or '—'} | {package_text} | {resource_text} | `{backend['license_class']}`<br>**{status_text}** |"
        )

    lines.extend(
        [
            "",
            f"## 6. Backend 能力与显式参数契约（{len(backends)} 个）",
            "",
            "| Backend | 功能说明 | 支持的 Actions | Method schema | 每个 Action 必填 method 字段 | 每个 Action 必填 settings 字段 | 实际验证 / 安装备注 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for backend in backends:
        evidence = []
        smoke_cases = resource_smoke_by_backend.get(backend["id"], [])
        evidence.extend(
            f"real smoke `{smoke['case_id']}`={smoke['status']} ({smoke.get('elapsed_seconds')} s)"
            for smoke in smoke_cases
        )
        data_evidence = [
            item for item in data_smokes.get("cases", []) if item.get("backend") == backend["id"]
        ]
        evidence.extend(
            f"live `{item['action']}`={item['status']} ({item.get('elapsed_seconds')} s)"
            for item in data_evidence
        )
        if not evidence:
            evidence.append(
                "environment health="
                + ("available" if (backend.get("health") or {}).get("available") else "unavailable")
            )
        if backend.get("install_notes"):
            evidence.append(backend["install_notes"])
        lines.append(
            f"| `{backend['id']}` | {md(backend['description'])} | {code_list(backend['capabilities'])} | {map_text(backend.get('method_schema') or {})} | {required_by_action(backend.get('required_method_fields') or {})} | {required_by_action(backend.get('required_setting_fields') or {})} | {md('<br>'.join(evidence))} |"
        )

    lines.extend(
        [
            "",
            "## 7. 隔离运行环境逐项记录",
            "",
            "| Runtime | Group / Conda name / Path | 声明包 | Health checks | Backend 覆盖 | Python / pip check / model checks | 结果 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for group in ("profiles", "support_environments"):
        for name, specification in (profiles_config.get(group) or {}).items():
            result = profile_results.get(name, {})
            packages = (
                "Conda: " + (", ".join(specification.get("conda_packages") or []) or "—")
                + "<br>Pip: "
                + (", ".join(specification.get("pip_packages") or []) or "—")
            )
            checks = specification.get("health_checks") or {}
            check_text = "<br>".join(
                [
                    "modules=" + (", ".join(checks.get("modules") or []) or "—"),
                    "commands=" + (", ".join(checks.get("commands") or []) or "—"),
                    "external=" + (", ".join(checks.get("external_commands") or []) or "—"),
                    "models=" + (", ".join((checks.get("models") or {}).keys()) or "—"),
                ]
            )
            model_text = ", ".join(
                f"{model}={'pass' if item.get('success') else 'fail'}"
                for model, item in (result.get("model_checks") or {}).items()
            ) or "—"
            detail = (
                f"Python {result.get('python_version', '—')}<br>"
                f"pip_check={'pass' if (result.get('dependency_check') or {}).get('success') else 'fail/未记录'}<br>"
                f"models={model_text}"
            )
            lines.append(
                f"| `{name}` | {group}<br>`{specification.get('conda_name')}`<br>`{relative(specification.get('environment'))}` | {packages} | {md(check_text)} | {code_list(specification.get('backends'))} | {detail} | **{'pass' if result.get('required_ok') else 'fail/未记录'}** |"
            )

    lines.extend(
        [
            "",
            "## 8. 注册科学资源与独立软件逐项记录",
            "",
            "| Resource ID | 类型 / 版本 / 格式 | 适用后端 | 本地实体路径 | 来源 / 归档校验 | 覆盖 | 显式选择 | 深度验证 | 科学范围、许可与引用 |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for resource in resources:
        status = resource_status_by_id.get(resource["id"], {})
        archive_records = [
            (label, resource.get(key) or {})
            for label, key in (
                ("archive", "archive"),
                ("distribution", "distribution_archive"),
                ("source", "source_archive"),
            )
            if resource.get(key)
        ]
        archive_parts = [
            f"{label}: `{relative(record.get('path'))}`<br>"
            f"{record.get('checksum_algorithm')}:{record.get('checksum')}"
            for label, record in archive_records
        ]
        if resource.get("checksum"):
            archive_parts.append(
                f"file: {resource.get('checksum_algorithm')}:{resource.get('checksum')}"
            )
        archive_text = "<br>".join(archive_parts) or "—"
        coverage = "runtime executable"
        if resource.get("kind") == "element_file_collection":
            coverage = f"{resource.get('element_count', 0)} elements"
        elif resource.get("kind") == "slater_koster_parameter_set":
            coverage = (
                f"{resource.get('element_count', 0)} elements; "
                f"{resource.get('pair_count', 0)} directed SKF pairs"
            )
        elif resource.get("kind") == "model_checkpoint":
            branches = resource.get("model_branches") or []
            if branches:
                coverage = f"exact checkpoint; {len(branches)} branches"
            elif resource.get("single_task"):
                coverage = "exact single-task checkpoint"
            else:
                coverage = "one exact checkpoint"
        elif resource.get("kind") == "single_file_resource":
            coverage = "one exact registered scientific input file"
        deep = status.get("deep_element_checksums") or {}
        if resource.get("kind") == "backend_executable":
            version_probe = status.get("version_probe") or {}
            validation = (
                f"status={status.get('status', '未记录')}<br>"
                f"checksum={'pass' if (status.get('checksum') or {}).get('ok') else 'fail/未记录'}<br>"
                f"target={'pass' if status.get('target_exists') else 'fail/未记录'}<br>"
                f"version={version_probe.get('matched_text') or version_probe.get('first_line') or '未记录'}"
            )
        elif resource.get("kind") in {"model_checkpoint", "single_file_resource"}:
            validation = (
                f"status={status.get('status', '未记录')}<br>"
                f"size={status.get('size_bytes', resource.get('size_bytes', '—'))} bytes<br>"
                f"checksum={'pass' if (status.get('checksum') or {}).get('ok') else 'fail/未记录'}"
            )
        else:
            validation = (
                f"status={status.get('status', '未记录')}<br>"
                f"files={status.get('file_count', '—')}/{status.get('expected_file_count', '—')}<br>"
                f"deep_checksums={'pass' if deep.get('ok') else ('not_applicable' if not deep else 'fail')}"
            )
        source = resource.get("source_url")
        source_text = f"[official source]({source})<br>{archive_text}" if source else archive_text
        scope = (
            f"{resource.get('scientific_scope', '—')}<br>"
            f"{resource.get('license_and_citation', '—')}"
        )
        lines.append(
            f"| `{resource['id']}` | `{resource.get('kind')}`<br>v{md(resource.get('version'))}<br>{md(resource.get('format'))}<br>XC={md(resource.get('xc_functional'))} | {code_list(resource.get('compatible_backends'))} | `{md(relative(resource.get('path')))}` | {source_text} | {coverage} | `{md(resource.get('selection_syntax', 'runtime-managed'))}` | {validation} | {md(scope)} |"
        )

    lines.extend(["", "### 8.1 元素与 Slater–Koster 覆盖明细", ""])
    for resource in resources:
        elements = resource.get("elements") or []
        if not elements:
            continue
        lines.extend(
            [
                f"<details><summary><code>{resource['id']}</code>：{len(elements)} 个元素"
                + (
                    f"，{resource.get('pair_count')} 个有向参数对"
                    if resource.get("pair_count") is not None
                    else ""
                )
                + "</summary>",
                "",
                "元素：" + ", ".join(f"`{item}`" for item in elements),
            ]
        )
        pairs = resource.get("available_pairs") or []
        if pairs:
            lines.extend(["", "有向 SKF 文件：" + ", ".join(f"`{item}`" for item in pairs)])
        lines.extend(["", "</details>", ""])

    efficiency = next(
        (item for item in resources if item["id"] == "qe_sssp_1_3_pbe_efficiency"),
        {},
    ).get("element_metadata", {})
    precision = next(
        (item for item in resources if item["id"] == "qe_sssp_1_3_pbe_precision"),
        {},
    ).get("element_metadata", {})
    if efficiency or precision:
        lines.extend(
            [
                "### 8.2 SSSP 1.3.0 PBE 每元素文件与推荐截断能",
                "",
                "下表只暴露元数据，不替 Agent 选择 efficiency/precision，也不自动把推荐值写入计算。多元素体系的最终 cutoff 仍需 Agent 明确决定。",
                "",
                "| Element | Efficiency UPF | ecutwfc / ecutrho (Ry) | Precision UPF | ecutwfc / ecutrho (Ry) |",
                "|---|---|---:|---|---:|",
            ]
        )
        for element in sorted(set(efficiency) | set(precision)):
            eff = efficiency.get(element, {})
            pre = precision.get(element, {})
            lines.append(
                f"| `{element}` | `{md(eff.get('filename'))}` | {md(eff.get('cutoff_wfc'))} / {md(eff.get('cutoff_rho'))} | `{md(pre.get('filename'))}` | {md(pre.get('cutoff_wfc'))} / {md(pre.get('cutoff_rho'))} |"
            )

    lines.extend(
        [
            "",
            "## 9. 下载资源真实计算证据",
            "",
            "| Case | Action / Backend | 版本 / 并行 | 显式 ResourceRefs | 用时 | 结果摘要 | 状态 |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for item in resource_smokes.get("cases", []):
        refs = ", ".join(
            f"`{ref.get('resource_id')}`" + (f"/{ref.get('element')}" if ref.get("element") else "")
            for ref in item.get("resource_refs", [])
        ) or "runtime-managed binary"
        execution = (
            f"version={item.get('backend_version') or '—'}<br>"
            f"nprocs={item.get('parallel_processes') or '—'}"
        )
        lines.append(
            f"| `{item['case_id']}` | `{item['action']}` / `{item['backend']}` | {execution} | {refs} | {item.get('elapsed_seconds')} s | {md(item.get('result'))} | **{item['status']}** |"
        )

    lines.extend(
        [
            "",
            "## 10. 在线数据源实时验证",
            "",
            "| Action / Backend | 实时请求 | 用时 | 返回记录数 | 状态 / 说明 |",
            "|---|---|---:|---:|---|",
        ]
    )
    for item in data_smokes.get("cases", []):
        lines.append(
            f"| `{item['action']}` / `{item.get('backend')}` | 有界 timeout，1 条记录 | {item.get('elapsed_seconds')} s | {md(item.get('record_count'))} | **{item['status']}**{('<br>' + md(item.get('error'))) if item.get('error') else ''} |"
        )

    lines.extend(
        [
            "",
            "## 11. ORCA、VASP 与显式 MLIP 配置",
            "",
            "ORCA 已作为 Agent 可显式选择的 `orca` BackendSpec 完成配置；它仍不是固定流程工具，系统不会替 Agent 选择 ORCA，也不会在 ORCA 失败时自动改用其他量化软件。",
            "",
            "- 主程序：`.software_cache/orca/6.1.1/orca`（ORCA 6.1.1，AVX2，共享 OpenMPI 4.1.8 构建）。",
            "- MPI：`.software_cache/openmpi/4.1.8/`；`PATH` 与 `LD_LIBRARY_PATH` 只注入 `quantum`/`reaction` runtime。",
            "- 稳定入口：`.tool_envs/quantum/bin/orca` 与 `.tool_envs/quantum/bin/mpirun`；`CHEMGRAPH_ORCA_COMMAND` 使用主程序完整路径。",
            "- Agent 通过 `backend_id=orca`、`method_spec`、`action_settings` 和 `resource_limits.cpu_cores` 自主决定调用；`cpu_cores>1` 才生成对应 `%pal nprocs`。",
            "- 真实验证覆盖 energy（PAL2）、Hessian、geometry optimization 和 dipole；优化结果显式读取最终 `job.xyz`，不误取轨迹第一帧。",
            "- VASP 6.3.2 已在 `.software_cache/vasp/6.3.2` 编译；`vasp` Backend 只接收 Agent 明确提供的 POTCAR、ENCUT、k 点、XC、展宽和收敛参数。随源码提供的 Si POTCAR 仅用于测试，生产 PAW 数据仍需许可证持有人补充。",
            "- NequIP/Allegro 的 7 个 checkpoint 与 DeePMD 的 5 个 checkpoint 均以独立 `resource://` ID 登记。适配器不会按任务描述选模型；DeePMD 多任务模型还强制 Agent 指定 branch。",
        ]
    )

    lines.extend(
        [
            "",
            "## 12. 用户请求软件与工具配置矩阵（59 项）",
            "",
            "本节覆盖新增请求清单。`configured` 表示依赖 runtime 已准备好，不等同于自动工作流，也不等同于已经为该软件增加公共 BackendSpec；`runtime_only` 保留给 Agent/后续原子适配使用。模型权重仍只进入 `.model_cache`，软件与独立数据只进入 `.software_cache`。",
            "",
            "| 类别 | 名称 | 状态 | 类型 / 许可 | Runtime / 模块 / 命令 | 缓存与模型 | Agent 接口状态 | 功能、限制与手动处理 |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in requested_software.get("software", []):
        verification = item.get("verification") or {}
        environment = item.get("environment_detail") or {}
        modules = []
        for name, value in (verification.get("modules") or {}).items():
            if value.get("available"):
                state = "OK"
            elif "timed out" in str(value.get("error") or ""):
                state = "timeout"
            else:
                state = "failed"
            modules.append(
                f"`{name}`={state}"
                + (f" ({value.get('version')})" if value.get("version") else "")
            )
        commands = [
            f"`{name}`={'OK' if path else 'missing'}"
            for name, path in (verification.get("commands") or {}).items()
        ]
        runtime_text = (
            f"`{md(environment.get('name'))}` / `{md(environment.get('path'))}`<br>"
            f"modules: {', '.join(modules) or '—'}<br>"
            f"commands: {', '.join(commands) or '—'}"
        )
        cache_parts = []
        for value, result in (verification.get("cache_paths") or {}).items():
            cache_parts.append(
                f"`{md(value)}`={'OK' if result.get('exists') else 'missing'}"
            )
        if item.get("model_cache"):
            cache_parts.append(
                f"model=`{md(item['model_cache'])}`（显式选择；调用时不自动下载）"
            )
        official = item.get("official_url")
        notes = f"{md(item.get('role'))}<br>{md(item.get('notes'))}"
        if official:
            notes += f"<br>[official]({official})"
        lines.append(
            f"| {md(item.get('category'))} | `{md(item.get('name'))}` | **{md(item.get('status'))}** | `{md(item.get('kind'))}`<br>{md(item.get('license'))} | {runtime_text} | {'<br>'.join(cache_parts) or '—'} | `{md(item.get('public_adapter'))}` | {notes} |"
        )

    lines.extend(
        [
            "",
            "## 13. 重放命令",
            "",
            "```bash",
            ".toolbox_env/bin/python scripts/configure_toolbox_resources.py",
            ".toolbox_env/bin/python scripts/run_scientific_resource_smokes.py",
            ".toolbox_env/bin/python scripts/run_data_source_smokes.py",
            ".toolbox_env/bin/python scripts/check_mcp_profile_envs.py --check-models --timeout-seconds 600",
            ".toolbox_env/bin/python scripts/audit_requested_software.py --timeout-seconds 20",
            ".toolbox_env/bin/python -m pytest -q --junitxml=config/pytest_status.xml",
            ".toolbox_env/bin/python scripts/verify_toolbox.py --smoke",
            ".toolbox_env/bin/python scripts/generate_tool_resource_matrix.py",
            "```",
            "",
            "这些命令只验证和执行 Agent 已明确指定的选择；它们不会形成面向 benchmark 任务的固定科学工作流。",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT)
    print(
        json.dumps(
            {
                "all_configured": all_configured,
                "unavailable": unavailable,
                "unexpected_unavailable": unexpected_unavailable,
                "profile_failures": profile_failures,
                "missing_profile_results": missing_profile_results,
            },
            ensure_ascii=False,
        )
    )
    return 0 if all_configured else 1


if __name__ == "__main__":
    raise SystemExit(main())
