# Stage00-03 筛选审计报告（2026-08-08）

## 1. 结论

本轮 Stage03 已从“几乎把所有论文判为混合实验”修正为可用于高精度纯计算论文门控的版本。350 篇中
最终保留 16 篇纯计算论文，人工逐篇复核未发现误放行；旧版本误杀的 14 篇纯计算论文被恢复。当前低
通过率主要由样本期刊分布和“论文级纯计算”目标造成，不应简单解释为 Stage03 仍然过严。

仍有两个高优先级风险：Stage02 允许已知 SI 解析失败的论文继续进入 Stage03；Stage03 尚无独立人工
标注集，因此当前只能证明通过集的观测 precision 较高，不能给出可靠 recall。

## 2. 数据范围

本报告分析的是中止旧全流程后已经完成的部分，而不是全部 500 篇：

| 阶段 | 输入/产物 | 结果 |
|---|---:|---|
| Stage00 | 500 篇 | 正文 500；432 篇远端已有 SI；68 篇远端未配 SI |
| Stage01 | 500 篇 | 440 篇有 SI；4 篇确认无 SI；55 篇获取错误；1 篇 SI 不可用 |
| Stage01 pass | 444 篇 | 56 篇不确定状态被保守 hold |
| Stage02 已执行 | 350/444 篇 | 350 篇正文全部通过；其余 94 篇因任务被停止而尚未处理 |
| Stage03 | 350 篇 | 全部完成，无 processing error |

Stage00 的 500 篇并不是计算化学期刊样本。前五个期刊占 441/500（88.2%）：JACS 157、Angewandte
133、Chemical Science 68、ACS Catalysis 52、Green Chemistry 31。这个分布天然包含大量实验主导或
实验-计算混合论文。

Stage01 的 56 篇 hold 也存在出版社偏差，其中 Angewandte 24 篇、Chemical Science 9 篇、Accounts of
Chemical Research 7 篇。网络/反爬失败没有被错误解释成“确认无 SI”，这一点是正确的，但仍会改变进入
下游的期刊分布。

## 3. Stage02 审计

已处理 350 篇的正文解析结果：

- GROBID：347/350；
- `pdftotext` 回退：3/350；
- 正文失败：0；
- 正文字符数中位数约 33,061，最少 7,002。

368 个 SI/附件的结果：

- GROBID：360；
- `pdftotext`：3；
- archive 结构化抽取：1；
- 解析失败：4；
- 成功率：364/368（98.91%）。

问题在于 4 个 SI 失败后，对应 paper bundle 仍标为 pass。它们在本轮 Stage03 中均因正文或其他 SI
明确包含作者实验而被淘汰，没有形成实际误放行；但该行为存在确定的未来风险：如果作者实验或关键
计算信息只存在于失败 SI，Stage03 会在不完整证据上作出论文级结论。

建议将 Stage02 输出增加 `document_completeness`：

- `complete`：正文及所有已知 SI 均成功；
- `confirmed_no_si`：Stage01 已确认无 SI，且正文成功；
- `incomplete_known_document`：任何已知正文/SI 解析失败；
- `unknown_assets`：Stage01 的补充材料状态仍不确定。

Stage03 只允许前两类进入；后两类 hold/retry。不能用“正文解析成功”替代“论文证据包完整”。

## 4. Stage03 修改与结果

### 4.1 修改

Stage03 r6/r7 做了以下调整：

1. prompt 明确区分当前作者实验、当前作者计算和外部实验数据，并加入 DFT、MD、声子、外部 PDB/XFEL、
   实验数据库、NMR 和合成的正反例；
2. 只有原文 quote 可回映且通过实验语义规则的证据，才允许证明作者做了实验；
3. 模型声称有实验但没有验证证据时进入 uncertain retry，不能直接淘汰；
4. 达到输出 token 上限的修复 JSON 不再直接使用，必须 compact/essential retry 得到完整响应；
5. 在 block 和 UTF-8 分段两层清除原子坐标，同时保留坐标前后的自然语言；
6. LCA/流程模拟、组学/序列分析、既有动物实验数据的数字化/统计/因果推断等非目标计算，在没有
   DFT、MD、QM/MM 等目标证据时归为 `computational_content_not_found`。

### 4.2 最终分布

