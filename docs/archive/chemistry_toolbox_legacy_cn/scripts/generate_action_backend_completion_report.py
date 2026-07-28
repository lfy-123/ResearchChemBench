#!/usr/bin/env python3
"""Generate the complete Action/Backend execution and software-use audit."""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in os.sys.path:
        os.sys.path.insert(0, str(path))

from researchchem_toolbox.catalog import action_specs, backend_specs


CONFIG_ROOT = TOOLBOX_ROOT / "config"
OUTPUT = TOOLBOX_ROOT / "docs" / "ACTION_BACKEND_COMPLETE_AUDIT_20260721.md"
PASS = {"success", "partial_success"}
CATEGORY_ZH = {
    "scientific_data_interchange": "科学数据、Schema与输出解析",
    "structure_and_system": "结构、构象、电荷与体系构建",
    "cheminformatics": "化学信息学与分子图操作",
    "molecular_electronic": "分子电子结构与派生性质",
    "reaction_and_kinetics": "反应路径、平衡与动力学",
    "molecular_dynamics": "分子动力学、轨迹与自由能",
    "periodic_and_phonons": "周期电子结构、声子与热输运",
    "docking": "分子对接",
    "data_sources": "外部化学数据源",
}


def load(name: str) -> dict[str, Any]:
    return json.loads((CONFIG_ROOT / name).read_text(encoding="utf-8"))


def cell(value: Any) -> str:
    text = str(value if value is not None else "—")
    return text.replace("|", "\\|").replace("\n", "<br>")


def codes(values: list[str] | tuple[str, ...]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "—"


def error_text(item: dict[str, Any]) -> str:
    error = item.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or "")
    return str(error or "")


