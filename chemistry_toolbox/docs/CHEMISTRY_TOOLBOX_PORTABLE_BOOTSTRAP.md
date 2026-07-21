# 化学工具箱自动配置与可迁移部署

本文档说明如何把当前 ResearchChemBench 化学工具箱尽可能精确地迁移到另一台服务器。自动化方案由两部分组成：

- `capture_portable_toolbox_lock.py`：在维护机器上读取真实安装状态，生成平台锁定清单；
- `bootstrap_chemistry_toolbox.sh`：在目标机器上创建缺失环境、校验已有环境、迁移大型资源并执行工具箱验证。

这套机制不会把所有软件塞入一个 Conda 环境，也不会把科学工作流固定下来。它只复现 MCP 后端运行环境；智能体仍然看到完整 Action/Backend 目录，并自主选择 Action、Backend、参数和调用顺序。

当前提交的 `linux-64` 清单包含 42 个记录：39 个精确 Conda 环境和 3 个资源型运行目录；同时登记了 48 个当前必需资源和 10 个需要许可、接口条件或人工决策的项目。

## 1. 锁定范围

锁定清单位于：

```text
chemistry_toolbox/environment/locks/
└── linux-64/
    ├── manifest.json
    ├── core/
    │   ├── conda-explicit.txt
    │   ├── pip-requirements.txt
    │   └── pip-lock.json
    └── <其他环境>/
        ├── conda-explicit.txt
        ├── pip-requirements.txt
        └── pip-lock.json
```

各层的可复现保证如下。

| 层级 | 锁定方式 | 迁移保证 |
|---|---|---|
| Conda 包 | 完整构建 URL、build、平台和包文件 SHA-256 | 在 `linux-64` 上恢复完全相同的 Conda 构建 |
| pip 包 | 以运行中 Python 的 `pip list` 为准锁定名称和版本 | 避免只依赖可能陈旧的 Conda `pypi_0` 元数据 |
| 项目代码 | 记录 Git commit，项目包按 `--no-deps --editable` 重新安装 | 后端始终使用目标 checkout 的代码 |
| 工具箱配置 | 对 MCP profile、辅助环境、软件清单和资源清单计算 SHA-256 | 防止用旧锁恢复已经改变的 Backend/资源配置 |
| 模型、参数库和关键程序 | 记录路径、版本、存在性以及已登记校验和 | 迁移后检查模型、赝势、DFTB 参数和关键二进制是否完整 |
| 手工/许可项目 | 在 manifest 中单独列出，不自动下载 | 避免绕过许可证、账号或人工审批 |

少量 pip 包可能在原环境中留下构建机临时 `file://` 路径。非 editable 包会转换成相同运行时版本的索引依赖，并在 `pip-lock.json` 中标记 `byte_identical_source=false`；真正的本地 editable 依赖如果不在仓库内，则作为不可迁移阻塞项报告，不会静默替换。

## 2. 在维护机器上刷新锁

必须使用已经配置好的核心环境运行，因为清单生成器需要 PyYAML：

```bash
cd /path/to/ResearchChemBench
.toolbox_env/bin/python \
  chemistry_toolbox/scripts/capture_portable_toolbox_lock.py
```

常用选项：

```bash
# 只刷新指定环境
.toolbox_env/bin/python chemistry_toolbox/scripts/capture_portable_toolbox_lock.py \
  --environments core,services,quantum

# 同时对配置引用的关键可执行文件计算 SHA-256；大型文件较多时会更慢
.toolbox_env/bin/python chemistry_toolbox/scripts/capture_portable_toolbox_lock.py \
  --hash-critical-assets

# 指定 Conda 可执行文件或输出目录
.toolbox_env/bin/python chemistry_toolbox/scripts/capture_portable_toolbox_lock.py \
  --conda /path/to/conda \
  --output-root chemistry_toolbox/environment/locks
```

刷新后应审查并提交整个 `chemistry_toolbox/environment/locks/linux-64`。软件环境发生实质变化时，应重新生成全部环境，而不是只修改手写依赖列表。

## 3. 校验当前服务器

以下命令只读检查，不创建或删除环境：

```bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --verify-only \
  --report /tmp/researchchem-bootstrap-status.json
```

它会检查：

1. 主机平台、CPU 指令集和锁定平台是否兼容；
2. 配置文件是否与生成锁时一致；
3. 每个 Conda 环境的精确构建集合；
4. 每个 pip 安装包的运行时版本和 `pip check` 是否相对源环境退化；
5. 必需软件、模型和科学数据是否存在且校验和正确；
6. Action/Backend 注册结构是否有效。

更完整但耗时更长的后端 profile 与 MCP smoke：

```bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --verify-only \
  --full-verify \
  --profile-timeout 900 \
  --report /tmp/researchchem-bootstrap-full-status.json
```

## 4. 部署到新服务器

目标机器至少需要：

