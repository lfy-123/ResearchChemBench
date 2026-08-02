# Stage 03-05 重构实施记录

## 1. 目标

按照 `docs/modifiy/STAGE_03_05_REDESIGN_PLAN.md` 完整替换语料管线原有的第三、四、五阶段：

- Stage 03：Softcite 核心软件覆盖门控。
- Stage 04：单一本地通用模型 API 的完整计算过程门控。
- Stage 05：GROBID Quantities 与关键词解析器结合的明确资源上限门控。

旧的综合分类、低成本混合筛选和 Seed 审计不再出现在语料主流程中。

## 2. Git 基线

实施前先固定前序工作：

- `c97d969 feat(data-pipeline): replace cheap PDF extraction with GROBID`
- `ad1f47b docs(data-pipeline): specify stage 03-05 redesign`

基线验证：

- `python -m unittest discover -s tests -v`：48 项通过。
- `ruff check src scripts tests`：通过。

## 3. 实施清单

- [x] 固定并部署 Softcite 源码版本。
- [x] 固定并部署 GROBID Quantities 源码版本。
- [x] 实现 Stage 03 客户端、软件规则和三类路由。
- [x] 实现 Stage 04 证据构建、API 调用和严格响应校验。
- [x] 实现 Stage 05 资源召回、双解析器、归一化和上限判定。
- [x] 删除语料主流程中的旧 Stage 03-05。
- [x] 更新 Stage 06 MinerU 队列输入。
- [ ] 更新配置、脚本、日志、阶段索引和 README。
- [x] 完成单元测试。
- [ ] 完成服务集成测试。
- [ ] 对 Stage 02 的 17 篇正式论文完成监督运行和人工复核。
- [ ] 修复真实运行中发现的问题并完成回归。
- [ ] 编写最终测试结果分析报告。

## 4. 实施日志

### 2026-08-02：建立重构基线

- 确认 Stage 02 已保存 17 篇唯一正式论文的 GROBID TEI、结构化记录和正文文本。
- 确认原始 38 份 PDF 中排除了 14 份附件和 7 份重复正文。
- 确认第三方源码统一放置在 `data_pipeline/third_party`，第三方源码本体不提交到主仓库。
- 确认用户允许删除并完全替换原 Stage 03、Stage 04、Stage 05 主流程代码。

后续每个实现、测试、故障和修复将在本节追加记录。

### 2026-08-02：固定第三方版本并适配主环境

- Softcite 固定到 `c7c83852a3cad8f2d9d07ce3de6fbe852e23c19a`。
- GROBID Quantities 固定到 `d0d55592f4d0ddbe6a549e06613349adaa2d1cd7`。
- DeLFT 固定到 `d8505592c38058b9b0abbde14d4ddedff3ad7d0f`。
- 三个 GitHub checkout 全部位于 `data_pipeline/third_party`，主仓库只追踪固定 commit、补丁和 bootstrap 脚本。
- 主环境保持 `transformers==4.57.3`、`torch==2.6.0+cu124` 和 `numpy==1.26.4`；DeLFT 使用 `--no-deps` 安装，避免按其旧依赖声明降级主环境。
- 安装 TensorFlow 2.17.1、`tf_keras` 2.17.0、JEP 4.3.1 和 DeLFT 所需辅助包。
- 稳定版 `tensorflow-addons` 与 Keras 3 不兼容，改用官方 `tfa-nightly==0.23.0.dev20240415222534`。
- Softcite 的旧 `asm:asm:3.3.1` 与当前依赖图中的 ASM 9 冲突，补丁删除旧 ASM 显式依赖。
- Softcite 的软件实体模型由 Wapiti 切换到官方 DeLFT BERT；软件使用上下文仍由 Softcite 二分类模型判断。
- 发现 `context_shared_bert` 权重文件内容损坏，使用 `HF_ENDPOINT=https://hf-mirror.com` 重新下载，并在 bootstrap 中加入 `h5py` 完整性校验。

### 2026-08-02：实现并替换 Stage 03-05

- Stage 03 新增 Softcite 客户端、自动服务生命周期、TEI 软件抽取、显式别名补召回、核心/辅助角色规则、工具箱直接覆盖和能力等价路由。
- Softcite NER 在样例论文中漏掉 LOBSTER。为避免已知工具静默漏检，增加工具箱软件别名在 TEI 中的确定性召回；召回后仍调用 Softcite `characterizeSoftwareContext` 判断是否为作者实际使用。
- Stage 04 从 GROBID TEI 构建标题、摘要、核心软件证据、方法、结果和结论压缩文本，只调用一个 OpenAI 兼容 JSON API。
- Stage 04 对 `complete` 放行，对 `incomplete` 和 `uncertain` 淘汰；模型未配置、API 调用失败或响应无法校验时记录 `skipped`/`skipped_error` 并放行，不执行规则回退。
- Stage 05 对资源关键词命中的句子调用 GROBID Quantities，同时用严格关键词解析器补充 CPU、GPU、内存和运行时间。
- GROBID Quantities 实测能识别时间，但不能稳定将 `1024 CPU cores` 绑定为 CPU 核数，因此关键词解析器是必要补充。
- Stage 05 只淘汰明确属于本文实际计算且超过上限的数值；平台容量、物理模拟时长、含糊信息和无资源信息默认放行。
- 删除 `corpus_classify.py`、`seed_audit.py`、旧 `pre_screen_documents()` 及对应 CLI 子命令。
- Stage 09 改为非筛选性的 MinerU 结果合并，Stage 10 改为 extraction-ready 快照，不再重新执行旧分类或旧预筛选。
- Stage 06 MinerU 队列只接收 Stage 05 放行论文。

### 2026-08-02：基线测试

- 新增 Stage 03 三类路由、背景/辅助软件、Stage 04 完整/不完整/跳过/调用失败、Stage 05 资源边界和物理时长排除测试。
- `python -m ruff check data_pipeline/src data_pipeline/tests`：通过。
- `python -m unittest discover -s data_pipeline/tests -q`：49 项通过。
- 下一步执行自动启动/停止服务的集成测试和 17 篇正式论文监督运行。