| 决策 | 数量 | 比例 | 含义 |
|---|---:|---:|---|
| `computational_content_confirmed` | 16 | 4.57% | 原创、计算 primary、流程完整、无作者实验 |
| `not_pure_computational` | 267 | 76.29% | 有目标计算，但作者也完成了实体实验 |
| `computational_content_not_found` | 66 | 18.86% | 没有目标分子/材料计算流程 |
| `background_only` | 1 | 0.29% | 只有背景信息 |
| processing error / uncertain | 0 | 0% | 无未决记录 |

267 篇混合论文中，212 篇的计算是 primary，55 篇是 supporting。它们中的很多确实具有完整 DFT/MD
流程，但同时有作者合成、NMR、XPS、电化学或催化测试。按本项目当前“纯计算论文”定义，淘汰正确；
“计算流程完整”不等于“整篇论文纯计算”。

期刊分布进一步说明了样本偏差：ACS Catalysis 6/41 通过，Chemical Science 3/47，JACS 5/118，
Angewandte 1/88；Green Chemistry、Nature Chemistry 和 Nature Catalysis 本批均无纯计算通过项。

## 5. 筛选准确性审计

### 5.1 通过集

16 篇通过项已逐篇检查 Stage02 正文/SI、Stage03 计算证据和作者实验反证：

- 16/16 均为 `original_research`、`computation_role=primary`、`workflow_complete=yes`；
- 16/16 均有完整的模型/结构、实际计算操作和化学结果证据；
- 16/16 的正文和 SI 均解析成功；
- 16/16 均无验证后的作者实验引用。

覆盖的方法包括 DFT/从头算/MD、NEO-DFT、VASP 声子和能带、QM/MM、MLIP-MD + NEB、metadynamics、
ai-GCMC、GW-BSE 和基于 DFT 数据的材料模型。人工审计期间发现并修正了 1 个误放行：该论文只对既有
动物纳米毒性实验数据做随机森林、因果推断和粒子群优化，不属于目标计算化学。

因此当前通过集的观测 precision 为 16/16；样本太小，不能把它解释为总体 precision=100%。

### 5.2 混合集

267 篇 `not_pure` 全部至少有一条可回映原文的作者实验引用。对风险最高的子集进一步检查：

- 仅有 1 条实验引用的 3 篇分别为称量/制备竹粉、XPS 实测、GC/MS 实测，均为真实作者实验；
- 28 篇没有命中简单“measured/recorded/synthesized”动作正则，但其证据包含明确实验步骤、仪器、
  本文图谱或测试条件，抽查未发现把 DFT/MD/外部数据当作作者实验的旧错误。

剩余风险是引用归属而非计算/实验概念混淆。当前外部证据正则对整句生效，例如“we synthesized X using
a previously reported procedure”可能因为 `previously reported` 被错误视为外部实验；反过来，只有图注
而缺少动作主体时仍较依赖 LLM 的 `this_paper` 归属判断。

### 5.3 无目标计算集

对 67 篇 `not_found/background_only` 的 GROBID 全文重新搜索 DFT、MD、QM/MM、VASP、Gaussian、ORCA、
CP2K、GROMACS 等强信号：

- 60 篇完全没有强信号；
- 7 篇有 1--3 次命中，逐条检查后分别是前人 DFT 引用、NLDFT 孔径分析、Gaussian 曲线拟合、英文
  “molecular dynamics”泛指、或 SI 图注中的常规 DFT 孔径计算；
- 未发现当前作者实际完成目标计算却被归为 `not_found` 的样本。

这项反查降低了明显漏筛的风险，但无法发现没有常见软件/方法词的自定义计算工作流，因此 recall 仍未
被正式测量。

### 5.4 与旧版本比较

同一批 300 篇重叠样本中：

- 1 篇旧通过项继续通过；
- 14 篇从旧 `not_pure` 恢复为纯计算；
- 55 篇从笼统 `not_pure` 修正为无目标计算；
- 228 篇仍为混合计算实验；
- 2 篇旧 `not_found` 保持淘汰（其中 1 篇细分为 background only）。

