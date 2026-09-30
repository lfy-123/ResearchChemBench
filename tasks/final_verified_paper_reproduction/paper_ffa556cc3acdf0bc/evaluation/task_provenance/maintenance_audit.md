# 已批准修复记录（2026-09-23）

授权：负责人同意 MAINTENANCE_REPORT 第 15 节方案及 D1–D7。正文/SI 为主，验证计算为辅；只在 verified_tasks 修复，无新量化计算、无迁移授权。

已按批准方案分离 PR guidance，取消普通 limitation/停止表态的 required 和独立得分，显式采用 scientific_results 策略；保留真实失败诊断、对象/态/收敛/敏感性证据与原科学数值容差，修复已发现的 [] 选择器并接回必要关键点。

已公开四个构象的 30 碳实验标签映射，仅提取基于正文 Fig.1/SI 图连接和楔键的身份表，不公开 NOESY 距离、NMR 计算值、概率或胜者。

收尾复查：修复清理后的残句及“失败也称 complete”矛盾；保留主结果要求，提供不必虚构数值/结构的早期失败格式。针对主对象重复/缺失与成功状态做契约检查；普通免责声明不作为必需字段或成果。

计算档案已补成有效链、源方法/验证差异、原始输入输出和当前 3 个关键点/1 条科学结论对应；不把 reference 变成 evaluator、不写入虚构计算。

## 2026-09-24 输入简介与四构象实物同步

SI supplementary_002 PDF p5/Table S2、pp12–13 方法和 pp26–32 构象，配合当前四份 XYZ/碳映射及已有 NMR 验证，确认是两种相对构型候选、各两个构象。本次仅把 task_info.data[0].description 改成“两候选各两构象，共四份完整 XYZ”，未增加或替换任何结构、实验位移、碳标签、概率或胜者信息。原输入完整，评分和成功计算不变；无新增计算或迁移。测试及本轮结果见 MAINTENANCE_REPORT.md 第19节。

## 2026-09-24 成功计算档案的依赖和主校准澄清

复核 SI S12–13 的作者路线、group_4 原生父几何配对和 AUTHOR_NMR_CLOSURE_20260918.md，并直接读取 dp4_results.json：四个 B3LYP 最低点为既有结果复用，不能写成从后来 M06 筛查结果重新依次计算；主校准是 DP4+ 方法软件参数库 CHCl3/mPW1PW91 对应 TMS 188.48755 ppm，自算 189.1954 ppm 只作敏感性。author_standard_computed 的 E/G 分支分别给 B 概率 99.999956799%/99.999937279%，原 reference 主概率真实，并非数值错误。

仅澄清 verified_computation_reference.md 的有效依赖、权重、主/对照校准及原始证据链接；task、全部公开输入、schema、五个 evaluator JSON 不变。没有把对照输出包装成主链，没有新增 QM、改构型答案或制造新的评分门槛。检查与版本见 MAINTENANCE_REPORT.md 第20节。
