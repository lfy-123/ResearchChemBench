# 计算化学论文管线重构实施记录

> 开始日期：2026-08-06
>
> 设计依据：`COMPUTATIONAL_CHEMISTRY_TOOLBOX_SCREENING_REDESIGN.md`
>
> Git 策略：直接在本地 `main` 工作树逐阶段修改和验证；未得到明确要求前不推送远端。

## 1. 实施原则

- 主要修改 `data_pipeline/`，其他模块只允许增加工具箱能力的只读导出。
- 保留用户和历史运行产生的现有修改，不回退无关文件。
- 每个阶段先定义输入/输出 schema，再实现，再运行针对性测试。
- 单篇论文或附件失败必须隔离，不能拖垮整个批次。
- 旧阶段实现保留到新流程 shadow run 通过，再决定迁移或删除。
- 所有实际命令、测试结果、偏差和后续事项在本文持续记录。

## 2. 基线审计

### 2026-08-06：现有实现

- 当前代码只有 Stage 01-07，没有 Stage 00。
- Stage 01 递归扫描 PDF，每个 PDF 初始都获得独立 `paper_id`，尚不能可靠聚合论文目录。
- Stage 02 默认排除 supplementary PDF。
- Stage 03 使用 Softcite 做软件硬门控，`software_not_identified` 直接淘汰。
- Stage 04 使用 GROBID Quantities 和远程 LLM 做资源筛选。
- Stage 05 会发现和下载代码仓库、数据集等广泛资产，与新边界不符。
- Stage 06/07 分别是 Builder/Judge，需要顺延为 Stage 07/08。
- 微批次和沙箱已经支持服务在任务生命周期内复用，可作为新流程基础设施保留。

### 2026-08-06：远端数据

- 完整 `en-paper-hzzj` 有 21,836 篇，覆盖 ACS、Wiley、RSC、Elsevier、Nature。
- KPS 20260603 有 935,148 条有效元数据和 107 个原始期刊名。
- 431,475 篇元数据有 `support_path`，但 496,624 是路径引用数，不等于当前快照实际
  对象数。实际对象和映射审计见 `REMOTE_DATASET_JOURNAL_AUDIT.md`。
- 详细统计见 `REMOTE_DATASET_JOURNAL_AUDIT.md`。

## 3. 阶段进度

| 阶段 | 状态 | 说明 |
| --- | --- | --- |
| 设计文档 Stage 00 修订 | completed | 已加入远端复制、论文目录和本地 SI 路由契约 |
| 公共 schema | completed | `paper_id` 贯穿正文、SI、规则证据、附件和能力判断 |
| Stage 00 | implemented | 远端流式选择、正文/SI 分组、原子目录、游标与恢复 |
| Stage 01 | implemented | 读取 `paper.json`，同篇正文/SI 共用 `paper_id` |
| Stage 02 | implemented | 正文和已有 SI 均进入 GROBID/回退路径并生成 paper bundle |
| Stage 03 | implemented | YAML 版本化规则，无 LLM，保存证据和排除证据 |
| Stage 04 | implemented | 已有 SI 零网络跳过；同源 `support_path` 优先；六类官网适配器 |
| Stage 05 | implemented | Softcite 并发预筛，保留 method-only/software-unknown，单文档错误隔离 |
| Stage 06 | implemented | 只解析新附件，复用 Stage 02 SI；pdftotext/GROBID/MinerU 质量升级 |
| Stage 07 | migrated | Builder 已顺延并更新能力、科学意义和防平凡任务约束 |
| Stage 08 | migrated | Judge 已顺延并更新独立终审约束 |
| 编排/CLI/配置 | implemented | 主 `run` 已切换 Stage 00-08；沙箱服务跨 Stage 02-06 复用 |
| 全流程验证 | in progress | 单元测试通过；真实 2 篇沙箱冒烟正在等待平台资源调度 |

### 2026-08-06：Stage 00-04 缺陷复核和修复

- 确认旧 Stage 00 将 KPS 元数据 `support_path` 拼到错误快照根目录，导致 850 篇本可
  直接匹配 SI 的论文被误报缺失。
- Stage 00 schema 升级为 2，按数据集真实 `supplementary_prefix` 列举或 `HEAD` 验证
  对象，再以 DOI 文件名和 `_sup_N` 建立一对多映射；旧 schema 禁止静默 resume。
