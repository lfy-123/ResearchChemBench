# 已批准修复记录（2026-09-23）

授权：负责人同意 MAINTENANCE_REPORT 第 15 节方案及 D1–D7。正文/SI 为主，验证计算为辅；只在 verified_tasks 修复，无新量化计算、无迁移授权。

已按批准方案分离 PR guidance，取消普通 limitation/停止表态的 required 和独立得分，显式采用 scientific_results 策略；保留真实失败诊断、对象/态/收敛/敏感性证据与原科学数值容差，修复已发现的 [] 选择器并接回必要关键点。

收尾复查：修复清理后的残句及“失败也称 complete”矛盾；保留主结果要求，提供不必虚构数值/结构的早期失败格式。针对主对象重复/缺失与成功状态做契约检查；普通免责声明不作为必需字段或成果。

计算档案已补成有效链、源方法/验证差异、原始输入输出和当前 4 个关键点/1 条科学结论对应；不把 reference 变成 evaluator、不写入虚构计算。

末轮回查删除仍残留在 expected/statement 的必写免责声明措辞；失败说明不再与成功最低点/排序结果等价。保留真实科学量、必要验证和部分过程证据。

## 2026-09-24 Cy2 能量判据与作者/验证路线归属修复

负责人批准末轮建议后，直接核读正文 PDF pp5–6、SI §2.8 与 Table S3：正文 2T1>S1 对象是 rubrene 湮灭剂；Cy2 用 S1−T1、T2−S1 态间距讨论 ISC，单分子四能量本身不能测定增强 SOC/ISC。旧 task 将两者串联、PR 结论泛称检验 heavy-atom 增强，确有对象/解释歧义。

两模式现保留四个能量、原状态/收敛要求及全部数值容差，解释统一为 Cy2 态序与能隙；2T1−S1 仅可选诊断、不独立计分，不要求算 rubrene/SOC/速率，也不增加 limitation 声明。同步 task、schema 字段描述、最终结论及规则、evidence_map、reference；PR task_info 同步。AR 未加入作者机理或数值答案。S1−T1=.8354、T2−S1=.2311 eV 仅是既有能量相减，无新量化步骤或新阈值。

关联核查同时发现 paper_route 的 Authors' implemented route 把本地 TD triplet-root 写成作者方法，现依正文改回 UDFT，并另段准确记本地 TD(Triplets,Root=1) 为方法开放任务允许的验证路线。历史 group results.json 解释保留只读，不能作为 Cy2 证明 rubrene 条件的依据；其实际能量、频率/态身份等有效证据继续使用。测试与版本见 MAINTENANCE_REPORT.md 第20节；无新增量化计算，无目录迁移。
