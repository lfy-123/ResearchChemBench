# Stage06/07 v5 Round 9：代表性复核与 Prompt 修正计划

日期：2026-08-22  
回归目录：`runs/stage06-07-v5-round8-deepseek10-concurrency10-20260822`  
模型/Harness：DeepSeek-v4-pro-0813 / Codex / high / 并发 10

## 1. 终态与代码侧结论

本批次 10 篇全部正常终态，10/10 `approved_with_repairs`，10/10 通过
`mechanical_pre_publish` 和 published-bundle 检查，10/10 published；没有
`mechanical_publish_blocked`、schema-load failure、objective failure 或 429。Stage07B
没有触发条件：没有出现“科学批准后因同类简单机械合同问题重复阻断”的样本。

代码侧的 159 个 Stage06/07 回归测试继续为 `159 passed`。因此本轮没有发现新的
确定性 transport/gate bug，也没有修改机械 gate。

## 2. 逐篇科学代表性复核

| paper | 终态选择 | 对论文计算主线的复核 | 判断 |
|---|---|---|---|
| `10679580b3d561b4` | full-paper core | Ni(111) 有/无 adatom 的完整 DFT 机制比较覆盖论文计算主张；实验 Fe/steel 不是计算路线 | A，合理 |
| `1d169922882bb51a` | [010] Li+/polaron 耦合动力学子流程 | 直接覆盖标题/摘要的 ion-polaron synergy 和 rate-determining step；稳定性、容量和 AIMD 是独立外围分支 | B，合理 |
| `2f302589e5e9e420` | full computational core | 优化、偶极、ESP、分子内氢键共同闭合介电下降机制 | A，合理 |
| `33b0755b4819d475` | 2,2′-linked Figure 3 子流程 | 任务闭合，但论文标题/摘要/结论的最高中心性是 8,8′-linked、BINOL/DBINOL 增强的 triplet photosensitization；选中的 2,2′ 分支是基线/对照性质，Stage07 没有充分解释为何它高于 8,8′ 主线 | C，需重选或证据支持 |
| `3ff745491bb60f01` | full DFT HOMO–LUMO core | 论文唯一计算机制主张是 probe→product 的 gap/localization；实验 sensing 不属于计算范围 | A，合理 |
| `557c6f813c2ec1ad` | intermolecular reduced PCET 子流程 | 论文摘要和结论明确强调 intramolecular PB-Rhodol 的 one-electron/proton-transfer 及效率提升；Stage06/07 选择了坐标更容易的 intermolecular branch，未证明它是最高中心性子问题 | C，需优先核查 PB-Rhodol；若其闭合不可恢复，应科学拒绝而不是用较外围分支替代 |
| `814f98ceae0df938` | full VASP activation/adsorption core | 覆盖 vacancy/O2 activation 和 phenol/p-BQ adsorption 三个计算主张；来源几何不足被正确标为 non-blocking | A，合理；元数据标题仍需修复 |
| `c95823ea55103c23` | facet-dependent ethylene→EG RDS 子流程 | 直接支撑标题/摘要中的 facet selectivity 和 RDS；Mn oxidation/phosphate 分支有明确遗漏理由和较弱输入闭合 | B，合理 |
| `db423ba23faa1ee4` | Cu-methoxide 1,4-addition TS 子流程 | Scheme 5c 是 active-nucleophile 机制的闭合核心；indole control、失败搜索、平衡和重排是分立支撑 | B，合理 |
| `e6a39f88c25d4cfa` | A-c/A-o quinuclidine donor-affinity 子流程 | 该支路支持 Lewis-base release，但标题/摘要/结论的最高中心性是 photoswitchable Lewis-acid catalysis、gLA/eLA 和催化 reaction profile；FIA/Diels–Alder 主线没有进入选定任务 | C，需重选或在源数据不足时拒绝，不能仅因 donor route 易闭合而接受 |

初步科学代表性为 7/10 基本符合 A/B，3/10 有 C 级风险。这里不是要求所有任务都批准；如果 33、557 或 e6 的真正最高中心性计算路线无法在不猜测科学事实的条件下闭合，正确结果应是科学拒绝，而不是发布较容易包装的外围任务。

## 3. 其他可重复问题

两篇已发布任务的 `paper_info.title` 仍不可靠：

- `814f98ceae0df938` 写成 `Supporting Information`，而主文标题是
  `Piezocatalytic oxidation of lignin-derived phenol to p-benzoquinone...`；
- `e6a39f88c25d4cfa` 写成 MinerU 图片标记，而主文标题是
  `Photoswitching Lewis Acid Catalysis with Highly Fatigue Resistant Photochromic Boronates`。

这不是科学 scope 或 mechanical gate 问题，但说明 Stage07 目前只在部分样本中主动修复 provenance metadata。应在通用科学审计 Prompt 中明确要求用主文 evidence 校验 title/DOI/journal，修复 SI 标题、viewer boilerplate、图片标记等 malformed metadata。

软件方面本批 10 篇均为 `available`，没有样本能检验“所需程序不在 toolbox 时登记而不拒绝”的负向路径；当前代码和 Prompt 没有把缺软件当科学拒绝，保持目标要求。

自主公共面、route evidence map、mode-specific binding 和 mechanical reports 在 10 篇中均未发现新的共性泄漏或合同阻断；Stage07 对 3ff、c958、e6 等样本已经实际修复了字段、输入和答案泄漏。

## 4. 根因归类

1. 33/557/e6 的问题不是代码能用关键词确定的规则，而是 Stage06A/Stage07 没有把标题、摘要、结论中的最高中心性计算主张形成一张强制的比较证据表；模型更偏向选择坐标和数据最容易闭合的支路。
2. 现有 Prompt 已要求“比较 title/abstract/main figures/conclusions”，但没有明确禁止“最高中心性 claim 未覆盖时以另一个闭合但较低中心性支路替代”，也没有要求在该情况下给出科学拒绝或 workflow redesign。
3. `paper_info` 标题校验没有成为 Stage07 的明确审计项；这是通用 provenance/prompt 缺口，不应增加论文特例代码。

## 5. Round 9 修改计划

只修改通用 Prompt，不增加 paper/molecule/固定答案规则：

1. Stage06A 的 `representativeness_review` 增加“headline/primary/supporting”中心性标注要求；候选必须说明是否直接覆盖最高中心性计算主张，以及是否只是 baseline/control/secondary/application 支路。
2. Stage06A 明确：若完整路线不可用，最高中心性子流程也无法闭合，则写科学失败；不得用可闭合但较外围支路提高通过率。
3. Stage07 增加独立 headline-claim closure 检查：必须从标题/摘要/结论和主图得到中心性主张，逐候选比较；若选定 scope 不覆盖最高中心性主张，只有在证据证明该主张路线不可恢复时才能接受，并须记录 `rejected_or_unconstructible_central_scope` 或 workflow redesign，而不是默认批准。
4. Stage07 增加通用 `paper_info` provenance 检查：以 main-paper evidence 校验 title、DOI、journal；SI heading、viewer boilerplate 和 image-markup 不能作为论文标题。
5. 不修改 mechanical gate，不引入科学中心性代码评分，不启用 Stage07B。

Round 9 修改后先跑 Stage06/07 单测，再重新随机抽取 10 篇 Stage05 论文做 DeepSeek 回归；逐篇检查上述三类 C 风险是否被重选/拒绝/有证据接受，以及错误标题是否消失。
