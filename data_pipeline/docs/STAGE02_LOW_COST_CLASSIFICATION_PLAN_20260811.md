# Stage02 低成本分类修改计划

## 目标

在不设定目标通过率的前提下，判断论文是否包含可构成有意义评估子任务的完整计算化学流程，并将
论文中计算与实验的主次关系作为元数据分类：

1. `computational_content_confirmed`：纯计算化学，Pass。
2. `computational_primary_mixed_confirmed`：计算产生核心贡献，实验验证或辅助，Pass。
3. `computational_experimental_co_primary_confirmed`：计算与实验共同主导，Pass。
4. `experimental_primary_benchmarkable_computation`：实验主导，但计算流程完整、非平凡且产生独立
   化学结果，Pass。
5. `computational_workflow_not_benchmarkable`：存在计算，但没有完整、有科学意义的输入—计算—输出
   链，Reject。
6. `computational_content_not_found`：没有作者执行的计算化学流程，Reject。
7. `uncertain`：作者归属或流程完整性证据不足，Hold。

`non_original_article` 和 `processing_failed` 继续作为文章/运行状态保存。

## 实施步骤

- 本地扫描完整正文和全部已知 SI，排除参考文献与坐标转储，宽召回计算和作者实验线索。
- 构造正文叙事、计算证据、实验依据三类有界证据包，避免 SI 或单一证据类型垄断 prompt。
- 全文完全没有实质计算信号时零调用淘汰；不使用规则判断计算与实验的主次。
- 每篇候选默认调用一次 screening LLM，要求输出工作流、生成结果、科学用途、论文角色和双向反事实。
- 程序验证 evidence ID；规则检索器提供正证据锚点，但其漏召回不再作为否定一个模型引用的依据。
- 高精度全文规则找到的作者实验句直接加入模型可见证据包，避免程序与模型使用不同证据裁决。
- 首轮得到候选 Pass 时进行一次独立短复审；复核输入/体系、计算操作、生成输出和科学用途，二次仍
  无法确认则 Hold。
- 四种完整流程标签进入 Stage03；流程不足和无计算内容写入 rejected；Hold 写入 held。
- Registry 只删除 Stage00-03 明确拒绝论文，保留 Hold 资产以便恢复。

## 成本约束

- 默认 prompt 上限：36000字符。
- 默认分类输出：2048 tokens，并限制为1个核心结论、2个工作流步骤和1个实验贡献；软件与资源由 Stage03 从全文独立提取，不在 Stage02 重复输出。
- 默认调用次数：明确 Reject 论文1次；候选 Pass 或契约冲突论文2次；明显无计算论文0次。
- 审计同时记录语义调用数、底层成功 HTTP 尝试数、缓存命中和无法完整计数的失败请求。
- 使用独立 namespace 和 prompt 版本，禁止复用旧 Map/Reduce 缓存。

## 验证

- 单元测试覆盖七类决策、证据包平衡、零调用、单调用、候选通过复审、缓存失效和 Hold 资产保留。
- 从完整解析历史样本中冻结200篇高难度分层评估集，并锁定正文、SI、内容块路径及 SHA256。
- 人工标签与 Stage02 推理相互隔离，统计混淆矩阵、Pass precision/recall、Hold率及每篇调用数。
- 逐篇复核误判后再提出通用改进，不为个别论文添加特例规则。
