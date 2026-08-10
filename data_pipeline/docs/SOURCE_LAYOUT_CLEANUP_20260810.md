# 数据管线源码整理记录（2026-08-10）

## 目标

删除旧版和当前版并存的实现，将唯一现行流程按 Stage00-07 放到 `src/stages/`，并移除不再参与
运行、测试或维护的临时文件、兼容入口和历史报告。此次整理不改变 Stage02/03 的筛选政策。

## 源码迁移

- 将 `src/v2` 的当前配置、契约、模型客户端、prompt、runtime 和 pipeline 移到 `src/` 顶层。
- 将当前阶段实现分别迁到 `stage00_remote_corpus` 至 `stage07_task_judge`。
- Stage01 合并论文清点、去重、正文/SI 归组、补充材料获取和低成本解析。
- Stage04 MinerU 实现从 Stage03 文件中完整拆出，Stage03 只保留软件与资源门控。
- 删除旧 `src/agents`、`src/orchestration`、旧阶段目录和 `src/v2` 兼容层。
- CLI 只保留 `run`、`prepare-remote-corpus`、`sandbox` 和 `mineru-queue`。

## 文件清理

- 删除旧批处理脚本、逐阶段兼容入口和重复 Xinghe 示例脚本。
- 删除旧配置文件和本机专用 `config.*.local.json`，保留一个 `config.example.json`。
- 删除 `runs/`、`.tmp/`、`.tools/`、`.stage03_llm_runtime/`、测试缓存和重复 MinerU 脚本。
- 删除过时设计草案和一次性运行报告，重新建立当前架构和 prompt 职责文档。
- 保留 `.envs/`、`.model_cache/`、`third_party/`、`datasets/` 和 `config.local.env`，因为它们是
  当前运行所需的本地资产；通过 `.gitignore` 排除。

## 兼容性

旧配置布局和旧 Python 导入路径不再支持。入口改为：

```bash
python -m src.cli run --config config.local.json
```

配置必须符合 `researchchembench-data-pipeline/v2` 契约，但该字符串只表示数据契约版本，不代表
源码仍位于 `src/v2`。
