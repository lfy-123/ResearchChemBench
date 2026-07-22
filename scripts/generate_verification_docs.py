#!/usr/bin/env python3
"""Generate the canonical six-task audit and current toolbox capability catalog."""

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "verification"
TASK_REPORT = OUTPUT_DIR / "HETEROBIARYL_PV_SIX_TASK_VERIFICATION_20260722.md"
TOOLBOX_REPORT = OUTPUT_DIR / "CHEMISTRY_TOOLBOX_CURRENT_CAPABILITY_CATALOG_20260722.md"

TASK_WORKSPACES = {
    "Heterobiaryl_PV_01_Protonation": (
        ROOT
        / "workspaces/cli_runs/batch_20260722_022026_75d612/"
        "Heterobiaryl_PV_01_Protonation_opencode_20260722_022026_982eca"
    ),
    "Heterobiaryl_PV_02_CC_Selectivity": (
        ROOT
        / "workspaces/cli_runs/batch_20260722_022026_75d612/"
        "Heterobiaryl_PV_02_CC_Selectivity_opencode_20260722_022026_2ad54f"
    ),
    "Heterobiaryl_PV_03_CC_vs_CO": (
        ROOT
        / "workspaces/cli_runs/batch_20260722_022026_75d612/"
        "Heterobiaryl_PV_03_CC_vs_CO_opencode_20260722_023239_04e948"
    ),
    "Heterobiaryl_PV_04_Coupling_Mechanism": (
        ROOT
        / "workspaces/cli_runs/batch_20260722_022026_75d612/"
        "Heterobiaryl_PV_04_Coupling_Mechanism_opencode_20260722_024020_82a222"
    ),
    "Heterobiaryl_PV_05_Rate_Determining_Step": (
        ROOT
        / "workspaces/cli_runs/batch_20260722_022026_75d612/"
        "Heterobiaryl_PV_05_Rate_Determining_Step_opencode_20260722_024535_72f8c8"
    ),
    "Heterobiaryl_PV_06_End_to_End": (
        ROOT
        / "workspaces/cli_runs/batch_20260722_033901_2c5d7e/"
        "Heterobiaryl_PV_06_End_to_End_opencode_20260722_033901_6f1773"
    ),
}

SHORT_RESULT = {
    "Heterobiaryl_PV_01_Protonation": (
        "复现 P0/P1/P2 约 31.1/19.5/14.0 kcal mol⁻¹；趋势正确，RRHO 与参考 mRRHO 略有差异。"
    ),
    "Heterobiaryl_PV_02_CC_Selectivity": (
        "路径和驻点赋值错误，得到错误的 ΔΔG‡ 并误判为热力学控制。"
    ),
    "Heterobiaryl_PV_03_CC_vs_CO": (
        "正确判断 C−C 为主并承认 C−O TS 缺失，但把 C−C 势垒算成约 21.3 而非 14.3 kcal mol⁻¹。"
    ),
    "Heterobiaryl_PV_04_Coupling_Mechanism": (
        "识别 asynchronous 特征，但误判为 concerted，遗漏 dearomatized intermediate。"
    ),
    "Heterobiaryl_PV_05_Rate_Determining_Step": (
        "实验取代基趋势正确，但把 ligand coupling 错当整体 RDS，未分离速率与选择性控制。"
    ),
    "Heterobiaryl_PV_06_End_to_End": (
        "完成 66 结构/198 记录审计和可复现报告，但能量、P(V) 机理、RDS 与中间体判断存在系统性错误。"
    ),
}

