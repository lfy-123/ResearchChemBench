# Verification documents

- [Heterobiaryl P(V) 六任务运行验证台账](HETEROBIARYL_PV_SIX_TASK_VERIFICATION_20260722.md)：任务指令、匿名数据、Agent/Judge token、Scientific MCP/native 工具轨迹、Agent 结果、评分与参考答案。
- [当前化学工具箱能力目录](CHEMISTRY_TOOLBOX_CURRENT_CAPABILITY_CATALOG_20260722.md)：106 个 Actions、76 个 BackendSpecs、106 项软件/程序/接口 inventory、原生命令、分析 runtimes、科学资源和论文筛选建议。

两份主文档可通过以下命令从当前 Catalog 和已保存 workspace 重新生成：

```bash
.toolbox_env/bin/python scripts/generate_verification_docs.py
```
