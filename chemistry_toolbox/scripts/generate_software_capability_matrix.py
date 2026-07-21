#!/usr/bin/env python3
"""Render the software capability audit from the managed cache index."""

from __future__ import annotations

import json
import re
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
INDEX = ROOT / ".software_cache" / "documentation" / "index.json"
OUTPUT = TOOLBOX_ROOT / "docs" / "CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md"


def _cell(values: list[str] | None, *, limit: int = 12) -> str:
    items = list(values or [])
    if not items:
        return "—"
    shown = items[:limit]
    text = "<br>".join(f"`{value}`" for value in shown)
    if len(items) > limit:
        text += f"<br>…另有 {len(items) - limit} 项"
    return text


def _plain(value: object) -> str:
    text = str(value or "—").replace("|", "\\|")
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    value = json.loads(INDEX.read_text(encoding="utf-8"))
    records = list(value.get("software") or [])
    public = [item for item in records if item.get("current_validated_actions")]
    candidate = [item for item in records if item.get("candidate_actions")]
    documented = [item for item in records if item.get("official_sources")]
    lines = [
        "# ResearchChemBench 软件能力扩展矩阵",
        "",
        f"> 生成时间：`{value.get('generated_at')}`。由 `chemistry_toolbox/scripts/generate_software_capability_matrix.py` 从本地资料缓存生成。",
        "",
        "## 1. 审计摘要",
        "",
        "| 项目 | 数量 |",
        "|---|---:|",
        f"| 软件/算法/数据源记录 | {len(records)} |",
        f"| 已有公开 Action 映射 | {len(public)} |",
        f"| 已登记候选扩展 Action | {len(candidate)} |",
        f"| 已登记官方资料入口 | {len(documented)} |",
        "",
        "能力状态必须按 `documented → installed → adapted → validated` 逐级提升。表中的候选 Action 不能直接理解为当前 MCP 可用能力。",
        "",
        "## 2. 已审计候选扩展",
        "",
        "| 软件 | 检测版本 | 当前已验证 Actions | 候选 Actions | 官方资料 |",
        "|---|---|---|---|---|",
    ]
    for item in sorted(candidate, key=lambda row: row["software_id"]):
        sources = "<br>".join(
            f"[{source.get('title', 'official')}]({source.get('url')})"
            for source in item.get("official_sources") or []
        ) or "—"
        lines.append(
            "| {name}<br>`{sid}` | {versions} | {current} | {candidates} | {sources} |".format(
                name=_plain(item.get("display_name")),
                sid=item["software_id"],
                versions=_plain(", ".join(item.get("detected_versions") or []) or "unknown"),
                current=_cell(item.get("current_validated_actions")),
                candidates=_cell(item.get("candidate_actions"), limit=20),
                sources=sources,
            )
        )

    lines.extend(
        [
            "",
            "## 3. 完整软件、算法和数据源清单",
            "",
            "| ID / 名称 | 检测版本 | 清单状态 / Adapter | 当前公开 Actions | 候选 Actions | 本地资料 | 备注 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in sorted(records, key=lambda row: row["software_id"]):
        versions = ", ".join(item.get("detected_versions") or []) or "unknown"
        status = f"{item.get('inventory_status') or 'not listed'}<br>{item.get('public_adapter') or 'catalog/backend only'}"
        downloads = len(item.get("downloads") or [])
        errors = len(item.get("download_errors") or [])
        local_documents = item.get("local_documents") or []
        local_available = sum(bool(document.get("available")) for document in local_documents)
        local = (
            f"sources={len(item.get('official_sources') or [])}<br>"
            f"downloads={downloads}<br>local_docs={local_available}/{len(local_documents)}<br>"
            f"errors={errors}"
        )
        lines.append(
            "| `{sid}`<br>{name} | {versions} | {status} | {current} | {candidates} | {local} | {notes} |".format(
                sid=item["software_id"],
                name=_plain(item.get("display_name")),
                versions=_plain(versions),
                status=status,
                current=_cell(item.get("current_validated_actions")),
                candidates=_cell(item.get("candidate_actions")),
                local=local,
                notes=_plain(item.get("notes")),
            )
        )

    lines.extend(
        [
            "",
            "## 4. 判定规则",
            "",
            "- `current_validated_actions` 来自当前 `BACKEND_SPECS`，表示已经进入公共 Catalog；仍需以测试报告确认科学正确性。",
            "- `candidate_actions` 来自官方功能审计，只表示计划适配方向。",
            "- `runtime_only` 表示软件已安装或已缓存，但没有完整 ActionSpec、BackendSpec、Handler、Artifact 和端到端测试链。",
            "- 数据源客户端、解析库和工作流框架不自动成为 Agent 可选计算 Backend。",
            "- 本地资料位于 `.software_cache/documentation/<software>/<version>/`，下载文件带 SHA-256 和原始 URL。",
            "- 软件包内置手册保留在对应 `.software_cache/<software>/<version>/`，矩阵同时记录路径、大小和 SHA-256，不重复复制大型许可文件。",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "records": len(records)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
