# Strict Flash Stage 00-06 五百篇测试报告

日期：2026-08-07

## 1. 结论

本次 500 篇严格模式任务完整结束，50/50 个微批次成功，0 个失败。Stage 03 从 500 篇中
保留 283 篇确认包含作者实际执行计算的原创研究；Stage 05 再按工具箱功能级后端、执行
语境和方法族交集收紧到 158 篇，占原始样本的 31.6%。Stage 06 处理 166 份补充材料，
0 个解析错误。

本轮结果适合作为 Builder 的高精度候选集，但不能把 158 篇直接称为 benchmark-ready。
其中 136 篇的计算在论文中属于 supporting，后续仍需由 Builder 判断能否形成非平凡、
输入和答案可分离、可客观评分的任务。

## 2. 测试配置

- 代码版本：`0f29bf7 feat(data-pipeline): enforce strict screening precision`；
- 数据集：`en-paper-hzzj`，seeded sample 500 篇，seed `20260806`；
- Stage 00 同时复制远端已存在的补充材料，并按 `paper_id/main|supplementary` 分组；
- Stage 02-06：每批 10 篇、最多 5 个微批次并发，同一微批次阶段串行；
- Stage 03：规则召回后由 `deepseek-v4-flash` 审查全部规则候选，16 路 API 并发；
- 筛选策略：`strict`，模型/API/证据不确定时 fail closed；
- Stage 05：5 个 Softcite 实例；只接受 functional、执行语境成立且方法族匹配的直接后端；
- 沙箱：128 CPU、256 GiB，一个沙箱贯穿 Stage 02-06，任务结束后统一停止；
- 总墙钟时间：6500.207 秒，即 1 小时 48 分 20 秒。

## 3. 阶段结果

| 阶段 | 输入 | 主要结果 | 继续 |
| --- | ---: | --- | ---: |
| Stage 00 | 500 篇 | 500 正文、435 份 SI；429 篇有 SI、71 篇无 SI；0 复制失败 | 500 |
| Stage 01 | 935 PDF | 935 canonical、0 duplicate、0 excluded | 500 篇 |
| Stage 02 | 935 PDF | GROBID 931；`pdftotext` 回退 4；0 最终失败 | 500 篇 |
| Stage 03 | 500 篇 | strong 283、not computational 191、LLM unconfirmed 26 | 283 |
| Stage 04 | 283 篇 | 已有 SI 255、下载 4、部分下载 4、访问受阻 19、确认无 SI 1 | 283 路由至 Stage 05，其中 264 可保留 |
| Stage 05 | 283 篇 | direct 158、method-only 58、direct-unverified 48、SI unavailable 19 | 158 |
| Stage 06 | 158 篇 | 166 份 SI；161 份复用 Stage 02、5 份新解析；0 错误 | 158 |

Stage 03 通过率为 56.6%。Stage 05 保留 Stage 03 候选的 55.8%，最终保留率为原始 500
篇的 31.6%。Stage 04 的一篇 `absent_confirmed` 论文符合“确认无 SI 可保留”的规则，
但随后因只有方法证据、没有合格工具箱后端而在 Stage 05 淘汰。

## 4. Stage 02 解析质量

4 个 GROBID 请求分别因 503/504 回退 `pdftotext`，回退文本质量分为 82.6、86.1、
91.2 和 93.5，均可供后续筛选。正文平均质量分 96.23，SI 平均 76.69。

17 份文档被质量规则标记为 `needs_ocr`，其中 7 份正文实际是 editorial board、
correction 或 addition 页面，均被 Stage 03 淘汰；其余 10 份为低文本密度 SI。当前没有
因这 17 份文档导致流程错误，但低质量 SI 仍可能造成保守漏筛，符合本轮“精度优先”的
取舍。

## 5. Stage 03 筛选效果

规则层结果为 219 strong、110 weak、171 无候选证据。329 个 strong/weak 全部进入 Flash：

- 206 个 rule-strong 保持 strong；
- 77 个 rule-weak 被模型确认并提升为 strong；
- 19 个 rule-weak 和 1 个 rule-strong 被确认不是作者执行的计算；
- 26 个候选因严格条件不完整而进入 `llm_unconfirmed`，没有放行；
- 4 篇被模型识别为 review，全部淘汰，综述没有进入 Stage 04。

329 次模型调用全部获得结构化响应，无 API、JSON、schema 或截断错误。平均单次模型耗时
2.587 秒，P95 为 3.662 秒，累计 1,111,439 tokens。通过候选中 35 篇计算为 primary，
248 篇为 supporting。

### 严格拒绝分析

26 个 `llm_unconfirmed` 中，24 个是模型将 `performed_computation` 返回为 `uncertain`，
1 个虽返回 yes 但置信度只有 0.8，1 个虽返回 yes 但文章类型为 review。24 个 uncertain
样本里，多数 reason 文本同时声称作者做过 DFT/MD，存在模型字段自相矛盾；严格模式没有
猜测修正，全部 fail closed。这会牺牲召回率，但没有造成错误放行。

### 人工证据抽查

按输出顺序均匀抽取 20 个 Stage 03 通过样本，20/20 均能在正文或 SI 中找到模型引用的
作者执行句，例如 `we performed`、`calculations were carried out using` 或明确的软件和
方法配置；没有发现仅引用前人工作、仅出现缩写或综述型样本。该抽查支持当前高精度
方向，但不是带人工金标准的统计 precision。

