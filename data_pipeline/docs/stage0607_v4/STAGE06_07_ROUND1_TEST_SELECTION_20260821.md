# Stage06/07 第1轮多样性测试抽样

日期：2026-08-21  
代码基线：`1ac85c6`   
模型：`deepseek-v4-pro-0813`  
harness：`codex`  
并发：10

## 抽样依据

从已保留的批量运行结果
`runs/stage06-07-gpt-5.6-sol-stage05-passed-concurrency8-20260820T033608Z`
的 376 个已生成 Stage06 摘要中，按上一轮运行状态分层抽取，覆盖构建成功、不可构建、工件交付失败和目标失败四类。该批量任务曾被用户停止，因此本轮只把它作为多样性抽样来源，不把其 Stage07 未运行状态当作质量结论。

## 选定论文

| 类别 | paper_id | DOI |
|---|---|---|
| provisional_constructed | `paper_9897b87641707c46` | 10.1016/j.ica.2026.123082 |
| provisional_constructed | `paper_3e4cad1d1d650d0c` | 10.1021/acscatal.5c06048 |
| provisional_constructed | `paper_48278ec4f02de3d9` | 10.1021/jacs.5c15273 |
| artifact_delivery_failure_retryable | `paper_08c040bf4e456891` | 10.1039/d5cp04305k |
| artifact_delivery_failure_retryable | `paper_5d94285cfbd51973` | 10.1002/slct.202505650 |
| artifact_delivery_failure_retryable | `paper_4f347e11020a9b86` | 10.1002/slct.202505016 |
| provisional_not_constructible | `paper_5ea491c741fbd8d4` | 10.1016/j.molstruc.2026.145359 |
| provisional_not_constructible | `paper_298959ead2e91023` | 10.1021/acs.inorgchem.5c04909 |
| provisional_not_constructible | `paper_669e50ef52a799ee` | 10.1039/d5dt02898a |
| objective_failure_retryable | `paper_884dc6e99e15db1d` | 10.1021/acs.jpcc.5c06463 |

## 验收重点

每篇均检查 Stage06A 科学目标/路线选择、Stage06B 脱敏后输入闭合、Stage07 科学审计与修复、机械发布状态、evaluator dry-run 和最终公开目录。只有在机械阻断持续集中于可确定修复的运输问题时，才考虑实现 Stage07B。
