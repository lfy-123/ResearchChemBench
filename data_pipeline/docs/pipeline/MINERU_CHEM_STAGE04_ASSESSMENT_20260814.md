# MinerU.Chem Stage04 适配评估（2026-08-14）

## 结论

当前不使用 MinerU.Chem 替换 Stage04 的 MinerU 3.4.4 主解析器。

MinerU.Chem 适合在未来作为 Stage04 的可选化学图片 OCR 增强层，用于从图片区域提取分子和反应结构；它不能替代 Stage04 当前负责的全文 Markdown、公式、表格、章节和阅读顺序解析。在官方提供可批量调用的化学解析 API 或本地部署代码前，不把它接入生产批处理。

## 调研结果

### 官方 MinerU.Chem

- 技术报告：https://arxiv.org/abs/2608.03525
- 在线入口：https://mineru.net/chem/
- 官方 MinerU：https://github.com/opendatalab/MinerU
- 官方 API 文档：https://mineru.net/apiManage/docs

技术报告明确说明 MinerU.Chem 构建在通用 MinerU 解析管线之上，增加化学相关性筛选、分子检测、分子标识符提取、结构识别和反应图解析，产物是 Molecule Summary List 与 Reaction Summary List。因此它是化学图像后处理能力，不是通用全文解析器的替代实现。

截至本次检查：

- 官方报告和项目页只给出 MinerU 在线平台入口，没有给出 MinerU.Chem 的官方本地源码仓库。
- 官方文档解析 API 的公开 `model_version` 只有 `pipeline`、`vlm` 和 `MinerU-HTML`，没有 MinerU.Chem 参数或化学汇总产物契约。
- 官方开源 MinerU 仓库未提供与报告所述五个 MinerU.Chem 模块相对应的本地部署入口。

### GitHub 同名第三方仓库

仓库：https://github.com/wyn-pixelx/mineru-chem

该仓库不是 OpenDataLab 官方仓库，而是个人维护的 `MinerU 2.5.4 with chemical recognition` 分支。它在旧版 MinerU pipeline 中加入 ChemDet 和 MolScribe，并将识别结果写成 `<smiles>` 标记。当前管线使用的是仓库内固定的 MinerU 3.4.4，因此直接替换存在以下问题：

- 通用解析器从 3.4.4 回退到 2.5.4；
- 实现不是技术报告中的 CARBON 和完整五模块 MinerU.Chem；
- 模型权重来自个人 ChemDet 仓库和 MolScribe，不能等同于官方报告性能；
- 未提供与当前 Stage04 相同的批量、重试、质量门控和输出兼容性保证；
- 需要新增约 15 GB 环境与模型，并重新验证 CPU/GPU 吞吐。

因此，名称相似不足以证明它是官方 MinerU.Chem，也不足以承担生产替换。

## Stage04 适配边界

未来满足以下条件后，可增加 `mineru_chem.enabled` 可选配置，但仍保留标准 MinerU 主解析。它的定位是辅助 OCR，失败或低置信度时不影响正文结果：

1. 有可自动部署的官方本地实现，或有文档化、可批量调用的官方 API。
2. 标准 MinerU 先生成全文 Markdown/content list，MinerU.Chem 只读取页面图片与布局区域。
3. 化学增强失败不得使正文解析失败；结果单独缓存并支持 resume。
4. 结构化输出至少包含文档、页码、区域、SMILES/MolFile、反应物/产物映射、置信度和模型版本。
5. 在独立化学论文集上验证正文质量不退化、结构识别准确率、单页耗时、显存/内存和失败恢复。
6. Stage05 只能把化学结构结果当补充证据，不能用低置信度 OCSR 结果覆盖论文原文。

## 当前决定

- 保持 Stage04 使用 MinerU 3.4.4。
- 将 MinerU.Chem 视为可选的 `chemistry_ocr` 后处理，不作为主解析器替换。
- 不安装、不提交、也不依赖第三方 `wyn-pixelx/mineru-chem`。
- 不因 MinerU.Chem 尚不可部署而阻塞 Stage02/03 修正和新的 Stage00-05 批处理。