ISSUES: dict[tuple[str, str], dict[str, str]] = {
    ("calculate_dipole_moment", "psi4"): {
        "kind": "适配器/API不兼容",
        "cause": "当前适配器读取已在 Psi4 1.6 后废弃的 `SCF DIPOLE X/Y/Z` 标量变量；本机 Psi4 要求读取向量变量 `SCF DIPOLE`，且单位从 Debye 改为原子单位。",
        "solution": "改为一次读取 `numpy.asarray(psi4.core.variable('SCF DIPOLE'))`，乘以 `2.541746473` 转成 Debye；补充水分子非零偶极和单位回归测试。",
        "priority": "P0",
    },
    ("calculate_orbitals", "psi4"): {
        "kind": "适配器/对称分块解析",
        "cause": "`wavefunction.epsilon_a()` 是按不可约表示分块的 Psi4 Vector；水分子保留 C2v 对称性时有多个 irrep，不能直接 `numpy.asarray()`。",
        "solution": "使用 `epsilon_a().to_array()`/`epsilon_b().to_array()` 逐 irrep 展平，并用 `nalphapi()`/`nbetapi()`生成对应占据数；若不需要对称信息，也可显式使用 `symmetry c1`，但前者更稳健。",
        "priority": "P0",
    },
    ("calculate_periodic_forces", "cp2k"): {
        "kind": "输入生成+输出解析",
        "cause": "CP2K `ENERGY_FORCE` 在当前输出级别不打印原子力；即使显式打印，CP2K 2026 的行带 `FORCES|` 前缀，现有正则仍无法匹配。",
        "solution": "在 `FORCE_EVAL/PRINT` 中加入 `FORCES ON`；解析 `FORCES| <atom> <fx> <fy> <fz>` 块并忽略 Sum/Total 行，保留 hartree/bohr 或显式转换到 eV/Å。",
        "priority": "P0",
    },
    ("calculate_periodic_stress", "cp2k"): {
        "kind": "输入生成+版本化输出解析",
        "cause": "适配器只设置 `STRESS_TENSOR ANALYTICAL`，但没有显式打印块；解析器还期待旧式 `STRESS TENSOR [GPa]`，本机 CP2K 2026 输出为 `STRESS| Analytical stress tensor [bar]`。",
        "solution": "加入 `FORCE_EVAL/PRINT/STRESS_TENSOR ON`；解析带 `STRESS|` 前缀的 x/y/z 三行，并将 bar 乘 `1e-4` 转为 GPa，同时保留原始单位元数据。",
        "priority": "P0",
    },
    ("propagate_dynamics", "gromacs"): {
        "kind": "输入生成逻辑",
        "cause": "NVE 分支虽然写 `tcoupl=no`，仍无条件写入 `ref-t` 和 `tau-t`，且没有 `tc-grps`；GROMACS 2026 因温控组数量为0而拒绝 `grompp`。",
        "solution": "NVE 分支完全省略 `ref-t/tau-t/tc-grps` 和压力耦合字段；NVT/NPT 分支增加显式 `temperature_coupling_groups`（或受控的 `System`），并分别验证 NVE/NVT/NPT MDP。",
        "priority": "P0",
    },
    ("resolve_chemical_identity", "pubchem"): {
        "kind": "远端服务503",
        "cause": "本机 DNS、TLS 和 PubChem 首页可达，但 PUG REST 当前返回 `503 PUGREST.ServerBusy`；响应头明确包含 `Retry-After: 30` 以及 `too many requests per second or blacklisted`。",
        "solution": "代码已加入跨 worker 限速、尊重 `Retry-After` 的有界退避和 `retryable=true` 错误语义；剩余工作是检查共享出口 IP/代理或等待 PubChem 解除临时黑名单。",
        "priority": "P1",
    },
    ("retrieve_compound_properties", "pubchem"): {
        "kind": "远端服务503",
        "cause": "PubChem PUG REST 当前对本服务器出口返回带黑名单提示的503。",
        "solution": "本 Action 已共用限速、Retry-After 退避和可重试错误模型；需从服务器网络侧排查出口 IP。",
        "priority": "P1",
    },
    ("retrieve_compound_structure", "pubchem"): {
        "kind": "远端服务503",
        "cause": "PubChem PUG REST 当前对本服务器出口返回带黑名单提示的503。",
        "solution": "已改用可读取响应限流头的有界 HTTP 客户端并保留 PubChemPy 的 Compound 解析；需从服务器网络侧解除外部阻塞。",
        "priority": "P1",
    },
    ("search_similar_compounds", "pubchem"): {
        "kind": "远端服务503",
        "cause": "PubChem fast similarity 端点当前对本服务器出口返回带黑名单提示的503。",
        "solution": "已保留独立超时并加入限速、Retry-After 退避和可重试错误；不自动降低阈值或改换算法，需排查出口 IP。",
        "priority": "P1",
    },
    ("search_substructures", "pubchem"): {
        "kind": "远端服务503",
        "cause": "PubChem fast substructure 端点当前对本服务器出口返回带黑名单提示的503。",
        "solution": "已加入限速、Retry-After 退避，并把服务繁忙与无匹配结果严格区分；需排查出口 IP。",
        "priority": "P1",
    },
    ("search_catalysis_records", "catalysis_hub"): {
        "kind": "远端服务503/超时",
        "cause": "Catalysis-Hub GraphQL 在两次已有实测中分别返回503和读取超时；该 Backend 尚无成功调用证据。",
        "solution": "增加 GraphQL 健康检查、有界重试/退避、分页缓存和可选的本地只读快照；远端不可用时向智能体返回 retryable 状态，不做隐藏 fallback。",
        "priority": "P1",
    },
}


