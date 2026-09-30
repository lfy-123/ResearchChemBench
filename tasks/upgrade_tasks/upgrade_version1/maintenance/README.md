# 第一批离线维护检查

`check_batch1.py` 只检查本批 12 包的结构、运行时适配、公开导出、模式一致性、历史快照哈希及公开提交契约。使用的合成格式样例只写入临时目录并随检查删除，不是科学结果，不进入任务包。

在仓库根目录运行：

```bash
.envs/researchchembench/bin/python tasks/upgrade_tasks/maintenance/check_batch1.py
```

检查通过后更新上级 `batch1_validation_report.json`。不运行量化计算，不调用 LLM judge，不改动 final/hold，也不自动修改任务包或重建包哈希。

任务包应显式通过 `TaskRepository(roots=[Path('tasks/upgrade_tasks')])` 加载，仅用于此批开发/先导；本次没有变更默认任务发现目录或部署正式题库。修改任何包内容后需用仓库 `package_payload_entries` 和 `package_content_hash` 更新对应 manifest，并同步批次清单；不应通过关闭校验绕过哈希。

维护检查不能替代各包 `evaluation/reference_validation_plan.md` 所列真实参考验证。正式语义评分、数值容差校准和科学通过认定仍待完成。
