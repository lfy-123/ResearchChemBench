# Flash Stage 00-06 百篇测试报告

日期：2026-08-07

## 1. 测试配置

- 数据集：`en-paper-hzzj`，seeded sample 100 篇正文；
- 流程：Stage 00 -> 01 -> 微批次 Stage 02 -> 03 -> 04 -> 05 -> 06；
- 微批次：每批 10 篇、最多 5 批并行、同一批内阶段串行；
- Stage 03：规则优先，边界样本使用 `deepseek-v4-flash`；
- 沙箱：申请 128 CPU/256 GiB 等待 600 秒未调度，自动改用 64 CPU/128 GiB；
- 生命周期：一个沙箱和一组 GROBID/Softcite 服务贯穿任务，结束后统一停止；
- 总墙钟时间：532.424 秒，不含首次 128 CPU 沙箱的 600 秒调度等待。

样本覆盖 10 类已知期刊和 3 篇期刊元数据缺失记录。DOI 出版商前缀分布为 ACS 40、
Wiley 28、RSC 23、Elsevier 7、Nature 2，不是单一 Wiley 样本。

## 2. 阶段结果

| 阶段 | 输入 | 结果 | 继续 |
| --- | ---: | --- | ---: |
| Stage 00 | 100 篇 | 100 正文、84 个 SI；82 篇有 SI，18 篇无 SI；0 复制失败 | 100 |
| Stage 01 | 184 PDF | 184 canonical、0 duplicate、0 excluded | 100 篇 |
| Stage 02 | 184 PDF | GROBID 181；pdftotext 回退 3；0 最终解析失败 | 100 篇 |
| Stage 03 正式运行 | 100 篇 | strong 48、weak 10、not computational 42 | 58 |
| Stage 04 | 58 篇 | 已有 SI 跳过 54、下载成功 1、访问受阻 3 | 55 可用，3 丢弃 |
| Stage 05 | 58 篇 | direct 43、method-only 6、unsupported 6、SI unavailable 3 | 49 |
| Stage 06 | 49 篇 | 51 个文档证据；49 篇复用 Stage 02 SI；0 错误 | 49 |

Stage 04 唯一下载成功论文为 DOI `10.1016/j.chempr.2024.02.004`，获得 2 个正式附件。
3 篇 Wiley 论文的官网请求为 `access_blocked`，按二元保留规则在 Stage 05 丢弃。

## 3. Stage 03 Flash 修复后复核

首次完整运行使用 512 输出 token 和提供方默认 thinking。47 篇进入模型复核，其中 5 篇
非 JSON 回退规则，另 7 篇 `finish_reason=length` 的截断响应仍可解析前半段，因缺少
confidence 被保守留为 weak。该行为不会产生错误 strong，但审计状态不准确。

修复内容：

- 输出上限改为 1024；
- 外部 Flash 显式设置 `thinking=disabled`；
- `finish_reason=length` 或缺少任一必填字段直接回退规则；
- `max_tokens` 和 `thinking` 纳入缓存键；
- 引用无法回映原文仍按 uncertain 回退。

同一批 47 个边界样本定向重放结果：

- 47/47 均 `finish_reason=stop`，0 截断、0 缺字段；
- 45 篇形成有效 yes/no，2 篇因证据引用无法回映而保守回退规则；
- 最终 Stage 03 为 strong 56、weak 2、not computational 42；
- 规则基线为 strong 36、weak 25、not computational 39；模型改变 24 个判定；
- 规则到最终：weak -> strong 19、weak -> reject 4、reject -> strong 1；
- 修复前后候选集合完全相同，均为同一组 58 篇，因此 Stage 04-06 无需重跑；
- 47 次调用累计 101,779 tokens，并发调用耗时和为 92.149 秒，实际墙钟约 19 秒。

## 4. 并发与耗时

10 个微批次的单批阶段耗时范围和中位数：

| 阶段 | 最短 | 中位数 | 最长 | 说明 |
| --- | ---: | ---: | ---: | --- |
| Stage 02 | 6 s | 41.5 s | 305 s | 3 个 GROBID 网关超时形成长尾并回退 pdftotext |
| Stage 03 | 8 s | 24 s | 30 s | 包含规则和 Flash 边界复核 |
| Stage 04 | <1 s | <1 s | 12 s | 大部分已有 SI 直接跳过，仅一篇下载 |
| Stage 05 | 42 s | 115 s | 164 s | Softcite 是当前主要吞吐瓶颈 |
| Stage 06 | 0.2 s | 0.7 s | 1.0 s | 本批幸存论文全部复用 Stage 02 SI 文本 |

Stage 02-06 确实是微批次流水：不同批次同时位于不同阶段；Stage 05 完成一个批次后立即
释放并发槽给下一批 Stage 02，不等待全部 100 篇完成同一阶段。

## 5. 运行中发现并修复的问题

1. GROBID 在 5 批并发时短暂返回 503，3 个长请求最终为 504；管线正确回退
   `pdftotext`，失败率 1.63%，没有论文丢失。后续可为 GROBID 单独降低 semaphore，
   避免少数 900 秒级长尾。
2. 一篇 SI 含超长 POSCAR 坐标，旧代码将整段放入 Softcite GET query，返回 431。
   已改为以软件别名为中心截取最多 600 字符，客户端也有 600 字符防御上限，并增加
   回归测试。历史运行保留该单文档错误以供审计；论文由其他文档证据正常判定。
3. Flash 输出预算和 thinking 配置问题已按第 3 节修复，并用同批真实证据完成定向重放。

## 6. 验证和产物

- 完整测试：116 passed，6 subtests passed；
- Ruff、shell 语法、`git diff --check -- data_pipeline` 全部通过；
- H200 rlaunch 请求已确认 `Stopped`，没有部署或下载本地模型；
- CPU 沙箱 `sbx-5cf1a62c-39a` 已为 `Terminated`；
- 正式运行目录：`data_pipeline/runs/redesigned_stage00_06_100_flash_20260807/`；
- 修复后 Stage 03 定向结果：
  `run/outputs/stage03_flash_1024_no_thinking_validation/`。

本轮未测试本地 `Qwen3-30B-A3B-Instruct-2507`。其部署脚本和参数接口保留，等待 GPU
资源宽松后再执行 H200 启停、服务健康检查和同批对照测试。
