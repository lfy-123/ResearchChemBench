# Stage 04 远端缺失补充材料下载审计

日期：2026-08-06

## 1. 审计目标

本次审计针对 `redesigned_stage00_06_seeded_1000` 中远端 `en-paper-hzzj/support/` 未找到配套补充材料的 150 篇论文，回答三个问题：

1. 这些论文是否确实没有补充材料；
2. 当前 Stage 04 是否能够发现并下载出版社附件；
3. 绕过 Stage 04 后，人工使用出版社官方地址是否能够下载。

逐篇结果见 `STAGE04_MISSING_SI_PAPER_STATUS_20260806.csv`。本文中的“未确认”不能解释为“没有补充材料”。

## 2. 样本与方法

150 篇论文来自已选 1000 篇论文中未在实际远端 support inventory 找到 SI 的部分，出版社分布如下：

| 出版社 | 论文数 | 修复后 Stage 03 候选数 |
| --- | ---: | ---: |
| Wiley | 49 | 34 |
| ACS | 51 | 20 |
| Elsevier | 38 | 20 |
| RSC | 12 | 9 |
| 合计 | 150 | 83 |

执行了四类检查：

1. 用当前 `stage04_supplementary_acquisition` 原样处理全部 150 篇；
2. 检查 Stage 04 的 landing URL、HTTP 状态和附件发现结果；
3. 在出版社官方域名上直接探测附件，Elsevier 使用 DOI 解析得到的 PII 检查官方 `ars.els-cdn.com` 附件；
4. 对代表性附件做完整下载和文件级校验，并用出版社官方页面核验 Wiley、ACS 和 RSC 的补充材料信息。

网络路径同时检查了开发机默认代理、无代理、`closeai-proxy` 和认证代理。默认代理对 Wiley、ACS、RSC 返回 403；无代理及认证代理在当前机器上超时；`closeai-proxy` 的 CONNECT 请求返回 403。Elsevier 官方 CDN 可通过默认代理访问。

## 3. Stage 04 实测结果

当前 Stage 04 对 150 篇论文发现并下载的附件数为 **0**：

| 出版社 | Stage 04 结果 | 数量 |
| --- | --- | ---: |
| Wiley | `access_blocked` | 49 |
| ACS | `access_blocked` | 49 |
| ACS | `timeout` | 2 |
| RSC | `access_blocked` | 12 |
| Elsevier | `not_found` / `not_attempted` | 38 |

这个结果不能用作“论文没有 SI”的判断。它混合了三种不同语义：出版社拒绝当前出口、网络超时、适配器没有在 HTML 中发现附件。

## 4. 人工核验结果

### 4.1 Elsevier

38 篇中有 **28 篇**在 Elsevier 官方 CDN 上确认存在附件，共确认 **75 个附件**：

| 类型 | 数量 |
| --- | ---: |
| PDF | 63 |
| MP4 | 8 |
| XLSX | 3 |
| ZIP | 1 |

这些附件按服务器声明的完整大小合计约 600.6 MiB。修复后 Stage 03 保留的 20 篇 Elsevier 论文中，18 篇确认存在附件。

代表样本 `10.1016/j.checat.2023.100826` 的 `mmc1.pdf` 已做完整人工下载：

- 文件大小：21,943,314 bytes；
- PDF 版本：1.7；
- 页数：208；
- SHA256：`e55cc8e797fde83c0c755b8548aa46ede115bdf8bc476e81873d941c01c1de5b`；
- `pypdf` 能读取元数据和首页文本，文件有效。

剩余 10 篇除常规 `mmc1` 到 `mmc4` 外，又检查了 `mmc1` 到 `mmc10` 及 PDF、DOCX、ZIP、XLSX、CSV、TXT、PPTX、MP4、MOV 扩展名，未找到附件。这个结果只能说明常见官方附件命名下未发现资源，不能严格证明论文没有其他形式的补充材料。

### 4.2 Wiley

官方页面明确确认下列 5 篇存在补充材料：

| DOI | 官方页面列出的附件 |
| --- | --- |
| `10.1002/anie.202424756` | DOCX 及 ZIP |
| `10.1002/anie.202502890` | PDF，2.4 MB |
| `10.1002/anie.202506618` | DOCX，146.5 MB；另有 AVI 视频 |
| `10.1002/anie.202509661` | DOCX，4.5 MB |
| `10.1002/anie.202511921` | DOCX，15.9 MB |

当前机器直接访问页面和 `downloadSupplement` 地址均为 403，关闭代理则超时，因此本次没有完成 Wiley 文件下载。这里是“已确认存在但当前出口不能下载”，不是“无 SI”。

其中 4 篇属于修复后 Stage 03 候选。`10.1002/anie.202506618` 被 Stage 03 淘汰，但也证明正文没有明确 SI 声明时仍可能存在官方附件。

### 4.3 ACS

官方 ACS 页面明确确认 `10.1021/jacs.4c08163` 存在 `ja4c08163_si_001.zip`，大小 15.74 MB；该论文属于修复后 Stage 03 候选。当前 Stage 04 对 ACS 页面得到 403，ACS Figshare API 在当前网络出口也返回 403，因此未完成文件下载。

其余 ACS 论文不能因为 403 被判定为无 SI。样本中包含 Accounts 综述、Correction、Retraction、Masthead 等非普通研究论文，这些论文没有附件的先验概率较高，但需要文章类型门控或官方元数据确认，不能由下载错误推断。

### 4.4 RSC

