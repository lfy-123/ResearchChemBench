"""Seal batch5 development handoff; verify package bytes without mutating packages."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
sys.path.insert(0, str(ROOT))
from evaluation.contracts.task_package import package_content_hash, package_payload_entries

MODES = ("autonomous_research", "paper_reproduction")
IDS = json.loads((B / "assignment.json").read_text())["batch"]["papers"]

DETAILS = {
    "paper_0cd74ae20ab933f3": {
        "title": "Cu₂ 交换：轴向取代、几何与自旋模型",
        "science": "保留完整四桥 paddlewheel，建立 H/Me/OMe 三系列各自松弛核与公共 Cu₂O₈C₄/轴向 N 核的六格比较。三重态和破缺对称态保留 S²、投影、局域自旋及真实输出；代表 R_H 另作可调用的 CASSCF 或自旋翻转校准。以 J=E_S−E_T、H=−J S₁·S₂ 和三重态简并度 3 统一定义，分离取代的电子效应和几何效应。",
        "sources": "正文 PDF 第 6–7 页 Figure 5、式 1–2；SI 第 5–6 页计算方法、第 35–36 页 Table S4 的 SF-TDA/SF-TDDFT/CASSCF 比较。原运行 J 与文献锚点的差异保留在私有快照，不作为新版正确值。",
        "evaluator": "重点检查六格对象一致性、投影和符号/因子、同几何高层校准及差值的不确定性。只交旧 J 或布居标量、忽略自旋污染、强排小于误差的排序均不能完成。",
        "feasibility": "可走 ORCA BS-DFT/CASSCF 或已确认可调用的自旋翻转路线；先验证一个 R_H 的 BS/三重态和参考态。专用 PySCF-forge 实现不假定存在。",
        "limits": "公共核、三系列新增输出与高层不确定性未计算；孤立分子的交换不能证明材料热致变色。",
    },
    "paper_2c439196c2f349c9": {
        "title": "INP：瞬时电子响应、热记忆与混合模型",
        "science": "把原孤立分子能隙任务改为同一组实际时间/功率观测上的三模型比较，要求跨浓度共享参数、保留条件预测、残差和参数剖面。加入 Figure 10 的 27 个真实离散测点及像素坐标、标尺和 ±4 像素读取包络；该包络是数字化误差，不冒充实验标准差。未把作者拟合线或时间常数当成独立观测。",
        "sources": "正文第 3、9–11 页，Figures 6/9/10；SI 第 6–7 页 S7/S8；正文第 11 页的数据可按请求取得说明。已核对 532 nm、三浓度、1 mm 光程、时间曲线 50 mW 以及 Z-scan 的光束条件；不能将 Z-scan 束腰自动当 SSPM 已校准束腰。数字化源图和审计在 source_review/INP_fig10_digitization_audit.json。",
        "evaluator": "同观测和统一误差模型、参数共享、保留条件预测及可识别性成为主评分项。禁止三套互不约束拟合、由 HOMO/LUMO 推热机制、没有参数区间就宣布唯一机制占比。",
        "feasibility": "Python/SciPy 即可开展后续数据审计和模型拟合；没有必需的量化引擎运行。当前可提交零启动的 bounded_failure。",
        "limits": "明确 blocked：其余独立功率/强度与 Z-scan 测点、可信误差、SSPM 光束/仪器响应和热参数界限仍不完整。27 个时间测点不足以解除辨识输入门槛；须补齐数据来源和校准，再建立拟合参考与噪声容差。未联系作者，未拟合新参考。",
    },
    "paper_3316e45a74258fb7": {
        "title": "TADF：三种供体布局与匹配扭转干预",
        "science": "给出 TD_2T、CD_2T、TD_2C 的完整映射图和 C72H49N7/C72H47N7/C72H45N7 身份。三布局各含松弛与指定 45° 扭转控制，明确原子四元组；比较对应 S/T 态、f、NTO、SOC，垂直与绝热指标分列，并保留独立构象尝试。",
        "sources": "正文第 2–5 页、Figure 1；新取得的正式出版社 SI Sections I/II、S3–S6、Table S1。系统名经 OPSIN 和 RDKit 核对；SI 的复制名称/中间体标签和基组简写存在问题，连接关系由结构图和 HRMS 交叉确认。",
        "evaluator": "评分转到六格状态对应、布局/几何干预和实际 SOC；拒绝只给 ΔEST 或按 root 编号盲配。明确源基组简写不能未经说明等同另一个基组。",
        "feasibility": "Gaussian/ORCA TD/SOC 与 Multiwfn 可构成路线；先做 TD_2T 两构象、SOC 接口和态窗口先导。",
        "limits": "完整 C72 体系成本与根跟踪需要先导；新增固定扭转、SOC、绝热参考和 CT 方法误差未计算。ΔEST/SOC 不单独证明 RISC 速率或器件 EQE。",
    },
    "paper_3d1d9b7f6df049da": {
        "title": "Y₂ 富勒烯：模式特异的磁张量导数",
        "science": "保留两个笼型的 96 原子 C87H7Y2 中性双重态，明确 Y 的 81/82 行映射。侧向模式候选与纵向/笼振动负对照分别做 ±h、±h/2，提交共同坐标系中的完整 g/A 张量导数、旋转协变核查，以及 20/100 K 的 Bose 占据与 n(n+1) 代理量。",
        "sources": "正文第 3、8–10 页与 Figure 7；SI 第 2 页方法、第 20–26 页 Table S3、Figures S16/S17；同时核查原始公开坐标和电子奇偶。",
        "evaluator": "要求真实模式投影、步长收敛、张量框架和负对照，而非只复述侧向运动解释。坐标轴旋转造成的假导数与不同本征向量错配属于科学错误。",
        "feasibility": "源方法包含 ORCA 的 PBE/def2-TZVP 与 Y ECP 几何、PBE-ZORA EPR；先验证一个双重态、侧向本征向量和稳定张量再扩展。",
        "limits": "新模式矩阵、负对照与导数误差未运行；不要求也不声称从这些静态代理量算出 T1/T2 或定量弛豫寿命。",
    },
    "paper_72822e4ddb5d9b11": {
        "title": "Ni 配合物：闭壳层、三重态和 BS 竞争",
        "science": "保持完整 165 原子 C87H72Cl2N2NiO 中性配合物；B3LYP/BP86 分别尝试 CS、三重态和至少两个独立 BS 起点，提交占据、自旋布居、波函数稳定性及振动证据，分离垂直与绝热能差。显式允许有证据的 BS 坍缩而非虚构第二极小点。",
        "sources": "正文第 4 页；SI 第 10–11 页电子态讨论和第一配位层 def2-TZVP/其余 def2-SVP 方法。核查 165 原子对应 489 个内部振动自由度。",
        "evaluator": "由旧单一绝热标量改为双方法电子态矩阵和固定几何控制。BS 失败不能证明闭壳层正确；只有结构、占据和收敛诊断支持的坍缩才可关闭候选。",
        "feasibility": "Gaussian/ORCA 波函数与频率路线可用；先完成完整模型的 CS/T/两 BS 起点先导和第一配位层映射。",
        "limits": "新 BS、稳定性及双方法配对参考仍缺；频率须与声称极小点的电子面和方法一致。",
    },
    "paper_80441aced6051d86": {
        "title": "CB7/CB8：主体、客体配对和受限几何",
        "science": "补全中性 CB7/CB8 映射图，保持 G1 二价阳离子身份，分别组装 1:1 CB7:G1 与 1:2 CB8:G1。设置完整主体/冻结删主体、四个冻结删伙伴控制和松弛自由单/双客体；用态性质和跃迁密度区分主体响应、客体耦合及几何限制。",
        "sources": "正文第 2–4 页；正式出版社 SI B/C/D、Table S2。由 190/272 原子复合物只提取主体连接关系，验证 CB7 C42H42N28O14、CB8 C48H48N32O16；新增作者结合坐标没有进入公开输入。",
        "evaluator": "所有模式共享同一 host_matrix/coupling_controls/mechanism_comparison。单客体距离/滑移/扭转须为 null；状态窗口内无适当暗态时，暗态和能差为 null 并有搜索解释。双客体间几何和删伙伴对照仍必需，不能借缺暗态豁免。",
        "feasibility": "Gaussian/ORCA 含色散几何与水连续介质 TD 可实施；先验证一个 CB7:G1 放置和同几何删主体对。",
        "limits": "放置、主体删除/伙伴删除的光谱参考和误差尚未计算。删主体包括极化与交换，不能统称纯静电；垂直态不能直接证明发射波长、量子产率或寿命。",
    },
    "paper_94b0a8ae694590ea": {
        "title": "SWCNT 界面：吸附、功函数与电荷转移",
        "science": "保留三个完整 2BF/2BT/2C8Ph 分子；补充明确标为基准定义的 (10,10) 理想管，12 重复单元/480 C、轴向周期和 18 Å 横向真空。用完整吸附体、冻结片段和松弛片段分解 Eint/Edef/Eads，报告共同真空基准的功函数及密度差；24 单元配双吸附体检验固定覆盖度的尺寸影响。",
        "sources": "正文材料方法的 XFS22 管径/长度及分子 DFT 讨论，SI 第 10、15、20 页分子身份。论文未指定单一手性，新增管结构为 ASE 理想起点而非伪称源 CIF。",
        "evaluator": "同覆盖度尺寸、k 点/真空和姿态敏感性绑定输出；禁止仅用孤立 HOMO/LUMO、混淆真空能零或把分子间不同式总能直接比较。",
        "feasibility": "ASE 加已配置 GPAW/QE 等周期路线；先验证清洁管和一个 2BF 位姿，再扩三分子。",
        "limits": "未求新吸附极小点、密度或功函数参考；结果仅适用于明确模型，不推材料功率因子、输运或未支持 NEGF。",
    },
    "paper_988bc12ae3768679": {
        "title": "isoDPP：质子位点/互变异构候选与联合光谱",
        "science": "公开中性 C30H20N6O4 父图及六个必需起点：neutral_parent、neutral_lactim、acid_O、acid_azoN、base_O、base_lactamN。质子增减、原子对应与 lactam→lactim 键级编辑明确；原酸/碱优化答案坐标移入私有快照。以酸/中/碱 NMR 与 UV 联合残差、平衡质子循环及混合物可识别性判别候选。",
        "sources": "正文第 3 页计算方法、第 4–6 页 Table 1/Figure 3；正式 SI Table S2 和光谱/坐标段。核实实验 NMR 酸 6.95、中性 6.80、碱 6.10 ppm；作者计算列 6.95/6.35/7.98 不当作观测。光学用水相条件，NMR 用 DMSO-d6，不能混成同一溶剂。",
        "evaluator": "六个起点均须尝试；保留候选须有匹配溶剂的两类预测，坍缩须有目标/结构证据，失败不能冒充淘汰。中性实验 UV 未提供，允许 null。跨电荷排序必须平衡 H+ 交换，不能比较裸总能。支持、反驳和充分证据的混合/不可区分结论同等评估。",
        "feasibility": "RDKit 已完成图/价态检查；后续 Gaussian/ORCA 溶液优化、TD 和 GIAO 加可审计热化学可实施。先验证酸/碱各两种位点与 NMR/质子参考。",
        "limits": "候选种子不代表有效极小点；所有新增候选能量、塌缩、联合残差和溶液质子循环未计算，不能沿用旧狭窄误差。目标为首版 C 范围，不保证最终可唯一归属。",
    },
    "paper_a21b91f97ce3c68f": {
        "title": "有机锡：几何干预与标量耦合分解",
        "science": "给出 6/7/13 三对完整三正丁基锡模型，分别对应 thp、1,3-dioxan-2 和 1,3-dithian-5；明确 Sn/13C 与相连扭转四元组。对轴/赤道构象计算有符号 119Sn–13C 耦合及 FC/SD/PSO/DSO，并设置固定 Sn–C 距离的 ±30° 扭转和固定扭转的 ±0.03 Å 距离干预。",
        "sources": "正文超共轭讨论；SI 第 2 页方法、Table S3（第 5–6 页）配对定义。源方法明确采用非相对论哈密顿量，TZP-ZORA 是基组名，不能仅凭名字称已作 ZORA。",
        "evaluator": "绑定 signed-J 分量、同定义平均、几何保持条件和轨道分析，不接受只由键长相关性断言超共轭因果。NBO3.1 或有验证的替代局域化可用，不强加新商业服务。",
        "feasibility": "需先在已配置分子软件中验证一完整对、同位素符号和耦合基组/轨道分析，然后扩干预网格。",
        "limits": "新增受限 J 网格与相对论/基组敏感性未跑；跨哈密顿量数值不共享旧容差。",
    },
    "paper_b5c446c7067dd511": {
        "title": "HLCT：高态 SOC、竞争通道与几何控制",
        "science": "将原 AR 名称列表与 PR 源 SMILES 的输入差异消除，四个 Ph/Na/An/Py 完整图和终端/桥映射两模式相同。全系列保留松弛态；Ph/An 代表体系补根数 5→10 的 SOC/NTO 和 45° 扭转控制，比较相邻三重态竞争通道。",
        "sources": "正文第 3–5 页 Figure 3；SI 第 2–6 页低/高态、NTO/IFCT 定义。源 Py 的 CT/LE 百分比对不自洽，必须从实际密度归一化，不能照抄。",
        "evaluator": "从少数能级和作者高态标签转为物理态跟踪、竞争态窗口、SOC 及几何干预。缺代表控制、用 root 标签代替态身份或只复述 HLCT 解释不能通过。",
        "feasibility": "Gaussian/ORCA TD/SOC 与 Multiwfn 路线；先在 Ph/An 证明高态根跟踪与窗口稳定。",
        "limits": "新增高态 SOC、几何控制和方法误差无参考计算；不推出绝对 RISC、器件效率或产率。",
    },
    "paper_c23cfabbd34b087f": {
        "title": "PAH：拓扑、取代、几何与开壳层竞争",
        "science": "公开四个 1M/2M × OMe/TIPS 源模型的图和同拓扑公共骨架映射，比较 CS/BS/T 与独立占据诊断，再做冻结公共骨架的取代干预和代表高层校准。明确源计算 TIPS 模型是 C≡C–SiH3，1M/2M 差 C2H2；2M′ 是氧化对象而非另一构象。",
        "sources": "正文电子/光学讨论；SI 第 42 页起计算方法和四模型坐标段。只保留图身份，不把原闭壳层坐标块来源或状态赢家公开。",
        "evaluator": "检查同式/同能量基准的态差、冻结骨架与松弛效应，并结合多参考诊断解释光谱。禁止跨分子式总能排序、错误 TIPS 全分子或默认 BS 代表真实单重态。",
        "feasibility": "Gaussian/ORCA 稳定性/TD 及必要代表 CASSCF；先验证一个 1M 和一个 2M 状态组与 MCS 映射。",
        "limits": "新增各态极小点、冻结干预和校准参考未运行；所有新图只是输入，非优化证据。",
    },
    "paper_d8e5490cd9942f4f": {
        "title": "La/Tb/Lu：构象、替换和配位水循环",
        "science": "以完整 La 源图建立 La/Tb/Lu × syn/anti × 0/1 水矩阵，加入冻结 La 骨架金属替换和松弛配位水循环。提供正式数值 ECP/基组：La46/Tb54/Lu60 核、各 11 个显式中性原子电子，(7s6p5d)/[5s4p3d]。严格区分伪单重态与真实 Tb 4f 自旋；水脱离允许证据化分支。",
        "sources": "正文第 3/5 页；SI 第 21–22 页 ECP/热化学、水循环与第 33 页参考 13。进一步取得源 University of Cologne MWB 系数并保存来源、内容哈希、核电荷及收缩审计。",
        "evaluator": "以同金属 syn/anti ΔG、固定骨架响应和原子守恒水循环代替跨金属裸总能，明定 298 K/标准态和低频处理。周期赝势安装不能替代该分子 ECP；输入系数核查不冒充引擎或极小点验证。",
        "feasibility": "原数值基组/ECP 缺口已由正式文件解除；下一步为 Gaussian/ORCA 解析、电子数核对、La 极小点/频率及 Tb 单点先导。",
        "limits": "引擎解析、最低点、扩展水合热化学与误差仍未运行，因此保持 pending_reference。无完整交换循环不宣称定量金属萃取选择性。",
    },
    "paper_e0791c047a731974": {
        "title": "敏化剂—rubrene：SOC 与两种独立能量条件",
        "science": "IR780/Cy1/Cy2 的 +1 完整图与独立中性 rubrene C42H28 同时提供，统一 CHCl3 边界。区分垂直敏化剂态、绝热 T1 与独立 rubrene S1/T1；分别计算受体 T1−供体 T1 和 2×rubrene T1−rubrene S1。Cy2 六段明确共轭链扭转控制检验几何影响。",
        "sources": "正文第 4–6 页；SI 第 7–8 页方法、第 24–30 页各态坐标部分。rubrene 命名图独立核验；三敏化剂骨架并非等结构替换，不能把整体差异全归于单个重原子。",
        "evaluator": "重心为真实 SOC/态局域化与供受体两个闭合条件，拒绝用 Cy2 一套能量替代 rubrene，或只由重原子标签断言 ISC。",
        "feasibility": "ORCA SOC/TD、Gaussian 溶液态和 Multiwfn；先验证 Cy2 重元素接口和 rubrene 态身份，再扩全系列。",
        "limits": "新 SOC、rubrene 独立能量和几何/相对论敏感性未算；不推碰撞速率、浓度效应或上转换量子产率。",
    },
    "paper_e31cc7bc7b21b610": {
        "title": "Ir–Ir：真实二核模型、截短与片段干预",
        "science": "补全 Egan C44H52N2O6 与每配体四个 tBu→H 的 egan C28H20N2O6 映射，构建完整/截短二核 C88H104Ir2N4O12 与 C56H40Ir2N4O12 成对任务。规定 N/O 配位、局部螺旋起点和中性双重态片段；用 Eint/Edef/Eassoc、0.2/0.5 Å 分离和 30° 扭转、占据/自旋及密度交叉检验成键。",
        "sources": "正文第 3 页计算、合成分子式及第 7–9 页成键讨论；SI 第 27–30 页实际是 54 原子 Hap4Ir2，不是上述完整/截短 Egan 配对的现成参考。原单核标量及单位问题保留私有，退出当前目标。",
        "evaluator": "必须完整/截短配对、固定片段电荷/自旋/相对论和同定义能量分解；单一键级或旧单核排序不足。C2h 鞍点不冒充极小点，Hap 另模型不充当新参考。",
        "feasibility": "Gaussian/ORCA 相对论与 Multiwfn，强关联诊断后决定高层校准；先验证一完整/截短对和片段态。",
        "limits": "所有新二核最低点与片段分解未计算；仅构建了可审计图、映射和受控实验定义，不暗示 Ir–Ir 已成键。",
    },
    "paper_eda19e7c8edd4b39": {
        "title": "NiAl：空位、表面偏析和新相的闭合循环",
        "science": "由两空位标量扩为 B2 的 2×2×2/3×3×3 缺陷、(100) Ni/Al 终止与 (110) 混合表面，以及 L12 Ni3Al 候选的统一化学势比较。定义体相移除—slab 加入的守恒循环、7/9 层和 15/20 Å 真空敏感性。补 B2/L12 理想起点并明说不是源 CIF。",
        "sources": "正文第 6–8 页 Figure 6/方法；取得正式 Nature Communications SI 41467_2025_67397_MOESM1_ESM.pdf 并核读表面偏析段。仓库 supplementary_001 是同行评审文件，不能替代正式 SI。正式 SI 的析出前基体 Al 偏析在 PR/私有证据中准确保留，AR 不预告赢家。",
        "evaluator": "分别评估体相空位、洁净基体偏析和 Ni3Al 热力学，重算原子数/化学势和能量基准；拒绝由两空位能推出普遍 Ni 偏析、忽略终止面或将静态能量等同析出速率。",
        "feasibility": "GPAW/QE 与 ASE；先验证元素/B2 参考、一个空位和混合 (110) 的守恒循环，再扩终止面/相。",
        "limits": "PAW/基组/k 点/展宽先导和全部新增 slab/相参考未运行；理想晶格不代表已收敛平衡结构。",
    },
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    validation = json.loads((B / "validation_report.json").read_text())
    identities = json.loads((B / "identity_validation_report.json").read_text())
    assert validation["status"] == identities["status"] == "passed"
    assert len(IDS) == len(DETAILS) == 15 and set(IDS) == set(DETAILS)
    checks = []

    def verify(name, valid):
        checks.append({"test": name, "passed": bool(valid)})
        if not valid:
            raise AssertionError(name)

    papers = []
    handoff_rows = []
    for pid in IDS:
        row = json.loads((B / "paper_status" / (pid + ".json")).read_text())
        verify(pid + ":regression_completed", row["checks"]["full_batch_regression"] == "passed")
        row["checks"]["identity_input_audit"] = "passed"
        row["source_review"] = "paper_reviews/" + pid + ".md"
        row["source_packages"] = {}
        row["result_panels"] = []
        package_entries = []
        for mode in MODES:
            path = ROOT / row["packages"][mode]
            manifest = json.loads((path / "package_manifest.json").read_text())
            content_hash = package_content_hash(package_payload_entries(path))
            verify(pid + ":" + mode + ":frozen_official_payload_hash", content_hash == manifest["package_content_sha256"] == row["package_hashes"][mode])
            audit = json.loads((path / "evaluation/task_provenance/upgrade_audit.json").read_text())
            source = ROOT / audit["source"]
            source_files = {str(p.relative_to(source)) for p in source.rglob("*") if p.is_file()}
            verify(pid + ":" + mode + ":complete_source_snapshot_inventory", source_files == set(audit["source_payload_snapshots"]))
            snapshot_files = {str(p.relative_to(path)) for p in (path / "evaluation/legacy_final_snapshot").rglob("*") if p.is_file()}
            verify(pid + ":" + mode + ":exact_snapshot_inventory", snapshot_files == {v["snapshot"] for v in audit["source_payload_snapshots"].values()})
            verify(pid + ":" + mode + ":unchanged_source_package_hash", package_content_hash(package_payload_entries(source)) == audit["source_package_content_sha256"])
            row["source_packages"][mode] = {"path": audit["source"], "package_content_sha256": audit["source_package_content_sha256"]}
            package_entries.append({"mode": mode, "path": row["packages"][mode], "package_content_sha256": content_hash, "manifest_file_sha256": sha(path / "package_manifest.json"), "stop_modifying": True})
            if mode == MODES[0]:
                result_schema = json.loads((path / "agent_input/submission_schema.json").read_text())["result_schema"]
                row["result_panels"] = list(result_schema["properties"]["results"]["properties"])
                row["source_documents"] = audit["source_docs"]
        row["stop_modifying"] = True
        row["development_handoff_at"] = timestamp
        row["scientific_validation_passed"] = False
        row["reference_validation_plan"] = {m: row["packages"][m] + "/evaluation/reference_validation_plan.md" for m in MODES}
        write_json(B / "paper_status" / (pid + ".json"), row)
        papers.append(row)
        handoff_rows.append({"paper_id": pid, "handoff_id": "batch5-20260927-" + pid, "status": row["status"], "package_ready_for_supervisor_review": True, "scientific_validation_passed": False, "stop_modifying": True, "packages": package_entries, "unresolved_issues": row["blockers"] + row["new_reference_gaps"], "reference_validation_plan": row["reference_validation_plan"]})

        d = DETAILS[pid]
        text = f"# {pid} — {d['title']}\n\n状态：`{row['status']}`；类别：{row['old_class']} → {row['new_class']}；AR/PR 均已完成开发实施。\n\n"
        for title, key in [("科学升级", "science"), ("实际核读正文/SI", "sources"), ("评估改动", "evaluator"), ("可行路线和最低先导", "feasibility"), ("限制和新增参考缺口", "limits")]:
            text += f"## {title}\n\n{d[key]}\n\n"
        text += "## 提交和验证入口\n\n命名结果面板：" + "、".join("`" + p + "`" for p in row["result_panels"]) + "。\n\n"
        text += "两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。\n\n"
        for mode in MODES:
            text += f"- {mode}: `{row['packages'][mode]}`；payload SHA256 `{row['package_hashes'][mode]}`\n"
        text += "\n官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。\n"
        (B / "paper_reviews" / (pid + ".md")).write_text(text)

    counts = dict(Counter(p["status"] for p in papers))
    validation_summary = {k: v for k, v in validation.items() if k != "results"}
    identity_summary = {k: v for k, v in identities.items() if k != "results"}
    integrity = {"status": "passed", "checks": len(checks), "scope": "Read-only handoff hash and complete source-snapshot inventory checks.", "results": checks}
    write_json(B / "handoff_integrity_report.json", integrity)
    manifest = {"batch": 5, "date": "2026-09-27", "finalized_at": timestamp, "status": "development_implemented_and_handed_off", "papers_count": 15, "packages_count": 30, "status_counts": counts, "scientific_engine_starts": 0, "new_scientific_calculations_performed": False, "expanded_scientific_validation_passed": False, "stop_modifying": True, "checks": {"official_package_runtime_output_contract": validation_summary, "input_identity": identity_summary, "handoff_integrity": {k: v for k, v in integrity.items() if k != "results"}}, "check_reports": {f: sha(B / f) for f in ["validation_report.json", "identity_validation_report.json", "handoff_integrity_report.json"]}, "papers": papers}
    write_json(B / "manifest.json", manifest)

    report = """# 第 5 批开发升级报告

