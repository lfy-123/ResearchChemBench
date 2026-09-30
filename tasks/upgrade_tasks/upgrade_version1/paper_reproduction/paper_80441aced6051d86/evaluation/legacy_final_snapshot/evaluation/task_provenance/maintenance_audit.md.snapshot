# 已批准修复记录（2026-09-23）

授权：负责人同意 MAINTENANCE_REPORT 第 15 节方案及 D1–D7。正文/SI 为主，验证计算为辅；只在 verified_tasks 修复，无新量化计算、无迁移授权。

已将 g1_monomer.xyz 替换为拓扑独立生成的未优化初始结构，原作者终态存 evaluation/author_results/g1_monomer.xyz；原子映射与电荷、连接性保持。未使用作者坐标、扭角/距离约束或能量排名生成新起点；未新增量化计算。

已将 g1_dimer.xyz 替换为拓扑独立生成的未优化初始结构，原作者终态存 evaluation/author_results/g1_dimer.xyz；原子映射与电荷、连接性保持。未使用作者坐标、扭角/距离约束或能量排名生成新起点；未新增量化计算。

已按批准方案分离 PR guidance，取消普通 limitation/停止表态的 required 和独立得分，显式采用 scientific_results 策略；保留真实失败诊断、对象/态/收敛/敏感性证据与原科学数值容差，修复已发现的 [] 选择器并接回必要关键点。

水介质已公开；AR 目标改为中立问法；明确平面投影与全质心距离区别。主结果与失败尝试可共存，频率未完成可如实 null；complete 仍要求全部观测。作者优化结果作为现有几何描述符的私有参照，未新增 RMSD 打分。

收尾复查：修复清理后的残句及“失败也称 complete”矛盾；保留主结果要求，提供不必虚构数值/结构的早期失败格式。针对主对象重复/缺失与成功状态做契约检查；普通免责声明不作为必需字段或成果。

计算档案已补成有效链、源方法/验证差异、原始输入输出和当前 4 个关键点/1 条科学结论对应；不把 reference 变成 evaluator、不写入虚构计算。

末轮回查删除仍残留在 expected/statement 的必写免责声明措辞；失败说明不再与成功最低点/排序结果等价。保留真实科学量、必要验证和部分过程证据。

## 2026-09-23 二次回查：定义与提交契约修复

正文 p3–4 的单体扭转/二聚体堆积仍为科学目标；group_4/finalize_paper_804.py:124–153 的实际验证使用 SVD 最小二乘平面及 acos(abs(dot)) 急角，原题面却允许任意 dihedral 定义。现公开原子环集合与主测量口径，保留既有 target/tolerance。task 曾承诺 inline coordinates，而 complete schema 只接收 structure_path，现统一为非空文件路径；不新增坐标格式分支。二聚体 slip 仍是质心向量与平均平面的急角，不改为法线角。独立 starter 和私有作者结果均未改。

本次只澄清既定科学子目标，不改数值 target/tolerance、不增加 limitation 评分；未重算、未运行 LLM judge、未迁移目录。
