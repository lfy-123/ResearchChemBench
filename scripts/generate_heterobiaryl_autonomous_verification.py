#!/usr/bin/env python3
"""Generate the autonomous-computation audit for the six Heterobiaryl P(V) tasks."""

from __future__ import annotations

import hashlib
import json
import os
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ARCHIVE = ROOT / "tasks/_heterobiaryl_pv_shared/public/autonomous_inputs.zip"
REPORT = (
    ROOT
    / "docs/verification/"
    "HETEROBIARYL_PV_AUTONOMOUS_COMPUTATION_VERIFICATION_20260722.md"
)
TASK_IDS = [
    "Heterobiaryl_PV_01_Protonation",
    "Heterobiaryl_PV_02_CC_Selectivity",
    "Heterobiaryl_PV_03_CC_vs_CO",
    "Heterobiaryl_PV_04_Coupling_Mechanism",
    "Heterobiaryl_PV_05_Rate_Determining_Step",
    "Heterobiaryl_PV_06_End_to_End",
]

REFERENCE_SUMMARIES = {
    TASK_IDS[0]: (
        "P0/P1/P2 的 BiPy 活化自由能约为 30/20/14 kcal mol-1；逐次 N-质子化降低势垒。"
        "第一次约降低 10，第二次约降低 6 kcal mol-1。"
    ),
    TASK_IDS[1]: (
        "P0/P1/P2 中 BiPy/PhPy 势垒分别约为 30/37、20/27、14/25 kcal mol-1；"
        "BiPy 动力学占优，强放能产物热力学不是选择性来源。"
    ),
    TASK_IDS[2]: (
        "P2 中 C-C 与 C-O 参考势垒约为 14 和 18 kcal mol-1；差约 4 kcal mol-1，"
        "标准酸性乙醇条件下 C-C 路径动力学占优。"
    ),
    TASK_IDS[3]: (
        "关键偶联为 stepwise、asynchronous apical-to-equatorial ligand coupling；"
        "TS 后存在 dearomatized intermediate，氧孤对沿关键坐标变化很小。"
    ),
    TASK_IDS[4]: (
        "标准酸性条件下主要决速步骤是醇/烷氧负离子向 phosphonium 磷中心加成；"
        "后续 P(V) 配体偶联是选择性决定步骤，dearomatized 中间体后的塌陷近不可逆。"
    ),
    TASK_IDS[5]: (
        "应整合质子化势垒、BiPy/PhPy 与 C-C/C-O 竞争、stepwise asynchronous 机理、"
        "dearomatized intermediate 和加成决速/偶联选控的完整证据链。"
    ),
}