12 篇论文的官方页面均未列出 `Supplementary files` 区域。文章类型包括 9 篇 Review Article、1 篇 Paper 和 2 篇 Edge Article。`10.1039/D4SC04947K` 的数据可用性声明还明确表示数据包含在正文中。

因此这 12 篇目前归类为“官方页面未列出补充材料”，置信度高于单纯的下载失败，但仍保留原始页面证据，不使用 HTTP 404/403 单独证明附件不存在。

## 5. 逐篇状态汇总

| 状态 | 论文数 | 含义 |
| --- | ---: | --- |
| `confirmed_present_official_cdn` | 28 | Elsevier 官方 CDN 已返回真实附件 |
| `confirmed_present_official_page` | 6 | Wiley/ACS 官方页面明确列出附件 |
| `no_supplementary_listed_official_page` | 12 | RSC 官方文章页没有附件区 |
| `not_found_after_official_cdn_pattern_probe` | 10 | Elsevier 常见官方附件路径扩展探测未命中 |
| `unverified_access_blocked` | 94 | Wiley/ACS 站点被当前网络出口阻断，无法确认 |

因此，150 篇中至少 **34 篇确定存在补充材料**。在修复后 Stage 03 的 83 篇候选中，至少 **23 篇确定存在补充材料**，9 篇 RSC 官方页面未列出附件，另外 51 篇仍需在可访问 Wiley/ACS 的网络环境下确认。

## 6. 根因分析

### 6.1 Elsevier 是代码发现缺陷

当前通用适配器只解析 landing HTML 中的 `<a>`、部分 `<meta>` 和 `<link>`。Elsevier DOI 最终落在 `linkinghub.elsevier.com/retrieve/pii/<PII>`，该 HTML 不包含静态 SI 链接；实际附件位于 `ars.els-cdn.com/content/image/1-s2.0-<PII>-mmcN.<ext>`。所以 Stage 04 报 `not_found`，而直接访问官方 CDN 可以成功。

### 6.2 Wiley、ACS、RSC 主要是访问和动态页面问题

当前适配器假设出版社正文页面可以由普通 HTTP 客户端直接获取，并且附件以静态链接存在。Wiley、ACS、RSC 对当前出口返回 403 或依赖动态内容；通用 HTML 解析不足以覆盖这些站点。不同代理的对照测试没有改变这一结论。

### 6.3 文件格式限制会继续造成漏下载

Stage 04 默认只允许 PDF。已确认的 Wiley 附件中有 DOCX、ZIP、AVI，Elsevier 中有 XLSX、ZIP、MP4，ACS 代表样本为 ZIP。即使附件发现成功，这些文件也会被标记为 `unsupported_format`。如果 Stage 04 的目标是补齐“补充材料”，默认格式至少需要覆盖 PDF、DOCX、ZIP、XLSX；视频是否保留应单独配置。

### 6.4 状态语义不够严格

`not_found`、`access_blocked`、`timeout`、`confirmed_absent` 必须分开。当前流程虽然保留了部分 attempt 信息，但上层统计容易把“没有下载到”误读成“论文没有 SI”。Stage 04 不应在没有官方否定证据时输出等价于无 SI 的结论。

## 7. 建议的修复顺序

1. 为 Elsevier 增加专用发现器：从 DOI/Crossref/landing URL 提取 PII，再使用官方元数据或有界 `mmc` 发现策略；不要只解析 linkinghub HTML。
2. 为 Wiley、ACS、RSC 分别实现出版社专用发现器，优先使用官方结构化元数据或附件 API；对 401/403/429 保留 `access_blocked`，支持重试和断点恢复。
3. 将允许格式拆成文档附件和多媒体附件两组。文档默认覆盖 PDF、DOCX、ZIP、XLSX、CSV、TXT；视频由显式参数控制。
4. 增加 `confirmed_absent` 的严格定义：只有官方页面或结构化元数据明确无附件时才能使用；403、超时和适配器未发现一律进入 `unknown/needs_retry`。
5. 为每篇论文保存 landing URL、附件清单、HTTP 状态、发现器版本和原始元数据缓存，便于审计。
6. 修复后先重跑这 150 篇作为回归集。最低验收条件是 Elsevier 已确认的 28 篇能够全部发现，且不会把 Wiley/ACS 的 403 记录成无附件。

## 8. 本次审计边界

第 2-7 节记录的是修复前基线。本次没有恢复已暂停的 1000 篇流水线或启动沙箱。
Wiley/ACS 的 94 篇仍需在能够访问出版社页面或官方附件 API 的网络环境下继续确认。

## 9. 审计后的代码修复

根据本报告证据，随后完成以下修改：

- Elsevier 适配器从 LinkingHub URL 提取 PII，并以有界 HEAD 请求发现官方 CDN 的
  `mmc` 附件；
- Stage 04 增加 `presence_status=available|absent_confirmed|present_unavailable|unknown`；
- 默认正式 SI 格式扩展到 PDF、DOCX、ZIP、XLSX、CSV、TXT、CIF，视频仍不默认下载；
- Stage 05/06 只保留确认无 SI 或至少一个正式 SI 已下载落盘的论文；
- 非 PDF SI 在 Stage 06 作为原始资产保留，不误交给 `pdftotext`。

真实网络回归中，`10.1016/j.checat.2023.100826` 已由新适配器发现 4 个附件（3 PDF、
1 XLSX）；`10.1016/j.checat.2023.100898` 完成有界探测后未发现附件并记录
`absent_confirmed`。逐篇 CSV 仍保留修复前 150 篇基线结果，便于后续全量回归对照。
