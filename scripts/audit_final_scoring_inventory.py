"""Read-only final package inventory; writes audit artifacts only when requested."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from evaluation.contracts import validate_task_package
from evaluation.scoring.adapters import _runtime_contract
from evaluation.scoring.rules import associate_rules


ROOT = Path(__file__).resolve().parents[1]
MODES = ("autonomous_research", "paper_reproduction")


def read(path):
    return json.loads(path.read_text())


def inventory():
    rows, details = [], []
    for mode in MODES:
        for task in sorted((ROOT / "tasks" / f"final_verified_{mode}").glob("paper_*")):
            if not task.is_dir():
                continue
            ref = {name: read(task / "evaluation" / name) for name in (
                "reference_key_points.json", "reference_conclusions.json", "scoring_rules.json",
                "critical_failures.json", "evidence_map.json")}
            kp = ref["reference_key_points.json"]["items"]
            conclusions = ref["reference_conclusions.json"]["items"]
            rules = associate_rules(ref)
            linked = {k for c in conclusions for k in c.get("supporting_key_point_ids", [])}
            ruled = {r["rule"]["reference_id"] for r in rules}
            types = Counter(k.get("key_point_type", "unspecified") for k in kp)
            schema = read(task / "agent_input/submission_schema.json")
            runtime = _runtime_contract(task_type=mode, reference=ref, submission=schema)
            validation = validate_task_package(task)
            public = sorted((task / "agent_input").rglob("*"))
            row = {
                "paper_id": task.name, "mode": mode,
                "key_points": len(kp), "process_key_points": types["process"],
                "result_key_points": types["result"],
                "other_key_points": len(kp) - types["process"] - types["result"],
                "conclusions": len(conclusions),
                "final_role_conclusions": sum(c.get("claim_role") == "final" for c in conclusions),
                "conclusion_max_scores": "/".join(str(c["max_score"]) for c in runtime["scientific_conclusion_rubric"]),
                "rules": len(rules), "numeric_rules": sum(r["rule"]["type"] == "numeric" for r in rules),
                "unlinked_key_points": ";".join(k["key_point_id"] for k in kp if k["key_point_id"] not in linked),
                "key_points_without_direct_rule": ";".join(k["key_point_id"] for k in kp if k["key_point_id"] not in ruled),
                "standalone_rules": ";".join(r["rule_id"] for r in rules if not r["conclusion_ids"]),
                "contract_status": validation.status,
                "reference_present": (task / "evaluation/verified_computation_reference.md").is_file(),
                "public_files": sum(p.is_file() for p in public),
                "public_symlinks": ";".join(str(p.relative_to(task)) for p in public if p.is_symlink()),
            }
            rows.append(row)
            details.append({**row, "task_path": str(task.relative_to(ROOT)),
                "key_point_types": dict(types), "key_point_items": kp,
                "conclusion_items": conclusions, "rule_associations": rules,
                "contract_findings": [str(f) for f in validation.findings],
                "public_paths": [str(p.relative_to(task)) for p in public if p.is_file()]})
    return rows, details


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-prefix", type=Path)
    args = parser.parse_args()
    rows, details = inventory()
    summary = {
        "papers": len({r["paper_id"] for r in rows}), "packages": len(rows),
        "by_mode": dict(Counter(r["mode"] for r in rows)),
        "key_points_total": sum(r["key_points"] for r in rows),
        "conclusions_total": sum(r["conclusions"] for r in rows),
        "conclusion_distribution": dict(sorted(Counter(r["conclusions"] for r in rows).items())),
        "key_point_distribution": dict(sorted(Counter(r["key_points"] for r in rows).items())),
        "contract_status": dict(Counter(r["contract_status"] for r in rows)),
        "unlinked_packages": [r for r in rows if r["unlinked_key_points"] or r["standalone_rules"]],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.output_prefix:
        prefix = args.output_prefix
        prefix.parent.mkdir(parents=True, exist_ok=True)
        with prefix.with_suffix(".csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        prefix.with_suffix(".json").write_text(json.dumps({"summary": summary, "tasks": details}, ensure_ascii=False, indent=2) + "\n")
        lines = ["# 当前 final 逐任务评分项目统计", "", "日期：2026-09-18。机器读取当前文件和运行时适配器；不代表逐篇科学认证。", "",
            "关键点包括 process、result 及其他类型，并不全部是中间数值结果；结论数是实际科学轴 rubric 项数。过程轴另外有 7 项、合计 100 分。",
            "", "结论数包括全部实际计分条目；final 标签列单列严格的 `claim_role=final` 数量。PR 的 paper_08c040bf4e456891 还有一条 interpretation，同样占科学轴 50 分。", "",
            "| 论文 | 模式 | 关键点总数 | process | result | 其他 | 计分结论数 | final 标签 | 各结论满分 | 规则数 / numeric |", "|---|---|---:|---:|---:|---:|---:|---:|---|---|"]
        for r in sorted(rows, key=lambda r: (r["paper_id"], r["mode"])):
            lines.append(f"| {r['paper_id']} | {'AR' if r['mode']=='autonomous_research' else 'PR'} | {r['key_points']} | {r['process_key_points']} | {r['result_key_points']} | {r['other_key_points']} | {r['conclusions']} | {r['final_role_conclusions']} | {r['conclusion_max_scores']} | {r['rules']} / {r['numeric_rules']} |")
        prefix.with_suffix(".md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
