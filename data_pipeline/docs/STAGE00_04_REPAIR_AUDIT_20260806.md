# Stage 00-04 映射、规则和补充材料修复审计

> 日期：2026-08-06
>
> 范围：已暂停的 1000 篇 shadow run、全部授权远端论文前缀、Stage 03 分层抽查、
> Stage 04 代码与人工网络下载对照。

## 1. 旧运行基线

旧运行 `runs/redesigned_stage00_06_seeded_1000` 在修复前得到：

| 阶段 | 结果 |
| --- | --- |
| Stage 00 | 1000 正文，0 SI，145 complete，855 partial |
| Stage 01 | 1000 正文，0 SHA256 重复 |
| Stage 02 | 999 GROBID 成功，1 pdftotext 回退 |
| Stage 03 | strong 290，weak 245，not computational 465 |
| Stage 04 | access blocked 503，not attempted 18，timeout 13，partial 1 |

Stage 00 的 855 个 partial 不是远端缺少 SI，而是错误地尝试了 956 个不存在的 KPS
快照路径。Stage 04 随后把本应在 Stage 00 复制的论文再次送往官网，放大为 503 个 403。

## 2. 远端正文/SI 映射事实

| 数据集 | 正文对象 | SI 对象 | SI 论文 | 映射结论 |
| --- | ---: | ---: | ---: | --- |
| `en-paper-hzzj` | 21,836 | 19,110 | 18,498 | 全部按 `_sup_N` 映射，0 孤立 |
| `KPS/dt=2026-05-07` | 935,168 | 496,360 | 431,240 | 全部符合命名；100 个随机 owner 经大小写归一化后正文均存在 |
| `KPS/dt=2026-06-18` | 99 | 23 | 10 | 全部映射，0 孤立 |
| `KPS/20260603_bu` | 0 | 265 | 未作为正文语料 | 只有元数据和少量 Nature SI |

`KPS/20260603_bu` JSONL 中的 496,624 个 `support_path` 是引用，不是该目录中的实际
对象。`en-paper-hzzj` 应从自己的 `support/` 目录查找 SI，其主流编号从 `_sup_0`
开始；KPS 快照通常从 `_sup_1` 开始。匹配必须解析编号后缀，不能假定固定编号。

本次 1000 篇选择中，850 篇有 901 个实际远端 SI。修复后的 Stage 03 共有 590 个候选，
其中 507 篇已有远端 SI，只有 83 篇需要 Stage 04 官网补全：Wiley 34、ACS 20、
Elsevier 20、RSC 9。

## 3. Stage 03 分层抽查

抽查按 strong/weak/reject 三类的分数区间和证据组合取样。它不是人工 ground-truth
数据集，结论仅用于发现明显规则错误。

### 3.1 strong

- `10.1039/d4sc00701h`：正文明确给出 B3LYP/LANL2TZ/6-31+G(d,p) 计算，分类合理。
- `10.1021/acscatal.4c03724`：明确用 DFT 研究催化机理，分类合理。
- `10.1021/acs.accounts.4c00640`：方法综述中术语大量重复，虽与计算高度相关，但不应
  因 165 个命中获得 476.7 的无界分数；后续 Builder 仍需排除无新可执行任务的综述。

### 3.2 weak

- `10.1021/acscatal.4c02385`：正文称 DFT calculations，但固定执行模板未命中；保留
  weak 合理。
- `10.1021/jacs.4c16837`：明确包含 DFT+BSE 计算，weak 用于高召回合理，后续 SI 可
  补足执行和参数证据。
- `10.1039/d4sc02089h`：Review 引用他人的 atomistic MD，是明显噪声候选；weak 不等于
  最终通过，应由 Stage 05/Builder 淘汰。

### 3.3 not computational

- 多个 0 分实验论文和只含 `we performed measurements` 的论文淘汰合理。
- `10.1039/d4sc03832k` 明确写有 r2SCAN-3c、wB97X-D4 和 calculations were performed，
  因词表只有单数 `quantum chemical calculation` 被错误淘汰。
- `10.1021/jacs.4c12648` 明确是高通量第一性原理材料筛选，因执行句式不在四个模板中
  被错误淘汰。

修复包括：补齐常见复数方法短语；保存 `raw_score`；对同一规则/章节的计分贡献设上限；
具体方法在有效章节多次出现但未命中执行模板时归入 weak。对现有 1000 篇文本回放后：

| 分类 | 修复前 | 修复后 | 变化 |
| --- | ---: | ---: | ---: |
| strong | 290 | 291 | +1 |
| weak | 245 | 299 | +54 |
| reject | 465 | 410 | -55 |

原 strong/weak 无降级；55 个旧 reject 被恢复为候选。两个已确认的明显漏筛样本分别转为
strong 和 weak。最高用于判定的 score 从 479 降到 115，原始命中量仍保存在
`raw_score` 中供审计。

## 4. Stage 04 人工下载对照

- Wiley `10.1002/anie.202424756` 的公开文章元数据列出 DOCX 和 ZIP 两个 SI。当前机器
  通过平台代理访问文章页及直接 `downloadSupplement` 均返回 HTTP 403；关闭代理后
  TCP 连接超时。因此它是“SI 存在但当前出口受限”，不是代码可以标成 `not_found`。
- RSC `10.1039/D4SC04947K` 和 `10.1039/D4SC02089H` 的公开页面没有 Supplementary
  files，属于真实无 SI；当前机器访问 RSC 页面同样为代理 403/直连超时，所以管线只能
  保存 `access_blocked`，不能在该网络下证明 `not_found`。
- Nature 旧适配器把 `#MOESM` 页内锚点当附件，并漏掉 `static-content.springer.com`
  正式 ESM 域名；Elsevier 漏掉 `els-cdn.com`。这些均已修复并增加测试。

## 5. 实现约束

1. Stage 00 schema 升级为 2；旧目录不能静默 resume，必须新建输出目录重新建立映射。
2. `support_path` 只保留为 `metadata_support_hints`，实际复制 URI 来自真实对象清单或
   成功的远端 `HEAD`。
3. Stage 04 只重试 `matched_remote_uris`，不再拼接未经验证的元数据路径。
4. 官网 401/403/429 统一为 `access_blocked`，不作为科学淘汰。
5. 出版商适配器只接受官方域名和明确标记为 supplementary/supporting 的链接或 meta。

## 6. 验证

- Stage 00/03/04 定向测试：19 passed。
- 真实 Stage 00 烟雾：20 篇正文、21 个 SI、20 个 complete、0 partial、0 copy failure；
  一篇含两个 SI，均进入同一 `paper_id/supplementary/`。
- 旧 1000 篇 Stage 03 文本只读回放完成；未覆盖历史输出。
- 正式 1000 篇重跑必须使用新 Stage 00 工作目录，不能复用 schema 1 产物。
- 全部 `data_pipeline/tests` 回归：97 passed，6 subtests passed；Ruff、Python 编译和
  shell 语法检查通过。