本批 15 篇、30 个 AR/PR 包均已完成开发实施并逐篇保存。14 篇为 `implemented_pending_expanded_reference`；INP（`paper_2c439196c2f349c9`）为 `blocked`，已完成可做的输入整理、三模型契约和 evaluator，但实验数据/校准门槛尚未解除。类别目标包含 4 篇加强 B、10 篇 A→B 和 1 篇 A→C；这是实施范围，不能理解为科学验证等级已认证。

本进程新增科学引擎启动为 **0**，没有运行长量化计算、HPC、付费服务或 LLM 科学判卷。完成的是图/连接/电荷/映射检查、正式 ECP 输入核对、理想周期起点构造、已有图像测点数字化及任务包回归。新增参考能量、光谱、响应、容差均未伪造；旧 final 的 PASS 不构成新版完成声明。

## 包组织、科学边界与评估

只在本批 `tasks/upgrade_tasks/{autonomous_research,paper_reproduction}/paper_id` 和本协调目录写入。每包从对应 final 复制并记录源 payload 哈希，全部源文件逐字节存于私有 `evaluation/legacy_final_snapshot/*.snapshot`。未改动源 final、hold、论文、verification、升级方案或公共维护工具；未提交 git、未清理其他进程文件。

保留 task.md 的 Scientific objective、Public inputs and scientific boundaries、Required scientific validation/investigation、Deliverables 等科学英语结构。PR 单独加入作者原假设、原理/方法及新增对照边界；AR 公开的是可实施对象/实验观测，不公开新终态、赢家或参考计算值。两模式共享科学目标、对象数据、schema、完成标准和五份科学 evaluator。

