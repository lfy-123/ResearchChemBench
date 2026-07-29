# ResearchChemBench 资源缓存迁移与根目录审计

日期：2026-07-29
分支：`codex/consolidate-toolbox-envs-20260729`

## 1. 结论

- 当前代码和资源注册表已不再依赖仓库根目录的 `download/`。
- 仍被工具箱使用的伪势、DFTB 参数、ORCA 安装包和 GNINA 二进制均已复制到 `.software_cache/`，并改为仓库相对路径。
- 原 `download/` 完整保留，未删除；它现在主要是历史下载包、重复归档和下载器快照。
- 按用户最新要求，没有重命名任何 Conda 环境目录；继续保留 `.toolbox_env`、`.tool_envs` 和 `.tool_envs_merged`。
- 资源注册深度校验为 27/27 通过，真实科学计算冒烟测试为 24/24 通过。

## 2. 已迁移的有效资源

| 资源 | 原位置 | 当前有效位置 |
|---|---|---|
| Quantum ESPRESSO SSSP efficiency/precision | `download/qe_pseudos/` | `.software_cache/resources/qe_pseudos/` |
| SIESTA PseudoDojo PSML | `download/nc-sr-05_pbe_standard_psml*` | `.software_cache/resources/siesta_pseudos/` |
| ABINIT PseudoDojo PSP8 | `download/abinit_pseudos/` | `.software_cache/resources/abinit_pseudos/` |
| DFTB+ 3ob、matsci 参数 | `download/dftb_params/` | `.software_cache/resources/dftb_params/` |
| ORCA 6.1.1 安装包 | `download/orca_6_1_1_*.run` | `.software_cache/orca/download/` |
| GNINA 1.3.3 | `download/software/gnina/` | `.software_cache/gnina/1.3.3/` |

相关注册信息已同步到：

- `chemistry_toolbox/config/toolbox_resources.json`
- `chemistry_toolbox/environment/locks/linux-64/manifest.json`
- `chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.py`
- `chemistry_toolbox/scripts/capture_portable_toolbox_lock.py`

`download/` 不再属于便携锁允许的资产根目录。配置文件中的 `download/` 字样仅剩 `.software_cache/.../download/...` 这种缓存内部子目录名，不再指向仓库根目录的 `download/`。

## 3. 验证结果

| 检查 | 结果 |
|---|---:|
| 科学资源深度验证 | 27/27 通过 |
| 工具箱结构验证 | 通过；104 个科学 Action、77 个后端、56 个原生软件可发现 |
| 真实科学资源计算 | 24/24 通过 |
| 资源与环境相关单元测试 | 38/38 通过 |
| 现有便携锁核验 | 43/43 环境或外部运行时通过 |
| 三层 MCP 端到端冒烟 | 通过；Action、原生软件指南、通用程序、持久任务、Artifact 与 trace 链均正常 |

真实计算覆盖了 QE、SIESTA、ABINIT、DFTB+、GNINA、ORCA、NequIP、Allegro、DeePMD 和 VASP，证明迁移后的资源路径不仅“文件存在”，而且能够被后端真实读取并返回结果。

验证时同时修复了一项维护问题：资源冒烟脚本仍向公共请求模型传递已取消暴露的 `walltime_seconds`；现已删除，由工具箱统一超时策略控制。

## 4. 根目录审计

以下目录没有删除。分类中的“可清理”只表示当前代码运行不依赖，仍应在人工确认数据价值后处理。

| 目录 | 当前用途 | 判断 |
|---|---|---|
| `.git`、`.github` | Git 历史与自动化配置 | 必须保留 |
| `assets`、`chemistry_toolbox`、`docs`、`eval_configs`、`evaluation`、`scripts`、`tasks`、`tests` | 项目代码、任务、文档和测试 | 必须保留 |
| `.software_cache`、`.model_cache` | 软件、伪势、参数和模型缓存 | 迁移所需，必须保留 |
| `.toolbox_env` | 当前 ResearchChemBench 主环境 | 必须保留 |
| `.tool_envs_merged` | 六个合并后的工具环境 | 当前目标布局，必须保留 |
| `.tool_envs` | 原 40 个工具环境 | 旧环境备份；暂时保留，待用户确认后再处理 |
| `.conda_envs` | 指向旧环境和主环境的 Conda 名称别名，约 19 KB | 可重建；手工按环境名调用时仍可能使用，不建议立即删除 |
| `.venv` | 主环境缺失时脚本使用的 Python fallback，约 451 MB | 当前 `.toolbox_env` 存在，因此不是主路径；可在取消 fallback 后清理 |
| `.pytest_cache` | pytest 缓存，约 132 KB | 可安全重建 |
| `researchchembench.egg-info` | editable install 生成的元数据，约 131 KB | 可安全重建 |
| 根目录 `_tool_results`、`_tool_artifacts` | 在仓库根目录运行工具时产生的结果和 provenance，约 2.2 MB | 代码不依赖，但清理会丢失历史证据 |
| 根目录 `outputs` | 临时运行输出，当前约 1.5 KB | 可重建；运行任务时不要删除 |
| `workspaces` | 历史评估结果、轨迹和部分验证基线 | 不是软件依赖，但部分报告/任务构建脚本引用其中的已验证结果，不可整体删除 |
| `download` | 历史下载缓存和重复归档，约 23 GB | 当前代码已不依赖；可在核对备份和许可要求后单独归档或删除 |

## 5. 后续人工决策

建议优先处理空间占用最大的 `download/`，但本次不删除。若以后决定清理，应先确认：

1. `.software_cache` 与 `.model_cache` 已纳入迁移或备份清单；
2. ORCA、VASP 等许可软件的原始安装介质是否需要离线留档；
3. `download/public_downloads_twice/` 中是否存在尚未登记、但希望保留的原始来源快照；
4. 在新服务器完成一次 27/27 资源校验和 24/24 真实计算复验。