PAPER_FIT = {
    "scientific_data_interchange": (
        "带 Gaussian/ORCA/NWChem 等输出、QCSchema 记录或需要统一解析/验证的论文"
    ),
    "structure_and_system": (
        "构象搜索、质子化、部分电荷、力场参数化、溶剂化、晶体/表面建模论文"
    ),
    "cheminformatics": (
        "描述符、指纹、相似性、子结构和分子标识符数据集论文"
    ),
    "molecular_electronic": (
        "分子 DFT/从头算、几何优化、频率、热化学、激发态、光谱和波函数分析论文"
    ),
    "reaction_and_kinetics": (
        "反应路径、TS/IRC、自由能剖面、选择性、速率常数和反应网络论文"
    ),
    "molecular_dynamics": (
        "经典/第一性原理/增强采样 MD、轨迹分析、自由能与输运论文"
    ),
    "periodic_and_phonons": (
        "周期 DFT、结构弛豫、能带/DOS、声子、热输运和多体材料计算论文"
    ),
    "docking": (
        "蛋白-配体对接、构象排序和结构准备论文"
    ),
    "data_sources": (
        "需要 PubChem、NIST WebBook、Materials Project、PDB 等公开数据检索的任务"
    ),
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _escape(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", "<br>")


def _link(path: Path, label: str | None = None, *, base: Path) -> str:
    relative = os.path.relpath(path, base.parent).replace(os.sep, "/")
    return f"[{label or path.name}]({relative})"


def _trace_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    values = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            values.append(item)
    return values


def _judge_history(workspace: Path) -> list[dict[str, Any]]:
    return [
        item
        for item in _trace_events(workspace / "_score_history.jsonl")
        if item.get("history_source") == "judge_call"
    ]


def _run_length_tools(names: list[str]) -> str:
    if not names:
        return "无"
    chunks: list[str] = []
    current = names[0]
    count = 1
    for name in names[1:]:
        if name == current:
            count += 1
            continue
        chunks.append(f"`{current}`×{count}" if count > 1 else f"`{current}`")
        current = name
        count = 1
    chunks.append(f"`{current}`×{count}" if count > 1 else f"`{current}`")
    return " → ".join(chunks)


def _data_inventory(workspace: Path) -> dict[str, Any]:
    root = workspace / "data" / "benchmark_data"
    files = [path for path in root.rglob("*") if path.is_file()]
    top = Counter(path.relative_to(root).parts[0] for path in files)
    suffix = Counter(path.suffix.lower() or "<no extension>" for path in files)
    return {
        "root": root,
        "file_count": len(files),
        "total_bytes": sum(path.stat().st_size for path in files),
        "top_level_counts": dict(sorted(top.items())),
        "suffix_counts": dict(sorted(suffix.items())),
    }


def _task_artifacts(workspace: Path) -> list[tuple[str, int]]:
    values = []
    for directory in ("code", "outputs", "report"):
        root = workspace / directory
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file():
                values.append((str(path.relative_to(workspace)), path.stat().st_size))
    values.sort()
    return values


def generate_task_report() -> None:
    from evaluation.token_usage import workspace_token_usage
    from evaluation.trace import load_native_agent_trace

    records = []
    for task_id, workspace in TASK_WORKSPACES.items():
        task_dir = ROOT / "tasks" / task_id
        info = _load(task_dir / "task_info.json")
        truth = _load(task_dir / "target_study" / "ground_truth.json")
        meta = _load(workspace / "_meta.json")
        score = _load(workspace / "_score.json")
        usage = workspace_token_usage(workspace)
        scientific = _trace_events(workspace / "_tool_trace.jsonl")
        native = load_native_agent_trace(workspace)
        history = _judge_history(workspace)
        judge_total = sum(
            int((item.get("judge_usage") or {}).get("total_tokens") or 0)
            for item in history
        )
        records.append(
            {
                "task_id": task_id,
                "task_dir": task_dir,
                "workspace": workspace,
                "info": info,
                "truth": truth,
                "meta": meta,
                "score": score,
                "usage": usage,
                "scientific": scientific,
                "native": native,
                "judge_history": history,
                "judge_total": judge_total,
            }
        )

    first_inventory = _data_inventory(records[0]["workspace"])
    total_agent = sum(item["usage"]["tokens"]["total"] for item in records)
    total_cache = sum(item["usage"]["tokens"]["cache_read"] for item in records)
    total_judge = sum(item["judge_total"] for item in records)
    lines = [
        "# Heterobiaryl P(V) 六任务运行验证台账",
        "",
        "生成日期：2026-07-22  ",
        "数据来源：六个最终有效 OpenCode workspace、任务公开输入、隐藏参考答案和 append-only 评分历史。本文档不重新运行 Agent 或 Judge。",
        "",
        "## 1. 总览",
        "",
        "| 任务 | 指令主题 | 分数 | Agent steps / sessions | Agent token | cache read | Scientific MCP 成功/总数 | Native 成功/总数 | 结果摘要 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in records:
        meta = item["meta"]
        score = item["score"]
        scientific = item["scientific"]
        native = item["native"]
        usage = item["usage"]
        lines.append(
            "| {task} | {category} | {score}/{maximum} | {steps}/{sessions} | {tokens:,} | "
            "{cache:,} | {s_ok}/{s_all} | {n_ok}/{n_all} | {summary} |".format(
                task=item["task_id"].replace("Heterobiaryl_PV_", "Q"),
                category=_escape(item["info"].get("category")),
                score=score.get("score"),
                maximum=score.get("score_max"),
                steps=usage["model_step_count"],
                sessions=usage["session_count"],
                tokens=usage["tokens"]["total"],
                cache=usage["tokens"]["cache_read"],
                s_ok=sum(event.get("status") in {"success", "partial_success"} for event in scientific),
                s_all=len(scientific),
                n_ok=sum(event.get("status") == "success" for event in native),
                n_all=len(native),
                summary=_escape(SHORT_RESULT[item["task_id"]]),
            )
        )
    lines.extend(
        [
            "",
            f"- 六任务 Agent token 合计：**{total_agent:,}**。",
            f"- 其中 cache-read：**{total_cache:,}**。",
            f"- 当前评分历史中可核查的 Judge token 合计：**{total_judge:,}**。",
            "- 上述运行发生在渐进式发现重构之前，因此每轮均携带完整 Action schema；这些数据可作为后续 progressive 复跑的历史基线。",
            "",
            "## 2. 六任务共同输入数据",
            "",
            "六题使用同一份匿名化证据包，但科学问题和评分 reference 不同。任务目录中的 `computational_records.zip` 是指向共享公开包的符号链接，运行时会校验 SHA-256 后解压为只读 `data/benchmark_data`。",
            "",
            f"- 公开 archive SHA-256：`97fa402aec3fa9191d0352485c7c4a8c77415d47d7c917dcb1cc0548f04d495d`。",
            f"- 解压文件总数：**{first_inventory['file_count']}**。",
            f"- 解压总字节：**{first_inventory['total_bytes']:,} B**。",
            f"- 顶层文件/目录计数：`{json.dumps(first_inventory['top_level_counts'], ensure_ascii=False)}`。",
            f"- 文件扩展名计数：`{json.dumps(first_inventory['suffix_counts'], ensure_ascii=False)}`。",
            "",
            "关键公开文件：",
            "",
            "- `README.md`：数据包结构说明；",
            "- `candidate_manifest.json`：匿名候选结构和体系信息；",
            "- `record_manifest.json`：计算记录、方法和文件关联；",
            "- `starting_structure_manifest.json`：起始构象清单；",
            "- `data_limitations.json`：缺失 IRC/C−O TS 等边界；",
            "- `experimental_evidence/experimental_observations.csv|json`：匿名实验观察；",
            "- `records/`、`structures/` 和 starting structures：Gaussian/ORCA 记录与几何数据。",
            "",
        ]
    )

    for index, item in enumerate(records, 1):
        task_id = item["task_id"]
        info = item["info"]
        truth = item["truth"]
        meta = item["meta"]
        score = item["score"]
        usage = item["usage"]
        scientific = item["scientific"]
        native = item["native"]
        workspace = item["workspace"]
        task_dir = item["task_dir"]
        native_counts = Counter(str(event.get("tool")) for event in native)
        latest_judge = score.get("judge_usage") or {}
        lines.extend(
            [
                f"## {index + 2}. {task_id}",
                "",
                "### 任务指令",
                "",
                f"> {info['task']}",
                "",
                "### 任务数据声明",
                "",
                "| 名称 | workspace 路径 | 类型 | 描述 |",
                "|---|---|---|---|",
            ]
        )
        for datum in info.get("data", []):
            lines.append(
                f"| {_escape(datum.get('name'))} | `{_escape(datum.get('path'))}` | "
                f"{_escape(datum.get('type'))} | {_escape(datum.get('description'))} |"
            )
        lines.extend(
            [
                "",
                "Archive extraction：",
                "",
                "```json",
                json.dumps(info.get("archive_extractions", []), indent=2, ensure_ascii=False),
                "```",
                "",
                "### 最终运行与 token",
                "",
                f"- Workspace：{_link(workspace, workspace.name, base=TASK_REPORT)}",
                f"- Task definition：{_link(task_dir / 'task_info.json', 'task_info.json', base=TASK_REPORT)}",
                f"- Ground truth：{_link(task_dir / 'target_study/ground_truth.json', 'ground_truth.json', base=TASK_REPORT)}",
                f"- 状态：`{meta.get('status')}`；模型：`{meta.get('model')}`；耗时：`{meta.get('duration_seconds')} s`。",
                "",
                "| 指标 | 数值 |",
                "|---|---:|",
                f"| Agent model steps | {usage['model_step_count']} |",
                f"| Agent sessions | {usage['session_count']} |",
                f"| Agent total tokens | {usage['tokens']['total']:,} |",
                f"| Agent uncached input | {usage['tokens']['input']:,} |",
                f"| Agent cache read | {usage['tokens']['cache_read']:,} |",
                f"| Agent output | {usage['tokens']['output']:,} |",
                f"| Agent reasoning | {usage['tokens']['reasoning']:,} |",
                f"| First model step total | {usage['first_model_step_tokens']['total']:,} |",
                f"| Latest Judge total | {int(latest_judge.get('total_tokens') or 0):,} |",
                f"| Judge calls retained in history | {len(item['judge_history'])} |",
                f"| Retained Judge token total | {item['judge_total']:,} |",
                "",
                "### 智能体工具调用流程",
                "",
                f"Scientific MCP：{sum(e.get('status') in {'success', 'partial_success'} for e in scientific)}/{len(scientific)} 成功。",
                "",
            ]
        )
        if scientific:
            lines.extend(
                [
                    "| 序号 | Action | 状态 | 请求 Backend/source | 错误摘要 |",
                    "|---:|---|---|---|---|",
                ]
            )
            for event in scientific:
                request = (event.get("arguments") or {}).get("request") or {}
                selected = request.get("backend_id") or request.get("source_id") or "—"
                error = event.get("error") or {}
                if isinstance(error, dict):
                    error_text = error.get("message") or error.get("code") or ""
                else:
                    error_text = str(error or "")
                lines.append(
                    f"| {event.get('sequence')} | `{_escape(event.get('tool'))}` | "
                    f"{_escape(event.get('status'))} | `{_escape(selected)}` | {_escape(error_text)[:240]} |"
                )
        else:
            lines.append("该任务没有进入 Scientific MCP dispatcher，主要使用 Agent 原生文件/脚本工具完成分析。")
        lines.extend(
            [
                "",
                f"Native/OpenCode 工具：{sum(e.get('status') == 'success' for e in native)}/{len(native)} 成功。",
                "",
                "| 工具 | 次数 |",
                "|---|---:|",
            ]
        )
        for name, count in native_counts.most_common():
            lines.append(f"| `{_escape(name)}` | {count} |")
        ordered = [str(event.get("tool")) for event in native]
        lines.extend(
            [
                "",
                "连续相同调用压缩后的顺序：",
                "",
                _run_length_tools(ordered),
                "",
                "可核查轨迹：",
                "",
            ]
        )
        if (workspace / "_tool_trace.jsonl").is_file():
            lines.append(
                f"- {_link(workspace / '_tool_trace.jsonl', '_tool_trace.jsonl', base=TASK_REPORT)}：Scientific MCP 结果与 provenance；"
            )
        else:
            lines.append("- `_tool_trace.jsonl`：本任务未调用 Scientific MCP，因此未生成该文件；")
        lines.extend(
            [
                f"- {_link(workspace / '_model_io.jsonl', '_model_io.jsonl', base=TASK_REPORT)}：主/子 Agent 每步输入输出、reasoning、tool part 和 token；",
                f"- {_link(workspace / '_agent_output.jsonl', '_agent_output.jsonl', base=TASK_REPORT)}：主 Agent CLI 原始事件；",
                "",
                "### 智能体结果",
                "",
                f"**结果摘要：** {SHORT_RESULT[task_id]}",
                "",
                f"- 最终报告：{_link(workspace / 'report/report.md', 'report/report.md', base=TASK_REPORT)}",
                f"- 最终分数：**{score.get('score')}/{score.get('score_max')}**。",
                f"- Judge 总结：{score.get('rationale', '')}",
                "",
                "低于满分的评分项：",
                "",
                "| Criterion | 得分 | 上限 | 裁判说明 |",
                "|---|---:|---:|---|",
            ]
        )
        deductions = [
            criterion
            for criterion in score.get("criteria", [])
            if float(criterion.get("score", 0)) < float(criterion.get("max_score", 0))
        ]
        if deductions:
            for criterion in deductions:
                lines.append(
                    f"| `{_escape(criterion.get('id'))}` | {criterion.get('score')} | "
                    f"{criterion.get('max_score')} | {_escape(criterion.get('rationale'))} |"
                )
        else:
            lines.append("| — | — | — | 无扣分项 |")
        report_text = (workspace / "report" / "report.md").read_text(
            encoding="utf-8", errors="replace"
        )
        lines.extend(
            [
                "",
                "完整 Agent 报告快照：",
                "",
                "```markdown",
                report_text.rstrip(),
                "```",
                "",
                "### 参考答案",
                "",
                "```json",
                json.dumps(truth.get("expected_result"), indent=2, ensure_ascii=False),
                "```",
                "",
                "参考条件与证据边界：",
                "",
                "```json",
                json.dumps(truth.get("reference_evidence"), indent=2, ensure_ascii=False),
                "```",
                "",
                "### 主要产物文件",
                "",
                "| 路径 | 大小 |",
                "|---|---:|",
            ]
        )
        artifacts = _task_artifacts(workspace)
        for relative, size in artifacts[:100]:
            lines.append(f"| `{_escape(relative)}` | {size:,} B |")
        if len(artifacts) > 100:
            lines.append(f"| … | 另有 {len(artifacts) - 100} 个文件，见 workspace |")
        lines.append("")

    lines.extend(
        [
            "## 9. 跨任务观察",
            "",
            "1. Q1 证明相同数据包足以恢复高质量统一势垒；Q2–Q6 的低分因此不能简单归因于输入数据不可用。",
            "2. 旧运行中大量 token 来自完整工具 schema 和多轮 cache-read；新的 progressive 暴露方式应在复跑时显著降低该部分。",
            "3. Scientific MCP 失败主要是 Agent 漏字段、显式上限过小或 JSON/路径错误；native 脚本提供了开放式恢复能力。",
            "4. Q2/Q3 的子 Agent 工具已经从 `_model_io.jsonl` 纳入评分，因此低分反映最终科学赋值而非轨迹遗漏。",
            "5. 六题最难的共同点是匿名结构角色赋值、统一热化学口径和机理步骤角色分离，而不是单一软件是否安装。",
            "",
        ]
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TASK_REPORT.write_text("\n".join(lines), encoding="utf-8")


def generate_toolbox_report() -> None:
    from chemistry_toolbox.mcp.execution_models import (
        AnalysisRuntimeListRequest,
        SoftwareListRequest,
    )
    from chemistry_toolbox.mcp.software_catalog import (
        list_analysis_runtimes,
        list_software,
        load_native_guides,
    )
    from researchchem_toolbox.catalog import CATEGORY_LABELS, catalog_snapshot

    snapshot = catalog_snapshot(include_health=True, discovery_mode="progressive")
    actions = snapshot["actions"]
    backends = snapshot["backends"]
    resources = snapshot["resources"]
    backend_by_id = {item["id"]: item for item in backends}
    software = list_software(SoftwareListRequest(limit=500))["software"]
    guides = load_native_guides()["software"]
    runtimes = list_analysis_runtimes(
        AnalysisRuntimeListRequest(available_only=False)
    )["runtimes"]
    available_software = sum(bool(item.get("available")) for item in software)
    registered_software = sum(bool(item.get("backend_registered")) for item in software)
    native_software = sum(bool(item.get("native_commands")) for item in software)

    lines = [
        "# ResearchChemBench 当前化学工具箱能力目录",
        "",
        "生成日期：2026-07-22  ",
        f"Catalog hash：`{snapshot['catalog_hash']}`  ",
        "用途：帮助从计算化学论文中选择与当前工具箱能力匹配、同时又能评估 Agent 自主编排的软件和科学任务。",
        "",
        "## 1. 当前规模与概念关系",
        "",
        f"- 预定义 Actions：**{len(actions)}**（Scientific {sum(not x['data_action'] for x in actions)}，Data {sum(x['data_action'] for x in actions)}）。",
        f"- BackendSpecs：**{len(backends)}**。一个软件可因不同适配器/算法注册多个 Backend，一个 Backend 也可服务多个 Action。",
        f"- 软件、程序库、工作流组件和数据接口 inventory：**{len(software)}**，当前探测可用 **{available_software}**。",
        f"- 其中直接注册 Backend 的 inventory 项：**{registered_software}**；含 reviewed native command 的项：**{native_software}**。",
        f"- 可编程分析 runtime：**{len(runtimes)}**。",
        f"- 注册科学资源：**{len(resources)}**。",
        "- 默认 MCP：20 个首屏工具；完整 Catalog 通过 progressive discovery 按需加载。",
        "",
        "```text",
        "论文科学步骤 ──> Action（做什么） ──> Backend（由谁实现）",
        "                     │                    │",
        "                     │                    ├─ Python 库/算法适配器",
        "                     │                    ├─ 外部计算软件",
        "                     │                    └─ 数据接口",
        "                     ├─ 若已有 Action：execute_action",
        "                     ├─ 若无 Action：软件原生输入 + submit_native_job",
        "                     └─ 若需自定义分析：Agent 程序 + submit_analysis_program",
        "```",
        "",
        "因此本文档中的 Action 数、Backend 数和 software inventory 数不会相等，这是多对多关系，不是重复注册错误。",
        "",
        "## 2. 按领域的 Action 覆盖与论文匹配建议",
        "",
        "| 领域 | Action 数 | 主要用途 | 适合寻找的论文 | Action IDs |",
        "|---|---:|---|---|---|",
    ]
    for category, label in CATEGORY_LABELS.items():
        category_actions = [item for item in actions if item["category"] == category]
        lines.append(
            f"| `{category}` | {len(category_actions)} | {_escape(label)} | "
            f"{_escape(PAPER_FIT[category])} | {'<br>'.join('`' + item['id'] + '`' for item in category_actions)} |"
        )

    lines.extend(
        [
            "",
            "## 3. 全部预定义 Actions",
            "",
            "Action 是一个原子科学行为，不是固定 workflow。Agent 可自由组合、重复、分支或跳过。",
            "",
            "| Action | 领域 | 功能 | 主输出 | 选择策略 | 必需输入 | 可选输入 | 可用 Backends |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for action in actions:
        providers = []
        for backend_id in action["backend_ids"]:
            status = (backend_by_id[backend_id].get("health") or {}).get("status", "not_probed")
            providers.append(f"`{backend_id}` ({status})")
        lines.append(
            f"| `{action['id']}` | `{action['category']}` | {_escape(action['description'])} | "
            f"`{_escape(action['primary_output'])}` | `{action['selection_policy']}` | "
            f"{', '.join('`' + x + '`' for x in action['required_inputs']) or '—'} | "
            f"{', '.join('`' + x + '`' for x in action['optional_inputs']) or '—'} | "
            f"{'<br>'.join(providers)} |"
        )

    lines.extend(
        [
            "",
            "## 4. 全部 BackendSpecs",
            "",
            "| Backend | 显示名称 | Runtime | 状态 | License | 能力数 | Python modules | Executables | 外部资源 |",
            "|---|---|---|---|---|---:|---|---|---|",
        ]
    )
    for backend in backends:
        health = backend.get("health") or {}
        lines.append(
            f"| `{backend['id']}` | {_escape(backend['display_name'])} | `{backend['runtime']}` | "
            f"{health.get('status', 'not_probed')} | {_escape(backend['license_class'])} | "
            f"{len(backend['capabilities'])} | {_escape(', '.join(backend['python_modules']) or '—')} | "
            f"{_escape(', '.join(backend['executables']) or '—')} | "
            f"{_escape('; '.join(backend['required_data_resources']) or '—')} |"
        )
    lines.extend(["", "### 4.1 Backend 到 Action 的完整映射", ""])
    for backend in backends:
        lines.extend(
            [
                f"#### `{backend['id']}` — {backend['display_name']}",
                "",
                f"- 说明：{backend['description']}",
                f"- Runtime：`{backend['runtime']}`；状态：`{(backend.get('health') or {}).get('status', 'not_probed')}`；License：`{backend['license_class']}`。",
                f"- Actions（{len(backend['capabilities'])}）：" + ", ".join(f"`{item}`" for item in backend["capabilities"]),
                f"- Conda：{', '.join(backend['conda_packages']) or '—'}；Pip：{', '.join(backend['pip_packages']) or '—'}。",
                f"- 安装说明：{backend.get('install_notes') or '—'}",
                "",
            ]
        )

    lines.extend(
        [
            "## 5. 软件、程序库、工作流组件和数据接口 Inventory",
            "",
            "该表不仅包含独立计算软件，也包含 Python 库、工作流系统、可视化程序和外部数据接口。`backend_registered=false` 不等于无用：它仍可能通过 native command 或 Agent-authored Python 程序使用。",
            "",
            "| Software ID | 名称 | 可用 | Backend registered | Runtime | 版本 | Actions | Native commands | 本地文档 |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in software:
        commands = [
            f"`{command['executable']}` ({'available' if command.get('available') else 'missing'})"
            for command in item.get("native_commands", [])
        ]
        lines.append(
            f"| `{item['software_id']}` | {_escape(item['display_name'])} | "
            f"{'yes' if item.get('available') else 'no'} | "
            f"{'yes' if item.get('backend_registered') else 'no'} | "
            f"`{_escape(item.get('runtime'))}` | {_escape(', '.join(item.get('detected_versions') or []) or '—')} | "
            f"{'<br>'.join('`' + x + '`' for x in item.get('actions', [])) or '—'} | "
            f"{'<br>'.join(commands) or '—'} | {'yes' if item.get('documentation_cached') else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## 6. Reviewed 软件原生命令指南",
            "",
            "以下软件可由 Agent 在查看 `inspect_software` 后编写原生输入并显式执行。表中只是命令入口，不代表固定科学流程。",
            "",
            "| Software | 用途 | 命令 | Synopsis | 输入模式 |",
            "|---|---|---|---|---|",
        ]
    )
    for software_id, guide in guides.items():
        for executable, command in (guide.get("commands") or {}).items():
            lines.append(
                f"| `{software_id}` | {_escape(guide.get('purpose'))} | `{executable}` | "
                f"`{_escape(command.get('synopsis'))}` | `{_escape(command.get('input_mode'))}` |"
            )

    lines.extend(
        [
            "",
            "## 7. 可编程分析 Runtimes",
            "",
            "| Runtime | 可用 | Python | Modules | Commands | 关联 Backends |",
            "|---|---|---|---|---|---|",
        ]
    )
    for runtime in runtimes:
        lines.append(
            f"| `{runtime['runtime']}` | {'yes' if runtime.get('available') else 'no'} | "
            f"`{_escape(runtime.get('python'))}` | {_escape(', '.join(runtime.get('modules') or []) or '—')} | "
            f"{_escape(', '.join(runtime.get('configured_commands') or []) or '—')} | "
            f"{_escape(', '.join(runtime.get('backends') or []) or '—')} |"
        )

    lines.extend(
        [
            "",
            "## 8. 注册科学资源",
            "",
            "| Resource | Kind | 版本 | 格式 | 可用 | 兼容 Backend | 选择语法 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for resource in resources:
        lines.append(
            f"| `{resource['id']}` | `{_escape(resource.get('kind'))}` | "
            f"{_escape(resource.get('version'))} | {_escape(resource.get('format'))} | "
            f"{'yes' if resource.get('available') else 'no'} | "
            f"{_escape(', '.join(resource.get('compatible_backends') or []))} | "
            f"`{_escape(resource.get('selection_syntax'))}` |"
        )

    lines.extend(
        [
            "",
            "## 9. 用该目录筛选论文的建议",
            "",
            "### 9.1 优先选择",
            "",
            "1. 提供原始输入/输出、结构、轨迹或补充数据，可在隔离环境中重算或重新解析。",
            "2. 包含 3–15 个相互依赖的科学步骤，既能调用已有 Action，也需要 Agent 在原生软件或 Python 层补充分析。",
            "3. 关键软件位于第 5/6 节且当前 available，或者论文数据足以只做后处理和验证。",
            "4. 参考答案能拆成过程 rubric：输入审计、方法选择、计算、验证、结论和不确定性。",
            "5. 有竞争假设、路径或模型，避免只靠一次查询即可回答。",
            "",
            "### 9.2 谨慎选择",
            "",
            "1. 依赖未提供 license、专有势函数或不可获得训练数据的论文。",
            "2. 单次计算需要超出 benchmark 节点预算的大规模周期 DFT、长时间 MD 或高阶多参考计算。",
            "3. 关键结论只存在于图片、人工判断或未公开脚本中，无法形成可核查 reference。",
            "4. 所有步骤都被一个专用脚本完全封装，无法评价 Agent 的编排决策。",
            "",
            "### 9.3 推荐的论文任务形状",
            "",
            "- 构象生成 → 多级量化优化/频率 → GoodVibes 热化学 → 反应自由能/选择性；",
            "- 反应物/TS/产物记录解析 → IRC/键变化验证 → 速率常数与实验趋势整合；",
            "- 晶体结构标准化 → 周期弛豫 → 能带/DOS/声子 → 稳定性或输运结论；",
            "- 系统构建 → MD/增强采样 → 轨迹/自由能分析 → 机理结论；",
            "- 蛋白/配体准备 → docking → pose/score 分析 → 与实验活性比较；",
            "- 公共数据库检索 → 结构/性质标准化 → 计算验证 → 数据驱动结论。",
            "",
            "## 10. 相关现有详细文档",
            "",
            f"- {_link(ROOT / 'chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md', '工具/Backend/资源矩阵', base=TOOLBOX_REPORT)}",
            f"- {_link(ROOT / 'chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md', '软件能力矩阵', base=TOOLBOX_REPORT)}",
            f"- {_link(ROOT / 'chemistry_toolbox/docs/TOOLBOX_STATUS.md', '当前健康状态', base=TOOLBOX_REPORT)}",
            f"- {_link(ROOT / 'chemistry_toolbox/docs/PROGRESSIVE_TOOL_DISCOVERY_REFACTOR_REPORT_20260722.md', '渐进式发现与 token 报告', base=TOOLBOX_REPORT)}",
            "",
        ]
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TOOLBOX_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    generate_task_report()
    generate_toolbox_report()
    print(TASK_REPORT)
    print(TOOLBOX_REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
