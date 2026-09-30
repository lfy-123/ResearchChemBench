# 已批准修复记录（2026-09-23）

授权：负责人同意 MAINTENANCE_REPORT 第 15 节方案及 D1–D7。正文/SI 为主，验证计算为辅；只在 verified_tasks 修复，无新量化计算、无迁移授权。

已将 dbc_ph_s0.xyz 替换为拓扑独立生成的未优化初始结构，原作者终态存 evaluation/author_results/dbc_ph_s0.xyz；原子映射与电荷、连接性保持。未使用作者坐标、扭角/距离约束或能量排名生成新起点；未新增量化计算。

已将 dbc_nap_s0.xyz 替换为拓扑独立生成的未优化初始结构，原作者终态存 evaluation/author_results/dbc_nap_s0.xyz；原子映射与电荷、连接性保持。未使用作者坐标、扭角/距离约束或能量排名生成新起点；未新增量化计算。

已按批准方案分离 PR guidance，取消普通 limitation/停止表态的 required 和独立得分，显式采用 scientific_results 策略；保留真实失败诊断、对象/态/收敛/敏感性证据与原科学数值容差，修复已发现的 [] 选择器并接回必要关键点。

收尾复查：修复清理后的残句及“失败也称 complete”矛盾；保留主结果要求，提供不必虚构数值/结构的早期失败格式。针对主对象重复/缺失与成功状态做契约检查；普通免责声明不作为必需字段或成果。

计算档案已补成有效链、源方法/验证差异、原始输入输出和当前 2 个关键点/1 条科学结论对应；不把 reference 变成 evaluator、不写入虚构计算。

## 2026-09-23 二次回查：定义与提交契约修复

SI pp11/13 Tables S5/S7 分别列出 Ph/Nap 在 S0 和 S1 优化几何的 5 个 singlet TD 根，而不是 S1→Sn 激发态吸收。删除未定义的“requested window”替代条件，明确两几何各至少根 1–5。schema 的 validated 分支补两几何/根唯一性覆盖，partial/failure 分支保持可提交，不用缺失值凑成功。真实历史记录 Ph 的 S0/S1 为 10/5 根，Nap 为 10/10 根，已有计算足够；未新添计算目标。

本次只澄清既定科学子目标，不改数值 target/tolerance、不增加 limitation 评分；未重算、未运行 LLM judge、未迁移目录。

## 2026-09-24 成功分支证据契约修复

依据正文 PDF p6/Fig.5、SI pp11/13 的态/轨道分析要求及 group_2 真实结果复核：原 validated 分支仍接受仅含 failure_report 的 orbital_evidence，或空白的轨道/态证据。本次只在 validated 条件下要求 criterion、HOMO、LUMO 及 S0/S1 evidence 为含非空白字符的字符串；轨道缺失仍可提交 bounded_failure 和已有部分结果，额外失败尝试不影响完整主结果。

历史两分子的完整轨道和态证据仍可按原科学数值提交；未固定 population 算法或要求新增轨道百分比。非空格式不等同证据有效，科学判定仍依原 evaluator。未改 task 科学要求、评分目标/容差或 reference，未新算、迁移。定向测试见仓库 tests/test_verified_task_contract_repairs_20260924.py；本轮结果集中记于 MAINTENANCE_REPORT.md 第19节。
