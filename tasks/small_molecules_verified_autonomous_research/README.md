# 小分子自主科研任务：33篇维护集合

2026-11-03任务指令补充：`paper_7a1d5d7c60a0ae04`将现有一句提示强化为持续研究至最终结论、不草草提交未完成报告，指令修订为`research_completion_reinforced_20261103`；评分规则和权重未改。见[审查页](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/papers/paper_7a1d5d7c60a0ae04.md)。

2026-11-03补充：`paper_09c8aaf14b70371f`与`paper_4e9774f4128551d3`完成正文/SI核对，当前修订为`source_checked_evidence_scope_20261103`，已同步升级目录与[审核材料](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/两题正文SI核对与证据范围修订_20261103.md)。评分仍为v3、各题100分。

2026-11-03：已将`upgrade_version/autonomous_research/`中的19题完整复制到本目录顶层，与原14题并列，共33题、146项最终结论，每题100分。新增19题与升级目录逐文件哈希一致；原14题任务文件未改动。按当前评分JSON重新统计，原14题为74项，新增19题为72项；下文历史说明中的70项不代表当前数量。新增任务以各自第一轮/第二轮专家反馈版本为基础，其中两题已追加上述来源复核修订，详见[升级目录说明](upgrade_version/README.md)。

|新增论文ID|输入卡|
|---|---|
|`paper_09c8aaf14b70371f`|[task.md](paper_09c8aaf14b70371f/agent_input/task.md)|
|`paper_0dc85595cab7bc0a`|[task.md](paper_0dc85595cab7bc0a/agent_input/task.md)|
|`paper_2a71ffa4b0a90809`|[task.md](paper_2a71ffa4b0a90809/agent_input/task.md)|
|`paper_3e27c1888e57a947`|[task.md](paper_3e27c1888e57a947/agent_input/task.md)|
|`paper_4761e82fee080c35`|[task.md](paper_4761e82fee080c35/agent_input/task.md)|
|`paper_4e9774f4128551d3`|[task.md](paper_4e9774f4128551d3/agent_input/task.md)|
|`paper_6d19b537a0030e5a`|[task.md](paper_6d19b537a0030e5a/agent_input/task.md)|
|`paper_7516a3cbacb70032`|[task.md](paper_7516a3cbacb70032/agent_input/task.md)|
|`paper_7a1d5d7c60a0ae04`|[task.md](paper_7a1d5d7c60a0ae04/agent_input/task.md)|
|`paper_7cfd59d5c7061c6b`|[task.md](paper_7cfd59d5c7061c6b/agent_input/task.md)|
|`paper_8769f3cc6d18e26c`|[task.md](paper_8769f3cc6d18e26c/agent_input/task.md)|
|`paper_87f5566528287b60`|[task.md](paper_87f5566528287b60/agent_input/task.md)|
|`paper_9f24eac60feca79d`|[task.md](paper_9f24eac60feca79d/agent_input/task.md)|
|`paper_b33676a2051f5e91`|[task.md](paper_b33676a2051f5e91/agent_input/task.md)|
|`paper_c49993ae88ffa0e3`|[task.md](paper_c49993ae88ffa0e3/agent_input/task.md)|
|`paper_c625cba3ce868eb1`|[task.md](paper_c625cba3ce868eb1/agent_input/task.md)|
|`paper_cfff299c39d69520`|[task.md](paper_cfff299c39d69520/agent_input/task.md)|
|`paper_ea6fdc38b4a7f8c7`|[task.md](paper_ea6fdc38b4a7f8c7/agent_input/task.md)|
|`paper_fb75113b35e12c7c`|[task.md](paper_fb75113b35e12c7c/agent_input/task.md)|

---

# 小分子自主科研任务：14篇人工审核后的V3评分规则

更新：2026-11-02。该批次为下表所列原14个`paper_*`目录；本目录当前还包括上文新增19题。版本：`human_review_conclusion_evidence_20261102`；评分策略仍为`paper_science_v3`，运行时为`final_results_100`。

**每题100分，共70个子项，全部采用pass/fail，不保留need_review或人工待定分。** 评分对象是有实际计算证据支持的科学结论、机制解释及适用范围。论文数值、容差、精确比例、距离或频率不作为匹配门槛；所需数值仍必须实际计算、提交并由原生记录支持。只猜结论、只填数字或只提交作业不能得分。

本轮以2026-11-01的两份人工审核表为依据：9篇调整权重、拆分或明确科学条件，5篇保留原命题及权重并同步版本。分级评分通过多个二元子项实现，各项独立保留有证据的分数；存在累进条件的分支项在各自规则中明示。整题成功要求核心子项全部通过，但某项失败不将已得分清零。