# These notes are an expert audit of the saved evidence, not another model score.
EXPERT_AUDIT_NOTES = {
    TASK_IDS[0]: [
        "同步 ORCA 合同修复后的有效运行完成九种子筛选、三代表精修、反应物 Hessian/振动/353.15 K 1 M 热化学以及多种 TS 搜索；Judge 评分 58/100，objective flags 为空。",
        "只有 P1 的 Sella 分支得到一个 64.4i cm-1 候选一阶鞍点和 38.7 kcal mol-1 势垒；隐藏参考 P1 约 20 kcal mol-1，且 Agent 没有运行 IRC 或验证该软模确实对应目标 C-C 坐标。",
        "P0/P2 的 pysisyphus 端点经独立 Hessian 证实为 minima，畸变 Sella 初猜触发 xTB 数值异常。因此本轮没有 P0/P2 势垒，不能检验参考的 30 -> 20 -> 14 kcal mol-1 单调下降。",
        "报告一方面声称质子化增加势垒，另一方面又称 P1 最优/趋势非单调，结论自相矛盾并与隐藏参考相反。一次分析作业遗漏 staged input 也是 Agent 合同错误；框架未自动换 Backend 或参数。",
    ],
    TASK_IDS[1]: [
        "收敛状态修复后的有效运行覆盖九个种子优化、两类竞争路径的 12 次 TS 尝试、Hessian、振动和热化学，Judge 评分 45/100，objective flags 为空。",
        "Agent 把含多个近零虚频的端点误报为恰好一个虚频，并由此得到非物理的负活化自由能；同时没有生成产品能量，且报告声称 1 M、实际热化学使用 1 atm。",
        "最终把选择性归因为热力学/产品稳定性而非隐藏参考要求的 BiPy 动力学优势。这属于模型的驻点验证和科学解释错误，不是框架替换 Backend 或自动回退。",
    ],
    TASK_IDS[2]: [
        "完成两条竞争路径、TS/Hessian 和能量比较，过程覆盖充分。",
        "C-C 约 1.13、C-O 上界约 66.87 kcal mol-1，与隐藏参考 14/18 的定量偏差很大；100 分反映当前过程型 rubric 宽松，不代表高精度复现。",
        "该结果是裁判标定风险的重要样例。",
    ],
    TASK_IDS[3]: [
        "在修复后的最终运行中完成九种子优化、五次 pysisyphus 搜索、一轮 Sella、独立 Hessian/振动和键级分析，Judge 评分 55/100。",
        "定性判断 stepwise、asynchronous 与隐藏参考一致；但没有得到真正一阶鞍点、IRC、沿路径键变化或 dearomatized intermediate，因此机理证据仍不完整。",
        "Sella 内部返回 order=1，但独立 Hessian 只有数值近零虚频，Agent 正确把该端点降级为 minimum；三个达到循环上限的 pysisyphus 结果也被新适配层正确标成 partial/unconverged。",
        "Judge objective flags 为空，说明本轮低分来自科学搜索与证据不足，而不是框架阻塞。",
    ],
    TASK_IDS[4]: [
        "有效运行正确复现实验相对速率和 Hammett 趋势，但在受管证据边界修复后重评分仅 22/100，objective flags 为空。",
        "关键 27--36 kcal mol-1 扫描和所谓全解离产品优化由 Agent 直接在 OpenCode bash 中启动 xTB，不属于三层 Chemistry MCP 的 managed scientific evidence；相关计算 criterion 因而为 0。",
        "受管 pysisyphus 搜索在 200 个循环后被正确标记为 partial/unconverged，独立 Hessian 也没有确认一阶鞍点。Agent 最初遗漏 P2 电荷，但读到 provenance 后显式改为 charge=2。",
        "最终仍把 ligand coupling 错当整体 RDS，未计算醇加成势垒，也未区分加成决速、偶联选择性决定和后续不可逆塌陷。这是模型的证据选择与科学结论错误。",
    ],
    TASK_IDS[5]: [
        "端到端运行产生 44 次 MCP 调用，其中按最终状态重算的 managed scientific success/attempt 为 25/28；Judge 评分 38/100 且 objective flags 为空。TS 达到循环上限被正确保留为 partial/unconverged，没有发生自动 Backend 或参数替换。",
        "Agent 只优化每个质子化状态的 SEED_01，没有按任务要求筛选九个替代种子；P1 振动结果含 19.85i cm-1 模式，却仍被当作普通反应物热化学状态，驻点验证不充分。",
        "受管计算只给出 P0 碎片化产品反应能约 +129 kcal mol-1 和一个未收敛搜索端点约 +136 kcal mol-1；没有构建 P0/P1/P2 势垒、BiPy/PhPy、C-C/C-O、醇加成或完整动力学的可比 profile。",
        "最终声称 concerted reductive elimination，并把 Hammett 趋势直接解释为该单步坐标；这与隐藏参考的 P2 活性态、stepwise asynchronous/dearomatized intermediate 以及醇加成决速相冲突，也没有 IRC 或直接键重排证据。",
        "三次热化学 ArtifactRef 类型错误在 schema 校验阶段被拒绝后由 Agent 显式修正；这些以及一次错误 Backend discovery 都是可观察的 Agent 合同错误，不是框架故障。",
    ],
}

FIXES = [
    ("307bdab", "接受 pysisyphus 中常见 xTB 方法标签"),
    ("79c3509", "暴露精确 pysisyphus 原生合同"),
    ("53d7376", "识别 ORCA 零退出码下的内部异常终止"),
    ("a360581", "预检 inline structure 并改进 TS 错误信息"),
    ("6c27d81", "加入 pysisyphus 1.0.0 可执行原生模板"),
    ("eff7723", "在 worker 前验证 pysisyphus YAML"),
    ("8b86183", "将当前 ORCA 安装限制为已验证的单核执行"),
    ("5fc2f94", "校验热化学 EnergyResult/FrequencyResult 语义交接"),
    ("9889211", "在优化和 TS 结构产物中保留电荷/多重度"),
    ("0a7e027", "按异步作业最终状态统计 managed scientific success"),
    ("0e46d94", "记录实际解析后的分子电荷与自旋 provenance"),
    ("e1c5896", "把达到最大循环数的 pysisyphus 搜索标记为未收敛 partial result"),
    ("6326396", "从完整 tool result 而非截断 preview 解析异步作业终态"),
    ("954f889", "限制同步 ORCA Action，并为长作业暴露显式异步原生路径"),
    ("425cae2", "禁止裁判把 OpenCode shell/file 调用计作 managed scientific evidence"),
]