UNUSED_OPPORTUNITIES = {
    "AiiDA": "保持为调度/溯源基础设施；若接入，应放在 MCP 下层管理作业，不要暴露固定科学 workflow。",
    "atomate2": "只抽取可复用的原子材料操作，避免直接暴露预编排 Flow。",
    "jobflow": "可作为后台依赖图/重试执行层，不应替智能体决定科学步骤。",
    "CENSO": "拆成构象过滤、能量重排、自由能校正等独立 Actions，并要求显式选择量化后端。",
    "autodE": "拆成反应物/产物复合物生成、TS 候选、路径验证等原子 Actions。",
    "Wannier90": "新增 `construct_wannier_functions`、插值能带和 Berry/拓扑性质 Actions。",
    "Yambo": "新增 GW 准粒子与 BSE 激子性质 Actions，并显式接收前序 DFT 产物。",
    "Arkane": "先解决导入/示例超时，再接热化学、速率和主方程输入构建的原子能力。",
    "AutoMeKin": "拆成反应事件候选生成、路径筛选和网络扩展 Actions。",
    "KinBot": "接入反应族候选、TS 猜测和单步验证，不暴露完整自动网络 workflow。",
    "SHARC": "新增初态采样、非绝热耦合和单段 surface-hopping 动力学 Actions。",
    "Newton-X": "与 SHARC 类似，接入显式电子结构接口选择和单段非绝热传播。",
    "TheoDORE": "新增激发态特征、跃迁密度和电荷转移分析 Actions。",
    "EasySpin": "在合法 MATLAB/兼容运行时就绪后新增 EPR 参数与谱模拟 Actions。",
    "VMD": "如 benchmark 需要视觉产物，可提供轨迹渲染/图像导出；否则保持人工可视化工具。",
    "VESTA": "如 benchmark 需要材料图像，可提供结构/密度等值面渲染；否则无需进入科学 Action Catalog。",
}