| Case | 论文ID / 公开题面 | 子项数 | 分值顺序 |
|---|---|---:|---|
| case_01 | [paper_a3892396b1843698](paper_a3892396b1843698/agent_input/task.md) | 5 | 15/15/15/15/40 |
| case_02 | [paper_8fefc96b015c4577](paper_8fefc96b015c4577/agent_input/task.md) | 3 | 25/25/50 |
| case_03 | [paper_cf8ce1fc0fbcd300](paper_cf8ce1fc0fbcd300/agent_input/task.md) | 5 | 30/25/25/10/10 |
| case_04 | [paper_3c3d73b8715d5fcd](paper_3c3d73b8715d5fcd/agent_input/task.md) | 5 | 30/30/10/20/10 |
| case_05 | [paper_1db677efcdd782ac](paper_1db677efcdd782ac/agent_input/task.md) | 6 | 15/15/15/20/15/20 |
| case_06 | [paper_32dea3515c2c7240](paper_32dea3515c2c7240/agent_input/task.md) | 7 | 15/15/10/10/10/20/20 |
| case_07 | [paper_8cd7be72ae518048](paper_8cd7be72ae518048/agent_input/task.md) | 6 | 20/20/20/15/10/15 |
| case_08 | [paper_080931b1681a8b09](paper_080931b1681a8b09/agent_input/task.md) | 4 | 30/25/25/20 |
| case_09 | [paper_5d9fa6b2dd23daf1](paper_5d9fa6b2dd23daf1/agent_input/task.md) | 7 | 15/15/15/15/30/5/5 |
| case_10 | [paper_1bcf80caf9e64d55](paper_1bcf80caf9e64d55/agent_input/task.md) | 6 | 40/10/10/10/20/10 |
| case_11 | [paper_d142c9737f95225b](paper_d142c9737f95225b/agent_input/task.md) | 6 | 20/20/20/15/15/10 |
| case_12 | [paper_f62b895afc2db020](paper_f62b895afc2db020/agent_input/task.md) | 4 | 30/30/20/20 |
| case_13 | [paper_47948e26afff46f6](paper_47948e26afff46f6/agent_input/task.md) | 3 | 40/40/20 |
| case_14 | [paper_f2a9e1bc87fc9b54](paper_f2a9e1bc87fc9b54/agent_input/task.md) | 3 | 35/30/35 |

## 使用与审查入口

- [修改总结与逐篇审核](../../docs/handle/14篇人工审核评分规则修订_20261102/修改总结与逐篇审核.md)：人工意见落实、前后分值、科学边界、验证结果与限制。
- [4篇人工审核原表](4篇论文新评分规则审核表_20261101.md)与[10篇人工审核原表](10篇论文新评分规则审核表_20261101.md)保留原文。
- 每篇`evaluation/scoring_rules.json`为现行唯一计分合同；`scoring_guide.md`为详细可读标准。
- `reference_conclusions.json`、`conclusion_coverage.json`、`SCORING_INTERFACE.md`及`package_manifest.json`已同步。
- `agent_input/task.md`公开问题及必要证据要求，不含私有参考答案。输入分子、既定条件及预算未改。

## 科学与版本边界

允许回答同一公开问题、有实际证据的等效模型或机制；不强制作者软件、节点名、精确构象或唯一IRC算法。原子身份、成键、电子态、条件及配平参照仍是科学有效性的要求。API或证据读取失败仍按基础设施问题处理，不能伪装成科学零分。

`paper_32dea3515c2c7240`新增强调的两条到产物完整生产性路径有论文依据，但既有独立验证主要覆盖关键构型竞争与孤立反转；本次未新增两条全路径的量化验证。P/S反转比较限定在各自规定溶剂/温度模型，不能外推同条件速率或内禀难度。

`verified_computation_reference.md`、`historical_reference/`及既有备份中的旧窗口和旧评分语句仅作历史记录，**不再产生现行计分门槛**。当前规则没有任何论文数值硬窗。

本目录为维护集合，现有V3启动入口会将任务暂存为标准`autonomous_research/<paper_id>`布局。本次未改harness或评分引擎、未改正在运行的冻结输入、未覆盖历史分数。重新评分历史提交时须显式记录所用新规则版本，不能把旧分直接当成本版结果。

`v1_backup/`、`v2_backup/`、`not_ready/`、`upgrade_version/`及本目录其他历史批次文档不属于下述原14篇计分合同；新增19题的顶层副本采用各自现行评分规则。