每篇命名面板把新增研究矩阵落实到可审计字段、单位、原子对应、状态和记录引用；`report/results.json` 与可读 `report/report.md` 均必需。100 分 rubric 中对象/定义 10 分、新比较 65 分、证据化假设检验/稳健性 15 分、结论 10 分；具体比较绑定对应字段与原始文件。新的支持、反驳和证据充分的不可区分结论公平评分。缺核心比较、错误对象/电荷/态或能零、仅旧标量、失败冒充完成均受拒绝。

`bounded_failure` 可以零引擎启动、零资源计数、空证据数组和无计算记录，必须说明输入缺口/已做尝试/解除条件；格式可接受不等于科学通过。证据化 BS、候选或配位水坍缩允许提交，不强造有效极小点。安全 `./outputs/...` 路径可用，`..` 越界不可用。顶部 optional 保持可选，不列为硬失败。

## 验证结果

"""
    report += f"- 官方包/运行时/公开 materialize/AR–PR 一致性/源哈希/schema 与正反例：**{validation['checks']} 项通过**，发现范围 `{validation['repository_test_scope']}`。\n"
    report += f"- 输入图、映射、电荷、扭转连接、周期计量及 ECP：**{identities['checks']} 项通过**，包括 {identities['mapped_graphs']} 个映射图。\n"
    report += f"- 冻结前逐包官方 payload 哈希、完整源快照清单及源包未变：**{len(checks)} 项通过**。\n"
    report += "- 通过 `TaskRepository(roots=[Path('tasks/upgrade_tasks')])` 加载，未改默认正式库发现机制。\n- 所有合成正反例只在临时目录，均标注非科学数据；未进入任务 payload。\n\n"
    report += "复现命令（仓库根目录）：\n\n```bash\n.envs/researchchembench/bin/python tasks/upgrade_tasks/coordination_20260927/batch5/check_batch.py\n.envs/researchchembench/bin/python tasks/upgrade_tasks/coordination_20260927/batch5/check_identities.py\n```\n\n"
    report += "这些检查确认包与输入结构，并未运行新参考或证明科学预测。正式科学验证先执行每包 `evaluation/reference_validation_plan.md` 的输入/接口/代表性先导，再覆盖完整矩阵、诊断及误差校准。\n\n## 逐篇结果\n\n"
    for index, row in enumerate(papers, 1):
        pid = row["paper_id"]
        d = DETAILS[pid]
        report += f"### {index}. {pid} — {d['title']}\n\n"
        report += f"状态：`{row['status']}`；{row['old_class']} → {row['new_class']}。\n\n"
        for label, key in [("科学升级", "science"), ("正文/SI 依据", "sources"), ("评估改动", "evaluator"), ("可行性", "feasibility"), ("限制/待补参考", "limits")]:
            report += f"**{label}：**{d[key]}\n\n"
        report += "**结果面板：**" + "、".join("`" + p + "`" for p in row["result_panels"]) + "。\n\n"
        report += f"[逐篇审查](paper_reviews/{pid}.md) · [AR 验证计划](../../autonomous_research/{pid}/evaluation/reference_validation_plan.md) · [PR 验证计划](../../paper_reproduction/{pid}/evaluation/reference_validation_plan.md)。源文件及哈希见各包 `evaluation/task_provenance/upgrade_audit.json`。\n\n"
    report += """## 已处理监督反馈与交接

