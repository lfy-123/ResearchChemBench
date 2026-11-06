# 新服务器接入 ARCHE：复用共享存储

入口：`scripts/install_arche_dependencies.sh`。本入口针对**新服务器与当前服务器共享同一存储及绝对路径**的场景，只安装新服务器缺少的系统软件，并检查共享依赖。不会安装、升级或重建 benchmark/ARCHE Python 环境，不执行 pip/Conda，不下载模型或内核，也不启动评估。

当前自动安装支持 **Ubuntu 22.04 / Linux x86_64**，与现有 QEMU C virtiofsd 部署一致。其他发行版可用 `--check` 查看缺项，但不会被自动认定为兼容。现有托管 QEMU 启动器要求在新服务器的 root 账户/容器中运行；不满足权限时脚本会明确报错。

## 已共享的内容

| 内容 | 当前共享位置或默认值 |
| --- | --- |
| benchmark 框架 | `.envs/researchchembench/` |
| 通用化学工具环境 | `.envs/general-modern-openmpi5/`；其他已有工具环境继续按 benchmark 配置使用 |
| ARCHE 客户端 / SDK | `.envs/arche-client/` |
| ARCHE / BGE 编码依赖 | `.envs/arche-benchmark/` |
| BGE-M3 权重 | `/inspire/hdd/global_user/lifangyuan-253108110077/Models/bge-m3` |
| guest 内核及模块 | `workspaces/arche_e2e_20260929/qemu/kernel/`，版本 `6.8.0-101-generic` |
| 原生 Codex 执行器缓存 | `workspaces/arche_e2e_20260928/uml/probe/codex_runtime/` |
| 科学软件、任务和结果 | 既有 `.software_cache/`、任务库及按论文组织的结果目录 |

脚本检查解释器是否可执行、实际导入是否成功、解释器软链接的最终目标是否也在共享根内，以及模型、内核模块和执行器文件是否存在。共享盘可访问不等于二进制在任何系统都兼容；检查失败会报告缺项，不通过重装共享环境解决。

系统安装清单是 QEMU、`qemu-system-common` 中的 C virtiofsd、OpenSSH、busybox-static、cpio、gzip/xz、C 编译工具、证书及基础系统工具。只通过 apt 安装缺少的包；所有包已存在时跳过 apt。使用仓库随附的原生 bwrap，不另换执行器版本。

## 在新服务器执行

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

# 一键安装当前服务器缺少的系统包，并检查共享环境。
# 已是 root 时直接用 bash；普通账户可使用 sudo -E bash。
bash scripts/install_arche_dependencies.sh
```

成功后会输出该服务器专属配置的完整路径。按输出执行 `source`，然后检查部署：

```bash
source /完整路径/.runtime_cache/arche/hosts/<服务器标识>/runtime.env
bash scripts/run_arche_gpt56_eval.sh --check

# 环境检查通过后再启动所选评估任务。
ARCHE_EVAL_PAPER_SEARCH=true \
bash scripts/run_arche_gpt56_eval.sh --paper paper_2f2aa11ea61a32bb
```

请使用脚本打印的实际配置路径，不把尖括号占位符直接粘贴执行。配置不含 API 密钥；现有私有 API 配置继续共享。配置中的 `ARCHE_EVAL_DEPLOYMENT=managed` 让新服务器建立自己的 QEMU、BGE、SSH、代理服务；不会尝试操作旧服务器的服务进程。

不同服务器生成各自的路径配置；其中 STATE_DIR 仅用作预检和旧布局兼容目录：

```text
.runtime_cache/arche/hosts/<hostname+machine-id摘要>/
    runtime.env
    setup_report.json

workspaces/arche_gpt56/.runtime/hosts/<hostname+machine-id摘要>/
    deployment/
    launch.lock
    active_run.json
```

Python 环境、权重、任务和结果继续共享。2026-10-06 起，每次新评估的部署自动放在该次结果目录的 `.runtime/deployment/`，独占服务 PID、SSH 密钥、端口及 guest 控制文件。不同服务器、不同终端可并行评估不同任务。后续使用 `--status/--cancel/--down --run-dir DIR` 定位任务；停止和恢复在原主机执行，无需再手工匹配端口和 STATE_DIR。

## 只检查或自定义路径

```bash
# 只检查，不安装系统包，也不写配置。
bash scripts/install_arche_dependencies.sh --check

# 仅打印计划：不安装、不加载模型库、不写文件。
bash scripts/install_arche_dependencies.sh --dry-run

# 共享盘首次读取较慢时延长每个 Python 环境的导入等待。
bash scripts/install_arche_dependencies.sh --check --probe-timeout 300
```

路径可用 `--shared-root`、`--env-root`、`--bge-model`、`--kernel-root`、`--kernel-version`、`--runtime-cache` 覆盖。这些指向既有共享文件，不触发创建 Python 环境或下载。只有安装模式检查全部通过时才生成 `runtime.env`；失败记录为 `blocked`。

依赖检查不调用模型 API、不计算化学任务，也不代表 API 余额、网络出口、全部科学软件或正式评分已验证。后续 `run_arche_gpt56_eval.sh --check` 会创建独立部署并检查 guest 沙箱、BGE、宿主通道等，完成后自动关闭测试服务。具体科学软件仍按 benchmark 的实际运行检查。

## 验证范围

开发时在当前服务器执行只读检查和无副作用的计划预览，并用离线测试验证系统包安装边界、共享环境不重装、缺项失败、每服务器配置隔离、路径转义、重复执行及 Codex 结果目录保护。没有在当前服务器执行 apt 安装，没有重建共享环境，没有启动新的付费评估。新服务器上的真实 apt 安装及完整 QEMU 冷启动需在目标服务器执行以上命令后确认。

2026-10-04 本机验证结果：`--check` 全部通过，7 项安装边界测试通过，shell 语法检查通过。共享盘首次导入曾触发 60 秒超时，默认已调整为每环境 180 秒并通过复查；这不触发任何重装。