通过样本的方法族以 electronic structure 为主：264 篇；其次为 reaction kinetics 129、
periodic materials 111、molecular dynamics 71、free energy 35、chemistry ML 30、
docking/conformer 12、multiscale 4。一篇论文可计入多个方法族。

## 6. Stage 04 补充材料

283 个 Stage 03 候选中，255 篇在 Stage 00 已带 SI，因此不访问官网。其余 28 篇的结果：

- 4 篇完整下载、4 篇部分下载，共落盘 18 个 PDF 附件；
- 19 篇官网返回 403，记录为 `access_blocked/unknown`，随后严格淘汰；
- 1 篇官方页面可确认没有补充材料，记录为 `absent_confirmed` 并保留到 Stage 05。

Stage 04 没有把 403 当成“没有 SI”，二元保留规则执行正确。8 篇获得新附件的论文中，
只有 2 篇同时通过 Stage 05；Stage 06 对这 2 篇新解析了 5 个 PDF。其余 6 篇因后端或
方法覆盖不足被淘汰，而不是因补充材料状态淘汰。

## 7. Stage 05 工具箱覆盖效果

全量检查 158 个 `direct_candidate`，每篇都满足以下不变量：

- 至少一个直接后端的 `validation_level=functional`；
- 软件执行语境为真，不是参考文献、品牌词或只出现名称；
- Stage 03 方法族与工具箱后端能力存在交集；
- 没有依靠 capability-equivalent、interface、catalogued 或 unknown 能力放行。

实际形成放行依据的后端计数为 Gaussian 93、VASP 57、ORCA 23、CREST 7、LOBSTER 2；
同一论文可以有多个后端。每个通过样本至少有 Gaussian、VASP 或 ORCA 之一作为功能级
直接依据，CREST/LOBSTER 只作为附加能力出现。

按输出顺序均匀抽取 25 个通过样本，25/25 都有明确的软件执行句和匹配方法。48 个
`direct_support_unverified` 因只有 interface/catalogued、缺执行语境或能力验证不足停止；
58 个 `method_only_rejected` 只有 DFT/MD 等方法证据但没有合格直接后端；19 个
`supplementary_unavailable` 与 Stage 04 的 19 个 unknown 一一对应。

仍需注意，158 篇中 136 篇的计算角色为 supporting。Stage 05 证明“论文中的某个计算
过程可由功能级工具箱后端覆盖”，并不证明该过程已经具有 benchmark 科学意义、完整输入
或可靠 ground truth，这应留给 Stage 07 Builder。

## 8. Stage 06

Stage 06 处理 158 篇、166 份 SI：156 篇直接复用 Stage 02 的 SI 文本，共 161 份文档；
2 篇使用 `pdftotext` 新解析 Stage 04 下载的 5 份文档。5 份新文档质量分为 92.1-97.8，
无解析错误。最终证据包已保存软件、参数、输入和结果线索，供 Builder 使用。

## 9. 并发、长尾和资源释放

Stage 02-06 确实按 50 个微批次流水执行：同一微批次严格按 02 -> 03 -> 04 -> 05 -> 06，
不同微批次最多 5 路并发，GROBID 和 5 个 Softcite 实例由全部批次共享。没有逐阶段启动
或停止沙箱服务。

本次存在明显性能长尾：04:38:17 至 05:57:43 期间只有一个进度事件，两个连续日志间隔
合计 4766 秒（79 分 26 秒）。当时 batch 48 的 Stage 03 和多个批次的 Softcite Stage 05
请求仍未结束；服务日志没有 OOM、进程退出或最终错误，因此不能仅凭现有证据确定是平台
调度停顿、代理连接长尾还是 Softcite 请求阻塞。扣除该异常区间，任务其余部分约 28 分
54 秒。后续大批运行前应增加阶段 heartbeat、单文档 wall-time watchdog，并降低 Softcite
多次重试的总超时上限。

任务结束后已通过沙箱 API 复核：`sbx-2795c316-bb1` 状态为 `Terminated`，环境资源使用
为 0；本轮没有启动 H200 或本地 Qwen 模型。

## 10. 产物

- 完整运行目录：`data_pipeline/runs/redesigned_stage00_06_500_strict_flash_20260807/`；
- 汇总：`run_summary.json`；
- Stage 03 判定及 Flash 缓存：`run/outputs/stage_03_computation_relevance/`；
- Stage 05 能力判定：`run/outputs/stage_05_preliminary_coverage/decisions.jsonl`；
- 158 篇最终候选及 SI 证据：
  `run/outputs/stage_06_supplementary_extraction/supplementary_evidence_bundles.jsonl`；
- 候选原始正文和远端已有 SI 仍按 `paper_id` 保存于
  `stage_00_remote_corpus/corpus/`；可用前述 158 条 evidence bundle 作为保留清单；
- 代码修改前已通过完整测试：127 passed、8 subtests passed；Ruff、compileall 和
  `git diff --check -- data_pipeline` 均通过。

本轮没有发现导致错误放行、批次失败或结果丢失的功能 bug，因此测试后没有继续改动筛选
语义。需要单独处理的是 79 分钟运行长尾；它是吞吐风险，不影响本轮结果完整性。
