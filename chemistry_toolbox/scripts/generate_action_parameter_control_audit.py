#!/usr/bin/env python3
"""Generate the per-Action controllable/fixed parameter audit."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, REPOSITORY_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.catalog import catalog_snapshot
from researchchem_toolbox.discovery import inspect_action
from researchchem_toolbox.specs import ACTION_SPECS, BACKEND_SPECS


OUTPUT = REPOSITORY_ROOT / "docs/check/ACTION_PARAMETER_CONTROL_AUDIT.md"


def md(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, (dict, list, tuple, bool)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def code(value: str) -> str:
    return f"`{value}`"


def parameter_shape(item: dict[str, Any]) -> str:
    parts = [str(item.get("type") or "documented value")]
    if item.get("allowed_values") is not None:
        parts.append("可选=" + md(item["allowed_values"]))
    if item.get("minimum") is not None:
        parts.append("min=" + md(item["minimum"]))
    if item.get("maximum") is not None:
        parts.append("max=" + md(item["maximum"]))
    if item.get("maximum_items") is not None:
        parts.append("最多项=" + md(item["maximum_items"]))
    return "; ".join(parts)


def section_rows(contract: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for section_name in ("inputs", "method_spec", "action_settings", "resource_limits"):
        section = contract["sections"][section_name]
        values = [
            *section.get("required", []),
            *section.get("optional", []),
            *section.get("optional_documented", []),
            *section.get("optional_with_defaults", []),
        ]
        seen: set[str] = set()
        for item in values:
            field_name = str(item["name"])
            if field_name in seen:
                continue
            seen.add(field_name)
            rows.append((f"{section_name}.{field_name}", item))
    return rows


def selection_rows(action: Any, provider: Any) -> list[tuple[str, dict[str, Any]]]:
    values: list[tuple[str, dict[str, Any]]] = []
    if action.selection_policy in {"agent_backend_required", "agent_components_required"}:
        values.append(
            (
                "backend_id",
                {
                    "required": True,
                    "type": "provider id",
                    "allowed_values": list(action.backend_ids),
                    "description": "智能体为该 Action 显式选择的科学软件/后端。",
                    "impact": "改变后端可能改变可用方法、数值实现、性能、许可证约束和结果；系统不会自动回退。",
                },
            )
        )
    elif action.selection_policy == "agent_source_required":
        values.append(
            (
                "source_id",
                {
                    "required": True,
                    "type": "data source id",
                    "allowed_values": list(action.backend_ids),
                    "description": "智能体显式选择的外部数据源。",
                    "impact": "改变数据源可能改变记录覆盖、字段、版本和远程服务行为。",
                },
            )
        )
    for role in provider.required_component_roles.get(action.id, ()):
        values.append(
            (
                f"component_backends.{role}",
                {
                    "required": True,
                    "type": "component backend id",
                    "allowed_values": list(
                        provider.component_backend_options[action.id][role]
                    ),
                    "description": f"复合 Action 的 {role} 组件后端。",
                    "impact": "改变组件会改变复合计算中的实际科学引擎和对应嵌套参数要求。",
                },
            )
        )
    return values


def main() -> int:
    snapshot = catalog_snapshot(include_health=False)
    backend_map = {item.id: item for item in BACKEND_SPECS}
    pair_count = sum(len(item.backend_ids) for item in ACTION_SPECS)
    category_counts = Counter(item.category for item in ACTION_SPECS)
    controllable_count = 0
    fixed_count = 0

    lines = [
        "# Chemistry Toolbox Action 参数可控性审计",
        "",
        "> 生成日期：2026-07-24  ",
        "> 范围：当前冻结目录中的全部预设 Action 及其全部 Backend 组合。  ",
        "> 生成器：`chemistry_toolbox/scripts/generate_action_parameter_control_audit.py`",
        "",
        "## 1. 结论",
        "",
        "本次修改把 Action 参数目录统一成四个可控区：`inputs`、`method_spec`、`action_settings` 和 `resource_limits`。每个公开字段现在都包含用途和影响；可选字段包含真实默认值；必填字段明确标记为必须由智能体提供，不再借后端防御性 fallback 冒充公开默认值。后端运行时、可执行文件白名单、资源上限和禁止自动回退等约束则单独列为不可控制参数。",
        "",
        "`export_electron_density_grid/orca` 的 `action_settings.grid_points_per_axis` 默认值已从 100 改为 **300**，即默认生成 **300³ = 27,000,000** 个体素。允许范围为 20–400。相对 100³，300³ 的体素数、理想内存/文件量和主要网格处理成本约增加 27 倍；更细网格通常减小离散化误差，但并非越大越必然正确，仍需做收敛检查。实际采用的点数现在写入 Action 结果和 provenance。",
        "",
        "## 2. 审计规模与定义",
        "",
        f"- Action：{len(ACTION_SPECS)} 个",
        f"- Backend：{len(BACKEND_SPECS)} 个",
        f"- Action/Backend 合同：{pair_count} 组",
        "- 自动检查：遍历全部合同，并静态扫描后端源码中的 `mapping.get(default)` 与条件字段，阻止新增未登记参数。",
        "",
        "可控制参数是智能体能在 `execute_action` 请求中显式提供或覆盖的值。不可控制参数是选择某个 Backend 后由安装、适配器安全边界或服务策略固定的值；若需要改变它们，应新增通用参数能力或选择另一个 Backend，而不是悄悄改写运行结果。",
        "",
        "类别分布：",
        "",
        "| 类别 | Action 数 |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(category_counts.items()))
    lines.extend(
        [
            "",
            "## 3. 重点 Action：ORCA 电子密度网格导出",
            "",
            "| 参数 | 可控性 | 默认/固定值 | 范围 | 作用与影响 |",
            "|---|---|---|---|---|",
            "| `action_settings.grid_points_per_axis` | 智能体可控 | `300` | 20–400 | 每个笛卡尔轴的采样点数；总网格规模约为 N³。增大通常降低离散化误差，但立方级增加时间、内存和 cube 文件大小。 |",
            "| `backend_runtime.cube_boundary_selection` | 不可控 | ORCA `orca_plot` 内部决定 | — | 当前适配器可控制分辨率，但未暴露独立的包围盒/padding 类型入口。 |",
            "| `resource_limits.cpu_cores` | 智能体可控 | `null` | ≥1，ORCA 上限 48 | 影响 ORCA/MPI 资源分配；更多核不保证线性加速，并增加总内存压力。 |",
            "| `resource_limits.memory_mb` | 智能体可控 | `null` | ≥128 MB | 与核数共同决定每进程内存；设置不当会导致 ORCA 内存校验失败。 |",
            "",
            "## 4. 全局资源参数",
            "",
            "下面四项出现在每个 Action 合同中，并在后续逐 Action 计数中重复计入：",
            "",
            "| 参数 | 默认值 | 作用 |",
            "|---|---:|---|",
            "| `resource_limits.walltime_seconds` | `1800` | 同步 Action 的最长运行时间；增大会允许更长计算，也会更久占用工作进程。 |",
            "| `resource_limits.memory_mb` | `null` | 请求的内存预算；过低会失败，核数很高时过大的每进程内存会超过主机预算。 |",
            "| `resource_limits.cpu_cores` | `null` | 请求 CPU 进程/线程数；加速效果依软件和体系而定。 |",
            "| `resource_limits.gpu_count` | `null` | 请求 GPU 数；只对支持 GPU 的后端有效。 |",
            "",
            "## 5. 逐 Action / Backend 参数清单",
            "",
        ]
    )

    for action in sorted(ACTION_SPECS, key=lambda item: item.id):
        lines.extend(
            [
                f"### {code(action.id)}",
                "",
                md(action.description),
                "",
                f"- 类别：`{action.category}`",
                f"- 主要输出：`{action.primary_output}`",
                f"- Provider 选择策略：`{action.selection_policy}`",
                "",
            ]
        )
        for backend_id in action.backend_ids:
            provider = backend_map[backend_id]
            inspected = inspect_action(
                action.id, backend_id=backend_id, snapshot=snapshot
            )
            contract = inspected["selected_request_contract"]
            controllable = [
                *selection_rows(action, provider),
                *section_rows(contract),
            ]
            fixed = list(contract["backend_fixed_parameters"])
            if action.selection_policy in {"fixed_source", "internal_deterministic"}:
                fixed.insert(
                    0,
                    {
                        "path": "backend_runtime.provider_selection",
                        "description": f"Provider is fixed to {backend_id}.",
                        "reason": f"The Action provider-selection policy is {action.selection_policy}.",
                    },
                )
            controllable_count += len(controllable)
            fixed_count += len(fixed)

            lines.extend(
                [
                    f"#### Backend {code(backend_id)}",
                    "",
                    f"可控参数 {len(controllable)} 项；不可控制参数 {len(fixed)} 项。",
                    "",
                    "可控参数：",
                    "",
                    "| 参数路径 | 必填 | 默认值 | 类型/范围 | 作用 | 参数变化的影响 |",
                    "|---|---|---|---|---|---|",
                ]
            )
            for field_path, item in controllable:
                required = bool(item.get("required"))
                default = "—（必须显式提供）" if required else code(md(item.get("default")))
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            code(field_path),
                            "是" if required else "否",
                            default,
                            md(parameter_shape(item)),
                            md(item.get("description") or "—"),
                            md(item.get("impact") or "—"),
                        ]
                    )
                    + " |"
                )
            lines.extend(
                [
                    "",
                    "不可控制参数：",
                    "",
                    "| 参数路径 | 固定内容 | 固定原因 |",
                    "|---|---|---|",
                ]
            )
            for item in fixed:
                lines.append(
                    f"| {code(str(item['path']))} | {md(item.get('description'))} | {md(item.get('reason'))} |"
                )
            conditionals = contract.get("conditional_requirements") or []
            if conditionals:
                lines.extend(["", "条件要求：", ""])
                lines.extend(
                    f"- `{md(item['name'])}`：{md(item['rule'])}"
                    for item in conditionals
                )
            lines.append("")

    lines.extend(
        [
            "## 6. 汇总统计与维护规则",
            "",
            f"- 逐合同列出的智能体可控参数行：{controllable_count} 行（同名全局参数在不同合同中分别计数）。",
            f"- 逐合同列出的不可控制参数行：{fixed_count} 行。",
            "- 所有可选参数必须具有 `default`、`description` 和 `impact`。",
            "- 所有必填参数必须具有 `description` 和 `impact`，且目录不得声称其有公开默认值。",
            "- 后端源码新增 `.get(default)` 或条件参数后，若未进入公开合同，`test_action_parameter_exposure.py` 会失败。",
            "- 参数大小不统一解释为“越大越准确”：网格点数、截断能和采样数通常存在精度/成本权衡；容差往往越小越严格；温度、压力、电荷、方法等会改变物理问题本身。",
            "",
            "## 7. 已知固定边界",
            "",
            "1. ORCA `orca_plot` 的 cube 包围盒/padding 当前仍由软件内部决定；只开放每轴点数。若后续需要严格比较不同尺寸分子的体素间距，应新增通用的“显式网格边界/原点/轴向”能力。",
            "2. Multiwfn `calculate_electron_isodensity_surface` 的历史字段名为 `grid_spacing_angstrom`，而安装版菜单提示输入单位为 Bohr。当前审计把该单位语义差异显式列入不可控制约束，没有在本次参数目录修改中静默改变旧任务数值；建议另行做带迁移兼容的字段修正。",
            "3. 可执行程序、Python 模块、许可证和安装数据由运维环境固定；智能体可以选择目录中其他 Backend，或使用允许的原生软件/可编程层，但预设 Action 不允许替换已选 Backend 的实现。",
            "",
            "## 8. 验证",
            "",
            "本报告对应的实现由以下测试保护：",
            "",
            "- `chemistry_toolbox/tests/test_action_parameter_exposure.py`：全部合同的用途、影响、默认值、固定约束与源码隐藏字段检查。",
            "- `chemistry_toolbox/tests/test_electron_density_surface_actions.py`：300³ 默认菜单、覆盖参数和结果/provenance 记录检查。",
            "- `chemistry_toolbox/tests/test_progressive_discovery.py`：渐进式目录和请求模板回归检查。",
            "",
        ]
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