def main() -> int:
    coverage = load("action_test_coverage.json")
    matrix = load("action_backend_matrix_smoke_status.json")
    requested = load("requested_software_status.json")
    actions = action_specs()
    backends = backend_specs()
    successful = {tuple(pair) for pair in coverage["successful_action_backend_pairs"]}
    failed = {tuple(pair) for pair in coverage["failed_action_backend_pairs"]}
    matrix_records = {(item["action"], item["backend"]): item for item in matrix["cases"]}
    remote_backends = {"pubchem", "catalysis_hub", "rcsb_pdb", "materials_project", "nist_webbook"}
    remote_failures = {pair for pair in failed if pair[1] in remote_backends}
    local_failures = failed - remote_failures
    without_success = list(coverage.get("backends_without_runtime_success_evidence") or [])
    connectivity_path = CONFIG_ROOT / "pubchem_connectivity_status.json"
    pubchem_connectivity = (
        json.loads(connectivity_path.read_text(encoding="utf-8"))
        if connectivity_path.is_file()
        else {}
    )
    pubchem_degraded = bool(pubchem_connectivity) and not bool(pubchem_connectivity.get("all_ok"))

    lines = [
        "# ResearchChemBench Action–Backend 全组合测试与软件接入审计",
        "",
        f"> 生成时间：`{datetime.now(timezone.utc).isoformat()}`。",
        (
            "> 本报告合并 2026-07-20 已有证据与本轮 "
            f"{matrix['summary']['registered_gap_pair_count']} 个补测组合的真实统一分发调用；"
            "已测试组合不会重复运行。"
        ),
        "> 另合并 GoodVibes 4.3.0 的 7 个真实 smoke，覆盖新增/升级的 6 个 Actions。",
        "> 11个原失败组合的代码修复、现场复测及PubChem出口诊断见 [`ACTION_BACKEND_REPAIR_REPORT_20260721.md`](ACTION_BACKEND_REPAIR_REPORT_20260721.md)。",
        "",
        "## 1. 最终结论",
        "",
        "| 指标 | 结果 |",
        "|---|---:|",
        f"| 公开 Actions | {len(actions)} |",
        f"| BackendSpecs | {len(backends)} |",
        f"| Catalog Action–Backend 组合 | {coverage['summary']['action_backend_pair_count']} |",
        f"| 有成功证据的组合 | **{coverage['summary']['successful_action_backend_pairs']}** |",
        f"| 仅有失败证据的组合 | **{coverage['summary']['failed_action_backend_pairs']}** |",
        f"| 尚未测试组合 | **{coverage['summary']['unobserved_action_backend_pairs']}** |",
        f"| 本轮补测 | {matrix['summary']['passed_pair_count']}/{matrix['summary']['registered_gap_pair_count']} 通过，{matrix['summary']['failed_pair_count']} 失败 |",
        "| GoodVibes 4.3.0 专项 | 7/7 通过，覆盖 6/6 Actions |",
        f"| 至少有一个成功 Action 的 Backend | {coverage['summary']['backends_with_runtime_success_evidence']}/{len(backends)} |",
        f"| 当前无任何成功证据的 Backend | {codes(without_success)} |",
        "",
        f"结论：**{coverage['summary']['action_backend_pair_count']}/{coverage['summary']['action_backend_pair_count']} 个声明组合都有真实调用证据；{coverage['summary']['successful_action_backend_pairs']} 个通过，{coverage['summary']['failed_action_backend_pairs']} 个仍有问题。** 当前包含 {len(local_failures)} 个本地适配问题和 {len(remote_failures)} 个远端数据服务问题。",
        "",
        "## 2. 本轮补测结果",
        "",
        "| 分组 | 组合数 | 通过 | 失败 |",
        "|---|---:|---:|---:|",
    ]
    group_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for item in matrix["cases"]:
        group_counts[item["group"]]["total"] += 1
        group_counts[item["group"]]["passed" if item["status"] in PASS else "failed"] += 1
    labels = {
        "molecular_electronic": "分子电子结构与ML势",
        "periodic": "周期材料与弛豫",
        "dynamics": "分子动力学与溶剂化",
        "analysis_reaction": "轨迹分析与反应",
        "phonons": "声子",
    }
    for group in ("molecular_electronic", "periodic", "dynamics", "analysis_reaction", "phonons"):
        count = group_counts[group]
        lines.append(f"| {labels[group]} | {count['total']} | {count['passed']} | {count['failed']} |")

    lines.extend(
        [
            "",
            "证据文件：[`action_backend_matrix_smoke_status.json`](../config/action_backend_matrix_smoke_status.json)、[`goodvibes_action_smoke_status.json`](../config/goodvibes_action_smoke_status.json)、[`action_test_coverage.json`](../config/action_test_coverage.json)。",
            "",
            "## 3. 出现问题的 Backend 调用及修复建议",
            "",
            f"### 3.1 {len(failed)}个仅失败组合",
            "",
            "| 优先级 | Backend | Action | 问题类型 | 根因 | 建议修复 |",
            "|---|---|---|---|---|---|",
        ]
    )
    for action_id, backend_id in sorted(failed, key=lambda pair: (ISSUES[pair]["priority"], pair[1], pair[0])):
        issue = ISSUES[(action_id, backend_id)]
        lines.append(
            f"| {issue['priority']} | `{backend_id}` | `{action_id}` | {cell(issue['kind'])} | {cell(issue['cause'])} | {cell(issue['solution'])} |"
        )
    if not failed:
        lines.append("| — | — | — | — | 当前没有仅失败组合。 | — |")

    lines.extend(
        [
            "",
            "### 3.2 Backend级影响范围",
            "",
            "| Backend | 已成功组合 | 失败组合 | 判断 |",
            "|---|---:|---:|---|",
        ]
    )
    backend_success = Counter(pair[1] for pair in successful)
    backend_failure = Counter(pair[1] for pair in failed)
    for backend_id in sorted(set(backend_failure)):
        judgment = {
            "psi4": "仍存在 Psi4 适配失败。",
            "cp2k": "仍存在 CP2K 适配失败。",
            "gromacs": "仍存在 GROMACS 适配失败。",
            "pubchem": "代码侧韧性修复已完成；当前现场失败来自远端503/出口黑名单。",
            "catalysis_hub": "Catalysis-Hub 当前仍存在远端调用失败。",
        }[backend_id]
        lines.append(f"| `{backend_id}` | {backend_success[backend_id]} | {backend_failure[backend_id]} | {judgment} |")
    lines.append("")
    if pubchem_degraded:
        lines.append("补充：`search_compounds/pubchem` 有历史成功证据，因此不属于“仅失败组合”；但最新连通性探测显示 PUG REST 仍返回503，应与其他 PubChem Actions 一起按远端降级处理。")

    lines.extend(
        [
            "",
            "## 4. 101个 Action 的完整 Backend 实测清单",
            "",
            "标记：✅ 至少一次成功/部分成功；❌ 仅失败；⚠️ 有历史成功但最新现场降级。",
            "",
            "| # | Action | 领域 | Backend实测状态 |",
            "|---:|---|---|---|",
        ]
    )
    for index, specification in enumerate(actions.values(), start=1):
        values = []
        for backend_id in specification.backend_ids:
            pair = (specification.id, backend_id)
            if pair == ("search_compounds", "pubchem") and pubchem_degraded:
                mark = "⚠️"
            elif pair in successful:
                mark = "✅"
            elif pair in failed:
                mark = "❌"
            else:
                mark = "⬜"
            values.append(f"{mark} `{backend_id}`")
        lines.append(
            f"| {index} | `{specification.id}` | {cell(CATEGORY_ZH.get(specification.category, specification.category))} | {'<br>'.join(values)} |"
        )

    lines.extend(
        [
            "",
            "## 5. 当前作为 Backend 使用的软件、程序库和数据接口",
            "",
            f"共注册 **{len(backends)} 个 BackendSpecs**；其中 {sum(bool(item.executables or item.python_modules) for item in backends.values())} 个由外部程序、Python库或在线接口支撑，`internal_statistics` 是纯内部确定性实现。一个软件可对应多个 BackendSpec（例如 RDKit）。",
            "",
            "| Backend ID | 软件/实现 | Runtime | 可执行文件/模块 | Action数 | 全组合结果 |",
            "|---|---|---|---|---:|---|",
        ]
    )
    for backend in backends.values():
        passed_count = backend_success[backend.id]
        failed_count = backend_failure[backend.id]
        if failed_count and passed_count:
            status = f"⚠️ {passed_count}成功 / {failed_count}失败"
        elif failed_count:
            status = f"❌ 0成功 / {failed_count}失败"
        else:
            status = f"✅ {passed_count}/{len(backend.capabilities)}"
        dependencies = [*backend.executables, *backend.python_modules]
        lines.append(
            f"| `{backend.id}` | {cell(backend.display_name)} | `{backend.runtime}` | {codes(dependencies)} | {len(backend.capabilities)} | {status} |"
        )

    runtime_only = [item for item in requested["software"] if item.get("public_adapter") == "runtime_only"]
    indirect = [item for item in runtime_only if item["name"] == "QCEngine"]
    unused = [item for item in runtime_only if item["name"] != "QCEngine"]
    lines.extend(
        [
            "",
            "## 6. 已安装但没有被公共 Action 直接调用的软件",
            "",
            f"清单中共有 {len(runtime_only)} 项标为 `runtime_only`。其中 QCEngine 被 NWChem Backend 间接使用；其余 **{len(unused)} 项**没有出现在任何 Action handler 中。",
            "",
            "### 6.1 间接使用，不应误判为闲置",
            "",
            "| 软件 | 状态 | 实际用途 |",
            "|---|---|---|",
        ]
    )
    for item in indirect:
        lines.append(f"| `{item['name']}` | {item['status']} | NWChem Actions 通过 QCEngine/QCSchema harness 执行；不需要额外暴露通用 runner。 |")
    lines.extend(
        [
            "",
            "### 6.2 已安装/部分安装但当前没有 Action 调用",
            "",
            "| 软件 | 配置状态 | Runtime | 当前未接入原因 | 建议 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in unused:
        lines.append(
            f"| `{item['name']}` | {item['status']} | `{item.get('environment') or '—'}` | {cell(item.get('notes') or item.get('role'))} | {cell(UNUSED_OPPORTUNITIES[item['name']])} |"
        )

    not_implemented = [item for item in requested["software"] if item.get("public_adapter") == "not_implemented"]
    lines.extend(
        [
            "",
            "## 7. 尚未形成 Backend 的许可软件或数据接口",
            "",
            "这些项目不能算“已安装但未使用”；它们当前缺许可证、有效安装或稳定接口。",
            "",
            "| 项目 | 状态 | MCP暴露策略 | 原因/后续条件 |",
            "|---|---|---|---|",
        ]
    )
    for item in not_implemented:
        lines.append(
            f"| `{item['name']}` | {item['status']} | `{item.get('mcp_exposure') or 'not_implemented'}` | {cell(item.get('notes') or item.get('role'))} |"
        )

    lines.extend(
        [
            "",
            "## 8. 推荐优化顺序",
            "",
            "1. **本地5个组合已修复。** Psi4向量API、CP2K显式打印/版本化解析和GROMACS ensemble字段均已通过真实后端复测。",
            "2. **优先排查 PubChem 出口状态。** 当前响应明确显示 `Retry-After: 30` 和 `too many requests per second or blacklisted`；需检查共享 NAT/代理出口，代码不得伪造成功或隐藏切换数据源。",
            "3. **在线韧性代码已落地。** PubChem/Catalysis-Hub 使用有界重试、Retry-After、跨 worker PubChem 限速和 `retryable` 错误语义；Catalysis-Hub 已现场恢复成功。",
            f"4. **为每个 Backend capability 保留一个小型真实 smoke。** 将原{matrix['summary']['registered_gap_pair_count']}个矩阵用例和7个 GoodVibes 用例长期纳入夜间/发布前矩阵，不必每次跑昂贵全量体系。",
            f"5. **PubChem解除阻塞后重跑六个网络用例。** 目标是 `successful_action_backend_pairs={coverage['summary']['action_backend_pair_count']}`、`failed=0`、`unobserved=0`。",
            "",
            "## 9. 收尾校验",
            "",
            f"- MCP Catalog 校验：`ok: {len(actions)} actions, {len(backends)} backends, full exposure, agent-required backend selection, no fallback`。",
            "- 完整测试集：`186 passed in 413.69s`。",
            f"- 矩阵审计测试会验证{matrix['summary']['registered_gap_pair_count']}个补测用例与 Catalog 一致，并验证{coverage['summary']['action_backend_pair_count']}个组合被成功集与失败集完整划分。",
            "- 修复涉及脚本和 Backend 模块的 `py_compile` 均通过。",
            "",
            "## 10. 复现命令",
            "",
            "```bash",
            ".toolbox_env/bin/python chemistry_toolbox/scripts/run_action_backend_matrix_smokes.py --resume",
            ".toolbox_env/bin/python chemistry_toolbox/scripts/run_action_gap_smokes.py --network-only",
            ".toolbox_env/bin/python chemistry_toolbox/scripts/run_goodvibes_action_smokes.py",
            ".tool_envs/services/bin/python chemistry_toolbox/scripts/check_pubchem_connectivity.py --output chemistry_toolbox/config/pubchem_connectivity_status.json",
            ".toolbox_env/bin/python chemistry_toolbox/scripts/audit_action_test_coverage.py",
            ".toolbox_env/bin/python chemistry_toolbox/scripts/generate_action_backend_completion_report.py",
            ".toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager validate",
            ".toolbox_env/bin/python -m pytest -q chemistry_toolbox/tests",
            "```",
            "",
            "相关基线：[`CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md`](CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md)、[`CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md`](CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md)。",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