SUPERSEDED_RUNS = [
    (
        "Q1 旧最终运行",
        ROOT
        / "workspaces/cli_runs/batch_20260722_134227_3a5473/"
        "Heterobiaryl_PV_01_Protonation_opencode_20260722_134227_de5b37",
        "4 个达到最大循环数的 pysisyphus TS 搜索被旧适配层错误计为 converged。",
        "70 分结果作废，使用 e1c5896 后的收敛安全运行替代。",
    ),
    (
        "同步/异步合同修复前 Q1",
        ROOT
        / "workspaces/cli_runs/batch_20260722_171802_f29209/"
        "Heterobiaryl_PV_01_Protonation_opencode_20260722_171802_0d88bc",
        "Agent 同时请求三个 walltime_seconds=86400 的同步 ORCA 优化，但 MCP 客户端上限为 3600 秒，且服务只实际启动第一个；后两个不可能在合同内完成。",
        "在确定性超时前主动终止并作废；同步 ORCA Action 现限制为 1800 秒，长计算必须由 Agent 显式编写输入并提交异步 native job。",
    ),
    (
        "Q2 旧最终运行",
        ROOT
        / "workspaces/cli_runs/batch_20260722_134227_3a5473/"
        "Heterobiaryl_PV_02_CC_Selectivity_opencode_20260722_134227_a08b71",
        "10 个达到最大循环数的 pysisyphus TS 搜索被旧适配层错误计为 converged。",
        "70 分结果作废，使用 e1c5896 后的收敛安全运行替代。",
    ),
    (
        "Q5 旧最终运行",
        ROOT
        / "workspaces/cli_runs/batch_20260722_134227_3a5473/"
        "Heterobiaryl_PV_05_Rate_Determining_Step_opencode_20260722_141952_f16c49",
        "关键 pysisyphus TS 搜索达到最大循环数却被记作 converged。",
        "83 分结果作废，使用 e1c5896 后的收敛安全运行替代。",
    ),
    (
        "Q5 managed-evidence 规则修复前评分",
        ROOT
        / "workspaces/cli_runs/batch_20260722_171802_f29209/"
        "Heterobiaryl_PV_05_Rate_Determining_Step_opencode_20260722_173155_5a5a43",
        "初次 Judge 把 OpenCode bash 中直接启动的 xTB 约束扫描当作 managed coupling evidence，给出 46 分。",
        "Agent 轨迹不重跑；425cae2 后同轨迹重评分为 22 分，完整前后快照保存在 _score_history.jsonl。",
    ),
    (
        "初始子任务批次",
        ROOT
        / "workspaces/cli_runs/batch_20260722_134227_3a5473/"
        "Heterobiaryl_PV_04_Coupling_Mechanism_opencode_20260722_140505_6f7bf7",
        "Provider stream 挂起，人工终止；没有形成可评分科研结果。",
        "诊断运行，不作为最终结果。",
    ),
    (
        "原生合同修复前复跑",
        ROOT
        / "workspaces/cli_runs/batch_20260722_154657_f0a605/"
        "Heterobiaryl_PV_04_Coupling_Mechanism_opencode_20260722_154657_57508c",
        "完成并得 57 分，但 Agent 因缺少精确模板猜测了无效 pysisyphus YAML。",
        "补充 1.0.0 原生模板和 worker 前 YAML 预检。",
    ),
    (
        "ORCA 资源诊断复跑",
        ROOT
        / "workspaces/cli_runs/batch_20260722_161031_65b5c0/"
        "Heterobiaryl_PV_04_Coupling_Mechanism_opencode_20260722_161031_1588cf",
        "多次 PAL4 ORCA MPI/PMIX 失败后进入长时单核优化。",
        "为节省资源主动停止；将本安装的 ORCA Backend 声明为单核上限。",
    ),
    (
        "分子状态元数据修复前复跑",
        ROOT
        / "workspaces/cli_runs/batch_20260722_162658_f15ed1/"
        "Heterobiaryl_PV_04_Coupling_Mechanism_opencode_20260722_162658_675b07",
        "Agent 实际以 --chrg 2 运行 P2，但类型化 XYZ 产物显示默认 charge=0，Judge 因而误判并给 9 分。",
        "分数作废；保留命令证据并修复输出电荷/多重度与 resolved-state provenance。",
    ),
    (
        "收敛状态修复前复跑",
        ROOT
        / "workspaces/cli_runs/batch_20260722_164510_16d17e/"
        "Heterobiaryl_PV_04_Coupling_Mechanism_opencode_20260722_164510_da6966",
        "pysisyphus 明确达到最大循环数，但适配层因存在最后几何而错误返回 converged=true。",
        "主动停止；改为 partial_success/converged=false 并保留未收敛端点。",
    ),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            values.append(item)
    return values


def escape(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", "<br>")


def compact(value: Any, limit: int = 280) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def relative_link(path: Path, label: str | None = None) -> str:
    relative = os.path.relpath(path, REPORT.parent).replace(os.sep, "/")
    if not path.exists():
        return f"`{label or relative}`（已按 workspace 保留策略清理）"
    return f"[{label or path.name}]({relative})"


def newest_completed_workspace(task_id: str) -> Path:
    candidates = []
    pattern = f"{task_id}_opencode_*"
    for workspace in (ROOT / "workspaces/cli_runs").glob(f"batch_*/{pattern}"):
        meta_path = workspace / "_meta.json"
        score_path = workspace / "_score.json"
        if not meta_path.is_file() or not score_path.is_file():
            continue
        try:
            meta = load_json(meta_path)
        except (json.JSONDecodeError, OSError):
            continue
        if meta.get("status") == "completed":
            candidates.append(workspace)
    if not candidates:
        raise FileNotFoundError(f"No completed and scored workspace for {task_id}")
    return max(candidates, key=lambda item: item.stat().st_mtime_ns)


def event_result(
    event: dict[str, Any], workspace: Path | None = None
) -> dict[str, Any]:
    if workspace is not None and isinstance(event.get("result_path"), str):
        path = (workspace / event["result_path"]).resolve()
        try:
            path.relative_to(workspace.resolve())
            payload = load_json(path)
        except (ValueError, OSError, json.JSONDecodeError):
            payload = {}
        if isinstance(payload, dict):
            value = payload.get("result")
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    value = None
            if isinstance(value, dict):
                return value
    value = event.get("result_preview")
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def event_request(event: dict[str, Any]) -> dict[str, Any]:
    arguments = event.get("arguments")
    if not isinstance(arguments, dict):
        return {}
    request = arguments.get("request")
    return request if isinstance(request, dict) else arguments


def event_backend(event: dict[str, Any]) -> str:
    request = event_request(event)
    backend = request.get("backend_id") or request.get("runtime") or request.get("software_id")
    components = request.get("component_backends")
    values = [str(backend)] if backend else []
    if isinstance(components, dict) and components:
        values.append("components=" + compact(components, 100))
    return "; ".join(values) or "-"


def event_input_summary(event: dict[str, Any]) -> str:
    request = event_request(event)
    selected = {
        key: request[key]
        for key in (
            "action_id",
            "inputs",
            "method_spec",
            "action_settings",
            "resource_limits",
            "script_path",
            "arguments",
            "job_id",
        )
        if key in request
    }
    return compact(selected, 360) if selected else "-"


def event_artifacts(event: dict[str, Any]) -> str:
    values = []
    for item in event.get("artifacts") or []:
        if not isinstance(item, dict):
            continue
        values.append(str(item.get("artifact_id") or item.get("path") or ""))
    return ", ".join(value for value in values if value)[:260] or "-"


def event_output_summary(event: dict[str, Any], workspace: Path) -> str:
    payload = event_result(event, workspace)
    if not payload:
        return "-"
    summary = {
        key: payload[key]
        for key in (
            "status",
            "action",
            "backend",
            "job_id",
            "job_status",
            "terminal",
        )
        if key in payload
    }
    result = payload.get("result")
    if isinstance(result, dict):
        core: dict[str, Any] = {}
        for key, value in result.items():
            if key == "structure" and isinstance(value, dict):
                core[key] = {
                    field: value[field]
                    for field in (
                        "artifact_id",
                        "atom_count",
                        "charge",
                        "multiplicity",
                        "source_path",
                    )
                    if field in value
                }
            elif key == "matrix" and isinstance(value, dict):
                core[key] = {
                    field: value[field]
                    for field in ("artifact_id", "shape")
                    if field in value
                }
            elif key == "frequencies_cm1" and isinstance(value, list):
                imaginary = [
                    item.get("imaginary")
                    for item in value
                    if isinstance(item, dict) and float(item.get("imaginary") or 0) > 0
                ]
                core[key] = {
                    "mode_count": len(value),
                    "imaginary_count": len(imaginary),
                    "largest_imaginary": max(imaginary, default=0),
                }
            else:
                core[key] = value
        summary["result"] = core
    job = payload.get("job")
    if isinstance(job, dict):
        summary["job"] = {
            key: job[key]
            for key in ("job_id", "status", "duration_seconds", "return_code", "error")
            if key in job
        }
    if payload.get("warnings"):
        summary["warnings"] = payload["warnings"]
    if payload.get("error"):
        summary["error"] = payload["error"]
    return compact(summary, 460)


def job_terminal_states(
    events: list[dict[str, Any]], workspace: Path | None = None
) -> dict[str, dict[str, Any]]:
    states: dict[str, dict[str, Any]] = {}
    for event in events:
        if event.get("tool") not in {
            "submit_native_job",
            "submit_analysis_program",
            "get_execution_job",
            "collect_execution_job",
            "cancel_execution_job",
        }:
            continue
        result = event_result(event, workspace)
        job = result.get("job") if isinstance(result.get("job"), dict) else {}
        request = event_request(event)
        job_id = result.get("job_id") or job.get("job_id") or request.get("job_id")
        if not isinstance(job_id, str):
            continue
        state = result.get("job_status") or job.get("status")
        record = states.setdefault(job_id, {"job_id": job_id, "tool": event.get("tool")})
        if isinstance(state, str):
            record["state"] = state
        error = job.get("error") or result.get("error")
        if error:
            record["error"] = error
        if event.get("tool") in {"submit_native_job", "submit_analysis_program"}:
            record["submit_tool"] = event.get("tool")
            record["label"] = request.get("label")
    return states


def run_length(values: list[str]) -> str:
    if not values:
        return "无"
    output = []
    current = values[0]
    count = 1
    for value in values[1:]:
        if value == current:
            count += 1
            continue
        output.append(f"`{current}` x {count}" if count > 1 else f"`{current}`")
        current = value
        count = 1
    output.append(f"`{current}` x {count}" if count > 1 else f"`{current}`")
    return " -> ".join(output)


def output_inventory(workspace: Path) -> dict[str, Any]:
    files = []
    for name in ("code", "outputs", "report"):
        root = workspace / name
        if not root.is_dir():
            continue
        files.extend(path for path in root.rglob("*") if path.is_file())
    groups = Counter(path.relative_to(workspace).parts[0] for path in files)
    return {
        "count": len(files),
        "bytes": sum(path.stat().st_size for path in files),
        "groups": dict(sorted(groups.items())),
    }


def public_archive_inventory() -> dict[str, Any]:
    digest = hashlib.sha256(PUBLIC_ARCHIVE.read_bytes()).hexdigest()
    with zipfile.ZipFile(PUBLIC_ARCHIVE) as archive:
        entries = [
            {"path": item.filename, "size": item.file_size}
            for item in archive.infolist()
            if not item.is_dir()
        ]
    return {
        "sha256": digest,
        "entries": entries,
        "count": len(entries),
        "bytes": sum(item["size"] for item in entries),
    }


def classify_failure(event: dict[str, Any], workspace: Path | None = None) -> str:
    status = str(event.get("status") or "")
    error = compact(
        event.get("error") or event_result(event, workspace).get("error") or {}, 500
    ).casefold()
    if status == "invalid_request":
        return "Agent 参数/合同错误，框架在执行前拒绝"
    if any(token in error for token in ("scc", "scf", "converg", "overlap", "short distance")):
        return "数值或初猜导致的科学计算失败"
    if "modulenotfounderror" in error or "no module named" in error:
        return "Agent 编写程序的依赖/代码错误"
    if "resource" in error or "walltime" in error or "timeout" in error:
        return "显式资源限制或超时"
    return "需结合完整日志复核"


def collect_record(task_id: str) -> dict[str, Any]:
    from evaluation.token_usage import workspace_token_usage
    from evaluation.trace import load_native_agent_trace, process_metrics

    workspace = newest_completed_workspace(task_id)
    task_dir = ROOT / "tasks" / task_id
    events = load_jsonl(workspace / "_tool_trace.jsonl")
    return {
        "task_id": task_id,
        "workspace": workspace,
        "task": load_json(task_dir / "task_info.json"),
        "truth": load_json(task_dir / "target_study/ground_truth.json"),
        "meta": load_json(workspace / "_meta.json"),
        "score": load_json(workspace / "_score.json"),
        "catalog": load_json(workspace / "_toolbox_catalog.json"),
        "events": events,
        "metrics": process_metrics(events, workspace=workspace),
        "native": load_native_agent_trace(workspace),
        "usage": workspace_token_usage(workspace),
        "jobs": job_terminal_states(events, workspace),
        "inventory": output_inventory(workspace),
        "agent_report": (workspace / "report/report.md").read_text(
            encoding="utf-8", errors="replace"
        ),
    }


def append_task(lines: list[str], index: int, record: dict[str, Any]) -> None:
    task_id = record["task_id"]
    task = record["task"]
    truth = record["truth"]
    meta = record["meta"]
    score = record["score"]
    usage = record["usage"]
    metrics = record["metrics"]
    events = record["events"]
    native = record["native"]
    workspace = record["workspace"]
    lines.extend(
        [
            "",
            f"## {index}. {task_id}",
            "",
            "### 任务指令",
            "",
            *[f"> {line}" if line else ">" for line in str(task.get("task", "")).splitlines()],
            "",
            "任务指令没有给出软件名、Action 名、Backend 名、固定调用顺序或论文身份。",
            "",
            "### 输入与评分合同",
            "",
            "| 字段 | 内容 |",
            "|---|---|",
            f"| Category | `{escape(task.get('category'))}` |",
            f"| 公开数据 | `{escape((task.get('data') or [{}])[0].get('path'))}` |",
            f"| 数据说明 | {escape((task.get('data') or [{}])[0].get('description'))} |",
            f"| Archive SHA-256 | `{escape((task.get('archive_extractions') or [{}])[0].get('sha256'))}` |",
            f"| Managed computation 最少成功数 | {escape((truth.get('managed_computation_policy') or {}).get('minimum_successful_scientific_calls'))} |",
            f"| 隐藏参考摘要 | {escape(REFERENCE_SUMMARIES[task_id])} |",
            "",
            "机器可读 expected result：",
            "",
            "```json",
            json.dumps(truth.get("expected_result"), ensure_ascii=False, indent=2),
            "```",
            "",
            "Ground-truth rubric：",
            "",
            "| Criterion | 上限 | 评分要求 |",
            "|---|---:|---|",
        ]
    )
    for criterion in truth.get("scoring_rubric") or []:
        lines.append(
            f"| `{escape(criterion.get('id'))}` | {criterion.get('max_score')} | {escape(criterion.get('criterion'))} |"
        )
    lines.extend(
        [
            "",
            "### 最终运行、Token 与产物",
            "",
            f"- Workspace：{relative_link(workspace)}",
            f"- 状态：`{meta.get('status')}`；模型：`{meta.get('model')}`；耗时：{float(meta.get('duration_seconds') or 0):.3f} s。",
            f"- Frozen catalog hash：`{record['catalog'].get('catalog_hash')}`。",
            f"- 报告：{relative_link(workspace / 'report/report.md', 'report/report.md')}；分数：**{score.get('score')}/{score.get('score_max')}**。",
            f"- 完整轨迹：{relative_link(workspace / '_model_io.jsonl', '_model_io.jsonl')}；MCP：{relative_link(workspace / '_tool_trace.jsonl', '_tool_trace.jsonl')}；Agent stream：{relative_link(workspace / '_agent_output.jsonl', '_agent_output.jsonl')}。",
            "",
            "| Token/运行指标 | 数值 |",
            "|---|---:|",
            f"| Agent model steps | {usage['model_step_count']:,} |",
            f"| Agent sessions | {usage['session_count']:,} |",
            f"| Agent total tokens | {usage['tokens']['total']:,} |",
            f"| uncached input | {usage['tokens']['input']:,} |",
            f"| cache read | {usage['tokens']['cache_read']:,} |",
            f"| output | {usage['tokens']['output']:,} |",
            f"| reasoning | {usage['tokens']['reasoning']:,} |",
            f"| First model step total | {usage['first_model_step_tokens']['total']:,} |",
            f"| Judge total tokens | {int((score.get('judge_usage') or {}).get('total_tokens') or 0):,} |",
            f"| Initial instruction bytes | {int(meta.get('instruction_bytes') or 0):,} |",
            f"| Frozen catalog snapshot bytes | {int(meta.get('catalog_snapshot_bytes') or 0):,} |",
            f"| Public MCP tool count | {int(meta.get('mcp_public_tool_count') or 0):,} |",
            f"| MCP calls success/total | {metrics['successful_tool_calls']}/{metrics['tool_call_count']} |",
            f"| Managed scientific success/attempt | {metrics['successful_managed_scientific_calls']}/{metrics['managed_scientific_attempt_count']} |",
            f"| Managed failed/incomplete | {metrics['failed_managed_scientific_calls']}/{metrics.get('incomplete_managed_scientific_calls', 0)} |",
            f"| Native tools success/total | {sum(item.get('status') == 'success' for item in native)}/{len(native)} |",
            f"| code/outputs/report files | {record['inventory']['count']:,} ({record['inventory']['bytes']:,} bytes) |",
            "",
            "### MCP 工具流程",
            "",
            "下表按实际 sequence 原样保留；框架没有自动选择 Backend、重试或回退。",
            "",
            "| Seq | Tool/Action | Backend/runtime | 状态 | 秒 | Agent 提供的核心参数 | 结果摘要 | 产物 |",
            "|---:|---|---|---|---:|---|---|---|",
        ]
    )
    for event in events:
        lines.append(
            "| {seq} | `{tool}` | {backend} | `{status}` | {seconds:.3f} | {inputs} | {result} | {artifacts} |".format(
                seq=event.get("sequence", ""),
                tool=escape(event.get("tool")),
                backend=escape(event_backend(event)),
                status=escape(event.get("status")),
                seconds=float(event.get("duration_seconds") or 0),
                inputs=escape(event_input_summary(event)),
                result=escape(event_output_summary(event, workspace)),
                artifacts=escape(event_artifacts(event)),
            )
        )
    tool_counts = Counter(str(item.get("tool")) for item in events)
    backend_counts = Counter(
        event_backend(item) for item in events if event_backend(item) != "-"
    )
    lines.extend(
        [
            "",
            "MCP 调用计数：" + ", ".join(f"`{key}` x {value}" for key, value in tool_counts.most_common()),
            "",
            "Backend/runtime 计数：" + (", ".join(f"`{key}` x {value}" for key, value in backend_counts.most_common()) or "无"),
            "",
            "Native/OpenCode 工具压缩顺序：" + run_length([str(item.get("tool")) for item in native]),
            "",
            "### Native/OpenCode 工具流程",
            "",
            "这些调用用于文件检查、报告撰写或 Agent 自行运行 shell。即使 shell 中启动了化学程序，也不计入 managed scientific evidence；完整未截断内容保存在 `_model_io.jsonl`。",
            "",
            "| Seq | Tool | 状态 | 秒 | 参数摘要 | 结果摘要 | 管理边界 |",
            "|---:|---|---|---:|---|---|---|",
        ]
    )
    for event in native:
        lines.append(
            f"| {event.get('sequence')} | `{escape(event.get('tool'))}` | "
            f"`{escape(event.get('status'))}` | {float(event.get('duration_seconds') or 0):.3f} | "
            f"{escape(compact(event.get('arguments') or {}, 460))} | "
            f"{escape(compact(event.get('result_preview') or event.get('error') or {}, 460))} | "
            "OpenCode native；不计 managed evidence |"
        )
    lines.extend(
        [
            "",
            "### 失败与异步作业终态",
            "",
        ]
    )
    failures = [item for item in events if item.get("status") not in {"success", "partial_success"}]
    if failures:
        lines.extend(
            [
                "| Seq | Tool | 状态 | 审计分类 | 原始错误摘要 |",
                "|---:|---|---|---|---|",
            ]
        )
        for event in failures:
            error = event.get("error") or event_result(event, workspace).get("error") or {}
            lines.append(
                f"| {event.get('sequence')} | `{escape(event.get('tool'))}` | `{escape(event.get('status'))}` | "
                f"{escape(classify_failure(event, workspace))} | {escape(compact(error, 500))} |"
            )
    else:
        lines.append("没有 transport/Action 失败事件。")
    lines.extend(["", "异步作业：", ""])
    if record["jobs"]:
        lines.extend(
            [
                "| Job id | 提交工具 | 最终可观察状态 | 标签 | 错误 |",
                "|---|---|---|---|---|",
            ]
        )
        for job in record["jobs"].values():
            lines.append(
                f"| `{job['job_id']}` | `{escape(job.get('submit_tool'))}` | `{escape(job.get('state'))}` | "
                f"{escape(job.get('label'))} | {escape(compact(job.get('error') or {}, 380))} |"
            )
    else:
        lines.append("没有异步 native/program 作业。")
    lines.extend(
        [
            "",
            "### Judge 评分",
            "",
            f"Judge rationale：{score.get('rationale') or '未提供'}",
            "",
            "| Criterion | 得分 | 上限 | 理由 |",
            "|---|---:|---:|---|",
        ]
    )
    for criterion in score.get("criteria") or []:
        lines.append(
            f"| `{escape(criterion.get('id'))}` | {criterion.get('score')} | {criterion.get('max_score')} | {escape(criterion.get('rationale'))} |"
        )
    flags = score.get("objective_issue_flags") or []
    lines.extend(
        [
            "",
            "Judge objective flags：" + ("；".join(str(item) for item in flags) if flags else "无。"),
            "",
            "### 独立科学审计与参考差距",
            "",
        ]
    )
    notes = EXPERT_AUDIT_NOTES[task_id]
    if notes:
        lines.extend(f"- {item}" for item in notes)
    else:
        lines.append("- 待最终有效运行完成后由生成器配置补全。")
    lines.extend(
        [
            f"- 隐藏参考：{REFERENCE_SUMMARIES[task_id]}",
            "",
            "### Agent 最终报告原文",
            "",
            "<details>",
            "<summary>展开 report/report.md</summary>",
            "",
            record["agent_report"].rstrip(),
            "",
            "</details>",
        ]
    )


def main() -> int:
    records = [collect_record(task_id) for task_id in TASK_IDS]
    public_archive = public_archive_inventory()
    total_agent = sum(item["usage"]["tokens"]["total"] for item in records)
    total_judge = sum(
        int((item["score"].get("judge_usage") or {}).get("total_tokens") or 0)
        for item in records
    )
    total_calls = sum(item["metrics"]["tool_call_count"] for item in records)
    total_managed = sum(
        item["metrics"]["managed_scientific_attempt_count"] for item in records
    )
    total_managed_success = sum(
        item["metrics"]["successful_managed_scientific_calls"] for item in records
    )
    lines = [
        "# Heterobiaryl P(V) 自主计算六任务最终验证报告",
        "",
        "生成日期：2026-07-22",
        "",
        "本报告只把公开的九个未优化种子、实验条件和论文报告测量值视为 Agent 输入。所有作者计算输出、优化驻点、能量、频率、路径标签和参考答案均位于隐藏 reference 区域，仅用于事后评分与本报告审计。",
        "最终 workspace 的选择规则是：对每个 task_id 选择时间最新、`_meta.json` 状态为 completed 且存在 `_score.json` 的运行；所有因框架问题作废的旧运行在后文单列。",
        "",
        "## 1. 结论总览",
        "",
        "| 任务 | 分数 | Agent token | Judge token | MCP 成功/总数 | Managed 成功/尝试 | Agent 核心结论与参考符合度 |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in records:
        task_id = item["task_id"]
        lines.append(
            f"| {task_id.replace('Heterobiaryl_PV_', 'Q')} | {item['score'].get('score')}/{item['score'].get('score_max')} | "
            f"{item['usage']['tokens']['total']:,} | {int((item['score'].get('judge_usage') or {}).get('total_tokens') or 0):,} | "
            f"{item['metrics']['successful_tool_calls']}/{item['metrics']['tool_call_count']} | "
            f"{item['metrics']['successful_managed_scientific_calls']}/{item['metrics']['managed_scientific_attempt_count']} | "
            f"{escape((EXPERT_AUDIT_NOTES[task_id] or ['见逐题审计。'])[0])} |"
        )
    lines.extend(
        [
            "",
            f"六任务合计 Agent token：**{total_agent:,}**；Judge token：**{total_judge:,}**；MCP 调用：**{total_calls:,}**；按异步终态重算的 managed scientific 成功/尝试：**{total_managed_success}/{total_managed}**。",
            "",
            "分数衡量当前 rubric 下的任务表现，不等同于高精度科学复现。尤其 Q3 的过程分为满分，但数值与隐藏高层级参考偏差很大。",
            "",
            "## 2. Agent 可见数据边界",
            "",
            "| 项目 | 数值 |",
            "|---|---:|",
            "| Archive | `tasks/_heterobiaryl_pv_shared/public/autonomous_inputs.zip` |",
            f"| SHA-256 | `{public_archive['sha256']}` |",
            f"| 文件数 | {public_archive['count']} |",
            f"| 解压字节 | {public_archive['bytes']:,} |",
            "| 未优化种子 | 9（P0/P1/P2 各 3） |",
            "| 完成计算输出 | **0** |",
            "| 优化驻点 | **0** |",
            "",
            "公开文件仅含 `README.md`、`chemical_system.json`、`data_scope.json`、实验测量 CSV/JSON、起始结构清单和九个 XYZ。完整清洗审计见 "
            + relative_link(ROOT / "tasks/_heterobiaryl_pv_shared/reference/CURATION_AUDIT.md", "CURATION_AUDIT.md")
            + "。",
            "",
            "| Archive member | 字节 |",
            "|---|---:|",
        ]
    )
    lines.extend(
        f"| `{escape(item['path'])}` | {item['size']:,} |"
        for item in public_archive["entries"]
    )
    lines.extend(
        [
            "",
            "## 3. 工具暴露与客观偏差修复",
            "",
            "六题使用同一套 task-independent Action/Backend 目录和渐进式发现入口。针对已证实的客观合同问题只重跑受影响任务，因此最终 workspace 的 frozen catalog hash 可能随修复提交不同；每题精确 hash 在逐题运行信息中列出。初始提示只提供领域索引；Agent 自主调用 `search_actions`/`inspect_action`、选择 Action/Backend/参数，或进入软件原生层与可编程层。框架不按任务推荐工具、不自动选择 Backend、不自动重试、不做失败回退。",
            "",
            "| Commit | 修复 |",
            "|---|---|",
        ]
    )
    lines.extend(f"| `{commit}` | {description} |" for commit, description in FIXES)
    lines.extend(
        [
            "",
            "关键验证原则：数值不收敛、错误 TS 初猜和 Agent 自写程序错误保留为模型/科学过程的一部分；只有合同含糊、错误状态分类、错误资源声明、错误产物元数据或评分统计错误才修改框架并复跑受影响任务。",
            "",
            "### 诊断与作废运行",
            "",
            "| 阶段 | Workspace | 观察 | 处理 |",
            "|---|---|---|---|",
        ]
    )
    for label, workspace, observation, disposition in SUPERSEDED_RUNS:
        lines.append(
            f"| {label} | {relative_link(workspace)} | {observation} | {disposition} |"
        )
    for index, record in enumerate(records, start=4):
        append_task(lines, index, record)
    lines.extend(
        [
            "",
            "## 10. 跨任务结论",
            "",
            "- 工具箱能够让 Agent 从原始种子启动真实优化、能量、TS、Hessian、振动、键级、原生软件和自编程序作业；六题不再能靠读取预计算输出完成。",
            "- 当前主要瓶颈已经从 MCP 合同失败转移到开放式反应路径提出、可靠 TS/IRC 定位、统一热化学层级和科学停止条件。",
            "- 低成本 GFN2-xTB 适合筛选，但不能仅凭其单一路径结果声称复现论文级自由能或机理；Q3 是最明显的评分标定案例。",
            "- Judge 需要同时核对命令 provenance、类型化产物和隐藏参考。仅依据某一个字段可能产生误判；最终有效 Q4 已在分子状态元数据修复后运行。",
            "- 端到端任务的 token 不应机械等于五个子任务之和：它是一次共享上下文、共享中间产物的独立轨迹；本报告同时给出步骤、调用和 token，便于判断其是否真正执行了跨阶段计算。",
            "",
            "## 11. 重现与审计入口",
            "",
            "```bash",
            ".envs/researchchembench/bin/python scripts/generate_heterobiaryl_autonomous_verification.py",
            ".envs/researchchembench/bin/pytest -q",
            "```",
            "",
            "每题 workspace 中的 `_model_io.jsonl` 保存每一步模型输入、输出、reasoning、tool part 和 token；`_tool_trace.jsonl` 保存 MCP 请求、状态、耗时、错误和 artifacts；`_tool_results/` 与 `_tool_artifacts/` 保存不可变结果与 provenance。",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    rendered = "\n".join(lines)
    rendered = "\n".join(line.rstrip() for line in rendered.splitlines()).rstrip() + "\n"
    REPORT.write_text(rendered, encoding="utf-8")
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
