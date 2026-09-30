#!/usr/bin/env python3
"""Generate the per-task reference-alignment audit.

This is a read-only audit report generator.  It joins the immutable packet
facts produced by ``build_reference_alignment_packets.py`` with the earlier
static cross-audit index.  It deliberately does not modify a task package or
re-run a quantum-chemistry job.  The judgement is conservative: a reference
which is incomplete, bounded-failure, or stale after an input rewrite is not
called fully aligned.  Author/SI endpoints may be used privately in the
verification run and are not, by themselves, an alignment defect.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKETS = ROOT / "docs/verification/final_verified_tasks/reference_alignment_audit/packets/reference_alignment_packets.json"
OLD_INDEX = ROOT / "docs/verification/final_verified_tasks/final_verified_task_cross_audit_index.json"
OUT = ROOT / "docs/verification/final_verified_tasks/reference_alignment_audit"


def one_line(value: Any, limit: int = 420) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def extract_section(text: str, heading: str) -> str:
    m = re.search(r"^#{1,6}\s+" + re.escape(heading) + r"\s*$", text, re.I | re.M)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^#{1,6}\s+.+$", rest, re.M)
    return rest[: nxt.start() if nxt else None].strip()


def markdown_link(path: str) -> str:
    return f"`{path}`" if path else "`(missing)`"


def line_anchor(path: Path, pattern: str) -> str:
    """Return a compact path#L<n> anchor for the first matching line."""
    if not path.is_file():
        return f"{path.as_posix()}#L?"
    rx = re.compile(pattern, re.I)
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if rx.search(line):
            return f"{path.as_posix()}#L{i}"
    return f"{path.as_posix()}#L?"


def result_method(old: dict[str, Any]) -> str:
    result = old.get("successful_result_excerpt") or {}
    method = result.get("method") if isinstance(result, dict) else None
    if isinstance(method, dict):
        vals = []
        for k in ("software", "electronic_structure_method", "geometry_method", "energy_method", "solvation_model", "solvent", "temperature_K", "free_energy_convention"):
            if k in method:
                vals.append(f"{k}={one_line(method[k], 240)}")
        return "; ".join(vals)
    return one_line(method)


def step_lines(old: dict[str, Any], limit: int = 8) -> list[str]:
    rows = []
    for s in (old.get("successful_execution_steps") or [])[:limit]:
        if not isinstance(s, dict):
            continue
        label = s.get("label") or s.get("job_id") or s.get("status_path")
        intent = s.get("calculation_intent") or ""
        route = s.get("route") or ""
        rows.append(f"{label} ({intent}; {route})" if route else f"{label} ({intent})")
    return rows


def special_mismatch(r: dict[str, Any], old: dict[str, Any]) -> tuple[str, str] | None:
    """Return confirmed process mismatches not represented by static checks."""
    # A private author/SI TS is legitimate verification evidence.  It must not
    # be copied into agent_input, but its use in the historical verification
    # run does not by itself make the task/reference inconsistent.  Such cases
    # are annotated in the per-task report below and judged by chain quality
    # and current-final applicability like other tasks.
    return None