- Linux x86-64；
- Python 3.10 或更高版本，用于启动标准库 bootstrap；
- Conda、Mamba 或兼容的 Conda 环境管理器；
- 足够的磁盘空间保存全部隔离环境和大型资源；
- 对当前 AVX2 ORCA 和 AVX-512 NAMD 构建兼容的 CPU，或者明确禁用不兼容后端。

先复制或 checkout 与锁定清单相符的仓库代码，然后执行：

```bash
cd /new/path/ResearchChemBench
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --asset-source /old/path/ResearchChemBench \
  --asset-mode copy \
  --continue-on-error \
  --report /tmp/researchchem-bootstrap-status.json
```

默认行为是：

- 环境不存在：按精确锁创建；
- 环境已存在：只校验，不修改；
- `.software_cache`、`.model_cache` 和 `download`：合并复制，不删除目标已有文件；
- 资源就绪后：创建必要的可执行文件链接和运行时 hook；
- 不修改用户的全局 Conda `envs_dirs`，也不删除用户环境注册记录；
- 不复制 `config.local.env`、API key、许可证服务器凭据或其他密钥。

如果目标服务器可以直接访问原始大型资源，并且不希望复制，可以链接：

```bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --asset-source /shared/ResearchChemBench-assets \
  --asset-mode link
```

链接模式要求目标的三个资源根目录尚不存在，避免脚本替换已有数据。

若要删除并精确重建所有受管 Conda 环境，必须显式给出：

```bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --asset-source /old/path/ResearchChemBench \
  --recreate
```

`--recreate` 只允许处理 `.toolbox_env` 和 `.tool_envs/*`，不会删除其他路径。

## 5. 部分环境与 dry-run

预览操作而不写入：

```bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --dry-run \
  --asset-source /old/path/ResearchChemBench
```

只创建或检查部分环境：

```bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --environments core,services,quantum
```

部分环境模式不会执行面向完整工具箱的最终配置和全目录验证。环境 ID 来自 `manifest.json`，不是 Action 或 Backend 名称。

## 6. 离线恢复

Conda 锁包含官方构建 URL 和 SHA-256。在线恢复时可直接精确下载。完全离线的新服务器还必须提前准备两类缓存：

1. 锁中所有 `.conda`/`.tar.bz2` 包已经存在于目标 Conda 的 package cache；
2. 所有 `pip-requirements.txt` 对应 wheel 已放入 wheelhouse。

然后运行：

```bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh \
  --offline \
  --wheelhouse /shared/researchchem-wheels \
  --asset-source /shared/ResearchChemBench-assets
```

`--offline` 会给 Conda 增加离线模式，并让 pip 使用 `--no-index`。它不会凭空生成缺失的包文件；若 package cache 或 wheelhouse 不完整，报告会明确指出失败环境。在线安装成功后，Conda 自身的 package cache 也可作为后续同平台离线部署的来源。

## 7. 许可软件和人工边界

下列内容不会由脚本从互联网自动获取：

- ORCA、Gaussian、GAMESS、AMBER、CHARMM、Schrödinger、VASP POTCAR 等受许可或需注册的内容；
- MATLAB/EasySpin 所需合法许可证或许可证服务器配置；
- Materials Project 等服务的 API key；
- 配置中已经按操作者要求禁用的软件。

这些内容可以由操作者合法地放入源机器相应缓存，再由 `--asset-source` 复制或链接。清单只记录路径和可公开提交的校验信息，不提交软件本体、模型权重或凭据。

## 8. 平台与 ABI 限制

当前精确锁是 `linux-64` 平台锁，不是跨操作系统依赖描述。macOS、Windows、ARM64 或不同 GPU/CUDA 栈必须重新建立并测试独立平台锁。

此外还要注意：

- 当前 ORCA 包使用 AVX2；当前 NAMD 默认指向 AVX-512 构建；
- 某些源码编译程序可能依赖源主机的 glibc、OpenMPI、Fortran/C++ runtime 或 RPATH；
- GPU 后端还受 NVIDIA driver/CUDA 兼容性约束；
- `--allow-cpu-mismatch` 只适合明确不调用相关 Backend 的部署，它不会让不兼容二进制变得可运行。

因此，“依赖安装成功”之后仍要运行 profile smoke。锁文件保证版本与构建来源，运行时审计负责发现硬件和 ABI 差异。

## 9. 推荐维护流程

每次升级、增加或删除软件后按以下顺序处理：

1. 在维护服务器上完成软件安装和 Action/Backend 测试；
2. 运行全部环境锁定生成器；
3. 运行 `bootstrap_chemistry_toolbox.sh --verify-only`；
4. 审查锁差异，确认没有凭据、临时主机路径或意外依赖；
5. 提交代码、配置和平台锁；
6. 在一台空白同平台服务器上至少做一次真实恢复与 `--full-verify`；
7. 把许可软件、模型和数据的受控副本独立备份，不纳入 Git。

这套流程能够自动处理可公开重建的环境，并把无法自动化的许可证、凭据、硬件和私有资源问题转化为明确的部署报告，而不是在运行 Action 时才隐式失败。
