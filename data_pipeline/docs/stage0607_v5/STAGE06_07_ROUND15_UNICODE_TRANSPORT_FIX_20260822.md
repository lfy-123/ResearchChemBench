# Stage06/07 v5 Round 15 Unicode transport 修复

日期：2026-08-22

基线：`1120aaa`

## 1. 触发证据

Round 14 的 `paper_51a03695e1ccb105` 在 Agent 启动前进入 `objective_failure_retryable`：

`UnicodeEncodeError: 'utf-8' codec can't encode characters ... surrogates not allowed`

直接检查 immutable SI PDF 发现，pypdf 在第 11 页把 supplementary-plane 数学字母作为 UTF-16 surrogate code units 返回。Stage06 的 `_extract_pdf_layout_materials()` 未规范化这些 code units，写 `pypdf_layout.txt` 时失败。

这是确定的 Stage06 文件运输 bug，不是论文科学问题、Prompt 问题或模型能力问题。

## 2. 修复

- 新增 `_normalize_unicode_scalar_text()`：合法 UTF-16 surrogate pair 合并成 Unicode scalar；孤立 surrogate 替换为 `U+FFFD`。
- 仅在 Stage06 自己调用 pypdf 生成 layout 文本的输入边界应用规范化。
- 不修改 Stage00–05，不改写源 PDF，不加入论文/分子/软件规则。
- Stage06 implementation version 更新为 `v13-unicode-safe-source-layout-20260822`。

## 3. 验证

- 新增 surrogate pair + isolated surrogate 回归测试；
- 全量测试：`553 passed`；
- 用触发问题的原 SI PDF 直接重跑 `_extract_pdf_layout_materials()`：成功生成 95,686 字符 UTF-8 layout，无 surrogate code unit，并正常生成 derived materials/evidence；
- `git diff --check`：通过。

Round 14 的其余 worker 已在修复前加载代码，继续保持其原始测试版本。批次完成后单独重跑失败论文，验证它能越过输入准备并进入正常 Stage06A 科学处理。
