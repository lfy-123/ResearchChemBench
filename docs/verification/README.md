# Verification documents

- [Heterobiaryl P(V) 六任务运行验证台账](HETEROBIARYL_PV_SIX_TASK_VERIFICATION_20260722.md)：任务指令、匿名数据、Agent/Judge token、Scientific MCP/native 工具轨迹、Agent 结果、评分与参考答案。
- [Heterobiaryl P(V) 自主计算六任务最终验证报告](HETEROBIARYL_PV_AUTONOMOUS_COMPUTATION_VERIFICATION_20260722.md)：清洗后的原始输入边界、最终有效运行、完整受管与非受管轨迹、客观问题修复、逐题科学审计及参考差距。
- [当前化学工具箱能力目录](CHEMISTRY_TOOLBOX_CURRENT_CAPABILITY_CATALOG_20260722.md)：106 个 Actions、76 个 BackendSpecs、106 项软件/程序/接口 inventory、原生命令、分析 runtimes、科学资源和论文筛选建议。

上述文档可通过以下命令从当前 Catalog 和已保存 workspace 重新生成：

```bash
.toolbox_env/bin/python scripts/generate_verification_docs.py
.toolbox_env/bin/python scripts/generate_heterobiaryl_autonomous_verification.py
```