- Stage 04 不再读取原始 `support_path` 猜测 URI，只重试 Stage 00 已验证对象。
- Stage 03 限制重复命中计分并扩充方法词形；旧 465 个 reject 中恢复 55 个候选。
- Nature/Elsevier 官方附件域名和 HTML meta 发现已补齐，Nature 页内锚点已排除。
- 详细证据见 `STAGE00_04_REPAIR_AUDIT_20260806.md`。

## 4. 变更记录

### 2026-08-06：设计更新

- 新增 Stage 00：从授权远端选择指定数量正文，复制远端已有 SI，并按 `paper_id` 整理。
- Stage 02 改为解析正文和 Stage 00 已复制的 SI。
- Stage 03 规则证据同时使用正文和已有 SI，且不调用 LLM。
- Stage 04 对已有 SI 的论文逐篇跳过，只处理仍缺 SI 的候选。
- Stage 06 只解析 Stage 04 新下载且尚未解析的 SI。

### 2026-08-06：Stage 00-02

- 新增 `src/integrations/xinghe.py`，对授权 URI 做前缀校验并使用只读对象接口。
- Stage 00 使用服务端 `StartAfter` 恢复远端枚举，复制事件采用追加审计。
- 每篇输出 `corpus/<paper_id>/paper.json|main/|supplementary/`；单个 SI 复制失败只使
  该论文状态为 `partial`。
- Stage 01 从最近的 `paper.json` 读取身份与角色；Stage 02 不再排除 SI。
- Stage 02 新增 `paper_text_bundles.jsonl`，分别保存正文、SI 和单附件解析错误。

### 2026-08-06：Stage 03-06

- Stage 03 新增方法本体、正证据规则和负面语境规则；输出正文/SI 可定位证据，不导入
  LLM client。
- Stage 04 实现 ACS、RSC、Elsevier、Wiley、Nature 和 MDPI 官网域名适配；非官网
  链接不会进入下载队列。
- Stage 05 复用 Softcite NER/上下文判定，但将旧硬门控改成论文级预筛；Softcite
  单文档错误记录为 `stage_error` 并继续。
- `assets/toolbox_capabilities.json` 固定 catalog hash 和方法族映射；未声明限制保持
  `unknown`。
- Stage 06 复用 Stage 02 已解析 SI，仅处理 Stage 04 新附件并生成软件、参数、输入、
  结果证据包。

### 2026-08-06：编排和批处理

- 主编排切换为 Stage 00-08，旧 late-stage 入口和旧阶段目录暂时只读保留。
- GROBID context 从 Stage 02 持续到 Stage 06；沙箱由整次 `run` context 统一清理。
- `prepare-remote-corpus` CLI 可单独运行 Stage 00。
- 历史名称 `scripts/run_stage_01_04_batches.sh` 保留作为兼容入口，但实际任务改为一次
  选择 1000 篇正文及其 SI，并固定运行到新 Stage 06；默认沙箱为 128 CPU/256 GiB。

## 5. 测试记录

- 新阶段定向测试：15 passed。
- 批处理、旧门控兼容和错误隔离测试：20 passed，6 subtests passed。
- 完整测试集：`81 passed, 6 subtests passed`。
- Ruff、`bash -n`、Python 编译和 `git diff --check` 已通过。
- 真实冒烟：2026-08-06 18:50 HKT 提交 2 篇 Stage 00-06，平台已创建
  `128 CPU/256 GiB` 环境，但截至本条记录沙箱仍为 `Pending`，阶段计时尚未开始。

## 6. 已知风险和待办

- 远端 1.6 GB JSONL 当前按流扫描匹配本批文件；1000 篇可运行，但跨多批扩展时仍应
  增加本地索引缓存。
- `en-paper-hzzj` PDF 前缀与 KPS 元数据不是完全同步，Stage 00 必须允许元数据缺失。
- 出版商在线附件下载可能出现 403；不得绕过授权，需保留 `access_blocked` 状态。
- 当前新版主编排采用阶段级 worker 并发；旧 microbatch 编排仍对应旧阶段语义，尚未
  接回新版 Stage 02-06，因此本次 1000 篇验证使用阶段屏障和阶段内并发。
- 当前平台代理对 Wiley/RSC 文章页返回 403，直连超时；对象存储已有 SI 不受影响，
  其余官网补全需保留 `access_blocked` 或换用具备合法访问能力的出口重试。

### 2026-08-06：修复后回归

- 全部 `data_pipeline/tests`：97 passed，6 subtests passed。
- Ruff、Python compileall、批处理 Python 编译和 shell 语法检查通过。
- 真实 Stage 00 取 20 篇：20 篇正文、21 个 SI、0 partial、0 copy failure。