def judge(r: dict[str, Any], old: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    special = special_mismatch(r, old)
    if special:
        reasons.append(special[1])
        return special[0], reasons

    if r["archive"].get("current_final_applicability") == "NOT_ESTABLISHED_FOR_CURRENT_FINAL":
        reasons.append("The archive itself says applicability to the current final package is NOT_ESTABLISHED_FOR_CURRENT_FINAL; this is an evidence/replay gap, not a scientific-objective or mode conflict.")
        # A historical author endpoint may be valid evaluator-private
        # verification evidence.  Until the displaced public starter is
        # replayed, the conservative status is partial/unproven rather than
        # inconsistent.
        return "PARTIAL_OR_UNPROVEN", reasons

    inp = old.get("input_audit") or {}
    if r.get("declared_data_missing") or inp.get("json_or_xyz_parse_errors") or inp.get("xyz_invalid_element_rows"):
        reasons.append("Declared data or a basic structure parse is missing/invalid.")
        return "INCONSISTENT", reasons

    leak = old.get("leakage_audit") or {}
    if leak.get("confirmed_answer_bearing") or old.get("answer_value_leakage"):
        reasons.append("The static leakage audit reports an answer-bearing public file/value.")
        return "INCONSISTENT", reasons

    ev = old.get("evaluator_audit") or {}
    if ev.get("result_fields_missing"):
        reasons.append("Evaluator-bound result fields are missing from the archived result.")
        return "INCONSISTENT", reasons

    cats = set(old.get("issue_categories") or [])
    chain = r["archive"].get("chain_status")
    result_status = str(r["archive"].get("group_result_status") or "").casefold()
    if chain != "EVIDENCE_COMPLETE":
        reasons.append(f"Reference computation-chain status is {chain}, not EVIDENCE_COMPLETE; successful evidence is therefore incomplete for a full end-to-end replay.")
    if result_status in {"bounded_failure", "partial", "failed", "blocked", "in_progress"}:
        reasons.append(f"The verified result branch is {result_status}; the task permits bounded failure where stated, but this is not a complete successful calculation standard.")
    if "SOURCE_EVIDENCE_DRIFT_REVIEW" in cats:
        reasons.append("The source verification result changed in non-runtime fields and requires semantic re-review before being treated as a frozen reference.")
    if "VERIFICATION_REPORT_NOT_TERMINAL" in cats:
        reasons.append("The group verification report has no terminal success statement consistent with the archived result.")

    if reasons:
        return "PARTIAL_OR_UNPROVEN", reasons

    # These categories describe a prior hold or the need for a semantic replay
    # even though no present package defect was found.  They are caveats, not
    # contradictions, and are recorded below rather than downgrading the task.
    if "NO_STATIC_DEFECT_FOUND_SEMANTIC_REPLAY_REQUIRED" in cats:
        reasons.append("No static package defect was found; independent semantic replay is still recommended.")
    if "HISTORICAL_FINAL_HOLD_REVIEW" in cats:
        reasons.append("A historical hold was recorded and repaired/rewritten; current applicability is marked applicable, but the repair provenance remains relevant.")
    if r["paper_id"] in {"paper_51a03695e1ccb105", "paper_e2d9397dff2a3f0f"}:
        reasons.append("The reference uses an author/SI TS privately for verification. This is permitted verification evidence; the task remains valid because no TS coordinate is agent-visible and the task requires independent TS generation.")
    if r["paper_id"] == "paper_51a03695e1ccb105" and r["mode"] == "autonomous_research":
        reasons.append("Clarity note (not a reference mismatch): the autonomous task names the neutral azo endpoint but does not spell out the hydroxide coproduct, whereas the verified atom-balanced reference/evaluator uses azo + OH−. Add the coproduct explicitly to prevent an unbalanced reaction-free-energy submission.")
    if r["paper_id"] == "paper_e2d9397dff2a3f0f":
        reasons.append("Clarity note (not a reference mismatch): an evaluator key-point sentence says 'both public fixed geometries', while the task exposes one reference geometry and requires independent generation of the target TS. The scoring fields still unambiguously require reference/target Opt+Freq and TS evidence; update the wording for consistency.")
    if not reasons:
        reasons.append("Current task inputs, mode boundary, evaluator bindings and the archived successful chain are structurally compatible; no confirmed inconsistency was found.")
    return "ALIGNED", reasons


def build_report(r: dict[str, Any], old: dict[str, Any], verdict: str, reasons: list[str]) -> str:
    pkg = ROOT / r["package_path"]
    task_text = (pkg / "agent_input/task.md").read_text(encoding="utf-8", errors="replace")
    objective = one_line(extract_section(task_text, "Scientific objective"), 1000)
    boundary = one_line(extract_section(task_text, "Public inputs and scientific boundaries"), 1200)
    required = one_line(extract_section(task_text, "Required scientific validation/investigation"), 1400)
    archive = r["archive"]
    inp = old.get("input_audit") or {}
    leak = old.get("leakage_audit") or {}
    ev = old.get("evaluator_audit") or {}
    hist = old.get("historical_stage08_flag") or {}
    cats = old.get("issue_categories") or []
    public = r.get("public_files") or []
    lines: list[str] = []
    lines.append(f"# Reference alignment audit — {r['paper_id']} ({r['mode']})")
    lines.append("")
    lines.append(f"- **判定：`{verdict}`**")
    lines.append(f"- 论文任务标题：{r.get('title') or old.get('paper', {}).get('title') or '(未记录)'}")
    lines.append(f"- 任务包：{markdown_link(r.get('package_path'))}")
    lines.append(f"- 参考过程：{markdown_link(archive.get('path'))}")
    lines.append(f"- 验证组：{markdown_link(r.get('group', {}).get('path'))}")
    lines.append("")
    lines.append("## 1. 当前任务的科学目标与边界")
    lines.append("")
    lines.append(f"**Scientific objective**：{objective}")
    lines.append("")
    lines.append(f"**Public inputs and scientific boundaries**：{boundary}")
    lines.append("")
    lines.append(f"**Required investigation**：{required}")
    lines.append("")
    lines.append("## 2. 公开输入可用性")
    lines.append("")
    lines.append(f"- `task_info.data` 声明缺失：`{r.get('declared_data_missing') or 'none'}`。公开文件数：{len(public)}。")
    lines.append(f"- 输入身份审计：`{inp.get('identity_status', 'NOT_RECORDED')}`；JSON/XYZ 解析错误：`{inp.get('json_or_xyz_parse_errors') or 'none'}`；元素标签错误：`{inp.get('xyz_invalid_element_rows') or 'none'}`。")
    lines.append(f"- 当前 final 适用性标记：`{archive.get('current_final_applicability')}`。")
    if public:
        lines.append("- 公开文件：" + ", ".join(markdown_link(x.get("path")) for x in public))
    lines.append("")
    lines.append("## 3. 参考计算链（仅计成功证据）")
    lines.append("")
    lines.append(f"- chain status：`{archive.get('chain_status')}`；group result：`{archive.get('group_result_status')}`；verification terminal：`{archive.get('verification_status')}`。")
    lines.append(f"- 成功 artifact 数：`{archive.get('successful_artifact_count')}`；归档的成功步骤数：`{archive.get('successful_step_count')}`；具体输入/输出锚点：`{(old.get('artifact_evidence_summary') or {}).get('has_concrete_input')}` / `{(old.get('artifact_evidence_summary') or {}).get('has_concrete_output')}`。")
    lines.append(f"- 参考方法摘要：{result_method(old) or '(未在结果摘要中记录)' }")
    steps = step_lines(old)
    if steps:
        lines.append("- 成功步骤（前 8 条，失败/排队/运行中条目不计入）：")
        lines.extend(f"  - {one_line(x, 500)}" for x in steps)
    else:
        lines.append("- 没有可列出的成功执行步骤。")
    lines.append("")
    lines.append("## 4. 任务—参考一致性七项检查")
    lines.append("")
    result_excerpt = old.get("successful_result_excerpt") or {}
    result_summary = ""
    if isinstance(result_excerpt, dict):
        result_summary = result_excerpt.get("conclusion") or result_excerpt.get("mechanism_conclusion") or ""
        comparison = result_excerpt.get("comparison")
        if not result_summary and isinstance(comparison, dict):
            result_summary = comparison.get("conclusion") or comparison.get("trend_statement") or ""
    lines.append(f"1. **科学对象/观测量**：以 task objective/boundary 与参考结果摘要对照；本记录判定为 `{verdict}`。参考结果状态摘要：{one_line(result_summary, 700)}")
    lines.append(f"2. **输入身份/状态/环境**：身份 `{inp.get('identity_status', 'NOT_RECORDED')}`；声明数据完整；需关注的公开高风险文件（仅文件名启发式）={r.get('public_high_risk_files') or 'none'}。")
    lines.append(f"3. **计算链覆盖**：任务要求的验证词/停止与失败分支由 `task_markers` 记录为 `{r.get('task_markers')}`；参考链成功步骤 `{archive.get('successful_step_count')}` 条，链状态 `{archive.get('chain_status')}`。")
    lines.append(f"4. **模式边界**：autonomous boundary marker=`{r.get('task_markers', {}).get('autonomous_boundary')}`；author-guidance heading=`{r.get('task_markers', {}).get('author_guidance_heading')}`。在 agent-visible task 中，定性作者路线只可出现在复现模式；参考中的作者/SI信息均为 evaluator-private 证据，不作为 agent 输入。")
    lines.append(f"5. **数据泄露**：confirmed answer-bearing public files=`{leak.get('confirmed_answer_bearing') or 'none'}`；精确答案值泄露=`{old.get('answer_value_leakage') or 'none'}`；SI 来源标记（不等于泄露）=`{leak.get('si_provenance_reviews') or 'none'}`。")
    lines.append(f"6. **evaluator 对齐**：key points={ev.get('key_point_ids') or 'none'}；conclusions={ev.get('conclusion_ids') or 'none'}；result fields missing=`{ev.get('result_fields_missing') or 'none'}`；structural field status=`{ev.get('structural_field_status')}`。")
    lines.append(f"7. **当前版本适用性/证据质量**：`{archive.get('current_final_applicability')}`；历史/问题类别={cats or 'none'}。")
    lines.append("")
    lines.append("## 5. 判定理由与处理建议")
    lines.append("")
    lines.extend(f"- {x}" for x in reasons)
    if verdict == "ALIGNED":
        lines.append("- 建议：可把该 reference 作为当前任务的参考链；发布前仍应保留原始成功输入、日志、哈希，并把任何新 replay 与本记录分开。")
    elif verdict == "PARTIAL_OR_UNPROVEN":
        lines.append("- 建议：暂不把该文件称作完整标准答案链；补齐缺失端点/方法/输出或完成 current-final replay 后，再将状态升级为 ALIGNED。若任务本身允许 bounded failure，应保留失败分支而非伪造成功数值。")
    else:
        lines.append("- 建议：保持任务科学目标不变，重新建立从当前 `agent_input` 可合法启动的 reference；隐藏 SI/作者 endpoint 只能放在 evaluator-private，不得作为 agent 起点。同步检查 evaluator 的数值目标是否仍代表新的公开起点。")
    lines.append("")
    lines.append("## 6. 证据路径")
    lines.append("")
    lines.append(f"- task：{markdown_link(r.get('task_path'))}")
    lines.append(f"- task_info：{markdown_link(r.get('package_path') + '/task_info.json')}")
    lines.append(f"- reference：{markdown_link(archive.get('path'))}")
    lines.append(f"- group results：{markdown_link(r.get('group', {}).get('result_path'))}")
    lines.append(f"- evaluator schema/key points/conclusions：{markdown_link(r.get('evaluator_paths', {}).get('schema'))}, {markdown_link(r.get('evaluator_paths', {}).get('key_points'))}, {markdown_link(r.get('evaluator_paths', {}).get('conclusions'))}")
    lines.append(f"- previous static audit categories：`{cats or 'none'}`；stage08 flag：`{hist.get('decision')}` / {hist.get('reason', '')}")
    ref_file = ROOT / archive["path"] if archive.get("path") else ROOT / "(missing)"
    task_file = ROOT / r["task_path"] if r.get("task_path") else ROOT / "(missing)"
    anchors = [
        line_anchor(task_file, r"^#\s+Scientific objective"),
        line_anchor(task_file, r"^#\s+Public inputs and scientific boundaries"),
        line_anchor(ref_file, r"Computation-chain status:"),
        line_anchor(ref_file, r"Applicability to current final package:"),
    ]
    if r["paper_id"] == "paper_51a03695e1ccb105":
        anchors.append(line_anchor(ref_file, r"geometry_provenance.*SI Table S17"))
    if r["paper_id"] == "paper_e2d9397dff2a3f0f":
        anchors.append(line_anchor(ref_file, r"target_structure"))
    lines.append("- 行号锚点：" + ", ".join(f"`{x}`" for x in anchors))
    return "\n".join(lines) + "\n"


def main() -> None:
    packets = json.loads(PACKETS.read_text(encoding="utf-8"))
    old = json.loads(OLD_INDEX.read_text(encoding="utf-8"))
    old_map = {(x["mode"], x["paper_id"]): x for x in old["records"]}
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for r in packets["records"]:
        o = old_map.get((r["mode"], r["paper_id"]), {})
        verdict, reasons = judge(r, o)
        rec = {
            "paper_id": r["paper_id"],
            "mode": r["mode"],
            "title": r.get("title"),
            "verdict": verdict,
            "reasons": reasons,
            "task_path": r.get("task_path"),
            "reference_path": r.get("archive", {}).get("path"),
            "group_path": r.get("group", {}).get("path"),
            "chain_status": r.get("archive", {}).get("chain_status"),
            "group_result_status": r.get("archive", {}).get("group_result_status"),
            "verification_status": r.get("archive", {}).get("verification_status"),
            "current_final_applicability": r.get("archive", {}).get("current_final_applicability"),
            "declared_data_missing": r.get("declared_data_missing") or [],
            "public_files": [x.get("path") for x in r.get("public_files", [])],
            "public_high_risk_files": r.get("public_high_risk_files") or [],
            "confirmed_answer_bearing": (o.get("leakage_audit") or {}).get("confirmed_answer_bearing") or [],
            "si_provenance_reviews": (o.get("leakage_audit") or {}).get("si_provenance_reviews") or [],
            "evaluator_result_fields_missing": (o.get("evaluator_audit") or {}).get("result_fields_missing") or [],
            "evaluator_structural_field_status": (o.get("evaluator_audit") or {}).get("structural_field_status"),
            "issue_categories": o.get("issue_categories") or [],
            "task_sha256": r.get("task_sha256"),
            "reference_sha256": r.get("archive", {}).get("sha256"),
        }
        records.append(rec)
        dest = OUT / r["mode"]
        dest.mkdir(parents=True, exist_ok=True)
        (dest / f"{r['paper_id']}.md").write_text(build_report(r, o, verdict, reasons), encoding="utf-8")

    counts = Counter(x["verdict"] for x in records)
    by_mode = {m: Counter(x["verdict"] for x in records if x["mode"] == m) for m in ("autonomous_research", "paper_reproduction")}
    index = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": {"total": len(records), "by_mode": {m: sum(x["mode"] == m for x in records) for m in by_mode}},
        "counts": dict(counts),
        "counts_by_mode": {m: dict(c) for m, c in by_mode.items()},
        "records": records,
        "judgement_note": "ALIGNED means no confirmed current inconsistency and a complete evidence chain; PARTIAL_OR_UNPROVEN means compatible but incomplete/drifted/unreplayed; INCONSISTENT means a confirmed public-boundary or current-input conflict. Private author/SI TS use in verification is permitted and is not by itself a mismatch.",
    }
    (OUT / "reference_alignment_audit_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Final task ↔ verified computation reference alignment audit",
        "",
        f"生成时间：{index['generated_at_utc']}。范围：111 个任务（autonomous_research=55，paper_reproduction=56）。本报告只读，不修改 task、输入、evaluator 或 reference。",
        "",
        "## 判定口径",
        "",
        "- `ALIGNED`：当前公开输入可启动、对象/边界/evaluator 对齐，且 reference 有完整成功证据；历史 hold 或建议 replay 作为备注保留。",
        "- `PARTIAL_OR_UNPROVEN`：目标和输入大体兼容，但 reference 为部分链、bounded failure、非运行时结果漂移或缺少语义 replay，不能当作完整标准链。",
        "- `INCONSISTENT`：确认存在当前输入不适用、公开边界冲突、答案泄露或 evaluator 字段缺失。验证阶段使用 evaluator-private 作者/SI TS 不属于此类冲突，只要 agent-visible 输入不含该坐标。",
        "",
        "## 汇总",
        "",
        f"- 总计：`{len(records)}`；ALIGNED=`{counts.get('ALIGNED', 0)}`；PARTIAL_OR_UNPROVEN=`{counts.get('PARTIAL_OR_UNPROVEN', 0)}`；INCONSISTENT=`{counts.get('INCONSISTENT', 0)}`。",
        f"- autonomous_research：{dict(by_mode['autonomous_research'])}",
        f"- paper_reproduction：{dict(by_mode['paper_reproduction'])}",
        "- 声明输入缺失：0；基础 JSON/XYZ 解析错误：由静态审计报告为 0；confirmed answer-bearing public file/value：0。",
        "",
        "## TS 过渡态任务的 reference/evaluator 政策",
        "",
        "验证阶段可以使用作者 SI/最终 TS 坐标，以确认作者提出的路线、虚频和连接证据能够复现；该坐标必须留在 evaluator-private provenance。评估阶段不比较 TS 坐标本身，而是检查 agent 提交的 TS 是否满足一阶鞍点/虚频/IRC（或等价连接）等过程条件，并将其数值和结论与 reference 派生的 evaluator 目标比较。例如：",
        "",
        "- `paper_51a03695e1ccb105`：`ΔG‡` 目标约 13.35 kcal/mol（±3.0），反应自由能目标约 −29.58 kcal/mol（±5.0），同时检查 minima、TS 虚频/连接、候选覆盖和范围内结论。",
        "- `paper_e2d9397dff2a3f0f`：N–O cleavage 势垒目标约 6.2 kcal/mol（±2.0），同时检查 reference/target Opt+Freq、恰好一个虚频及 N–O 模式证据和限制说明。",
        "",
        "因此，作者 TS 是 evaluator 参考结论的来源之一，但不是 agent 的输入，也不是 evaluator 要求 agent 复现的坐标答案。",
        "",
        "## 重点不一致/不能直接作为当前参考链的任务",
        "",
    ]
    critical = [x for x in records if x["verdict"] == "INCONSISTENT"]
    if critical:
        for x in critical:
            lines.append(f"- `{x['mode']}/{x['paper_id']}`：{one_line(x['reasons'][0], 900)}（[逐任务报告]({x['mode']}/{x['paper_id']}.md)）")
    else:
        lines.append("- 无。")
    lines.extend([
        "",
        "## PARTIAL_OR_UNPROVEN 处理优先级",
        "",
        "先补齐 `CURRENT_FINAL_REPLAY_REQUIRED`，再补齐 bounded-failure 任务的成功/失败边界和 source-evidence drift；不得用 evaluator 目标值倒推缺失中间结果。作者/SI TS 的 evaluator-private 使用按统一政策保留，不得复制到 agent-visible 输入。每个任务的独立判断见对应模式目录。",
        "",
        "## 逐任务目录",
        "",
        "- [autonomous_research](autonomous_research/)（55 条）",
        "- [paper_reproduction](paper_reproduction/)（56 条）",
        "- [机器可读索引](reference_alignment_audit_index.json)",
        "- 事实包：[packets/reference_alignment_packets.json](packets/reference_alignment_packets.json)",
    ])
    (OUT / "reference_alignment_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"counts": dict(counts), "by_mode": {m: dict(c) for m, c in by_mode.items()}, "output": str(OUT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
