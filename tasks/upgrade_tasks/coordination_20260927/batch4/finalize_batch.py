"""Aggregate checked batch4 artifacts and seal a reviewable development handoff.

This script only writes inside its own coordination directory. It never mutates
packages, final sources, scientific references, or other batches.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
B = Path(__file__).resolve().parent
ROOT = B.parents[3]
sys.path.insert(0, str(ROOT))
from evaluation.contracts.task_package import (
    package_content_hash, package_payload_entries, validate_task_package,
)

MODES = ("autonomous_research", "paper_reproduction")
SUPERVISOR = "01a0e2da-982a-7b32-bcc1-744840298ce5"
DETAILS = {
    "paper_3235db287859287e": (
        "旧 E/Z 自由能仅能作为同约定端点核对，不能验证氧转移或动力学。",
        "先独立构建一个底物氧自由基序列和一个外源水氧/离子竞争序列，核对碘、质子、电子库存；再补 OH 保护干预和两套同位素映射，取完整多段路径的有效最大能垒。",
        "拒绝只交 E/Z 标量与同位素文字；原子守恒且满足观测约束的替代路线可以反驳作者。新路径和方法敏感性尚未计算。",
    ),
    "paper_4e9774f4128551d3": (
        "旧 S20/50 产品自由能只能用于端点热力学，不能替代双面质子化势垒或外消旋酸加权。",
        "从映射烯醇-TMS、一个 CSA 对映体和一分子 MeOH 开始，验证两面进攻与共同零点预组织代价，再完成第二酸对映体或严格对称映射、外消旋加权和溶剂对照。",
        "拒绝以产品稳定性作面选择性、无依据省去反离子或酸对映体；完成全部路径后接近零的加权差异可接受。源混合比例冲突已公开。",
    ),
    "paper_60f4c45810428116": (
        "旧还原电势只约束还原热力学；SI 实测网格及其删失分类可用。RBF 曲面不能提供独立机理速率。",
        "解除阻塞需独立生成/回淬/重排/捕获速率区间或经过验证的势垒，以及回淬终态的电荷/电子账本。随后才校验 ODE 守恒、混合稀释、三个完整条件留出和共享温度参数的可辨识性。",
        "当前 blocked。已补真实观测，但没有臆造速率区间、检测下限或回淬物种。拒绝每个格点独立拟合、留出泄漏及把 trace/n.d./堵塞视为测得零；解除输入阻塞后证据充分的秩亏结论允许。",
    ),
    "paper_db6c4e0558113873": (
        "旧 298.15 K 的 syn/anti Cu 中间体差仅为端点/低频诊断，不是 40°C 下消除或直接氯转移的参考势垒。",
        "先核对完整 allyl/acac 与 Cu 电子数，计算连接端点的一条 Cu C–Cl 出口和一条 PhSO2Cl→自由基氯转移；再补第二立体出口、自旋和构象敏感性。",
        "拒绝裸 CuCl、省 acac 或跨库存比较绝对总能；直接转移胜出或两者不可区分均可。新结合自由能与自旋参考仍缺。",
    ),
    "paper_e2d9397dff2a3f0f": (
        "旧约 110i 模态和 13.8434 kcal/mol 数值没有 IRC，且 N–O 位移很小，仅作为需复核的诊断。",
        "先用真实模态和双向端点验证 bda 的 N10–O5 裂解，再做单一 bcs 图干预；逐配体完成开环、开环后 NH3 进攻与直接进攻，共六个段，统一到初始配合物+NH3 及相同 N–N 终点。",
        "拒绝用氧化自由能作化学势垒、横向虚频作裂解，或将开环一步与完整进攻比较。bcs 闭合盆地实证消失时允许坍缩，不编造极小点或独立势垒。",
    ),
    "paper_fcc3c7f2c46a0fbe": (
        "旧 4b 几何/XRD 比较提示名称、SMILES 与构象限制，不验证抗氧化反应循环。",
        "校验 E 构型和真实供氢位点，先闭合 4c/4h 的同质子/电子基准热化学循环并做显式 DPPH HAT，再扩至 4b/4i，检查循环闭合、位点替代和 EtOH 敏感性。",
        "拒绝把 OMe 当酚、把 DMSO 当活性测定溶剂、把不溶当无活性或由轨道隙推精确 IC50；多个机制均可行可以成为完成结论，不能外推绝对活性。",
    ),
    "paper_0e835b370ddd37b6": (
        "既有 1/V′ H2 路径和分离物参考可在同对象、同协议下复用；缺少 4 和匹配进度分解。",
        "先核对中性二配位 Si 的 4 图与 H2 路径，再为三体系在 H–H=0.80/1.00/1.20/1.40 Å 四点计算冻结片段能；用真实计算确定闭合残差与方法敏感性。",
        "拒绝省略 4、错位进度比较或给冻结片段加热修正。形变和相互作用共同控制的解释可接受；新增对照仍待计算。",
    ),
    "paper_9132719dbf91c978": (
        "既有 INT-G/TS6、双向端点、释放扫描及分离 Pd/H2 文件可逐条审计复用；DMAc 再配位和混合标准态对照仍是新缺口。",
        "先核验一条旧 H–H 路径和束缚/分离 H2 身份，再优化 Pd(XantPhos)(DMAc)，构建 H2 气体 1 atm/溶质 1 M 与全 1 M 两套账本及压力敏感性。",
        "拒绝把 η2-H2 改名自由气体、删 XantPhos 或混搭标准态。H–H 成键易而释放/再配位不利是有效结果；局部模型不能证明整体周转。",
    ),
    "paper_534ae3b6e2fb695f": (
        "旧三二胺 HOMO/TCE 指标仅为描述符基线；原包的 TMC 是背景对象，没有酰化势垒。",
        "先跑 ODA+TMC 映射 C1002/Cl1003 的完整首酰化及单酰胺+HCl 终点，再原样扩到 6FODA/PFMB；保留必要加成、消除、质子转移段并取最大值，做匹配 N–C 进度分解。",
        "拒绝仅交 HOMO 指数、丢 HCl 或跨胺比较不同反应段。允许势垒排序反驳亲核性指数；局部气相 1 M 控制不证明膜界面动力学或性能。",
    ),
    "paper_6f9a36fff6964313": (
        "旧孤立离子对 Mulliken 电荷只能作为分区相关描述符，不能证明协同催化。",
        "核对两催化剂的完整 OTf/KI/环氧化物/水/CO2 库存，先各完成一条末端开环，再补苄位出口和受限催化剂定位对照，计入组织代价。",
        "只冻结 CO2 环加成中的一步；拒绝省离子库存或跨催化阶段比较。修正后没有保留双功能优势也可完成；真实水混合物/压力与有限模型分列。",
    ),
    "paper_c625cba3ce868eb1": (
        "旧水相反应物电荷/偶极不含试剂、过渡态或产物，不能认证 DCM 中的区域选择性。",
        "核对 NBS 溴化和质子转移后，从可比溴化前体完成六元与七元闭环；计入面选择、构象准备以及 succinimide/Et3N 质子账本。",
        "以实际图和源非酶对照纠正方案的五/六元表述；拒绝虚构五元路径、把 row22 氢当氧或把 Br− 当亲电体。完整比较后构象主导或不可区分均可；不声称酶内 QM/MM。",
    ),
    "paper_d3b4575397179146": (
        "旧四催化剂 TDA/NTO 光谱可以帮助态特征诊断，不含底物自由基阳离子、催化剂阴离子或氧再生热化学。",
        "先用 dF/dOMe 核验中性/阴离子、真实底物阳离子、弛豫三重态与 E00，并用合适方法校准三重氧/单重氧/超氧；再完成四催化剂同基准 SET、EnT 和再生循环。",
        "schema 固定三种氧态电荷/多重度，但物理态正确性还须原始波函数审查。拒绝 E00=垂直 S1、换电极基准或由热力学可行性断言唯一机制、寿命/产率；双机制必要条件均满足允许。",
    ),
    "paper_ef26687d63a37e29": (
        "旧引发剂加合物 ADCH/ESP/接触分析可审身份，不能改名为碳酸酯增长链或替代传播/回咬势垒。",
        "验证 PA 短链及两 Et3B，完成 CO2 插入→PO 开环全序列和保留缩短链共产品的回咬；再做无 PA 匹配模型，用同一组势垒推十倍活度变化。",
        "拒绝省共产品/第二 Et3B 或只挑易传播段；PA 优势减弱、消失或被复合干预混杂均可如实解释。短链结构变化不能归因于纯静电，也不能证明体相聚合性能。",
    ),
    "paper_0dc85595cab7bc0a": (
        "旧 xTB 候选枚举和图检查只作搜索诊断；4.30 Å 与 ±15 kJ/mol 剪枝未经校准，不能冻结成新标准。",
        "重新纳入旧距离边界附近的图异构闭环和构象，两阶段均作 DFT 精化；每阶段至少一个关键闭环提供映射 S0 路径及物理激发态追踪，并维护氢/氧化层守恒。",
        "拒绝跨氢数比较总能、只用旧截止剪枝或将最低 S0 终点指定唯一光产物。真实排除/坍缩可省不存在的能量但须搜索证据；多个候选保留允许，全动力学仍可选。",
    ),
    "paper_a3892396b1843698": (
        "旧 GFN2-xTB/RRHO 两路径与势垒可作准备和调试，不能替代 DFT 校准或轨迹分支。",
        "先 DFT 精化非约束 [3,3]/[5,5] 与端点映射，再施加定义的反号二面角干预，记录电子准备代价，解除约束后搜索两通道。",
        "拒绝把约束几何叫自由极小点、忽略准备能或由驻点断言精确分支；两个独立控制回到同盆地时提交完整坍缩证据，无须虚构两个自由能值。",
    ),
    "paper_8fefc96b015c4577": (
        "旧短链 DMSO 的 B 零点势垒和 C–C 模态记录可复核，但没有全 IRC，不能填补长链、DCE 或新增端点。",
        "先核对 56 原子同系物与 radical map10，验证关键长链双路径的真实模态和双向端点，再完成两链长/两溶剂交叉，量化长链低频、构象、方法差异与匹配进度形变。",
        "拒绝复制短链行号、混用能量零点或省交叉格；证据支持的长链近简并可以完成，不强制反转。实验添加剂也变，受控溶剂结论需限定。",
    ),
}


def load(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_json(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def rel_link(label, target):
    return f"[{label}]({Path(os.path.relpath(target, B)).as_posix()})"


def main():
    manifest = load(B / "manifest.json")
    ids = load(B / "assignment.json")["batch"]["papers"]
    assert manifest["scope"] == ids and set(DETAILS) == set(ids)
    notes = load(B / "review_notes.json")
    shards = [load(B / f"validation_shard_{i}.json") for i in range(1, 5)]
    assert all(s["status"] == "passed" and s["repository_mode"] == "full_roots" for s in shards)
    assert [p for s in shards for p in s["paper_ids"]] == ids
    merged, hashes = {}, {}
    for s in shards:
        assert s["checks"] == len(s["results"])
        assert s["scientific_calculations_run"] == 0 and s["LLM_judge_run"] is False
        for result in s["results"]:
            assert result["passed"] is True
            if result["test"] in merged:
                assert merged[result["test"]] == result, result["test"]
            merged[result["test"]] = result
        for key, value in s["package_hashes"].items():
            assert key not in hashes
            hashes[key] = value
    assert len(hashes) == 32
    source_files, snapshots, package_details = {}, 0, {}
    for row in manifest["papers"]:
        pid = row["paper_id"]
        assert pid in ids
        summaries = []
        for mode in MODES:
            key = f"{mode}/{pid}"
            package = ROOT / "tasks/upgrade_tasks" / key
            value = validate_task_package(package)
            assert value.status == "passed", (key, value.findings)
            current = {
                "package_content_sha256": package_content_hash(package_payload_entries(package)),
                "package_manifest_sha256": sha(package / "package_manifest.json"),
            }
            assert current == hashes[key], (key, "changed after shard validation")
            audit = load(package / "evaluation/task_provenance/upgrade_audit.json")
            assert audit["new_scientific_calculations_performed"] is False
            assert audit["status"] == row["status"]
            for original, snap in audit["source_payload_snapshots"].items():
                origin = ROOT / audit["source"] / original
                assert sha(origin) == sha(package / snap["snapshot"]) == snap["sha256"]
                source_files[origin.relative_to(ROOT).as_posix()] = snap["sha256"]
                snapshots += 1
            for item in audit["source_docs"] + audit["source_pdf_review"]:
                assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
                source_files[item["path"]] = item["sha256"]
            rubric = load(package / "evaluation/scoring_rules.json")["scientific_rubric"]
            assert sum(x["max_score"] for x in rubric) == 100
            summaries.append({
                "mode": mode, "path": package.relative_to(ROOT).as_posix(),
                **current, "official_validate_task_package": "passed",
                "runtime_adapter": "split-computational-evaluator.v3-flat",
                "weight_sum": 100, "source_snapshots_verified": len(audit["source_payload_snapshots"]),
                "private_materialization_leak": False,
            })
        per_tests = [x for x in merged.values() if x["test"].startswith(pid + ":")]
        row["checks"] = {
            "status": "passed", "unique_named_checks": len(per_tests),
            "packages": summaries, "contract_examples_are_synthetic": True,
            "scientific_evaluator_calibration_run": False,
        }
        row["package_ready_for_supervisor_review"] = True
        row["scientific_pass_claimed"] = False
        package_details[pid] = summaries
    moment = datetime.now(timezone.utc).isoformat()
    counts = Counter(x["new_class"] for x in manifest["papers"])
    statuses = Counter(x["status"] for x in manifest["papers"])
    assert dict(counts) == {"C": 7, "B": 9}
    assert statuses["blocked"] == 1 and statuses["implemented_pending_expanded_reference"] == 15
    validation = {
        "date": "2026-09-27", "checked_at_utc": moment, "batch": 4,
        "status": "passed", "paper_ids": ids, "paper_count": 16, "package_count": 32,
        "checks": len(merged), "unique_named_checks": len(merged),
        "executed_shard_checks": sum(s["checks"] for s in shards),
        "duplicate_named_checks": sum(s["checks"] for s in shards) - len(merged),
        "shards": [{"path": f"validation_shard_{i}.json", "sha256": sha(B / f"validation_shard_{i}.json"), "checks": s["checks"], "status": s["status"]} for i, s in enumerate(shards, 1)],
        "repository_mode": "TaskRepository(roots=[Path('tasks/upgrade_tasks')])",
        "scientific_calculations_run": 0, "LLM_judge_run": False,
        "boundary": shards[0]["boundary"],
        "post_regression_package_hashes_rechecked": True,
        "source_snapshot_pairs_verified": snapshots,
        "package_hashes": hashes,
        "per_paper": {p["paper_id"]: {"development_status": p["status"], "unique_named_checks": p["checks"]["unique_named_checks"], "package_count": 2, "checks_passed": True, "scientific_pass_claimed": False} for p in manifest["papers"]},
        "results": list(merged.values()),
    }
    write_json("validation_report.json", validation)
    write_json("source_integrity.json", {
        "checked_at_utc": moment, "status": "passed", "files": source_files,
        "source_file_count": len(source_files), "snapshot_pairs_verified": snapshots,
        "scope": "Exact final-source files, source PDFs and guidance documents recorded in the 32 audits; no claim about unrelated repository changes.",
    })
    manifest.update({
        "development_delivery_status": "implemented_and_contract_checked_handed_off",
        "finalized_at_utc": moment, "paper_count": 16, "package_count": 32,
        "class_counts": dict(counts), "scientific_status_counts": dict(statuses),
        "checks_summary": {"status": "passed", "unique_named_checks": len(merged), "executed_shard_checks": validation["executed_shard_checks"], "report": "validation_report.json", "source_integrity_report": "source_integrity.json", "scientific_evaluator_calibration_run": False},
        "implementation_changes_stopped": True,
    })
    write_json("manifest.json", manifest)

    report = [
        "# 第 4 批：局部竞争路径与动力学——开发升级交付报告", "",
        f"交付日期：2026-09-27；封存核对时间：{moment}。", "",
        "本批 16 篇、32 个 AR/PR 开发包已完成实质升级并通过官方包、运行时、公开导出和提交契约检查。升级后为 9 篇 B、7 篇 C；15 篇状态为 `implemented_pending_expanded_reference`，1 篇动力学任务 `paper_60f4c45810428116` 保持 `blocked`。这些状态是开发交付状态，不表示扩展科学目标已经验证通过。", "",
        "本轮新科学计算为 0，量化引擎启动为 0，未运行付费 LLM 科学裁判校准。已完成源 PDF/SI 实质段落及选定图表核对、已有结果复核、分子图/化学计量检查、公开观测转录及软件契约测试。合成提交只在临时目录用于格式回归，均标记为非科学数据。", "",
        "## 实施与评估契约", "",
        "每篇 AR/PR 从相应现行 final 包复制；旧文件逐字节保存为私有 `evaluation/legacy_final_snapshot/*.snapshot`，来源、文件哈希、源指导文档和所读 PDF 页码写入 `upgrade_audit.json`。旧 PASS 与旧狭窄标量未作为新版本完成声明。", "",
        "AR/PR 的科学目标、可用对象、公开数据、submission_schema/guide 和五份科学 evaluator 保持一致；task.md 仅 PR 多出作者假设、源路线/方法与本次新增干预的区别。AR 移除会泄露待判终态的作者产品/中间体答案坐标，保留足够的映射连接与独立构建输入。", "",
        "所有任务要求 `report/results.json` 和 `report/report.md`；新增研究矩阵包含具体行/列、数值、能量零点、电子/热校正/Gibbs 分项、路径模式/双向端点与原始产物路径。评分共 100 分：身份/基准 10，逐篇三个科学面板 30/25/15，稳健性 10，结论 10。五份 evaluator 的规则直接绑定对应结果字段与原始证据。", "",
        "支持、反驳及证据充分的不可区分结果等价对待。实证坍缩/无独立极小点有专门分支，不强制虚构不存在的能垒。核心对照缺失、错误对象/态/零点、仅旧标量、失败冒充完成会失去相关完成信用。顶部 optional 内容未升级为核心失败条件。新增参考和误差界限须由真实新计算校准，没有机械沿用旧 ± 范围。", "",
        "已修复监督指出的两个共性问题：路径拒绝 `..` 越界并允许合法 `./`；前置输入或环境阻塞允许 `calculation_records=[]`、空实际方法与零科学资源的 `pre_engine` 诊断提交，同时要求诊断文件、原因和缺失端点。该失败分支不能携带声称完成的矩阵/科学支持结论；完整分支仍要求真实计算记录和全部核心面板。", "",
        "## 检查范围及其限制", "",
        f"四个检查分片共执行 {validation['executed_shard_checks']} 个命名断言，去重后 {len(merged)} 个，全部通过。重复项来自全批化学图检查和仓库加载；去重规则按测试名且要求结果完全一致。32 个测试时包哈希在汇总时再次与官方 `package_payload_entries`/`package_content_hash` 计算值一致。", "",
        "检查使用 `.envs/researchchembench/bin/python` 和 `TaskRepository(roots=[Path('tasks/upgrade_tasks')])`，没有改变默认正式库发现机制。覆盖 JSON/JSON Schema、validate_task_package、load_runtime_evaluation、权重 100、materialize 精确公开清单且不导出 evaluator/快照、AR/PR 同科学与公开数据、源快照、完整/反驳/不可区分/坍缩/诚实失败正例及逐篇缺面板、缺端点、错误显式态、旧标量、路径越界等反例。", "",
        "这些是包和提交传输/结构检查，不会因合成样例被 schema 接受就授予科学 PASS。数值范围内但物理错误的自旋、伪造日志、错误能量参考等仍须科学 evaluator 检查原始输出；本轮没有把语义规则校准伪装成执行过的数值验证。", "",
        f"来源完整性另核对 {snapshots} 对 source/snapshot 和 {len(source_files)} 个去重来源文件；范围限定为各包审计列出的 final、源 PDF 与指导文档，详见 [source_integrity.json](source_integrity.json)。", "",
        "复跑入口为 `check_batch.py --shard 1` 至 `--shard 4`，再执行 `finalize_batch.py`。仅在本批仍由当前实施负责人持有写权时重新生成；移交后如监督已改包，旧测试哈希不匹配会使汇总失败，必须对新版本重新检查。", "",
        "## 逐篇交付", "",
    ]
    for i, row in enumerate(manifest["papers"], 1):
        pid = row["paper_id"]
        package = ROOT / row["packages"][0]
        rubric = load(package / "evaluation/scoring_rules.json")["scientific_rubric"]
        reuse, pilot, limits = DETAILS[pid]
        report += [f"### {i}. {pid}", "", f"**范围与状态：** {notes[pid]['upgrade_zh']} 状态 `{row['status']}`。", "", f"**正文/SI 实质依据：** {notes[pid]['source_zh']}", ""]
        for source in row["source_pages_reviewed"]:
            label = Path(source["path"]).name
            pages = "、".join(map(str, source["pdf_pages_1_based"]))
            report.append(f"- {rel_link(label, ROOT / source['path'])}：PDF 物理页 {pages}；源 SHA256 见该包审计。")
        report += ["", f"**评估改动：** 三个科学面板分别为 " + "；".join(f"`$.results.{x['id']}`（{x['max_score']} 分）" for x in rubric if x["id"] not in {"identity", "robustness", "conclusion"}) + "。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。", "", f"**旧参考可复用边界：** {reuse}", "", f"**可实施先导和未完成参考：** {pilot}", "", f"**拒绝项、公平替代结论及限制：** {limits}", "", f"**检查：** {row['checks']['unique_named_checks']} 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。", "", "**文件入口：** " + "；".join([rel_link("AR task", ROOT / row["packages"][0] / "agent_input/task.md"), rel_link("PR task", ROOT / row["packages"][1] / "agent_input/task.md"), rel_link("提交 schema", package / "agent_input/submission_schema.json"), rel_link("扩展参考计划", package / "evaluation/reference_validation_plan.md"), rel_link("审计", package / "evaluation/task_provenance/upgrade_audit.json")]) + "。", ""]
    report += [
        "## 阻塞、软件范围和移交", "",
        "唯一输入阻塞为 `paper_60f4c45810428116`：SI Table S2 的 25 个网格位置已提供，其中 23 个非堵塞位置保留原观测/删失分类；还缺独立速率区间与回淬 sink 身份/电荷电子守恒。已有电势与 RBF 插值均不能填补缺口。包的网络、可辨识性、留出字段和失败诊断已实现，解除条件写在两模式参考计划和 manifest，不能因有观测网格就宣称科学就绪。", "",
        "其余 15 篇输入与有限对照已经可审查，新增参考仍须按各计划计算。方法范围以已查 `chemistry_toolbox` README/config/native guides 为准：Gaussian/ORCA 用于相应分子 DFT、频率、TD/redox；路径采用可审计的 IRC/模态跟随，xTB/CREST 只作初筛准备；Python/SciPy 负责账本与 ODE。软件可调用不代表具体方法已校准。NBO/PyFrag 依可用性作为可选诊断，未引入无依据 NEGF、体相模型或新付费服务。", "",
        "已完成本批开发写入，32 个包按 [HANDOFF.json](HANDOFF.json) 的 content/manifest 双哈希移交监督。`stopped_writing_paper_ids` 包含全部 16 篇及优先请求的 a389、913、60f；本实施进程不再修改这些包。监督会话 `" + SUPERVISOR + "` 可据此独立复核和冻结可计算快照。`package_ready_for_supervisor_review` 只表示开发包可审查，不表示科学验证通过；后续科学预算或运行由监督另行管理。", "",
        "交付清单：[manifest.json](manifest.json)、[validation_report.json](validation_report.json)、[STATUS.md](STATUS.md)、[HANDOFF.md](HANDOFF.md)、[HANDOFF.json](HANDOFF.json)。", "",
    ]
    (B / "REPORT.md").write_text("\n".join(report))
    status = ["# 第 4 批升级状态", "", f"更新：{moment}。16 篇/32 包开发升级与契约检查已完成并移交；本轮科学计算及引擎启动均为 0。", "", f"检查通过：{len(merged)} 个去重命名断言（四分片共 {validation['executed_shard_checks']} 次）；32 个包双哈希已回读核对。", "", "| 论文 | 类别 | 科学状态 | 开发/检查/移交 |", "|---|---|---|---|"]
    for row in manifest["papers"]:
        status.append(f"| {row['paper_id']} | {row['old_class']}→{row['new_class']} | {row['status']} | 两模式完成；检查通过；已停止修改 |")
    status += ["", "阻塞：60f 的独立速率区间及回淬终态/电子账本待补，实测网格已提供。其余 15 篇待扩展科学参考；本轮没有新科学 PASS。", "", "[逐篇报告](REPORT.md) · [包清单](manifest.json) · [检查报告](validation_report.json) · [移交](HANDOFF.json)", ""]
    (B / "STATUS.md").write_text("\n".join(status))
    handoff_papers = [{
        "paper_id": p["paper_id"], "development_status": p["status"],
        "old_class": p["old_class"], "new_class": p["new_class"],
        "packages": package_details[p["paper_id"]],
        "unresolved_reference_gaps": p["new_reference_gaps"],
        "input_blockers": p["blockers"],
        "implementation_changes_stopped": True,
        "package_ready_for_supervisor_review": True,
        "scientific_ready": False, "scientific_pass_claimed": False,
        "scientific_calculations_performed_in_development": False,
        "contract_check_path": "validation_report.json",
    } for p in manifest["papers"]]
    handoff = {
        "batch": 4, "handed_off_at_utc": moment,
        "implementation_owner": "batch4.build_batch",
        "recipient_supervisor_session": SUPERVISOR,
        "state": "development_writes_stopped_ready_for_independent_supervisor_review",
        "stopped_writing_paper_ids": ids,
        "priority_paper_ids": ["paper_a3892396b1843698", "paper_9132719dbf91c978", "paper_60f4c45810428116"],
        "package_ready_does_not_mean_scientific_pass": True,
        "contract_check_paths": ["validation_report.json"] + [f"validation_shard_{i}.json" for i in range(1, 5)],
        "validation_report_sha256": sha(B / "validation_report.json"),
        "manifest_sha256": sha(B / "manifest.json"),
        "source_integrity_sha256": sha(B / "source_integrity.json"),
        "REPORT_sha256": sha(B / "REPORT.md"),
        "papers": handoff_papers,
    }
    write_json("HANDOFF.json", handoff)
    (B / "HANDOFF.md").write_text(
        "# 第 4 批开发移交\n\n"
        f"时间：{moment}；接管监督：`{SUPERVISOR}`。\n\n"
        "16 篇、32 个开发包已停止写入，全部可进入主进程独立复核。包含优先三篇 `paper_a3892396b1843698`、`paper_9132719dbf91c978`、`paper_60f4c45810428116`。\n\n"
        "准确包路径、content SHA256、manifest SHA256、逐篇参考缺口和输入阻塞见 [HANDOFF.json](HANDOFF.json)。哈希对应四分片验证过且汇总再次官方核对的字节版本。\n\n"
        "15 篇 `implemented_pending_expanded_reference`，60f 为 `blocked`（独立速率与回淬身份/电子守恒待补）；开发就绪不是科学通过。新计算 0，科学裁判校准未执行。\n\n"
        "监督可开始独立验证/冻结；当前实施负责人不再修改这些包。需要后续修复时，应由接管方明确新的版本/所有权，避免覆盖已冻结包。\n\n"
        "[中文逐篇报告](REPORT.md) · [验证报告](validation_report.json) · [来源完整性](source_integrity.json)\n"
    )
    for name in ("REPORT.md", "STATUS.md", "HANDOFF.md"):
        for link in re.findall(r"\]\(([^)]+)\)", (B / name).read_text()):
            assert (B / link.split("#")[0]).exists(), (name, link)
    # Read written JSON back; preserve package hashes as the final handoff boundary.
    for name in ("validation_report.json", "source_integrity.json", "manifest.json", "HANDOFF.json"):
        load(B / name)
    for key, checked in hashes.items():
        package = ROOT / "tasks/upgrade_tasks" / key
        assert package_content_hash(package_payload_entries(package)) == checked["package_content_sha256"]
        assert sha(package / "package_manifest.json") == checked["package_manifest_sha256"]
    print(json.dumps({"status": "passed", "papers": 16, "packages": 32, "unique_checks": len(merged), "executed_shard_checks": validation["executed_shard_checks"], "source_snapshot_pairs_verified": snapshots, "source_files_verified": len(source_files), "scientific_calculations": 0, "handoff": str(B / "HANDOFF.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
