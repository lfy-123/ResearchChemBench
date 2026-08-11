# Stage02 低成本分类修改计划

## 目标

在不设定目标通过率的前提下，以高精度区分：

1. `computational_content_confirmed`：纯计算化学，Pass。
2. `computational_primary_mixed_confirmed`：计算产生核心贡献，实验验证或辅助，Pass。
3. `experimental_primary_computational_support`：实验产生核心贡献，计算用于解释，Reject。
4. `computational_content_not_found`：没有实质计算化学流程，Reject。
5. `uncertain`：证据、解析或主次关系不足，Hold。

`non_original_article` 和 `processing_failed` 继续作为文章/运行状态保存。

## 实施步骤

- 本地扫描完整正文和全部已知 SI，排除参考文献与坐标转储，宽召回计算和作者实验线索。
- 构造正文叙事、计算证据、实验依据三类有界证据包，避免 SI 或单一证据类型垄断 prompt。
- 全文完全没有实质计算信号时零调用淘汰；不使用规则判断计算与实验的主次。
- 每篇候选默认调用一次 screening LLM，要求输出工作流、核心结论、双向论据和反事实。
- 程序按证据类型验证 evidence ID；工作流和计算必需结论必须引用计算证据，不能用叙事或实验块代替。
- 高精度全文规则找到的作者实验句直接加入模型可见证据包，避免程序与模型使用不同证据裁决。
- 仅在证据或契约冲突时进行一次独立复审；二次仍冲突则 Hold。
- 两种计算主导标签进入 Stage03；实验主导和无计算内容写入 rejected；Hold 写入 held。
- Registry 只删除 Stage00-03 明确拒绝论文，保留 Hold 资产以便恢复。

## 成本约束

- 默认 prompt 上限：36000字符。
- 默认分类输出：1536 tokens。
- 默认调用次数：候选论文1次；冲突论文2次；明显无计算论文0次。
- 审计同时记录语义调用数、底层成功 HTTP 尝试数、缓存命中和无法完整计数的失败请求。
- 使用独立 namespace 和 prompt 版本，禁止复用旧 Map/Reduce 缓存。

## 验证

- 单元测试覆盖五类决策、证据包平衡、零调用、单调用、条件复审、缓存失效和 Hold 资产保留。
- 从完整解析历史样本中冻结200篇高难度分层评估集，并锁定正文、SI、内容块路径及 SHA256。
- 人工标签与 Stage02 推理相互隔离，统计混淆矩阵、Pass precision/recall、Hold率及每篇调用数。
- 逐篇复核误判后再提出通用改进，不为个别论文添加特例规则。