CB7 单客体不强制不存在的第二客体几何；无适当暗态时不强造暗态和数值劈裂。对应正例及错误数值、缺解释、缺删伙伴的反例已通过。所有包均验证合法零启动 failure，且不能将它改称 supported。Y₂ 任务只要求张量导数/Bose 代理量，不编造定量寿命。安全带 `./` 的输出路径已通过契约。

本进程对全部 15 篇停止修改，供 supervisor `01a0e2da-982a-7b32-bcc1-744840298ce5` 逐篇冻结、亲自复核和启动其另行授权的真实验证。`handoff.json` 逐篇记录移交 ID、两个 payload 哈希、manifest 文件哈希、未解决问题、验证计划和 `stop_modifying: true`；`manifest.json` 保留全部路径、状态和检查摘要。

构建脚本是开发历史，部分输入准备脚本有顶层副作用，**不要在已冻结包上盲目重跑生成器**。后续若需修包，应先核对 handoff 哈希和监督进程是否已经取得写权，以免覆盖正在运行的验证快照。开发就绪不代表科学通过；INP 的输入阻塞和其余新增参考缺口必须在后续记录中继续可见。
"""
    (B / "REPORT.md").write_text(report)
    status = "# 第 5 批状态\n\n开发实施已保存并移交；15 篇/30 包。新增科学引擎启动 0；14 篇 pending expanded reference，1 篇 blocked。全部条目 `stop_modifying: true`。\n\n"
    status += f"官方检查 {validation['checks']}、身份检查 {identities['checks']}、交接完整性检查 {len(checks)} 全部通过；均不代表新版科学验证通过。\n\n"
    for row in papers:
        status += f"- {row['paper_id']}：{row['status']}；AR/PR 已冻结移交。\n"
    status += "\n入口：[REPORT.md](REPORT.md)、[manifest.json](manifest.json)、[handoff.json](handoff.json)、[validation_report.json](validation_report.json)。\n"
    (B / "STATUS.md").write_text(status)
    handoff = {"batch": 5, "handoff_at": timestamp, "supervisor_thread_id": "01a0e2da-982a-7b32-bcc1-744840298ce5", "development_worker_thread_id": "01a0e27f-4c62-7241-b1ba-47af9c7e733e", "stop_modifying": True, "scientific_engine_starts": 0, "development_only": True, "counts": {"papers": 15, "packages": 30, **counts}, "report_sha256": sha(B / "REPORT.md"), "manifest_sha256": sha(B / "manifest.json"), "check_report_sha256": manifest["check_reports"], "papers": handoff_rows}
    write_json(B / "handoff.json", handoff)
    handoff_md = "# 第 5 批冻结交接\n\n30 个开发包现已停止修改。逐包完整哈希和未解决事项见 [handoff.json](handoff.json)，逐篇中文科学说明见 [REPORT.md](REPORT.md)。\n\n"
    handoff_md += "14 篇已实现但待扩展参考，INP 一篇输入阻塞；全部尚无新版科学 PASS。监督复核/真实验证仍是下一阶段。\n\n| 论文 | 状态 | AR payload SHA256 | PR payload SHA256 | 停止修改 |\n|---|---|---|---|---|\n"
    for row in papers:
        handoff_md += f"| {row['paper_id']} | {row['status']} | `{row['package_hashes'][MODES[0]]}` | `{row['package_hashes'][MODES[1]]}` | true |\n"
    (B / "HANDOFF.md").write_text(handoff_md)
    print(json.dumps({"status": "handed_off", "papers": 15, "packages": 30, "status_counts": counts, "official_checks": validation["checks"], "identity_checks": identities["checks"], "handoff_integrity_checks": len(checks), "stop_modifying": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
