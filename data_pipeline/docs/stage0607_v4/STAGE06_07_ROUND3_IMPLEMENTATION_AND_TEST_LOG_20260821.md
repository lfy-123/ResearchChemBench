# Stage06/07 第3轮实现与回归记录

日期：2026-08-21  
基线：`a7de708`（代码修复随后提交为下一版本）  
测试：`runs/stage06-07-v4-round3-deepseek10-concurrency10-20260821`

## 第3轮结果

- 10/10 CLI任务完成，`failed_count=0`。
- 9篇进入Stage07科学审计，8篇科学批准，1篇 Stage06 objective failure。
- 7篇 mechanical通过并发布，2篇 mechanical阻断。
- 第2轮遗留的 dotted field mapping 阻断已全部消失。

## 新发现

1. 一个通用 JSONPath 兼容问题：Ground Truth 使用 `$.stationary_points[*].id` 这类数组通配路径，旧 gate parser 不接受 `[*]`，造成两个纯路径语法 finding。——代码问题，已支持 wildcard。
2. 一个通用 JSON Schema 表达问题：自主模式用 `additionalProperties: {schema}` 描述按模型标签展开的对象，旧 gate只把 `true` 视为开放对象，错误报告字段缺失。——代码问题，已将 schema 对象型 `additionalProperties` 作为可观察的开放路径。
3. 第3轮剩余的两个阻断均由上述两类代码语义造成，不是科学审计结论，不需要 Stage07B。

## 代码修改

- `_jsonpath_tokens()` 支持 `[*]`。
- `_schema_path_status()` 支持 `additionalProperties` 为 schema 对象，并沿 wildcard/items继续解析。
- 新增 dotted/wildcard 回归测试。

## 验证

- Stage06/07专项：133 tests（本轮新增后相关筛选通过）。
- 全量：522 passed。

## 下一步

提交本轮版本后重新跑同10篇回归。若 mechanical阻断只剩真实缺文件/合同不闭合，说明 gate 的通用误报已清除；随后进入20篇扩大测试。Stage07B暂不实现。