旧版约 47.3% map 响应达到 token 上限；新版 4,641 次首轮 map 中 48 次截断（1.03%），均经重试或
坐标过滤恢复。350 次 reduce 中 2 次截断，均 compact retry 成功。完整 Stage03 运行约 56 分钟，首轮
map 输入约 18.3M tokens；准确性改善明显，但吞吐仍有优化空间。

## 6. 当前问题与解决优先级

### P0：证据包完整性门控

Stage02 必须阻止任何已知文档解析失败的论文进入 Stage03。为 OCR 型 SI 增加 MinerU/OCR 重试；压缩包、
表格等结构化附件应有类型专用解析器。只有 `complete` 或 `confirmed_no_si` 才能作纯计算结论。

### P0：建立独立人工标注集

当前没有 recall 指标。建议冻结至少 200 篇标注集，并与 prompt 开发集分离：包含全部当前通过项、实验
证据较弱的边界项、强计算关键词但被淘汰的论文、非目标 ML/LCA/bioinformatics，以及不同期刊随机
样本。标签至少包括 `pure/mixed/no_target`、计算 role、作者实验归属和关键 quote。发布前以通过集
precision 为首要指标，目标不低于 95%；recall 单独报告，不用低 recall 换取错误通过。

### P1：Stage00 采样改为“富集但不硬筛”

随机从当前综合/实验期刊抽样导致每 350 篇只产出 16 篇。应在 Stage00 增加可复现的分层/加权采样：

- 如果远端存在计算化学期刊，按期刊和年份设独立配额；
- 使用标题、摘要、主题词和历史 Stage03 结果计算 enrichment score；
- 保留一部分随机样本用于估计总体分布，不能只采高分论文；
- enrichment 只改变处理优先级，不作为不可审计的硬淘汰条件。

### P1：作者实验归属采用结构化证据规则

把简单外部关键词正则改为子句级判断：同时记录 subject（we/authors/prior work）、action、object、来源
段落和时态。单条图注或弱引用不应独立淘汰；可以要求一条强 Methods/Experimental 过程证据，或两条
相互独立的弱证据。明确的当前作者动作应优先于“following a reported method”等方法来源短语。

### P1：非目标计算使用固定 taxonomy

当前已经从 prompt 转向 prompt + 确定性规则，但继续追加正则会逐渐脆弱。建议让 map 输出受控
`target_family`：quantum chemistry、atomistic simulation、reaction/kinetics、computed-data ML 等；
另列 experimental-data statistics、bioinformatics、LCA/process、instrument analysis。代码按 enum 和
证据校验，不让 LLM 自由创造方法类别。未知类别进入 review，不由模型常识自动放行。

### P1：缓存显式包含实现版本

微批 hash 当前主要依赖 prompt version。坐标过滤、证据清洗和确定性决策规则变化也会改变结果，应新增
`STAGE03_IMPLEMENTATION_VERSION` 并加入 stage hash，避免非 prompt 代码升级后错误复用旧产物。

### P2：降低 Stage03 长文成本

准确性稳定后可增加 section-aware evidence routing：优先 Methods/Computational/Experimental、SI 方法段
以及包含目标计算/实验词的块，首尾摘要用于文章角色判断；低置信或证据覆盖不足时再回退全文。不能用
廉价规则直接硬淘汰，否则会重新引入旧版漏筛。

### P2：保留紧凑的混合论文二级池

当前 212 篇“计算 primary 但作者也做实验”的论文不符合正式纯计算集，但可能含可独立复现的计算子任务。
建议正式路径继续淘汰，同时保留 paper ID、方法、软件、实验反证和淘汰原因的紧凑审计记录，不保留大
体积中间文本。这样未来放宽到任务级纯计算时无需重新处理全部 PDF。

## 7. 建议的下一步

1. 先实现 Stage02 完整性门控和 Stage03 implementation version；
2. 冻结 200 篇人工标注/holdout，计算 precision、recall 和错误类型；
3. 根据远端期刊全集调整 Stage00 分层采样，再运行新的 500 篇；
4. 在新样本上只校准 Stage00-03，确认通过集 precision 后再批量启动 Stage04-06。

本轮详细运行产物位于 `runs/v2_stage03_r6_350_20260808/`，最终记录 run ID 为
`v2-stage03-r7-350-20260808`。实现变更记录见 `docs/v2/IMPLEMENTATION_LOG.md`。
