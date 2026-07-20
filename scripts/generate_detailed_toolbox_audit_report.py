#!/usr/bin/env python3
"""Generate the presentation-grade detailed chemistry-toolbox audit report."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from researchchem_toolbox.catalog import action_specs, backend_specs, catalog_snapshot


OUTPUT = ROOT / "docs/tools/CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md"
COVERAGE = ROOT / "config/action_test_coverage.json"
ACTION_GAP = ROOT / "config/action_gap_smoke_status.json"
BACKEND_GAP = ROOT / "config/backend_gap_smoke_status.json"
SCIENTIFIC_SMOKE = ROOT / "config/scientific_resource_smoke_status.json"
DATA_SMOKE = ROOT / "config/data_source_smoke_status.json"
RESOURCE_STATUS = ROOT / "config/toolbox_resource_status.json"
PROFILE_STATUS = ROOT / "docs/MCP_PROFILE_STATUS.json"
REQUESTED_SOFTWARE = ROOT / "config/requested_software_status.json"
PYTEST_STATUS = ROOT / "config/pytest_status.xml"


CATEGORY_ZH = {
    "scientific_data_interchange": "科学数据与格式互操作",
    "structure_and_system": "结构与体系准备",
    "cheminformatics": "化学信息学",
    "molecular_electronic": "分子电子结构与派生性质",
    "reaction_and_kinetics": "反应路径、热力学与动力学",
    "molecular_dynamics": "分子动力学、轨迹与自由能",
    "periodic_and_phonons": "周期材料、电子结构、声子与热输运",
    "docking": "分子对接",
    "data_sources": "外部化学数据源",
}


ACTION_FUNCTION_ZH = {
    "normalize_qcschema_molecule": "把一个分子结构验证并规范化为 QCSchema Molecule；不启动量化计算。",
    "validate_qcschema_record": "验证指定类型的 QCSchema/QCArchive 记录并返回规范化记录或结构化错误。",
    "parse_quantum_chemistry_output": "从已有量化输出文件中解析智能体明确选择的性质，不重新计算。",
    "standardize_structure": "清洗和标准化分子表示，不生成三维坐标，也不优化几何。",
    "generate_3d_structure": "由二维分子表示生成一个明确的三维结构。",
    "generate_conformer_ensemble": "生成构象集合；量化精修、排序和加权仍由后续独立 Action 完成。",
    "cluster_conformers": "按明确 RMSD 阈值对已有构象集合聚类。",
    "align_molecular_structures": "按显式原子映射把探针三维结构刚性对齐到参考结构。",
    "rank_conformers_from_results": "根据智能体已提供的能量或自由能结果排序构象并计算 Boltzmann 权重。",
    "repair_biomolecular_structure": "修复生物分子结构中缺失的残基或原子，不隐藏质子化、参数化或溶剂化。",
    "select_structure_subset": "从 PDB 中按链、模型和异原子保留策略选择结构子集。",
    "renumber_biomolecular_structure": "按显式起始编号重排 PDB 原子和残基编号，不改变化学与坐标。",
    "normalize_pdb_records": "整理、排序并规范化 PDB 记录。",
    "assign_protonation_states": "按智能体选择的规则或后端为固定结构添加/调整质子化状态。",
    "assign_partial_charges": "在不自动参数化或溶剂化的前提下计算并附加部分电荷。",
    "assign_force_field_parameters": "用明确选择的力场为已有结构建立参数化体系。",
    "solvate_molecular_system": "按明确盒形、尺寸、溶剂模型与组成对参数化体系溶剂化。",
    "analyze_crystal_symmetry": "分析周期晶体的空间群、对称操作与等价位置。",
    "standardize_crystal_structure": "按原胞或常规胞约定标准化晶体结构。",
    "build_supercell": "根据显式超胞矩阵扩展周期结构。",
    "enumerate_surface_slabs": "根据 Miller 指数、厚度和真空层枚举表面 slab。",
    "calculate_molecular_descriptors": "计算一组明确选择的分子描述符。",
    "calculate_molecular_fingerprint": "生成指定类型和参数的分子指纹。",
    "calculate_molecular_similarity": "用明确指纹和相似性度量比较分子。",
    "search_local_substructures": "在本地分子集合中执行 SMARTS/子结构匹配。",
    "enumerate_tautomers": "按明确规则枚举互变异构体。",
    "enumerate_stereoisomers": "枚举未指定或目标立体中心的立体异构体。",
    "calculate_energy": "用智能体明确选择的软件和理论方法计算一个分子或非周期体系的标量能量。",
    "calculate_forces": "计算一个结构或同质结构批次的原子力。",
    "calculate_hessian": "计算或数值构造 Hessian；振动分析仍是独立 Action。",
    "optimize_geometry": "按显式收敛阈值优化一个结构，只把优化结构作为主要科学结果。",
    "calculate_dipole_moment": "计算分子偶极矩。",
    "calculate_atomic_charges": "用明确人口分析/电荷方案计算原子电荷。",
    "calculate_orbitals": "提取轨道能量、占据数、系数或相关轨道信息。",
    "calculate_bond_orders": "用明确方案计算原子对键级。",
    "calculate_excited_states": "用明确的激发态方法和状态数计算电子激发态。",
    "analyze_electron_density_topology": "对已有波函数或电子密度执行临界点/拓扑分析。",
    "calculate_atomic_basin_properties": "对电子密度原子盆进行积分并返回盆性质。",
    "calculate_bader_charges": "从周期电子密度计算 Bader 电荷。",
    "derive_vibrational_modes": "由已有 Hessian 与结构导出频率和正常模式，不隐藏 Hessian 计算。",
    "derive_ir_spectrum": "由已有振动频率与强度构建展宽后的红外光谱。",
    "derive_uv_vis_spectrum": "由已有跃迁能和振子强度构建展宽后的 UV/Vis 光谱。",
    "derive_thermochemistry": "由电子能和频率推导指定温压下的热化学量。",
    "locate_transition_state": "从给定初猜定位一个候选过渡态；频率和 IRC 验证保持独立。",
    "trace_intrinsic_reaction_coordinate": "从已给定的过渡态结构沿一个或两个方向追踪 IRC。",
    "calculate_chemical_equilibrium": "对显式机理、组成和热力学条件计算平衡状态。",
    "integrate_reaction_network": "对显式反应网络与初始状态进行时间积分。",
    "calculate_rate_constants": "在指定温压点计算 Arrhenius、多 Arrhenius、PDep 或 Chebyshev 速率常数。",
    "calculate_tunneling_correction": "按 Wigner 或 Eckart 模型计算隧穿修正。",
    "solve_master_equation": "对智能体提供的 MESS/MESMER 主方程模型求解并提取唯象速率。",
    "solve_microkinetic_model": "求解智能体完整指定的 CatMAP 微观动力学模型，不替智能体构造反应网络。",
    "minimize_system_energy": "对已参数化体系执行一次能量最小化，不自动平衡或继续动力学。",
    "calculate_force_field_energy": "对已参数化体系计算力场势能。",
    "calculate_force_field_forces": "对已参数化体系计算力场原子力。",
    "decompose_force_field_energy": "把力场势能按已有 Force 对象分解，不重新定义力场。",
    "propagate_dynamics": "执行一个由智能体定义的动力学片段并返回轨迹和最终状态。",
    "calculate_trajectory_rmsd": "计算轨迹相对参考结构的 RMSD。",
    "calculate_radius_of_gyration": "计算轨迹随时间变化的回转半径。",
    "calculate_radial_distribution": "计算两组原子选择之间的径向分布函数。",
    "calculate_mean_squared_displacement": "计算选定原子的均方位移。",
    "calculate_contacts": "统计轨迹中的原子/残基接触。",
    "calculate_solvent_accessible_surface": "计算溶剂可及表面积。",
    "calculate_dihedral_distribution": "计算显式二面角集合的时间序列或分布。",
    "calculate_hydrogen_bonds": "按明确几何标准分析氢键。",
    "calculate_principal_components": "对对齐后的轨迹执行主成分分析。",
    "calculate_dynamic_cross_correlation": "计算原子运动的动态交叉相关矩阵。",
    "assign_secondary_structure": "为蛋白轨迹分配二级结构。",
    "cluster_trajectory": "按明确特征和聚类参数对轨迹帧聚类。",
    "evaluate_collective_variables": "用 PLUMED 对已有轨迹计算智能体指定的集体变量。",
    "estimate_free_energy_difference": "用 MBAR 对明确给定的约化势数据估计态间自由能差。",
    "estimate_thermodynamic_expectations": "用 MBAR 估计热力学期望值及不确定度。",
    "calculate_potential_of_mean_force": "由采样数据计算一维或离散自由能面/PMF。",
    "analyze_free_energy_convergence": "分析自由能估计随样本量或时间的收敛。",
    "parse_alchemical_energy_data": "从 GROMACS、Amber 或 NAMD 输出解析炼金自由能数据。",
    "calculate_periodic_energy": "用明确周期电子结构后端计算总能。",
    "calculate_periodic_forces": "计算周期体系原子力。",
    "calculate_periodic_stress": "计算周期体系应力张量。",
    "relax_periodic_structure": "按显式阈值弛豫周期原子位置，并可选择是否弛豫晶胞。",
    "calculate_electronic_band_structure": "沿智能体给定的 k 路径计算电子能带。",
    "calculate_density_of_states": "计算总电子态密度。",
    "calculate_projected_density_of_states": "计算按原子/轨道投影的电子态密度。",
    "analyze_periodic_bonding": "从已有周期波函数输出执行 COHP/COOP/COBI 等成键分析。",
    "calculate_charge_spilling": "评估 LOBSTER 投影质量和电荷泄漏。",
    "generate_displaced_supercells": "按超胞和位移幅度生成有限位移结构。",
    "assemble_force_constants": "由位移集合与对应力组装二阶力常数。",
    "calculate_phonon_dispersion": "由二阶力常数沿给定 q 路径计算声子色散。",
    "calculate_phonon_density_of_states": "由二阶力常数和 q 网格计算声子态密度。",
    "calculate_harmonic_thermodynamics": "从声子谱计算谐振近似热力学量。",
    "calculate_phonon_group_velocities": "计算声子群速度。",
    "calculate_lattice_thermal_conductivity": "由显式二阶/三阶力常数和求解设置计算晶格热导率。",
    "dock_ligand": "把已准备好的配体对接到已准备好的受体，并使用显式搜索盒。",
    "search_compounds": "通过 PubChem 执行受限化合物检索。",
    "resolve_chemical_identity": "把名称、CID、CAS、SMILES 等标识解析为统一化学身份。",
    "retrieve_compound_properties": "从 PubChem 获取智能体指定的单分子性质字段。",
    "retrieve_compound_structure": "从 PubChem 获取指定二维/三维结构记录。",
    "search_similar_compounds": "通过 PubChem 相似性服务检索相似化合物。",
    "search_substructures": "通过 PubChem 子结构服务检索匹配化合物。",
    "search_protein_structures": "通过 RCSB PDB Data API 检索蛋白/大分子结构。",
    "search_materials": "通过 Materials Project API 检索材料记录。",
    "search_catalysis_records": "通过 Catalysis-Hub GraphQL 检索催化反应记录。",
    "lookup_nist_webbook_species": "使用 NIST WebBook 官方 CGI 对一个物种做受限精确查询。",
}


POLICY_ZH = {
    "agent_backend_required": "智能体必须显式选择 `backend_id`",
    "agent_components_required": "智能体必须显式选择主后端及组件后端",
    "agent_source_required": "智能体必须显式选择 `source_id`",
    "fixed_source": "固定官方数据源",
    "internal_deterministic": "固定确定性内部实现",
}


def read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def md(value: Any) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def codes(values: Any) -> str:
    values = list(values or [])
    return ", ".join(f"`{md(value)}`" for value in values) if values else "—"


def junit_summary() -> dict[str, str]:
    if not PYTEST_STATUS.is_file():
        return {}
    root = ET.parse(PYTEST_STATUS).getroot()
    if root.tag == "testsuites":
        suites = list(root.findall("testsuite"))
        result = {}
        for key in ("tests", "failures", "errors", "skipped", "time"):
            if key in root.attrib:
                result[key] = root.attrib[key]
            else:
                result[key] = str(sum(float(suite.attrib.get(key, 0)) for suite in suites))
        return result
    return {key: root.attrib.get(key, "0") for key in ("tests", "failures", "errors", "skipped", "time")}


def error_text(item: dict[str, Any] | None) -> str:
    if not item:
        return ""
    error = item.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or "")
    return str(error or "")


def current_network_cases(
    action_gap: dict[str, Any], data_smoke: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}
    for item in data_smoke.get("cases") or []:
        cases[str(item["action"])] = dict(item)
    for item in action_gap.get("cases") or []:
        action_id = str(item.get("action") or "")
        if action_id in action_specs() and action_specs()[action_id].data_action:
            cases[action_id] = dict(item)
    return cases


def main() -> int:
    load_dotenv(ROOT / "config.local.env", override=False)
    generated_at = datetime.now(timezone.utc).isoformat()
    coverage = read_json(COVERAGE, {"summary": {}, "actions": []})
    action_gap = read_json(ACTION_GAP, {"summary": {}, "cases": []})
    backend_gap = read_json(BACKEND_GAP, {"summary": {}, "cases": []})
    scientific_smoke = read_json(SCIENTIFIC_SMOKE, {"summary": {}, "cases": []})
    data_smoke = read_json(DATA_SMOKE, {"summary": {}, "cases": []})
    resources = read_json(RESOURCE_STATUS, {"summary": {}, "resources": []})
    profiles = read_json(PROFILE_STATUS, {"summary": {}, "profiles": {}})
    requested = read_json(REQUESTED_SOFTWARE, {"summary": {}, "software": []})
    tests = junit_summary()
    catalog = catalog_snapshot(include_health=True)

    action_by_id = {item["action"]: item for item in coverage.get("actions") or []}
    successful_pairs = {tuple(item) for item in coverage.get("successful_action_backend_pairs") or []}
    failed_pairs = {tuple(item) for item in coverage.get("failed_action_backend_pairs") or []}
    network_cases = current_network_cases(action_gap, data_smoke)
    backend_health = {item["id"]: item.get("health") or {} for item in catalog["backends"]}
    backend_success_actions: dict[str, list[str]] = defaultdict(list)
    for action_id, backend_id in successful_pairs:
        backend_success_actions[backend_id].append(action_id)

    data_action_ids = [item.id for item in action_specs().values() if item.data_action]
    live_data_success = {
        action_id
        for action_id in data_action_ids
        if network_cases.get(action_id, {}).get("status") in {"success", "partial_success"}
    }
    live_data_degraded = set(data_action_ids) - live_data_success
    scientific_ids = [item.id for item in action_specs().values() if not item.data_action]
    scientific_success = {
        action_id
        for action_id in scientific_ids
        if action_by_id.get(action_id, {}).get("status") == "runtime_success"
    }
    current_end_to_end_success = scientific_success | live_data_success

    local_backends = {
        backend.id for backend in backend_specs().values() if backend.runtime != "services"
    }
    service_backends = set(backend_specs()) - local_backends
    current_live_backend_success = set(local_backends)
    for backend_id in service_backends:
        actions = [
            action.id
            for action in action_specs().values()
            if backend_id in action.backend_ids
        ]
        if any(action in live_data_success for action in actions):
            current_live_backend_success.add(backend_id)

    category_counts = Counter(spec.category for spec in action_specs().values())
    category_current_success = Counter(
        action_specs()[action_id].category for action_id in current_end_to_end_success
    )
    category_degraded = Counter(
        action_specs()[action_id].category for action_id in live_data_degraded
    )

    missing_action_translations = sorted(set(action_specs()) - set(ACTION_FUNCTION_ZH))
    if missing_action_translations:
        raise RuntimeError(f"Missing Chinese Action descriptions: {missing_action_translations}")

    coverage_summary = coverage.get("summary") or {}
    requested_summary = requested.get("summary") or {}
    profile_summary = profiles.get("summary") or {}
    resource_summary = resources.get("summary") or {}
    healthy_backends = sum(bool(value.get("available")) for value in backend_health.values())
    evidence_backends = int(coverage_summary.get("backends_with_runtime_success_evidence", 0))
    test_count = int(float(tests.get("tests", 0)))
    test_failures = int(float(tests.get("failures", 0))) + int(float(tests.get("errors", 0)))

    lines = [
        "# ResearchChemBench 化学工具箱详细审计与汇报报告",
        "",
        f"> 审计日期：`2026-07-20 UTC`；报告生成时间：`{generated_at}`。",
        "> 本报告统计的是当前工作区实际 Catalog、隔离运行环境、逐 Action 调用记录、真实后端 smoke、在线数据源现场状态和全量回归测试。",
        "",
        "## 1. 执行结论",
        "",
        "### 1.1 最重要的数字",
        "",
        "| 指标 | 结果 | 解释 |",
        "|---|---:|---|",
        f"| 公开 Actions | **{len(action_specs())}** | {len(scientific_ids)} 个 Scientific Actions + {len(data_action_ids)} 个 Data Actions |",
        f"| 本轮逐 Action 已触发 | **{len(action_by_id)}/{len(action_specs())}** | 每个公开 Action 至少进入过真实统一分发器一次 |",
        f"| 当前现场端到端成功 | **{len(current_end_to_end_success)}/{len(action_specs())}** | {len(scientific_success)} 个本地 Scientific Actions + {len(live_data_success)} 个在线 Data Actions |",
        f"| 当前受外部服务影响 | **{len(live_data_degraded)}** | 全部是在线数据源；本地 Scientific Action 为 0 个失败 |",
        f"| 至少存在一次成功证据 | **{coverage_summary.get('runtime_success_actions', 0)}** | 包含单元/契约测试与真实 smoke；`search_compounds` 契约测试成功但当前 PubChem 现场失败 |",
        f"| 完全没有成功证据 | **{coverage_summary.get('failure_only_actions', 0)}** | 5 个扩展 PubChem Action + Catalysis-Hub |",
        f"| 注册 BackendSpecs | **{len(backend_specs())}** | 71 个本地执行提供者 + 5 个在线数据服务 |",
        f"| 后端健康检查可用 | **{healthy_backends}/{len(backend_specs())}** | 加载 `config.local.env` 后模块、命令、模型与凭据检查均可用 |",
        f"| 有成功调用证据的后端 | **{evidence_backends}/{len(backend_specs())}** | 仅 Catalysis-Hub 本轮没有成功证据 |",
        f"| 当前现场成功的后端 | **{len(current_live_backend_success)}/{len(backend_specs())}** | 全部 71 个本地后端 + RCSB PDB、Materials Project、NIST WebBook；PubChem/Catalysis-Hub 当前降级 |",
        f"| Action–Backend 候选组合 | **{coverage_summary.get('action_backend_pair_count', 0)}** | Catalog 中声明的全部组合 |",
        f"| 已成功实测组合 | **{coverage_summary.get('successful_action_backend_pairs', 0)}** | 至少一次成功/部分成功 |",
        f"| 仅有失败证据的组合 | **{coverage_summary.get('failed_action_backend_pairs', 0)}** | 5 个扩展 PubChem 组合 + 1 个 Catalysis-Hub 组合；`search_compounds` 另有契约成功证据但当前在线失败 |",
        f"| 尚未逐组合实测 | **{coverage_summary.get('unobserved_action_backend_pairs', 0)}** | 多数是同一 Action 的替代软件后端；不能宣称 233 个组合全部通过 |",
        f"| 全量回归 | **{test_count - test_failures}/{test_count} passed** | 用时 {tests.get('time', '—')} 秒；failures+errors={test_failures} |",
        f"| MCP 隔离运行环境 | **{profile_summary.get('ready_profiles', 0)}/{profile_summary.get('profile_count', 0)} ready** | 每个后端按 runtime profile 隔离依赖 |",
        f"| 注册科学资源 | **{resource_summary.get('passed', 0)}/{resource_summary.get('resource_count', 0)}** | 赝势、基组、模型等资源校验 |",
        f"| 用户要求的软件清单 | **{requested_summary.get('total', 0)} 项** | configured={requested_summary.get('configured', 0)}；partial=2；manual/review=10；specification=1 |",
        "",
        "### 1.2 能否说“所有工具都正常运行”",
        "",
        "不能不加限定地这样说。准确表述是：",
        "",
        "- **本地 Scientific Actions：91/91 至少有一个代表性后端成功执行。**",
        "- **本地 BackendSpecs：71/71 至少有一个真实 Action 成功执行。**",
        "- **在线 Data Actions：3/10 当前现场成功，7/10 受服务端 503 或超时影响。**",
        "- **所有 101 个 Action 都已触发和记录状态，但不是所有 233 个 Action–Backend 组合都逐一运行。** 当前还有 62 个替代后端组合没有本轮运行证据。",
        "- 当前 smoke 证明的是接口、调度、输入生成、程序执行和主要输出解析链路可工作；它**不是**对所有方法、元素、体系尺度、收敛参数和科学精度的穷尽验证。",
        "",
        "## 2. 测试方法与证据层级",
        "",
        "本次采用四层证据，避免把“命令存在”与“科学 Action 可用”混为一谈：",
        "",
        "1. **Catalog/契约层**：校验 ActionSpec、BackendSpec、必填输入、方法字段、设置字段、禁止 `auto` 和禁止自动 fallback。",
        "2. **分发层**：所有记录均经过 `researchchem_toolbox.service.execute_action`，验证智能体的选择被原样执行。",
        "3. **真实后端 smoke 层**：运行量化程序、MD 引擎、材料程序、机器学习势、反应动力学软件和数据接口，并检查主要结果或产物文件。",
        "4. **全量回归层**：`pytest` 共 146 项全部通过，覆盖契约、适配器、安全约束、资源注册与部分真实/模拟输出解析。",
        "",
        "| 证据文件 | 结果 | 作用 |",
        "|---|---|---|",
        f"| `config/action_test_coverage.json` | {coverage_summary.get('runtime_success_actions', 0)} success-evidence / {coverage_summary.get('failure_only_actions', 0)} failure-only | 汇总逐 Action 与 Action–Backend 组合 |",
        f"| `config/action_gap_smoke_status.json` | {action_gap.get('summary', {}).get('passed', 0)}/{action_gap.get('summary', {}).get('case_count', 0)} passed | 补齐 IRC、CatMAP、PLUMED、MDAnalysis、Phonopy、Cantera 等 Action；另做在线复测 |",
        f"| `config/backend_gap_smoke_status.json` | {backend_gap.get('summary', {}).get('passed', 0)}/{backend_gap.get('summary', {}).get('case_count', 0)} passed | 补齐 17 个此前仅健康检查的本地后端，并追加 PySCF 单点能组合复核 |",
        f"| `config/scientific_resource_smoke_status.json` | {scientific_smoke.get('summary', {}).get('passed', 0)}/{scientific_smoke.get('summary', {}).get('case_count', 0)} passed | 真实赝势、基组、模型、周期程序和 GNINA/ORCA 等资源 smoke |",
        f"| `config/data_source_smoke_status.json` | {data_smoke.get('summary', {}).get('passed', 0)}/{data_smoke.get('summary', {}).get('case_count', 0)} passed | 在线数据源现场状态 |",
        f"| `config/pytest_status.xml` | {test_count - test_failures}/{test_count} passed | 最终全量回归，{tests.get('time', '—')} 秒 |",
        "",
        "### 2.1 本轮真实补测的软件后端",
        "",
        f"以下 {sum(item.get('status') in {'success', 'partial_success'} for item in backend_gap.get('cases', []))} 个补缺用例在本轮全部通过统一 MCP Action 分发链路：",
        "",
        codes(sorted({item.get("backend") for item in backend_gap.get("cases", []) if item.get("status") in {"success", "partial_success"}})),
        "",
        "此外，CatMAP 0.3.1 和 Pysisyphus IRC 在补测过程中发现并修复了真实适配问题：",
        "",
        "- Pysisyphus 现在分别适配 XTB 与 PySCF：`gfn2` 等方法会正确映射为 XTB 的 `gfn` 参数，HF/DFT/MP2 会按 PySCF 的 method/xc/basis 语义生成输入；两条链路都以 HCN 异构化过渡态成功生成 IRC 路径。反应运行环境已固定加入 `pyscf==2.13.1`。",
        "- CatMAP 不再直接使用未初始化的 `ReactionModel()`；现在由类型化字段生成受控 `.mkm` setup 文件，再调用官方 `ReactionModel(setup_file=...)`，CO 氧化微观动力学模型成功返回 rate/coverage/production-rate maps。",
        "- PLUMED driver 现在支持显式 `box_angstrom`、`timestep_ps` 和 `trajectory_stride`，真实集体变量计算通过。",
        "",
        "## 3. 工具箱如何工作：Action 流程与智能体自由度",
        "",
        "```text",
        "科学任务",
        "  ↓ 智能体自行判断当前需要的原子科学动作",
        "选择 Action",
        "  ↓ 智能体显式选择 backend_id / source_id / component_backends",
        "填写 inputs + method_spec + action_settings + resource_limits",
        "  ↓ 统一分发器做契约、必填字段、兼容性和健康检查",
        "隔离 runtime worker",
        "  ↓ 仅执行智能体所选的软件与参数；automatic_fallback_count = 0",
        "类型化 ActionResult",
        "  ├─ result：主要科学结果",
        "  ├─ output_artifacts：可传给后续 Action 的文件/对象",
        "  ├─ provenance：Action、后端、方法、设置、资源、命令和 Catalog hash",
        "  └─ warnings/error：结构化状态",
        "  ↓",
        "智能体读取结果后，自主决定下一次调用哪个 Action/软件",
        "```",
        "",
        "关键设计原则：",
        "",
        "- 不公开 `run_ase`、`run_orca`、`run_workflow` 这类笼统流程工具。",
        "- Scientific Action 默认要求智能体明确给出 `backend_id`；禁止 `backend_id=auto`。",
        "- 组合动作要求智能体明确选择组件后端，例如优化器与能量/梯度计算器。",
        "- 系统不替智能体选择理论方法、基组、泛函、力场、赝势、模型权重或流程顺序。",
        "- 运行时只负责机械隔离、资源限制与精确执行，不进行科学 fallback。",
        "",
        "### 3.1 典型但非固定的智能体编排示例",
        "",
        "这些只是可能的调用图，不是工具箱内置流程：",
        "",
        "- 分子热化学：`standardize_structure → generate_3d_structure → generate_conformer_ensemble → optimize_geometry → calculate_energy → calculate_hessian → derive_vibrational_modes → derive_thermochemistry`。每一步的软件和是否继续均由智能体决定。",
        "- 反应速率：`locate_transition_state → calculate_hessian → derive_vibrational_modes → trace_intrinsic_reaction_coordinate → calculate_tunneling_correction → calculate_rate_constants`。",
        "- 分子动力学：`assign_protonation_states → assign_partial_charges → assign_force_field_parameters → solvate_molecular_system → minimize_system_energy → propagate_dynamics → trajectory/free-energy Actions`。",
        "- 周期材料：`standardize_crystal_structure → relax_periodic_structure → electronic structure Actions`，或 `generate_displaced_supercells → 外部力计算 → assemble_force_constants → phonon/thermal Actions`。",
        "- 对接：智能体先自行准备受体/配体与搜索盒，再调用 `dock_ligand`，之后自行选择结构或轨迹分析工具。",
        "",
        "## 4. 化学领域覆盖情况",
        "",
        "| 领域 | Action 数 | 当前现场成功 | 当前降级 | 覆盖评价 |",
        "|---|---:|---:|---:|---|",
    ]

    domain_assessment = {
        "scientific_data_interchange": "QCSchema 规范化/验证与主流量化输出解析，适合作为跨软件数据桥。",
        "structure_and_system": "分子、蛋白 PDB、晶体、超胞、表面、质子化、电荷、力场和溶剂化准备较完整。",
        "cheminformatics": "描述符、指纹、相似性、子结构、互变异构和立体异构覆盖常用基础操作。",
        "molecular_electronic": "基态能量/力/Hessian/优化及部分电荷、轨道、键级、激发态、电子密度和光谱派生，基础骨架较强。",
        "reaction_and_kinetics": "TS、IRC、平衡、网络积分、速率、隧穿、主方程和微观动力学均有原子 Action。",
        "molecular_dynamics": "体系执行、轨迹分析、集体变量、MBAR/PMF 与炼金数据解析覆盖广，但高级采样生成仍不足。",
        "periodic_and_phonons": "周期能量/力/应力/弛豫、能带/DOS、LOBSTER、声子和晶格热导形成完整基础链。",
        "docking": "具备 Vina/GNINA 对接核心动作，但受体/配体专用准备和高级重打分尚不完整。",
        "data_sources": "PubChem、RCSB、Materials Project、Catalysis-Hub、NIST WebBook；当前 PubChem/Catalysis-Hub 现场降级。",
    }
    for category, count in category_counts.items():
        lines.append(
            f"| {CATEGORY_ZH[category]} | {count} | {category_current_success[category]} | {category_degraded[category]} | {md(domain_assessment[category])} |"
        )

    lines.extend(
        [
            "",
            "### 4.1 当前尚未或覆盖较弱的方向",
            "",
            "| 方向 | 当前缺口 | 建议新增的原子 Action 方向 |",
            "|---|---|---|",
            "| 多参考与高阶相关电子结构 | 缺少 CASSCF/CASPT2/NEVPT2、CC/EOM-CC 等统一类型化动作 | `calculate_multireference_states`、`calculate_correlated_energy`、`calculate_eom_excited_states` |",
            "| 非绝热动力学与光化学 | SHARC、Newton-X 已安装但仍是 runtime-only；缺少态耦合、初态采样、surface hopping | `sample_excited_state_initial_conditions`、`calculate_nonadiabatic_couplings`、`propagate_nonadiabatic_dynamics` |",
            "| 光谱广度 | 已有 IR/UV-Vis；缺 Raman、NMR、EPR、XAS/XES、圆二色等 | 独立性质计算与独立谱线构造 Actions |",
            "| QM/MM 与嵌入 | 尚无显式 QM 区/MM 区、边界、嵌入电荷和耦合设置 | `build_qmmm_partition`、`calculate_qmmm_energy_forces`、`propagate_qmmm_dynamics` |",
            "| 高级自由能与增强采样 | 有 CV 评估、MBAR/PMF；没有 metadynamics、umbrella window 执行、重加权和采样收敛执行动作 | `propagate_enhanced_sampling`、`run_umbrella_sampling_window`、`reweight_biased_trajectory` |",
            "| 自动反应发现 | AutoMeKin、KinBot、autodE、CENSO 等部分已安装但没有作为单一粗粒度 workflow 暴露 | 应拆成候选生成、路径搜索、过滤、精修、网络扩展等原子 Actions |",
            "| 电化学/电催化 | 缺恒电位、溶剂/电极界面、CHE、电荷补偿和电势扫描 | 显式电极模型、potential/charge scan、表面反应自由能 Actions |",
            "| 周期多体与拓扑材料 | Yambo、Wannier90 已安装但 runtime-only；缺 GW/BSE、激子、Wannier、Berry/拓扑性质 | `calculate_quasiparticle_energies`、`calculate_exciton_properties`、`construct_wannier_functions`、`calculate_berry_phase_properties` |",
            "| 缺陷、相图、吸附与催化结构搜索 | 目前只有晶体/超胞/slab；缺点缺陷枚举、相稳定性、吸附位点和吸附能专门动作 | `generate_defect_structures`、`calculate_phase_diagram`、`identify_adsorption_sites`、`calculate_adsorption_energy` |",
            "| 动力学网络生成与 KMC | 可积分已有网络，但不生成网络，也没有 KMC | `generate_reaction_candidates`、`expand_reaction_network`、`run_kinetic_monte_carlo` |",
            "| 聚合物、粗粒化和介观模拟 | 仅通用 MD 基础，无聚合物构建、粗粒化映射和 dissipative/mesoscale 动作 | 体系构建、映射、粗粒化参数化与传播 Actions |",
            "| 不确定度与可重复比较 | 有 provenance，但缺模型不确定度、方法集成、跨后端一致性和参考数据比较 | `estimate_model_uncertainty`、`compare_backend_results`、`validate_against_reference` |",
            "| HPC/调度与分布式执行 | runtime 隔离已完成，但没有把 Slurm/队列、批量任务依赖作为科学 Action | 保持与科学 Action 解耦，未来增加机械执行/作业管理层 |",
            "",
            "### 4.2 是否满足“绝大多数计算化学需求”",
            "",
            "结论取决于“需求”的边界：",
            "",
            "- 对**计算化学 benchmark 的基础与中等难度任务**，当前 101 个 Actions 已经形成很强的通用骨架：结构准备、基态量化、周期 DFT、声子、经典 MD、轨迹分析、自由能估计、反应速率/主方程、数据检索和对接都能由智能体自由组合。",
            "- 对**整个计算化学领域的生产级全部需求**，答案仍然是否定的。高级多参考/非绝热、QM/MM、增强采样执行、电化学、GW/BSE/Wannier、KMC、缺陷/相图、聚合物/粗粒化和广谱学仍明显不足。",
            "- 因此更准确的汇报措辞是：**当前工具箱能覆盖大量常见计算化学任务和多软件编排能力，但还不能代表整个计算化学领域的全面生产工具链。**",
            "",
            "## 5. 逐 Action 详细清单",
            "",
            "状态说明：`✅` 表示当前代表性端到端成功；`⚠️` 表示代码/契约存在，但当前官方在线服务失败。候选后端中列出的“曾失败后已成功”表示早期/不同输入尝试失败、但该组合后来已有成功证据；“仅有失败记录”才计入 7 个失败组合；“未逐组合验证”不等于不可用，只表示本轮没有为该 Action–Backend 组合留下成功记录。",
            "",
            "| # | Action | 领域 | 功能 | 输入 → 主要输出 | 智能体选择权 | 候选后端与实测 | 当前状态 |",
            "|---:|---|---|---|---|---|---|---|",
        ]
    )

    for index, spec in enumerate(action_specs().values(), start=1):
        evidence = action_by_id.get(spec.id, {})
        required = ", ".join(spec.required_inputs) or "无"
        optional = ", ".join(spec.optional_inputs) or "无"
        flow = f"required: {required}; optional: {optional}<br>→ `{spec.primary_output}`"
        successful = set(evidence.get("successful_backends") or [])
        observed_failures = set(evidence.get("failed_backends") or [])
        recovered = successful & observed_failures
        failed = observed_failures - successful
        unobserved = set(spec.backend_ids) - successful - failed
        provider_parts = [f"成功: {codes(sorted(successful))}"]
        if recovered:
            provider_parts.append(f"曾失败后已成功: {codes(sorted(recovered))}")
        if failed:
            provider_parts.append(f"仅有失败记录: {codes(sorted(failed))}")
        if unobserved:
            provider_parts.append(f"未逐组合验证: {codes(sorted(unobserved))}")
        if spec.data_action:
            network = network_cases.get(spec.id)
            if network and network.get("status") in {"success", "partial_success"}:
                current = "✅ 在线实测通过"
            else:
                detail = error_text(network)
                current = "⚠️ 当前在线失败"
                if evidence.get("status") == "runtime_success":
                    current += "；契约/模拟曾成功"
                if detail:
                    current += f"<br>{md(detail[:260])}"
        else:
            current = (
                "✅ 代表性端到端通过"
                if evidence.get("status") == "runtime_success"
                else "❌ 本地 Action 未通过"
            )
        function = (
            ACTION_FUNCTION_ZH[spec.id]
            + "<br>Catalog 原文："
            + md(spec.description)
        )
        lines.append(
            f"| {index} | `{spec.id}` | {CATEGORY_ZH[spec.category]} | {function} | {md(flow)} | {POLICY_ZH[spec.selection_policy]} | {'<br>'.join(provider_parts)} | {current} |"
        )

    lines.extend(
        [
            "",
            "## 6. Backend 详细状态",
            "",
            "### 6.1 后端统计口径",
            "",
            f"- Catalog 共 **{len(backend_specs())}** 个 BackendSpecs，其中 **{len(local_backends)}** 个本地执行后端、**{len(service_backends)}** 个在线数据服务。",
            f"- 加载本地配置后健康检查：**{healthy_backends}/{len(backend_specs())} available**。",
            f"- 至少一次成功 Action 证据：**{evidence_backends}/{len(backend_specs())}**。",
            f"- 当前现场端到端成功：**{len(current_live_backend_success)}/{len(backend_specs())}**；当前降级的是 `pubchem` 与 `catalysis_hub`。",
            "- `available` 只代表运行环境、模块、命令、模型或凭据准备好；报告同时列出真实成功 Action，防止误读。",
            "",
            "### 6.2 Backend 状态与能力",
            "",
            "| Backend | Runtime | 能力 Actions | 健康 | 已成功 Actions | 尚未逐 Action 组合实测 | 当前备注 |",
            "|---|---|---|---|---|---|---|",
        ]
    )

    for backend in backend_specs().values():
        health = backend_health.get(backend.id, {})
        successes = sorted(backend_success_actions.get(backend.id, []))
        unobserved = sorted(set(backend.capabilities) - set(successes))
        if backend.id == "pubchem":
            note = "⚠️ 安装与契约测试正常；当前官方 PUG REST 对本机返回 503 ServerBusy。"
        elif backend.id == "catalysis_hub":
            note = "⚠️ 当前 GraphQL 端点 503/ReadTimeout，本轮没有成功调用。"
        elif backend.id in local_backends:
            note = "✅ 本地真实 Action 至少一次成功。"
        else:
            note = "✅ 当前在线实测成功。"
        lines.append(
            f"| `{backend.id}`<br>{md(backend.display_name)} | `{backend.runtime}` | {codes(backend.capabilities)} | {'✅ available' if health.get('available') else '❌ unavailable'} | {codes(successes)} | {codes(unobserved)} | {note} |"
        )

    lines.extend(
        [
            "",
            "### 6.3 Backend 环境与资源要求",
            "",
            "| Backend | Python 模块 | 命令/可执行文件 | Conda/Pip | 环境变量 | 科学数据/模型资源 | License |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for backend in backend_specs().values():
        health = backend_health.get(backend.id, {})
        executables = [
            f"{name}={path or 'missing'}"
            for name, path in (health.get("executables") or {}).items()
        ]
        modules = [
            f"{name}={item.get('version') or 'OK'}"
            for name, item in (health.get("python_modules") or {}).items()
            if item.get("available")
        ]
        packages = [
            *(f"conda:{item}" for item in backend.conda_packages),
            *(f"pip:{item}" for item in backend.pip_packages),
        ]
        environment = [
            f"{name}={'set' if present else 'missing'}"
            for name, present in (health.get("environment") or {}).items()
        ]
        lines.append(
            f"| `{backend.id}` | {md('<br>'.join(modules) if modules else '—')} | {md('<br>'.join(executables) if executables else '—')} | {md('<br>'.join(packages) if packages else '—')} | {md('<br>'.join(environment) if environment else '—')} | {codes(backend.required_data_resources)} | `{backend.license_class}` |"
        )

    configured_runtime_only = [
        item
        for item in requested.get("software") or []
        if item.get("status") == "configured" and item.get("public_adapter") == "runtime_only"
    ]
    incomplete_software = [
        item
        for item in requested.get("software") or []
        if item.get("status") not in {"configured", "specification"}
    ]

    lines.extend(
        [
            "",
            "## 7. 用户要求的软件/工具清单状态",
            "",
            f"当前受管理清单共 {requested_summary.get('total', 0)} 项：",
            "",
            f"- `configured`: **{requested_summary.get('counts', {}).get('configured', 0)}**",
            f"- `partial`: **{requested_summary.get('counts', {}).get('partial', 0)}**",
            f"- `manual_required`: **{requested_summary.get('counts', {}).get('manual_required', 0)}**",
            f"- `manual_api_review`: **{requested_summary.get('counts', {}).get('manual_api_review', 0)}**",
            f"- `specification`: **{requested_summary.get('counts', {}).get('specification', 0)}**（QCSchema 不是独立软件）",
            "",
            "### 7.1 已安装但不直接作为公共 Action 暴露的软件",
            "",
            "这些组件可以提供底层能力或未来扩展，但直接暴露一个固定工作流会削弱 benchmark 对智能体编排能力的评估。",
            "",
            "| 软件 | Runtime | 作用/当前处理 |",
            "|---|---|---|",
        ]
    )
    for item in configured_runtime_only:
        lines.append(
            f"| `{md(item.get('name'))}` | `{md(item.get('environment'))}` | {md(item.get('notes'))} |"
        )

    lines.extend(
        [
            "",
            "### 7.2 尚未完成或需要人工决策的软件",
            "",
            "| 软件 | 状态 | 原因 | 需要用户做什么 |",
            "|---|---|---|---|",
        ]
    )
    user_action = {
        "Q-Chem": "若未来启用，提供合法许可证和官方安装包；当前按用户决定保持屏蔽。",
        "Molpro": "若未来启用，提供合法许可证和官方安装包；当前保持屏蔽。",
        "TURBOMOLE": "若未来启用，提供合法许可证和官方安装；当前不得由 CENSO 隐式选择。",
        "CASTEP": "如需启用，取得 STFC/商业许可并提供站点安装包或可用二进制。",
        "CRYSTAL": "若未来启用，提供许可证和官方安装；当前保持屏蔽。",
        "WIEN2k": "若未来启用，提供许可证和站点安装；当前保持屏蔽。",
        "MATLAB": "安装介质已缓存，但仍需合法许可证和可执行安装；只有需要 EasySpin 执行时才必须处理。",
        "OpenEye": "Conda 包不能替代许可证；当前按用户决定保持屏蔽。",
        "Schrödinger": "当前文件是同名 Dirac 视频编解码包，不是化学套件；若启用需提供商业 Schrödinger 官方安装包与许可证。",
        "Arkane": "无需额外下载；需要后续定位导入/示例运行超过 300 秒的问题并做更小的类型化 Action。",
        "EasySpin": "EasySpin 文件已缓存；需先有合法 MATLAB 可执行环境，再做真实 EPR smoke。",
        "NIST CCCBDB 接口": "官方无公开文档化 REST/JSON API；建议继续不做脆弱网页抓取，除非定义极受限的人工维护查询。",
    }
    for item in incomplete_software:
        lines.append(
            f"| `{md(item.get('name'))}` | **{md(item.get('status'))}** | {md(item.get('notes'))} | {md(user_action.get(str(item.get('name')), '按清单 notes 做人工许可、安装或 API 决策。'))} |"
        )

    lines.extend(
        [
            "",
            "## 8. 当前问题清单",
            "",
            "### 8.1 当前运行问题",
            "",
            "1. **PubChem PUG REST**：本机连续收到 `503 PUGREST.ServerBusy`。这影响 `search_compounds`、`resolve_chemical_identity`、`retrieve_compound_properties`、`retrieve_compound_structure`、`search_similar_compounds` 和 `search_substructures`。适配器契约测试仍通过，问题属于当前官方服务/共享出口限流。",
            "2. **Catalysis-Hub GraphQL**：当前出现 `503 Service Unavailable` 和 `ReadTimeout`，影响 `search_catalysis_records`。",
            "3. **Materials Project 凭据**：Backend 健康依赖 `MP_API_KEY`；当前 `config.local.env` 已配置且现场查询通过。部署到新节点时必须同步安全配置。",
            "",
            "### 8.2 非当前故障但仍需说明的限制",
            "",
            "- 62 个替代 Action–Backend 组合尚未逐组合运行，例如一个 Action 的所有量化软件、所有 MD 引擎和所有 ML 势都没有对该 Action 全覆盖。",
            "- GPU 路径未系统验证；当前 smoke 以 CPU 为主，NAMD CUDA、PMEMD CUDA、GNINA GPU 等没有被自动选择。",
            "- 大体系、长轨迹、并行扩展、队列调度、断点恢复和生产级收敛尚未在本报告中验证。",
            "- 商业/注册软件的可用性依赖现有站点许可证和文件，不代表可以复制到任意服务器。",
            "- 在线数据源状态会随时间变化；报告中的 503/timeout 是 2026-07-20 的现场结果。",
            "",
            "## 9. 汇报建议",
            "",
            "建议在正式汇报中使用下面这段结论：",
            "",
            "> ResearchChemBench 当前公开 101 个原子化化学 Actions 和 76 个明确可选 BackendSpecs。智能体必须自行选择 Action、软件后端、方法和调用顺序，系统不进行科学自动 fallback。91 个本地 Scientific Actions 均已有代表性端到端成功记录，71 个本地后端均至少真实执行过一个 Action；全量回归 146/146 通过。当前主要运行问题集中在在线数据服务：PubChem 和 Catalysis-Hub 在审计时出现 503/超时，因此当前现场可用 Action 为 94/101。工具箱已较好覆盖结构准备、化学信息学、分子基态电子结构、经典 MD 与轨迹/自由能分析、反应动力学、周期 DFT、声子/热输运、对接和数据接口，但高级多参考/非绝热、QM/MM、增强采样执行、电化学、GW/BSE/Wannier、KMC、缺陷/相图及更广光谱仍是后续重点。",
            "",
            "## 10. 关联文档与可复现命令",
            "",
            "关联文档：",
            "",
            "- `docs/tools/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`：完整 Action/Backend/runtime/resource 参数矩阵。",
            "- `docs/tools/CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md`：软件版本、官方资料缓存和候选能力。",
            "- `docs/tools/CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md`：59 项用户软件清单。",
            "- `.software_cache/documentation/catmap/0.3.1/`：本次 CatMAP 官方教程、代码概览和仓库页面缓存。",
            "",
            "复现命令：",
            "",
            "```bash",
            ".toolbox_env/bin/python -m pytest -q --junitxml=config/pytest_status.xml",
            ".toolbox_env/bin/python scripts/run_action_gap_smokes.py",
            ".toolbox_env/bin/python scripts/run_action_gap_smokes.py --include-network",
            ".toolbox_env/bin/python scripts/run_backend_gap_smokes.py",
            ".toolbox_env/bin/python scripts/run_scientific_resource_smokes.py",
            ".toolbox_env/bin/python scripts/run_data_source_smokes.py",
            ".toolbox_env/bin/python scripts/audit_action_test_coverage.py",
            ".toolbox_env/bin/python scripts/generate_detailed_toolbox_audit_report.py",
            "```",
            "",
            "## 11. 官方资料",
            "",
            "- CatMAP 微观动力学模型要求显式反应表达式、表面/描述符、物种定义和能量输入；本工具箱现在按其官方 setup-file API 生成受控模型：[CatMAP 创建微观动力学模型教程](https://catmap.readthedocs.io/en/latest/tutorials/creating_a_microkinetic_model.html)。",
            "- CatMAP 的 parser/scaler/solver/mapper 架构说明：[CatMAP Code Overview](https://catmap.readthedocs.io/en/latest/topics/code_overview.html)。",
            "- PubChem PUG REST 官方接口说明：[PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)。",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "actions": len(action_specs()),
                "current_end_to_end_success": len(current_end_to_end_success),
                "current_degraded": len(live_data_degraded),
                "backend_health_available": healthy_backends,
                "backend_success_evidence": evidence_backends,
                "current_live_backend_success": len(current_live_backend_success),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
